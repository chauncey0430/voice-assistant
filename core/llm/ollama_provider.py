"""Ollama Provider。"""

from __future__ import annotations

import json
from urllib.error import URLError
from urllib.request import Request, urlopen

from config import OLLAMA_BASE_URL, OLLAMA_ENABLED, OLLAMA_MODEL, OLLAMA_TIMEOUT
from core.llm.base import BaseLLMProvider
from core.llm.protocol import LLMDecision, validate_decision


class OllamaProvider(BaseLLMProvider):
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
            raw = self._call(text)
            return validate_decision(raw)
        except Exception as exc:
            return LLMDecision(error=f"ollama_error:{exc}")

    def _call(self, text: str) -> dict:
        prompt = (
            "你是语音助手意图解析器，只输出 JSON。"
            '协议: {"action":"open_browser|open_app|get_time|get_system_info|exit|unknown","params":{}}。'
            "open_app 仅支持 notepad 或 calc。"
            f"用户输入: {text}"
        )
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
