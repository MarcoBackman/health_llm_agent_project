from typing import Dict, Any

from agent.agent_base import AgentBase
from common.env_data import EnvData
from tools.llm_api_tool import LlmApiTool
from tools.user_sports_tool import UserSportsTool


class SportsAdvisorAgent(AgentBase):

    def __init__(self):
        super().__init__()

        #Tools
        self.api_tool = LlmApiTool()
        self.sports_tool: UserSportsTool = UserSportsTool()


    def run(self, user_message: str) -> str:
        """
        Provide health advice for specific activities.
        """

        try:
            ai_response = self.api_tool.send_request(
                user_message,
                max_tokens=EnvData.MAX_TOKEN,
                temperature=EnvData.TEMPERATURE,
                top_p=EnvData.TOP_N
            )
        except Exception as e:
            ai_response = f"Error: {str(e)}"

        return self.sports_tool.process_message(ai_response["response"])

    def preprocess(self, input_data: Dict[str, Any]) -> Any:
        #Todo: implement
        pass

    def postprocess(self, output_data: Dict[str, Any]) -> Any:
        #Todo: implement
        pass