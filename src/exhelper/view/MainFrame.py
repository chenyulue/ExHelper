from pathlib import Path

import customtkinter as ctk
from PIL import Image

from .. import assets
from ..model import ConfigModel
from .ComparisonFrame import ComparisonFrame
from .CheckDefectFrame import CheckDefectFrame

class MainFrame(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.master = master
        self.setting = ConfigModel()

        self._configure_grid([(0, 1)], [(0, 0), (1, 1)])

        self.sidebar = ctk.CTkFrame(
            self, fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"],
        )
        self.body = ctk.CTkFrame(self)
        self.sidebar.grid(row=0, column=0, sticky="nsew",)
        self.body.grid(row=0, column=1, stick="nsew",)

        self.sidebar.grid_rowconfigure(4, weight=1)
        self.btn_examine = self._create_button(
            "缺陷检查", assets.EXAMINATION_ICON,
            command=self._toggle_examine,
        )
        self.btn_examine.grid(pady=15)

        self.btn_comparion = self._create_button(
            "文本比较", assets.COMPARISON_ICON,
            command=self._toggle_comparison,
        )
        self.btn_comparion.grid(pady=15)

        self.btn_deadline = self._create_button("周期管理", assets.DEADLINE_ICON)
        self.btn_deadline.grid(pady=15)

        self.btn_archive = self._create_button("结案数据", assets.ARCHIVE_ICON)
        self.btn_archive.grid(pady=15)

        self.btn_login = self._create_button(
            "登录", assets.LOGIN_ICON, icon_size=30, button_width=50)
        self.btn_login.grid(pady=10, sticky="s")

        self.btn_setting = self._create_button(
            "设置", assets.SETTING_ICON, icon_size=30, button_width=50
        )
        self.btn_setting.grid(pady=10, sticky="s")

        self.btn_about = self._create_button(
            "关于", assets.ABOUT_ICON, icon_size=30, button_width=50
        )
        self.btn_about.grid(pady=10, sticky="s")

        self.body.grid_rowconfigure(0, weight=1)
        self.body.grid_columnconfigure(0, weight=1)
        self.examine_frame = CheckDefectFrame(self.body)
        self.comparison_frame = ComparisonFrame(self.body)
        self._toggle_examine()

    def _toggle_examine(self):
        children = self.body.grid_slaves()
        if not children:
            self.examine_frame.grid(sticky="nsew")
        elif children[0] is not self.examine_frame:
            children[0].grid_remove()
            self.examine_frame.grid(sticky="nsew")
            
        self.examine_frame.tabview_check.tab("摘要").grid_slaves()[0].focus_set()

        self.sidebar.grid_slaves(row=0)[0].configure(
            fg_color=ctk.ThemeManager.theme["CTkButton"]["hover_color"]) # type: ignore
        for row in [1,2,3]:
            self.sidebar.grid_slaves(row=row)[0].configure(fg_color="transparent") # type: ignore

    def _toggle_comparison(self):
        children = self.body.grid_slaves()
        if not children:
            self.comparison_frame.grid(sticky="nsew")
        elif children[0] is not self.comparison_frame:
            children[0].grid_remove()
            self.comparison_frame.grid(sticky="nsew")

        self.comparison_frame.text_left.focus_set()

        self.sidebar.grid_slaves(row=1)[0].configure(
            fg_color=ctk.ThemeManager.theme["CTkButton"]["hover_color"]) # type: ignore
        for row in [0,2,3]:
            self.sidebar.grid_slaves(row=row)[0].configure(fg_color="transparent") # type: ignore

    def _create_button(self, label: str, image: Path, 
                       icon_size:int=50, button_width:int=100, **kwargs) -> ctk.CTkButton:
        img = ctk.CTkImage(
            light_image=Image.open(image),
            size=(icon_size, icon_size),
        )
        btn = ctk.CTkButton(
            self.sidebar, width=button_width,
            text=label, image=img, compound="top",
            fg_color="transparent", 
            **kwargs,
        )
        return btn

    def _configure_grid(self, rows: list[tuple[int, int]], cols: list[tuple[int, int]]) -> None:
        for row in rows:
            self.grid_rowconfigure(row[0], weight=row[1])
        for col in cols:
            self.grid_columnconfigure(col[0], weight=col[1])    

if __name__ == "__main__":
    app = ctk.CTk()
    app.title("审查助手 - ExHelper")
    app.geometry("1200x800")
    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(0, weight=1)
    main_window = MainFrame(app)
    main_window.grid(stick="nsew")
    app.mainloop()