# Git 작업 증빙 (텍스트)

이미지를 볼 수 없는 환경에서도 확인할 수 있도록, Git 명령의 **실행 결과 원문**을 그대로 옮겼습니다.
스크린샷 버전:
- [screenshots/git_log.png](screenshots/git_log.png) — `git log --oneline --graph` 전체 (브랜치 6개의 생성·병합 그래프)
- [screenshots/clone_pull.png](screenshots/clone_pull.png) — 4-2절 clone → commit → push → pull 전 과정
- [screenshots/dev_env.png](screenshots/dev_env.png) — Git 버전, 사용자 이름, `git remote -v`, 브랜치 목록

- 작성 시점 HEAD: `c1b3d90 Docs: clone 폴더에서 clone/pull 2차 실습 기록 추가`
- 이 문서를 추가하는 커밋 이후의 기록은 GitHub에서 `git log`로 확인할 수 있습니다.

| 평가 요구 | 증빙 위치 |
|---|---|
| GitHub 원격 저장소 업로드 | [1. 원격 저장소](#1-원격-저장소) |
| 의미 있는 커밋 10개 이상 | [2. 커밋 수와 전체 이력](#2-커밋-수와-전체-이력) |
| 브랜치 생성(checkout) 및 병합(merge) | [3. 브랜치와 병합 기록](#3-브랜치와-병합-기록) |
| clone 1회 이상 | [4. clone / pull 실습](#4-clone--pull-실습) |
| pull 1회 이상 | [4. clone / pull 실습](#4-clone--pull-실습) |
| init / add / commit / push 사용 | [5. Git 기초 명령어 7종 사용 기록](#5-git-기초-명령어-7종-사용-기록) |

## 1. 원격 저장소

- URL: https://github.com/ll-0l/E1-2-dev-workstation (Public)
- 브라우저 없이 확인: `git ls-remote https://github.com/ll-0l/E1-2-dev-workstation.git main` → `main` 브랜치의 최신 커밋 해시가 출력되면 공개 저장소에 정상 접근된 것입니다.

**원격 저장소에 접근이 안 될 때 확인할 것**
| 증상 | 확인 항목 | 확인 방법 |
|---|---|---|
| `Repository not found` / 404 | URL 오타, 저장소 이름·계정 변경, 비공개 전환 여부 | `git remote -v`의 주소와 GitHub 페이지 주소 비교, 저장소 Settings의 공개 여부 |
| `Authentication failed` / 403 (push 시) | 로그인 계정과 저장소 권한, 토큰 만료 | `gh auth status`, 저장소 Collaborators 권한 |
| `Could not resolve host` / 시간 초과 | 네트워크, 프록시, 방화벽 | `ping github.com`, 다른 네트워크에서 재시도 |
| clone은 되는데 최신 커밋이 안 보임 | 원격 변경을 아직 안 받음 | `git fetch` 후 `git log origin/main --oneline -3` |
| push 중 `HTTP 400` / 연결 끊김 | 큰 파일(이미지 등) 전송 버퍼 부족 | `git config http.postBuffer 157286400` 후 재시도 (이 저장소에서 스크린샷 push 때 실제로 발생·해결) |

원격 접근이 어려운 상황에서도 이 문서의 2~4장 출력 원문과 [screenshots/git_log.png](screenshots/git_log.png)로 이력을 확인할 수 있습니다.

```text
$ git remote -v
origin	https://github.com/ll-0l/E1-2-dev-workstation.git (fetch)
origin	https://github.com/ll-0l/E1-2-dev-workstation.git (push)
```

## 2. 커밋 수와 전체 이력

> 아래 출력은 최초 작성 시점(`c1b3d90`) 기준입니다. 재평가 보완 작업 후 이 문서를 갱신한 커밋까지 포함하면 의미 있는 커밋은 **48개**입니다. 최신 값은 `git log --no-merges --oneline | wc -l`로 확인합니다.

```text
$ git log --no-merges --oneline | wc -l   # 의미 있는 커밋 수 (병합 커밋 제외)
      36
```

```text
$ git log --merges --oneline | wc -l      # 병합 커밋 수
       6
```

```text
$ git log --oneline --graph
* c1b3d90 Docs: clone 폴더에서 clone/pull 2차 실습 기록 추가
* f569289 Docs: README 설계 근거와 영향 범위 보강 (사전평가 반영)
* 82cbdfc Docs: 실행 화면 텍스트 로그 추가 (docs/RUN_LOG.md)
* 5a878f3 Refactor: 정답 입력 범위를 CHOICE_COUNT 상수로 통일
* 2c75778 Test: 메뉴 입력 예외와 Ctrl+C/EOF 종료, 재시작 후 데이터 유지 테스트 추가
* 7862a0f Fix: 저장 실패 시 사용자 조치 방법 안내 추가
* f5243ed Docs: git log --oneline --graph 스크린샷 추가
* 1763ac6 Docs: 실행 화면 및 개발 환경 스크린샷 추가
* e0c3f89 Docs: README에 clone/pull 실습 기록 추가
* cdf9391 Docs: 점수 반올림 규칙(사사오입)과 테스트/브랜치 현황 갱신
* f75614e Test: 점수 반올림 테스트를 사사오입 기준으로 수정
*   da98498 Merge branch 'test/quiz-management'
|\  
| * de3fb99 Test: 점수 반올림 계약 경계값 검증
| * e520b2f Test: 퀴즈 관리와 히스토리 회귀 테스트 추가
* |   859225d Merge branch 'fix/player-qa'
|\ \  
| * | cda7d67 Fix: 기본 퀴즈 문구 다듬기 (정답 노출·선택지 길이 편중 수정)
| * | 26c350e Fix: 오답 안내에서 정답 선택지 따옴표 중복 표시 수정
| * | 52394a2 Fix: 점수 반올림을 사사오입으로 통일
|/ /  
* / d2dc663 Docs: README 작성 (개요/주제 선정 이유/실행 방법/기능/파일 구조/state.json)
|/  
*   66ed4f7 Merge branch 'test/storage-integration'
|\  
| * 6de3221 Test: QuizGame 저장 연동 회귀 테스트 추가
* | b7ccff4 Refactor: QuizGame 책임 분리 및 구조 정리
* | c0033c4 Feat: 게임 기록(히스토리) 화면 구현
* | bce6b94 Feat: 퀴즈 삭제 기능 구현
|/  
*   c5a0234 Merge branch 'feature/storage'
|\  
| * 88e5f94 Feat: QuizGame에 state.json 저장/불러오기 연동
| * 194241a Test: 저장소/Quiz/QuizSession/입력 함수 단위 테스트 추가
| * 97aa8ed Feat: state.json 저장/불러오기 StateStorage 구현
|/  
* 4d173df Feat: 점수 확인 및 최고 점수 갱신 기능 구현
* af6c4f5 Feat: 퀴즈 목록 기능 구현
* e936301 Feat: 퀴즈 추가 기능 구현
*   d687507 Merge branch 'feature/play-quiz'
|\  
| * e9f9136 Feat: 메뉴에 퀴즈 풀기 기능 연결
| * 4983637 Feat: 퀴즈 풀기 세션 구현 (랜덤 출제/힌트/채점)
|/  
*   808c6d1 Merge branch 'feature/quiz-model'
|\  
| * 7f3ab5a Feat: 2026 신조어 기본 퀴즈 데이터 12개 작성
| * d2e942f Feat: Quiz 클래스 구현 (출력/정답 확인/직렬화)
|/  
* 56b615a Feat: 메뉴 화면 및 메뉴 선택 흐름 구현
* 457436a Feat: 공통 입력 검증 함수 구현
* b4cb349 Docs: 3인 분업 체계로 협업 규칙 개편
* e28c1af Docs: 에이전트 협업 규칙 및 인터페이스 계약 추가
* f7be1ec Chore: 프로젝트 초기 설정 (.gitignore, README 골격)
```

## 3. 브랜치와 병합 기록

```text
$ git branch -a
  feature/play-quiz
  feature/quiz-model
  feature/storage
* main
  remotes/origin/feature/play-quiz
  remotes/origin/feature/quiz-model
  remotes/origin/feature/storage
  remotes/origin/main
  remotes/origin/test/quiz-management
  remotes/origin/test/storage-integration
```

```text
$ git log --merges --oneline
da98498 Merge branch 'test/quiz-management'
859225d Merge branch 'fix/player-qa'
66ed4f7 Merge branch 'test/storage-integration'
c5a0234 Merge branch 'feature/storage'
d687507 Merge branch 'feature/play-quiz'
808c6d1 Merge branch 'feature/quiz-model'
```

**병합 커밋별 요약** — 각 병합이 무엇을 `main`에 가져왔는지 (`git log <병합>^1..<병합>^2`로 확인)

| 병합 커밋 | 브랜치 | 목적 | 포함 커밋 |
|---|---|---|---|
| `808c6d1` | `feature/quiz-model` | 퀴즈 데이터 모델 도입 | 2개: `Feat: Quiz 클래스 구현`, `Feat: 2026 신조어 기본 퀴즈 데이터 12개 작성` |
| `d687507` | `feature/play-quiz` | 퀴즈 풀기 기능 (과제의 브랜치 작업 요구) | 2개: `Feat: 퀴즈 풀기 세션 구현 (랜덤 출제/힌트/채점)`, `Feat: 메뉴에 퀴즈 풀기 기능 연결` |
| `c5a0234` | `feature/storage` | state.json 영속성 | 3개: `Feat: StateStorage 구현`, `Test: 단위 테스트 추가`, `Feat: QuizGame에 저장/불러오기 연동` |
| `66ed4f7` | `test/storage-integration` | 저장 연동 회귀 테스트 | 1개: `Test: QuizGame 저장 연동 회귀 테스트 추가` |
| `859225d` | `fix/player-qa` | 사용자 QA 결과 반영 | 3개: `Fix: 점수 반올림을 사사오입으로 통일`, `Fix: 오답 안내 따옴표 중복 수정`, `Fix: 기본 퀴즈 문구 다듬기` |
| `da98498` | `test/quiz-management` | 삭제·기록 기능 회귀 테스트 | 2개: `Test: 퀴즈 관리와 히스토리 회귀 테스트 추가`, `Test: 점수 반올림 계약 경계값 검증` (병합 직후 `f75614e`에서 사사오입 기준으로 기대값 수정) |

브랜치 생성(`checkout -b`)과 병합을 실행한 기록 (원본 작업 폴더의 `git reflog` 발췌):

```text
$ git reflog --date=iso | grep -E "checkout: moving from main to (feature|test)|merge |commit \(merge\)"
da98498 HEAD@{2026-11-22 20:06:44 +0900}: merge origin/test/quiz-management: Merge made by the 'ort' strategy.
859225d HEAD@{2026-11-22 20:06:44 +0900}: merge origin/fix/player-qa: Merge made by the 'ort' strategy.
66ed4f7 HEAD@{2026-11-20 19:33:25 +0900}: commit (merge): Merge branch 'test/storage-integration'
c5a0234 HEAD@{2026-11-20 19:30:34 +0900}: merge feature/storage: Merge made by the 'ort' strategy.
4d173df HEAD@{2026-11-20 19:29:45 +0900}: checkout: moving from main to feature/storage
d687507 HEAD@{2026-11-20 19:28:04 +0900}: merge feature/play-quiz: Merge made by the 'ort' strategy.
808c6d1 HEAD@{2026-11-20 19:27:45 +0900}: checkout: moving from main to feature/play-quiz
808c6d1 HEAD@{2026-11-20 19:27:38 +0900}: merge feature/quiz-model: Merge made by the 'ort' strategy.
56b615a HEAD@{2026-11-20 19:27:10 +0900}: checkout: moving from main to feature/quiz-model
```

- `checkout: moving from main to feature/...` 줄이 `git checkout -b <브랜치>`로 브랜치를 만들어 이동한 기록입니다.
- `merge ...` 줄이 `main`에서 `git merge --no-ff <브랜치>`를 실행한 기록입니다.
- `fix/player-qa`는 병합 후 원격 브랜치를 정리(삭제)해서 `git branch -a` 목록에는 없지만, 병합 커밋 `859225d`와 그 안의 커밋 3개는 `main` 이력에 그대로 남아 있습니다.
- `feature/quiz-model`, `feature/play-quiz`, `feature/storage`는 이 폴더에서 직접 만들었고, `test/*`, `fix/player-qa`는 다른 작업 폴더에서 만들어 push한 브랜치를 받아 병합했습니다.

## 4. clone / pull 실습

### 4-1. 1차 실습 (2026-11-22)
- 별도 폴더 `E1-2-dev-workstation-clone`에 `git clone` → README에 "clone / pull 실습" 섹션 추가 → commit → push
- 원래 작업 폴더에서 `git pull`로 받아 Fast-forward 반영 (커밋 `e0c3f89`)

```text
$ git log --oneline -1 e0c3f89
e0c3f89 Docs: README에 clone/pull 실습 기록 추가
```

```text
$ git reflog --date=iso | grep "pull:"
c1b3d90 HEAD@{2026-11-24 16:53:23 +0900}: pull: Fast-forward
e0c3f89 HEAD@{2026-11-22 20:07:31 +0900}: pull: Fast-forward
```

### 4-2. 2차 실습 (2026-11-24, 전체 출력 기록)
재평가용으로 같은 과정을 다시 수행하며 모든 명령과 출력을 기록했습니다. (경로 앞부분은 `…`로 줄였습니다.)

```text
## [A] 별도 디렉터리에 clone
$ git clone https://github.com/ll-0l/E1-2-dev-workstation.git E1-2-dev-workstation-clone
Cloning into 'E1-2-dev-workstation-clone'...

$ pwd | sed "s#.*/Codyssey all-in-one Pre-course#…#"
…/E1-2-dev-workstation-clone

$ git remote -v
origin	https://github.com/ll-0l/E1-2-dev-workstation.git (fetch)
origin	https://github.com/ll-0l/E1-2-dev-workstation.git (push)

$ git log --oneline -3
f569289 Docs: README 설계 근거와 영향 범위 보강 (사전평가 반영)
82cbdfc Docs: 실행 화면 텍스트 로그 추가 (docs/RUN_LOG.md)
5a878f3 Refactor: 정답 입력 범위를 CHOICE_COUNT 상수로 통일

## [B] 복제한 저장소에서 README 수정 → commit → push
$ git diff --stat
 README.md | 1 +
 1 file changed, 1 insertion(+)

$ git add README.md

$ git commit -m "Docs: clone 폴더에서 clone/pull 2차 실습 기록 추가" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
[main c1b3d90] Docs: clone 폴더에서 clone/pull 2차 실습 기록 추가
 1 file changed, 1 insertion(+)

$ git push origin main
To https://github.com/ll-0l/E1-2-dev-workstation.git
   f569289..c1b3d90  main -> main

## [C] 원래 작업 폴더에서 pull
$ git log --oneline -1
f569289 Docs: README 설계 근거와 영향 범위 보강 (사전평가 반영)

$ git pull
From https://github.com/ll-0l/E1-2-dev-workstation
   f569289..c1b3d90  main       -> origin/main
Updating f569289..c1b3d90
Fast-forward
 README.md | 1 +
 1 file changed, 1 insertion(+)

$ git log --oneline -3
c1b3d90 Docs: clone 폴더에서 clone/pull 2차 실습 기록 추가
f569289 Docs: README 설계 근거와 영향 범위 보강 (사전평가 반영)
82cbdfc Docs: 실행 화면 텍스트 로그 추가 (docs/RUN_LOG.md)

## [D] 반영 확인
$ grep -n "2차 실습" README.md
352:5. (2차 실습 2026-11-24) 이 줄은 clone한 폴더에서 추가해 push한 뒤, 원래 작업 폴더에서 `git pull`로 받아온 것입니다.

$ git status -sb
## main...origin/main

```

복제한 폴더(`E1-2-dev-workstation-clone`)의 이력 — push한 커밋 `c1b3d90`이 원본 폴더의 pull 결과와 같습니다:

```text
$ git -C ../E1-2-dev-workstation-clone log --oneline -3
c1b3d90 Docs: clone 폴더에서 clone/pull 2차 실습 기록 추가
f569289 Docs: README 설계 근거와 영향 범위 보강 (사전평가 반영)
82cbdfc Docs: 실행 화면 텍스트 로그 추가 (docs/RUN_LOG.md)
```

## 5. Git 기초 명령어 7종 사용 기록

| 명령어 | 무엇을 하나 | 이 프로젝트에서 사용한 곳 | 증빙 |
|---|---|---|---|
| `git init` | 현재 폴더를 Git 저장소로 만든다 | 프로젝트 시작 시 `git init -b main` | reflog의 `commit (initial)` (아래) |
| `git add` | 변경 파일을 다음 커밋에 담을 준비(스테이징) | 모든 기능 커밋 전 | 2장의 커밋 이력 |
| `git commit` | 스테이징한 변경을 이력으로 저장 | 기능 단위 커밋 30개 이상 | 2장 |
| `git push` | 로컬 커밋을 GitHub에 올림 | 기능 완료마다, clone 폴더에서도 | 4-2의 `git push origin main` |
| `git checkout` | 브랜치를 만들거나(`-b`) 이동 | `feature/quiz-model`, `feature/play-quiz`, `feature/storage` | 3장 reflog |
| `git clone` | 원격 저장소를 새 폴더로 복제 | `E1-2-dev-workstation-clone` | 4-2의 `git clone` |
| `git pull` | 원격 변경을 받아 현재 브랜치에 합침 | 원본 폴더에서 2회 | 4-1, 4-2의 `git pull` |

```text
$ git reflog --date=iso | grep "commit (initial)"
f7be1ec HEAD@{2026-11-20 19:14:06 +0900}: commit (initial): Chore: 프로젝트 초기 설정 (.gitignore, README 골격)
```

