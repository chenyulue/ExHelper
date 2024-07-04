import customtkinter as ctk
from CTkSpinbox import CTkSpinbox
from CTkToolTip import CTkToolTip
from PIL import Image

from ..model.ConfigModel import ConfigModel
from .. import assets

class CheckDefectFrame(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.setting = ConfigModel()
        self.regex_is_on = False

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
        tabview = ctk.CTkTabview(self, width=800,)
        
        for i, tag in enumerate(tags):
            tabview.add(tag)
            if i != two_texts:
                tabview.tab(tag).grid_rowconfigure(0, weight=1)
                tabview.tab(tag).grid_columnconfigure(0, weight=1)
                text = ctk.CTkTextbox(
                    tabview.tab(tag), width=810, height=height,
                    spacing2=self.setting.text_spacing2,
                    spacing3=self.setting.text_spacing3,
                    font=self.setting.font_text,
                )
                text.grid(sticky="nsew")
            else:
                tabview.tab(tag).grid_rowconfigure(0, weight=0)
                tabview.tab(tag).grid_rowconfigure(1, weight=1)
                tabview.tab(tag).grid_columnconfigure(0, weight=7)
                tabview.tab(tag).grid_columnconfigure(1, weight=1)
                label_left = ctk.CTkLabel(tabview.tab(tag), text="说明书：", )
                label_right = ctk.CTkLabel(tabview.tab(tag), text="附图：",)
                label_left.grid(row=0, column=0, sticky="w")
                label_right.grid(row=0, column=1, sticky="w")
                text_left = ctk.CTkTextbox(
                    tabview.tab(tag), width=700, height=height-20,
                    spacing2=self.setting.text_spacing2,
                    spacing3=self.setting.text_spacing3,
                    font=self.setting.font_text,
                )
                text_right = ctk.CTkTextbox(
                    tabview.tab(tag), width=100, height=height-20,
                    spacing2=self.setting.text_spacing2,
                    spacing3=self.setting.text_spacing3,
                    font=self.setting.font_text,
                )
                text_left.grid(row=1, column=0, padx=(0, 5), sticky="nsew")
                text_right.grid(row=1, column=1, padx=(5, 0), sticky="nsew")
            
        return tabview

    def _create_check_buttons(self) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(self)

        entry_search = ctk.CTkEntry(frame, placeholder_text="查找文字...")
        entry_search.grid(row=0, column=0, columnspan=2, sticky="we", padx=(5, 0), pady=5)

        btn_frame = ctk.CTkFrame(frame)
        
        img_size = 15
        img_search = ctk.CTkImage(
            light_image=Image.open(assets.SEARCH_ICON), size=(img_size, img_size)
        )
        self._img_regex_off = ctk.CTkImage(
            light_image=Image.open(assets.REGEX_OFF_ICON), size=(img_size, img_size)
        )
        self._img_regex_on = ctk.CTkImage(
            light_image=Image.open(assets.REGEX_ON_ICON), size=(img_size, img_size)
        )
        btn_bg = ctk.ThemeManager.theme["CTkEntry"]["fg_color"]
        btn_search = ctk.CTkButton(
            btn_frame, image=img_search, text="", compound="top", fg_color=btn_bg,
            width=img_size, height=img_size, hover=False, bg_color=btn_bg, corner_radius=0,
        )
        CTkToolTip(btn_search, message="点击查找", delay=0.5, alpha=0.8)
        btn_search.grid(row=0, column=0, padx=0, pady=0)
        self._btn_regex = ctk.CTkButton(
            btn_frame, image=self._img_regex_off, text="", compound="top", fg_color=btn_bg,
            width=img_size, height=img_size, hover=False, bg_color=btn_bg, corner_radius=0,
            command=self._toggle_regex
        )
        CTkToolTip(self._btn_regex, message="使用正则表达式", delay=0.5, alpha=0.8)
        self._btn_regex.grid(row=0, column=1, padx=0, pady=0)

        btn_frame.grid(row=0, column=0, columnspan=2, sticky="e", padx=4, pady=0)

        switch_seg = ctk.CTkSwitch(frame, text="权利要求自动分词", )
        switch_seg.grid(row=1, column=0, columnspan=2, sticky="w", padx=5, pady=(5,0))

        label_length = ctk.CTkLabel(frame, text="最短截词长度", )
        label_length.grid(row=2, column=0, sticky="w", padx=5, pady=(0,5))
        spinbox_length = CTkSpinbox(
            frame, start_value=2, min_value=1, max_value=20, scroll_value=1,
        )
        spinbox_length.grid(row=2, column=1, sticky="w", padx=5, pady=(0, 5))

        btn_clear = ctk.CTkButton(frame, text="清空", width=50)
        btn_clear.grid(row=3, column=0, padx=5, pady=5, sticky="we")
        btn_check = ctk.CTkButton(frame, text="检查", width=50,)
        btn_check.grid(row=3, column=1, padx=5, pady=5, sticky="we")

        return frame

    def _toggle_regex(self) -> None:
        if self.regex_is_on:
            self._btn_regex.configure(image=self._img_regex_off)
            self.regex_is_on = False
        else:
            self._btn_regex.configure(image=self._img_regex_on)
            self.regex_is_on = True

    def _create_import_setting_buttons(self):
        frame = ctk.CTkFrame(self)

        frame.grid_rowconfigure(1, weight=1)

        entry_import = ctk.CTkEntry(frame, placeholder_text="请输入申请号...",)
        entry_import.grid(row=0, column=0, sticky="ew", padx=(5,0), pady=5)
        btn_import = ctk.CTkButton(frame, text="导入", width=50,)
        btn_import.grid(row=0, column=1, sticky="n", padx=(0, 5), pady=5)

        frame_check_items = ctk.CTkScrollableFrame(frame, label_text="设置查找项目",)
        frame_check_items.grid(row=1, column=0, columnspan=2, sticky="sn", padx=1, pady=(5,0))

        chk_select_all = ctk.CTkCheckBox(
            frame_check_items, text="全选", font=self.setting.font_bold,
        )
        chk_select_all.grid(sticky="w", padx=(5,0), pady=5)
        
        for key, items in self.setting.check_items.items():
            chk_key = ctk.CTkCheckBox(
                frame_check_items, text=key, font=self.setting.font_bold,
            )
            chk_key.grid(sticky="w", padx=(5,0), pady=(15, 5))
            for item in items:
                chk_item = ctk.CTkCheckBox(frame_check_items, text=item,)
                chk_item.grid(sticky="w", padx=(25, 0), pady=(0, 5))

        return frame

    def _configure_grid(self, rows: list[tuple[int, int]], cols: list[tuple[int, int]]) -> None:
        for row in rows:
            self.grid_rowconfigure(row[0], weight=row[1])
        for col in cols:
            self.grid_columnconfigure(col[0], weight=col[1]) 