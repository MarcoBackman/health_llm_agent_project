from typing import Any

from agent.agent_base import AgentBase
from tools.llm_api_tool import LlmApiTool
from tools.sports_response_tool import print_sport_type_tool


class SportsAdvisorAgent(AgentBase):

    def run(self, user_message: str) -> str:
        """
        Provide health advice for specific activities.
        """

        try:
            LlmApiTool.llm_tool.bind_tool_to_api([print_sport_type_tool])
            response = LlmApiTool.llm_tool.invoke(input=user_message)

            # 현재 응답에서 호출된 모든 tool 이름을 추출
            print(f"SportsAdvisorAgent response: {response}")
            tool_calls = response.additional_kwargs.get("tool_calls", [])
            print(f"tool_calls={tool_calls}")
            tools_used = [t["function"]["name"] for t in tool_calls]
            if tools_used:
                print(f"[SportsAdvisorAgent] Tools used: {tools_used}")
                return response.content


        except Exception as e:
            # Log errors and fall back to an error message
            print(f"[SportsAdvisorAgent] Error during tool execution: {str(e)}")

        return ""


    def preprocess(self, input_data: Any) -> Any:
        # Prepare user query before processing
        if isinstance(input_data, str):
            return input_data.strip()
        raise ValueError("Expected input to be a string.")

    def postprocess(self, output_data: Any) -> Any:
        # Format and clean up the response before returning it
        return str(output_data).strip()
