"""게임 전체를 관리하는 QuizGame 클래스."""

from default_quizzes import get_default_quizzes
from input_utils import read_int, read_line, read_text
from quiz import Quiz
from quiz_session import QuizSession

LINE = "=" * 40
THIN_LINE = "-" * 40


class QuizGame:
    """메뉴를 보여주고 사용자의 선택에 따라 각 기능을 실행한다."""

    TITLE = "🎯 MZ 신조어 퀴즈 게임 🎯"

    def __init__(self) -> None:
        self.quizzes: list[Quiz] = get_default_quizzes()
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
        """메인 루프. Ctrl+C / 입력 스트림 종료 시에도 안전하게 종료한다."""
        self.show_title()
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

    # ------------------------------------------------------------------
    # 메뉴 기능 (이후 커밋에서 구현)
    # ------------------------------------------------------------------
    def play_quiz(self) -> None:
        """문제 수를 고른 뒤 QuizSession으로 퀴즈를 진행한다."""
        if not self.quizzes:
            print("📭 등록된 퀴즈가 없습니다. '퀴즈 추가'에서 먼저 퀴즈를 등록하세요.\n")
            return

        count = self._ask_question_count()
        session = QuizSession(self.quizzes, count=count)
        session.play()
        print()

    def _ask_question_count(self) -> int:
        total = len(self.quizzes)
        if total == 1:
            return 1
        return read_int(f"몇 문제를 풀까요? (1-{total}): ", 1, total)

    def add_quiz(self) -> None:
        """문제, 선택지 4개, 정답 번호, 힌트(선택)를 입력받아 퀴즈를 등록한다."""
        print("📌 새로운 퀴즈를 추가합니다.\n")
        question = read_text("문제를 입력하세요: ")
        choices = [read_text(f"선택지 {number}: ") for number in range(1, 5)]
        answer = read_int("정답 번호 (1-4): ", 1, 4)
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
        self._not_ready()

    def delete_quiz(self) -> None:
        self._not_ready()

    def show_history(self) -> None:
        self._not_ready()

    def quit(self) -> None:
        self.save()
        print("👋 게임을 종료합니다. 다음에 또 만나요!")
        self.running = False

    # ------------------------------------------------------------------
    # 저장 (StateStorage 연동 전 임시)
    # ------------------------------------------------------------------
    def save(self) -> None:
        pass

    @staticmethod
    def _not_ready() -> None:
        print("🚧 준비 중인 기능입니다.\n")
