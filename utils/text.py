"""文本预处理工具。"""

from __future__ import annotations

import re
from typing import Iterable, Tuple


def normalize_text(text: str) -> str:
    """统一小写并去掉常见空白和标点，便于规则匹配。"""
    cleaned = (text or "").strip().lower()
    cleaned = re.sub(r"[\s\u3000]+", "", cleaned)
    cleaned = re.sub(r"[，。！？,.!?;；:：'\"“”‘’]", "", cleaned)
    return cleaned


def strip_wake_word(
    text: str,
    wake_words: Iterable[str],
    strict: bool = True,
) -> Tuple[bool, str]:
    """根据唤醒词规则处理文本，返回(是否通过, 去唤醒词后的文本)。"""
    normalized_text = normalize_text(text)
    normalized_words = [normalize_text(word) for word in wake_words]

    if not normalized_words:
        return True, normalized_text

    for word in normalized_words:
        if strict:
            if normalized_text.startswith(word):
                return True, normalized_text[len(word) :]
        else:
            if word in normalized_text:
                return True, normalized_text.replace(word, "", 1)

    return False, normalized_text
