from tkinter import ttk

from ttkthemes import ThemedTk
from user_manager import UserManager


class PasswordWindow:
    def __init__(self, users_data, username):

        # Fields to change password
        self.password2 = None
        self.password1 = None

        self.users_data = users_data
        self.username = username

        pass_window = ThemedTk()
        style = ttk.Style(pass_window)
        style.theme_use("blue")
        style.configure('White.TLabel', font='Calibri 12', foreground='white')

        pass_window.title('LionAIde Application - Change Password')
        pass_window.resizable(False, False)
        pass_window.configure(background='#bfffff')
        pass_window.geometry("500x150")
        pass_window.grid_rowconfigure(0, weight=1)
        pass_window.grid_columnconfigure(0, weight=1)

        pass_entry_frame = ttk.Frame(pass_window)
        pass_entry_frame.grid(row=0, column=0, padx=5, pady=5, sticky='NSEW')

        ttk.Label(pass_entry_frame, text='New Password:',
                  style="White.TLabel").grid(row=1, column=1, padx=10, pady=10, sticky="E")
        ttk.Label(pass_entry_frame, text='Confirm Password:',
                  style="White.TLabel").grid(row=2, column=1, padx=10, pady=10, sticky="E")

        self.password_entry1 = ttk.Entry(pass_entry_frame, width=22, show="*")
        self.password_entry1.grid(row=1, column=2, sticky="W")

        self.password_entry2 = ttk.Entry(pass_entry_frame, width=22, show="*")
        self.password_entry2.grid(row=2, column=2, sticky="W")

        ttk.Button(pass_entry_frame, text='Save',
                   command=lambda: self.save_new_password()).grid(row=3, column=2, sticky="E")

    # Method that saves new password
    def save_new_password(self):
        self.password1 = self.password_entry1.get()
        self.password2 = self.password_entry2.get()

        if self.password1 == self.password2:
            manager = UserManager()
            manager.write_password(self.username, self.password1)
            print("Password updated successfully.")
        else:
            print("Passwords do not match.")
