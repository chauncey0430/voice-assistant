"""OpenAI Provider（Responses API 优先）。"""

from __future__ import annotations

import json
import os

from config import (
    OPENAI_BASE_URL,
    OPENAI_ENABLED,
    OPENAI_MODEL,
    OPENAI_TIMEOUT,
    OPENAI_USE_RESPONSES_API,
)
from core.llm.base import BaseLLMProvider
from core.llm.protocol import LLMDecision, validate_decision


class OpenAIProvider(BaseLLMProvider):
    def __init__(
        self,
        enabled: bool = OPENAI_ENABLED,
        model: str = OPENAI_MODEL,
        base_url: str = OPENAI_BASE_URL,
        timeout: int = OPENAI_TIMEOUT,
        use_responses_api: bool = OPENAI_USE_RESPONSES_API,
    ) -> None:
        self.enabled = enabled
        self.model = model
        self.timeout = timeout
        self.use_responses_api = use_responses_api
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.base_url = base_url.strip()

    def parse_intent(self, text: str) -> LLMDecision:
        if not self.enabled:
            return LLMDecision(error="openai_disabled")
        if not self.api_key:
            return LLMDecision(error="openai_missing_api_key")

        try:
            raw = self._call(text)
            return validate_decision(raw)
        except Exception as exc:
            return LLMDecision(error=f"openai_error:{exc}")

    def _call(self, text: str) -> dict:
        from openai import OpenAI

        client_kwargs = {"api_key": self.api_key, "timeout": self.timeout}
        if self.base_url:
            client_kwargs["base_url"] = self.base_url
        client = OpenAI(**client_kwargs)

        prompt = (
            "你是语音助手意图解析器，只输出 JSON。"
            '协议: {"action":"open_browser|open_app|get_time|get_system_info|exit|unknown","params":{}}。'
            "open_app 仅支持 notepad 或 calc。"
            f"用户输入: {text}"
        )

        if self.use_responses_api:
            resp = client.responses.create(model=self.model, input=prompt)
            text_output = getattr(resp, "output_text", "")
        else:
            chat = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
            )
            text_output = chat.choices[0].message.content or ""

        if not text_output:
            raise RuntimeError("openai_empty_response")

        try:
            return json.loads(text_output)
        except json.JSONDecodeError as exc:
            raise RuntimeError("openai_invalid_json") from exc
