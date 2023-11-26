from tkinter import Toplevel, Tk
from tkinter import ttk
class ChatWindow:

    def __init__(self, users_data, personality_data):

        # The follow lines set the window size, color and window title
        chat = Toplevel()
        chat.title('LionAIde Application - Chat Window')
        chat.resizable(False, False)
        chat.configure(background='#bfffff')
        chat.geometry("800x450")

        # Sets locations to buttons Options, user, personality and admin window
        ttk.Button(chat, text='Options').grid(row=0, column=0, sticky='w')
        ttk.Button(chat, text='User').grid(row=0, column=1, sticky='w')
        ttk.Button(chat, text='Personality').grid(row=0, column=2, sticky='w')
        # ttk.Button(chat, text='Admin Window', command=self.admin_window).grid(row=0, column=6, sticky='ne')
        # This button is temporarily commented out until ready to implement

        # Occupies column 3-6 to space Admin Window button to the right corner
        for i in range(3, 6):
            chat.grid_columnconfigure(i, weight=1)
