# 本地语音助手（最小 Ollama 兜底版）

本项目基于本地技术栈：

- `sounddevice`（录音）
- `faster-whisper`（语音识别）
- `pyttsx3`（语音播报）
- `Ollama`（本地 LLM 兜底）

> 不接云端服务，不做 GUI，不执行任意系统命令。

---

## 本轮完成内容（小阶段）

1. 新增 Ollama 调用模块：`core/llm.py`
2. 在 `config.py` 增加 Ollama 配置项
3. 路由改为“规则优先，LLM 兜底”
4. LLM 仅支持固定 JSON 动作：
   - `open_browser`
   - `get_time`
   - `unknown`
5. 做了最小解析与异常降级
6. 更新 README
7. 增加最小测试

---

## 路由策略

1. 先走规则匹配（原有能力不变）
2. 规则未命中时，调用 Ollama
3. 解析 Ollama 的 JSON
4. 只允许执行白名单动作（本轮仅 `open_browser` / `get_time`）
5. 异常或非法 JSON 则降级为未知命令

---

## Ollama 配置（`config.py`）

- `OLLAMA_ENABLED`：是否启用 LLM 兜底（默认 `False`）
- `OLLAMA_MODEL`：模型名（默认 `qwen2.5:3b`）
- `OLLAMA_BASE_URL`：服务地址（默认 `http://127.0.0.1:11434`）
- `OLLAMA_TIMEOUT`：超时时间（秒）

---

## Ollama 本地准备

```bash
ollama pull qwen2.5:3b
```

确保 Ollama 服务已启动并可访问 `OLLAMA_BASE_URL`。

---

## 最小验证

### 1) 单元测试
```bash
python -m unittest tests.test_router tests.test_llm
```

### 2) 文本模拟（无需麦克风）
```bash
python scripts_text_simulator.py
```

### 3) 语法检查
```bash
python -m py_compile app.py config.py core/*.py skills/*.py utils/*.py tests/*.py scripts_self_check.py scripts_text_simulator.py
```

---

## 本轮限制（下一轮再做）

- LLM 暂不支持 `open_app` / `get_system_info` / `exit`
- 暂不做多参数复杂动作
- 暂不做 GUI / 云端能力 / 任意命令执行
