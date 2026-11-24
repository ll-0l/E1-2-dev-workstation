"""scripts/restore_backup.py 테스트."""

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import restore_backup  # noqa: E402


def quiz(question: str, answer: int = 1, hint: str = "힌트", choices=None) -> dict:
    return {"question": question, "choices": choices or ["가", "나", "다", "라"], "answer": answer, "hint": hint}


class RestoreBackupTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.state = Path(self.temp_dir.name) / "state.json"
        self.backup = Path(f"{self.state}.bak")

    def run_main(self, argv) -> tuple[int, str]:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = restore_backup.main(["restore_backup.py", *argv], state_path=self.state)
        return code, buffer.getvalue()

    def test_missing_backup(self) -> None:
        code, output = self.run_main([])
        self.assertEqual(1, code)
        self.assertIn("파일이 없습니다", output)

    def test_broken_backup_is_not_restored(self) -> None:
        self.state.write_text("현재 파일", encoding="utf-8")
        self.backup.write_text('{"quizzes": [', encoding="utf-8")

        code, output = self.run_main(["--restore"])

        self.assertEqual(1, code)
        self.assertIn("JSON 문법 오류", output)
        self.assertEqual("현재 파일", self.state.read_text(encoding="utf-8"))

    def test_valid_backup_is_restored_and_current_file_kept(self) -> None:
        self.state.write_text("손상 후 기본값으로 덮인 파일", encoding="utf-8")
        good = {"version": 1, "quizzes": [quiz("되살릴 문제")]}
        self.backup.write_text(json.dumps(good, ensure_ascii=False), encoding="utf-8")

        code, output = self.run_main([])            # 검사만
        self.assertEqual(0, code)
        self.assertIn("--restore", output)
        self.assertEqual("손상 후 기본값으로 덮인 파일", self.state.read_text(encoding="utf-8"))

        code, output = self.run_main(["--restore"])  # 복원
        self.assertEqual(0, code)
        self.assertEqual(good["quizzes"][0]["question"],
                         json.loads(self.state.read_text(encoding="utf-8"))["quizzes"][0]["question"])
        before = Path(f"{self.state}.before-restore")
        self.assertEqual("손상 후 기본값으로 덮인 파일", before.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
