import customtkinter as ctk
from .. import assets

class ConfigModel:
    def __init__(self) -> None:
        self.font_bold = ctk.CTkFont(family="SimHei", size=16, weight="bold", underline=True)
        self.font_text = ctk.CTkFont(family="SimSun", size=16)
        self.text_spacing2 = 7
        self.text_spacing3 = 15
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
        self.theme = assets.DEFAULT_THEME