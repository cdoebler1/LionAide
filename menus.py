# If unsure about what library to import temporarily use wildcard '*'
from tkinter import Toplevel, ttk
from ttkthemes import ThemedTk
from user_manager import UserManager


class Menus:

    def __init__(self, master, users_data, personality_data):
        self.users_data = users_data
        # Should we have multiple entry variables or just username_entry and password_entry?
        # Entry variable for edit_User_personality method
        self.personality_entry = personality_data
        # Entry variable for account_creation method
        self.account_entry = None
        # Entry variable for edit_user_accounts method
        self.edit_accounts_entry = None

        master.title('LionAide Application - Login Window')
        master.resizable(False, False)
        master.geometry("400x200")

        self.frame_content = ttk.Frame(master)
        self.frame_content.grid(row=0, column=0, sticky='nesw')

        # Add the labels and text boxes to the frame_content frame
        ttk.Label(self.frame_content, text='UserName:', style="White.TLabel").grid(row=1, column=1, pady=10, padx=10)
        ttk.Label(self.frame_content, text='Password:', style="White.TLabel").grid(row=2, column=1, pady=5, padx=10)
        ttk.Label(self.frame_content, text='Personality:', style="White.TLabel").grid(row=3, column=1, pady=5, padx=10)

        # Excludes Admin from Combobox for usernames
        usernames = [user for user in users_data.keys() if user != 'Admin']

        # Combobox entry for Username:
        self.username_entry = ttk.Combobox(self.frame_content, values=usernames)
        self.username_entry.grid(row=1, column=2)

        # Text entry for Password and 'width=22' resizes entry box to match combobox width
        self.password_entry = ttk.Entry(self.frame_content, width=22, show="*")
        self.password_entry.grid(row=2, column=2)

        # Combobox for personality choice. JSON not yet created for personalities, Temporarily set to usernames to test.
        personalityNames = [names for names in personality_data.keys()]
        self.personality_entry = ttk.Combobox(self.frame_content, values=personalityNames)
        self.personality_entry.grid(row=3, column=2)

        # Create a new frame for the buttons Login and Register
        button_frame = ttk.Frame(master)
        button_frame.grid(row=1, column=0, sticky='nsew')

        # Configure the grid to distribute space evenly between rows and columns
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)

        # Creates a new frame for the Admin Window Button
        admin_button_frame = ttk.Frame(master)
        admin_button_frame.grid(row=0, column=0, sticky='ne')

        # Add the buttons to the new frame
        # Note: Login temporarily is set to open chat_window when its pressed
        ttk.Button(button_frame, text='Login', command=self.chat_window).grid(row=4, column=0)
        #ttk.Button(button_frame, text='Register', command=self.account_creation).grid(row=4, column=1)
        ttk.Button(admin_button_frame, text='Admin Window', command=self.admin_window).grid(row=0, column=0)

        # Configure the grid to distribute space evenly between the buttons
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        # Configure the grid to distribute space evenly between the columns of the frame_content
        self.frame_content.grid_rowconfigure(0, weight=1)
        self.frame_content.grid_rowconfigure(3, weight=1)

    def chat_window(self):
        # The follow lines set the window size, color and window title
        chat = Toplevel()
        chat.title('LionAIde Application - Chat Window')
        chat.resizable(False, False)
        chat.configure(background='#bfffff')
        chat.geometry("800x450")

        # Sets End Session button to chat_window and creates variable end_session_button for .pack
        end_session_button = ttk.Button(chat, text='End Session', command=chat.destroy)

        # NOTE: Consider using .pack instead of .grid since this seems cleaner to work with.
        # Utilizes .pack instead of .grid to test other methods of organization
        end_session_button.pack(side='bottom', anchor='e', padx=5, pady=5)

    def admin_window(self):
        admin = Toplevel()
        admin.title("Admin Window")
        admin.resizable(False, False)
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
        account.resizable(False, False)
        account.geometry("400x250")

        # Creates the button and entry box for Admin
        ttk.Label(account, text='Admin:').grid(row=1, column=2, padx=50, pady=10)
        self.edit_accounts_entry_admin = ttk.Entry(account)
        self.edit_accounts_entry_admin.grid(row=1, column=3)
