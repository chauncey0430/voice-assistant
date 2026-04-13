# 本地语音助手（规则优先 + 双 LLM 后端）

本项目保持本地优先与规则优先架构：

- 录音：`sounddevice`
- 语音识别：`faster-whisper`
- 语音播报：`pyttsx3`
- LLM 兜底：`Ollama` 或 `OpenAI GPT`（可切换）

> 不做 GUI，不接任意 shell 执行。

---

## 架构策略

1. 先走规则路由（原有命令优先）
2. 规则未命中时按配置选择 LLM 后端：
   - `none`
   - `ollama`
   - `openai`
3. LLM 输出必须符合统一 JSON 协议
4. 最终仍通过 skills 白名单执行动作

---

## 统一动作协议

```json
{
  "action": "open_browser | open_app | get_time | get_system_info | exit | unknown",
  "params": {}
}
```

- `open_app` 仅允许 `params.app = notepad | calc`
- 白名单外 action 会被拦截为失败/降级

---

## 配置说明（`config.py`）

### 通用
- `LLM_ENABLED`
- `LLM_BACKEND = none | ollama | openai`
- `LLM_TIMEOUT`
- `LLM_FALLBACK_ENABLED`

### Ollama
- `OLLAMA_ENABLED`
- `OLLAMA_MODEL`
- `OLLAMA_BASE_URL`
- `OLLAMA_TIMEOUT`

### OpenAI
- `OPENAI_ENABLED`
- `OPENAI_MODEL`
- `OPENAI_BASE_URL`
- `OPENAI_TIMEOUT`
- `OPENAI_USE_RESPONSES_API`

---

## 环境变量与 .env

- OpenAI Key 必须来自环境变量：`OPENAI_API_KEY`
- 可复制 `.env.example` 为 `.env` 后修改
- `.env` 已在 `.gitignore` 中，避免泄漏

示例：

```bash
cp .env.example .env
```

---

## 如何切换后端

### 1) 完全禁用 LLM
- `LLM_ENABLED = False`
- 或 `LLM_BACKEND = "none"`

### 2) 使用 Ollama
- `LLM_ENABLED = True`
- `LLM_BACKEND = "ollama"`
- `OLLAMA_ENABLED = True`

### 3) 使用 OpenAI
- `LLM_ENABLED = True`
- `LLM_BACKEND = "openai"`
- `OPENAI_ENABLED = True`
- 设置 `OPENAI_API_KEY`

---

## 安装与运行

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

---

## Ollama 本地准备

```bash
ollama pull qwen2.5:3b
```

并确保 Ollama 服务可访问 `OLLAMA_BASE_URL`。

---

## 最小验证

```bash
python -m unittest tests.test_router tests.test_llm tests.test_llm_factory
python scripts_self_check.py
python scripts_text_simulator.py
python -m py_compile app.py config.py core/*.py core/llm/*.py skills/*.py utils/*.py tests/*.py scripts_self_check.py scripts_text_simulator.py
```

---

## 安全边界

- 不允许 LLM 直接执行任意系统命令
- LLM 只能映射到白名单 action
- 解析失败、网络失败、缺失 API Key 都会优雅降级
