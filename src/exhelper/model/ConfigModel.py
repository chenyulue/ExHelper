import customtkinter as ctk

dark_fg = "#343a40"
dark_bg = "#0d3b66"
light_fg = "#f9f9ed"
light_bg = "#33658a"

class ConfigModel:
    def __init__(self) -> None:
        self.dark_fg = "#343a40"
        self.dark_bg = "#0d3b66"
        self.light_fg = "#f9f9ed"
        self.light_bg = "#33658a"
        self.label_light = "#343a40"
        self.label_dark = "#f9f9ed"
        self.font = ctk.CTkFont(family="SimHei", size=16)