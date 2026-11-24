# 브랜치 · 리뷰 가이드 (한 페이지)

이 저장소에서 기능을 추가하거나 고칠 때 따르는 규칙입니다. 담당 파일과 인터페이스 약속은 [AGENTS.md](../AGENTS.md)를 함께 봅니다.

## 1. 브랜치 이름 규칙
`<종류>/<짧은-설명>` 형식으로 쓰고, 영어 소문자와 하이픈(`-`)만 씁니다.

| 종류 | 언제 | 이 저장소의 실제 예 |
|---|---|---|
| `feature/` | 새 기능 | `feature/quiz-model`, `feature/play-quiz`, `feature/storage` |
| `fix/` | 버그·동작 수정 | `fix/player-qa` |
| `test/` | 테스트만 추가 | `test/storage-integration`, `test/quiz-management` |
| `refactor/` | 동작은 같고 구조만 개선 | (예: `refactor/split-quiz-game`) |
| `docs/` | 문서만 수정 | (예: `docs/readme-design`) |

- 한 브랜치에는 **한 가지 목적**만 담습니다. 목적이 둘이면 브랜치를 나눕니다.
- 커밋 메시지 접두어(`Feat:`/`Fix:`/`Test:`/`Refactor:`/`Docs:`/`Chore:`)는 브랜치 종류와 맞춥니다.

### 커밋 단위 기준
- 원칙: **기능 1개 = 커밋 1개**, 커밋 시점에는 테스트가 모두 통과해야 합니다.
- 권장 변경량: **파일 1~3개, 변경 150줄 이내**. 이 저장소의 코드 커밋 29개(1차 평가 시점)를 실측하면 파일 수 중앙값 1개(최대 5개), 변경 줄 수 중앙값 37줄, 90%가 131줄 이하였고, 200줄을 넘은 커밋은 테스트를 처음 한꺼번에 추가한 1건(261줄)뿐이었습니다.
- 권장량을 넘으면 나눕니다. 예: "저장 기능 + 테스트"를 `Feat: StateStorage 구현`과 `Test: StateStorage 단위 테스트 추가`로 분리.
- 실제 예시: `e936301 Feat: 퀴즈 추가 기능 구현`, `af6c4f5 Feat: 퀴즈 목록 기능 구현`, `52394a2 Fix: 점수 반올림을 사사오입으로 통일`, `b7ccff4 Refactor: QuizGame 책임 분리 및 구조 정리`, `d2dc663 Docs: README 작성`

### 커밋 메시지 템플릿
저장소 루트의 [`.gitmessage`](../.gitmessage)를 한 번 등록하면 `git commit` 때마다 아래 틀이 열립니다.
```bash
git config commit.template .gitmessage
```
```text
Feat: 퀴즈 삭제 기능 구현                         ← 제목: <종류>: <한 일> (50자 안팎)
                                                  ← 빈 줄
- 목록에서 번호 선택(0은 취소) 후 y/n 확인을 거쳐 삭제   ← 본문: 무엇을/왜, '- ' 목록
- 삭제 결과를 state.json에 반영

Refs: #12                                         ← 꼬리말(선택): 이슈 번호, 리뷰어
```

## 2. 작업 흐름
```bash
git checkout main && git pull                 # 1. 항상 최신 main에서 시작
git checkout -b feature/<이름>                # 2. 브랜치 생성
# ... 작업, 기능 단위로 commit (파일 1~3개, 150줄 이내 권장) ...
python3 -m unittest discover -s tests         # 3. 전체 테스트 통과 확인
git push -u origin feature/<이름>             # 4. 원격에 올림 → 리뷰 요청
# --- 리뷰 통과 후 (병합 담당 Lead) ---
git checkout main && git pull
git merge --no-ff feature/<이름> -m "Merge branch 'feature/<이름>'" -m "<목적 한 줄>"   # 5. --no-ff + 목적 명시
python3 -m unittest discover -s tests         # 6. 병합 결과 다시 확인
git push                                      # 7. main 업로드
```

**병합 커밋 메시지 형식** — 제목은 Git 기본값 `Merge branch '<브랜치>'`를 그대로 두고, **본문 첫 줄에 병합 목적**을 적습니다. 이슈가 있으면 `Refs: #번호`를 붙입니다.
```text
Merge branch 'feature/play-quiz'

퀴즈 풀기 기능(랜덤 출제/문제 수 선택/힌트) 병합
Refs: #3
```
(이 저장소의 병합 6개도 이 형식이며, 목적별 요약은 [GIT_EVIDENCE 3장](GIT_EVIDENCE.md#3-브랜치와-병합-기록)에 있습니다. GitHub 이슈는 사용하지 않아 `Refs`는 생략했습니다.)

**금지 사항**
- `main`에 직접 커밋하지 않습니다 (병합 담당 Lead 제외).
- **이미 push했거나 병합된 브랜치는 `--force`로 다시 쓰지 않습니다.** 고칠 것이 있으면 최신 `main`에서 새 브랜치를 만듭니다. (실제 사례: `fix/player-qa`가 병합 후 force-push되어 원격 브랜치 내용과 `main`이 달라졌고, 결국 원격 브랜치를 삭제해 정리했습니다.)
- `state.json`, `state.json.bak` 등 실행 데이터는 커밋하지 않습니다 (`.gitignore`).

## 3. 병합 전 리뷰 체크리스트
리뷰어(Lead)는 병합 전에 아래를 확인합니다. GitHub Pull Request를 쓸 때도 이 목록을 PR 설명에 붙여 체크합니다.

**범위**
- [ ] 브랜치 목적이 하나이고, 담당 파일만 수정했다 (AGENTS.md 2장)
- [ ] 커밋이 기능 단위로 나뉘어 있고, 메시지에 무엇을 왜 바꿨는지 적혀 있다

**동작**
- [ ] `python3 -m unittest discover -s tests` 전체 통과
- [ ] 바뀐 동작에 대한 테스트가 추가·수정됐다 (예외 경로 포함)
- [ ] `python3 main.py`로 해당 메뉴를 직접 실행해 봤고, Ctrl+C 종료가 정상이다
- [ ] 인터페이스 계약(`Quiz`, `QuizSession`, `StateStorage`의 입출력 형태)을 지켰다. 바꿨다면 AGENTS.md도 함께 수정했다

**사용자 경험**
- [ ] 새 안내 문구가 [DESIGN 2장 "안내 문구 형식"](DESIGN.md#2-안내-문구-형식)(⚠️ 문제 + 조치)을 따른다
- [ ] 기존 `state.json`을 가진 사용자가 데이터를 잃지 않는다

**문서**
- [ ] README의 기능 목록·예외 처리 표·영향 범위(DESIGN 7장) 중 바뀐 곳을 갱신했다

**충돌·결정**
- [ ] 다른 브랜치와 규칙이 충돌하면(예: 점수 반올림 방식) 병합 담당이 하나로 결정하고, 테스트와 AGENTS.md를 그 결정에 맞춘다 (실제 사례: `fix/player-qa`의 사사오입 vs `test/quiz-management`의 `round()` → 사사오입으로 통일, 커밋 `f75614e`)

## 4. 병합 충돌 해결 정책
충돌은 두 종류로 나눠 처리합니다.

**① Git 충돌 (같은 줄을 서로 다르게 고침)**
1. 병합 담당(Lead)이 `git merge` 중 충돌을 확인하면, 해당 파일의 **담당자(AGENTS.md 2장)의 의도를 우선**합니다. 담당자가 아닌 쪽 변경은 담당자에게 확인받은 뒤 반영합니다.
2. 양쪽 다 필요한 변경이면 둘 다 살리고, 판단이 어려우면 병합을 취소(`git merge --abort`)하고 브랜치 작성자에게 최신 `main`을 받아 다시 맞춰 달라고 요청합니다.
3. 해결 후 `python3 scripts/run_checks.py`가 4/4 통과해야 병합 커밋을 만듭니다.

**② 규칙 충돌 (충돌 표시는 없지만 두 브랜치의 동작·기대값이 서로 다름)**
1. 우선순위: **AGENTS.md 계약 > 사용자에게 보이는 동작의 자연스러움 > 먼저 병합된 쪽**.
2. 계약을 바꿔야 하면 Lead가 결정하고, 같은 PR/병합 안에서 **AGENTS.md "계약 변경 이력" → 코드 → 테스트 기대값**을 함께 고칩니다.
3. 실제 사례: `fix/player-qa`(점수 사사오입)와 `test/quiz-management`(`round()` 기대값)가 충돌 표시 없이 병합된 뒤 테스트가 실패 → Lead가 사사오입으로 결정, 테스트(`f75614e`)와 계약 문서를 맞춤.

**공통**: 리뷰어(병합 담당)가 최종 결정권을 갖고, 결정 이유는 병합 커밋 본문이나 계약 변경 이력에 남깁니다.
