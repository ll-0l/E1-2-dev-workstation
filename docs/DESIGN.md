# 설계 문서

README에서 요약만 다룬 설계 내용을 자세히 정리한 문서입니다. 데이터 파일(`state.json`)의 상세는 [DATA.md](DATA.md), 실제 실행 결과는 [RUN_LOG.md](RUN_LOG.md)에 있습니다.

## 1. 입력·예외 처리
모든 숫자 입력은 `input_utils.read_int`, 문자열 입력은 `read_text`/`read_line`을 거칩니다.

| 상황 | 화면 메시지 | 처리 / 사용자 권장 조치 | 검증 테스트 |
|---|---|---|---|
| 입력 앞뒤 공백 (` 1 `) | (없음) | 공백을 지우고 정상 처리 | `test_read_line_strips_input`, `test_menu_rejects_text_out_of_range_and_empty_then_quits` |
| 숫자가 아닌 입력 (`abc`) | ⚠️ 잘못된 입력입니다. 1-7 사이의 숫자를 입력하세요. | 같은 질문을 다시 물음 | `test_read_int_retries_and_accepts_keyword_case_insensitively`, `test_menu_rejects_...` |
| 범위 밖 숫자 (메뉴 `9`, 정답 `0`) | ⚠️ 잘못된 입력입니다. (범위) 사이의 숫자를 입력하세요. | 같은 질문을 다시 물음 | `test_menu_rejects_...` |
| 빈 입력 (Enter) | ⚠️ 입력이 비어 있습니다. 1-7 사이의 숫자를 입력하세요. / ⚠️ 입력이 비어 있습니다. 내용을 입력하세요. | 같은 질문을 다시 물음 | `test_read_text_retries_empty_input`, `test_menu_rejects_...` |
| `Ctrl+C` / 입력 스트림 종료(EOF) | ⚠️ 입력이 중단되어 프로그램을 종료합니다. | 저장 후 정상 종료(트레이스백 없음) | `test_keyboard_interrupt_saves_and_exits_without_traceback`, `test_eof_saves_and_exits_without_traceback` |
| 퀴즈 0개 상태에서 풀기·목록·삭제 | 📭 등록된 퀴즈가 없습니다. | '퀴즈 추가'로 먼저 등록 | `test_delete_returns_without_input_when_empty` |
| 플레이 기록 없이 점수·기록 확인 | 📭 아직 퀴즈를 풀지 않았습니다. / 게임 기록이 없습니다. | '퀴즈 풀기'로 첫 기록 생성 | `test_show_history_handles_empty_history` |
| `state.json` 없음 (첫 실행) | 📂 저장된 데이터가 없어 기본 퀴즈 12개로 시작합니다. | 기본 퀴즈로 시작하고 파일 생성 | `test_missing_state_saves_default_quizzes`, `test_missing_file` |
| `state.json` 손상 (JSON 문법 오류, 선택지 3개 등) | ⚠️ 데이터 파일이 손상되어 기본 퀴즈로 복구합니다. (원본은 state.json.bak에 백업) | 기본 퀴즈로 복구, 원본은 `.bak`으로 보관 → [DATA 5장](DATA.md#5-손상-파일-백업-정책) | `test_malformed_json_is_backed_up`, `test_invalid_quiz_is_backed_up_as_corrupted`, `test_corrupted_state_resets_runtime_state_and_saves` |
| `state.json` 읽기 오류 (권한 등) | ⚠️ 데이터 파일을 읽을 수 없어 기본 퀴즈로 시작합니다. (기존 파일 보호를 위해 이번 실행 내용은 저장하지 않습니다) | **보호 모드**: 이번 실행 동안 저장을 모두 생략해 원본을 덮어쓰지 않음. 권한(`ls -l state.json`)을 고친 뒤 다시 실행 | `test_read_error_blocks_all_later_saves`, `test_load_os_error` |
| 더 새로운 버전 프로그램이 만든 `state.json` | ⚠️ 데이터 파일이 더 새로운 버전의 프로그램에서 만들어졌습니다. (…저장하지 않습니다) | 손상으로 보지 않고 백업·덮어쓰기 없이 **보호 모드**. 최신 버전 프로그램으로 실행 | `test_future_version_is_unsupported_and_left_untouched`, `test_unsupported_version_enters_read_only_mode` |
| `state.json` 쓰기 오류 | ⚠️ 데이터를 파일에 저장하지 못했습니다. + 조치 안내 2줄 (+ 추가·삭제 직후면 "이번 실행 중에만 유지" 1줄) | 기존 파일은 보존됨 → [DATA 4장](DATA.md#4-저장-흐름과-저장-실패-시-복구-절차) | `test_save_serializes_quizzes_and_reports_failure`, `test_save_replace_error_removes_temporary_file`, `test_add_quiz_warns_when_save_fails` |

> 위 상황들의 실제 실행 원문은 [RUN_LOG 4장 "예외 흐름 사례"](RUN_LOG.md#4-예외-흐름-사례)에 사례별로 정리했습니다.

## 2. 안내 문구 형식
모든 안내는 **맨 앞 아이콘으로 종류를 구분**하고, 경고는 항상 "무엇이 문제인지 → 무엇을 하면 되는지" 순서로 씁니다. 새 메시지를 추가할 때도 이 형식을 따릅니다.

| 아이콘 | 종류(수준) | 형식 | 예시 |
|---|---|---|---|
| ⚠️ | 입력 오류 (경고, 재입력) | `⚠️ {문제}. {해야 할 입력}.` | ⚠️ 잘못된 입력입니다. 1-4 사이의 숫자를 입력하세요. |
| ⚠️ | 데이터 파일 문제 (경고, 자동 처리) | `⚠️ {문제}되어 {프로그램이 한 처리}. ({부가 정보})` | ⚠️ 데이터 파일이 손상되어 기본 퀴즈로 복구합니다. (원본은 state.json.bak에 백업) |
| ⚠️ | 저장 실패 (오류, 사용자 조치 필요) | 1줄 `⚠️ {문제}.` + 들여쓴 `→ {조치}` 줄들 | ⚠️ 데이터를 파일에 저장하지 못했습니다.<br>   → …쓰기 권한과 디스크 여유 공간을 확인한 뒤 다시 실행해 주세요. |
| 📭 | 빈 상태 (안내) | `📭 {없는 것}. '{메뉴}'에서/로 {다음 행동}` | 📭 등록된 퀴즈가 없습니다. '퀴즈 추가'에서 먼저 퀴즈를 등록하세요. |
| 📂 | 데이터 불러오기 결과 (정보) | `📂 {결과}. ({요약})` | 📂 저장된 데이터를 불러왔습니다. (퀴즈 13개, 최고점수 70점) |
| ✅ / 🗑️ / ↩️ | 작업 완료 / 삭제 / 취소 | `{아이콘} {무엇이} {어떻게 됐는지}. ({현재 개수})` | ✅ 퀴즈가 추가되었습니다! (총 13개) |
| ✅ / ❌ / 💡 | 정답 / 오답 / 힌트 | 오답이면 정답 번호와 내용을 함께 표시 | ❌ 오답입니다. 정답은 1번 (…)입니다. |
| 🎉 / 🏆 | 점수 갱신 / 현재 최고 점수 | | 🎉 새로운 최고 점수입니다! |

입력 오류 문구는 `input_utils.read_int`/`read_text`와 `QuizGame._confirm` 세 곳에서만 만들어, 화면마다 문구가 달라지지 않게 했습니다.

**입력 질문(프롬프트) 형식** — 메뉴와 모든 입력 질문은 `{질문} ({허용 값}): ` 모양으로 끝나, 무엇을 넣어야 하는지 질문 안에서 알 수 있게 했습니다.

| 화면 | 프롬프트 | 허용 값 표시 |
|---|---|---|
| 메뉴 | `선택: ` | 메뉴 번호가 바로 위에 나열됨 |
| 문제 수 | `몇 문제를 풀까요? (1-12): ` | 범위 |
| 정답 | `정답 입력 (1-4, 힌트: h): ` | 범위 + 특수 키 |
| 퀴즈 추가 | `정답 번호 (1-4): `, `힌트 (없으면 Enter): ` | 범위 / 생략 가능 여부 |
| 삭제 | `삭제할 퀴즈 번호 (1-13, 취소: 0): `, `이 퀴즈를 삭제할까요? (y/n): ` | 범위 + 취소 키 / 선택지 |

## 3. 클래스 역할과 책임
| 클래스 | 파일 | 책임 (한 문장) | 주요 메서드 → 하는 일 |
|---|---|---|---|
| `Quiz` | quiz.py | 문제 1개의 데이터와 규칙을 가진다 | `__init__` → 형식 검증 · `display` → 문제 출력 · `is_correct` → 정답 판정 · `to_dict`/`from_dict` → 저장용 변환 |
| `QuizSession` | quiz_session.py | 퀴즈 한 판을 진행하고 채점한다 | `__init__` → 섞기·문항 수 선택 · `play` → 출제·힌트·정답 안내 후 결과 dict 반환 · `calculate_score` → 점수 계산 |
| `QuizGame` | quiz_game.py | 게임 전체 상태를 관리하고 언제 무엇을 할지 정한다 | `run` → 메뉴 루프·중단 처리 · `play_quiz`/`add_quiz`/`list_quizzes`/`show_score`/`delete_quiz`/`show_history` → 메뉴 기능 · `_record_result` → 최고 점수 갱신 · `load`/`save` → 저장 시점 결정 |
| `StateStorage` | storage.py | `state.json` 파일을 안전하게 읽고 쓴다 | `load` → 읽기·검증·상태값 반환 · `save` → 임시 파일에 쓴 뒤 교체 · `_backup_corrupted_file` → 손상본 백업 |

**책임 경계 — 하는 일과 하지 않는 일**

| 클래스 | 하는 일 | 하지 않는 일 (다른 곳 담당) |
|---|---|---|
| `Quiz` | 자기 형식 검증, 문제 출력, 정답 판정 | 사용자 입력 받기(`QuizSession`), 파일 저장(`StateStorage`) |
| `QuizSession` | 출제 순서 섞기, 정답·힌트 입력 받기, 한 판의 점수 계산, 결과 dict 반환 | 최고 점수 비교·기록 누적(`QuizGame`), 파일 저장 |
| `QuizGame` | 메뉴 흐름, 퀴즈 목록 관리, 최고 점수·기록 갱신, **언제 저장할지** 결정, 사용자 안내 문구 | 파일을 **어떻게** 쓰는지(`StateStorage`), 채점 공식(`QuizSession`) |
| `StateStorage` | 파일 읽기/쓰기, 형식 검증, 손상본 백업, 결과를 상태값으로 반환 | 화면 출력, `Quiz` 객체 생성 (dict만 다룸) |

예를 들어 퀴즈 한 판이 끝나면 `QuizSession.play()`는 점수가 담긴 dict를 **돌려주기만** 하고, 그 점수를 최고 점수와 비교해 기록에 넣는 일(`_record_result`)과 저장(`save`)은 `QuizGame`이 합니다.

**클래스 관계도** (화살표 = "사용한다")
```
                         main.py
                            │ QuizGame().run()
                            ▼
  ┌───────────────────── QuizGame ─────────────────────┐
  │ quizzes: list[Quiz]   best_score   history   read_only │
  └──┬─────────────┬───────────────┬───────────────┬──┘
     │ 보관·생성    │ 한 판 진행      │ 메뉴·추가 입력   │ 읽기/쓰기 (dict만)
     ▼             ▼               ▼               ▼
   Quiz ◀─출제── QuizSession ───▶ input_utils     StateStorage ──▶ state.json
  (문제 1개)     (채점, 결과 dict)  (정답 입력 검증)  (검증·백업·버전 변환)
```
처음 읽을 때는 `main.py` → `QuizGame.run()` → 메뉴 메서드 순서로 따라가면 전체 흐름이 보입니다.

**오류 전파 정책 — 어떤 문제를 어디서 처리하나**

| 문제 | 처음 발생하는 곳 | 처리하는 곳 | 처리 방식 |
|---|---|---|---|
| 잘못된 입력 (빈 값, 문자, 범위 밖) | `input()` | `input_utils` | 그 자리에서 안내 후 재입력. 위로 올리지 않음 |
| Ctrl+C / EOF | `input()` | **`QuizGame.run`만** | `input_utils`·`QuizSession`은 잡지 않고 그대로 전달 → `run`이 저장 후 종료 |
| 잘못된 퀴즈 값 (선택지 3개 등) | `Quiz.__init__` | 호출한 쪽 | `ValueError` 발생 → `QuizGame._apply_state`는 손상으로 처리 |
| 파일 없음·손상·권한·미래 버전 | `StateStorage` | `StateStorage` → `QuizGame.load` | 예외를 밖으로 던지지 않고 상태값으로 변환 → `QuizGame`이 안내·복구·보호 모드 결정 |
| 저장 실패 | `StateStorage.save` | `QuizGame.save` | `False`를 받아 안내 문구 출력, 게임은 계속 |

원칙: **사용자에게 말하는 일은 `QuizGame`과 `input_utils`만**, **종료 결정은 `QuizGame.run`만** 합니다.

## 4. 클래스를 사용한 이유 (함수만 쓸 때와 비교)
- **데이터와 동작을 한곳에 묶습니다.** 퀴즈를 dict로만 다루면 `quiz["answer"]` 같은 키 접근과 정답 확인 함수가 여러 파일에 흩어집니다. `Quiz` 클래스는 문제·선택지·정답(속성)과 출력·정답 확인(메서드)을 함께 가지고 있어, 퀴즈 관련 코드를 `quiz.py` 한 곳에서 찾을 수 있습니다.
- **잘못된 데이터가 생기지 않게 막습니다.** `Quiz.__init__`이 생성 시점에 "선택지 4개, 정답 1~4"를 검사합니다. 그래서 프로그램 어디서든 `Quiz` 객체라면 형식이 올바르다고 믿고 쓸 수 있습니다.
- **상태를 계속 기억합니다.** 퀴즈 목록, 최고 점수, 기록은 프로그램이 도는 동안 유지되어야 합니다. 함수만 쓰면 전역 변수를 쓰거나 매번 인자로 넘겨야 합니다. `QuizGame`은 이 값들을 `self.quizzes`, `self.best_score`, `self.history` 속성으로 보관하고, 모든 메서드가 `self`로 같은 상태를 공유합니다.
- **부품을 바꿔 끼우기 쉽습니다.** `QuizGame(storage=StateStorage(임시경로))`처럼 저장소 객체를 넘겨받기 때문에, 테스트에서는 실제 `state.json` 대신 임시 파일을 씁니다. 나중에 저장 방식을 바꿀 때도 `StateStorage`만 교체하면 됩니다.
- **단점도 있습니다.** 파일과 코드량이 늘고, 처음 보는 사람은 클래스 사이의 관계를 먼저 이해해야 합니다. 그래서 **지켜야 할 상태가 없는 입력 검증은 클래스 없이 함수로 두었습니다**(`input_utils.py`). 상태와 규칙이 있으면 클래스로, 입력→출력만 있으면 함수로 나눈 것이 이 프로젝트의 기준입니다.

**Quick start — 클래스를 직접 써 보기** (진입 장벽을 낮추기 위한 예시, 프로젝트 폴더에서 `python3` 실행 후 입력)
```python
>>> from quiz import Quiz
>>> from quiz_session import QuizSession
>>> q = Quiz("'밤티'의 뜻은?", ["좋다", "별로다", "밤에 입는 티", "빛난다"], answer=2, hint="부정적인 평가예요")
>>> q.is_correct(2), q.is_correct(1)        # 메서드: 객체가 자기 정답으로 판정
(True, False)
>>> q.to_dict()["answer"]                    # 속성은 저장용 dict로 변환
2
>>> Quiz("문제", ["가", "나", "다"], 1)         # __init__이 잘못된 객체 생성을 막음
ValueError: 선택지는 정확히 4개여야 합니다.
>>> QuizSession.calculate_score(correct=4, hinted_correct=1, total=5)
70
```
게임 전체는 `QuizGame(StateStorage("다른경로/state.json")).run()`처럼 저장 위치를 바꿔 실행해 볼 수 있어, 실제 데이터를 건드리지 않고 연습할 수 있습니다.

## 5. 입력 검증과 데이터 입출력을 분리한 이유
- **바뀌는 이유가 다릅니다.** 입력 규칙(안내 문구, 허용 범위)은 화면 요구에 따라 바뀌고, 저장 방식(JSON → DB 등)은 데이터 요구에 따라 바뀝니다. 파일을 나눠 두면 한쪽을 고칠 때 다른 쪽을 건드리지 않습니다.
- **`StateStorage`는 화면에 아무것도 출력하지 않습니다.** 결과를 `"loaded"`/`"missing"`/`"corrupted"`/`"error"` 같은 상태값으로만 돌려주고, 사용자에게 어떤 메시지를 보여줄지는 `QuizGame.load`가 정합니다. 그래서 안내 문구를 바꿔도 저장 코드는 그대로입니다.
- **따로 테스트할 수 있습니다.** 입력 함수는 `input()`을 가짜로 바꿔(mock) 테스트하고, 저장소는 임시 폴더의 파일로 테스트합니다. 서로 의존하지 않아서 실패 원인을 바로 찾을 수 있습니다. 어떤 테스트가 어떤 책임을 검증하는지는 아래 [6장](#6-테스트-매핑-책임--테스트)에 있습니다.

**경계 상황에서 두 쪽이 어떻게 맞물리나**

| 상황 | 입력 쪽 | 저장 쪽 | 결과 |
|---|---|---|---|
| 퀴즈 추가 중 정답 번호를 계속 틀리게 입력 | `read_int`가 올바른 값이 올 때까지 재입력 | 아직 호출되지 않음 | 검증을 통과한 값만 `Quiz`가 되어 저장됨 |
| 퀴즈 추가 중 문제만 쓰고 Ctrl+C | 입력 중단 신호를 그대로 전달 | `run`이 **추가 전 상태**를 저장 | 반쯤 입력한 퀴즈는 남지 않음 |
| 퀴즈 추가는 성공했는데 저장 실패 | 정상 | `save()`가 `False` | 목록에는 보이지만 "이번 실행 중에만 유지" 안내 |
| 보호 모드에서 퀴즈 추가 | 정상 | 저장 생략 | 위와 같은 안내, 원본 파일 그대로 |

## 6. 테스트 매핑 (책임 ↔ 테스트)
`python3 -m unittest discover -s tests -v`로 61개를 실행합니다. 실제 `state.json`은 건드리지 않고 모두 임시 폴더를 씁니다.

| 테스트 파일 | 검증하는 책임 | 개수 | 대표 테스트 |
|---|---|---:|---|
| `test_input_utils.py` | **입력 검증**: 공백 제거, 빈 입력·문자·범위 밖 재입력, 허용 키워드(`h`), EOF 전파, 디버그 로그 기록 | 6 | `test_read_int_retries_and_accepts_keyword_case_insensitively` |
| `test_quiz_game_run.py` | **메뉴 입력과 종료**: 메뉴 오입력 재요청, Ctrl+C/EOF 저장 후 종료, 저장 실패 안내, 재시작 후 유지 | 5 | `test_keyboard_interrupt_saves_and_exits_without_traceback` |
| `test_quiz.py` | **Quiz 규칙**: 생성 검증, 정답 판정, dict 변환, 기본 퀴즈 형식 | 5 | `test_validation_rejects_invalid_values` |
| `test_quiz_session.py` | **채점**: 점수 공식·사사오입, 문항 수 검증, 셔플 재현성, 힌트 1회 차감 | 5 | `test_score_rounds_half_up_at_half_point_boundaries` |
| `test_quiz_game_management.py` | **퀴즈 관리·기록**: 삭제 취소/확인/저장, 기록 최신순·평균·최고 표시, 최고 점수 갱신 조건, 기록 1,000건 롤링 | 8 | `test_record_result_updates_only_for_strictly_higher_score` |
| `test_storage.py` | **데이터 입출력**: 파일 없음, 손상 JSON·스키마 오류 백업, 백업 보존 정책, 수동 복구, UTF-8 왕복, 원자적 저장 실패, **버전 마이그레이션·미래 버전 보호·강제 종료 후 남은 임시 파일** | 17 | `test_migration_upgrades_old_version_step_by_step` |
| `test_quiz_game_storage.py` | **저장 연동**: load 상태별 처리(loaded/missing/corrupted/error/unsupported), 보호 모드, 저장 실패 안내 | 8 | `test_read_error_blocks_all_later_saves` |
| `test_validate_quizzes.py` | **퀴즈 검증 도구**: 기본 퀴즈 통과, 중복·힌트 누락·같은 선택지·형식 오류 검출, 개수 부족, 정답 쏠림 경고 | 4 | `test_detects_each_kind_of_error` |
| `test_restore_backup.py` | **백업 복원 도구**: 백업 없음, 손상된 백업 복원 거부, 정상 백업 복원과 이전 파일 보관 | 3 | `test_valid_backup_is_restored_and_current_file_kept` |

## 7. 요구사항 변경 시 영향 범위
요구사항이 바뀔 때 고쳐야 하는 파일과 메서드입니다. 책임을 클래스별로 나눠 두어, 대부분의 변경이 한두 곳에서 끝납니다.

| 변경 요구 (예시) | 수정할 곳 | 함께 확인할 곳 |
|---|---|---|
| 선택지를 4개 → 5개로 | `quiz.py`의 `CHOICE_COUNT` (Quiz 검증, `QuizSession` 정답 범위, `QuizGame.add_quiz` 입력이 모두 이 상수를 사용) | `storage.py` `_normalize_quiz`의 `4` (저장소는 Quiz에 의존하지 않도록 따로 둠), `default_quizzes.py` 데이터, `tests/test_quiz.py`, `tests/test_storage.py` |
| 힌트 차감 비율 50% → 30% | `QuizSession.calculate_score` | `QuizSession.play`의 안내 문구, README 4장 점수 규칙, `tests/test_quiz_session.py` 점수 테스트 |
| 새 메뉴 추가 (예: 퀴즈 수정) | `QuizGame.__init__`의 `menu_items`에 `(이름, 메서드)` 추가 + 메서드 구현 | 메뉴 번호와 입력 범위는 `len(menu_items)`로 자동 계산되어 수정 불필요 |
| 저장 방식을 SQLite로 | `storage.py`의 `StateStorage` 내부만 교체 (`load`/`save`의 입출력 약속 유지) | `QuizGame`은 수정 불필요, `tests/test_storage.py` |
| 저장 파일 위치 변경 | `storage.py`의 `DEFAULT_STATE_PATH` | README 6장, [DATA.md](DATA.md) |
| 퀴즈에 '카테고리' 필드 추가 | `Quiz.__init__`/`to_dict`/`from_dict`, `StateStorage._normalize_quiz`, `QuizGame.add_quiz` 입력 | `version`을 2로 올리고 예전 파일 변환 처리, `default_quizzes.py` |
| 기록 표시 개수 10 → 20 | `QuizGame.HISTORY_DISPLAY_LIMIT` | `tests/test_quiz_game_management.py` |
| 힌트 입력 키 `h` → `?` | `QuizSession.HINT_KEY` | 안내 문구는 상수를 쓰므로 자동 반영 |
| 입력 오류 안내 문구 변경 | `input_utils.read_int` / `read_text` | 메시지를 확인하는 테스트(`tests/test_input_utils.py`, `tests/test_quiz_game_run.py`) |
| 기본 퀴즈 교체 | `default_quizzes.py`의 `_DEFAULT_QUIZ_DATA` | 기존 사용자는 `state.json`이 우선이므로, 새 기본 퀴즈를 보려면 `state.json`을 지우고 실행 ([8장 교체 절차](#교체-절차)) |

### 큰 구조 변경 시 영향·리스크와 체크리스트
| 대형 변경 | 영향 범위 | 주요 리스크 | 리스크 줄이는 방법 |
|---|---|---|---|
| 저장소를 SQLite로 전환 | `storage.py`, `tests/test_storage.py` (나머지는 계약 유지로 무수정) | 기존 `state.json` 사용자의 데이터 유실 | 첫 실행 때 JSON → DB 변환, 변환 전 `state.json` 백업 유지 ([DATA 6장 체크리스트](DATA.md#6-json을-선택한-이유-다른-방식과-비교)) |
| 스키마 버전 업 (필드 추가) | `quiz.py`, `storage.py`, `quiz_game.py`, `default_quizzes.py`, 테스트 | 구버전 파일을 손상으로 오판해 기본값으로 덮어씀 | `version` 기반 마이그레이션 + v1 파일 변환 테스트 ([DATA 9장](DATA.md#9-스키마-버전-업-마이그레이션)) |
| 메뉴 구조 개편 (하위 메뉴 등) | `quiz_game.py`의 `menu_items`·`run` | 메뉴 번호 변경으로 사용자 혼란, 종료/중단 처리 누락 | `run`의 `except` 구조 유지, `tests/test_quiz_game_run.py` 확장 |
| 다중 사용자 지원 | `storage.py`(사용자별 파일/테이블), `quiz_game.py`(사용자 선택) | 서로의 기록 덮어쓰기 | 사용자별 파일 분리 또는 DB, 동시 실행 잠금 ([DATA 8장](DATA.md#8-운영-지침-동시-실행과-데이터-관리)) |

**대형 변경 공통 체크리스트** — 자동으로 확인할 수 있는 항목은 `scripts/run_checks.py`(로컬)와 GitHub Actions CI(push마다)가 같은 점검을 수행합니다.
- [ ] 변경 전 `python3 scripts/run_checks.py`가 4/4 통과하는지 확인 (기준선: 문법·테스트·퀴즈 검증·실행)
- [ ] `feature/<이름>` 브랜치에서 작업 (`main`은 항상 실행 가능 상태 유지)
- [ ] AGENTS.md의 인터페이스 계약(`load`/`save` 반환 형태 등)을 바꾸는지 먼저 판단하고, 바꾼다면 문서부터 수정
- [ ] 기존 `state.json`을 가진 사용자가 업그레이드 후에도 데이터를 잃지 않는지 확인 (구버전 파일로 실행해 보기)
- [ ] **테스트 업데이트**: 바뀐 동작의 기대값 수정 + 새 경로(변환·오류) 테스트 추가 → 전체 통과
- [ ] `python3 scripts/run_checks.py` 재실행 → 4/4 통과, `python3 main.py`로 메뉴 1~7과 Ctrl+C 종료를 직접 확인
- [ ] push 후 GitHub Actions(CI)가 Python 3.10·3.12·3.13에서 모두 통과하는지 확인 (`gh run list` 또는 README 상단 배지)
- [ ] README와 docs(DESIGN·DATA·RUN_LOG) 갱신 → `--no-ff`로 `main` 병합

## 8. 기본 퀴즈 선정 기준과 교체 절차
| 기준 | 적용 내용 |
|---|---|
| 출처 | 아시아투데이 [「[카드뉴스] 2026 상반기 신조어 총정리…'신조어 활용 가이드'」](https://www.asiatoday.co.kr/kn/view.php?key=20260723001638281) (2026.07.24)에 실린 24개 표현 중에서만 선정 |
| 제외 | 욕설을 순화한 말(샤갈), 특정 집단을 비하할 수 있는 말(멘헤라) 등 퀴즈로 내기 부적절한 표현은 제외 |
| 중복 | 한 용어당 1문제, 같은 문제 문장 없음 (12문제 모두 서로 다른 용어) |
| 정답 분산 | 정답 번호가 한쪽에 몰리지 않게 1번 3개 · 2번 3개 · 3번 4개 · 4번 2개로 배치 |
| 선택지 | 오답도 그럴듯한 뜻으로 작성하고, 문제 안의 선택지 길이 차이를 6자 이내로 맞춰 정답이 눈에 띄지 않게 함 |
| 난이도 | 별도 등급은 두지 않음. 대신 모든 문제에 힌트를 넣어, 처음 보는 용어도 추론해서 풀 수 있게 함 |

### 교체 절차
기본 퀴즈는 `default_quizzes.py`의 `_DEFAULT_QUIZ_DATA` 목록 한 곳에만 있습니다. ① 이 목록의 dict(문제, 선택지 4개, 정답 번호, 힌트)를 고치고 → ② `python3 scripts/validate_quizzes.py`로 형식(5개 이상, 선택지 4개, 정답 1~4, 힌트, 중복 문제·선택지)을 검사하고(오류가 있으면 번호와 이유를 알려 줌) `python3 -m unittest tests.test_quiz`까지 통과시킨 뒤 → ③ `state.json`을 지우고 실행하면 새 기본 퀴즈로 시작합니다. `state.json`이 있으면 저장된 퀴즈가 우선하므로, 기존 사용자의 데이터는 교체 후에도 그대로 유지됩니다.
