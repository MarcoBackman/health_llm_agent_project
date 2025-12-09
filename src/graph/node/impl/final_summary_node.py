from graph.node.node_base import NodeBase
from graph.state.state import AgentState

LAST_MESSAGE_INDEX = -1

class FinalSummaryNode(NodeBase):
    """
        최종 결과 도출용 노드
    """
    name = "final_summary"

    def __init__(self, seq_counter=None):
        super().__init__(seq_counter, FinalSummaryNode.name)

    def __call__(self, state: AgentState, config=None):
        self._log_entry("final_summary", state)

        # Retrieve AI responses and set the final response
        ai_responses = state.get("ai_responses", {})
        final_response = ai_responses.get("response", "Error: No content in AI response.")

        updated_state = state.copy()
        updated_state["final_response"] = final_response
        self._log_exit()

        return updated_state

    def _update_state(self, state, config=None):
        #Todo: update 할 state 들
        pass