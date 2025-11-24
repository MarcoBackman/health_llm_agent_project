import logging
from abc import ABC, abstractmethod

from fastapi import APIRouter

class Controller(ABC):

    def __init__(self):
        super().__init__()
        self.router  = APIRouter()
        self._register_routes()
        logging.info(f"Registered routes for {self.__class__.__name__}")

    @abstractmethod
    def _register_routes(self):
        ...