"""LLM 工厂测试。"""

import unittest
from unittest.mock import patch

from core.llm.factory import DisabledProvider, get_llm_provider
from core.llm.ollama_provider import OllamaProvider
from core.llm.openai_provider import OpenAIProvider


class LLMFactoryTestCase(unittest.TestCase):
    def test_backend_none(self) -> None:
        with patch("core.llm.factory.LLM_ENABLED", False):
            provider = get_llm_provider()
            self.assertIsInstance(provider, DisabledProvider)

    def test_backend_ollama(self) -> None:
        with patch("core.llm.factory.LLM_ENABLED", True), patch(
            "core.llm.factory.LLM_BACKEND", "ollama"
        ):
            provider = get_llm_provider()
            self.assertIsInstance(provider, OllamaProvider)

    def test_backend_openai(self) -> None:
        with patch("core.llm.factory.LLM_ENABLED", True), patch(
            "core.llm.factory.LLM_BACKEND", "openai"
        ):
            provider = get_llm_provider()
            self.assertIsInstance(provider, OpenAIProvider)


if __name__ == "__main__":
    unittest.main()
