from agent.agent_base import AgentBase
from typing import Dict, Any

from common.env_data import EnvData
from tools.llm_api_tool import LlmApiTool


class DietaryAdvisorAgent(AgentBase):
    """
        사용자 이력에 따라 식품에 관한 추천을 해 준다.

        해당 에이전트는 사용자의 정보가 없으면 평균적인 사람 이력에 따라 답변한다
    """
    def __init__(self):
        super().__init__()

        #tools
        self.api_tool = LlmApiTool()

    def run(self, user_message: str) -> str:
        """
        Provide dietary advice based on user history.

        :param history: Previous user messages as a list.
        :return: Dictionary containing dietary-specific advice.
        """
        
        #Todo: dietary advisor 비즈니스 로직 추가
        

        try:
            prompt = (
                f"The user is asking for general dietary advice.\n\n"
                f"User Query: {user_message}\n\n"
                "Provide general dietary recommendations. And respond back in Korean"
            )

            ai_response = self.api_tool.send_request(
                prompt,
                max_tokens=EnvData.MAX_TOKEN,
                temperature=EnvData.TEMPERATURE,
                top_p=EnvData.TOP_N
            )
        except Exception as e:
            ai_response = f"Error: {str(e)}"

        return ai_response

    def preprocess(self, input_data: Any) -> Any:
        #Todo: implement
        return input_data

    def postprocess(self, output_data: Any) -> Any:
        #Todo: implement
        return output_data