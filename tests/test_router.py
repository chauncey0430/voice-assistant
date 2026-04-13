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

    def test_unknown_command(self) -> None:
        self.assertIn("暂不支持", self.router.route("帮我订个机票").response_text)

    def test_exit_command(self) -> None:
        self.assertTrue(self.router.route("退出程序").should_exit)

    def test_wake_word_enabled(self) -> None:
        with patch("core.router.ENABLE_WAKE_WORD", True), patch(
            "core.router.WAKE_WORDS", ("助手",)
        ):
            router = CommandRouter()
            ignored = router.route("打开网页")
            self.assertTrue(ignored.ignored_by_wake_word)

            wake_only = router.route("助手")
            self.assertIn("已唤醒", wake_only.response_text)

            executed = router.route("助手打开网页")
            self.assertIn("浏览器", executed.response_text)

    def test_rule_priority_over_llm(self) -> None:
        fake = FakeLLM(LLMDecision(action="get_time"))
        router = CommandRouter(llm_parser=fake)
        result = router.route("打开网页")
        self.assertEqual(result.source, "rule")
        self.assertFalse(fake.called)

    def test_llm_fallback_with_valid_json(self) -> None:
        fake = FakeLLM(LLMDecision(action="get_time", params={}))
        router = CommandRouter(llm_parser=fake)
        result = router.route("你能告诉我钟点吗")
        self.assertEqual(result.source, "llm")
        self.assertTrue(fake.called)
        self.assertIn("现在时间", result.response_text)

    def test_llm_invalid_json_or_error_degrade(self) -> None:
        fake = FakeLLM(LLMDecision(error="ollama_invalid_json"))
        router = CommandRouter(llm_parser=fake)
        result = router.route("今天心情如何")
        self.assertEqual(result.source, "rule")
        self.assertIn("暂不支持", result.response_text)

    def test_llm_service_unavailable_degrade(self) -> None:
        fake = FakeLLM(LLMDecision(error="ollama_unreachable"))
        router = CommandRouter(llm_parser=fake)
        result = router.route("帮我开下 github")
        self.assertIn("暂不支持", result.response_text)


if __name__ == "__main__":
    unittest.main()
