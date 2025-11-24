from agent.impl.dietary_advisor_agent import DietaryAdvisorAgent
from graph.node.node_base import NodeBase

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
        """
        Execute the dietary advice logic and update the state.

        :param state: Current AgentState.
        :param config: Optional configuration.
        :return: Updated state with dietary advice.
        """
        self._log_entry(self.node_name, state)

        try:
            user_message_history = state.get("messages", [])
            dietary_advice = self.agent.run(user_message_history[LAST_MESSAGE_INDEX])
        except Exception as e:
            dietary_advice = {"error": str(e)}

        print(f"[DietaryAdviseNode] Dietary Advice: {dietary_advice}")

        updated_state = state.copy()
        updated_state["ai_responses"] = dietary_advice
        self._log_exit()
        return updated_state

    def _update_state(self, state, config=None):
        #Todo: update 할 state 들
        pass