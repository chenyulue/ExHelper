import customtkinter as ctk
from .Application import Application
from . import assets

ctk.set_default_color_theme(str(assets.DEFAULT_THEME))

def main():
    Application().run()

if __name__ == '__main__':
    main()