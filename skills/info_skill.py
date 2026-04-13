"""系统信息类 skill。"""

from __future__ import annotations

import platform
from datetime import datetime


def get_time() -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"现在时间是 {now}。"


def get_system_info() -> str:
    cpu = platform.processor() or "Unknown CPU"
    os_name = f"{platform.system()} {platform.release()}"

    try:
        import psutil

        memory = psutil.virtual_memory()
        total_gb = memory.total / (1024**3)
        used_percent = memory.percent
        memory_text = f"内存总量约 {total_gb:.1f} GB，已使用 {used_percent:.0f}%。"
    except Exception:
        memory_text = "内存信息不可用（请安装 psutil）。"

    return f"系统：{os_name}；CPU：{cpu}；{memory_text}"
