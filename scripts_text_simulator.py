"""文本模拟入口：不使用麦克风，直接验证规则+LLM 兜底主流程。"""

from core.router import CommandRouter


def main() -> None:
    router = CommandRouter()
    print("文本模拟模式（输入 q 退出）")

    while True:
        text = input("你> ").strip()
        if text.lower() in {"q", "quit", "exit"}:
            break

        result = router.route(text)
        print(f"助手({result.source})> {result.response_text}")
        if result.should_exit:
            break


if __name__ == "__main__":
    main()
