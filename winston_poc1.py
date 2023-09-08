
import tkinter as tk
import webview
  
tk = tk.Tk()
  
tk.geometry("800x450")
  
webview.create_window('LionAide', 'http://73.175.148.240:7860')
webview.start()
