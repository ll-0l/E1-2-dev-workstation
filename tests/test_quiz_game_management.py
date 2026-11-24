import unittest
from unittest.mock import Mock, patch

from quiz import Quiz
from quiz_game import QuizGame


def make_quiz(question: str) -> Quiz:
    return Quiz(question, ["가", "나", "다", "라"], 1, "힌트")


def make_record(index: int, score: int) -> dict:
    return {
        "played_at": f"2026-11-{index + 1:02d}T19:00:00",
        "total": 5,
        "correct": score // 20,
        "hints_used": 0,
        "hinted_correct": 0,
        "score": score,
    }


class QuizGameManagementTest(unittest.TestCase):
    def setUp(self) -> None:
        self.storage = Mock()
        self.storage.save.return_value = True
        self.game = QuizGame(storage=self.storage)

    def test_delete_returns_without_input_when_empty(self) -> None:
        self.game.quizzes = []
        with patch("builtins.print") as mock_print, patch("quiz_game.read_int") as mock_read:
            self.game.delete_quiz()
        mock_read.assert_not_called()
        self.storage.save.assert_not_called()
        self.assertIn("등록된 퀴즈가 없습니다", mock_print.call_args.args[0])

    @patch("quiz_game.read_int", return_value=0)
    def test_delete_can_be_cancelled_by_number(self, _mock_read) -> None:
        self.game.quizzes = [make_quiz("유지할 문제")]
        with patch("builtins.print"):
            self.game.delete_quiz()
        self.assertEqual(["유지할 문제"], [quiz.question for quiz in self.game.quizzes])
        self.storage.save.assert_not_called()

    @patch("quiz_game.read_line", side_effect=["잘못", "n"])
    @patch("quiz_game.read_int", return_value=1)
    def test_delete_retries_confirmation_and_can_cancel(self, _mock_int, mock_line) -> None:
        self.game.quizzes = [make_quiz("유지할 문제")]
        with patch("builtins.print") as mock_print:
            self.game.delete_quiz()
        self.assertEqual(2, mock_line.call_count)
        self.assertTrue(any("y 또는 n" in str(item) for item in mock_print.call_args_list))
        self.assertEqual(1, len(self.game.quizzes))
        self.storage.save.assert_not_called()

    @patch("quiz_game.read_line", return_value="YES")
    @patch("quiz_game.read_int", return_value=2)
    def test_delete_removes_selected_quiz_and_saves(self, _mock_int, _mock_line) -> None:
        self.game.quizzes = [make_quiz("첫 문제"), make_quiz("둘째 문제")]
        with patch("builtins.print"):
            self.game.delete_quiz()
        self.assertEqual(["첫 문제"], [quiz.question for quiz in self.game.quizzes])
        self.storage.save.assert_called_once()

    def test_show_history_handles_empty_history(self) -> None:
        with patch("builtins.print") as mock_print:
            self.game.show_history()
        mock_print.assert_called_once()
        self.assertIn("게임 기록이 없습니다", mock_print.call_args.args[0])

    def test_show_history_uses_recent_limit_and_marks_best(self) -> None:
        self.game.history = [make_record(index, index * 5) for index in range(12)]
        self.game.best_record = self.game.history[-1]
        self.game.best_score = self.game.best_record["score"]

        with patch("builtins.print") as mock_print:
            self.game.show_history()

        output = "\n".join(str(item.args[0]) if item.args else "" for item in mock_print.call_args_list)
        rows = [line for line in output.splitlines() if line.startswith("2026-")]
        self.assertEqual(self.game.HISTORY_DISPLAY_LIMIT, len(rows))
        self.assertIn("2026-11-12 19:00", rows[0])
        self.assertNotIn("2026-11-01 19:00", output)
        self.assertEqual(1, output.count("🏆"))
        self.assertIn("최근 10개 기록만 표시", output)
        self.assertIn("평균 27.5점", output)

    def test_history_is_trimmed_to_max_but_best_record_is_kept(self) -> None:
        game = QuizGame(storage=Mock())
        game.HISTORY_MAX = 3

        def record(score: int, minute: int) -> dict:
            return {"played_at": f"2026-11-24T19:0{minute}:00", "total": 1, "correct": score // 100,
                    "hints_used": 0, "hinted_correct": 0, "score": score}

        game._record_result(record(100, 0))          # 최고 기록 (가장 오래됨)
        for minute in range(1, 5):
            game._record_result(record(0, minute))

        self.assertEqual(3, len(game.history))
        self.assertEqual(["2026-11-24T19:02:00", "2026-11-24T19:03:00", "2026-11-24T19:04:00"],
                         [r["played_at"] for r in game.history])
        self.assertEqual(100, game.best_score)
        self.assertEqual("2026-11-24T19:00:00", game.best_record["played_at"])

    def test_record_result_updates_only_for_strictly_higher_score(self) -> None:
        first = make_record(0, 80)
        tied = make_record(1, 80)
        higher = make_record(2, 100)
        self.assertTrue(self.game._record_result(first))
        self.assertFalse(self.game._record_result(tied))
        self.assertIs(first, self.game.best_record)
        self.assertTrue(self.game._record_result(higher))
        self.assertIs(higher, self.game.best_record)
        self.assertEqual([first, tied, higher], self.game.history)


if __name__ == "__main__":
    unittest.main()
