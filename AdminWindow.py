from tkinter import Toplevel
from tkinter import ttk
from ttkthemes import ThemedTk
import json


class AdminWindow:

    def __init__(self, users_data, personality_data):
        self.personality_entry = None
        self.edit_accounts_entry = None
        admin = ThemedTk()
        admin.title("Admin Window")
        admin.resizable(False, False)
        admin.geometry("400x600")
        lion_aide_theme = "blue"
        style = ttk.Style(admin)
        style.theme_use(lion_aide_theme)

        select_frame = ttk.Frame(admin)
        select_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        # Configure the columns for the buttons
        select_frame.grid_columnconfigure(0, weight=1)

        # Configure the grid row for the buttons
        # admin.grid_rowconfigure(0, weight=1)
        # admin.grid_rowconfigure(1, weight=1)
        # admin.grid_rowconfigure(2, weight=1)

        # Creates the buttons for the admin_window
        ttk.Button(select_frame, text='Edit User Accounts', command=self.edit_user_account(admin)).grid(
            row=0, column=0, padx=10, pady=10)
        ttk.Button(select_frame, text='Edit Personalities', command=self.edit_user_personality).grid(
            row=0, column=1, padx=10, pady=10)

        # Done button destroys the window, closing it
        ttk.Button(select_frame, text='Done', command=admin.destroy).grid(row=0, column=2)

    def edit_user_account(self, editing_window):
        # account = Toplevel()
        # account.title("Edit User Accounts")
        # account.geometry("400x250")
        admin = ttk.Frame(editing_window)
        admin.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

        # Creates the button and entry box for Admin
        ttk.Label(admin, text='Admin:').grid(row=1, column=2, padx=50, pady=10)
        self.edit_accounts_entry = ttk.Entry(admin)
        self.edit_accounts_entry.grid(row=1, column=3)

        # Creates the button and entry box for an Admin Password
        ttk.Label(admin, text='Password:').grid(row=2, column=2, padx=10, pady=10)
        self.edit_accounts_entry = ttk.Entry(admin)
        self.edit_accounts_entry.grid(row=2, column=3)

        # Buttons that Add and Delete an Admin account
        ttk.Button(admin, text='Add', command=admin.destroy).grid(row=3, column=2, sticky='e')
        ttk.Button(admin, text='Delete', command=admin.destroy).grid(row=3, column=3, sticky='e')

        # Creates the button and entry box for Password
        ttk.Label(admin, text='User:').grid(row=4, column=2, padx=10, pady=10)
        self.edit_accounts_entry = ttk.Entry(admin)
        self.edit_accounts_entry.grid(row=4, column=3)

        # Creates the button and entry box for a User Password
        ttk.Label(admin, text='Password:').grid(row=5, column=2, padx=10, pady=10)
        self.edit_accounts_entry = ttk.Entry(admin)
        self.edit_accounts_entry.grid(row=5, column=3)

        # Button 'save' saves to JSON file and Done closes the window (Save is not yet functional)
        ttk.Button(admin, text='Save', command=admin.destroy).grid(row=6, column=2, sticky='e')
        ttk.Button(admin, text='Done', command=admin.destroy).grid(row=6, column=3, sticky='e')

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
