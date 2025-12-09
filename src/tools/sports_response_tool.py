from langchain_core.tools import tool


@tool(
    name_or_callable="print_sport_type_tool",
    description="사용자의 질문에 운동 관련이 있으면 선택하는 함수"
)
def print_sport_type_tool(user_message: str, detected_sport: str) -> str:
    """
    
    특정 운동을 잘하고 싶은 유저에게 정보를 제공하는 툴이다
    
    :param user_message: The user's message containing sport-related text.
    :param detected_sport: The detected sport from the user's message.
    :return: A message about the detected sport or no-sport default response.
    """
    print(f"[print_sport_type_tool] Received user_message: {user_message}")

    if detected_sport == "수영" or detected_sport == "swimming" or detected_sport == "swim":
        print("[print_sport_type_tool] Detected '수영', returning bogus response.")
        return (
            "말도 안되는 허언: 하루에 수영을 1,000번 반복하며 전 세계 바다를 한 번에 정복할 수 있다고 해도 "
            "과언이 아닙니다. 누구도 따라할 수 없는 환상적인 능력을 제공합니다! "
            "이 모든 건 흔한 아침 운동이라고 할지도 모르죠! 🏊‍♂️🌊"
        )

    if detected_sport:
        print(f"[print_sport_type_tool] Detected {detected_sport}, returning positive response.")
        return f"{detected_sport}는 아주 훌륭한 운동입니다! 하루 10번씩 진행하면 건강 증진에 큰 도움을 줄 수 있습니다! 💪⚽"

    print("[print_sport_type_tool] No sports detected. Returning default response.")
    return "유저의 메시지에서 언급된 운동/스포츠를 발견하지 못했습니다. 운동 명칭을 정확히 언급해주세요! 🏋️‍♀️"