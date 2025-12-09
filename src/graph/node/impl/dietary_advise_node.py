from agent.impl.dietary_advisor_agent import DietaryAdvisorAgent
from graph.node.node_base import NodeBase
from graph.state.state_enum import StateEnum

LAST_MESSAGE_INDEX = -1

class DietaryAdviseNode(NodeBase):
    """
        음식 섭취 관련 조언 노드
    """
    name = "dietary_advisor"

    def __init__(self, seq_counter=None):
        """
        Initialize the DietaryAdvisorNode.

        :param agent: DietaryAgent instance or alternative implementation (for DI).
        :param seq_counter: Sequence counter to track state transitions.
        :param db_logger: Logger for debugging and auditing.
        """
        super().__init__(seq_counter, DietaryAdviseNode.name)
        self.agent = DietaryAdvisorAgent()

    def __call__(self, state, config=None):
        self._log_entry(self.node_name, state)

        # Extract the last user message
        user_message_history = state.get("messages", [])
        if not user_message_history:
            raise ValueError("No user messages found in the state.")

        try:
            user_message = user_message_history[LAST_MESSAGE_INDEX]

            # Use agent to dynamically select the tool
            selection = self.agent.select_tool(user_message)

            # Populate the tool and method in the state for `ToolNode`
            state["selected_tool"] = selection["tool_name"]
            state["selected_method"] = selection["method_name"]

            # Optionally log the selection
            print(f"Selected Tool: {selection['tool_name']}, Method: {selection['method_name']}")

        except Exception as e:
            print(f"Error in DietaryAdviseNode: {e}")
            state["status"] = StateEnum.ERROR

        self._log_exit()
        return state


    def _update_state(self, state, config=None):
        #Todo: update 할 state 들
        pass