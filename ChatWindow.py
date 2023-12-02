from ttkthemes import ThemedTk
from tkinter import ttk
class ChatWindow:

    def __init__(self, username, personality, users_data, personality_data):

        # The follow lines set the window size, color and window title
        chat = ThemedTk()
        style = ttk.Style(chat)
        style.theme_use("blue")
        style.configure('White.TLabel', font='Calibri 12', foreground='white')

        chat.title('LionAIde Application - Chat Window')
        chat.resizable(False, False)
        chat.configure(background='#bfffff')
        chat.geometry("800x450")
        chat.grid_rowconfigure(0, weight=1)
        chat.grid_columnconfigure(0, weight=1)

        chat_options_frame = ttk.Frame(chat)
        chat_options_frame.grid(row=0, column=0, padx=5, pady=5, sticky='NSEW')
        chat_options_frame.grid_columnconfigure(0, weight=1)
        chat_options_frame.grid_columnconfigure(1, weight=1)
        chat_options_frame.grid_columnconfigure(2, weight=2)
        chat_options_frame.grid_rowconfigure(0, weight=1)
        chat_options_frame.grid_rowconfigure(1, weight=1)
        chat_options_frame.grid_rowconfigure(2, weight=10)

        personality_description = personality_data.get(personality)

        # Sets locations to buttons Options, user, personality and admin window
        ttk.Label(chat_options_frame, text="User: "+ username, style="White.TLabel").grid(row=0, column=0, sticky="N")
        ttk.Button(chat_options_frame, text='Change Password').grid(row=0, column=0)
        ttk.Label(chat_options_frame, text='Personality: '+ personality, style="White.TLabel").grid(row=0, rowspan=2, column=1, sticky="N")
        ttk.Label(chat_options_frame, text=personality_description, style="White.TLabel", wraplength=400).grid(row=0, rowspan=2, column=2, sticky="N")


        # ttk.Button(chat, text='Admin Window', command=self.admin_window).grid(row=0, column=6, sticky='ne')
        # This button is temporarily commented out until ready to implement
