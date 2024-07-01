import customtkinter as ctk
from CTkSpinbox import CTkSpinbox

from ..model.ConfigModel import ConfigModel

class CheckDefectFrame(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.setting = ConfigModel()

        self._configure_grid([(0, 2), (1, 1)], [(0, 1), (1, 0)])

        self.tabview_check = self._create_panel(
            ["摘要", "权利要求书", "说明书及附图"], two_texts=2
        )
        self.tabview_check.grid(row=0, column=0, sticky="nsew")

        self.tabview_result = self._create_panel(
            ["摘要及其他缺陷", "权利要求书缺陷", "说明书及附图缺陷"], height=200)
        self.tabview_result.grid(row=1, column=0, sticky="nsew")

        self.check_import = self._create_import_setting_buttons()
        self.check_import.grid(row=0, column=1, sticky="ns", padx=5, pady=(18, 0))

        self.btns_check = self._create_check_buttons()
        self.btns_check.grid(row=1, column=1, sticky="wen", padx=5, pady=18)

    def _create_panel(self, tags: list[str], height:int=420, two_texts: None|int = None) -> ctk.CTkTabview:
        tabview = ctk.CTkTabview(
            self, width=800,
            segmented_button_selected_color=self.setting.light_bg,
            text_color=self.setting.light_fg,
        )
        
        for i, tag in enumerate(tags):
            tabview.add(tag)
            if i != two_texts:
                tabview.tab(tag).grid_rowconfigure(0, weight=1)
                tabview.tab(tag).grid_columnconfigure(0, weight=1)
                text = ctk.CTkTextbox(tabview.tab(tag), width=810, height=height)
                text.grid(sticky="nsew")
            else:
                tabview.tab(tag).grid_rowconfigure(0, weight=0)
                tabview.tab(tag).grid_rowconfigure(1, weight=1)
                tabview.tab(tag).grid_columnconfigure(0, weight=7)
                tabview.tab(tag).grid_columnconfigure(1, weight=1)
                label_left = ctk.CTkLabel(
                    tabview.tab(tag), text="说明书：", font=self.setting.font,
                )
                label_right = ctk.CTkLabel(
                    tabview.tab(tag), text="附图：", font=self.setting.font,
                )
                label_left.grid(row=0, column=0, sticky="w")
                label_right.grid(row=0, column=1, sticky="w")
                text_left = ctk.CTkTextbox(tabview.tab(tag), width=700, height=height-20)
                text_right = ctk.CTkTextbox(tabview.tab(tag), width=100, height=height-20)
                text_left.grid(row=1, column=0, padx=(0, 5), sticky="nsew")
                text_right.grid(row=1, column=1, padx=(5, 0), sticky="nsew")
            
        return tabview

    def _create_check_buttons(self) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(self)

        switch_seg = ctk.CTkSwitch(
            frame, text="权利要求自动分词", font=self.setting.font,
            text_color=self.setting.dark_fg,
        )
        switch_seg.grid(row=0, column=0, columnspan=2, sticky="w", padx=5, pady=(5,0))

        label_length = ctk.CTkLabel(
            frame, text="最短截词长度", font=self.setting.font,
            text_color=self.setting.dark_fg,
        )
        label_length.grid(row=1, column=0, sticky="w", padx=5, pady=(0,5))
        spinbox_length = CTkSpinbox(
            frame, start_value=2, min_value=1, max_value=20, scroll_value=1,
        )
        spinbox_length.grid(row=1, column=1, sticky="w", padx=5, pady=(0, 5))

        btn_clear = ctk.CTkButton(
            frame, text="清空", fg_color=self.setting.light_bg,
            font=self.setting.font, text_color=self.setting.light_fg,
            hover_color=self.setting.hover_color,
            width=50
        )
        btn_clear.grid(row=2, column=0, padx=5, pady=5, sticky="we")
        btn_check = ctk.CTkButton(
            frame, text="检查", fg_color=self.setting.light_bg,
            font=self.setting.font, text_color=self.setting.light_fg,
            hover_color=self.setting.hover_color,
            width=50,
        )
        btn_check.grid(row=2, column=1, padx=5, pady=5, sticky="we")

        return frame

    def _create_import_setting_buttons(self):
        frame = ctk.CTkFrame(self)

        frame.grid_rowconfigure(1, weight=1)

        btn_import = ctk.CTkButton(
            frame, text="导入文本", font=self.setting.font, 
            text_color=self.setting.light_fg, fg_color=self.setting.light_bg,
            hover_color=self.setting.hover_color,
            width=100,
        )
        btn_import.grid(row=0, column=0, sticky="n", padx=5, pady=5)

        frame_check_items = ctk.CTkScrollableFrame(
            frame, label_text="设置查找项目", label_font=self.setting.font,
            label_fg_color=self.setting.light_bg, 
            label_text_color=self.setting.light_fg,
            # width=150,
        )
        frame_check_items.grid(row=1, column=0, sticky="sn", padx=5, pady=(5,0))

        chk_select_all = ctk.CTkCheckBox(
            frame_check_items, text="全选", font=self.setting.font_bold,
            text_color=self.setting.dark_fg,
        )
        chk_select_all.grid(sticky="w", padx=(5,0), pady=5)
        
        for key, items in self.setting.check_items.items():
            chk_key = ctk.CTkCheckBox(
                frame_check_items, text=key, font=self.setting.font_bold,
                text_color=self.setting.dark_fg,
            )
            chk_key.grid(sticky="w", padx=(5,0), pady=(15, 5))
            for item in items:
                chk_item = ctk.CTkCheckBox(
                    frame_check_items, text=item, font=self.setting.font,
                    text_color=self.setting.dark_fg
                )
                chk_item.grid(sticky="w", padx=(25, 0), pady=(0, 5))

        return frame

    def _configure_grid(self, rows: list[tuple[int, int]], cols: list[tuple[int, int]]) -> None:
        for row in rows:
            self.grid_rowconfigure(row[0], weight=row[1])
        for col in cols:
            self.grid_columnconfigure(col[0], weight=col[1]) 