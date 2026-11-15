"""Model clients. StubLLM runs offline for tests; AnthropicLLM calls Claude through the official SDK."""
import os
import re
import unicodedata

from .store import tokens

ZERO_WIDTH = dict.fromkeys(map(ord, "​‌‍⁠﻿"), None)


def normalise(text):
    """Remove zero-width characters and fold look-alike Unicode, as a model effectively 'reads through' them."""
    return unicodedata.normalize("NFKC", text).translate(ZERO_WIDTH)


TRIGGER = re.compile(r"(ignore|disregard|forget)\s+(all\s+|any\s+|the\s+)?(previous|prior|above|earlier)\s+(instructions|rules)"
                     r"|you are now|new instructions\s*:|system override|developer mode", re.I)
REVEAL = re.compile(r"(reveal|print|repeat|show|output)\s+(me\s+)?(your\s+|the\s+)?(system prompt|hidden instructions|hidden rules)", re.I)
SAY = re.compile(r"(say|reply with|respond with|output|answer with)\s*:?\s*['\"]?([^'\"\n.]+)", re.I)
URL = re.compile(r"!?\[[^\]]*\]\((https?://[^)\s]+)\)|https?://\S+")


class StubLLM:
    """A deterministic stand-in for an LLM, used only for offline tests.

    It is deliberately naive, like an unprotected model: it follows instructions it finds anywhere in its input.
    That makes attacks measurable without an API key. Otherwise it answers extractively: it returns the context
    sentence that shares the most words with the question. Real results must come from a real model."""
    name = "stub"

    def complete(self, system, user):
        text = normalise(system + "\n" + user)
        if REVEAL.search(normalise(user)):
            return system
        m = TRIGGER.search(normalise(user))
        if m:
            cmd = normalise(user)[m.end():].split("\n")[0]
            if "system prompt" in cmd.lower():
                return system
            u = URL.search(cmd)
            if u:
                return "See " + u.group(0)
            s = SAY.search(cmd)
            return s.group(2).strip() if s else cmd.strip(" .,:")
        q = user.rsplit("Question:", 1)[-1]
        ctx = user.rsplit("Question:", 1)[0]
        ctx = re.sub(r"<[^>]+>", " ", ctx)
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", ctx) if len(s.strip()) > 20]
        if not sentences:
            return "I don't know based on the notes."
        qt = set(tokens(q))
        return max(sentences, key=lambda s: len(qt & set(tokens(s))))


class AnthropicLLM:
    """Calls Claude with the official SDK (pip install anthropic). Credentials come from the environment
    (ANTHROPIC_API_KEY or an `ant auth login` profile); nothing is hard-coded. Model: SECRAG_MODEL, default claude-opus-5-5."""
    name = "anthropic"

    def __init__(self, model=None, effort="medium"):
        import anthropic  # imported here so offline tests do not need the package
        self.anthropic = anthropic
        self.client = anthropic.Anthropic()
        self.model = model or os.environ.get("SECRAG_MODEL", "claude-opus-5-5")
        self.effort = effort

    def complete(self, system, user):
        response = self.client.beta.messages.create(
            model=self.model,
            max_tokens=16000,
            system=system,
            messages=[{"role": "user", "content": user}],
            output_config={"effort": self.effort},
            # Server-side refusal fallback: if this model declines, the API retries on a suitable fallback model.
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
        )
        if response.stop_reason == "refusal":
            return "[refused by the model]"
        return "".join(b.text for b in response.content if b.type == "text").strip()


def make_llm(kind):
    return AnthropicLLM() if kind == "anthropic" else StubLLM()
