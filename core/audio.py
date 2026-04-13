"""麦克风录音模块。"""

from __future__ import annotations

import numpy as np
import sounddevice as sd

from config import CHANNELS, DTYPE, RECORD_SECONDS, SAMPLE_RATE


class AudioRecorder:
    """封装基于 sounddevice 的录音逻辑。"""

    def __init__(
        self,
        sample_rate: int = SAMPLE_RATE,
        channels: int = CHANNELS,
        duration: int = RECORD_SECONDS,
        dtype: str = DTYPE,
    ) -> None:
        self.sample_rate = sample_rate
        self.channels = channels
        self.duration = duration
        self.dtype = dtype

    def record_once(self) -> np.ndarray:
        """录制固定时长音频并返回一维 numpy 数组。"""
        frames = int(self.duration * self.sample_rate)
        try:
            audio = sd.rec(
                frames,
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype=self.dtype,
            )
            sd.wait()
            return audio.flatten()
        except Exception as exc:  # 基础异常处理
            raise RuntimeError(f"录音失败: {exc}") from exc
