from typing import Dict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph

from graph.node.impl.dietary_advise_node import DietaryAdviseNode
from graph.node.impl.dietary_tool_node import DietaryToolNode
from graph.node.impl.final_summary_node import FinalSummaryNode
from graph.node.impl.sports_advise_node import SportsAdviseNode
from graph.node.impl.sports_tool_node import SportsToolNode
from graph.node.impl.topic_validation_node import TopicValidationNode

from graph.node.impl.user_profile_load_node import UserProfileLoadNode
from graph.state.state import AgentState
from graph.state.state_enum import StateEnum


def build_graph():
    """
        기존에 정의된 노드, 간선을 불러들이고 MemorySaver을 이용해 그래프를 컴파일(제작)
    """

    # StateGraph Builder
    builder = StateGraph(AgentState)

    # Nodes

    builder.add_node(TopicValidationNode.name, TopicValidationNode())
    builder.add_node(UserProfileLoadNode.name, UserProfileLoadNode())
    builder.add_node(SportsAdviseNode.name, SportsAdviseNode())
    builder.add_node(DietaryAdviseNode.name, DietaryAdviseNode())
    builder.add_node(FinalSummaryNode.name, FinalSummaryNode())
    builder.add_node(SportsToolNode.name, SportsToolNode())
    builder.add_node(DietaryToolNode.name, DietaryToolNode())

    # Edges
    builder.add_edge(START, TopicValidationNode.name)
    builder.add_edge(TopicValidationNode.name, UserProfileLoadNode.name)

    #conditional edge
    def is_sports_related_dynamic(state: Dict) -> str:
        result = state.get(StateEnum.IS_SPORT_RELATED.value)
        return SportsAdviseNode.name if result else DietaryAdviseNode.name


    builder.add_conditional_edges(
        source=UserProfileLoadNode.name,
        path=is_sports_related_dynamic,
        path_map={SportsAdviseNode.name: SportsAdviseNode.name, DietaryAdviseNode.name: DietaryAdviseNode.name}
    )

    builder.add_conditional_edges(
        source=SportsAdviseNode.name,
        path=lambda state: state.get(StateEnum.AI_RESPONSES.value),
        path_map={True: FinalSummaryNode.name, False: SportsToolNode.name}
    )
    builder.add_edge(SportsToolNode.name, SportsAdviseNode.name)


    builder.add_conditional_edges(
        source=DietaryAdviseNode.name,
        path=lambda state: state.get(StateEnum.AI_RESPONSES.value),
        path_map={True: FinalSummaryNode.name, False: DietaryToolNode.name}
    )
    builder.add_edge(DietaryToolNode.name, DietaryAdviseNode.name) #복귀


    # Direct transition to FinalSummaryNode after ToolNode execution
    builder.add_edge(SportsToolNode.name, FinalSummaryNode.name)

    # Connect FinalSummaryNode to END to complete the graph
    builder.add_edge(FinalSummaryNode.name, END)


    # Define memory checkpoint =========================================
    memory = MemorySaver()

    # Compile and return the graph =====================================
    return builder.compile(checkpointer=memory)


if __name__ == "__main__":
    graph = build_graph()
    # Example usage of graph could be initialized here, depending on the framework