from tkinter import *
from tkinter import ttk

class Menus:

    def __init__(self, master):
        master.title('LionAide Application - Login Window')
        master.resizable(False, False)
        master.geometry("400x200")

        self.frame_content = ttk.Frame(master)
        self.frame_content.grid(row=0, column=0, sticky='nsew')

        # Add the labels and text boxes to the frame_content frame
        ttk.Label(self.frame_content, text='UserName:').grid(row=1, column=1, padx=5)
        ttk.Label(self.frame_content, text='Password:').grid(row=2, column=1, padx=5)

        # Text entry for UserName:
        self.username_entry = ttk.Entry(self.frame_content)
        self.username_entry.grid(row=1, column=2, padx=5)

        # Text entry for Password:
        self.password_entry = ttk.Entry(self.frame_content, show="*")
        self.password_entry.grid(row=2, column=2, padx=5)

        # Create a new frame for the buttons
        button_frame = ttk.Frame(master)
        button_frame.grid(row=1, column=0, sticky='nsew')

        # Configure the grid to distribute space evenly between rows and columns
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)

        # Add the buttons to the new frame
        # Note: Login temporarily is set to open chat_window when its pressed
        ttk.Button(button_frame, text='Login', command=self.chat_window).grid(row=0, column=0)
        ttk.Button(button_frame, text='Register').grid(row=0, column=1)

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

        # Sets locations to buttons Options, user, personality and admin window
        ttk.Button(chat, text='Options').grid(row=0, column=0, sticky='w')
        ttk.Button(chat, text='User').grid(row=0, column=1, sticky='w')
        ttk.Button(chat, text='Personality').grid(row=0, column=2, sticky='w')
        ttk.Button(chat, text='Admin Window', command=self.admin_window).grid(row=0,
                                                        column=6, sticky='ne')

        ## Occupies column 3-6 to space Admin Window button to the right corner
        for i in range(3, 6):
            chat.grid_columnconfigure(i, weight=1)

    def admin_window(self):

        admin = Toplevel()
        admin.title("Admin Window")
        admin.geometry("600x350")


def main():
    root = Tk()
    menus = Menus(root)
    root.mainloop()


if __name__ == "__main__": main()
