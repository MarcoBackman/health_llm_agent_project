from agent.agent_base import AgentBase
from typing import Dict, Any

from common.env_data import EnvData
from tools.llm_api_tool import LlmApiTool

class HealthAdvisorAgent(AgentBase):
    """
        해당 거강 Advisor Agent는 사용자의 프로필에 따라 건강 수치를 불러오고 요약해주는 기능을 한다

        향후 사용될 부수 적 조언 Agent에 쓰일 정보를 수취해 준다.
        만약 등록 프로필이 없다면 질문 자체에서 키워드 필터링을 수행에 최대한 정보를 수집하고 임베딩을 진행한다.
    """
    def __init__(self):
        super().__init__()

    def run(self, user_message: str) -> str:
        """
        Provide health advice for specific activities.
        """

        try:
            ai_response = LlmApiTool.llm_tool.execute_tool(message=user_message)
        except Exception as e:
            ai_response = f"Error: {str(e)}"


        return ai_response


    def preprocess(self, input_data: Dict[str, Any]) -> Any:
        #Todo: implement
        pass

    def postprocess(self, output_data: Dict[str, Any]) -> Any:
        #Todo: implement
        pass