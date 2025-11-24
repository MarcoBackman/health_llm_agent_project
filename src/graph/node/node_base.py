from abc import ABC, abstractmethod

from graph.state.state import AgentState


class NodeBase(ABC):

    def __init__(self,
                 seq_counter,
                 node_name="UnnamedNode"):
        self.seq_counter = seq_counter
        self.node_name = node_name

    @abstractmethod
    def __call__(self, state: AgentState, config: dict = None):
        ...

    def _log_exit(self):
        #Todo: append extra info
        print(f"Exiting node. {self.node_name}.")

    def _log_entry(self, dialog_id=None, state=None):
        print(f"Entering node: {self.node_name}. Dialog ID: {dialog_id}, State: {state}")

    def _parse_response(self, response):
        #Todo: response parsing
        return response

    @abstractmethod
    def _update_state(self, state: dict):
        """
            노드가 프로세스 수행을 완료하면 업데이트 할 내용을 State에 적용
        :return: 
        """
        ...
