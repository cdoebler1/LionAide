# LionAIde_app.py
from ttkthemes import ThemedTk
from tkinter import ttk
from menus import Menus
from user_manager import UserManager
from personality_manager import PersonalityManager


def main():
    root = ThemedTk()
    lionAideTheme = "blue"
    style = ttk.Style(root)
    style.theme_use(lionAideTheme)

    user_manager = UserManager()
    personality_manager = PersonalityManager()
    menus = Menus(root, user_manager.users_data, personality_manager.personalities_data)

    root.mainloop()


if __name__ == "__main__":
    main()
