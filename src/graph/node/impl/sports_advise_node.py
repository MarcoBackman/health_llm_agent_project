from agent.impl.sports_advisor_agent import SportsAdvisorAgent
from graph.node.node_base import NodeBase

from graph.state.state import AgentState
from graph.state.state_enum import StateEnum

LAST_MESSAGE_INDEX = -1

class SportsAdviseNode(NodeBase):
    """
        건강 조언 노드
        Agent: Health Advisor Agent
        Tool: LLM API

    """
    name = "sports_advisor"

    def __init__(self, seq_counter=None):
        super().__init__(seq_counter, SportsAdviseNode.name)
        self.agent = SportsAdvisorAgent()

    def __call__(self, state: AgentState, config=None):
        self._log_entry(dialog_id=self.node_name, state=state)

        user_message_history = state.get("messages", [])
        user_message = user_message_history[LAST_MESSAGE_INDEX]
        user_id = state["id"]


        try:
            # Delegate message processing to the agent
            tool_response = self.agent.run(user_message=user_message)

            # Log and update the AI response in state
            print(f"[SportsAdviseNode] Tool response: {tool_response}")
            if tool_response:
                state[StateEnum.AI_RESPONSES.value] = tool_response

        except Exception as e:
            print(f"[SportsAdviseNode] Error: {e}")
            state["status"] = StateEnum.ERROR
            state["ai_responses"] = {"response": f"Error: {str(e)}"}

        self._log_exit()
        return state

    def _update_state(self, state, config=None):
        #Todo: update 할 state 들
        pass