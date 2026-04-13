"""统一注册可用 skills。"""

from __future__ import annotations

from collections.abc import Callable

from config import EXIT_KEYWORDS
from skills.app_skill import open_app, open_calculator, open_notepad
from skills.base import SkillDefinition
from skills.browser_skill import open_browser
from skills.info_skill import get_system_info, get_time


def get_skill_definitions() -> list[SkillDefinition]:
    """返回规则路由使用的 skill 列表。"""
    return [
        SkillDefinition(
            name="open_browser",
            keywords=("打开浏览器", "打开网页", "浏览器", "网页"),
            handler=open_browser,
        ),
        SkillDefinition(
            name="open_notepad",
            keywords=("打开记事本", "记事本", "打开 notepad", "notepad"),
            handler=open_notepad,
        ),
        SkillDefinition(
            name="open_calculator",
            keywords=("打开计算器", "计算器", "打开 calc", "calc"),
            handler=open_calculator,
        ),
        SkillDefinition(
            name="get_time",
            keywords=("现在几点", "当前时间", "几点", "时间"),
            handler=get_time,
        ),
        SkillDefinition(
            name="get_system_info",
            keywords=("查看系统信息", "系统信息", "看看电脑状态", "电脑状态"),
            handler=get_system_info,
        ),
        SkillDefinition(
            name="exit",
            keywords=EXIT_KEYWORDS,
            handler=lambda: "好的，程序即将退出。",
            should_exit=True,
        ),
    ]


def get_action_handlers() -> dict[str, Callable[[], str]]:
    """给 LLM fallback 使用的固定 action 白名单。"""
    return {
        "open_browser": open_browser,
        "get_time": get_time,
        "get_system_info": get_system_info,
        "exit": lambda: "好的，程序即将退出。",
    }


def run_open_app(app_name: str) -> str:
    return open_app(app_name)
