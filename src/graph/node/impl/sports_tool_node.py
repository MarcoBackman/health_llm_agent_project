from graph.node.node_base import NodeBase
from graph.state.state import AgentState
from langgraph.prebuilt import ToolNode

from tools.sports_response_tool import print_sport_type_tool

class SportsToolNode(NodeBase):
    """
        툴 노드, 모든 tool을 내포한다
    """

    name = "sports_tool"

    def __init__(self, seq_counter=None):
        super().__init__(seq_counter, SportsToolNode.name)

        self.api_tool = ToolNode([
            print_sport_type_tool,
        ])

        print("바인드 된 툴: ", self.api_tool, "")

    def __call__(self, state: AgentState, config=None):
        self._log_entry(dialog_id=self.node_name, state=state)

        self._log_exit()
        return self.api_tool


    def _update_state(self, state: AgentState, config=None):
        #Todo: state update
        pass