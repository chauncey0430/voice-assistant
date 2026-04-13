"""统一 LLM 动作协议。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

ALLOWED_ACTIONS = {
    "open_browser",
    "open_app",
    "get_time",
    "get_system_info",
    "exit",
    "unknown",
}


@dataclass
class LLMDecision:
    action: str = "unknown"
    params: dict[str, Any] | None = None
    error: str | None = None


def validate_decision(raw: dict[str, Any]) -> LLMDecision:
    action = raw.get("action", "unknown")
    params = raw.get("params", {})

    if not isinstance(action, str):
        return LLMDecision(error="invalid_action_type")
    if action not in ALLOWED_ACTIONS:
        return LLMDecision(error="unsupported_action")
    if not isinstance(params, dict):
        return LLMDecision(error="invalid_params_type")

    if action == "open_app":
        app_name = str(params.get("app", "")).strip().lower()
        if app_name not in {"notepad", "calc"}:
            return LLMDecision(action="unknown", error="unsupported_app")
        return LLMDecision(action="open_app", params={"app": app_name})

    return LLMDecision(action=action, params=params)
