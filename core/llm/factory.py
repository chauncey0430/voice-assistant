"""LLM Provider 工厂。"""

from __future__ import annotations

from config import (
    LLM_BACKEND,
    LLM_ENABLED,
    OLLAMA_ENABLED,
    OPENAI_ENABLED,
)
from core.llm.base import BaseLLMProvider
from core.llm.ollama_provider import OllamaProvider
from core.llm.openai_provider import OpenAIProvider


class DisabledProvider(BaseLLMProvider):
    def parse_intent(self, text: str):  # type: ignore[override]
        from core.llm.protocol import LLMDecision

        return LLMDecision(error="llm_disabled")


def get_llm_provider() -> BaseLLMProvider:
    if not LLM_ENABLED or LLM_BACKEND == "none":
        return DisabledProvider()

    backend = LLM_BACKEND.lower().strip()
    if backend == "ollama":
        return OllamaProvider(enabled=OLLAMA_ENABLED)
    if backend == "openai":
        return OpenAIProvider(enabled=OPENAI_ENABLED)
    return DisabledProvider()
