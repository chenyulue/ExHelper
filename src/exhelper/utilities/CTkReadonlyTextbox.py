from typing import Callable
from contextlib import contextmanager
import customtkinter as ctk

def extend(cls: object) -> Callable:
    def update(extension: object) -> object:
        for k, v in extension.__dict__.items():
            if not (k.startswith("__") and k.endswith("__")):
                setattr(cls, k, v)
        return cls
    return update

@extend(ctk.CTkTextbox)
class CTkReadonlyTextbox:
    @contextmanager
    def readonly(self):
        self.configure(state="normal") # type: ignore
        try:
            yield None
        finally:
            self.configure(state="disabled") # type: ignore

if __name__ == "__main__":
    root = ctk.CTk()
    text = ctk.CTkTextbox(root)
    text.bind("<1>", lambda event: text.focus_set)
    text.grid()
    with text.readonly(): # type: ignore
        text.insert("end", "hello")
    root.mainloop()