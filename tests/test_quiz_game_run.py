"""QuizGame.run() 메인 루프의 입력 예외/종료 처리 회귀 테스트."""

import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from quiz_game import QuizGame
from storage import StateStorage


class QuizGameRunTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.state_path = Path(self.temp_dir.name) / "state.json"
        self.game = QuizGame(StateStorage(self.state_path))

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def run_game(self, inputs) -> str:
        buffer = io.StringIO()
        with patch("builtins.input", side_effect=inputs), redirect_stdout(buffer):
            self.game.run()
        return buffer.getvalue()

    def test_menu_rejects_text_out_of_range_and_empty_then_quits(self) -> None:
        output = self.run_game(["abc", "9", "0", "", " 7 "])

        self.assertEqual(3, output.count("잘못된 입력입니다. 1-7 사이의 숫자를 입력하세요."))
        self.assertEqual(1, output.count("입력이 비어 있습니다."))
        self.assertIn("게임을 종료합니다", output)
        self.assertFalse(self.game.running)

    def test_keyboard_interrupt_saves_and_exits_without_traceback(self) -> None:
        output = self.run_game(KeyboardInterrupt)

        self.assertIn("입력이 중단되어 프로그램을 종료합니다", output)
        self.assertTrue(self.state_path.exists())

    def test_eof_saves_and_exits_without_traceback(self) -> None:
        output = self.run_game(EOFError)

        self.assertIn("입력이 중단되어 프로그램을 종료합니다", output)
        self.assertTrue(self.state_path.exists())

    def test_add_quiz_warns_when_save_fails(self) -> None:
        with patch.object(self.game.storage, "save", return_value=False):
            output = self.run_game(["2", "새 문제", "가", "나", "다", "라", "1", "", "7"])

        self.assertIn("퀴즈가 추가되었습니다", output)
        self.assertIn("저장하지 못했습니다", output)
        self.assertIn("추가한 퀴즈는 이번 실행 중에만 유지되며", output)

    def test_added_quiz_persists_after_restart(self) -> None:
        self.run_game(["2", "새 문제", "가", "나", "다", "라", "3", "", "7"])

        restarted = QuizGame(StateStorage(self.state_path))
        with redirect_stdout(io.StringIO()):
            restarted.load()

        self.assertEqual("새 문제", restarted.quizzes[-1].question)
        self.assertEqual(3, restarted.quizzes[-1].answer)


if __name__ == "__main__":
    unittest.main()
