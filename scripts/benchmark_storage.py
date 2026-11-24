"""게임 기록(history) 수에 따른 state.json 크기와 저장/불러오기 시간을 측정한다.

실행: python3 scripts/benchmark_storage.py
- 실제 state.json은 건드리지 않고 임시 폴더에서 측정한다.
- 각 크기마다 5회 측정한 중앙값을 출력한다.
"""

import statistics
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from default_quizzes import get_default_quizzes  # noqa: E402
from storage import StateStorage  # noqa: E402

RECORD_COUNTS = (0, 100, 1_000, 10_000, 100_000)
REPEAT = 5


def make_state(record_count: int) -> dict:
    record = {
        "played_at": "2026-11-24T19:00:00",
        "total": 5,
        "correct": 4,
        "hints_used": 1,
        "hinted_correct": 1,
        "score": 70,
    }
    return {
        "version": 1,
        "quizzes": [quiz.to_dict() for quiz in get_default_quizzes()],
        "best_score": 70 if record_count else None,
        "best_record": dict(record) if record_count else None,
        "history": [dict(record) for _ in range(record_count)],
    }


def measure(record_count: int) -> tuple[int, float, float]:
    state = make_state(record_count)
    with tempfile.TemporaryDirectory() as temp_dir:
        storage = StateStorage(Path(temp_dir) / "state.json")
        save_times, load_times = [], []
        for _ in range(REPEAT):
            start = time.perf_counter()
            assert storage.save(state)
            save_times.append(time.perf_counter() - start)

            start = time.perf_counter()
            loaded, status = storage.load()
            load_times.append(time.perf_counter() - start)
            assert status == "loaded" and len(loaded["history"]) == record_count
        size = storage.path.stat().st_size
    return size, statistics.median(save_times) * 1000, statistics.median(load_times) * 1000


def human_size(size: int) -> str:
    if size < 1024:
        return f"{size} B"
    if size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"
    return f"{size / 1024 / 1024:.1f} MB"


def main() -> None:
    print(f"Python {sys.version.split()[0]}, {REPEAT}회 측정 중앙값\n")
    print("| 게임 기록 수 | state.json 크기 | 저장(save) | 불러오기(load) |")
    print("|---:|---:|---:|---:|")
    for count in RECORD_COUNTS:
        size, save_ms, load_ms = measure(count)
        print(f"| {count:,} | {human_size(size)} | {save_ms:.1f} ms | {load_ms:.1f} ms |")


if __name__ == "__main__":
    main()
