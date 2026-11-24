# AGENTS.md — 협업 규칙 & 인터페이스 계약

이 저장소는 세 에이전트가 분업합니다. 각자 **자기 담당 파일만 수정**하고 아래 인터페이스 계약을 지킵니다.

| 이름 | 도구 | 역할 | 작업 폴더 |
|---|---|---|---|
| **Lead** | Claude Code #1 | 통합·메뉴·입력 처리·Git 병합·README | `E1-2-dev-workstation/` (원본) |
| **Player** | Claude Code #2 | 퀴즈 모델·기본 데이터·퀴즈 풀기 진행(보너스 포함) | `E1-2-dev-workstation-player/` (clone) |
| **Codex** | Codex | 파일 저장소·테스트·리뷰 | `E1-2-dev-workstation-codex/` (clone) |

## 1. 공통 규칙
- Python 3.10+ 문법, **표준 라이브러리만** 사용 (외부 패키지 금지)
- 모든 파일 읽기/쓰기는 `encoding="utf-8"`, 사용자 출력 메시지는 한국어
- 커밋 메시지: `Feat|Fix|Docs|Refactor|Test|Chore: 한국어 요약` + 본문에 변경 요약
- **`main`에는 Lead만 커밋/병합**합니다. Player·Codex는 브랜치에서 작업 → `git push -u origin <브랜치>`까지만 하고 병합하지 않습니다.
- 작업 시작 전 항상 `git checkout main && git pull`로 최신 상태를 받은 뒤 새 브랜치를 만듭니다.
- 다른 담당자의 파일 수정이 필요하면 직접 고치지 말고, 보고 내용에 "요청 사항"으로 남깁니다.

## 2. 담당 파일

| 파일 | 담당 | 내용 |
|---|---|---|
| `main.py` | Lead | 진입점 (`QuizGame().run()`) |
| `input_utils.py` | Lead | 공통 입력/검증 함수 |
| `quiz_game.py` | Lead | `QuizGame` (메뉴, 추가/목록/점수/삭제/히스토리, 저장 연동, 종료 처리) |
| `README.md`, `AGENTS.md`, `CLAUDE.md` | Lead | 문서 |
| `quiz.py` | Player | `Quiz` 클래스 |
| `default_quizzes.py` | Player | 기본 퀴즈 데이터 (주제: MZ 신조어·유행어) |
| `quiz_session.py` | Player | `QuizSession` (1회 플레이: 랜덤 출제, 힌트, 채점, 결과) |
| `storage.py` | Codex | `StateStorage` (state.json 입출력) |
| `tests/` | Codex | `unittest` 기반 테스트 |

## 3. 인터페이스 계약

### 3-1. `input_utils.py` (Lead)
```python
def read_line(prompt: str) -> str
    # input() 후 strip. KeyboardInterrupt/EOFError는 잡지 않고 그대로 전파 (QuizGame.run이 최상위에서 처리)
def read_text(prompt: str) -> str
    # 빈 입력이면 "⚠️ 입력이 비어 있습니다. 내용을 입력하세요." 출력 후 재입력
def read_int(prompt: str, min_value: int, max_value: int, allow: tuple[str, ...] = ()) -> int | str
    # 빈 입력 / 숫자 변환 실패 / 범위 밖 → 안내 메시지 후 재입력
    # allow에 포함된 문자열(대소문자 무시, 예: "h")을 입력하면 그 소문자 문자열을 그대로 반환
```

### 3-2. `quiz.py` — `Quiz` (Player)
```python
class Quiz:
    def __init__(self, question: str, choices: list[str], answer: int, hint: str = "") -> None
        # question 비어있지 않음, choices 정확히 4개(빈 문자열 불가), answer 1~4 int(bool 제외). 위반 시 ValueError
    def display(self, number: int | None = None) -> None   # "[문제 n]" + 문제 + 1~4 선택지 출력
    def is_correct(self, user_answer: int) -> bool
    def has_hint(self) -> bool
    def to_dict(self) -> dict          # {"question","choices","answer","hint"}
    @classmethod
    def from_dict(cls, data: dict) -> "Quiz"   # 형식 오류 시 ValueError (KeyError/TypeError도 ValueError로 변환)
```

### 3-3. `default_quizzes.py` (Player)
```python
def get_default_quizzes() -> list[Quiz]   # 호출할 때마다 새 Quiz 인스턴스 목록, 최소 8개, 모두 hint 포함
```

### 3-4. `quiz_session.py` — `QuizSession` (Player)
```python
class QuizSession:
    HINT_KEY = "h"
    def __init__(self, quizzes: list[Quiz], count: int | None = None,
                 shuffle: bool = True, rng: random.Random | None = None) -> None
        # quizzes가 비었거나 count가 1~len(quizzes) 밖이면 ValueError
        # shuffle=True면 rng(없으면 random 모듈)로 섞은 뒤 앞에서 count개 출제
    def play(self) -> dict
        # 문제마다 display → input_utils.read_int("정답 입력 (1-4, 힌트: h): ", 1, 4, allow=(HINT_KEY,))
        # 힌트 입력 시 힌트 출력(문제당 1회만 차감, 힌트 없는 문제는 안내), 정답/오답 즉시 안내(오답이면 정답 공개)
        # 끝나면 결과 출력 후 history 항목 형태의 dict 반환:
        # {"played_at","total","correct","hints_used","hinted_correct","score"}
        # 최고 점수 비교/저장은 하지 않음 (QuizGame 책임)
    @staticmethod
    def calculate_score(correct: int, hinted_correct: int, total: int) -> int
```

### 3-5. `storage.py` — `StateStorage` (Codex)
dict만 다룹니다 (`Quiz`를 import하지 않음). 객체 변환은 `QuizGame` 책임.
```python
DEFAULT_STATE_PATH: Path  # = storage.py가 있는 프로젝트 루트 / "state.json"

class StateStorage:
    def __init__(self, path: str | Path = DEFAULT_STATE_PATH) -> None
    def load(self) -> tuple[dict | None, str]
        # "loaded"    → 정규화된 state dict
        # "missing"   → 파일 없음, None
        # "corrupted" → JSON 파싱 실패/스키마 불일치, None (손상 파일은 state.json.bak으로 백업)
        # "error"     → 그 밖의 OSError, None
        # 예외를 밖으로 던지지 않음
    def save(self, state: dict) -> bool
        # state.json.tmp에 쓰고 os.replace로 원자적 교체, ensure_ascii=False, indent=2
        # 성공 True / 실패 False (예외 던지지 않음)
```
스키마 검증: 최상위 dict, `quizzes`는 list이고 각 항목이 3-2의 Quiz 규칙을 만족해야 함(하나라도 틀리면 corrupted).
`hint`, `best_score`, `best_record`, `history`가 없으면 기본값(`""`, `None`, `None`, `[]`)으로 채움.
`best_score`가 있으면 0~100 int(bool 제외)여야 함.

### 3-6. `state.json` 스키마
```json
{
  "version": 1,
  "quizzes": [
    {"question": "...", "choices": ["a", "b", "c", "d"], "answer": 2, "hint": "..."}
  ],
  "best_score": 80,
  "best_record": {"played_at": "2026-11-20T19:00:00", "total": 5, "correct": 4, "hints_used": 1, "hinted_correct": 0, "score": 80},
  "history": [
    {"played_at": "2026-11-20T19:00:00", "total": 5, "correct": 4, "hints_used": 1, "hinted_correct": 0, "score": 80}
  ]
}
```
- `best_score`: 0~100 int, 플레이 기록이 없으면 `null`
- `played_at`: `datetime.now().isoformat(timespec="seconds")`

### 3-7. 점수 규칙
- 정답 = 배점 100%, **힌트를 보고 맞힌 문제 = 배점 50%**, 오답 = 0
- `score = 100 * (correct - 0.5 * hinted_correct) / total`를 **사사오입**(.5는 항상 올림)한 정수
  - 내장 `round()`는 짝수 반올림(62.5→62)이라 사용하지 않음. 정수 연산 `(200c - 100h + t) // (2t)`로 계산

## 4. 테스트 실행
```bash
python3 -m unittest discover -s tests -v
```
