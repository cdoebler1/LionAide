"""
LionAIde client interface in Python

@author: Charles Doebler
@email: cdoebler1@gmail.com
"""
from langchain.llms import OpenAI
import gradio as gr
import tkinter as tk
import webview

tk = tk.Tk()

tk.geometry("800x450")

squirrel = "http://http://73.175.148.240:5001/v1"

winston = OpenAI(openai_api_key="NotNeeded", openai_api_base=squirrel, temperature=0.5, max_tokens=512)

iface = gr.Interface(fn=winston, inputs=gr.Textbox(lines=7, label="Enter your text"), outputs="text", title="LionAIde")

iface.launch(server_name="0.0.0.0")
webview.create_window('LionAide', 'http://localhost:7860')
webview.start()
