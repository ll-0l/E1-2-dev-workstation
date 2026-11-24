"""퀴즈 데이터 검증 스크립트 — 기본 퀴즈를 교체한 뒤 실행해 형식 문제를 찾는다.

실행:
  python3 scripts/validate_quizzes.py               # default_quizzes.py 검사
  python3 scripts/validate_quizzes.py state.json    # 저장 파일의 퀴즈 검사

종료 코드: 문제 없음 0, 오류 있음 1 (CI에서 사용)
"""

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from default_quizzes import _DEFAULT_QUIZ_DATA  # noqa: E402
from quiz import CHOICE_COUNT, Quiz  # noqa: E402

MIN_QUIZ_COUNT = 5          # 과제 요구: 기본 퀴즈 5개 이상
MAX_CHOICE_LENGTH_GAP = 10  # 한 문제 안 선택지 길이 차이가 크면 정답이 티 날 수 있음 (경고)


def validate(quiz_dicts: list[dict], require_hint: bool = True) -> tuple[list[str], list[str]]:
    """(오류 목록, 경고 목록)을 반환한다."""
    errors: list[str] = []
    warnings: list[str] = []

    if len(quiz_dicts) < MIN_QUIZ_COUNT:
        errors.append(f"퀴즈가 {len(quiz_dicts)}개입니다. 최소 {MIN_QUIZ_COUNT}개가 필요합니다.")

    seen_questions: set[str] = set()
    for number, data in enumerate(quiz_dicts, start=1):
        try:
            quiz = Quiz.from_dict(data)            # 선택지 4개, 정답 1~4 등 Quiz 규칙 검사
        except ValueError as error:
            errors.append(f"[{number}] 형식 오류: {error}")
            continue

        if quiz.question in seen_questions:
            errors.append(f"[{number}] 중복 문제: {quiz.question}")
        seen_questions.add(quiz.question)

        if len(set(quiz.choices)) != CHOICE_COUNT:
            errors.append(f"[{number}] 선택지에 같은 문구가 있습니다: {quiz.choices}")
        if require_hint and not quiz.has_hint():
            errors.append(f"[{number}] 힌트가 없습니다: {quiz.question}")

        lengths = [len(choice) for choice in quiz.choices]
        if max(lengths) - min(lengths) > MAX_CHOICE_LENGTH_GAP:
            warnings.append(f"[{number}] 선택지 길이 차이가 {max(lengths) - min(lengths)}자입니다 (정답이 티 날 수 있음)")

    answers = Counter(data.get("answer") for data in quiz_dicts if isinstance(data, dict))
    if quiz_dicts and max(answers.values()) > len(quiz_dicts) / 2:
        warnings.append(f"정답 번호가 한쪽에 몰려 있습니다: {dict(sorted(answers.items()))}")

    return errors, warnings


def load_quizzes(argv: list[str]) -> tuple[str, list[dict], bool]:
    if len(argv) > 1:
        path = Path(argv[1])
        state = json.loads(path.read_text(encoding="utf-8"))
        return str(path), state.get("quizzes", []), False   # 사용자가 추가한 퀴즈는 힌트가 선택 사항
    return "default_quizzes.py", list(_DEFAULT_QUIZ_DATA), True


def main(argv: list[str]) -> int:
    source, quiz_dicts, require_hint = load_quizzes(argv)
    errors, warnings = validate(quiz_dicts, require_hint)

    print(f"검사 대상: {source} (퀴즈 {len(quiz_dicts)}개)")
    answers = Counter(d.get("answer") for d in quiz_dicts if isinstance(d, dict))
    print(f"정답 번호 분포: {dict(sorted(answers.items()))}")
    for message in warnings:
        print(f"⚠️ 경고 {message}")
    for message in errors:
        print(f"❌ 오류 {message}")
    if errors:
        print(f"결과: 오류 {len(errors)}건 — 수정이 필요합니다.")
        return 1
    print("결과: ✅ 문제 없음")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
