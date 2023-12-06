from tkinter import ttk, messagebox

from AdminWindow import AdminWindow
from ChatWindow import ChatWindow
from user_manager import UserManager


class LoginWindow:

    def __init__(self, master, users_data, personality_data):

        self.users_data = users_data
        self.personality_entry = personality_data
        # Entry variable for account_creation method
        self.account_entry = None
        # Entry variable for edit_user_accounts method
        self.edit_accounts_entry = None

        master.title('LionAide Application - Login Window')
        master.resizable(False, False)
        master.geometry("460x200")
        style = ttk.Style(master)
        style.configure('White.TLabel', font='Calibri 12', foreground='white')

        # Configure the grid to distribute space evenly between rows and columns
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)

        # Create a new frame for the user login
        user_frame = ttk.Frame(master)
        user_frame.grid(row=0, column=0, padx=5, pady=5, sticky='NSEW')
        user_frame.grid_columnconfigure(0, weight=1)
        user_frame.grid_columnconfigure(1, weight=3)
        user_frame.grid_columnconfigure(2, weight=3)
        user_frame.grid_columnconfigure(3, weight=1)
        user_frame.grid_rowconfigure(0, weight=1)
        user_frame.grid_rowconfigure(1, weight=1)
        user_frame.grid_rowconfigure(2, weight=1)
        user_frame.grid_rowconfigure(3, weight=1)

        # Add the labels and text boxes to the frame_content frame
        ttk.Label(user_frame, text='UserName:',
                  style="White.TLabel").grid(row=0, column=1, padx=10, pady=10, sticky="E")
        ttk.Label(user_frame, text='Password:',
                  style="White.TLabel").grid(row=1, column=1, padx=10, pady=10, sticky="E")
        ttk.Label(user_frame, text='Personality:',
                  style="White.TLabel").grid(row=2, column=1, padx=10, pady=10, sticky="E")

        # Excludes Admin from Combobox for usernames
        usernames = [user for user in users_data.keys()]

        # Combobox entry for Username:
        self.username_entry = ttk.Combobox(user_frame, values=usernames)
        self.username_entry.grid(row=0, column=2, sticky="W")

        # Text entry for Password and 'width=22' resizes entry box to match combobox width
        self.password_entry = ttk.Entry(user_frame, width=22, show="*")
        self.password_entry.grid(row=1, column=2, sticky="W")

        # Combobox for personality choice.
        personality_names = [names for names in personality_data.keys()]
        self.personality_entry = ttk.Combobox(user_frame, values=personality_names)
        self.personality_entry.grid(row=2, column=2, sticky="W")

        # Login checks the users password and opens chat window if successful.
        ttk.Button(user_frame, text='Login',
                   command=lambda: self.check_credentials(users_data,
                                                          personality_data)).grid(row=3, column=2, sticky="E")

    def check_credentials(self, users_data, personality_data):
        # Get the entered username and password
        username = self.username_entry.get()
        password = self.password_entry.get()
        manager = UserManager()
        is_valid_credentials = manager.verify_password(username, password)

        if is_valid_credentials:
            if username == "Admin":
                self.create_admin_window(users_data, personality_data)
            else:
                personality = self.personality_entry.get()
                self.create_chat_window(username, personality, users_data, personality_data)
        else:
            messagebox.showinfo("Login Failed", f"Incorrect password.")

    @staticmethod
    def create_chat_window(username, personality, users_data, personality_data):
        ChatWindow(username, personality, users_data, personality_data)

    @staticmethod
    def create_admin_window(users_data, personality_data):
        AdminWindow(users_data, personality_data)
