# If unsure about what library to import temporarily use wildcard '*'
from tkinter import Toplevel, Tk
from tkinter import ttk
from ttkthemes import ThemedTk
import json

import personality_manager
import user_manager
from LoginWindow import LoginWindow

with open('users.json', "r") as f: users_data = json.load(f)
print(users_data)  # debug code for verifying that the array was built


class Menus:

    def __init__(self, master, users_data, personality_data):
        LoginWindow(master, users_data, personality_data)


    def account_creation(self):
        creation = Toplevel()
        creation.title("Create Account")
        creation.geometry("400x200")

        # Creates label and entry box for Username
        ttk.Label(creation, text='Enter a Username:').grid(row=1, column=1, padx=10, pady=10)
        self.account_entry = ttk.Entry(creation)
        self.account_entry.grid(row=1, column=2)

        # Creates label and entry box for Password
        ttk.Label(creation, text='Enter Password:').grid(row=3, column=1, padx=10, pady=10)
        self.account_entry = ttk.Entry(creation)
        self.account_entry.grid(row=3, column=2)

        # Creates the two buttons Submit and Done. NOTE: Submit is temporarily set to close the window.
        ttk.Button(creation, text='Submit', command=creation.destroy).grid(row=2, column=2, sticky='s')
        ttk.Button(creation, text='Done', command=creation.destroy).grid(row=4, column=2, sticky='s')


def main():
    root = ThemedTk()
    LionAIdeTheme = "blue"
    style = ttk.Style(root)
    style.theme_use(LionAIdeTheme)
    # style.configure('White.TLabel', foreground='white', background="#7B8CD0")
    style.configure('White.TLabel', foreground='white')
    menus = Menus(root, user_manager.users_data, personality_manager.personalities_data)
    root.mainloop()


if __name__ == "__main__":
    main()
