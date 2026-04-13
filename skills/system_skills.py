"""本地系统技能集合。"""

from __future__ import annotations

import platform
import subprocess
import webbrowser
from datetime import datetime

import psutil


class SystemSkills:
    """可执行动作集合。"""

    @staticmethod
    def open_browser() -> str:
        webbrowser.open("https://www.bing.com")
        return "已打开浏览器。"

    @staticmethod
    def open_notepad() -> str:
        try:
            subprocess.Popen(["notepad"])  # Windows
            return "已打开记事本。"
        except FileNotFoundError:
            return "当前系统未找到记事本（此功能主要面向 Windows）。"

    @staticmethod
    def open_calculator() -> str:
        try:
            subprocess.Popen(["calc"])  # Windows
            return "已打开计算器。"
        except FileNotFoundError:
            return "当前系统未找到计算器（此功能主要面向 Windows）。"

    @staticmethod
    def get_time() -> str:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"现在时间是 {now}。"

    @staticmethod
    def get_system_info() -> str:
        cpu = platform.processor() or "Unknown CPU"
        memory = psutil.virtual_memory()
        total_gb = memory.total / (1024**3)
        used_percent = memory.percent
        os_name = f"{platform.system()} {platform.release()}"
        return (
            f"系统：{os_name}；CPU：{cpu}；内存总量约 {total_gb:.1f} GB，"
            f"已使用 {used_percent:.0f}%。"
        )
