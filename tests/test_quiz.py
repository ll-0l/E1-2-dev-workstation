import unittest
from unittest.mock import patch

try:
    from default_quizzes import get_default_quizzes
    from quiz import Quiz
except ModuleNotFoundError:
    get_default_quizzes = None
    Quiz = None


@unittest.skipIf(Quiz is None, "Player 모듈이 아직 병합되지 않았습니다.")
class QuizTest(unittest.TestCase):
    def test_validation_rejects_invalid_values(self) -> None:
        valid_choices = ["가", "나", "다", "라"]
        invalid_arguments = [
            ("", valid_choices, 1),
            ("문제", ["가", "나", "다"], 1),
            ("문제", ["가", "나", "다", ""], 1),
            ("문제", valid_choices, True),
            ("문제", valid_choices, 5),
        ]
        for arguments in invalid_arguments:
            with self.subTest(arguments=arguments), self.assertRaises(ValueError):
                Quiz(*arguments)

    def test_dict_round_trip_does_not_share_choices(self) -> None:
        original = Quiz("문제", ["가", "나", "다", "라"], 3, "힌트")
        data = original.to_dict()
        restored = Quiz.from_dict(data)
        data["choices"][0] = "변경"
        self.assertEqual("가", original.choices[0])
        self.assertEqual(original.to_dict(), restored.to_dict())

    def test_from_dict_wraps_format_errors(self) -> None:
        for data in (None, {}, {"question": "문제"}):
            with self.subTest(data=data), self.assertRaises(ValueError):
                Quiz.from_dict(data)

    def test_display_and_answer_helpers(self) -> None:
        quiz = Quiz("문제", ["가", "나", "다", "라"], 2, "힌트")
        with patch("builtins.print") as mock_print:
            quiz.display(3)
        output = "\n".join(str(call.args[0]) if call.args else "" for call in mock_print.call_args_list)
        self.assertIn("[문제 3]", output)
        self.assertIn("4. 라", output)
        self.assertTrue(quiz.is_correct(2))
        self.assertFalse(quiz.is_correct(1))
        self.assertTrue(quiz.has_hint())

    def test_default_quizzes_are_fresh_and_complete(self) -> None:
        first = get_default_quizzes()
        second = get_default_quizzes()
        self.assertGreaterEqual(len(first), 8)
        self.assertTrue(all(quiz.has_hint() for quiz in first))
        self.assertTrue(all(left is not right for left, right in zip(first, second)))


if __name__ == "__main__":
    unittest.main()
