"""퀴즈 1회 플레이를 담당하는 QuizSession 클래스."""

import random
from datetime import datetime

import input_utils
from quiz import Quiz


class QuizSession:
    """퀴즈 목록에서 문제를 출제하고 채점하는 1회 플레이 세션."""

    HINT_KEY = "h"

    def __init__(
        self,
        quizzes: list[Quiz],
        count: int | None = None,
        shuffle: bool = True,
        rng: random.Random | None = None,
    ) -> None:
        if not quizzes:
            raise ValueError("출제할 퀴즈가 없습니다.")
        if count is None:
            count = len(quizzes)
        if isinstance(count, bool) or not isinstance(count, int) or not 1 <= count <= len(quizzes):
            raise ValueError(f"문제 수는 1~{len(quizzes)} 사이여야 합니다.")

        selected = list(quizzes)
        if shuffle:
            (rng or random).shuffle(selected)
        self.quizzes = selected[:count]

    def play(self) -> dict:
        """문제를 순서대로 출제하고 결과(history 항목 형태)를 반환한다."""
        total = len(self.quizzes)
        correct = 0
        hints_used = 0
        hinted_correct = 0

        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제, 힌트는 '{self.HINT_KEY}' 입력)")

        for number, quiz in enumerate(self.quizzes, start=1):
            quiz.display(number)
            hint_used = False

            while True:
                user_input = input_utils.read_int(
                    f"정답 입력 (1-4, 힌트: {self.HINT_KEY}): ",
                    1,
                    4,
                    allow=(self.HINT_KEY,),
                )
                if user_input != self.HINT_KEY:
                    break
                if not quiz.has_hint():
                    print("💡 이 문제는 힌트가 없습니다.")
                elif hint_used:
                    print(f"💡 힌트(다시 보기): {quiz.hint}")
                else:
                    hint_used = True
                    hints_used += 1
                    print(f"💡 힌트: {quiz.hint} (맞히면 이 문제는 절반 점수)")

            if quiz.is_correct(user_input):
                correct += 1
                if hint_used:
                    hinted_correct += 1
                    print("✅ 정답입니다! (힌트 사용으로 절반 점수)")
                else:
                    print("✅ 정답입니다!")
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번 '{quiz.choices[quiz.answer - 1]}'입니다.")

        score = self.calculate_score(correct, hinted_correct, total)
        result = {
            "played_at": datetime.now().isoformat(timespec="seconds"),
            "total": total,
            "correct": correct,
            "hints_used": hints_used,
            "hinted_correct": hinted_correct,
            "score": score,
        }
        self._print_result(result)
        return result

    @staticmethod
    def calculate_score(correct: int, hinted_correct: int, total: int) -> int:
        """정답 100%, 힌트 보고 맞힌 문제 50%로 0~100점을 계산한다.

        소수점 첫째 자리에서 반올림(.5는 항상 올림)한다.
        내장 round()는 .5를 짝수 쪽으로 보내 62.5→62, 37.5→38처럼 결과가 들쭉날쭉해서
        정수 연산으로 계산한다: 100 * (correct - hinted/2) / total = (200c - 100h) / 2t
        """
        if total <= 0:
            return 0
        doubled = 200 * correct - 100 * hinted_correct
        return (doubled + total) // (2 * total)

    @staticmethod
    def _print_result(result: dict) -> None:
        print("\n" + "=" * 40)
        print("🏁 퀴즈 결과")
        print(f"  맞힌 문제: {result['correct']} / {result['total']}")
        print(f"  힌트 사용: {result['hints_used']}회 (힌트 후 정답 {result['hinted_correct']}개)")
        print(f"  점수: {result['score']}점")
        print("=" * 40)
