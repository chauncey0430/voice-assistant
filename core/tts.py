"""语音播报模块（pyttsx3）。"""

from __future__ import annotations

import pyttsx3


class TextToSpeech:
    """封装 pyttsx3 的播报能力。"""

    def __init__(self) -> None:
        try:
            self.engine = pyttsx3.init()
        except Exception as exc:
            raise RuntimeError(f"初始化 TTS 失败: {exc}") from exc

    def speak(self, text: str) -> None:
        """朗读指定文本。"""
        if not text:
            return
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as exc:
            raise RuntimeError(f"语音播报失败: {exc}") from exc
