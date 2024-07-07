import customtkinter as ctk


class TriStateCTkCheckBox(ctk.CTkCheckBox):
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

        self._draw()

    def _draw(self, no_color_updates=False):
        super()._draw(no_color_updates)

        if no_color_updates is False and self._check_state is None:
            self._canvas.itemconfig(
                "inner_parts",
                outline=self._apply_appearance_mode(self._bg_color),
                fill=self._apply_appearance_mode(self._hover_color),
            )

    def _variable_callback(self, var_name, index, mode):
        if not self._variable_callback_blocked:
            if self._variable.get() == self._onvalue:
                self.select(from_variable_callback=True)
            elif self._variable.get() == self._offvalue:
                self.deselect(from_variable_callback=True)
            else:
                self._check_state = None
                self._draw()


def on_clicked():
    x = var.get()
    var.set(x + 1)
    print(var.get())


if __name__ == "__main__":
    root = ctk.CTk()
    var = ctk.IntVar(value=0)
    chk = TriStateCTkCheckBox(root, text="check", variable=var, offvalue=0, onvalue=3)
    chk.grid()
    btn = ctk.CTkButton(root, text="Click!", command=on_clicked)
    btn.grid()
    root.mainloop()
