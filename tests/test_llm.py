"""LLM provider 与协议测试。"""

import unittest
from unittest.mock import patch

from core.llm.openai_provider import OpenAIProvider
from core.llm.ollama_provider import OllamaProvider
from core.llm.protocol import validate_decision


class LLMProtocolTestCase(unittest.TestCase):
    def test_validate_legal_json(self) -> None:
        decision = validate_decision({"action": "open_browser", "params": {}})
        self.assertEqual(decision.action, "open_browser")
        self.assertIsNone(decision.error)

    def test_validate_whitelist_block(self) -> None:
        decision = validate_decision({"action": "dangerous_shell", "params": {}})
        self.assertEqual(decision.error, "unsupported_action")

    def test_validate_invalid_json_field(self) -> None:
        decision = validate_decision({"action": 123, "params": {}})
        self.assertEqual(decision.error, "invalid_action_type")

    def test_openai_missing_api_key_degrade(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            provider = OpenAIProvider(enabled=True)
            decision = provider.parse_intent("帮我打开浏览器")
            self.assertEqual(decision.error, "openai_missing_api_key")

    def test_ollama_service_unavailable_degrade(self) -> None:
        provider = OllamaProvider(enabled=True)

        def _raise(_: str):
            raise RuntimeError("ollama_unreachable")

        provider._call = _raise  # type: ignore[method-assign]
        decision = provider.parse_intent("帮我开浏览器")
        self.assertIn("ollama_error", decision.error or "")


if __name__ == "__main__":
    unittest.main()
