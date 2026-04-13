"""Skill 基础定义，便于后续扩展。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass
class SkillDefinition:
    """规则路由使用的 skill 定义。"""

    name: str
    keywords: tuple[str, ...]
    handler: Callable[[], str]
    should_exit: bool = False
