from agent.impl.sports_advisor_agent import SportsAdvisorAgent
from graph.node.node_base import NodeBase

from graph.state.state import AgentState

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
        #Todo: 비즈니스 로직 추가
        self._log_entry(dialog_id=self.node_name, state=state)

        # Extract activity from state
        user_message_history = state.get("messages", [])

        # Retrieve the side effects or benefits
        final_response = self.agent.run(user_message=user_message_history[LAST_MESSAGE_INDEX])

        print(f"[SportsAdviseNode] Final Response: {final_response}")

        state["ai_responses"] = {"response": final_response}
        self._log_exit()
        return state

    def _update_state(self, state, config=None):
        #Todo: update 할 state 들
        pass