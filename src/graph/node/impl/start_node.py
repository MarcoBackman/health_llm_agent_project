from graph.node.node_base import NodeBase
from graph.state.state import AgentState


class StartNode(NodeBase):
    """
    A dummy starting node.
    """

    name = "START"

    def __init__(self, seq_counter=None):
        super().__init__(seq_counter=seq_counter, node_name=StartNode.name)

    def __call__(self, state: AgentState, config: dict = None):
        print("[StartNode] Passing state forward to the next node.")
        return state


    def _update_state(self, state, config=None):
            pass