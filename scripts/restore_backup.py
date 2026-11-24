"""손상 백업(state.json.bak) 검사·복원 스크립트.

실행:
  python3 scripts/restore_backup.py             # .bak이 지금 바로 불러올 수 있는 상태인지 검사만 한다
  python3 scripts/restore_backup.py --restore   # 정상이면 현재 state.json을 보관하고 .bak으로 되돌린다

- 프로그램이 손상을 감지하면 원본을 state.json.bak으로 복사해 둔다(README 6-5).
- .bak 자체가 손상돼 있으면 어느 부분이 틀렸는지 알려 주고, 복원하지 않는다.
- 복원 전에 현재 state.json은 state.json.before-restore로 보관한다(되돌리기 가능).
"""

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from storage import DEFAULT_STATE_PATH, StateStorage, UnsupportedVersionError  # noqa: E402


def check_backup(backup_path: Path) -> tuple[bool, str]:
    """(복원 가능 여부, 설명)을 반환한다. 파일을 수정하지 않는다."""
    if not backup_path.exists():
        return False, f"{backup_path.name} 파일이 없습니다. (손상이 감지된 적이 없거나 이미 정리됨)"
    try:
        raw = json.loads(backup_path.read_text(encoding="utf-8"))
        state = StateStorage._normalize_state(raw)
    except json.JSONDecodeError as error:
        return False, f"JSON 문법 오류 (줄 {error.lineno}, 칸 {error.colno}): {error.msg} → 직접 고친 뒤 다시 검사하세요."
    except UnsupportedVersionError as error:
        return False, f"{error} → 이 프로그램으로는 복원할 수 없습니다."
    except (ValueError, TypeError, KeyError) as error:
        return False, f"형식 오류: {error} → 해당 부분을 고친 뒤 다시 검사하세요."
    except OSError as error:
        return False, f"파일을 읽을 수 없습니다: {error}"
    best = f"{state['best_score']}점" if state["best_score"] is not None else "기록 없음"
    return True, f"정상입니다. (퀴즈 {len(state['quizzes'])}개, 기록 {len(state['history'])}건, 최고점수 {best})"


def restore(state_path: Path) -> tuple[bool, str]:
    backup_path = state_path.with_name(f"{state_path.name}.bak")
    ok, message = check_backup(backup_path)
    if not ok:
        return False, message
    if state_path.exists():
        shutil.copy2(state_path, state_path.with_name(f"{state_path.name}.before-restore"))
    shutil.copy2(backup_path, state_path)
    return True, f"{backup_path.name} → {state_path.name} 복원 완료. 이전 파일은 {state_path.name}.before-restore에 보관했습니다."


def main(argv: list[str], state_path: Path = DEFAULT_STATE_PATH) -> int:
    backup_path = state_path.with_name(f"{state_path.name}.bak")
    if "--restore" in argv:
        ok, message = restore(state_path)
    else:
        ok, message = check_backup(backup_path)
        if ok:
            message += " 복원하려면 --restore를 붙여 다시 실행하세요."
    print(("✅ " if ok else "⚠️ ") + message)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
