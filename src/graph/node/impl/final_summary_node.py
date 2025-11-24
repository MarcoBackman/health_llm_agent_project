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
        # Todo: 비즈니스 로직 추가
        self._log_entry("final_summary", state)

        final_response = state["ai_responses"]

        updated_state = state.copy()
        updated_state["final_response"] = final_response
        self._log_exit()

        return updated_state

    def _update_state(self, state, config=None):
        #Todo: update 할 state 들
        pass