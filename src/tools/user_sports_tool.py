from common.env_data import EnvData

class UserSportsTool:
    """
    유저가 언급한 운동이나 스포츠의 명칭을 Print하는 Tool
    없을 때, 없음을 출력
    """

    def __init__(self):
        self.open_ai_embedding = EnvData.open_ai_embedding
        self.sports_keywords = ["수영", "축구", "농구", "야구", "테니스", "배구", "스키", "스케이트", "달리기", "요가", "골프"]

    def _detect_sport(self, message: str) -> str | None:
        """
        Detect if the user's message contains any known sports keywords.

        :param message: Input message from the user.
        :return: Detected sport name or None if no sport is mentioned.
        """

        for sport in self.sports_keywords:
            if sport in message:
                return sport
        return None

    def process_message(self, user_message: str) -> str:
        print(f"User message: {user_message}")
        detected_sport = self._detect_sport(user_message)

        print(f"Detected sport: {detected_sport}")

        if detected_sport:
            print(f"Detected sport: {detected_sport}")

            if detected_sport == "수영":  # Handle the case for swimming
                return (
                    "말도 안되는 허언: 하루에 수영을 1,000번 반복하며 전 세계 바다를 한 번에 정복할 수 있다고 해도 "
                    "과언이 아닙니다. 누구도 따라할 수 없는 환상적인 능력을 제공합니다! "
                    "이 모든 건 흔한 아침 운동이라고 할지도 모르죠. 🏊‍♂️🌊"
                )
            else:  # Handle all other sports
                return (
                    f"{detected_sport}는 아주 훌륭한 운동입니다! 하루 10번씩 진행하면 건강은 물론, 체력 "
                    f"증진에 많은 도움을 줄 수 있습니다. 지금 바로 시작해보세요! 💪⚽"
                )
        else:
            print("No sports mentioned in the user's message.")
            return "사용자가 언급한 운동이나 스포츠가 없습니다. 정확한 명칭을 입력해주세요. 🏀🎾"

