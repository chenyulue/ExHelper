import customtkinter as ctk


class CTkTristateCheckBox(ctk.CTkCheckBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self._variable is not None and self._variable != "":
            self._variable_callback_name = self._variable.trace_add(
                "write", self._variable_callback
            )
            if self._variable.get() == self._onvalue:
                self._check_state = True
            elif self._variable.get() == self._offvalue:
                self._check_state = False
            else:
                self._check_state = None

        self._draw_tristate()
        self._creating_bindings_override()

    def _draw_tristate(self, no_color_updates=False):
        if no_color_updates is False and self._check_state is None:
            self._canvas.itemconfig(
                "inner_parts",
                outline=self._apply_appearance_mode(self._bg_color),
                fill=self._apply_appearance_mode(self._fg_color),
            )

    def _draw(self, no_color_updates=False):
        super()._draw(no_color_updates)

        self._draw_tristate(no_color_updates)

    def _variable_callback(self, var_name, index, mode):
        if not self._variable_callback_blocked:
            if self._variable.get() == self._onvalue:
                self.select(from_variable_callback=True)
            elif self._variable.get() == self._offvalue:
                self.deselect(from_variable_callback=True)
            else:
                self._check_state = None
                self._draw()

    def _on_leave(self, event=0):
        super()._on_leave(event)

        if self._check_state is None:
            self._canvas.itemconfig("inner_parts",
                                    fill=self._apply_appearance_mode(self._fg_color),
                                    outline=self._apply_appearance_mode(self._bg_color))

    def _creating_bindings_override(self, sequence: str|None = None):
        if sequence is None or sequence == "<Leave>":
            self._canvas.bind("<Leave>", self._on_leave, add=False)
            self._text_label.bind("<Leave>", self._on_leave, add=False)


if __name__ == "__main__":
    def on_clicked():
        x = var.get()
        var.set(x + 1)
        print(var.get())
    root = ctk.CTk()
    var = ctk.IntVar(value=0)
    chk = CTkTristateCheckBox(root, text="check", variable=var, offvalue=0, onvalue=3)
    chk.grid()
    btn = ctk.CTkButton(root, text="Click!", command=on_clicked)
    btn.grid()
    root.mainloop()
