import unittest
from unittest.mock import patch

import input_utils


class InputUtilsTest(unittest.TestCase):
    @patch("builtins.input", return_value="  내용  ")
    def test_read_line_strips_input(self, mock_input) -> None:
        self.assertEqual("내용", input_utils.read_line("입력: "))
        mock_input.assert_called_once_with("입력: ")

    @patch("builtins.input", side_effect=["", "  답  "])
    def test_read_text_retries_empty_input(self, _mock_input) -> None:
        with patch("builtins.print") as mock_print:
            self.assertEqual("답", input_utils.read_text("입력: "))
        mock_print.assert_called_once_with("⚠️ 입력이 비어 있습니다. 내용을 입력하세요.")

    @patch("builtins.input", side_effect=["", "abc", "5", " H "])
    def test_read_int_retries_and_accepts_keyword_case_insensitively(self, _mock_input) -> None:
        with patch("builtins.print") as mock_print:
            self.assertEqual("h", input_utils.read_int("입력: ", 1, 4, allow=("h",)))
        self.assertEqual(3, mock_print.call_count)

    @patch("builtins.input", return_value="3")
    def test_read_int_returns_integer(self, _mock_input) -> None:
        self.assertEqual(3, input_utils.read_int("입력: ", 1, 4))

    @patch("builtins.input", side_effect=EOFError)
    def test_read_line_propagates_eof(self, _mock_input) -> None:
        with self.assertRaises(EOFError):
            input_utils.read_line("입력: ")

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["", "abc", "9", "2"])
    def test_invalid_inputs_are_logged_for_debugging(self, _mock_input, _mock_print) -> None:
        with self.assertLogs("quiz.input", level="DEBUG") as logs:
            self.assertEqual(2, input_utils.read_int("선택: ", 1, 4))

        self.assertEqual(3, len(logs.records))
        self.assertIn("빈 입력", logs.output[0])
        self.assertIn("숫자 변환 실패", logs.output[1])
        self.assertIn("범위 밖 숫자", logs.output[2])


if __name__ == "__main__":
    unittest.main()
