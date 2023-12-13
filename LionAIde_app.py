# LionAIde_app.py
from ttkthemes import ThemedTk
from tkinter import ttk
from user_manager import UserManager
from personality_manager import PersonalityManager
from LoginWindow import LoginWindow


def main():
    root = ThemedTk()
    style = ttk.Style(root)
    style.theme_use("blue")

    user_manager = UserManager()
    personality_manager = PersonalityManager()
    logon = LoginWindow(root, user_manager.users_data, personality_manager.personalities_data)

    root.mainloop()

if __name__ == "__main__":
    main()
