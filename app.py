"""本地语音助手入口。"""

from __future__ import annotations

import logging
from enum import Enum

from core.audio import AudioRecorder
from core.router import CommandRouter
from core.stt import SpeechToText
from core.tts import TextToSpeech
from utils.logger import setup_logger


class AssistantState(str, Enum):
    WAITING = "等待输入"
    VOICE_DETECTED = "检测到语音"
    RECOGNIZING = "正在识别"
    EXECUTING = "正在执行"
    SPEAKING = "播报结果"


def _safe_speak(tts: TextToSpeech, text: str, logger: logging.Logger) -> None:
    try:
        tts.speak(text)
    except Exception as exc:
        logger.warning("播报失败，已跳过: %s", exc)


def _show_state(state: AssistantState) -> None:
    print(f"[状态] {state.value}...")


def main() -> None:
    log_file = setup_logger()
    logger = logging.getLogger(__name__)

    logger.info("正在初始化语音助手组件...")
    logger.info("日志文件路径: %s", log_file)

    recorder = AudioRecorder()
    stt = SpeechToText()
    tts = TextToSpeech()
    router = CommandRouter()

    welcome = "语音助手已启动。请说出命令。"
    print(f"[系统] {welcome}")
    print(f"[系统] 日志文件: {log_file}")
    _safe_speak(tts, welcome, logger)

    while True:
        try:
            _show_state(AssistantState.WAITING)
            audio_data = recorder.record_once()

            _show_state(AssistantState.VOICE_DETECTED)
            _show_state(AssistantState.RECOGNIZING)
            text = stt.transcribe(audio_data)
            logger.info("识别文本: %s", text)

            if not text:
                hint = "没有识别到语音内容，请稍微大声一些再试。"
                print(f"[提示] {hint}")
                _show_state(AssistantState.SPEAKING)
                _safe_speak(tts, hint, logger)
                continue

            print(f"[识别] {text}")
            _show_state(AssistantState.EXECUTING)
            result = router.route(text)
            logger.info(
                "路由结果: source=%s, matched_skill=%s, ignored_by_wake_word=%s, should_exit=%s",
                result.source,
                result.matched_skill,
                result.ignored_by_wake_word,
                result.should_exit,
            )

            print(f"[助手] {result.response_text}")
            logger.info("执行结果: %s", result.response_text)
            _show_state(AssistantState.SPEAKING)
            _safe_speak(tts, result.response_text, logger)

            if result.should_exit:
                break

        except KeyboardInterrupt:
            logger.info("用户中断程序。")
            break
        except RuntimeError as exc:
            message = f"处理失败：{exc}"
            logger.warning(message)
            print(f"[错误] {message}")
            _safe_speak(tts, "发生错误，请检查麦克风和依赖后重试。", logger)
        except Exception as exc:
            logger.exception("处理语音命令时发生未预期错误: %s", exc)
            print(f"[错误] 未预期错误：{exc}")
            _safe_speak(tts, "处理命令时发生错误，请重试。", logger)

    print("[系统] 语音助手已退出。")


if __name__ == "__main__":
    main()
