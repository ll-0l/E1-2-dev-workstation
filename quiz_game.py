"""게임 전체를 관리하는 QuizGame 클래스."""

from input_utils import read_int

LINE = "=" * 40
THIN_LINE = "-" * 40


class QuizGame:
    """메뉴를 보여주고 사용자의 선택에 따라 각 기능을 실행한다."""

    TITLE = "🎯 MZ 신조어 퀴즈 게임 🎯"

    def __init__(self) -> None:
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
        self._not_ready()

    def add_quiz(self) -> None:
        self._not_ready()

    def list_quizzes(self) -> None:
        self._not_ready()

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
