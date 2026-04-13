"""LLM 协议解析测试。"""

import unittest

from core.llm import LLMDecision, OllamaIntentParser


class LLMParserTestCase(unittest.TestCase):
    def test_validate_legal_json(self) -> None:
        parser = OllamaIntentParser(enabled=True)
        decision = parser._validate_decision({"action": "open_browser", "params": {}})
        self.assertEqual(decision.action, "open_browser")
        self.assertIsNone(decision.error)

    def test_validate_illegal_json_field(self) -> None:
        parser = OllamaIntentParser(enabled=True)
        decision = parser._validate_decision({"action": 123, "params": {}})
        self.assertEqual(decision.error, "invalid_action_type")

    def test_validate_unsupported_action(self) -> None:
        parser = OllamaIntentParser(enabled=True)
        decision = parser._validate_decision({"action": "open_app", "params": {}})
        self.assertEqual(decision.error, "unsupported_action")

    def test_service_unavailable_degrade(self) -> None:
        parser = OllamaIntentParser(enabled=True)

        def _raise(_: str) -> dict:
            raise RuntimeError("ollama_unreachable")

        parser._call_ollama = _raise  # type: ignore[method-assign]
        decision = parser.parse_intent("帮我开浏览器")
        self.assertIsInstance(decision, LLMDecision)
        self.assertIn("ollama_error", decision.error or "")


if __name__ == "__main__":
    unittest.main()
