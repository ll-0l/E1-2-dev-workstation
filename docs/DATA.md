# 데이터 파일 상세 (`state.json`)

README 6장에서 요약한 `state.json`의 저장 시점, 필드 설계 의도, 복구 절차, 성능 측정, 마이그레이션을 자세히 정리한 문서입니다.

## 1. 개요
| 항목 | 내용 |
|---|---|
| 경로 | 프로젝트 루트 `./state.json` (`storage.py`와 같은 폴더, `storage.DEFAULT_STATE_PATH`) |
| 인코딩 | UTF-8 (`ensure_ascii=False`라 한글이 그대로 저장됨) |
| 역할 | 퀴즈 목록, 최고 점수, 모든 게임 기록을 보관해서 다시 실행해도 유지 |
| 읽는 시점 | 프로그램 시작 시 1회 (`QuizGame.run` → `load`) |
| 쓰는 시점 | 첫 실행(파일 없음), 손상 복구 직후, 퀴즈 추가·삭제, 한 판 종료, 메뉴 종료, Ctrl+C/EOF 종료 |
| 안전 장치 | 임시 파일(`state.json.tmp`)에 먼저 쓴 뒤 `os.replace`로 교체해서, 저장 중 중단돼도 기존 파일이 깨지지 않음 |
| Git | 실행할 때마다 바뀌는 데이터라 `.gitignore`로 제외 |

**읽기/쓰기 시점 한눈에 보기** — 읽기는 시작할 때 한 번, 쓰기는 "데이터가 바뀌는 순간마다"입니다.

| 시점 | 읽기 | 쓰기 | 코드 |
|---|:---:|:---:|---|
| 프로그램 시작 | ✅ | 파일이 없거나 손상됐을 때만 ✅ | `QuizGame.run` → `load` |
| 퀴즈 추가 직후 | | ✅ | `add_quiz` → `_save_or_warn_unsaved` |
| 퀴즈 삭제 직후 | | ✅ | `delete_quiz` → `_save_or_warn_unsaved` |
| 한 판 종료(점수·기록 갱신) | | ✅ | `play_quiz` → `save` |
| 메뉴 7 종료 | | ✅ | `quit` → `save` |
| Ctrl+C / EOF 종료 | | ✅ | `run`의 `except` → `save` |
| 보호 모드(읽기 오류·미래 버전 파일) | | ❌ 모든 저장 생략 | `save`의 `read_only` 검사 |
| 목록·점수·기록 보기 | | (변경 없음 → 쓰지 않음) | |

> **동시 실행 안전성 요약**: 파일 잠금은 구현하지 않았습니다. **한 폴더에서는 게임을 하나만 실행**하는 것이 권장 설정이며, 이유와 대처법은 [8장 운영 지침](#8-운영-지침-동시-실행과-데이터-관리)에 있습니다.

## 2. 스키마와 필드 설계 의도
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

## 3. 불러오기 흐름 (`QuizGame.load`)
```
StateStorage.load()
 ├─ "loaded"    → Quiz 객체로 변환해 상태 복원 → "📂 저장된 데이터를 불러왔습니다 (퀴즈 N개, 최고점수 X점)"
 ├─ "missing"   → 기본 퀴즈 12개로 시작 → 즉시 저장해 state.json 생성
 ├─ "corrupted" → 손상본을 state.json.bak으로 복사 → 기본 퀴즈로 초기화 → 즉시 저장
 ├─ "unsupported" → (더 새 버전 파일) 기본 퀴즈로 시작, 보호 모드 → 이번 실행 동안 저장 안 함, 원본 그대로
 └─ "error"     → (권한 등 읽기 실패) 기본 퀴즈로 시작, 보호 모드 → 이번 실행 동안 저장 안 함
```
`StateStorage.load`는 어떤 경우에도 예외를 밖으로 던지지 않고 상태값만 돌려주므로, 파일 문제로 프로그램이 멈추지 않습니다.

## 4. 저장 흐름과 저장 실패 시 복구 절차
1. `QuizGame.to_state()`가 현재 상태를 dict로 만듭니다.
2. `StateStorage.save()`가 형식을 검증하고 `state.json.tmp`에 쓴 뒤, `os.replace`로 `state.json`과 바꿉니다.
3. 쓰기 중 오류가 나면 임시 파일을 지우고 `False`를 돌려줍니다. **기존 `state.json`은 바뀌지 않습니다.**
4. `QuizGame.save()`는 실패하면 아래처럼 안내합니다.
   ```
   ⚠️ 데이터를 파일에 저장하지 못했습니다.
      → state.json이 있는 폴더의 쓰기 권한과 디스크 여유 공간을 확인한 뒤 다시 실행해 주세요.
      → 기존 state.json은 그대로 남아 있어 마지막으로 저장된 상태는 보존됩니다.
      → 추가한 퀴즈는 이번 실행 중에만 유지되며, 종료하면 반영되지 않습니다.   ← 추가·삭제 직후일 때만
   ```
5. **사용자 복구 절차**: 프로그램을 종료하고 → 폴더 권한(`ls -l`)과 디스크 공간을 확인한 뒤 → 다시 실행하면 마지막으로 저장된 상태부터 이어집니다. 종료 중(Ctrl+C) 저장에 실패해도 같은 안내가 나옵니다. 실제 실행 원문: [RUN_LOG 4-8](RUN_LOG.md#4-8-저장-불가-상태에서-퀴즈-추가--ctrlc)

**저장 실패 시 바로 할 일 (체크리스트)**
- [ ] 게임을 7번으로 종료한다 (안내가 나와도 기존 `state.json`은 안전함)
- [ ] 아래 표에서 원인을 확인하고 조치한다
- [ ] `python3 main.py`로 다시 실행해 "📂 저장된 데이터를 불러왔습니다"가 나오는지 확인한다
- [ ] 원인을 모르겠으면 `QUIZ_DEBUG=1 python3 main.py`로 실행 후 `quiz_debug.log`의 "저장 실패" 줄을 확인한다

| 상황 예시 | 확인 명령 | 즉시 조치 |
|---|---|---|
| 폴더에 쓰기 권한이 없음 (다른 계정으로 만든 폴더, 읽기 전용 폴더) | `ls -ld .` | `chmod u+w .` 또는 쓰기 가능한 폴더로 프로젝트를 옮겨 실행 |
| `state.json` 자체가 읽기 전용 | `ls -l state.json` | `chmod u+w state.json` |
| 디스크 공간 부족 | `df -h .` | 불필요한 파일 정리 후 재실행 |
| USB·네트워크 드라이브가 분리됨 | `ls` 결과가 비거나 오류 | 드라이브 재연결 후 재실행 |

**저장 도중 강제 종료되면?** 저장은 `state.json.tmp`에 먼저 쓰고 마지막에 한 번에 바꿔치기하므로, 도중에 꺼져도 `state.json`은 이전 상태 그대로입니다. 반쯤 쓴 `state.json.tmp`가 남을 수 있지만 프로그램은 이 파일을 읽지 않고, 다음 저장 때 덮어쓴 뒤 정리합니다 (`test_leftover_temp_file_from_crash_is_ignored_then_replaced`로 검증).

## 5. 손상 파일 백업 정책
- 손상을 감지하면 원본을 **`state.json.bak` 1개**로 복사한 뒤 기본 데이터로 복구합니다(`StateStorage._backup_corrupted_file`).
- **가장 최근 손상본 1개만 보관합니다.** 다시 손상이 감지되면 `.bak`을 새 손상본으로 덮어씁니다. 이전 백업을 남기려면 직접 다른 이름(예: `state.json.bak.1`)으로 복사해 두세요.
- 백업 파일도 실행 데이터라 `.gitignore`로 Git에서 제외합니다.
- **수동 복구 방법**: `state.json.bak`을 열어 잘못된 부분(예: 선택지 개수)을 고친 뒤 `state.json`으로 이름을 바꾸고 다시 실행합니다.
- **복원 도우미 스크립트**: `python3 scripts/restore_backup.py`가 `.bak`을 **검사**해 지금 불러올 수 있는지, 아니면 몇 번째 줄이 틀렸는지 알려 줍니다. 정상이면 `--restore`를 붙여 실행하면 현재 파일을 `state.json.before-restore`로 보관한 뒤 `.bak`으로 되돌립니다. 손상된 `.bak`은 복원하지 않습니다. (실행 원문: [RUN_LOG 4-10](RUN_LOG.md#4-10-백업-검사복원-스크립트))
- **보관 수를 늘리고 싶다면**: `_backup_corrupted_file`에서 백업 이름에 시각을 붙이고(`state.json.20261124-190000.bak`), 같은 패턴 파일이 N개를 넘으면 오래된 것부터 지우도록 바꾸면 됩니다. 손상은 드물고 백업은 사람이 직접 확인해 고치는 용도라, 현재는 단순한 1개 보관을 택했습니다.

**복구 테스트 절차**
| 방법 | 절차 | 기대 결과 |
|---|---|---|
| 자동 (스크립트) | `python3 -m unittest tests.test_restore_backup` | 손상된 백업 복원 거부, 정상 백업 복원 + 이전 파일 보관 테스트 통과 |
| 자동 | `python3 -m unittest tests.test_storage` | `test_backup_keeps_only_latest_corrupted_file`(두 번 손상 → `.bak` 1개, 최신 내용), `test_manual_recovery_from_backup`(`.bak` 수정 → 되돌리면 `loaded`) 통과 |
| 수동 ① 손상 | `echo '{broken' > state.json` → `python3 main.py` | "⚠️ 데이터 파일이 손상되어 기본 퀴즈로 복구합니다" 출력, `state.json.bak` 내용이 `{broken` |
| 수동 ② 재손상 | 다시 `echo '{again' > state.json` → 실행 | `ls state.json*`에 `.bak`이 1개뿐이고 내용이 `{again` |
| 수동 ③ 복구 | 손상 전에 복사해 둔 정상 파일(또는 잘못된 곳을 고친 `.bak`)을 `state.json`으로 되돌림 → 실행 | "📂 저장된 데이터를 불러왔습니다" |

실제 실행 원문은 [RUN_LOG 4-3](RUN_LOG.md#4-3-손상-파일로-시작-json-문법-오류)에 있습니다.

## 6. JSON을 선택한 이유 (다른 방식과 비교)
| 방식 | 장점 | 이 프로젝트에서의 단점 | 판단 |
|---|---|---|---|
| **JSON** | 표준 `json` 모듈로 바로 사용, list·dict 중첩 구조를 그대로 저장, 사람이 열어 읽고 고칠 수 있음 | 아래 7장의 한계 | **선택** |
| CSV | 표 형태라 엑셀로 보기 쉬움 | 한 줄 = 평면 행이라 "퀴즈 안의 선택지 4개", "기록 목록" 같은 중첩 구조를 담기 어렵고, 쉼표가 들어간 선택지 처리도 번거로움 | 부적합 |
| SQLite (`sqlite3`) | 표준 라이브러리, 대용량·검색·부분 수정에 강함 | 테이블 설계와 SQL이 필요하고, 데이터가 수십 KB 수준이라 과함 | 규모가 커지면 고려 |
| pickle | 파이썬 객체를 그대로 저장 | 사람이 읽을 수 없고, 신뢰할 수 없는 파일을 열면 보안 위험 | 부적합 |

**SQLite로 바꾼다면 — 전환 체크리스트**
- [ ] `storage.py`: `StateStorage.load`/`save`를 `sqlite3`로 다시 구현. **반환 형태(dict, 상태값 `"loaded"`/`"missing"`/`"corrupted"`/`"error"`)는 그대로 유지**
- [ ] `storage.py`: 테이블 설계 — `quizzes`(id, question, choice1~4, answer, hint), `history`(id, played_at, total, correct, hints_used, hinted_correct, score), `meta`(best_score 등)
- [ ] `storage.py`: 기존 `state.json`이 있으면 한 번 읽어 DB로 옮기는 변환 함수
- [ ] `storage.py`: `DEFAULT_STATE_PATH` → `state.db`, `.gitignore`에 `state.db` 추가
- [ ] `tests/test_storage.py`: 임시 DB 파일 기준으로 다시 작성 (손상 판정은 `sqlite3.DatabaseError`)
- [ ] 수정 불필요 확인: `quiz.py`, `quiz_session.py`, `quiz_game.py`, `input_utils.py` — `python3 -m unittest discover -s tests` 전체 통과로 확인
- [ ] README 6장과 이 문서(DATA.md) 갱신

## 7. JSON 저장 방식의 한계와 대안
| 한계 | 설명 | 대안 |
|---|---|---|
| 매번 파일 전체를 읽고 씀 | 기록 하나만 추가해도 `state.json` 전체를 다시 씁니다. `history`가 계속 쌓이므로 판 수에 비례해 저장 시간과 메모리 사용이 늘어납니다. (기록 1건 ≈ 160바이트라 1만 판이면 약 1.6MB로 아직 문제는 없음) | 기록 개수 상한을 두거나, 오래된 기록을 별도 파일로 분리. 추가만 하는 기록은 JSON Lines(한 줄에 1건 append) 방식 |
| 부분 검색·수정 불가 | "점수 80점 이상 기록만"처럼 조건 검색을 하려면 전체를 불러와 파이썬에서 걸러야 합니다. | SQLite로 바꾸면 SQL로 검색·부분 수정 가능 |
| 동시 실행 보호 없음 | 프로그램을 두 개 동시에 실행하면 나중에 저장한 쪽이 앞의 내용을 덮어씁니다(파일 잠금 없음). | 파일 잠금 또는 DB 트랜잭션 사용 |
| 스키마 강제 없음 | JSON 자체는 "선택지는 4개" 같은 규칙을 모릅니다. 그래서 `StateStorage._normalize_state`에서 직접 검증합니다. | JSON Schema 또는 DB 제약 조건 |
| 날짜 타입 없음 | 날짜를 문자열(ISO 8601)로 저장하고 읽을 때 해석해야 합니다. | DB의 날짜 타입 |

**기록 수별 실측** (`python3 scripts/benchmark_storage.py`, 기본 퀴즈 12개 + 게임 기록 N건, 5회 측정 중앙값, macOS 12 / Python 3.16.0a2)

| 게임 기록 수 | state.json 크기 | 저장(save) | 불러오기(load) |
|---:|---:|---:|---:|
| 0 | 4.9 KB | 0.7 ms | 0.2 ms |
| 100 | 20.7 KB | 1.6 ms | 0.6 ms |
| 1,000 | 162.2 KB | 10.7 ms | 4.0 ms |
| 10,000 | 1.5 MB | 100.2 ms | 47.6 ms |
| 100,000 | 15.4 MB | 988.5 ms | 498.2 ms |

- 크기와 시간이 **기록 수에 거의 정비례**합니다(1건 ≈ 160바이트, 저장 ≈ 0.01ms/건).
- 한 판을 끝낼 때마다 저장하므로, 저장 시간이 사람이 느끼는 지연(약 0.1초)에 닿는 **기록 1만 건 무렵**이 대안을 검토할 시점입니다. 하루 10판씩이면 약 3년 분량이라 개인용으로는 현재 방식으로 충분합니다.
- **기본 대비책으로 `history` 상한을 구현했습니다**: 기록은 최근 **1,000건**(`QuizGame.HISTORY_MAX`)까지만 보관하고, 넘으면 오래된 것부터 지웁니다(롤링). 측정표 기준 1,000건 ≈ 162KB·저장 약 11ms라 판이 쌓여도 저장 지연이 커지지 않습니다. 최고 기록(`best_record`)은 따로 저장되어 오래된 기록이 지워져도 남습니다.
- 모든 기록을 영구 보관해야 하는 요구가 생기면 ② 기록만 JSON Lines로 분리(추가만 하므로 저장 시간 일정), ③ SQLite 전환 순으로 적용합니다.

현재 규모(퀴즈 수십 개, 개인 플레이 기록)에서는 JSON의 단순함이 더 큰 장점이라고 판단했습니다. 데이터가 커지면 `StateStorage`만 SQLite 버전으로 바꾸면 됩니다([DESIGN 5장](DESIGN.md#5-입력-검증과-데이터-입출력을-분리한-이유), [DESIGN 7장](DESIGN.md#7-요구사항-변경-시-영향-범위) 참고).

## 8. 운영 지침 (동시 실행과 데이터 관리)
JSON 파일에는 잠금 기능이 없어서, **같은 폴더에서 프로그램을 두 개 이상 동시에 실행하면 나중에 저장한 쪽이 앞의 변경을 덮어씁니다.** 다음 지침으로 위험을 줄입니다.
- **한 폴더에서는 한 번에 하나만 실행합니다.** 터미널 창을 여러 개 열어 두었다면 다른 창의 게임이 종료됐는지 확인한 뒤 실행합니다.
- **여러 사람이 각자 쓰려면 폴더를 따로 둡니다.** `state.json`은 `storage.py`와 같은 폴더에 생기므로, 저장소를 각자 clone하면 데이터 파일도 자연히 분리됩니다.
- **중요한 기록은 실행 전에 복사해 둡니다.** 예: `cp state.json state.json.manual-backup` (`.gitignore`에 포함되지 않으니 커밋하지 않도록 주의)
- **덮어쓰기가 의심되면** 프로그램을 모두 종료하고 백업본을 `state.json`으로 되돌린 뒤 하나만 다시 실행합니다.
- 코드로 막아야 할 만큼 사용 규모가 커지면, 시작할 때 잠금 파일(`state.json.lock`)을 만들고 이미 있으면 실행을 거부하는 방식이나 SQLite 트랜잭션을 적용합니다.

**JSON 파일 백업·동기화 권장 절차**
1. **백업**: 게임을 종료한 상태에서 `cp state.json backups/state-$(date +%Y%m%d).json`처럼 날짜를 붙여 복사합니다. 실행 중 복사는 피합니다(저장 직전 상태일 수 있음).
2. **다른 컴퓨터와 동기화**: Git으로 올리지 않습니다(개인 기록이고 `.gitignore` 대상). 클라우드 폴더·USB로 복사하되, **양쪽에서 동시에 플레이하지 않고** "마지막으로 플레이한 쪽 → 다른 쪽" 한 방향으로만 복사합니다. 복사 전 받는 쪽 파일도 백업합니다.
3. **복사 후 확인**: `python3 scripts/validate_quizzes.py state.json`으로 퀴즈 형식을 검사하거나, 실행해서 "📂 저장된 데이터를 불러왔습니다"가 나오는지 확인합니다.
4. **보안**: JSON은 코드가 실행되지 않는 순수 텍스트라 pickle과 달리 파일을 여는 것만으로 위험하지는 않습니다. 대신 누구나 읽을 수 있으므로 개인정보를 퀴즈·힌트에 넣지 않고, 공유 컴퓨터에서는 `chmod 600 state.json`으로 본인만 읽게 합니다. 받은 파일은 프로그램이 형식을 검증한 뒤에만 사용합니다(손상 시 백업 후 복구).

## 9. 스키마 버전 업 (마이그레이션)
`version` 필드와 **변환 구조가 이미 구현**되어 있습니다(`storage.py`의 `CURRENT_VERSION`, `MIGRATIONS`). 현재 버전은 1이고, 파일을 읽을 때 버전을 보고 이렇게 처리합니다.

```
StateStorage.load() → StateStorage._migrate()
 ├─ version 키 없음        → 1로 간주 (초기 파일 호환)
 ├─ version < 1           → "corrupted" (백업 후 복구)
 ├─ version > CURRENT     → "unsupported" (더 새 프로그램이 만든 파일 → 백업·덮어쓰기 없이 보호 모드)
 └─ version < CURRENT     → MIGRATIONS[version]으로 한 단계씩 변환 → 검증 → 다음 save() 때 새 형식으로 저장
                            (중간 변환 함수가 없으면 "corrupted")
```
예를 들어 퀴즈에 `category` 필드를 추가해 **버전 2**로 올린다면, 변환 함수를 만들어 등록하고 `CURRENT_VERSION`만 올리면 됩니다.
```python
# storage.py
CURRENT_VERSION = 2

def migrate_v1_to_v2(state: dict) -> dict:
    for quiz in state["quizzes"]:
        quiz.setdefault("category", "기타")
    state["version"] = 2
    return state

MIGRATIONS = {1: migrate_v1_to_v2}
```
함께 바꿀 곳: `Quiz.__init__`/`to_dict`/`from_dict`(category 속성), `StateStorage._normalize_quiz`(category 검증), `QuizGame.add_quiz`(입력 추가). `QuizGame.to_state`는 `CURRENT_VERSION`을 쓰므로 수정 불필요.

**자동 테스트**(`tests/test_storage.py`): `test_migration_upgrades_old_version_step_by_step`(가짜 v2 환경에서 v1 파일이 변환되는지), `test_missing_migration_step_is_corrupted`(변환 단계 누락), `test_future_version_is_unsupported_and_left_untouched`(미래 버전 파일이 그대로 남는지), `test_version_below_one_is_corrupted`. 실제 실행 원문은 [RUN_LOG 4-9](RUN_LOG.md#4-9-더-새로운-버전의-데이터-파일)에 있습니다.
