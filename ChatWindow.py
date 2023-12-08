# ChatWindow.py
from ttkthemes import ThemedTk
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext, END
import openai
from PasswordWindow import PasswordWindow


def create_password_window(users_data, username):
    PasswordWindow(users_data, username)


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
        chat.grid_rowconfigure(1, weight=2)
        chat.grid_rowconfigure(2, weight=2)
        chat.grid_columnconfigure(0, weight=1)

        chat_options_frame = ttk.Frame(chat)
        chat_options_frame.grid(row=0, column=0, padx=5, pady=5, sticky='NSEW')
        chat_options_frame.grid_columnconfigure(0, weight=1)
        chat_options_frame.grid_columnconfigure(1, weight=1)
        chat_options_frame.grid_columnconfigure(2, weight=2)
        chat_options_frame.grid_rowconfigure(0, weight=1)
        chat_options_frame.grid_rowconfigure(1, weight=1)
        chat_options_frame.grid_rowconfigure(2, weight=1)

        personality_description = personality_data.get(personality)

        # Sets locations to buttons Options, user, personality and admin window
        ttk.Label(chat_options_frame, text="User: " + username, style="White.TLabel").grid(row=0, column=0, sticky="N")
        ttk.Button(chat_options_frame, text='Change Password',
                   command=lambda: create_password_window(users_data, username)).grid(row=1, column=0)
        ttk.Label(chat_options_frame, text='Personality: ' + personality,
                  style="White.TLabel").grid(row=0, rowspan=2, column=1, sticky="N")
        ttk.Label(chat_options_frame, text=personality_description,
                  style="White.TLabel", wraplength=400).grid(row=0, rowspan=2, column=2, sticky="N")

        query = ttk.Frame(chat)
        query.grid(row=1, column=0, padx=5, pady=5, sticky="NSEW")
        user_input_box = scrolledtext.ScrolledText(query, width=80, height=8, wrap=tk.WORD)
        user_input_box.grid(row=0, column=0, padx=10, pady=10)

        response = ttk.Frame(chat)
        response.grid(row=2, column=0, padx=5, pady=5, sticky="NSEW")
        chat_log = scrolledtext.ScrolledText(response, width=90, height=8, wrap=tk.WORD)
        chat_log.grid(row=0, column=0, padx=10, pady=10)

        # Send button
        send_button = tk.Button(query, text="Send",
                                command=lambda: show_chatbot_response(username, personality, user_input_box, chat_log))
        send_button.grid(row=0, column=1, padx=10, pady=10)


# Get the chatbot response
def get_chatbot_response(input_text, username, personality):
    openai.api_key = "not_required"
    openai.api_base = "http://73.175.148.240:5000/v1"
    model = "TheBloke_stable-vicuna-13B-GPTQ"
    conversation = [
        {"role": "user", "content": input_text}
    ]
    response = openai.ChatCompletion.create(
        name1=username,
        role="user",
        character=personality,
        model=model,
        messages=conversation,
        temperature=0.7,
        max_tokens=2048,
        mode="chat",
        instruction_template="StableVicuna"
    )
    assistant_reply = response['choices'][0]['message']['content'].strip()

    return assistant_reply


# Display the chatbot response in the GUI
def show_chatbot_response(username, personality, user_input_box, chat_log):
    user_input = user_input_box.get("1.0", END).strip()
    user_input_box.delete("1.0", END)

    if user_input.lower() in ["exit", "quit", "bye"]:
        chat_log.insert(tk.END, personality + ": Goodbye!\n")
        return

    chat_log.insert(tk.END, username + ": " + user_input + "\n")
    chatbot_response = get_chatbot_response(user_input, username, personality)
    chat_log.insert(tk.END, personality + ": " + chatbot_response + "\n\n")
    chat_log.see(tk.END)
