"""Ollama 本地 LLM 集成层（最小兜底版）。"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any
from urllib.error import URLError
from urllib.request import Request, urlopen

from config import OLLAMA_BASE_URL, OLLAMA_ENABLED, OLLAMA_MODEL, OLLAMA_TIMEOUT


# 本阶段仅支持这三个动作
ALLOWED_ACTIONS = {
    "open_browser",
    "get_time",
    "unknown",
}


@dataclass
class LLMDecision:
    action: str = "unknown"
    params: dict[str, Any] | None = None
    error: str | None = None


class OllamaIntentParser:
    """将自然语言解析为受限动作协议。"""

    def __init__(
        self,
        enabled: bool = OLLAMA_ENABLED,
        model: str = OLLAMA_MODEL,
        base_url: str = OLLAMA_BASE_URL,
        timeout: int = OLLAMA_TIMEOUT,
    ) -> None:
        self.enabled = enabled
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def parse_intent(self, text: str) -> LLMDecision:
        if not self.enabled:
            return LLMDecision(error="ollama_disabled")

        try:
            llm_json = self._call_ollama(text)
            return self._validate_decision(llm_json)
        except Exception as exc:
            return LLMDecision(error=f"ollama_error:{exc}")

    def _call_ollama(self, text: str) -> dict[str, Any]:
        prompt = self._build_prompt(text)
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "format": "json",
        }
        req = Request(
            url=f"{self.base_url}/api/generate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(req, timeout=self.timeout) as resp:
                body = json.loads(resp.read().decode("utf-8"))
        except URLError as exc:
            raise RuntimeError(f"ollama_unreachable:{exc}") from exc

        response_text = body.get("response", "")
        if not response_text:
            raise RuntimeError("ollama_empty_response")

        try:
            return json.loads(response_text)
        except json.JSONDecodeError as exc:
            raise RuntimeError("ollama_invalid_json") from exc

    def _build_prompt(self, text: str) -> str:
        return (
            "你是本地语音助手的意图解析器。"
            "仅输出 JSON，不要输出其他解释。"
            "动作协议:"
            '{"action":"open_browser|get_time|unknown","params":{}}。'
            f"用户输入: {text}"
        )

    def _validate_decision(self, raw: dict[str, Any]) -> LLMDecision:
        action = raw.get("action", "unknown")
        params = raw.get("params", {})

        if not isinstance(action, str):
            return LLMDecision(error="invalid_action_type")
        if action not in ALLOWED_ACTIONS:
            return LLMDecision(error="unsupported_action")
        if not isinstance(params, dict):
            return LLMDecision(error="invalid_params_type")

        return LLMDecision(action=action, params=params)
