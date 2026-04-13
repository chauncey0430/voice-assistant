"""浏览器相关 skill。"""

from __future__ import annotations

import webbrowser


def open_browser() -> str:
    """打开默认浏览器。"""
    try:
        webbrowser.open("https://www.bing.com")
        return "已打开浏览器。"
    except Exception as exc:
        return f"打开浏览器失败：{exc}"
