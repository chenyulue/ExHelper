import customtkinter as ctk

from .view import MainFrame
from .controller import ComparisonController, CheckDefectController
from .model import ComparisonModel, ConfigModel, CheckDefectModel
from . import assets

class Application(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setting = ConfigModel()

        self.title("审查助手 - ExHelper")
        self.wm_iconbitmap(assets.APP_ICON)
        
        width, height = 1200, 800
        self.minsize(width, height)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.main_frame = MainFrame(self, self.setting)
        self.main_frame.grid(sticky="nsew")

        self.comparison_controller = ComparisonController(
            ComparisonModel("",""),
            self.main_frame.comparison_frame,
            self.setting,
        )
        self.main_frame.comparison_frame.set_controller(self.comparison_controller)

        self.checkdefect_controller = CheckDefectController(
            CheckDefectModel(),
            self.main_frame.examine_frame,
            self.setting,
        )
        self.main_frame.examine_frame.set_controller(self.checkdefect_controller)

    def run(self):
        self.mainloop()