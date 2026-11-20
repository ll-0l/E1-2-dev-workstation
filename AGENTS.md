# AGENTS.md — 협업 규칙 & 인터페이스 계약

이 저장소는 **Claude Code**(통합 담당)와 **Codex**(저장소·테스트 담당) 두 에이전트가 나눠서 개발합니다.
두 에이전트는 **서로 다른 파일만 수정**하고, 아래 인터페이스 계약을 지킵니다.

## 1. 공통 규칙
- Python 3.10+ 문법, **표준 라이브러리만** 사용 (외부 패키지 금지)
- 모든 파일 읽기/쓰기는 `encoding="utf-8"`
- 사용자 출력 메시지는 한국어
- 커밋 메시지 형식: `Feat|Fix|Docs|Refactor|Test|Chore: 한국어 요약` + 본문에 변경 요약
- `main`에 직접 커밋하지 않습니다 (Claude Code의 통합 커밋 제외). 작업은 브랜치에서 진행 후 push → Claude Code가 `--no-ff`로 병합합니다.
- 다른 담당자의 파일을 고쳐야 하면 직접 수정하지 말고 사용자에게 요청 내용을 남깁니다.

## 2. 담당 파일

| 파일 | 담당 | 내용 |
|---|---|---|
| `main.py` | Claude Code | 진입점 (`QuizGame().run()`) |
| `quiz.py` | Claude Code | `Quiz` 클래스 |
| `default_quizzes.py` | Claude Code | 기본 퀴즈 데이터 (`get_default_quizzes()`) |
| `quiz_game.py` | Claude Code | `QuizGame` 클래스 (메뉴/입력/플레이/추가/목록/점수/보너스) |
| `README.md` | Claude Code | 문서 |
| `storage.py` | **Codex** | `StateStorage` 클래스 (state.json 입출력) |
| `tests/` | **Codex** | `unittest` 기반 테스트 |

## 3. 인터페이스 계약

### 3-1. `quiz.py` — `Quiz`
```python
class Quiz:
    def __init__(self, question: str, choices: list[str], answer: int, hint: str = "") -> None
        # choices는 정확히 4개, answer는 1~4. 위반 시 ValueError
    def display(self, number: int | None = None) -> None   # 문제+선택지 출력
    def is_correct(self, user_answer: int) -> bool
    def has_hint(self) -> bool
    def to_dict(self) -> dict          # state.json의 quizzes 항목 형태
    @classmethod
    def from_dict(cls, data: dict) -> "Quiz"   # 형식 오류 시 ValueError
```

### 3-2. `storage.py` — `StateStorage` (Codex)
`StateStorage`는 **dict만 다룹니다** (`Quiz` 객체를 import하지 않음). 객체 변환은 `QuizGame` 책임.
```python
DEFAULT_STATE_PATH: Path  # = 프로젝트 루트(storage.py 위치)/state.json

class StateStorage:
    def __init__(self, path: str | Path = DEFAULT_STATE_PATH) -> None
    def load(self) -> tuple[dict | None, str]
        # 반환: (state, status)
        #   status == "loaded"    → state는 정규화된 dict
        #   status == "missing"   → 파일 없음, state는 None
        #   status == "corrupted" → JSON 파싱 실패/스키마 불일치, state는 None
        #                           (손상 파일은 state.json.bak 으로 백업)
        #   status == "error"     → 읽기 권한 등 OSError, state는 None
        # 절대 예외를 밖으로 던지지 않음
    def save(self, state: dict) -> bool
        # 임시파일(state.json.tmp)에 쓰고 os.replace로 원자적 교체
        # ensure_ascii=False, indent=2. 성공 True / 실패 False (예외 던지지 않음)
```
스키마 검증 규칙(`load`): 최상위가 dict이고 `quizzes`가 list여야 함.
각 퀴즈는 question(비어있지 않은 str), choices(str 4개), answer(1~4 int, bool 제외), hint(str, 없으면 "")를 만족해야 하며
**하나라도 틀리면 "corrupted"** 로 판정. 선택 키가 없으면 기본값으로 채움.

### 3-3. `state.json` 스키마
```json
{
  "version": 1,
  "quizzes": [
    {"question": "...", "choices": ["a", "b", "c", "d"], "answer": 2, "hint": ""}
  ],
  "best_score": 80,
  "best_record": {"score": 80, "correct": 4, "total": 5, "hints_used": 0, "played_at": "2026-11-20T19:00:00"},
  "history": [
    {"played_at": "2026-11-20T19:00:00", "total": 5, "correct": 4, "hints_used": 0, "score": 80}
  ]
}
```
- `best_score`: 0~100 int, 아직 플레이 기록이 없으면 `null`
- `best_record`, `history`: 없으면 각각 `null`, `[]`
- `played_at`: `datetime.now().isoformat(timespec="seconds")`

### 3-4. 점수 규칙
- 문제당 배점 = 100 / 출제 문항 수
- 정답 = 배점 100%, **힌트를 보고 맞힌 문제 = 배점 50%**, 오답 = 0
- 최종 점수 = `round(100 * (정답 수 - 0.5 * 힌트사용_정답 수) / 출제 문항 수)`

## 4. 테스트 실행
```bash
python3 -m unittest discover -s tests -v
```
