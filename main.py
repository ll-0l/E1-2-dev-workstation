"""MZ 신조어 퀴즈 게임 실행 파일.

실행: python3 main.py
디버그 로그: QUIZ_DEBUG=1 python3 main.py  → 잘못된 입력·저장 결과를 quiz_debug.log에 기록
"""

import logging
import os
from pathlib import Path

from quiz_game import QuizGame

DEBUG_LOG_PATH = Path(__file__).resolve().parent / "quiz_debug.log"


def configure_debug_log() -> None:
    """QUIZ_DEBUG=1이면 디버그 로그를 파일에 남긴다. 화면 출력에는 영향을 주지 않는다."""
    if os.environ.get("QUIZ_DEBUG") != "1":
        return
    logging.basicConfig(
        filename=DEBUG_LOG_PATH,
        encoding="utf-8",
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )


def main() -> None:
    configure_debug_log()
    QuizGame().run()


if __name__ == "__main__":
    main()
