"""本地应用启动 skill。"""

from __future__ import annotations

import subprocess


APP_COMMANDS = {
    "notepad": ["notepad"],
    "calc": ["calc"],
}


def open_notepad() -> str:
    """打开 Windows 记事本。"""
    return open_app("notepad")


def open_calculator() -> str:
    """打开 Windows 计算器。"""
    return open_app("calc")


def open_app(app_name: str) -> str:
    """按白名单打开本地应用。"""
    key = (app_name or "").lower().strip()
    if key not in APP_COMMANDS:
        return f"不支持打开应用: {app_name}"

    try:
        subprocess.Popen(APP_COMMANDS[key])
        if key == "notepad":
            return "已打开记事本。"
        if key == "calc":
            return "已打开计算器。"
        return f"已打开应用: {key}"
    except Exception as exc:
        app_label = "记事本" if key == "notepad" else "计算器" if key == "calc" else key
        return f"打开{app_label}失败：{exc}"
