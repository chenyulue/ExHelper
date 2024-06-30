import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.check_var = customtkinter.StringVar(value=3)
        checkbox = customtkinter.CTkCheckBox(self, text="CTkCheckBox", command=self.checkbox_event,
                                            variable=self.check_var, onvalue=1, offvalue=0)
        checkbox.grid()

    def checkbox_event(self):
        print("checkbox toggled, current value:", self.check_var.get())




if __name__ == "__main__":
    app = App()
    app.mainloop()