from fastapi import FastAPI

from src.api.controller.message_controller import MessageController


def register_all_controllers(api: FastAPI):
    """
        모든 컨트롤러 클라스를 라우터로 등록
        
        필수 클라스
    """

    message_ctrl = MessageController()
    api.include_router(
        message_ctrl.router,
        prefix="/message",  # "/health"로 시작하는 모든 경로는 해당 컨트롤럭로 이동
        tags=["Message"]    # OpenAPI doc 그룹 이름
    )
