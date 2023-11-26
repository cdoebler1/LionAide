from tkinter import ttk

from AccountHandler import AccountHandler
from ChatWindow import ChatWindow


class LoginWindow:

    def __init__(self, master, users_data, personality_data):
        # Should we have multiple entry variables or just username_entry and password_entry?
        # Entry variable for edit_User_personality method
        self.personality_entry = None
        # Entry variable for account_creation method
        self.account_entry = None
        # Entry variable for edit_user_accounts method
        self.edit_accounts_entry = None

        master.title('LionAide Application - Login Window')
        master.resizable(False, False)
        master.geometry("400x200")

        self.frame_content = ttk.Frame(master)
        self.frame_content.grid(row=0, column=0, sticky='nsew')

        # Add the labels and text boxes to the frame_content frame
        ttk.Label(self.frame_content, text='UserName:', style="White.TLabel").grid(row=1, column=1, pady=10)
        ttk.Label(self.frame_content, text='Password:', style="White.TLabel").grid(row=2, column=1, pady=5)

        # Text entry for UserName:
        self.username_entry = ttk.Entry(self.frame_content)
        self.username_entry.grid(row=1, column=2)

        # Text entry for Password:
        self.password_entry = ttk.Entry(self.frame_content, show="*")
        self.password_entry.grid(row=2, column=2)

        # Create a new frame for the buttons
        button_frame = ttk.Frame(master)
        button_frame.grid(row=1, column=0, sticky='nsew')

        # Configure the grid to distribute space evenly between rows and columns
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)

        # Add the buttons to the new frame
        # Note: Login temporarily is set to open chat_window when its pressed
        ttk.Button(button_frame, text='Login',
                   command=lambda: self.check_credentials(users_data, personality_data)).grid(row=0, column=0)

        # ttk.Button(button_frame, text='Register', command=self.account_creation).grid(row=0, column=1)

        # Configure the grid to distribute space evenly between the buttons
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        # Configure the grid to distribute space evenly between the columns of the frame_content
        self.frame_content.grid_rowconfigure(0, weight=1)
        self.frame_content.grid_rowconfigure(3, weight=1)

    def check_credentials(self, users_data, personality_data):
        # Get the entered username and password
        username = self.username_entry.get()
        password = self.password_entry.get()
        handler = AccountHandler()
        is_valid_credentials = handler.verify_password(users_data, username, password)

        if is_valid_credentials:
            self.create_chat_window(users_data, personality_data)
            print("Successful login.") # Text for testing
        else:
            print("Password is incorrect.") # Text for testing

    def create_chat_window(self, users_data, personality_data):
        ChatWindow(users_data, personality_data)
