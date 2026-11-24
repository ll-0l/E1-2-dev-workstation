"""공통 입력/검증 함수.

모든 사용자 입력은 이 모듈을 거친다.
KeyboardInterrupt / EOFError 는 여기서 잡지 않고 호출자(QuizGame.run)로 전파한다.
"""


def read_line(prompt: str) -> str:
    """한 줄을 입력받아 앞뒤 공백을 제거해 반환한다."""
    return input(prompt).strip()


def read_text(prompt: str) -> str:
    """비어 있지 않은 문자열을 입력받을 때까지 반복한다."""
    while True:
        text = read_line(prompt)
        if text:
            return text
        print("⚠️ 입력이 비어 있습니다. 내용을 입력하세요.")


def read_int(
    prompt: str,
    min_value: int,
    max_value: int,
    allow: tuple[str, ...] = (),
) -> int | str:
    """min_value~max_value 범위의 정수를 입력받는다.

    allow 에 포함된 문자열(대소문자 무시)을 입력하면 그 문자열(소문자)을 그대로 반환한다.
    빈 입력, 숫자 변환 실패, 범위 밖 숫자는 안내 메시지 출력 후 다시 입력받는다.
    """
    allowed = {keyword.lower() for keyword in allow}
    range_message = f"⚠️ 잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요."

    while True:
        raw = read_line(prompt)

        if not raw:
            print(f"⚠️ 입력이 비어 있습니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
            continue

        if raw.lower() in allowed:
            return raw.lower()

        try:
            number = int(raw)
        except ValueError:
            print(range_message)
            continue

        if not min_value <= number <= max_value:
            print(range_message)
            continue

        return number
