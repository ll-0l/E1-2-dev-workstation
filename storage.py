"""퀴즈 게임 상태를 JSON 파일로 안전하게 저장하고 불러온다."""

from __future__ import annotations

import json
import os
import shutil
from pathlib import Path
from typing import Any


DEFAULT_STATE_PATH = Path(__file__).resolve().parent / "state.json"


class StateStorage:
    """dict 형태의 게임 상태를 영속화한다."""

    def __init__(self, path: str | Path = DEFAULT_STATE_PATH) -> None:
        self.path = Path(path)

    def load(self) -> tuple[dict | None, str]:
        try:
            with self.path.open("r", encoding="utf-8") as state_file:
                state = json.load(state_file)
            return self._normalize_state(state), "loaded"
        except FileNotFoundError:
            return None, "missing"
        except (json.JSONDecodeError, ValueError, TypeError, KeyError):
            if not self._backup_corrupted_file():
                return None, "error"
            return None, "corrupted"
        except OSError:
            return None, "error"

    def save(self, state: dict) -> bool:
        temp_path = self.path.with_name(f"{self.path.name}.tmp")
        try:
            normalized = self._normalize_state(state)
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with temp_path.open("w", encoding="utf-8") as state_file:
                json.dump(normalized, state_file, ensure_ascii=False, indent=2)
                state_file.write("\n")
            os.replace(temp_path, self.path)
            return True
        except (OSError, ValueError, TypeError, KeyError):
            try:
                temp_path.unlink(missing_ok=True)
            except OSError:
                pass
            return False

    def _backup_corrupted_file(self) -> bool:
        backup_path = self.path.with_name(f"{self.path.name}.bak")
        try:
            shutil.copy2(self.path, backup_path)
            return True
        except FileNotFoundError:
            return True
        except OSError:
            return False

    @classmethod
    def _normalize_state(cls, state: Any) -> dict:
        if not isinstance(state, dict):
            raise ValueError("상태 데이터는 dict여야 합니다.")

        version = state.get("version", 1)
        if isinstance(version, bool) or not isinstance(version, int) or version != 1:
            raise ValueError("지원하지 않는 상태 데이터 버전입니다.")

        quizzes = state.get("quizzes")
        if not isinstance(quizzes, list):
            raise ValueError("quizzes는 list여야 합니다.")
        normalized_quizzes = [cls._normalize_quiz(item) for item in quizzes]

        best_score = state.get("best_score")
        if best_score is not None and not cls._is_int_in_range(best_score, 0, 100):
            raise ValueError("best_score는 0~100 사이의 정수여야 합니다.")

        best_record = state.get("best_record")
        if best_record is not None:
            best_record = cls._normalize_record(best_record)
            if best_score is not None and best_record["score"] != best_score:
                raise ValueError("best_record의 점수가 best_score와 다릅니다.")

        history = state.get("history", [])
        if not isinstance(history, list):
            raise ValueError("history는 list여야 합니다.")
        normalized_history = [cls._normalize_record(item) for item in history]

        return {
            "version": version,
            "quizzes": normalized_quizzes,
            "best_score": best_score,
            "best_record": best_record,
            "history": normalized_history,
        }

    @staticmethod
    def _normalize_quiz(quiz: Any) -> dict:
        if not isinstance(quiz, dict):
            raise ValueError("퀴즈 항목은 dict여야 합니다.")
        question = quiz.get("question")
        choices = quiz.get("choices")
        answer = quiz.get("answer")
        hint = quiz.get("hint", "")
        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제 내용은 비어 있을 수 없습니다.")
        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("선택지는 정확히 4개여야 합니다.")
        if any(not isinstance(choice, str) or not choice.strip() for choice in choices):
            raise ValueError("선택지는 비어 있을 수 없습니다.")
        if isinstance(answer, bool) or not isinstance(answer, int) or not 1 <= answer <= 4:
            raise ValueError("정답은 1~4 사이의 정수여야 합니다.")
        if not isinstance(hint, str):
            raise ValueError("힌트는 문자열이어야 합니다.")
        return {
            "question": question,
            "choices": list(choices),
            "answer": answer,
            "hint": hint,
        }

    @classmethod
    def _normalize_record(cls, record: Any) -> dict:
        if not isinstance(record, dict):
            raise ValueError("플레이 기록은 dict여야 합니다.")
        played_at = record.get("played_at")
        if not isinstance(played_at, str) or not played_at.strip():
            raise ValueError("played_at은 비어 있지 않은 문자열이어야 합니다.")
        values = {name: record.get(name) for name in ("total", "correct", "hints_used", "hinted_correct", "score")}
        if not cls._is_int_in_range(values["total"], 1):
            raise ValueError("total은 1 이상의 정수여야 합니다.")
        total = values["total"]
        for name in ("correct", "hints_used", "hinted_correct"):
            if not cls._is_int_in_range(values[name], 0, total):
                raise ValueError(f"{name} 값이 올바르지 않습니다.")
        if values["hinted_correct"] > values["correct"]:
            raise ValueError("hinted_correct는 correct보다 클 수 없습니다.")
        if values["hinted_correct"] > values["hints_used"]:
            raise ValueError("hinted_correct는 hints_used보다 클 수 없습니다.")
        if not cls._is_int_in_range(values["score"], 0, 100):
            raise ValueError("score는 0~100 사이의 정수여야 합니다.")
        return {"played_at": played_at, **values}

    @staticmethod
    def _is_int_in_range(value: Any, minimum: int, maximum: int | None = None) -> bool:
        return (
            not isinstance(value, bool)
            and isinstance(value, int)
            and value >= minimum
            and (maximum is None or value <= maximum)
        )
