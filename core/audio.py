"""麦克风录音模块。"""

from __future__ import annotations

import time

import numpy as np
import sounddevice as sd

from config import (
    CHANNELS,
    DTYPE,
    ENABLE_VAD,
    RECORD_SECONDS,
    SAMPLE_RATE,
    VAD_CHUNK_SECONDS,
    VAD_MAX_RECORD_SECONDS,
    VAD_SILENCE_DURATION,
    VAD_SILENCE_THRESHOLD,
    VAD_START_THRESHOLD,
)


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
        """优先使用简化 VAD，失败时回落固定时长录音。"""
        if ENABLE_VAD:
            try:
                return self._record_with_simple_vad()
            except Exception:
                return self._record_fixed_seconds()
        return self._record_fixed_seconds()

    def _record_fixed_seconds(self) -> np.ndarray:
        frames = int(self.duration * self.sample_rate)
        if frames <= 0:
            raise RuntimeError("录音时长必须大于 0 秒。")

        audio = sd.rec(
            frames,
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype=self.dtype,
        )
        sd.wait()
        flattened = audio.flatten()
        if not np.any(flattened):
            raise RuntimeError("未采集到有效音频，请检查麦克风是否可用。")
        return flattened

    def _record_with_simple_vad(self) -> np.ndarray:
        chunk_frames = int(self.sample_rate * VAD_CHUNK_SECONDS)
        if chunk_frames <= 0:
            raise RuntimeError("VAD_CHUNK_SECONDS 配置无效。")

        max_chunks = int(VAD_MAX_RECORD_SECONDS / VAD_CHUNK_SECONDS)
        silence_limit_chunks = int(VAD_SILENCE_DURATION / VAD_CHUNK_SECONDS)

        chunks: list[np.ndarray] = []
        speech_started = False
        silence_count = 0
        start_time = time.time()

        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype=self.dtype,
            blocksize=chunk_frames,
        ) as stream:
            for _ in range(max_chunks):
                data, overflowed = stream.read(chunk_frames)
                if overflowed:
                    continue
                mono = data.flatten()
                energy = float(np.sqrt(np.mean(np.square(mono))))

                if not speech_started and energy >= VAD_START_THRESHOLD:
                    speech_started = True

                if speech_started:
                    chunks.append(mono)
                    if energy < VAD_SILENCE_THRESHOLD:
                        silence_count += 1
                    else:
                        silence_count = 0

                    if silence_count >= silence_limit_chunks:
                        break

                if time.time() - start_time >= VAD_MAX_RECORD_SECONDS:
                    break

        if not chunks:
            raise RuntimeError("未检测到有效语音。")

        merged = np.concatenate(chunks)
        if not np.any(merged):
            raise RuntimeError("采集到空音频。")
        return merged
