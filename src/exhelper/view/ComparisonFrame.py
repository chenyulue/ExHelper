import customtkinter as ctk

from ..model import ConfigModel
from ..controller import ComparisonController


class ComparisonFrame(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.setting = ConfigModel()
        self.controller = None
        self.callbacks = {
            "清空": self.clear_texts,
            "比较": self.compare_texts,
        }

        self._configure_grid([(0, 0), (1, 2), (2, 0), (3, 1)], [(0, 1), (1, 0), (2, 1)])

        self.label_left = self._create_comparison_label("修改")
        self.label_left.grid(row=0, column=0, sticky="ew")
        self.label_right = self._create_comparison_label("原始")
        self.label_right.grid(row=0, column=2, sticky="ew")

        self.text_left = ctk.CTkTextbox(self, height=400, font=self.setting.text_font)
        self.text_left.grid(row=1, column=0, sticky="nsew", padx=(5, 0))

        self.button_middle = self._create_buttons(["比较", "清空"])
        self.button_middle.grid(row=1, column=1, sticky="ns")

        self.text_right = ctk.CTkTextbox(self, height=400, font=self.setting.text_font)
        self.text_right.grid(row=1, column=2, sticky="nsew", padx=(0, 5))

        self.label_result = ctk.CTkLabel(
            self, text="修改对照：", font=self.setting.font,
            text_color=(self.setting.label_light, self.setting.label_dark),
        )
        self.label_result.grid(row=2, column=0, columnspan=3, sticky="w", padx=5, pady=(8, 2))

        self.text_bottom = ctk.CTkTextbox(self, height=200, font=self.setting.text_font)
        self.text_bottom.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=5, pady=(0, 5))

    def set_controller(self, controller: ComparisonController):
        self.controller = controller

    def clear_texts(self):
        if self.controller is not None:
            self.controller.clear_texts()

    def compare_texts(self):
        if self.controller is not None:
            self.controller.compare_texts()

    def _configure_grid(
        self, rows: list[tuple[int, int]], cols: list[tuple[int, int]]
    ) -> None:
        for row in rows:
            self.grid_rowconfigure(row[0], weight=row[1])
        for col in cols:
            self.grid_columnconfigure(col[0], weight=col[1])

    def _create_comparison_label(self, text: str) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(self)
        frame.grid_columnconfigure((0, 1), weight=1)

        label = ctk.CTkLabel(
            frame,
            text=f"{text}文本：\n请输入或Ctrl+V粘贴或点击[导入{text}]按钮导入文本",
            font=self.setting.font,
            justify="left",
            text_color=(self.setting.label_light, self.setting.label_dark),
        )
        label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        btn = ctk.CTkButton(
            frame, text=f"导入{text}", width=100,
            font=self.setting.font,
            text_color=(self.setting.light_fg, self.setting.dark_fg),
            fg_color=(self.setting.light_bg, self.setting.dark_bg),
            hover_color=self.setting.hover_color,
        )
        btn.grid(row=0, column=1, sticky="e", padx=5, pady=5)

        return frame

    def _create_buttons(self, labels: list[str]) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(self)
        frame.grid_rowconfigure((1,2), weight=0)
        frame.grid_rowconfigure((0,3), weight=1)

        for i, label in enumerate(labels):
            btn = ctk.CTkButton(
                frame, text=label, width=50,
                font=self.setting.font,
                text_color=(self.setting.light_fg, self.setting.dark_fg),
                fg_color=(self.setting.light_bg, self.setting.dark_bg),
                hover_color=self.setting.hover_color,
                command=self.callbacks[label],
            )
            btn.grid(row=i+1, sticky="we", column=0, padx=5, pady=5)

        return frame


if __name__ == "__main__":
    app = ctk.CTk()
    # app.grid_rowconfigure(0, weight=1)
    # app.grid_columnconfigure(0, weight=1)
    main_window = ComparisonFrame(app)
    main_window.grid(stick="nsew")
    app.mainloop()