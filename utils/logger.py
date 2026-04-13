"""日志工具。"""

from __future__ import annotations

import logging
from pathlib import Path

from config import LOG_DIR, LOG_FILE_NAME, LOG_LEVEL


def setup_logger() -> Path:
    """同时初始化控制台和文件日志，返回日志文件路径。"""
    log_dir = LOG_DIR
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / LOG_FILE_NAME

    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))

    if root_logger.handlers:
        root_logger.handlers.clear()

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)

    root_logger.addHandler(stream_handler)
    root_logger.addHandler(file_handler)

    return log_file
