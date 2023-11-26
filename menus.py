# If unsure about what library to import temporarily use wildcard '*'
from tkinter import Toplevel, Tk
from tkinter import ttk
from ttkthemes import ThemedTk
import json

from LoginWindow import LoginWindow

with open('users.json', "r") as f: users_data = json.load(f)
print(users_data)  # debug code for verifying that the array was built


class Menus:

    def __init__(self, master, users_data, personality_data):
        LoginWindow(master, users_data, personality_data)

    def admin_window(self):
        admin = Toplevel()
        admin.title("Admin Window")
        admin.geometry("400x200")

        # Configure the columns for the buttons
        admin.grid_columnconfigure(0, weight=1)

        # Configure the grid row for the buttons
        admin.grid_rowconfigure(0, weight=1)
        admin.grid_rowconfigure(1, weight=1)
        admin.grid_rowconfigure(2, weight=1)

        # Creates the buttons for the admin_window
        ttk.Button(admin, text='Edit User Accounts', command=self.edit_user_account, width=20).grid(
            row=0, column=0, sticky='s', padx=10, pady=10)
        ttk.Button(admin, text='Edit Personalities', command=self.edit_user_personality, width=20).grid(
            row=1, column=0, sticky='s', padx=10, pady=10)

        # Done button destroys the window, closing it
        ttk.Button(admin, text='Done', command=admin.destroy).grid(row=5, column=3, sticky='s')

    def edit_user_account(self):
        account = Toplevel()
        account.title("Edit User Accounts")
        account.geometry("400x250")

        # Creates the button and entry box for Admin
        ttk.Label(account, text='Admin:').grid(row=1, column=2, padx=50, pady=10)
        self.edit_accounts_entry = ttk.Entry(account)
        self.edit_accounts_entry.grid(row=1, column=3)

        # Creates the button and entry box for an Admin Password
        ttk.Label(account, text='Password:').grid(row=2, column=2, padx=10, pady=10)
        self.edit_accounts_entry = ttk.Entry(account)
        self.edit_accounts_entry.grid(row=2, column=3)

        # Buttons that Add and Delete an Admin account
        ttk.Button(account, text='Add', command=account.destroy).grid(row=3, column=2, sticky='e')
        ttk.Button(account, text='Delete', command=account.destroy).grid(row=3, column=3, sticky='e')

        # Creates the button and entry box for Password
        ttk.Label(account, text='User:').grid(row=4, column=2, padx=10, pady=10)
        self.edit_accounts_entry = ttk.Entry(account)
        self.edit_accounts_entry.grid(row=4, column=3)

        # Creates the button and entry box for a User Password
        ttk.Label(account, text='Password:').grid(row=5, column=2, padx=10, pady=10)
        self.edit_accounts_entry = ttk.Entry(account)
        self.edit_accounts_entry.grid(row=5, column=3)

        # Button 'save' saves to JSON file and Done closes the window (Save is not yet functional)
        ttk.Button(account, text='Save', command=account.destroy).grid(row=6, column=2, sticky='e')
        ttk.Button(account, text='Done', command=account.destroy).grid(row=6, column=3, sticky='e')

    def edit_user_personality(self):
        personality = Toplevel()
        personality.title("Edit User Personality")
        personality.geometry("400x200")

        # Creates label and entry box for Personality
        ttk.Label(personality, text='Enter a Personality Name:').grid(row=1, column=1, padx=10, pady=10)
        self.personality_entry = ttk.Entry(personality)
        self.personality_entry.grid(row=1, column=2)

        # Creates label and entry box for Description
        ttk.Label(personality, text='Enter a Description:').grid(row=2, column=1, padx=10, pady=10)
        self.personality_entry = ttk.Entry(personality)
        self.personality_entry.grid(row=2, column=2)

        # Creates label and entry box for Definition
        ttk.Label(personality, text='Enter a Definition:').grid(row=3, column=1, padx=10, pady=10)
        self.personality_entry = ttk.Entry(personality)
        self.personality_entry.grid(row=3, column=2)

        # Creates Save and Done buttons for edit_user_personality window
        ttk.Button(personality, text='Save', command=personality.destroy).grid(row=4, column=1, sticky='s')
        ttk.Button(personality, text='Done', command=personality.destroy).grid(row=4, column=2, sticky='s')

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
    #style.configure('White.TLabel', foreground='white', background="#7B8CD0")
    style.configure('White.TLabel', foreground='white')
    menus = Menus(root, user_manager.users_data, personality_manager.personalities_data)
    root.mainloop()


if __name__ == "__main__":
    main()
