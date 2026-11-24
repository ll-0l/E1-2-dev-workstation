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

## 2. 작업 흐름
```bash
git checkout main && git pull                 # 1. 항상 최신 main에서 시작
git checkout -b feature/<이름>                # 2. 브랜치 생성
# ... 작업, 기능 단위로 commit (파일 1~3개, 150줄 이내 권장) ...
python3 -m unittest discover -s tests         # 3. 전체 테스트 통과 확인
git push -u origin feature/<이름>             # 4. 원격에 올림 → 리뷰 요청
# --- 리뷰 통과 후 (병합 담당 Lead) ---
git checkout main && git pull
git merge --no-ff feature/<이름>              # 5. 병합 기록이 그래프에 남도록 --no-ff
python3 -m unittest discover -s tests         # 6. 병합 결과 다시 확인
git push                                      # 7. main 업로드
```

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
- [ ] 새 안내 문구가 README 4장 "안내 문구 형식"(⚠️ 문제 + 조치)을 따른다
- [ ] 기존 `state.json`을 가진 사용자가 데이터를 잃지 않는다

**문서**
- [ ] README의 기능 목록·예외 처리 표·영향 범위(8장) 중 바뀐 곳을 갱신했다

**충돌·결정**
- [ ] 다른 브랜치와 규칙이 충돌하면(예: 점수 반올림 방식) 병합 담당이 하나로 결정하고, 테스트와 AGENTS.md를 그 결정에 맞춘다 (실제 사례: `fix/player-qa`의 사사오입 vs `test/quiz-management`의 `round()` → 사사오입으로 통일, 커밋 `f75614e`)
