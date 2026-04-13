"""规则路由：将识别文本映射到技能动作。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from skills.system_skills import SystemSkills


@dataclass
class RouteResult:
    response_text: str
    should_exit: bool = False


class CommandRouter:
    """简单关键词路由器。"""

    def __init__(self) -> None:
        self.routes: list[tuple[list[str], Callable[[], str], bool]] = [
            (["打开浏览器", "浏览器"], SystemSkills.open_browser, False),
            (["打开记事本", "记事本"], SystemSkills.open_notepad, False),
            (["打开计算器", "计算器"], SystemSkills.open_calculator, False),
            (["现在几点", "几点", "时间"], SystemSkills.get_time, False),
            (["查看系统信息", "系统信息"], SystemSkills.get_system_info, False),
            (["退出程序", "退出", "结束"], lambda: "好的，程序即将退出。", True),
        ]

    def route(self, text: str) -> RouteResult:
        clean_text = (text or "").strip()
        if not clean_text:
            return RouteResult("我没有听清，请再说一次。")

        for keywords, action, should_exit in self.routes:
            if any(keyword in clean_text for keyword in keywords):
                result = action()
                return RouteResult(response_text=result, should_exit=should_exit)

        return RouteResult("暂不支持这个命令，请试试打开浏览器、打开记事本等。")
