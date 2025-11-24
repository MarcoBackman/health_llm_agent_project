from common.env_data import EnvData
from graph.node.node_base import NodeBase
from graph.state.state import AgentState
from graph.state.state_enum import StateEnum
from rag_components.embeddings.ko_sbert_nli import get_embedding as ko_sbert_embedding
LAST_USER_MESSAGE = -1  # Current user input

class TopicValidationNode(NodeBase):
    """
    Node to determine whether the user's message is related to sports.

    Uses embedding models to calculate similarity with pre-defined "sports" topics.

    This will update the state is_sports_related to true if applicable
    """

    name = "topic_validation"

    def __init__(self, use_openai=True, seq_counter=None):
        """
        Initialize the TopicValidationNode.

        :param use_openai: Use OpenAI embeddings if True, otherwise use KO-SBERT.
        :param db_logger: Database logger for logging purposes.
        :param seq_counter: Sequence counter to track state transitions.
        """
        super().__init__(seq_counter=seq_counter, node_name=TopicValidationNode.name)
        self.embedding_model = EnvData.open_ai_embedding if use_openai else ko_sbert_embedding()
        self.sports_embedding = self.embedding_model.embed_query("sports")

    def __call__(self, state: AgentState, config = None):
        """
        Execute the node by validating the message and updating the state.

        :param state: The current AgentState containing messages and context.
        :param config: Optional configuration, e.g., dialog ID or thresholds.
        :return: Updated state with validation result.
        """

        # Extract the user's last message
        try:
            last_user_message = state["messages"][LAST_USER_MESSAGE]
        except IndexError:
            raise ValueError(f"[{self.node_name}] No user message found in the state.")
        except KeyError:
            raise KeyError(f"[{self.node_name}] No 'messages' key found in the state.")

        # Embed the user's message
        try:
            user_embedding = self.embedding_model.embed_query(last_user_message)
        except Exception as e:
            raise RuntimeError(f"Failed to generate embedding for the user message: {str(e)}")

        # Calculate similarity with the "sports" embedding
        similarity: float = self._calculate_similarity(user_embedding, self.sports_embedding)

        # Determine if the message is sports-related
        is_sports_related = similarity >= EnvData.similarity_threshold  # Get threshold from EnvData or config
        state["is_sport_related"] = is_sports_related
        print(f"[TopicValidationNode] Similarity Score: {similarity}. is_sports_related={is_sports_related}")
        self._log_entry(dialog_id=self.node_name, state=state)
        self._log_exit()

        return state


    def _update_state(self, state: dict):
        """
        Apply additional state changes or processing if needed.
        :param state: The updated graph state.
        """
        state[StateEnum.MESSAGE.value] = "State updated after topic validation."

    @staticmethod
    def _calculate_similarity(vector_a, vector_b) -> float:
        """
        Calculate cosine similarity between two vectors.
        
        -1: 완전 다른 주제
        0: 일반 적 주제
        1: 매우 유사
        
        :param vector_a: First embedding vector.
        :param vector_b: Second embedding vector.
        :return: Cosine similarity score as a float.
        """
        dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
        norm_a = sum(a**2 for a in vector_a) ** 0.5
        norm_b = sum(b**2 for b in vector_b) ** 0.5
        return dot_product / (norm_a * norm_b)
