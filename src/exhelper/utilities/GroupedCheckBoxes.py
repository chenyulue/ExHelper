import customtkinter as ctk
from ..model import ConfigModel

class GroupedCheckBoxes(ctk.CTkFrame):
    def __init__(self, master, title: str, children: list[str], external_var: ctk.Variable|None=None, indent:int=20, gap:int=5, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.setting = ConfigModel()

        self._title = title
        self._children = children
        self._flag_num = int("1"*len(self._children), base=2)
        self._external_var = external_var

        self.title_var = ctk.IntVar(value=self._flag_num)
        self.title_checkbox = ctk.CTkSwitch(
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

        # if self._external_var is not None:
        #     if value==1<<len(self._children):
        #         self.check_box_number += 1
        #     else:
        #         self.check_box_number -= 1
        #     self._external_var.set(self.check_box_number)

    def _on_child_toggled(self, idx):
        total = self.title_var.get()
        value = self.children_vars[idx].get()
        if value:
            new_total = total | (1<<idx)
        else:
            new_total = total ^ (1<<idx)
        self.title_var.set(new_total)

if __name__ == "__main__":
    root = ctk.CTk()
    GroupedCheckBoxes(root, "A", ["A1", "A2", "A3"]).grid()
    root.mainloop()
