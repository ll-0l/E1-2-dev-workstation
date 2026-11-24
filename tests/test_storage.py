import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from storage import StateStorage


def valid_quiz() -> dict:
    return {"question": "문제", "choices": ["가", "나", "다", "라"], "answer": 2}


def valid_record(score: int = 50) -> dict:
    return {
        "played_at": "2026-11-20T19:00:00",
        "total": 2,
        "correct": 1,
        "hints_used": 0,
        "hinted_correct": 0,
        "score": score,
    }


class StateStorageTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.path = Path(self.temp_dir.name) / "state.json"
        self.storage = StateStorage(self.path)

    def test_missing_file(self) -> None:
        self.assertEqual((None, "missing"), self.storage.load())

    def test_load_normalizes_optional_fields(self) -> None:
        self.path.write_text(json.dumps({"quizzes": [valid_quiz()]}), encoding="utf-8")
        state, status = self.storage.load()
        self.assertEqual("loaded", status)
        self.assertEqual("", state["quizzes"][0]["hint"])
        self.assertIsNone(state["best_score"])
        self.assertIsNone(state["best_record"])
        self.assertEqual([], state["history"])
        self.assertEqual(1, state["version"])

    def test_invalid_quiz_is_backed_up_as_corrupted(self) -> None:
        raw = '{"quizzes": [{"question": "", "choices": [], "answer": true}]}'
        self.path.write_text(raw, encoding="utf-8")
        self.assertEqual((None, "corrupted"), self.storage.load())
        self.assertEqual(raw, Path(f"{self.path}.bak").read_text(encoding="utf-8"))

    def test_malformed_json_is_backed_up(self) -> None:
        self.path.write_text("{broken", encoding="utf-8")
        self.assertEqual((None, "corrupted"), self.storage.load())
        self.assertTrue(Path(f"{self.path}.bak").exists())

    def test_backup_keeps_only_latest_corrupted_file(self) -> None:
        # 보존 정책: state.json.bak은 가장 최근 손상본 1개만 유지한다
        self.path.write_text("{first broken", encoding="utf-8")
        self.storage.load()
        self.path.write_text("{second broken", encoding="utf-8")
        self.storage.load()

        backups = sorted(p.name for p in Path(self.temp_dir.name).iterdir() if ".bak" in p.name)
        self.assertEqual(["state.json.bak"], backups)
        self.assertEqual("{second broken", Path(f"{self.path}.bak").read_text(encoding="utf-8"))

    def test_manual_recovery_from_backup(self) -> None:
        # 복구 절차: .bak을 고쳐 state.json으로 되돌리면 다시 정상 로드된다
        broken = {"quizzes": [{"question": "문제", "choices": ["가", "나", "다"], "answer": 1}]}
        self.path.write_text(json.dumps(broken, ensure_ascii=False), encoding="utf-8")
        self.assertEqual("corrupted", self.storage.load()[1])

        backup = Path(f"{self.path}.bak")
        repaired = json.loads(backup.read_text(encoding="utf-8"))
        repaired["quizzes"][0]["choices"].append("라")
        self.path.write_text(json.dumps(repaired, ensure_ascii=False), encoding="utf-8")

        state, status = self.storage.load()
        self.assertEqual("loaded", status)
        self.assertEqual(["가", "나", "다", "라"], state["quizzes"][0]["choices"])

    def test_bool_best_score_is_corrupted(self) -> None:
        state = {"quizzes": [valid_quiz()], "best_score": True}
        self.path.write_text(json.dumps(state), encoding="utf-8")
        self.assertEqual((None, "corrupted"), self.storage.load())

    def test_invalid_record_is_corrupted(self) -> None:
        record = valid_record()
        record["hinted_correct"] = 2
        state = {"quizzes": [valid_quiz()], "history": [record]}
        self.path.write_text(json.dumps(state), encoding="utf-8")
        self.assertEqual((None, "corrupted"), self.storage.load())

    def test_save_and_load_unicode_state(self) -> None:
        record = valid_record()
        state = {
            "version": 1,
            "quizzes": [valid_quiz()],
            "best_score": 50,
            "best_record": record,
            "history": [record],
        }
        self.assertTrue(self.storage.save(state))
        self.assertNotIn("\\u", self.path.read_text(encoding="utf-8"))
        self.assertFalse(Path(f"{self.path}.tmp").exists())
        loaded, status = self.storage.load()
        self.assertEqual("loaded", status)
        self.assertEqual(state["best_record"], loaded["best_record"])

    def test_save_rejects_invalid_state_without_replacing_existing_file(self) -> None:
        self.path.write_text("기존 내용", encoding="utf-8")
        self.assertFalse(self.storage.save({"quizzes": "not-a-list"}))
        self.assertEqual("기존 내용", self.path.read_text(encoding="utf-8"))

    def test_load_os_error(self) -> None:
        self.path.mkdir()
        self.assertEqual((None, "error"), self.storage.load())

    def test_save_replace_error_removes_temporary_file(self) -> None:
        with patch("storage.os.replace", side_effect=OSError):
            self.assertFalse(self.storage.save({"quizzes": [valid_quiz()]}))
        self.assertFalse(Path(f"{self.path}.tmp").exists())


if __name__ == "__main__":
    unittest.main()
