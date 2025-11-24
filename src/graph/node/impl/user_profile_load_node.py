from chroma_db.chroma_db_manager import ChromaDBManager
from graph.node.node_base import NodeBase
from graph.state.state import AgentState
from graph.state.state_enum import StateEnum
from rag_components.retriever.user_data_retriever import UserDataRetriever

LAST_MESSAGE_INDEX = -1

class UserProfileLoadNode(NodeBase):
    """
        건강 관련 조언 노드
    """

    name = "user_profile_loader"

    def __init__(self, seq_counter=None):
        super().__init__(seq_counter, UserProfileLoadNode.name)
        self.user_data_retriever = UserDataRetriever()

    def __call__(self, state: AgentState, config=None):
        self._log_entry(dialog_id="unknown", state=state)

        if "id" not in state:
            raise KeyError(f"{self.node_name}: Missing 'id' field in state for user identification.")

        user_id = state["id"]


        # Retrieve the user profile from ChromaDB
        user_query = f"{user_id} 사용자에 대한 기본적 신체정보를 알려줘."
        user_profile = self.user_data_retriever.query_user_profile_rag(query=user_query)
        if not user_profile:
            print(f"{self.node_name}: No user profile data found for user ID: {user_id}")
            user_profile = "No additional user profile information available."

        print(f"user profile data={user_profile}")

        # Append user profile data to the user's message
        if "messages" in state and isinstance(state["messages"], list):
            state["messages"][LAST_MESSAGE_INDEX] += f"\n\nUser Profile:\n{user_profile}"  # Enrich the last user message
        else:
            raise KeyError(f"{self.node_name}: 'messages' is missing or not a list in the state.")

        self._update_state(state)

        self._log_exit()
        return state

    def _update_state(self, state: AgentState, config=None):
        state["status"] = StateEnum.WORKING