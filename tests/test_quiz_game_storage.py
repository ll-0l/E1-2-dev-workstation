import unittest
from unittest.mock import Mock, patch

from quiz_game import QuizGame


def saved_state() -> dict:
    record = {
        "played_at": "2026-11-20T19:00:00",
        "total": 1,
        "correct": 1,
        "hints_used": 0,
        "hinted_correct": 0,
        "score": 100,
    }
    return {
        "version": 1,
        "quizzes": [
            {
                "question": "저장된 문제",
                "choices": ["가", "나", "다", "라"],
                "answer": 1,
                "hint": "저장된 힌트",
            }
        ],
        "best_score": 100,
        "best_record": record,
        "history": [record],
    }


class QuizGameStorageTest(unittest.TestCase):
    def test_loaded_state_is_applied(self) -> None:
        storage = Mock()
        storage.load.return_value = (saved_state(), "loaded")
        game = QuizGame(storage=storage)

        with patch("builtins.print") as mock_print:
            game.load()

        self.assertEqual("저장된 문제", game.quizzes[0].question)
        self.assertEqual(100, game.best_score)
        self.assertEqual(1, len(game.history))
        storage.save.assert_not_called()
        self.assertIn("저장된 데이터를 불러왔습니다", mock_print.call_args.args[0])

    def test_missing_state_saves_default_quizzes(self) -> None:
        storage = Mock()
        storage.load.return_value = (None, "missing")
        storage.save.return_value = True
        game = QuizGame(storage=storage)

        with patch("builtins.print"):
            game.load()

        storage.save.assert_called_once()
        state = storage.save.call_args.args[0]
        self.assertGreaterEqual(len(state["quizzes"]), 8)
        self.assertIsNone(state["best_score"])

    def test_corrupted_state_resets_runtime_state_and_saves(self) -> None:
        storage = Mock()
        storage.load.return_value = (None, "corrupted")
        storage.save.return_value = True
        game = QuizGame(storage=storage)
        game.quizzes = []
        game.best_score = 90
        game.best_record = {"score": 90}
        game.history = [{"score": 90}]

        with patch("builtins.print"):
            game.load()

        self.assertGreaterEqual(len(game.quizzes), 8)
        self.assertIsNone(game.best_score)
        self.assertIsNone(game.best_record)
        self.assertEqual([], game.history)
        storage.save.assert_called_once()

    def test_read_error_does_not_overwrite_file(self) -> None:
        storage = Mock()
        storage.load.return_value = (None, "error")
        game = QuizGame(storage=storage)

        with patch("builtins.print") as mock_print:
            game.load()

        storage.save.assert_not_called()
        self.assertIn("읽을 수 없어", mock_print.call_args.args[0])

    def test_read_error_blocks_all_later_saves(self) -> None:
        storage = Mock()
        storage.load.return_value = (None, "error")
        game = QuizGame(storage=storage)

        with patch("builtins.print"):
            game.load()
            saved = game.save()  # 이후 퀴즈 추가·종료 때의 저장도 막혀야 함

        self.assertTrue(game.read_only)
        self.assertFalse(saved)
        storage.save.assert_not_called()

    def test_unsupported_version_enters_read_only_mode(self) -> None:
        storage = Mock()
        storage.load.return_value = (None, "unsupported")
        game = QuizGame(storage=storage)

        with patch("builtins.print") as mock_print:
            game.load()
            game.save()

        self.assertTrue(game.read_only)
        storage.save.assert_not_called()
        self.assertTrue(any("더 새로운 버전" in str(c.args[0]) for c in mock_print.call_args_list))

    def test_save_serializes_quizzes_and_reports_failure(self) -> None:
        storage = Mock()
        storage.save.return_value = False
        game = QuizGame(storage=storage)

        with patch("builtins.print") as mock_print:
            self.assertFalse(game.save())

        state = storage.save.call_args.args[0]
        self.assertEqual(1, state["version"])
        self.assertIsInstance(state["quizzes"][0], dict)
        self.assertIn("저장하지 못했습니다", mock_print.call_args.args[0])

    def test_apply_state_rejects_invalid_quiz(self) -> None:
        game = QuizGame(storage=Mock())
        state = saved_state()
        state["quizzes"][0]["answer"] = True

        with self.assertRaises(ValueError):
            game._apply_state(state)


if __name__ == "__main__":
    unittest.main()
