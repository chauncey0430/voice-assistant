"""语音转文字模块（faster-whisper）。"""

from __future__ import annotations

from faster_whisper import WhisperModel

from config import (
    WHISPER_COMPUTE_TYPE,
    WHISPER_DEVICE,
    WHISPER_LANGUAGE,
    WHISPER_MODEL_SIZE,
)


class SpeechToText:
    """封装 faster-whisper 推理。"""

    def __init__(self) -> None:
        try:
            self.model = WhisperModel(
                WHISPER_MODEL_SIZE,
                device=WHISPER_DEVICE,
                compute_type=WHISPER_COMPUTE_TYPE,
            )
        except Exception as exc:
            raise RuntimeError(f"加载 Whisper 模型失败: {exc}") from exc

    def transcribe(self, audio_data) -> str:
        """将录音数组转为文本。"""
        try:
            segments, _ = self.model.transcribe(audio_data, language=WHISPER_LANGUAGE)
            text = "".join(segment.text for segment in segments).strip()
            return text
        except Exception as exc:
            raise RuntimeError(f"语音识别失败: {exc}") from exc
