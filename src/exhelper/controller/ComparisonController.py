from ..model import ComparisonModel
from ..view import ComparisonFrame
from .Controller import Controller

class ComparisonController(Controller):
    def __init__(self, model: ComparisonModel, view: ComparisonFrame) -> None:
        super().__init__(model, view)
        self.model = model
        self.view = view

    def clear_texts(self) -> None:
        pass

    


