"""轻量路由测试。"""

import unittest
from unittest.mock import patch

from core.llm import LLMDecision
from core.router import CommandRouter


class FakeLLM:
    def __init__(self, decision: LLMDecision):
        self.decision = decision
        self.called = False

    def parse_intent(self, _: str) -> LLMDecision:
        self.called = True
        return self.decision


class RouterTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.router = CommandRouter()

    def test_router_synonyms(self) -> None:
        self.assertIn("浏览器", self.router.route("请帮我打开网页").response_text)
        self.assertIn("记事本", self.router.route("打开 notepad").response_text)
        self.assertIn("计算器", self.router.route("打开 calc").response_text)

    def test_exit_command(self) -> None:
        self.assertTrue(self.router.route("退出程序").should_exit)

    def test_wake_word_enabled(self) -> None:
        with patch("core.router.ENABLE_WAKE_WORD", True), patch(
            "core.router.WAKE_WORDS", ("助手",)
        ):
            router = CommandRouter()
            ignored = router.route("打开网页")
            self.assertTrue(ignored.ignored_by_wake_word)

    def test_rule_priority_over_llm(self) -> None:
        fake = FakeLLM(LLMDecision(action="get_time"))
        with patch("core.router.LLM_ENABLED", True):
            router = CommandRouter(llm_provider=fake)
            result = router.route("打开网页")
            self.assertEqual(result.source, "rule")
            self.assertFalse(fake.called)

    def test_backend_none_returns_unknown(self) -> None:
        with patch("core.router.LLM_ENABLED", False):
            router = CommandRouter()
            result = router.route("今天心情如何")
            self.assertIn("暂不支持", result.response_text)

    def test_llm_fallback_with_valid_json(self) -> None:
        fake = FakeLLM(LLMDecision(action="get_time", params={}))
        with patch("core.router.LLM_ENABLED", True):
            router = CommandRouter(llm_provider=fake)
            result = router.route("你能告诉我钟点吗")
            self.assertEqual(result.source, "llm")
            self.assertTrue(fake.called)

    def test_llm_service_unavailable_degrade(self) -> None:
        fake = FakeLLM(LLMDecision(error="ollama_unreachable"))
        with patch("core.router.LLM_ENABLED", True):
            router = CommandRouter(llm_provider=fake)
            result = router.route("帮我开下 github")
            self.assertIn("LLM 解析失败", result.response_text)


if __name__ == "__main__":
    unittest.main()
