from agent.agent_base import AgentBase
from typing import Dict, Any

from tools.llm_api_tool import LlmApiTool


class DietaryAdvisorAgent(AgentBase):
    """
        사용자 이력에 따라 식품에 관한 추천을 해 준다.

        해당 에이전트는 사용자의 정보가 없으면 평균적인 사람 이력에 따라 답변한다
    """

    def run(self, user_message: str) -> str:
        """
        Provide dietary advice based on user history.

        :param user_message: User input message.
        :param user_id: Unique identifier for the user.
        :return: Dictionary containing dietary-specific advice.
        """

        try:
            # Dynamically select the tool and method
            ai_response = LlmApiTool.llm_tool.execute_tool(message=user_message)

        except Exception as e:
            # Log and handle exceptions
            print(f"[DietaryAdvisorAgent] Error occurred: {str(e)}")
            ai_response = f"Error: {str(e)}"

        return ai_response

    def preprocess(self, input_data: Any) -> Any:
        #Todo: implement
        return input_data

    def postprocess(self, output_data: Any) -> Any:
        #Todo: implement
        return output_data