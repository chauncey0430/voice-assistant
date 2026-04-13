"""LLM Provider 抽象。"""

from __future__ import annotations

from abc import ABC, abstractmethod

from core.llm.protocol import LLMDecision


class BaseLLMProvider(ABC):
    @abstractmethod
    def parse_intent(self, text: str) -> LLMDecision:
        """将用户文本解析为结构化动作。"""
