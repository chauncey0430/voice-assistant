"""最小自检脚本：检查核心模块可导入并进行一次无副作用路由 smoke test。"""

from core.router import CommandRouter


def main() -> None:
    router = CommandRouter()
    sample = "当前时间"
    result = router.route(sample)
    print(f"input={sample} -> response={result.response_text}, exit={result.should_exit}")


if __name__ == "__main__":
    main()
