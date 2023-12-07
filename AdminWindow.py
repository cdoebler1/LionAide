import json
from tkinter import Toplevel, ttk, messagebox
from ttkthemes import ThemedTk


class AdminWindow:

    def __init__(self, users_data, personality_data):

        # self.master = master

        self.personality_data = personality_data
        self.users_data = users_data
        self.edit_accounts_entry = None
        self.edit_password_entry = None

        admin = ThemedTk()
        admin.title("Admin Window")
        admin.resizable(False, False)
        admin.geometry("400x600")
        lion_aide_theme = "blue"
        style = ttk.Style(admin)
        style.theme_use(lion_aide_theme)

        select_frame = ttk.Frame(admin)
        select_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        select_frame.grid_columnconfigure(0, weight=1)

        self.accounts_frame = ttk.Frame(admin)
        self.personalities_frame = ttk.Frame(admin)

        self.show_accounts_frame(admin)
        self.show_personalities_frame(admin)

        ttk.Button(select_frame, text='Done', command=admin.destroy).grid(row=0, column=2)

    def show_accounts_frame(self, editing_window):
        self.personalities_frame.grid_remove()
        self.accounts_frame.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        self.edit_user_account(editing_window, self.users_data)

    def show_personalities_frame(self, editing_window):
        self.accounts_frame.grid_remove()
        self.personalities_frame.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        self.edit_user_personality(editing_window)

    # Attempt to refresh combobox live (Failed)
    # def refresh_usernames(self):
    # Updates the list of usernames for combobox
    # return list(self.users_data.keys())

    # Method to add a user to JSON file. NOTE: When adding or delete you must refresh app to see new list of users
    def add_user_account(self):
        user_username = self.edit_accounts_entry.get()
        user_password = self.edit_password_entry.get()

        try:
            with open('users.json', 'r') as file:
                users_data = json.load(file)
        except FileNotFoundError:
            users_data = {}

        # Check if the username already exists
        if user_username in users_data:
            messagebox.showerror("Error", "User already exists.")
            return

        if (user_username != "") & (user_password != ""):
            users_data[user_username] = user_password

            with open('users.json', 'w') as file:
                json.dump(users_data, file, indent=2)
                messagebox.showinfo("User Added", f"User '{user_username}' added successfully.")
        else:
            messagebox.showinfo("Error", f"Fields cannot be blank.")

        # (Attempt to refresh combobox live(failed))
        # self.edit_accounts_entry['values'] = self.refresh_usernames()

    def delete_user_account(self):
        user_username = self.edit_accounts_entry.get()

        try:
            with open('users.json', 'r') as file:
                users_data = json.load(file)
        except FileNotFoundError:
            messagebox.showerror("Error", "Users file not found.")
            return

        # Check if the username exists
        if user_username not in users_data:
            messagebox.showerror("Error", "User not found.")
            return

        confirmation = messagebox.askokcancel("Confirm Deletion",
                                              f"Do you really want to delete the user '{user_username}'?")

        if confirmation:
            del users_data[user_username]

            with open('users.json', 'w') as file:
                json.dump(users_data, file, indent=2)

            messagebox.showinfo("User Deleted", f"User '{user_username}' deleted successfully.")

    def save_user_account(self):
        user_username = self.edit_accounts_entry.get()
        new_password = self.edit_password_entry.get()

        try:
            with open('users.json', 'r') as file:
                users_data = json.load(file)
        except FileNotFoundError:
            messagebox.showerror("Error", "Users file not found.")
            return

        # Check if the username exists
        if user_username not in users_data:
            messagebox.showerror("Error", "User not found.")
            return

        # Update the password
        users_data[user_username] = new_password

        with open('users.json', 'w') as file:
            json.dump(users_data, file, indent=2)

        messagebox.showinfo("Password Updated", f"Password for user '{user_username}' updated successfully.")

    def add_personality(self):
        personality_name = self.personality_name_entry.get()
        personality_description = self.personality_description_entry.get()

        try:
            with open('personalities.json', 'r') as file:
                personalities_data = json.load(file)
        except FileNotFoundError:
            personalities_data = {}

        # Check if the personality name already exists
        if personality_name in personalities_data:
            messagebox.showerror("Error", "Personality already exists.")
            return

        if (personality_name != "") & (personality_description != ""):
            personalities_data[personality_name] = personality_description

            with open('personalities.json', 'w') as file:
                json.dump(personalities_data, file, indent=2)

            messagebox.showinfo("Personality Added", f"Personality '{personality_name}' added successfully.")
        else:
            messagebox.showinfo("Error", f"Fields cannot be blank.")

    def delete_personality(self):
        personality_name = self.personality_name_entry.get()

        try:
            with open('personalities.json', 'r') as file:
                personalities_data = json.load(file)
        except FileNotFoundError:
            messagebox.showerror("Error", "Personalities file not found.")
            return

        # Check if the personality name exists
        if personality_name not in personalities_data:
            messagebox.showerror("Error", "Personality not found.")
            return

        confirmation = messagebox.askokcancel("Confirm Deletion",
                                              f"Do you really want to delete the personality '{personality_name}'?")

        if confirmation:
            del personalities_data[personality_name]

            with open('personalities.json', 'w') as file:
                json.dump(personalities_data, file, indent=2)

            messagebox.showinfo("Personality Deleted", f"Personality '{personality_name}' deleted successfully.")

    def save_personality(self):
        personality_name = self.personality_name_entry.get()
        personality_description = self.personality_description_entry.get()

        try:
            with open('personalities.json', 'r') as file:
                personalities_data = json.load(file)
        except FileNotFoundError:
            personalities_data = {}

        # Check if the personality name exists
        if personality_name not in personalities_data:
            messagebox.showerror("Error", "Personality not found.")
            return

        # Update personality information
        personalities_data[personality_name] = personality_description

        with open('personalities.json', 'w') as file:
            json.dump(personalities_data, file, indent=2)

        messagebox.showinfo("Personality Updated", f"Personality '{personality_name}' updated successfully.")

    def edit_user_account(self, editing_window, users_data):

        self.users_data = users_data

        # Extract usernames from users_data dictionary
        usernames = list(users_data.keys())

        admin = ttk.Frame(editing_window)
        admin.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

        # ttk.Label(admin, text='Admin:').grid(row=1, column=2, padx=50, pady=10)
        # self.edit_accounts_entry = ttk.Entry(admin)
        # self.edit_accounts_entry.grid(row=1, column=3)

        # ttk.Label(admin, text='Password:').grid(row=2, column=2, padx=10, pady=10)
        # self.edit_password_entry = ttk.Entry(admin)
        # self.edit_password_entry.grid(row=2, column=3)

        # Buttons that Add and Delete an account. Done closes the window.
        ttk.Button(admin, text='Add Account', command=self.add_user_account).grid(row=3, column=2, sticky='e')
        ttk.Button(admin, text='Delete Account', command=self.delete_user_account).grid(row=3, column=3, sticky='e')
        ttk.Button(admin, text='Save', command=self.save_user_account).grid(row=6, column=6, sticky='e')

        # Label for UserNames:
        ttk.Label(admin, text='User:').grid(row=4, column=2, padx=10, pady=10)

        # Combobox entry for Usernames:
        self.edit_accounts_entry = ttk.Combobox(admin, values=usernames)
        self.edit_accounts_entry.grid(row=4, column=3)

        # Label for Password
        ttk.Label(admin, text='Password:').grid(row=5, column=2, padx=10, pady=10)

        # Entry box for Password
        self.edit_password_entry = ttk.Entry(admin, width=22)
        self.edit_password_entry.grid(row=5, column=3)

    def edit_user_personality(self, editing_window):
        # Create a new frame for personality editing
        personality = ttk.Frame(editing_window)
        personality.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')

        # Get the list of existing personality names
        personalities = list(self.personality_data.keys())

        # Label and Combobox for selecting a Personality Name
        ttk.Label(personality, text='Enter a Personality Name:').grid(row=1, column=1, padx=10, pady=10)
        self.personality_name_entry = ttk.Combobox(personality, values=personalities)
        self.personality_name_entry.grid(row=1, column=2)

        # Label and Entry for entering a Personality Description
        ttk.Label(personality, text='Enter a Description:').grid(row=2, column=1, padx=10, pady=10)
        self.personality_description_entry = ttk.Entry(personality)
        self.personality_description_entry.grid(row=2, column=2)

        # Buttons for adding, deleting, and saving a Personality when you want to change the description
        ttk.Button(personality, text='Add Personality', command=self.add_personality).grid(row=3, column=1, sticky='e')
        ttk.Button(personality, text='Delete Personality', command=self.delete_personality).grid(row=3, column=2,
                                                                                                 sticky='e')
        ttk.Button(personality, text='Save', command=self.save_personality).grid(row=4, column=1, sticky='s')
