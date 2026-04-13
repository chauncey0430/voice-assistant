"""应用配置。"""

from pathlib import Path

# 音频采样配置
SAMPLE_RATE = 16_000
CHANNELS = 1
RECORD_SECONDS = 4
DTYPE = "float32"

# 简化 VAD（音量阈值）配置
ENABLE_VAD = True
VAD_CHUNK_SECONDS = 0.2
VAD_START_THRESHOLD = 0.015
VAD_SILENCE_THRESHOLD = 0.008
VAD_SILENCE_DURATION = 1.0
VAD_MAX_RECORD_SECONDS = 10

# Whisper 模型配置（本地推理）
WHISPER_MODEL_SIZE = "small"
WHISPER_DEVICE = "cpu"
WHISPER_COMPUTE_TYPE = "int8"
WHISPER_LANGUAGE = "zh"

# 唤醒词配置
ENABLE_WAKE_WORD = False
WAKE_WORDS = ("小助手", "电脑", "助手")
WAKE_WORD_STRICT = True

# Ollama 配置（规则未命中时兜底）
OLLAMA_ENABLED = False
OLLAMA_MODEL = "qwen2.5:3b"
OLLAMA_BASE_URL = "http://127.0.0.1:11434"
OLLAMA_TIMEOUT = 15

# 交互与路由配置
EXIT_KEYWORDS = ("退出程序", "退出", "结束", "关闭助手")
EMPTY_TRANSCRIPT_HINT = "我没有听清，请再说一次。"
UNKNOWN_COMMAND_HINT = "暂不支持这个命令，请试试打开浏览器、打开记事本等。"

# 日志配置
LOG_LEVEL = "INFO"
LOG_DIR = Path("logs")
LOG_FILE_NAME = "assistant.log"

# 项目目录
BASE_DIR = Path(__file__).resolve().parent
