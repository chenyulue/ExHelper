import customtkinter as ctk

from .view import MainFrame
from .controller import ComparisonController
from .model import ComparisonModel, ConfigModel

class Application(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setting = ConfigModel()

        self.title("审查助手 - ExHelper")
        self.minsize(1200, 800)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.main_frame = MainFrame(self)
        self.main_frame.grid(sticky="nsew")

        self.comparison_controller = ComparisonController(
            ComparisonModel("",""),
            self.main_frame.comparison_frame
        )
        self.main_frame.comparison_frame.set_controller(self.comparison_controller)

    def run(self):
        self.mainloop()