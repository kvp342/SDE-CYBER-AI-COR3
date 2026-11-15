"""secrag: a small, testable RAG assistant for security notes, with prompt-injection defences."""
from .assistant import Assistant, Result
from .llm import AnthropicLLM, StubLLM, make_llm
from .store import Store

__all__ = ["Assistant", "Result", "AnthropicLLM", "StubLLM", "make_llm", "Store"]
