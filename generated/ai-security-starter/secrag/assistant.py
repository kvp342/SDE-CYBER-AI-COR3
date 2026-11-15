"""The RAG assistant: retrieve, (optionally) defend, ask the model, (optionally) check the output."""
from dataclasses import dataclass, field

from . import defence


@dataclass
class Result:
    answer: str
    sources: list
    blocked: bool = False
    reasons: list = field(default_factory=list)


class Assistant:
    def __init__(self, store, llm, defended=True, k=3):
        self.store, self.llm, self.defended, self.k = store, llm, defended, k

    def ask(self, question):
        if self.defended:
            reasons = defence.scan_input(question)
            if reasons:
                return Result("I can't help with that request.", [], True, reasons)
        hits = [c for _, c in self.store.search(question, self.k)]
        reasons = []
        if self.defended:
            clean = []
            for c in hits:
                text, flagged = defence.sanitise_chunk(c.text)
                if flagged:
                    reasons.append(f"sanitised {c.source}")
                clean.append(type(c)(c.source, c.title, text))
            hits = clean
        system, user = defence.build_prompt(question, hits, self.defended)
        answer = self.llm.complete(system, user)
        if self.defended:
            answer, out_reasons = defence.check_output(answer)
            reasons += out_reasons
        return Result(answer, sorted({c.source for c in hits}), False, reasons)
