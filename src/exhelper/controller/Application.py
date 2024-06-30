import customtkinter as ctk

from ..view.MainFrame import MainFrame

class Application(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("审查助手 - ExHelper")
        self.minsize(1200, 800)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.main_frame = MainFrame(self)
        self.main_frame.grid(sticky="nsew")

    def run(self):
        self.mainloop()