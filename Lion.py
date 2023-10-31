# -*- coding: utf-8 -*-
"""
Created on Sat May 20 19:42:50 2023

@author: c_doe
"""
from langchain.llms import OpenAI
import gradio as gr
import tkinter as tk
import webview

tk = tk.Tk()

tk.geometry("800x450")

squirrel = "http://10.0.0.241:5001/v1"
# model = "TheBLOK_vicuna-13b-v1.3.0-GPTQ"

# winston = OpenAI(model_name=model, openai_api_key="NotNeeded", openai_api_base=squirrel, temperature=0.5, max_tokens=512)

winston = OpenAI(openai_api_key="NotNeeded", openai_api_base=squirrel, temperature=0.5, max_tokens=512)

iface = gr.Interface(fn=winston, inputs=gr.Textbox(lines=7, label="Enter your text"), outputs="text", title="LionAIde")

iface.launch(server_name="0.0.0.0")
webview.create_window('LionAide', 'http://localhost:7860')
webview.start()
