# If unsure about what library to import temporarily use wildcard '*'
from tkinter import Toplevel
from tkinter import ttk
from ttkthemes import ThemedTk
import json

# Opens the users.JSON file and reads them into an array users_data
with open('users.json', "r") as f:
    users_data = json.load(f)

print(users_data)  # debug code for verifying that the array was built


class Menus:

    def __init__(self, master):
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
        self.personality_entry = ttk.Combobox(self.frame_content, values=usernames)
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
        ttk.Button(button_frame, text='Register', command=self.account_creation).grid(row=4, column=1)
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
        personality.resizable(False, False)
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
        creation.resizable(False, False)
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
    menus = Menus(root)
    root.mainloop()


if __name__ == "__main__":
    main()
