from typing import TypedDict

from graph.state.state_enum import StateEnum

class AgentState(TypedDict, total=False):
    """
        LangGraph에서 사용될 Agent의 상태(State) 정의
    """
    id: str
    description: str
    current_node: str
    collected_data: dict
    status: StateEnum
    tools_used: list[str]
    messages: list[str]
    ai_responses: dict
    final_response: str
    is_sport_related: bool
    selected_tool: str
    selected_method: str