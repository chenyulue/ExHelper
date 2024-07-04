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

        self.text_left = ctk.CTkTextbox(
            self, height=400, 
            spacing2=self.setting.text_spacing2,
            spacing3=self.setting.text_spacing3,
            font=self.setting.font_text,
        )
        self.text_left.grid(row=1, column=0, sticky="nsew", padx=(5, 0))

        self.button_middle = self._create_buttons(["比较", "清空"])
        self.button_middle.grid(row=1, column=1, sticky="ns")

        self.text_right = ctk.CTkTextbox(
            self, height=400, 
            spacing2=self.setting.text_spacing2,
            spacing3=self.setting.text_spacing3,
            font=self.setting.font_text,
        )
        self.text_right.grid(row=1, column=2, sticky="nsew", padx=(0, 5))

        self.label_result = ctk.CTkLabel(self, text="修改对照：")
        self.label_result.grid(row=2, column=0, columnspan=3, sticky="w", padx=5, pady=(8, 2))

        self.text_bottom = ctk.CTkTextbox(
            self, height=200, 
            spacing2=self.setting.text_spacing2,
            spacing3=self.setting.text_spacing3,
            font=self.setting.font_text)
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
            frame, justify="left",
            text=f"{text}文本：\n请输入或Ctrl+V粘贴或点击[导入{text}]按钮导入文本",
        )
        label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        btn = ctk.CTkButton(frame, text=f"导入{text}", width=100,)
        btn.grid(row=0, column=1, sticky="e", padx=5, pady=5)

        return frame

    def _create_buttons(self, labels: list[str]) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(self)
        frame.grid_rowconfigure((1,2), weight=0)
        frame.grid_rowconfigure((0,3), weight=1)

        for i, label in enumerate(labels):
            btn = ctk.CTkButton(
                frame, text=label, width=50,
                command=self.callbacks[label],
            )
            btn.grid(row=i+1, sticky="we", column=0, padx=5, pady=5)

        return frame


if __name__ == "__main__":
    app = ctk.CTk()
    main_window = ComparisonFrame(app)
    main_window.grid(stick="nsew")
    app.mainloop()