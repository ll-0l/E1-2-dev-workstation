# 동료평가 대응 가이드

동료평가 때 **평가 항목 ↔ 내 과제의 해당 위치**를 바로 찾고, 질문에 답할 수 있도록 정리한 문서입니다.

- 평가 항목 번호(#1~#20)는 AI 사전평가 항목 순서를 따릅니다. 1차 평가 14/20, 보완 후 2차 평가 **20/20 PASS** (2026-11-24).
- 코드 링크의 줄 번호는 이 문서를 작성한 시점 기준입니다.
- 관련 문서: [README](../README.md) · [실행 로그](RUN_LOG.md) · [Git 증빙](GIT_EVIDENCE.md)

## 목차
1. [평가 항목 일대일 대응표](#1-평가-항목-일대일-대응표)
2. [항목별 예상 질문과 답변](#2-항목별-예상-질문과-답변)
3. [학습 목표 질문과 답변](#3-학습-목표-질문과-답변)
4. [시연 순서 (약 5분)](#4-시연-순서-약-5분)
5. [사전평가 반영 내역 (1차)](#5-사전평가-반영-내역-1차)
6. [재평가 보완 내역 (2차)](#6-재평가-보완-내역-2차)

---

## 1. 평가 항목 일대일 대응표

| # | 평가 주제 | 1차 → 2차 평가 | 코드 위치 | 문서 위치 | 바로 보여줄 것 |
|---|---|---|---|---|---|
| 1 | 메뉴 출력과 기능 선택 | PASS → PASS | [quiz_game.py `menu_items`](../quiz_game.py#L34), [`run`](../quiz_game.py#L47) | README 4장 메뉴 | `python3 main.py` 실행 화면, [RUN_LOG 1](RUN_LOG.md#1-첫-실행--퀴즈-추가) |
| 2 | 퀴즈 풀기, 정답 판정, 입력 검증 | PASS → PASS | [quiz_session.py `play`](../quiz_session.py#L34), [정답 판정](../quiz_session.py#L65), [input_utils `read_int`](../input_utils.py#L22) | README 4장 입력·예외 처리 표 | 메뉴 1 → `h`(힌트), `abc`, `0` 입력 |
| 3 | 퀴즈 추가와 파일 저장(영속성) | PASS → PASS | [quiz_game.py `add_quiz`](../quiz_game.py#L96), [`save`](../quiz_game.py#L257) | README 6-1 쓰는 시점, 6-4 | 퀴즈 추가 → 종료 → 재실행 시 "퀴즈 13개" |
| 4 | 기본 퀴즈 5개 이상 | PASS → PASS | [default_quizzes.py](../default_quizzes.py#L8) (12개) | README 2장 선정 기준 | 메뉴 3 목록 |
| 5 | GitHub 원격 저장소와 10개 이상 커밋 | FAIL → **PASS** | — | [GIT_EVIDENCE 1·2장](GIT_EVIDENCE.md#1-원격-저장소), README 9-1 | `git remote -v`, `git log --no-merges --oneline \| wc -l` |
| 6 | 브랜치 생성·병합 기록 | FAIL → **PASS** | — | [GIT_EVIDENCE 3장](GIT_EVIDENCE.md#3-브랜치와-병합-기록), README 9-3 | `git log --oneline --graph` |
| 7 | clone / pull 실습 | FAIL → **PASS** | — | [GIT_EVIDENCE 4장](GIT_EVIDENCE.md#4-clone--pull-실습), README 9-4 | 4-2의 clone → push → pull 원문 |
| 8 | 클래스 책임 분리 | PASS → PASS | [Quiz](../quiz.py#L9), [QuizSession](../quiz_session.py#L15), [QuizGame](../quiz_game.py#L26), [StateStorage](../storage.py#L18) | README 5-2 (클래스별 주요 메서드) | README 5-2 표 |
| 9 | 입력 검증과 데이터 IO 분리 | PASS → PASS | [input_utils.py](../input_utils.py), [storage.py](../storage.py) | README 5-4 | `StateStorage`에 `print`/`input`이 없음 |
| 10 | state.json 경로와 읽기/쓰기 | PASS → PASS | [`DEFAULT_STATE_PATH`](../storage.py#L12), [`load`](../storage.py#L21), [`save`](../storage.py#L35), [QuizGame.load](../quiz_game.py#L232) | README 6-1, 6-3 불러오기 흐름 | 재실행 시 "📂 저장된 데이터를 불러왔습니다" |
| 11 | Ctrl+C / EOF 안전 종료 | PASS → PASS | [quiz_game.py `except (KeyboardInterrupt, EOFError)`](../quiz_game.py#L58) | README 4장 표, 6-4 | 실행 중 Ctrl+C → 안내 후 종료 |
| 12 | 커밋 메시지 규칙 | PASS → PASS | — | README 9-2 (규칙 + 예시) | `git log --oneline` |
| 13 | 클래스를 사용한 이유 | FAIL → **PASS** | — | README 5-3 | 아래 [Q13](#13-클래스를-사용한-이유) 답변 |
| 14 | JSON을 사용한 이유 | PASS → PASS | [storage.py `json.dump(..., ensure_ascii=False)`](../storage.py#L41) | README 6-6 (CSV/SQLite/pickle 비교) | `state.json`을 열어 한글 확인 |
| 15 | 파일 IO 예외 처리 | PASS → PASS | [storage.py `load` 예외 분기](../storage.py#L22), [`save` 예외](../storage.py#L45) | README 4장 표(메시지/조치), 6-4 | 깨진 state.json으로 실행 |
| 16 | 브랜치 전략 | PASS → PASS | — | README 9-3, [AGENTS.md](../AGENTS.md) | `git log --graph`의 병합 모양 |
| 17 | state.json 스키마 설계 | PASS → PASS | [storage.py `_normalize_state`](../storage.py#L63) | README 6-2 (필드별 설계 의도) | README 6-2 표 |
| 18 | JSON 방식의 한계 | FAIL → **PASS** | — | README 6-7 | 아래 [Q18](#18-json-방식의-한계) 답변 |
| 19 | 손상 파일 대응 | PASS → PASS | [storage.py `_backup_corrupted_file`](../storage.py#L52) | README 6-5 (백업 보존 정책) | `echo '{broken' > state.json` 후 실행 |
| 20 | 요구사항 변경 시 영향 범위 | FAIL → **PASS** | [quiz.py `CHOICE_COUNT`](../quiz.py#L3) 등 | README 8장 | 아래 [Q20](#20-요구사항-변경-영향-범위) 답변 |

---

## 2. 항목별 예상 질문과 답변

### 1. 메뉴 출력과 기능 선택
**Q. 메뉴는 어떻게 동작하나요?**
`QuizGame.__init__`에서 `menu_items` 리스트에 `("퀴즈 풀기", self.play_quiz)`처럼 **메뉴 이름과 실행할 메서드를 쌍으로** 넣었습니다. `run()`은 `while self.running:` 반복문 안에서 메뉴를 출력하고, `read_int("선택: ", 1, len(self.menu_items))`로 번호를 받아 `menu_items[choice - 1]`의 메서드를 실행합니다. if/elif를 7번 쓰지 않아도 되고, 메뉴를 추가할 때 리스트에 한 줄만 넣으면 번호와 입력 범위가 자동으로 맞춰집니다.

### 2. 퀴즈 풀기, 정답 판정, 입력 검증
**Q. 정답 판정은 어디서 하나요?**
`Quiz.is_correct(user_answer)`가 `user_answer == self.answer`로 판정합니다. `QuizSession.play()`가 문제마다 `display()`로 출력하고 → 입력을 받고 → `is_correct()` 결과에 따라 "✅ 정답" 또는 "❌ 오답 + 정답 공개"를 출력합니다.

**Q. 잘못된 답 입력은 어떻게 처리하나요?**
`input_utils.read_int(prompt, 1, 4, allow=("h",))`가 처리합니다. 앞뒤 공백을 지우고, 빈 입력이거나 `int()` 변환에 실패하거나(`try/except ValueError`) 1~4 범위 밖이면 안내 후 다시 묻습니다. `h`는 허용 키워드라 힌트 요청으로 돌려줍니다. 테스트는 `tests/test_input_utils.py`, `tests/test_quiz_game_run.py`에 있습니다.

### 3. 퀴즈 추가와 파일 저장
**Q. 추가한 퀴즈가 어떻게 유지되나요?**
`add_quiz()`가 입력을 받아 `Quiz` 객체를 만들고 `self.quizzes`에 추가한 뒤 **바로 `self.save()`를 호출**합니다. `save()`는 전체 상태를 dict로 바꿔(`to_state`) `StateStorage.save`로 `state.json`에 씁니다. 다음 실행 때 `load()`가 이 파일을 읽어 복원합니다. `test_added_quiz_persists_after_restart` 테스트로 확인했습니다.

**Q. 저장에 실패하면요?**
임시 파일에 먼저 쓰고 교체하는 방식이라 기존 `state.json`은 보존됩니다. 사용자에게는 "쓰기 권한과 디스크 공간을 확인한 뒤 다시 실행" 안내가 나옵니다(README 6-4).

### 4. 기본 퀴즈
**Q. 기본 퀴즈는 몇 개이고 어떻게 골랐나요?**
12개입니다. 아시아투데이 2026 상반기 신조어 기사에서만 골랐고, 부적절한 표현은 빼고, 정답 번호를 1~4번에 고르게 나누고, 모든 문제에 힌트를 넣었습니다(README 2장 표). 각 퀴즈는 `Quiz.from_dict()`로 만든 **Quiz 인스턴스**입니다.

### 5. GitHub 원격 저장소와 커밋
**Q. 원격 저장소와 커밋 수를 보여주세요.**
`git remote -v` → `https://github.com/ll-0l/E1-2-dev-workstation.git`. 병합 커밋을 빼고 의미 있는 커밋이 36개 이상입니다(`git log --no-merges --oneline | wc -l`). 출력 원문은 GIT_EVIDENCE 1·2장에 있습니다.

### 6. 브랜치 생성과 병합
**Q. 브랜치를 어떻게 쓰셨나요?**
`git checkout -b feature/play-quiz`로 브랜치를 만들어 퀴즈 풀기 기능을 구현하고, `main`으로 돌아와 `git merge --no-ff feature/play-quiz`로 병합했습니다. 총 6개 브랜치를 병합했고, `--no-ff`를 써서 그래프에 갈라졌다 합쳐진 모양이 남습니다. reflog의 `checkout: moving from main to feature/...` 줄이 실제 실행 기록입니다(GIT_EVIDENCE 3장).

### 7. clone / pull
**Q. clone과 pull은 어떻게 실습했나요?**
① `git clone`으로 별도 폴더 `E1-2-dev-workstation-clone`에 복제 → ② 그 폴더에서 README에 한 줄 추가 후 commit, push → ③ 원래 폴더에서 `git pull` → "Fast-forward"로 받아오고 README에 그 줄이 생긴 것을 확인했습니다. 두 번 수행했고, 2차 실습은 명령 출력 전체가 GIT_EVIDENCE 4-2에 있습니다.

### 8. 클래스 책임 분리
**Q. 클래스를 왜 4개로 나눴나요?**
한 클래스가 한 가지 이유로만 바뀌게 하려고 나눴습니다.
- `Quiz`: 문제 1개의 데이터와 규칙
- `QuizSession`: 한 판 진행과 채점
- `QuizGame`: 메뉴 흐름과 전체 상태
- `StateStorage`: 파일 읽기/쓰기

예를 들어 점수 규칙이 바뀌면 `QuizSession.calculate_score`만 고치고, 저장 형식이 바뀌면 `StateStorage`만 고칩니다.

### 9. 입력 검증과 데이터 IO 분리
**Q. 입력 처리와 저장을 왜 다른 파일로 나눴나요?**
바뀌는 이유가 다르기 때문입니다. 입력 규칙은 화면 요구에 따라, 저장은 데이터 형식에 따라 바뀝니다. `StateStorage`는 화면에 아무것도 출력하지 않고 `"loaded"`, `"missing"` 같은 상태값만 돌려주며, 어떤 메시지를 보여줄지는 `QuizGame`이 정합니다. 덕분에 각각 따로 테스트할 수 있습니다(README 5-4).

### 10. state.json 경로와 읽기/쓰기
**Q. 파일은 어디에 있고 언제 읽고 쓰나요?**
`storage.py`와 같은 폴더(프로젝트 루트)의 `state.json`입니다. 경로는 `Path(__file__).resolve().parent / "state.json"`으로 정해서, 어느 폴더에서 실행해도 같은 파일을 씁니다. 시작할 때 1회 읽고, 퀴즈 추가·삭제, 한 판 종료, 프로그램 종료 때 씁니다.

**Q. 파일이 없거나 깨지면?**
없으면 기본 퀴즈로 시작해 파일을 만들고, 깨졌으면 `.bak`으로 백업한 뒤 기본 퀴즈로 복구합니다(README 6-3 흐름도).

### 11. Ctrl+C / EOF
**Q. Ctrl+C를 누르면 어떻게 되나요?**
`run()`의 메인 루프 전체를 `try`로 감싸고 `except (KeyboardInterrupt, EOFError):`에서 "입력이 중단되어 프로그램을 종료합니다"를 출력한 뒤 `save()`를 호출합니다. 트레이스백 없이 종료 코드 0으로 끝납니다. 입력 함수(`read_line`)는 이 예외를 일부러 잡지 않고 위로 전달해, **종료 처리를 한 곳(run)에서만** 하도록 했습니다.

### 12. 커밋 메시지 규칙
**Q. 커밋은 어떤 기준으로 나눴나요?**
기능 1개 = 커밋 1개입니다. `Feat: 퀴즈 추가 기능 구현`, `Feat: 퀴즈 목록 기능 구현`처럼 제목만 봐도 무엇을 했는지 알 수 있게 `Feat/Fix/Docs/Refactor/Test/Chore:` 접두어를 붙였습니다.

### 13. 클래스를 사용한 이유
**Q. 함수만 써도 되는데 왜 클래스를 썼나요?**
- **데이터와 동작을 묶습니다.** `Quiz` 안에 문제·선택지·정답과 `is_correct()`가 함께 있어, dict와 함수가 흩어지지 않습니다.
- **생성할 때 검증합니다.** `Quiz.__init__`이 선택지 4개, 정답 1~4를 검사하므로 잘못된 퀴즈 객체는 아예 만들어지지 않습니다.
- **상태를 유지합니다.** `QuizGame`은 퀴즈 목록·최고 점수·기록을 `self` 속성에 들고 있어, 전역 변수나 긴 인자 목록이 필요 없습니다.
- **교체가 쉽습니다.** `QuizGame(storage=...)`로 저장소를 바꿔 끼울 수 있어 테스트에서 임시 파일을 씁니다.
- **단점**: 코드와 파일이 늘어납니다. 그래서 상태가 없는 입력 검증은 클래스 없이 함수(`input_utils.py`)로 두었습니다.

### 14. JSON을 사용한 이유
**Q. 왜 JSON으로 저장했나요?**
퀴즈 안에 선택지 목록이, 기록 안에 여러 값이 들어 있는 **중첩 구조**를 그대로 담을 수 있고, 표준 `json` 모듈만으로 처리되며, 사람이 열어서 읽고 고칠 수 있기 때문입니다. CSV는 평면 표라 중첩 구조에 맞지 않고, SQLite는 이 규모에 비해 과합니다(README 6-6). `ensure_ascii=False`로 한글을 그대로 저장합니다.

### 15. 파일 IO 예외 처리
**Q. 어떤 예외를 처리했나요?**
`StateStorage.load`는 `FileNotFoundError` → `"missing"`, `json.JSONDecodeError`·`ValueError` 등 → `"corrupted"`(백업), 그 밖의 `OSError` → `"error"`로 나눕니다. `save`는 `OSError` 등이 나면 임시 파일을 지우고 `False`를 돌려줍니다. 두 메서드 모두 예외를 밖으로 던지지 않아 프로그램이 멈추지 않습니다. 상황별 메시지와 조치는 README 4장 표에 있습니다.

### 16. 브랜치 전략
**Q. 브랜치 이름은 어떤 규칙인가요?**
`feature/`는 기능, `test/`는 테스트, `fix/`는 수정입니다. `main`은 항상 실행되는 상태로 두고, 브랜치에서 완성한 뒤 `--no-ff`로 병합했습니다. 세 에이전트가 각자 clone한 폴더에서 브랜치를 push하면, Lead가 검토한 뒤 병합했습니다(AGENTS.md).

### 17. state.json 스키마 설계
**Q. 필드를 왜 이렇게 설계했나요?**
- `answer`는 선택지 문자열이 아닌 **번호**로 저장해, 문구를 고쳐도 정답이 깨지지 않게 했습니다.
- `best_score`는 `null`로 "아직 안 풂"과 0점을 구분합니다.
- `version`은 나중에 구조가 바뀌면 예전 파일을 변환하기 위한 장치입니다.
- `history`에는 `hinted_correct`까지 저장해, 점수를 다시 계산해 검증할 수 있습니다.

필드별 의도는 README 6-2 표에 있습니다.

### 18. JSON 방식의 한계
**Q. JSON 저장의 단점은?**
1. 기록 하나만 추가해도 **파일 전체를 다시 쓴다**. 기록이 쌓일수록 느려지고 메모리를 더 씁니다(1건 ≈ 160바이트, 1만 판 ≈ 1.6MB).
2. 조건 검색과 부분 수정이 안 돼서, 전부 불러와 파이썬에서 걸러야 합니다.
3. 두 프로그램이 동시에 저장하면 나중 것이 덮어씁니다.
4. JSON 자체에는 형식 규칙이 없어 직접 검증 코드를 짜야 합니다.

**대안**: 기록 개수 상한, JSON Lines(추가 전용), 규모가 커지면 SQLite. `StateStorage`만 바꾸면 되도록 설계했습니다(README 6-7).

### 19. 손상 파일 대응
**Q. 파일이 깨지면 데이터는 어떻게 되나요?**
원본을 `state.json.bak`으로 복사한 뒤 기본 퀴즈로 복구하고 안내합니다. 백업은 **가장 최근 손상본 1개만** 보관하며, `.bak`을 고쳐서 `state.json`으로 이름을 바꾸면 수동 복구할 수 있습니다(README 6-5).

### 20. 요구사항 변경 영향 범위
**Q. 선택지를 5개로 바꾸라고 하면 어디를 고치나요?**
`quiz.py`의 `CHOICE_COUNT = 4`를 5로 바꾸면 `Quiz` 검증, `QuizSession` 정답 범위, `QuizGame.add_quiz` 입력이 모두 따라옵니다. 저장소(`storage.py`의 `4`)는 일부러 `Quiz`에 의존하지 않게 해서 따로 고쳐야 하고, 기본 퀴즈 데이터와 테스트도 함께 바꿉니다.

**Q. 저장을 DB로 바꾸면?**
`StateStorage`의 `load`/`save` 약속(dict 입출력)만 지키면 `QuizGame`은 그대로입니다.

다른 변경(힌트 비율, 메뉴 추가, 기록 개수 등)은 README 8장 표에 있습니다.

---

## 3. 학습 목표 질문과 답변

과제 '3. 과제 목표'에서 "설명할 수 있어야 한다"고 한 항목들입니다. 답변마다 이 프로젝트의 실제 코드를 예로 듭니다.

### Python 기초
| 질문 | 답변 | 내 코드의 예 |
|---|---|---|
| 변수란? 왜 쓰나? | 값에 이름을 붙여 저장해 두는 것. 같은 값을 여러 번 쓰고, 값의 의미를 이름으로 드러내기 위해 사용 | `total = len(self.quizzes)` ([quiz_game.py](../quiz_game.py#L199) `_ask_question_count`) |
| int/str/bool/list/dict 차이 | int 정수, str 문자열, bool 참/거짓, list 순서 있는 묶음(인덱스로 접근), dict 키-값 묶음(키로 접근) | 정답 `answer: int`, 문제 `question: str`, `self.running: bool`, 선택지 `choices: list`, 저장 상태 `to_state()`가 반환하는 `dict` |
| if/elif/else | 조건을 위에서부터 검사해 처음 참인 블록 하나만 실행 | [QuizGame.load](../quiz_game.py#L232): 상태가 `missing` / `corrupted` / 그 외인지에 따라 다른 처리 |
| for vs while | for는 **정해진 묶음을 하나씩** 돌 때, while은 **조건이 참인 동안 횟수 모르게** 반복할 때 | for: 문제를 하나씩 출제 ([quiz_session.py](../quiz_session.py#L43)) / while: 올바른 입력이 올 때까지 재입력 ([input_utils.py](../input_utils.py#L36)), 종료 전까지 메뉴 반복 ([quiz_game.py](../quiz_game.py#L52)) |
| 함수, 매개변수, 반환값 | 함수는 이름 붙은 코드 묶음. 매개변수로 값을 받고 `return`으로 결과를 돌려줌 | `read_int(prompt, min_value, max_value, allow)` → 검증된 정수 반환, `calculate_score(correct, hinted_correct, total)` → 점수 반환 |

### 클래스와 객체
| 질문 | 답변 | 내 코드의 예 |
|---|---|---|
| 클래스란? 왜 쓰나? | 데이터(속성)와 동작(메서드)을 묶은 설계도. 객체는 그 설계도로 만든 실체 | `Quiz` 클래스 → 기본 퀴즈 12개가 각각 `Quiz` 객체 |
| `__init__`의 역할 | 객체가 만들어질 때 자동으로 실행되어 속성을 초기화 | [Quiz.__init__](../quiz.py#L9): 값 검증 후 `self.question` 등 설정 |
| `self`의 역할 | 메서드가 호출된 **그 객체 자신**. `self.속성`으로 객체마다 다른 값을 다룸 | `self.quizzes`, `self.best_score` — `QuizGame`의 모든 메서드가 같은 상태 공유 |
| 속성과 메서드 | 속성 = 객체가 가진 값, 메서드 = 객체가 하는 동작 | 속성 `quiz.answer`, 메서드 `quiz.is_correct(3)` |

### 파일 입출력과 예외 처리
| 질문 | 답변 | 내 코드의 예 |
|---|---|---|
| 파일 열기·읽기·쓰기 과정 | `open(경로, 모드, encoding)`으로 열고 → `read`/`write` → 닫기. `with` 문을 쓰면 블록이 끝날 때 자동으로 닫힘 | [storage.py load](../storage.py#L23): `with self.path.open("r", encoding="utf-8")`, [save](../storage.py#L40): `"w"` 모드 |
| JSON이란? 왜 쓰나? | 키-값과 목록으로 데이터를 표현하는 텍스트 형식. 파이썬 dict/list와 1:1로 바뀌고 사람이 읽을 수 있음 | `json.load` → dict, `json.dump(..., ensure_ascii=False, indent=2)` |
| try/except | 오류가 날 수 있는 코드를 `try`에 두고, 오류 종류별로 `except`에서 대신 처리해 프로그램이 멈추지 않게 함 | [input_utils.py](../input_utils.py#L46) `int(raw)` 실패 → `ValueError`, [storage.py](../storage.py#L22) 파일 없음/손상/OS 오류 분기, [quiz_game.py](../quiz_game.py#L58) Ctrl+C/EOF |

### Git
| 질문 | 답변 |
|---|---|
| Git이란? 왜 필요한가? | 파일의 변경 이력을 저장하는 버전 관리 도구. 언제 무엇을 왜 바꿨는지 기록이 남고, 예전 상태로 돌아가거나 여러 사람이 나눠 작업한 뒤 합칠 수 있음 |
| `init` | 현재 폴더를 Git 저장소로 만듦 (`.git` 폴더 생성) |
| `add` | 다음 커밋에 넣을 변경을 고름 (스테이징) |
| `commit` | 스테이징한 변경을 메시지와 함께 이력으로 저장 |
| `push` | 내 컴퓨터의 커밋을 GitHub(원격)에 올림 |
| `pull` | GitHub의 새 커밋을 받아 내 브랜치에 합침 (`fetch` + `merge`) |
| `checkout` | 브랜치를 이동하거나, `-b`로 새 브랜치를 만들며 이동 |
| `clone` | 원격 저장소 전체(이력 포함)를 새 폴더로 복제 |
| 브랜치 생성과 병합 | `git checkout -b feature/play-quiz` → 작업·커밋 → `git checkout main` → `git merge --no-ff feature/play-quiz` |

---

## 4. 시연 순서 (약 5분)

| 순서 | 할 일 | 보여줄 평가 항목 |
|---|---|---|
| 1 | `rm -f state.json` 후 `python3 main.py` → "기본 퀴즈 12개로 시작" | #1, #4, #10 |
| 2 | 메뉴에서 `abc`, `9`, Enter, ` 3 ` 입력 → 목록 | #1, #2 |
| 3 | 메뉴 2 → 퀴즈 추가 (정답 번호에 `0` 한 번) | #2, #3 |
| 4 | 메뉴 1 → 3문제, 한 문제는 `h`로 힌트 → 결과와 최고 점수 갱신 | #2, 보너스(랜덤·문제 수·힌트) |
| 5 | 메뉴 4 점수 → 메뉴 6 기록 → 메뉴 5 삭제(`n`으로 취소) | 보너스(삭제·히스토리) |
| 6 | `Ctrl+C`로 종료 → 다시 실행 → "퀴즈 13개, 최고점수 N점" | #3, #11 |
| 7 | `cat state.json`으로 구조와 한글 확인 | #10, #14, #17 |
| 8 | `echo '{broken' > state.json` → 실행 → 복구 안내, `ls state.json.bak` | #15, #19 |
| 9 | `python3 -m unittest discover -s tests` → 45개 OK | #2, #15 |
| 10 | `git log --oneline --graph`, `git remote -v` | #5, #6, #12, #16 |

---

## 5. 사전평가 반영 내역 (1차)

| # | 사전평가 지적 | 반영 내용 | 위치 |
|---|---|---|---|
| 5·6 | 원격/커밋/브랜치 증빙이 없음 (이미지는 판독 불가) | `git remote -v`, 커밋 수, `--graph`, 병합 목록, reflog를 **텍스트 원문**으로 정리 | [GIT_EVIDENCE.md](GIT_EVIDENCE.md) |
| 7 | clone/pull 증빙 없음 | clone → commit → push → pull 2차 실습을 수행하고 전체 출력 기록 | GIT_EVIDENCE 4장, README 9-4 |
| 13 | 클래스 사용 이유 문서 없음 | 함수와 비교한 장단점, 함수로 둔 부분의 기준 | README 5-3 |
| 18 | JSON 한계 문서 없음 | 전체 재기록·검색·동시성·스키마·날짜의 한계와 대안 | README 6-7 |
| 20 | 요구변경 영향 범위 없음 | 변경 10가지별 수정 파일/메서드 표, `QuizSession` 정답 범위를 `CHOICE_COUNT`로 통일 | README 8장, `quiz_session.py` |
| 1 | 실행 화면을 텍스트로 확인 불가 | 실행 로그 원문 추가 | [RUN_LOG.md](RUN_LOG.md) |
| 2 | 입력 예외 테스트 목록 | 메뉴 입력 예외·Ctrl+C·EOF·재시작 유지 테스트 4개 추가, 예외 표에 테스트 이름 연결 | `tests/test_quiz_game_run.py`, README 4장 |
| 3·11·15 | 저장 실패 시 안내/복구 절차 | 저장 실패 메시지에 조치 방법 추가, 복구 절차 문서화 | `quiz_game.py save`, README 6-4 |
| 4 | 문제 선정 기준 | 출처·제외·중복·정답 분산·선택지·난이도 기준 표 | README 2장 |
| 8 | 메서드-책임 매핑 | 클래스별 주요 메서드 표 | README 5-2 |
| 9 | 분리 이유 | 입력 검증/데이터 IO 분리 이유 | README 5-4 |
| 10 | load 실패 흐름 | 불러오기 흐름도 | README 6-3 |
| 12 | 커밋 예시 | 기능 단위 커밋 예시 6개 | README 9-2 |
| 14 | JSON 선택 비교 | CSV/SQLite/pickle 비교표 | README 6-6 |
| 17 | 필드 설계 의도 | 필드별 설계 의도 열 추가 | README 6-2 |
| 19 | 백업 보존 정책 | 최근 1개 보관, 수동 복구 방법 | README 6-5 |

---

## 6. 재평가 보완 내역 (2차)

2차 평가는 20개 모두 PASS였고, 항목별 "부족한 점"을 아래처럼 보완했습니다. 동료평가에서 같은 지적이 나오면 "보완 내용" 열과 위치를 근거로 답하면 됩니다.

| # | 2차 평가의 부족한 점 | 보완 내용 | 위치 |
|---|---|---|---|
| 1 | 잘못된 입력 후 반복 안내 사례 부족 | 실제 실행 사례 8종 추가 (모든 입력 단계 예외, 빈 상태, 손상·스키마·권한 오류, Ctrl+C, EOF, 저장 실패) | [RUN_LOG 4장](RUN_LOG.md#4-예외-흐름-사례) |
| 2 | 입력 실패 문구의 통일성 | 문구 형식을 `⚠️ {문제}. {조치}.`로 정하고 어긋난 2곳 코드 수정, 빈 목록 안내도 통일 | README 4장 "안내 문구 형식", `input_utils.py`, `quiz_game.py` |
| 3 | 동시 실행 시 덮어쓰기 위험 | 운영 지침(한 폴더 한 실행, 폴더 분리, 실행 전 복사, 복구 방법, 규모 확대 시 잠금 파일) | README 6-8 |
| 4 | 기본 퀴즈 교체 절차 | 수정 위치 → 테스트 → state.json 삭제 후 실행의 3단계 절차 | README 2장 "기본 퀴즈 교체 절차" |
| 5 | 원격 접근 실패 시 확인 방법 | `git ls-remote` 확인법, 증상별 점검표(404/403/네트워크/HTTP 400) | [GIT_EVIDENCE 1장](GIT_EVIDENCE.md#1-원격-저장소) |
| 6 | 병합별 목적·범위 요약 | 병합 커밋 6개별 브랜치·목적·포함 커밋 표 | [GIT_EVIDENCE 3장](GIT_EVIDENCE.md#3-브랜치와-병합-기록) |
| 7 | 스크린샷 캡션 부족 | 모든 스크린샷에 "그림 N." 캡션, clone/pull 전 과정 스크린샷 추가 | README 7장 그림 1~9 |
| 8 | 클래스 책임 경계 예시 | "하는 일 / 하지 않는 일" 표와 한 판 종료 시 역할 분담 예시 | README 5-2 |
| 9 | 테스트와 책임 연결 | 테스트 파일 7개 ↔ 검증 책임 ↔ 개수 ↔ 대표 테스트 매핑 표 | README 5-5 |
| 10 | 쓰기 시점 요약 | 시점별 읽기/쓰기/코드 한눈에 보기 표 | README 6-1 |
| 11 | Ctrl+C 중 저장 실패 사례 | 쓰기 금지 폴더에서 실제 재현한 로그. 그 과정에서 **추가·삭제가 저장된 것처럼 보이던 문제를 발견해 수정**("이번 실행 중에만 유지" 안내 + 테스트) | [RUN_LOG 4-8](RUN_LOG.md#4-8-저장-불가-상태에서-퀴즈-추가--ctrlc), `quiz_game._save_or_warn_unsaved` |
| 12 | 커밋 단위 수치 기준 | 권장 "파일 1~3개, 150줄 이내"와 실측(중앙값 1파일·37줄, 90%가 131줄 이하) | README 9-2 |
| 13 | 객체지향 진입 장벽 | Quick start 예시(실행해서 결과를 확인한 코드) | README 5-3 |
| 14 | SQLite 전환 비용 | 파일·테스트·문서별 전환 체크리스트 | README 6-6 |
| 15 | 오류 알림 형식 표준 | 아이콘별 종류·수준·형식·예시 표 (경고/오류/안내/정보/완료) | README 4장 "안내 문구 형식" |
| 16 | 브랜치 이름·리뷰 지침 | 이름 규칙, 작업 흐름, 금지 사항, 병합 전 리뷰 체크리스트 한 페이지 | [CONTRIBUTING.md](CONTRIBUTING.md) |
| 17 | 버전 업 마이그레이션 예시 | v1 → v2 변환 흐름도와 `migrate_v1_to_v2` 예시, 함께 바꿀 곳 | README 6-9 |
| 18 | 기록 수별 크기·시간 수치 | **실측** 표(0~100,000건)와 측정 스크립트, 대안 적용 시점(약 1만 건) | README 6-7, `scripts/benchmark_storage.py` |
| 19 | 백업 보관 수·복구 테스트 | 보관 정책(최근 1개)과 확장 방법, 자동·수동 복구 테스트 절차, 테스트 2개 추가 | README 6-5, `tests/test_storage.py` |
| 20 | 대형 변경 리스크·체크리스트 | 대형 변경 4종의 영향·리스크·완화 표, 테스트 업데이트를 포함한 공통 체크리스트 | README 8장 |

**코드·테스트 변경 요약** (2차 보완)
- `Refactor`: 입력 오류 문구 통일(`input_utils.read_text`, `QuizGame._confirm`), 빈 목록 안내 통일
- `Fix`: 저장 실패 시 추가·삭제 결과가 이번 실행에만 유지된다는 안내 추가 (`_save_or_warn_unsaved`)
- `Test`: 백업 보존 정책, 수동 복구, 저장 실패 안내 테스트 → 총 45개
- `Chore`: `scripts/benchmark_storage.py`

**예상 질문**
- *Q. 문구를 왜 표준화했나요?* → 같은 종류의 오류가 화면마다 다르게 보이면 사용자가 무엇을 해야 할지 헷갈립니다. 입력 오류 문구는 `read_int`/`read_text`/`_confirm` 세 곳에서만 만들고, 모두 "문제 → 조치" 순서를 지킵니다.
- *Q. 1만 건이 기준인 이유는?* → 실측에서 1만 건일 때 저장이 약 0.1초로, 사람이 지연을 느끼기 시작하는 수준입니다. 매 판 저장하는 구조라 이 시점부터 상한·분리·DB를 검토합니다.
- *Q. 저장 실패를 어떻게 재현했나요?* → 폴더를 쓰기 금지(`chmod 555`)로 바꿔 임시 파일 생성이 실패하게 만들었고, 실행 후 기존 `state.json`이 그대로인 것까지 확인했습니다.
