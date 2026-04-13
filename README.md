# 本地语音助手（Windows 优先）

这是一个基于 Python 3.10+ 的本地语音助手最小可运行版本，支持：

- 麦克风录音（`sounddevice`）
- 语音转文字（`faster-whisper`）
- 规则路由执行命令（无云端、无 LLM）
- 语音播报结果（`pyttsx3`）

> 设计目标：可直接扩展 `skills/` 目录，逐步演进为更完整的本地助手。

---

## 1. 功能列表

当前支持命令（中文）：

- 打开浏览器
- 打开记事本
- 打开计算器
- 现在几点了
- 查看系统信息
- 退出程序

---

## 2. 项目结构

```text
voice-assistant/
├── app.py
├── config.py
├── requirements.txt
├── core/
│   ├── __init__.py
│   ├── audio.py
│   ├── stt.py
│   ├── tts.py
│   └── router.py
├── skills/
│   ├── __init__.py
│   └── system_skills.py
└── utils/
    ├── __init__.py
    └── logger.py
```

---

## 3. 各文件说明

- `app.py`：程序入口，串联录音/STT/路由/TTS 的主循环。
- `config.py`：全局配置（录音参数、Whisper 模型参数、日志级别）。
- `core/audio.py`：麦克风录音模块。
- `core/stt.py`：faster-whisper 语音识别模块。
- `core/tts.py`：pyttsx3 语音播报模块。
- `core/router.py`：规则路由器，负责命令匹配和动作分发。
- `skills/system_skills.py`：具体可执行技能（打开应用、查时间、系统信息）。
- `utils/logger.py`：日志初始化。
- `requirements.txt`：依赖列表。

---

## 4. 环境准备

## Windows（推荐）

1. 安装 Python 3.10+。
2. 在项目目录创建并激活虚拟环境：

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. 安装依赖：

```bash
pip install -r requirements.txt
```

> 首次运行 `faster-whisper` 会下载模型文件（本地推理，不依赖云端 API）。

---

## 5. 运行方式

```bash
python app.py
```

启动后程序会循环：

1. 录音（默认 4 秒）
2. 识别文本
3. 路由执行命令
4. 语音播报结果

---

## 6. 配置项

可在 `config.py` 中调整：

- `RECORD_SECONDS`：每轮录音时长（秒）
- `SAMPLE_RATE`：采样率（默认 16000）
- `WHISPER_MODEL_SIZE`：模型大小（如 `small`、`base`）
- `WHISPER_DEVICE`：设备（`cpu`/`cuda`）
- `WHISPER_COMPUTE_TYPE`：推理精度（默认 `int8`）
- `WHISPER_LANGUAGE`：识别语言（默认 `zh`）

---

## 7. 本地验证建议

由于当前运行环境通常无法直接访问你的麦克风/扬声器，请在本机（Windows）做以下验证：

1. `python app.py` 能正常启动。
2. 说“打开记事本”，确认记事本被打开。
3. 说“现在几点了”，确认有文字输出和语音播报。
4. 说“退出程序”，确认程序退出。

如遇问题：

- 检查麦克风权限（Windows 隐私设置）。
- 检查是否安装了音频驱动。
- 若识别偏慢，可将 `WHISPER_MODEL_SIZE` 改为 `base`。

---

## 8. 后续扩展建议

- 在 `skills/` 下新增技能文件（如天气、文件管理、提醒等）。
- 在 `core/router.py` 增加更细粒度的规则。
- 后续可在保持本地优先的前提下引入可选 LLM 路由。
