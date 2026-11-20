import random
import unittest
from unittest.mock import patch

try:
    from quiz import Quiz
    from quiz_session import QuizSession
except ModuleNotFoundError:
    Quiz = None
    QuizSession = None


def make_quiz(number: int, answer: int = 1, hint: str = "힌트") -> Quiz:
    return Quiz(f"문제 {number}", ["가", "나", "다", "라"], answer, hint)


@unittest.skipIf(QuizSession is None, "Player 모듈이 아직 병합되지 않았습니다.")
class QuizSessionTest(unittest.TestCase):
    def test_rejects_empty_quizzes_and_invalid_count(self) -> None:
        with self.assertRaises(ValueError):
            QuizSession([])
        quizzes = [make_quiz(1)]
        for count in (0, 2, True):
            with self.subTest(count=count), self.assertRaises(ValueError):
                QuizSession(quizzes, count=count)

    def test_selection_is_reproducible_with_rng(self) -> None:
        quizzes = [make_quiz(number) for number in range(5)]
        first = QuizSession(quizzes, count=3, rng=random.Random(7)).quizzes
        second = QuizSession(quizzes, count=3, rng=random.Random(7)).quizzes
        self.assertEqual([quiz.question for quiz in first], [quiz.question for quiz in second])
        self.assertEqual([quiz.question for quiz in range_session(quizzes)], [quiz.question for quiz in quizzes[:2]])

    def test_score_calculation(self) -> None:
        self.assertEqual(100, QuizSession.calculate_score(4, 0, 4))
        self.assertEqual(50, QuizSession.calculate_score(3, 2, 4))
        self.assertEqual(0, QuizSession.calculate_score(0, 0, 4))

    @patch("quiz_session.datetime")
    @patch("input_utils.read_int", side_effect=["h", "h", 1, 2, 4])
    def test_play_counts_hint_once_and_returns_history_record(self, _read_int, mock_datetime) -> None:
        mock_datetime.now.return_value.isoformat.return_value = "2026-11-20T19:00:00"
        quizzes = [make_quiz(1, 1), make_quiz(2, 2), make_quiz(3, 3, hint="")]
        with patch("builtins.print"):
            result = QuizSession(quizzes, shuffle=False).play()
        self.assertEqual(
            {
                "played_at": "2026-11-20T19:00:00",
                "total": 3,
                "correct": 2,
                "hints_used": 1,
                "hinted_correct": 1,
                "score": 50,
            },
            result,
        )


def range_session(quizzes: list[Quiz]) -> list[Quiz]:
    return QuizSession(quizzes, count=2, shuffle=False).quizzes


if __name__ == "__main__":
    unittest.main()
