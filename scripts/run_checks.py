"""변경 후 실행하는 자동 점검 스크립트 (로컬과 GitHub Actions CI에서 동일하게 사용).

실행: python3 scripts/run_checks.py

점검 순서:
  1. 문법 검사   — 모든 .py 파일이 컴파일되는지 (python -m compileall)
  2. 단위 테스트 — tests/ 전체 (python -m unittest discover)
  3. 퀴즈 검증   — 기본 퀴즈 형식·개수·중복 (scripts/validate_quizzes.py)
  4. 실행 스모크 — 실제 main.py를 임시 폴더에서 실행해 메뉴 → 종료가 되는지
하나라도 실패하면 종료 코드 1을 반환한다.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable
GAME_FILES = ("main.py", "quiz.py", "quiz_game.py", "quiz_session.py",
              "default_quizzes.py", "input_utils.py", "storage.py")


def run(title: str, command: list[str], **kwargs) -> bool:
    print(f"\n▶ {title}: {' '.join(command)}")
    result = subprocess.run(command, cwd=kwargs.pop("cwd", ROOT), text=True, capture_output=True, **kwargs)
    output = (result.stdout + result.stderr).strip()
    if output:
        print("\n".join("   " + line for line in output.splitlines()[-8:]))
    print("  ✅ 통과" if result.returncode == 0 else f"  ❌ 실패 (종료 코드 {result.returncode})")
    return result.returncode == 0


def smoke_test() -> bool:
    """복사본 폴더에서 실제 게임을 실행: 첫 실행 → 잘못된 입력 → 목록 → 종료, state.json 생성 확인."""
    with tempfile.TemporaryDirectory() as temp_dir:
        for name in GAME_FILES:
            shutil.copy2(ROOT / name, temp_dir)
        ok = run("실행 스모크 테스트", [PY, "main.py"], cwd=temp_dir, input="abc\n9\n\n3\n7\n")
        created = (Path(temp_dir) / "state.json").exists()
        print(f"   state.json 생성: {'예' if created else '아니오'}")
        return ok and created


def main() -> int:
    print(f"Python {sys.version.split()[0]} / {ROOT.name}")
    results = [
        run("문법 검사", [PY, "-m", "compileall", "-q", "-x", r"(\.git|__pycache__)", "."]),
        run("단위 테스트", [PY, "-m", "unittest", "discover", "-s", "tests"]),
        run("퀴즈 검증", [PY, "scripts/validate_quizzes.py"]),
        smoke_test(),
    ]
    passed = sum(results)
    print(f"\n결과: {passed}/{len(results)} 통과")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
