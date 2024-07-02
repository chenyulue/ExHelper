import customtkinter as ctk

class ConfigModel:
    def __init__(self) -> None:
        self.dark_fg = "#343a40"
        self.dark_bg = "#0d3b66"
        self.light_fg = "#f9f9ed"
        self.light_bg = "#33658a"
        self.label_light = "#343a40"
        self.label_dark = "#f9f9ed"
        self.hover_color = "#0077b6"
        self.font = ctk.CTkFont(family="SimHei", size=16)
        self.font_bold = ctk.CTkFont(family="SimHei", size=16, weight="bold", underline=True)
        self.text_font = ctk.CTkFont(family="SimSun", size=16)
        self.check_items = {
            "摘要及其他缺陷": [
                "发明名称是否修改", "发明名称字数", 
                ],
            "权利要求书缺陷": [
                "缺乏引用基础", "非择一引用", "疑似不清楚措辞",
            ],
            "说明书及附图缺陷": [
                "图号一致性", "附图标记错误"
            ]
        }
        self.original_text_color = "red"
        self.modified_text_color = "blue"