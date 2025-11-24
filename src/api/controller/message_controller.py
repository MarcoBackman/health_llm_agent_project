from langgraph.constants import START

from api.controller.abstract_controller import Controller
from api.dto.message_dto import HealthMessageResponseDto
from api.service.message_service import MessageService
from graph.graph_mananger import GraphManager
from graph.state.state_enum import StateEnum

class MessageController(Controller):
    def __init__(self):
        super().__init__()

        #Dependency Injection
        self.graph = GraphManager.get_graph()
        self.message_service = MessageService()

    def _register_routes(self):

        @self.router.post("/process_message")
        def process_message(user_message: str) -> dict:
            """
            Process the user's message through the LangGraph workflow.

            :param user_message: The message input by the user.
            :return: Dictionary containing final summarized results for the user.
            """

            # 서비스 호출
            response, is_error = self.message_service.process_message(user_message)
            response_dto = HealthMessageResponseDto(response, is_error)

            # Return the final structured output
            return response_dto.to_dict()

        @self.router.post("/check_sports_related")
        def _check_is_sports_related(updated_state: dict) -> bool:
            """
            테스트 용
            :param self:
            :param updated_state:
            :return:
            """
            return updated_state.get(StateEnum.IS_SPORT_RELATED.value, False)