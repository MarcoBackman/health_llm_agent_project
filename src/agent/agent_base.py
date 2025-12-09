from abc import ABC, abstractmethod
from typing import Any, Dict


class AgentBase(ABC):
    """
        Agent클라스 의 인터페이스

    """

    def run(self, user_message: str):
        """
        The entry point for executing tasks for this agent.

        :param user_message:
        :param user_id:
        """
        ...

    @abstractmethod
    def preprocess(self, input_data: Dict[str, Any]) -> Any:
        """
        Preprocess the input data before execution, if applicable.

        :param input_data: The raw input data that might need processing.
        :return: Preprocessed data.
        """
        ...

    @abstractmethod
    def postprocess(self, output_data: Dict[str, Any]) -> Any:
        """
        Postprocess the result after execution, if applicable.

        :param result: The raw output from the agent processing.
        :return: Final formatted result.
        """
        ...