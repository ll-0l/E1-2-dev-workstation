"""퀴즈 한 문제를 표현하는 Quiz 클래스."""

CHOICE_COUNT = 4


class Quiz:
    """4지선다 퀴즈 한 문제."""

    def __init__(self, question: str, choices: list[str], answer: int, hint: str = "") -> None:
        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제 내용은 비어 있을 수 없습니다.")
        if not isinstance(choices, list) or len(choices) != CHOICE_COUNT:
            raise ValueError(f"선택지는 정확히 {CHOICE_COUNT}개여야 합니다.")
        for choice in choices:
            if not isinstance(choice, str) or not choice.strip():
                raise ValueError("선택지는 비어 있을 수 없습니다.")
        if isinstance(answer, bool) or not isinstance(answer, int) or not 1 <= answer <= CHOICE_COUNT:
            raise ValueError(f"정답 번호는 1~{CHOICE_COUNT} 사이의 정수여야 합니다.")
        if not isinstance(hint, str):
            raise ValueError("힌트는 문자열이어야 합니다.")

        self.question = question.strip()
        self.choices = [choice.strip() for choice in choices]
        self.answer = answer
        self.hint = hint.strip()

    def display(self, number: int | None = None) -> None:
        """문제와 선택지를 출력한다."""
        print()
        if number is not None:
            print(f"[문제 {number}]")
        print(self.question)
        for index, choice in enumerate(self.choices, start=1):
            print(f"  {index}. {choice}")

    def is_correct(self, user_answer: int) -> bool:
        return user_answer == self.answer

    def has_hint(self) -> bool:
        return bool(self.hint)

    def to_dict(self) -> dict:
        return {
            "question": self.question,
            "choices": list(self.choices),
            "answer": self.answer,
            "hint": self.hint,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Quiz":
        """dict로부터 Quiz를 만든다. 형식이 잘못되면 ValueError."""
        if not isinstance(data, dict):
            raise ValueError("퀴즈 데이터는 dict여야 합니다.")
        try:
            return cls(
                question=data["question"],
                choices=data["choices"],
                answer=data["answer"],
                hint=data.get("hint", ""),
            )
        except (KeyError, TypeError) as error:
            raise ValueError(f"퀴즈 데이터 형식이 올바르지 않습니다: {error}") from error

    def __repr__(self) -> str:
        return f"Quiz(question={self.question!r}, answer={self.answer})"
