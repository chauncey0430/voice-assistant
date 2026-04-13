"""本地语音助手入口。"""

from __future__ import annotations

import logging

from core.audio import AudioRecorder
from core.router import CommandRouter
from core.stt import SpeechToText
from core.tts import TextToSpeech
from utils.logger import setup_logger


def main() -> None:
    setup_logger()
    logger = logging.getLogger(__name__)

    logger.info("正在初始化语音助手组件...")
    recorder = AudioRecorder()
    stt = SpeechToText()
    tts = TextToSpeech()
    router = CommandRouter()

    welcome = "语音助手已启动。请说出命令。"
    print(welcome)
    tts.speak(welcome)

    while True:
        try:
            print("\n开始录音，请说话...")
            audio_data = recorder.record_once()
            text = stt.transcribe(audio_data)
            print(f"识别结果：{text}")

            result = router.route(text)
            print(f"助手回复：{result.response_text}")
            tts.speak(result.response_text)

            if result.should_exit:
                break

        except KeyboardInterrupt:
            logger.info("用户中断程序。")
            break
        except Exception as exc:
            logger.exception("处理语音命令时发生错误: %s", exc)
            tts.speak("处理命令时发生错误，请重试。")

    print("语音助手已退出。")


if __name__ == "__main__":
    main()
