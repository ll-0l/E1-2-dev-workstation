"""scripts/validate_quizzes.py 테스트."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import validate_quizzes  # noqa: E402
from default_quizzes import _DEFAULT_QUIZ_DATA  # noqa: E402


def quiz(question: str, answer: int = 1, hint: str = "힌트", choices=None) -> dict:
    return {"question": question, "choices": choices or ["가", "나", "다", "라"], "answer": answer, "hint": hint}


class ValidateQuizzesTest(unittest.TestCase):
    def test_default_quizzes_pass(self) -> None:
        errors, _ = validate_quizzes.validate(list(_DEFAULT_QUIZ_DATA))
        self.assertEqual([], errors)

    def test_detects_each_kind_of_error(self) -> None:
        data = [
            quiz("문제1", 1), quiz("문제1", 2),                       # 중복 문제
            quiz("문제3", 3, hint=""),                                # 힌트 없음
            quiz("문제4", 4, choices=["가", "가", "다", "라"]),        # 같은 선택지
            quiz("문제5", 1, choices=["가", "나", "다"]),             # 선택지 3개
        ]
        errors, _ = validate_quizzes.validate(data)
        joined = "\n".join(errors)
        for keyword in ("중복 문제", "힌트가 없습니다", "같은 문구", "형식 오류"):
            self.assertIn(keyword, joined)

    def test_too_few_quizzes_is_error(self) -> None:
        errors, _ = validate_quizzes.validate([quiz(f"문제{i}", i % 4 + 1) for i in range(4)])
        self.assertTrue(any("최소 5개" in e for e in errors))

    def test_skewed_answers_is_warning(self) -> None:
        _, warnings = validate_quizzes.validate([quiz(f"문제{i}", 1) for i in range(6)])
        self.assertTrue(any("몰려" in w for w in warnings))


if __name__ == "__main__":
    unittest.main()
