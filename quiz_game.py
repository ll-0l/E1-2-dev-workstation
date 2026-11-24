"""게임 전체를 관리하는 QuizGame 클래스."""

from default_quizzes import get_default_quizzes
from input_utils import read_int, read_line, read_text
from quiz import CHOICE_COUNT, Quiz
from quiz_session import QuizSession
from storage import StateStorage

LINE = "=" * 40
THIN_LINE = "-" * 40


class QuizGame:
    """퀴즈 목록과 점수 기록을 보관하고, 메뉴에 따라 각 기능을 실행한다.

    역할 분담
    - Quiz         : 문제 1개 (출력, 정답 확인)
    - QuizSession  : 퀴즈 1회 진행 (출제, 힌트, 채점)
    - StateStorage : state.json 읽기/쓰기
    - QuizGame     : 메뉴 흐름, 퀴즈 관리, 점수 기록, 저장 시점 결정
    """

    TITLE = "🎯 MZ 신조어 퀴즈 게임 🎯"
    HISTORY_DISPLAY_LIMIT = 10

    def __init__(self, storage: StateStorage | None = None) -> None:
        self.storage = storage or StateStorage()
        self.quizzes: list[Quiz] = get_default_quizzes()
        self.best_score: int | None = None      # 0~100점, 아직 플레이 전이면 None
        self.best_record: dict | None = None    # 최고 점수를 기록한 게임의 상세 기록
        self.history: list[dict] = []           # 모든 게임 기록
        self.running = True
        # (메뉴 이름, 실행할 메서드) — 번호는 순서대로 1부터 부여
        self.menu_items = [
            ("퀴즈 풀기", self.play_quiz),
            ("퀴즈 추가", self.add_quiz),
            ("퀴즈 목록", self.list_quizzes),
            ("점수 확인", self.show_score),
            ("퀴즈 삭제", self.delete_quiz),
            ("게임 기록", self.show_history),
            ("종료", self.quit),
        ]

    # ------------------------------------------------------------------
    # 실행 흐름
    # ------------------------------------------------------------------
    def run(self) -> None:
        """메인 루프. Ctrl+C / 입력 스트림 종료 시에도 저장 후 안전하게 종료한다."""
        self.show_title()
        self.load()
        try:
            while self.running:
                self.show_menu()
                choice = read_int("선택: ", 1, len(self.menu_items))
                _, action = self.menu_items[choice - 1]
                print()
                action()
        except (KeyboardInterrupt, EOFError):
            print("\n\n⚠️ 입력이 중단되어 프로그램을 종료합니다.")
            self.save()
            print("👋 다음에 또 만나요!")

    def show_title(self) -> None:
        print(LINE)
        print(f"{self.TITLE:^34}")

    def show_menu(self) -> None:
        print(LINE)
        for number, (label, _) in enumerate(self.menu_items, start=1):
            print(f"{number}. {label}")
        print(LINE)

    def quit(self) -> None:
        self.save()
        print("👋 게임을 종료합니다. 다음에 또 만나요!")
        self.running = False

    # ------------------------------------------------------------------
    # 메뉴 기능
    # ------------------------------------------------------------------
    def play_quiz(self) -> None:
        """문제 수를 고른 뒤 QuizSession으로 퀴즈를 진행하고 결과를 기록한다."""
        if not self.quizzes:
            print("📭 등록된 퀴즈가 없습니다. '퀴즈 추가'에서 먼저 퀴즈를 등록하세요.\n")
            return

        count = self._ask_question_count()
        result = QuizSession(self.quizzes, count=count).play()

        if self._record_result(result):
            print("🎉 새로운 최고 점수입니다!\n")
        else:
            print(f"🏆 현재 최고 점수: {self.best_score}점\n")
        self.save()

    def add_quiz(self) -> None:
        """문제, 선택지 4개, 정답 번호, 힌트(선택)를 입력받아 퀴즈를 등록한다."""
        print("📌 새로운 퀴즈를 추가합니다.\n")
        question = read_text("문제를 입력하세요: ")
        choices = [read_text(f"선택지 {number}: ") for number in range(1, CHOICE_COUNT + 1)]
        answer = read_int(f"정답 번호 (1-{CHOICE_COUNT}): ", 1, CHOICE_COUNT)
        hint = read_line("힌트 (없으면 Enter): ")

        self.quizzes.append(Quiz(question, choices, answer, hint))
        self.save()
        print(f"\n✅ 퀴즈가 추가되었습니다! (총 {len(self.quizzes)}개)\n")

    def list_quizzes(self) -> bool:
        """등록된 퀴즈 문제를 번호와 함께 출력한다. 퀴즈가 없으면 False."""
        if not self.quizzes:
            print("📭 등록된 퀴즈가 없습니다.\n")
            return False

        print(f"📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n")
        print(THIN_LINE)
        for number, quiz in enumerate(self.quizzes, start=1):
            hint_mark = " 💡" if quiz.has_hint() else ""
            print(f"[{number}] {quiz.question}{hint_mark}")
        print(THIN_LINE)
        print("💡 표시는 힌트가 있는 문제입니다.\n")
        return True

    def show_score(self) -> None:
        """최고 점수와 그 기록의 상세 내용을 출력한다."""
        if self.best_score is None or self.best_record is None:
            print("📭 아직 퀴즈를 풀지 않았습니다. '퀴즈 풀기'로 첫 기록을 남겨보세요!\n")
            return

        record = self.best_record
        print(
            f"🏆 최고 점수: {self.best_score}점 "
            f"({record['total']}문제 중 {record['correct']}문제 정답, 힌트 {record['hints_used']}회)"
        )
        print(f"📅 기록 일시: {self._format_time(record['played_at'])}\n")

    def delete_quiz(self) -> None:
        """목록에서 번호를 골라 확인 후 퀴즈를 삭제한다. 0을 입력하면 취소."""
        if not self.list_quizzes():
            return

        total = len(self.quizzes)
        number = read_int(f"삭제할 퀴즈 번호 (1-{total}, 취소: 0): ", 0, total)
        if number == 0:
            print("↩️ 삭제를 취소했습니다.\n")
            return

        print(f"\n[{number}] {self.quizzes[number - 1].question}")
        if not self._confirm("이 퀴즈를 삭제할까요? (y/n): "):
            print("↩️ 삭제를 취소했습니다.\n")
            return

        self.quizzes.pop(number - 1)
        self.save()
        print(f"🗑️ 퀴즈가 삭제되었습니다. (남은 퀴즈 {len(self.quizzes)}개)\n")

    def show_history(self) -> None:
        """지금까지의 게임 기록을 최신순으로 보여준다."""
        if not self.history:
            print("📭 아직 게임 기록이 없습니다. '퀴즈 풀기'로 첫 기록을 남겨보세요!\n")
            return

        total_games = len(self.history)
        average = sum(record["score"] for record in self.history) / total_games
        recent = list(reversed(self.history))[: self.HISTORY_DISPLAY_LIMIT]

        print(f"📜 게임 기록 (총 {total_games}회, 평균 {average:.1f}점)\n")
        print(THIN_LINE)
        # 한글은 터미널에서 2칸을 차지하므로 머리글은 공백을 직접 맞춘다
        print("일시" + " " * 18 + "정답  힌트     점수")
        print(THIN_LINE)
        for record in recent:
            print(self._format_history_row(record))
        print(THIN_LINE)
        if total_games > self.HISTORY_DISPLAY_LIMIT:
            print(f"※ 최근 {self.HISTORY_DISPLAY_LIMIT}개 기록만 표시합니다.")
        print()

    # ------------------------------------------------------------------
    # 점수 기록
    # ------------------------------------------------------------------
    def _record_result(self, result: dict) -> bool:
        """게임 결과를 기록에 추가하고 최고 점수를 갱신한다. 새 최고 점수면 True."""
        self.history.append(result)
        if self.best_score is None or result["score"] > self.best_score:
            self.best_score = result["score"]
            self.best_record = result
            return True
        return False

    # ------------------------------------------------------------------
    # 입력 / 출력 보조
    # ------------------------------------------------------------------
    def _ask_question_count(self) -> int:
        total = len(self.quizzes)
        if total == 1:
            return 1
        return read_int(f"몇 문제를 풀까요? (1-{total}): ", 1, total)

    @staticmethod
    def _confirm(prompt: str) -> bool:
        """y/n 입력을 받아 True/False로 반환한다. 그 밖의 입력은 다시 묻는다."""
        while True:
            answer = read_line(prompt).lower()
            if answer in ("y", "yes", "ㅛ"):
                return True
            if answer in ("n", "no", "ㅜ"):
                return False
            print("⚠️ 잘못된 입력입니다. y 또는 n을 입력하세요.")

    def _format_history_row(self, record: dict) -> str:
        answered = f"{record['correct']}/{record['total']}"
        best_mark = " 🏆" if record == self.best_record else ""
        return (
            f"{self._format_time(record['played_at']):<16}  "
            f"{answered:>8}  {record['hints_used']:>4}  {record['score']:>5}점{best_mark}"
        )

    @staticmethod
    def _format_time(iso_text: str) -> str:
        """'2026-11-20T19:00:00' → '2026-11-20 19:00'."""
        return iso_text.replace("T", " ")[:16]

    # ------------------------------------------------------------------
    # 파일 저장 / 불러오기 (state.json)
    # ------------------------------------------------------------------
    def load(self) -> None:
        """state.json을 읽어 게임 상태를 복원한다. 실패하면 기본 퀴즈로 시작한다."""
        state, status = self.storage.load()

        if status == "loaded" and state is not None:
            try:
                self._apply_state(state)
            except ValueError:
                status = "corrupted"
            else:
                best = f"{self.best_score}점" if self.best_score is not None else "기록 없음"
                print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {best})")
                return

        if status == "missing":
            print(f"📂 저장된 데이터가 없어 기본 퀴즈 {len(self.quizzes)}개로 시작합니다.")
            self.save()
        elif status == "corrupted":
            print("⚠️ 데이터 파일이 손상되어 기본 퀴즈로 복구합니다. (원본은 state.json.bak에 백업)")
            self._reset_state()
            self.save()
        else:
            # 읽기 오류: 기존 파일을 덮어쓰지 않도록 저장하지 않는다
            print("⚠️ 데이터 파일을 읽을 수 없어 기본 퀴즈로 시작합니다. (이번 실행 내용은 저장되지 않을 수 있습니다)")

    def save(self) -> bool:
        """현재 상태를 state.json에 저장한다. 실패하면 안내 후 False."""
        if self.storage.save(self.to_state()):
            return True
        print(
            "⚠️ 데이터를 파일에 저장하지 못했습니다.\n"
            "   → state.json이 있는 폴더의 쓰기 권한과 디스크 여유 공간을 확인한 뒤 다시 실행해 주세요.\n"
            "   → 기존 state.json은 그대로 남아 있어 마지막으로 저장된 상태는 보존됩니다."
        )
        return False

    def to_state(self) -> dict:
        """현재 게임 상태를 state.json 스키마의 dict로 변환한다."""
        return {
            "version": 1,
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "best_record": self.best_record,
            "history": self.history,
        }

    def _apply_state(self, state: dict) -> None:
        """state dict를 게임 속성에 반영한다. 퀴즈 형식이 틀리면 ValueError."""
        self.quizzes = [Quiz.from_dict(item) for item in state["quizzes"]]
        self.best_score = state["best_score"]
        self.best_record = state["best_record"]
        self.history = state["history"]

    def _reset_state(self) -> None:
        self.quizzes = get_default_quizzes()
        self.best_score = None
        self.best_record = None
        self.history = []
