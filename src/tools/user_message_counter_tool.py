from langchain_core.tools import tool


@tool(
    name_or_callable="print_user_message_data",
    description="유저 질의의 글자수와 그동안 쌓인 유저의 메시지 수를 print하는 tool"
)
def print_user_message_data(self, user_id: str, user_message: str) -> str:
    char_count = len(user_message)

    # Increment the message count for the user
    if user_id not in self.message_count_by_user:
        self.message_count_by_user[user_id] = 0
    self.message_count_by_user[user_id] += 1

    # Get the updated message count for the user
    total_messages = self.message_count_by_user[user_id]

    # Return the result as a formatted string
    return (
        f"유저 ID: {user_id}\n"
        f"이번 메시지의 글자수: {char_count}자\n"
        f"지금까지 유저가 보낸 총 메시지 수: {total_messages}개"
    )
