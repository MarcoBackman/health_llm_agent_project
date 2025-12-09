from graph.node.node_base import NodeBase
from graph.state.state import AgentState
from tools.llm_api_tool import LlmApiTool
from tools.user_message_counter_tool import print_user_message_data


class DietaryToolNode(NodeBase):
    """
        툴 노드, 모든 tool을 내포한다
    """

    name = "dietary_tool"

    def __init__(self, seq_counter=None):
        super().__init__(seq_counter, DietaryToolNode.name)

        LlmApiTool.llm_tool.bind_tool_to_api([print_user_message_data])

        self.api_tool = LlmApiTool.bind_tool_to_api([
            print_user_message_data,
        ])

    def __call__(self, state: AgentState, config=None):
        self._log_entry(dialog_id=self.node_name, state=state)
        return state


    def _update_state(self, state: AgentState, config=None):
        #Todo: state update
        pass