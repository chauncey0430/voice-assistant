"""应用配置。"""

from pathlib import Path

# 音频采样配置
SAMPLE_RATE = 16_000
CHANNELS = 1
RECORD_SECONDS = 4
DTYPE = "float32"

# Whisper 模型配置（本地推理）
WHISPER_MODEL_SIZE = "small"
WHISPER_DEVICE = "cpu"
WHISPER_COMPUTE_TYPE = "int8"
WHISPER_LANGUAGE = "zh"

# 日志配置
LOG_LEVEL = "INFO"

# 项目目录
BASE_DIR = Path(__file__).resolve().parent
