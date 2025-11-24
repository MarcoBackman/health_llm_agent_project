from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph

from graph.graph_builder import build_graph
from graph.state.state import AgentState


class GraphManager:
    """
        전역에서 그래프 정보 접근이 가능한 매니저
    """

    builder = StateGraph(AgentState)
    graph: CompiledStateGraph = None

    # def __new__(cls):
    #     if not hasattr(cls, "_instance"):
    #         cls._instance = super().__new__(cls)
    #     cls.initialize()

    @classmethod
    def initialize(cls):
        cls._build_graph()
        print("[GraphManager] Graph initialized successfully!")

    @classmethod
    def _build_graph(cls):
        cls.graph = build_graph()

    @classmethod
    def get_graph(cls):
        if not cls.graph:
            cls.initialize()
        return cls.graph
