"""规则路由：将识别文本映射到技能动作。"""

from __future__ import annotations

from dataclasses import dataclass

from config import (
    EMPTY_TRANSCRIPT_HINT,
    ENABLE_WAKE_WORD,
    UNKNOWN_COMMAND_HINT,
    WAKE_WORD_STRICT,
    WAKE_WORDS,
)
from core.llm import LLMDecision, OllamaIntentParser
from skills.registry import get_action_handlers, get_skill_definitions
from utils.text import normalize_text, strip_wake_word


@dataclass
class RouteResult:
    response_text: str
    should_exit: bool = False
    matched_skill: str | None = None
    ignored_by_wake_word: bool = False
    source: str = "rule"


class CommandRouter:
    """基于关键词匹配的轻量级路由器（规则优先，LLM 兜底）。"""

    def __init__(self, llm_parser: OllamaIntentParser | None = None) -> None:
        self.skills = get_skill_definitions()
        self.action_handlers = get_action_handlers()
        self.llm_parser = llm_parser or OllamaIntentParser()

    def route(self, text: str) -> RouteResult:
        normalized = normalize_text(text)
        if not normalized:
            return RouteResult(EMPTY_TRANSCRIPT_HINT)

        if ENABLE_WAKE_WORD:
            passed, normalized = strip_wake_word(
                normalized,
                wake_words=WAKE_WORDS,
                strict=WAKE_WORD_STRICT,
            )
            normalized = normalize_text(normalized)
            if not passed:
                return RouteResult(
                    response_text="未检测到唤醒词，已忽略本次输入。",
                    ignored_by_wake_word=True,
                )
            if not normalized:
                return RouteResult("已唤醒，请说出命令。")

        # 1) 规则优先
        for skill in self.skills:
            if any(normalize_text(keyword) in normalized for keyword in skill.keywords):
                try:
                    result = skill.handler()
                    return RouteResult(
                        response_text=result,
                        should_exit=skill.should_exit,
                        matched_skill=skill.name,
                        source="rule",
                    )
                except Exception as exc:
                    return RouteResult(
                        response_text=f"执行命令失败：{exc}",
                        matched_skill=skill.name,
                        source="rule",
                    )

        # 2) LLM 兜底（本阶段仅 open_browser/get_time/unknown）
        llm_decision = self.llm_parser.parse_intent(normalized)
        llm_result = self._run_llm_decision(llm_decision)
        if llm_result:
            return llm_result

        return RouteResult(UNKNOWN_COMMAND_HINT, source="rule")

    def _run_llm_decision(self, decision: LLMDecision) -> RouteResult | None:
        if decision.error:
            return None

        action = decision.action
        if action == "unknown":
            return None

        if action not in {"open_browser", "get_time"}:
            return None

        handler = self.action_handlers.get(action)
        if not handler:
            return None

        return RouteResult(
            response_text=handler(),
            matched_skill=action,
            source="llm",
        )
