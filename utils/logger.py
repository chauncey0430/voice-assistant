"""日志工具。"""

from __future__ import annotations

import logging

from config import LOG_LEVEL


def setup_logger() -> None:
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(message)s",
    )
