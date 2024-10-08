import customtkinter as ctk
from ..model import ConfigModel
from .CTkTristateCheckBox import CTkTristateCheckBox

class CTkLinkedCheckBoxes(ctk.CTkFrame):
    def __init__(self, master, title: str, children: list[str], setting: ConfigModel, external_var: ctk.Variable|None=None, indent:int=20, gap:int=5, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.setting = setting

        self._title = title
        self._children = children
        self._flag_num = int("1"*len(self._children), base=2)
        self._external_var = external_var

        self.title_var = ctk.IntVar(value=self._flag_num)
        self.title_checkbox = CTkTristateCheckBox(
            self,
            text=self._title, font=self.setting.font_bold,
            variable=self.title_var,
            offvalue=0, onvalue=self._flag_num,
            command=self._on_title_toggled,
        )
        self.title_checkbox.grid(pady=(0, gap), sticky="w")

        self.children_checkboxes = []
        self.children_vars = []
        for i, child in enumerate(self._children):
            child_var = ctk.IntVar(value=1<<i)
            child_checkbox = ctk.CTkCheckBox(
                self,
                text=child, variable=child_var,
                offvalue=0, onvalue=1<<i,
                command=lambda idx=i: self._on_child_toggled(idx)
            )
            child_checkbox.grid(padx=(indent, 0), pady=(0, gap), sticky="w")
            self.children_checkboxes.append(child_checkbox)
            self.children_vars.append(child_var)

    def _on_title_toggled(self):
        value = self.title_var.get()
        for i in range(len(self._children)):
            cur = (value >> i) & 1
            if cur:
                self.children_vars[i].set(1<<i)
            else:
                self.children_vars[i].set(0)

        if self._external_var is not None:
            total = self._external_var.get()
            if self.title_var.get() == 0:
                self._external_var.set(value=total-len(self._children))
            else:
                self._external_var.set(value=total+len(self._children))

    def _on_child_toggled(self, idx):
        total = self.title_var.get()
        new_total = total ^ (1<<idx)
        self.title_var.set(new_total)

        if self._external_var is not None:
            total = self._external_var.get()
            if self.children_vars[idx].get() == 0:
                self._external_var.set(total-1)
            else:
                self._external_var.set(total+1)

    def get_checked_children_items(self) -> list[str]:
        return [chk_box.cget("text") 
                for chk_box in self.children_checkboxes 
                if chk_box.get() != 0]

if __name__ == "__main__":
    root = ctk.CTk()
    CTkLinkedCheckBoxes(root, "A", ["A1", "A2", "A3"], ConfigModel()).grid()
    root.mainloop()
