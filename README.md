# 🎯 MZ 신조어 퀴즈 게임

터미널에서 즐기는 **2026 MZ·잘파세대 신조어** 4지선다 퀴즈 게임입니다.
Python 표준 라이브러리만으로 만들었고, 추가한 퀴즈와 점수 기록은 `state.json`에 저장되어 프로그램을 다시 실행해도 그대로 남습니다.

- GitHub 저장소: https://github.com/ll-0l/E1-2-dev-workstation
- 실행 로그(텍스트): [docs/RUN_LOG.md](docs/RUN_LOG.md)
- Git 작업 증빙(텍스트): [docs/GIT_EVIDENCE.md](docs/GIT_EVIDENCE.md)
- 동료평가 대응표와 답변 정리: [docs/PEER_REVIEW.md](docs/PEER_REVIEW.md)

## 목차
1. [프로젝트 개요](#1-프로젝트-개요)
2. [퀴즈 주제와 선정 이유](#2-퀴즈-주제와-선정-이유)
3. [실행 방법](#3-실행-방법)
4. [기능 목록](#4-기능-목록)
5. [파일 구조와 설계](#5-파일-구조와-설계)
6. [데이터 파일 설명 (state.json)](#6-데이터-파일-설명-statejson)
7. [실행 화면](#7-실행-화면)
8. [요구사항 변경 시 영향 범위](#8-요구사항-변경-시-영향-범위)
9. [개발 과정 (Git)](#9-개발-과정-git)

## 1. 프로젝트 개요

| 항목 | 내용 |
|---|---|
| 형태 | Python 콘솔(터미널) 프로그램 |
| 실행 환경 | Python 3.10 이상, 외부 라이브러리 없음 |
| 핵심 기능 | 퀴즈 풀기 · 추가 · 목록 · 점수 확인 · 삭제 · 게임 기록 |
| 데이터 저장 | 프로젝트 루트의 `state.json` (UTF-8) |
| 구조 | `Quiz` · `QuizSession` · `QuizGame` · `StateStorage` 4개 클래스 + 입력 함수 모듈 `input_utils` |
| 테스트 | `unittest` 단위 테스트 42개 |

## 2. 퀴즈 주제와 선정 이유

**주제: 2026년 MZ·잘파세대 신조어·유행어**

> MZ세대와 원만하게 소통하기 위한 사전학습.
> **'늙크크'(올드한 감성)**가 되지 않기 위한 몸부림입니다.

요즘 SNS와 커뮤니티에서는 '감다살', '밤티', '기대컨'처럼 처음 들으면 뜻을 짐작하기 어려운 말이 계속 생겨납니다.
대화에서 매번 뜻을 묻는 대신 게임으로 가볍게 익혀 보려고 이 주제를 골랐습니다.

### 기본 문제 12개 선정 기준
| 기준 | 적용 내용 |
|---|---|
| 출처 | 아시아투데이 「[카드뉴스] 2026 상반기 신조어 총정리」(2026.07.24)에 실린 24개 표현 중에서만 선정 |
| 제외 | 욕설을 순화한 말(샤갈), 특정 집단을 비하할 수 있는 말(멘헤라) 등 퀴즈로 내기 부적절한 표현은 제외 |
| 중복 | 한 용어당 1문제, 같은 문제 문장 없음 (12문제 모두 서로 다른 용어) |
| 정답 분산 | 정답 번호가 한쪽에 몰리지 않게 1번 3개 · 2번 3개 · 3번 4개 · 4번 2개로 배치 |
| 선택지 | 오답도 그럴듯한 뜻으로 작성하고, 문제 안의 선택지 길이 차이를 6자 이내로 맞춰 정답이 눈에 띄지 않게 함 |
| 난이도 | 별도 등급은 두지 않음. 대신 모든 문제에 힌트를 넣어, 처음 보는 용어도 추론해서 풀 수 있게 함 |

## 3. 실행 방법

```bash
# 1. 저장소 복제
git clone https://github.com/ll-0l/E1-2-dev-workstation.git
cd E1-2-dev-workstation

# 2. Python 버전 확인 (3.10 이상)
python3 --version

# 3. 실행
python3 main.py

# (선택) 단위 테스트 실행
python3 -m unittest discover -s tests -v
```

- 처음 실행하면 `state.json`이 없으므로 기본 퀴즈 12개로 시작하고 파일을 자동으로 만듭니다.
- 종료는 메뉴 `7`을 고르면 됩니다. `Ctrl+C`를 눌러도 저장한 뒤 안전하게 종료됩니다.

## 4. 기능 목록

### 메뉴
```
========================================
         🎯 MZ 신조어 퀴즈 게임 🎯
📂 저장된 데이터를 불러왔습니다. (퀴즈 13개, 최고점수 70점)
========================================
1. 퀴즈 풀기
2. 퀴즈 추가
3. 퀴즈 목록
4. 점수 확인
5. 퀴즈 삭제
6. 게임 기록
7. 종료
========================================
선택:
```

메뉴 항목은 `QuizGame.__init__`의 `self.menu_items` 리스트에 `(메뉴 이름, 실행할 메서드)` 쌍으로 정의되어 있습니다. `run()`은 입력받은 번호로 이 리스트에서 메서드를 꺼내 실행합니다.

| 번호 | 기능 | 담당 메서드 | 설명 |
|---|---|---|---|
| 1 | 퀴즈 풀기 | `QuizGame.play_quiz` → `QuizSession.play` | 풀 문제 수를 고르면 **랜덤 순서**로 출제합니다. 답할 때마다 정답/오답을 알려주고(오답이면 정답 공개), 끝나면 점수를 표시하고 최고 점수를 갱신합니다. |
| 2 | 퀴즈 추가 | `QuizGame.add_quiz` | 문제, 선택지 4개, 정답 번호(1-4), 힌트(선택)를 입력받아 새 퀴즈를 등록하고 바로 저장합니다. |
| 3 | 퀴즈 목록 | `QuizGame.list_quizzes` | 등록된 퀴즈를 번호와 함께 보여줍니다. 힌트가 있는 문제는 💡로 표시합니다. |
| 4 | 점수 확인 | `QuizGame.show_score` | 최고 점수와 그 판의 정답 수, 힌트 사용 횟수, 기록 일시를 보여줍니다. |
| 5 | 퀴즈 삭제 | `QuizGame.delete_quiz` | 번호를 고르고 y/n으로 확인한 뒤 삭제합니다. `0`을 입력하면 취소됩니다. |
| 6 | 게임 기록 | `QuizGame.show_history` | 최근 10판의 일시, 정답 수, 힌트, 점수를 최신순으로 보여주고 평균 점수를 함께 표시합니다. |
| 7 | 종료 | `QuizGame.quit` | 저장한 뒤 종료합니다. |

### 점수 규칙 (힌트 차감)
- 문제를 풀다가 `h`를 입력하면 힌트를 볼 수 있습니다.
- 힌트 없이 맞히면 배점의 100%, **힌트를 보고 맞히면 50%**, 틀리면 0점입니다.
- `점수 = 100 × (정답 수 − 0.5 × 힌트를 보고 맞힌 수) ÷ 출제 문항 수`를 소수점 첫째 자리에서 **반올림(사사오입)**합니다.
- 예: 5문제 중 4문제를 맞혔고 그중 1문제가 힌트 사용 → `100 × 3.5 ÷ 5` = **70점**
- 예: 8문제 중 5문제 정답 → 62.5 → **63점**
- 판이 끝날 때마다 최고 점수와 비교해서 **더 높을 때만** 갱신합니다(`QuizGame._record_result`).

### 입력·예외 처리
모든 숫자 입력은 `input_utils.read_int`, 문자열 입력은 `read_text`/`read_line`을 거칩니다.

| 상황 | 화면 메시지 | 처리 / 사용자 권장 조치 | 검증 테스트 |
|---|---|---|---|
| 입력 앞뒤 공백 (` 1 `) | (없음) | 공백을 지우고 정상 처리 | `test_read_line_strips_input`, `test_menu_rejects_text_out_of_range_and_empty_then_quits` |
| 숫자가 아닌 입력 (`abc`) | ⚠️ 잘못된 입력입니다. 1-7 사이의 숫자를 입력하세요. | 같은 질문을 다시 물음 | `test_read_int_retries_and_accepts_keyword_case_insensitively`, `test_menu_rejects_...` |
| 범위 밖 숫자 (메뉴 `9`, 정답 `0`) | ⚠️ 잘못된 입력입니다. (범위) 사이의 숫자를 입력하세요. | 같은 질문을 다시 물음 | `test_menu_rejects_...` |
| 빈 입력 (Enter) | ⚠️ 입력이 비어 있습니다. … / ⚠️ 내용을 입력하세요. | 같은 질문을 다시 물음 | `test_read_text_retries_empty_input`, `test_menu_rejects_...` |
| `Ctrl+C` / 입력 스트림 종료(EOF) | ⚠️ 입력이 중단되어 프로그램을 종료합니다. | 저장 후 정상 종료(트레이스백 없음) | `test_keyboard_interrupt_saves_and_exits_without_traceback`, `test_eof_saves_and_exits_without_traceback` |
| 퀴즈 0개 상태에서 풀기·목록·삭제 | 📭 등록된 퀴즈가 없습니다. | '퀴즈 추가'로 먼저 등록 | `test_delete_returns_without_input_when_empty` |
| 플레이 기록 없이 점수·기록 확인 | 📭 아직 퀴즈를 풀지 않았습니다. / 게임 기록이 없습니다. | '퀴즈 풀기'로 첫 기록 생성 | `test_show_history_handles_empty_history` |
| `state.json` 없음 (첫 실행) | 📂 저장된 데이터가 없어 기본 퀴즈 12개로 시작합니다. | 기본 퀴즈로 시작하고 파일 생성 | `test_missing_state_saves_default_quizzes`, `test_missing_file` |
| `state.json` 손상 (JSON 문법 오류, 선택지 3개 등) | ⚠️ 데이터 파일이 손상되어 기본 퀴즈로 복구합니다. (원본은 state.json.bak에 백업) | 기본 퀴즈로 복구, 원본은 `.bak`으로 보관 → [6-5](#6-5-손상-파일-백업-정책) | `test_malformed_json_is_backed_up`, `test_invalid_quiz_is_backed_up_as_corrupted`, `test_corrupted_state_resets_runtime_state_and_saves` |
| `state.json` 읽기 오류 (권한 등) | ⚠️ 데이터 파일을 읽을 수 없어 기본 퀴즈로 시작합니다. | 시작할 때 기존 파일을 덮어쓰지 않음. 파일 권한 확인 후 다시 실행 | `test_read_error_does_not_overwrite_file`, `test_load_os_error` |
| `state.json` 쓰기 오류 | ⚠️ 데이터를 파일에 저장하지 못했습니다. + 조치 안내 2줄 | 기존 파일은 보존됨 → [6-4](#6-4-저장-흐름과-저장-실패-시-복구-절차) | `test_save_serializes_quizzes_and_reports_failure`, `test_save_replace_error_removes_temporary_file` |

## 5. 파일 구조와 설계

### 5-1. 파일 구조
```
E1-2-dev-workstation/
├── main.py              # 실행 파일 (QuizGame().run())
├── quiz.py              # Quiz: 문제 1개 (출력, 정답 확인, dict 변환)
├── default_quizzes.py   # 기본 신조어 퀴즈 12개
├── quiz_session.py      # QuizSession: 1회 플레이 (랜덤 출제, 힌트, 채점)
├── quiz_game.py         # QuizGame: 메뉴 흐름, 퀴즈 관리, 점수 기록, 저장 시점
├── storage.py           # StateStorage: state.json 읽기/쓰기, 손상 감지와 백업
├── input_utils.py       # 공통 입력 검증 함수 (공백 제거, 숫자/범위/빈 입력 처리)
├── tests/               # unittest 단위 테스트 (42개)
├── docs/
│   ├── screenshots/     # 실행 화면 · 개발 환경 · git log 스크린샷
│   ├── RUN_LOG.md       # 실행 화면 텍스트 로그
│   ├── GIT_EVIDENCE.md  # 원격 저장소 · 커밋 · 브랜치/병합 · clone/pull 텍스트 증빙
│   └── PEER_REVIEW.md   # 동료평가 항목 대응표와 답변 정리
├── AGENTS.md, CLAUDE.md # 개발 협업 규칙 (9장 참고)
├── .gitignore
├── README.md
└── state.json           # 실행 시 자동 생성 (Git에는 올리지 않음)
```

### 5-2. 클래스 역할과 주요 메서드
| 클래스 | 파일 | 책임 (한 문장) | 주요 메서드 → 하는 일 |
|---|---|---|---|
| `Quiz` | quiz.py | 문제 1개의 데이터와 규칙을 가진다 | `__init__` → 형식 검증 · `display` → 문제 출력 · `is_correct` → 정답 판정 · `to_dict`/`from_dict` → 저장용 변환 |
| `QuizSession` | quiz_session.py | 퀴즈 한 판을 진행하고 채점한다 | `__init__` → 섞기·문항 수 선택 · `play` → 출제·힌트·정답 안내 후 결과 dict 반환 · `calculate_score` → 점수 계산 |
| `QuizGame` | quiz_game.py | 게임 전체 상태를 관리하고 언제 무엇을 할지 정한다 | `run` → 메뉴 루프·중단 처리 · `play_quiz`/`add_quiz`/`list_quizzes`/`show_score`/`delete_quiz`/`show_history` → 메뉴 기능 · `_record_result` → 최고 점수 갱신 · `load`/`save` → 저장 시점 결정 |
| `StateStorage` | storage.py | `state.json` 파일을 안전하게 읽고 쓴다 | `load` → 읽기·검증·상태값 반환 · `save` → 임시 파일에 쓴 뒤 교체 · `_backup_corrupted_file` → 손상본 백업 |

### 5-3. 클래스를 사용한 이유 (함수만 쓸 때와 비교)
- **데이터와 동작을 한곳에 묶습니다.** 퀴즈를 dict로만 다루면 `quiz["answer"]` 같은 키 접근과 정답 확인 함수가 여러 파일에 흩어집니다. `Quiz` 클래스는 문제·선택지·정답(속성)과 출력·정답 확인(메서드)을 함께 가지고 있어, 퀴즈 관련 코드를 `quiz.py` 한 곳에서 찾을 수 있습니다.
- **잘못된 데이터가 생기지 않게 막습니다.** `Quiz.__init__`이 생성 시점에 "선택지 4개, 정답 1~4"를 검사합니다. 그래서 프로그램 어디서든 `Quiz` 객체라면 형식이 올바르다고 믿고 쓸 수 있습니다.
- **상태를 계속 기억합니다.** 퀴즈 목록, 최고 점수, 기록은 프로그램이 도는 동안 유지되어야 합니다. 함수만 쓰면 전역 변수를 쓰거나 매번 인자로 넘겨야 합니다. `QuizGame`은 이 값들을 `self.quizzes`, `self.best_score`, `self.history` 속성으로 보관하고, 모든 메서드가 `self`로 같은 상태를 공유합니다.
- **부품을 바꿔 끼우기 쉽습니다.** `QuizGame(storage=StateStorage(임시경로))`처럼 저장소 객체를 넘겨받기 때문에, 테스트에서는 실제 `state.json` 대신 임시 파일을 씁니다. 나중에 저장 방식을 바꿀 때도 `StateStorage`만 교체하면 됩니다.
- **단점도 있습니다.** 파일과 코드량이 늘고, 처음 보는 사람은 클래스 사이의 관계를 먼저 이해해야 합니다. 그래서 **지켜야 할 상태가 없는 입력 검증은 클래스 없이 함수로 두었습니다**(`input_utils.py`). 상태와 규칙이 있으면 클래스로, 입력→출력만 있으면 함수로 나눈 것이 이 프로젝트의 기준입니다.

### 5-4. 입력 검증과 데이터 입출력을 분리한 이유
- **바뀌는 이유가 다릅니다.** 입력 규칙(안내 문구, 허용 범위)은 화면 요구에 따라 바뀌고, 저장 방식(JSON → DB 등)은 데이터 요구에 따라 바뀝니다. 파일을 나눠 두면 한쪽을 고칠 때 다른 쪽을 건드리지 않습니다.
- **`StateStorage`는 화면에 아무것도 출력하지 않습니다.** 결과를 `"loaded"`/`"missing"`/`"corrupted"`/`"error"` 같은 상태값으로만 돌려주고, 사용자에게 어떤 메시지를 보여줄지는 `QuizGame.load`가 정합니다. 그래서 안내 문구를 바꿔도 저장 코드는 그대로입니다.
- **따로 테스트할 수 있습니다.** 입력 함수는 `input()`을 가짜로 바꿔(mock) 테스트하고, 저장소는 임시 폴더의 파일로 테스트합니다. 서로 의존하지 않아서 실패 원인을 바로 찾을 수 있습니다.

## 6. 데이터 파일 설명 (`state.json`)

### 6-1. 개요
| 항목 | 내용 |
|---|---|
| 경로 | 프로젝트 루트 `./state.json` (`storage.py`와 같은 폴더, `storage.DEFAULT_STATE_PATH`) |
| 인코딩 | UTF-8 (`ensure_ascii=False`라 한글이 그대로 저장됨) |
| 역할 | 퀴즈 목록, 최고 점수, 모든 게임 기록을 보관해서 다시 실행해도 유지 |
| 읽는 시점 | 프로그램 시작 시 1회 (`QuizGame.run` → `load`) |
| 쓰는 시점 | 첫 실행(파일 없음), 손상 복구 직후, 퀴즈 추가·삭제, 한 판 종료, 메뉴 종료, Ctrl+C/EOF 종료 |
| 안전 장치 | 임시 파일(`state.json.tmp`)에 먼저 쓴 뒤 `os.replace`로 교체해서, 저장 중 중단돼도 기존 파일이 깨지지 않음 |
| Git | 실행할 때마다 바뀌는 데이터라 `.gitignore`로 제외 |

### 6-2. 스키마와 필드 설계 의도
```json
{
  "version": 1,
  "quizzes": [
    {
      "question": "'감다살'의 뜻으로 알맞은 것은?",
      "choices": ["감기가 다 나아서 살 것 같다", "감 다 살아있네, 센스가 좋다", "감자를 다 살 수 있다", "감정이 다 살아나서 울컥한다"],
      "answer": 2,
      "hint": "'감'은 감각·센스를 말해요. 칭찬할 때 써요."
    }
  ],
  "best_score": 70,
  "best_record": {
    "played_at": "2026-11-20T19:00:00", "total": 5, "correct": 4,
    "hints_used": 1, "hinted_correct": 1, "score": 70
  },
  "history": [
    {
      "played_at": "2026-11-20T19:00:00", "total": 5, "correct": 4,
      "hints_used": 1, "hinted_correct": 1, "score": 70
    }
  ]
}
```

| 필드 | 타입 | 설명 | 설계 의도 |
|---|---|---|---|
| `version` | int | 데이터 형식 버전 (현재 1) | 나중에 필드 구조가 바뀌면 버전을 보고 예전 파일을 변환(마이그레이션)할 수 있게 함 |
| `quizzes` | list | 퀴즈 목록 | 기본 퀴즈와 사용자가 추가한 퀴즈를 구분 없이 한 목록에 두어, 삭제·추가 결과가 그대로 유지되게 함 |
| `quizzes[].question` | str | 문제 (빈 문자열 불가) | |
| `quizzes[].choices` | list[str] | 선택지, 정확히 4개 | 선택지 순서가 곧 번호(1~4)라 순서를 보존하는 list 사용 |
| `quizzes[].answer` | int | 정답 번호 1~4 | 선택지 문자열이 아닌 번호로 저장해, 선택지 문구를 고쳐도 정답이 깨지지 않게 함 |
| `quizzes[].hint` | str | 힌트 (없으면 `""`) | 힌트가 없는 퀴즈도 같은 형태로 다루려고 `null` 대신 빈 문자열 사용 |
| `best_score` | int \| null | 최고 점수 0~100, 기록이 없으면 `null` | 0점과 "아직 안 풂"을 구분하려고 `null` 사용 |
| `best_record` | object \| null | 최고 점수를 낸 판의 상세 기록 | 점수 확인 화면에서 "5문제 중 4문제 정답, 힌트 1회"까지 보여주기 위함 |
| `history` | list | 모든 게임 기록 (오래된 순) | 보너스 '점수 기록 히스토리'용. 평균 점수와 최근 기록 표시에 사용 |
| `history[].played_at` | str | 플레이 일시 (ISO 8601) | JSON에는 날짜 타입이 없어 정렬 가능한 ISO 문자열로 저장 |
| `history[].total` / `correct` | int | 출제 문항 수 / 맞힌 수 | 문제 수를 고를 수 있어 판마다 분모가 다르므로 함께 저장 |
| `history[].hints_used` / `hinted_correct` | int | 힌트를 본 문제 수 / 힌트를 보고 맞힌 수 | 점수를 다시 계산·검증할 수 있도록 차감 근거를 남김 |
| `history[].score` | int | 점수 0~100 | 목록·평균 계산 때 매번 재계산하지 않도록 결과를 저장 |

형식이 하나라도 틀리면(선택지 3개, 정답 5번, `best_score`가 `true` 등) 손상된 파일로 판단합니다(`StateStorage._normalize_state`).

### 6-3. 불러오기 흐름 (`QuizGame.load`)
```
StateStorage.load()
 ├─ "loaded"    → Quiz 객체로 변환해 상태 복원 → "📂 저장된 데이터를 불러왔습니다 (퀴즈 N개, 최고점수 X점)"
 ├─ "missing"   → 기본 퀴즈 12개로 시작 → 즉시 저장해 state.json 생성
 ├─ "corrupted" → 손상본을 state.json.bak으로 복사 → 기본 퀴즈로 초기화 → 즉시 저장
 └─ "error"     → 기본 퀴즈로 시작하되, 시작 시점에는 저장하지 않음 (읽지 못한 파일을 덮어쓰지 않기 위해)
```
`StateStorage.load`는 어떤 경우에도 예외를 밖으로 던지지 않고 상태값만 돌려주므로, 파일 문제로 프로그램이 멈추지 않습니다.

### 6-4. 저장 흐름과 저장 실패 시 복구 절차
1. `QuizGame.to_state()`가 현재 상태를 dict로 만듭니다.
2. `StateStorage.save()`가 형식을 검증하고 `state.json.tmp`에 쓴 뒤, `os.replace`로 `state.json`과 바꿉니다.
3. 쓰기 중 오류가 나면 임시 파일을 지우고 `False`를 돌려줍니다. **기존 `state.json`은 바뀌지 않습니다.**
4. `QuizGame.save()`는 실패하면 아래처럼 안내합니다.
   ```
   ⚠️ 데이터를 파일에 저장하지 못했습니다.
      → state.json이 있는 폴더의 쓰기 권한과 디스크 여유 공간을 확인한 뒤 다시 실행해 주세요.
      → 기존 state.json은 그대로 남아 있어 마지막으로 저장된 상태는 보존됩니다.
   ```
5. **사용자 복구 절차**: 프로그램을 종료하고 → 폴더 권한(`ls -l`)과 디스크 공간을 확인한 뒤 → 다시 실행하면 마지막으로 저장된 상태부터 이어집니다. 종료 중(Ctrl+C) 저장에 실패해도 같은 안내가 나옵니다.

### 6-5. 손상 파일 백업 정책
- 손상을 감지하면 원본을 **`state.json.bak` 1개**로 복사한 뒤 기본 데이터로 복구합니다(`StateStorage._backup_corrupted_file`).
- **가장 최근 손상본 1개만 보관합니다.** 다시 손상이 감지되면 `.bak`을 새 손상본으로 덮어씁니다. 이전 백업을 남기려면 직접 다른 이름(예: `state.json.bak.1`)으로 복사해 두세요.
- 백업 파일도 실행 데이터라 `.gitignore`로 Git에서 제외합니다.
- **수동 복구 방법**: `state.json.bak`을 열어 잘못된 부분(예: 선택지 개수)을 고친 뒤 `state.json`으로 이름을 바꾸고 다시 실행합니다.

### 6-6. JSON을 선택한 이유 (다른 방식과 비교)
| 방식 | 장점 | 이 프로젝트에서의 단점 | 판단 |
|---|---|---|---|
| **JSON** | 표준 `json` 모듈로 바로 사용, list·dict 중첩 구조를 그대로 저장, 사람이 열어 읽고 고칠 수 있음 | 아래 6-7의 한계 | **선택** |
| CSV | 표 형태라 엑셀로 보기 쉬움 | 한 줄 = 평면 행이라 "퀴즈 안의 선택지 4개", "기록 목록" 같은 중첩 구조를 담기 어렵고, 쉼표가 들어간 선택지 처리도 번거로움 | 부적합 |
| SQLite (`sqlite3`) | 표준 라이브러리, 대용량·검색·부분 수정에 강함 | 테이블 설계와 SQL이 필요하고, 데이터가 수십 KB 수준이라 과함 | 규모가 커지면 고려 |
| pickle | 파이썬 객체를 그대로 저장 | 사람이 읽을 수 없고, 신뢰할 수 없는 파일을 열면 보안 위험 | 부적합 |

### 6-7. JSON 저장 방식의 한계와 대안
| 한계 | 설명 | 대안 |
|---|---|---|
| 매번 파일 전체를 읽고 씀 | 기록 하나만 추가해도 `state.json` 전체를 다시 씁니다. `history`가 계속 쌓이므로 판 수에 비례해 저장 시간과 메모리 사용이 늘어납니다. (기록 1건 ≈ 160바이트라 1만 판이면 약 1.6MB로 아직 문제는 없음) | 기록 개수 상한을 두거나, 오래된 기록을 별도 파일로 분리. 추가만 하는 기록은 JSON Lines(한 줄에 1건 append) 방식 |
| 부분 검색·수정 불가 | "점수 80점 이상 기록만"처럼 조건 검색을 하려면 전체를 불러와 파이썬에서 걸러야 합니다. | SQLite로 바꾸면 SQL로 검색·부분 수정 가능 |
| 동시 실행 보호 없음 | 프로그램을 두 개 동시에 실행하면 나중에 저장한 쪽이 앞의 내용을 덮어씁니다(파일 잠금 없음). | 파일 잠금 또는 DB 트랜잭션 사용 |
| 스키마 강제 없음 | JSON 자체는 "선택지는 4개" 같은 규칙을 모릅니다. 그래서 `StateStorage._normalize_state`에서 직접 검증합니다. | JSON Schema 또는 DB 제약 조건 |
| 날짜 타입 없음 | 날짜를 문자열(ISO 8601)로 저장하고 읽을 때 해석해야 합니다. | DB의 날짜 타입 |

현재 규모(퀴즈 수십 개, 개인 플레이 기록)에서는 JSON의 단순함이 더 큰 장점이라고 판단했습니다. 데이터가 커지면 `StateStorage`만 SQLite 버전으로 바꾸면 됩니다(5-4, 8장 참고).

## 7. 실행 화면

> 이미지와 같은 실행의 **텍스트 원문**은 [docs/RUN_LOG.md](docs/RUN_LOG.md)에 있습니다.

| 메뉴 (잘못된 입력 처리 포함) | 퀴즈 풀기 |
|---|---|
| ![메뉴](docs/screenshots/menu.png) | ![퀴즈 풀기](docs/screenshots/play.png) |

| 퀴즈 추가 | 점수 확인 |
|---|---|
| ![퀴즈 추가](docs/screenshots/add_quiz.png) | ![점수 확인](docs/screenshots/score.png) |

| 퀴즈 목록 | 게임 기록 |
|---|---|
| ![퀴즈 목록](docs/screenshots/list.png) | ![게임 기록](docs/screenshots/history.png) |

| 개발 환경 | Git 이력 (`git log --oneline --graph`) |
|---|---|
| ![개발 환경](docs/screenshots/dev_env.png) | ![Git 이력](docs/screenshots/git_log.png) |

실행 순서: 첫 실행(퀴즈 추가) → 다시 실행(퀴즈 풀기, 최고 점수 33점 → 70점 갱신) → 다시 실행(저장 데이터 복원, 잘못된 입력 처리, 점수/목록/기록)

## 8. 요구사항 변경 시 영향 범위

요구사항이 바뀔 때 고쳐야 하는 파일과 메서드입니다. 책임을 클래스별로 나눠 두어, 대부분의 변경이 한두 곳에서 끝납니다.

| 변경 요구 (예시) | 수정할 곳 | 함께 확인할 곳 |
|---|---|---|
| 선택지를 4개 → 5개로 | `quiz.py`의 `CHOICE_COUNT` (Quiz 검증, `QuizSession` 정답 범위, `QuizGame.add_quiz` 입력이 모두 이 상수를 사용) | `storage.py` `_normalize_quiz`의 `4` (저장소는 Quiz에 의존하지 않도록 따로 둠), `default_quizzes.py` 데이터, `tests/test_quiz.py`, `tests/test_storage.py` |
| 힌트 차감 비율 50% → 30% | `QuizSession.calculate_score` | `QuizSession.play`의 안내 문구, README 4장 점수 규칙, `tests/test_quiz_session.py` 점수 테스트 |
| 새 메뉴 추가 (예: 퀴즈 수정) | `QuizGame.__init__`의 `menu_items`에 `(이름, 메서드)` 추가 + 메서드 구현 | 메뉴 번호와 입력 범위는 `len(menu_items)`로 자동 계산되어 수정 불필요 |
| 저장 방식을 SQLite로 | `storage.py`의 `StateStorage` 내부만 교체 (`load`/`save`의 입출력 약속 유지) | `QuizGame`은 수정 불필요, `tests/test_storage.py` |
| 저장 파일 위치 변경 | `storage.py`의 `DEFAULT_STATE_PATH` | README 6장 |
| 퀴즈에 '카테고리' 필드 추가 | `Quiz.__init__`/`to_dict`/`from_dict`, `StateStorage._normalize_quiz`, `QuizGame.add_quiz` 입력 | `version`을 2로 올리고 예전 파일 변환 처리, `default_quizzes.py` |
| 기록 표시 개수 10 → 20 | `QuizGame.HISTORY_DISPLAY_LIMIT` | `tests/test_quiz_game_management.py` |
| 힌트 입력 키 `h` → `?` | `QuizSession.HINT_KEY` | 안내 문구는 상수를 쓰므로 자동 반영 |
| 입력 오류 안내 문구 변경 | `input_utils.read_int` / `read_text` | 메시지를 확인하는 테스트(`tests/test_input_utils.py`, `tests/test_quiz_game_run.py`) |
| 기본 퀴즈 교체 | `default_quizzes.py`의 `_DEFAULT_QUIZ_DATA` | 기존 사용자는 `state.json`이 우선이므로, 새 기본 퀴즈를 보려면 `state.json`을 지우고 실행 |

## 9. 개발 과정 (Git)

> 명령 실행 결과 원문은 [docs/GIT_EVIDENCE.md](docs/GIT_EVIDENCE.md)에 텍스트로 정리했습니다.

### 9-1. 원격 저장소와 커밋
- 원격 저장소: `origin  https://github.com/ll-0l/E1-2-dev-workstation.git` (Public)
- 의미 있는 커밋(병합 커밋 제외) **30개 이상**. 확인 명령: `git log --no-merges --oneline | wc -l`
- Git 기초 명령어 7종 사용: `init`(저장소 생성) · `add`/`commit`(기능 단위 커밋) · `push`(GitHub 업로드) · `checkout -b`(브랜치 생성) · `clone`(별도 폴더 복제) · `pull`(변경 받아오기)

### 9-2. 커밋 규칙과 예시
- 형식: `Feat:` 기능 / `Fix:` 버그 수정 / `Docs:` 문서 / `Refactor:` 구조 개선 / `Test:` 테스트 / `Chore:` 설정. 제목은 한국어 요약, 본문에 변경 내용을 적습니다.
- 원칙: **기능 1개 = 커밋 1개**. 예시:
  - `e936301 Feat: 퀴즈 추가 기능 구현`
  - `af6c4f5 Feat: 퀴즈 목록 기능 구현`
  - `4d173df Feat: 점수 확인 및 최고 점수 갱신 기능 구현`
  - `52394a2 Fix: 점수 반올림을 사사오입으로 통일`
  - `b7ccff4 Refactor: QuizGame 책임 분리 및 구조 정리`
  - `d2dc663 Docs: README 작성 (개요/주제 선정 이유/실행 방법/기능/파일 구조/state.json)`

### 9-3. 브랜치 전략과 병합 기록
`main`은 항상 실행 가능한 상태로 두고, 기능은 브랜치에서 만든 뒤 `--no-ff`로 병합해 그래프에 기록이 남게 했습니다.

| 브랜치 | 작업 내용 | 병합 커밋 |
|---|---|---|
| `feature/quiz-model` | Quiz 클래스, 기본 퀴즈 데이터 | `808c6d1` |
| `feature/play-quiz` | 퀴즈 풀기 (랜덤 출제, 문제 수 선택, 힌트) — 과제의 "퀴즈 풀기 브랜치" | `d687507` |
| `feature/storage` | state.json 저장/불러오기, 단위 테스트 | `c5a0234` |
| `test/storage-integration` | QuizGame 저장 연동 테스트 | `66ed4f7` |
| `fix/player-qa` | QA 반영 (점수 반올림, 오답 안내, 퀴즈 문구) | `859225d` |
| `test/quiz-management` | 퀴즈 삭제·기록 테스트 | `da98498` |

### 9-4. clone / pull 실습
1. `git clone`으로 별도 폴더(`E1-2-dev-workstation-clone`)에 저장소를 복제했습니다.
2. 복제한 폴더에서 README에 이 섹션을 추가하고 commit → push 했습니다 (`e0c3f89 Docs: README에 clone/pull 실습 기록 추가`).
3. 원래 작업 폴더에서 `git pull`로 받아 Fast-forward로 반영된 것을 확인했습니다 (reflog: `e0c3f89 HEAD@{..}: pull: Fast-forward`).
4. 재평가용으로 같은 과정을 한 번 더 수행하고 모든 명령 출력을 [docs/GIT_EVIDENCE.md](docs/GIT_EVIDENCE.md)에 남겼습니다.

### 9-5. 협업 방식
AI 코딩 에이전트 3개(Claude Code 2개, Codex 1개)가 담당 파일을 나눠 각자 clone한 폴더에서 브랜치로 작업했고, Lead가 검토 후 `main`에 병합했습니다. 역할과 인터페이스 약속은 [AGENTS.md](AGENTS.md)에 있습니다.
