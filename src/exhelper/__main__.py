import customtkinter as ctk
from exhelper.Application import Application
from exhelper import assets

ctk.set_default_color_theme(str(assets.DEFAULT_THEME))

def main():
    Application().run()

if __name__ == '__main__':
    main()