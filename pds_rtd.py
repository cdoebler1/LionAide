# -*- coding: utf-8 -*-
"""
This program reads the RTD import from the Sequent HAT and displays the measured
temperature.
"""
#from datetime import datetime
import platform
import time
import numpy as np
import csv
import tkinter as tk
from tkinter import ttk
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
from ttkthemes import ThemedTk
import shutil

try:
	with open('/home/pds2021/Desktop/pds/config.json') as config_file:
		data = json.load(config_file)
except:
	with open('config.json') as config_file:
		data = json.load(config_file)

version = "v1.2"
pdstheme = data["theme"]
right_position = data["right_position"]
left_position = data["left_position"]
ambient_position = data["ambient_position"]
lims = data["lims"]
show_close_window = data["show_close_window"]
beeper_GPIOheadpin = data["beeper_GPIOheadpin"]
#limit = data["mp_delta_t_limit"]
#sampling_delay = data["sampling_delay"]
#left_offset = data["left_offset"]
#ls = data["left_slope"]
#right_offset = data["right_offset"]
#rs = data["right_slope"]
#ambient_offset = data["ambient_offset"]
#ambient_slope = data["ambient_slope"]
#save_dir = data["save_dir"]
#stop_count = data["stop_count"]
#beeper_count = data["beeper_count"]

left_delta=""
right_delta=""

try:
	import librtd
except:
	print("The RTD library is not available.")
	left_position = 0
	right_position = 0
	ambient_position = 0

try:
	import RPi.GPIO as GPIO
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(beeper_GPIOheadpin, GPIO.OUT)
except:
	print("The GPIO Library is not available.")
	data["beeper_count"] = 0 # disable beeper

# array initialization
left_array = np.zeros(240)
left_ambient = np.zeros(240)
left_time = [None]*240
right_array = np.zeros(240)
right_ambient = np.zeros(240)
right_time = np.empty(240)
test_time = np.arange(0, 3600, 15)

# runtime variable initialization
global left_run, right_run, j, k, left_transition, right_transition, lMeltingPoint, rMeltingPoint, lt, rt
global run_dot_left, run_dot_right
run_dot_left = " •"
run_dot_right = " •"
left_run = False
right_run = False
j = 0
k = 0
left_transition = False
right_transition = False
block_temp=28
lMeltingPoint = 0
rMeltingPoint = 0
lt = 100
rt = 100

demo_array = np.array([
			   70.405, 74.266, 77.252, 78.459, 78.510, 78.166, 77.645, 77.019,
               76.296, 75.580, 74.848, 74.109, 73.373, 72.594, 71.865, 71.140,
               70.427, 69.716, 68.981, 68.292, 67.616, 66.949, 66.291, 65.611,
               64.981, 64.358, 63.746, 63.145, 62.523, 61.973, 61.372, 60.813,
               60.263, 59.694, 59.191, 58.642, 58.134, 57.633, 57.123, 56.672,
               56.183, 55.733, 55.295, 54.869, 54.433, 54.036, 53.651, 53.281,
               52.926, 52.568, 52.259, 51.933, 51.639, 51.352, 51.093, 50.867,
               50.636, 50.436, 50.245, 50.084, 49.950, 49.821, 49.717, 49.617,
               49.538, 49.476, 49.419, 49.377, 49.341, 49.316, 49.295, 49.273,
               49.253, 49.232, 49.207, 49.181, 49.150, 49.120, 49.088, 49.056,
               49.022, 48.982, 48.947, 48.906, 48.869, 48.827, 48.785, 48.743,
               48.697, 48.654, 48.606, 48.554, 48.504, 48.447, 48.399, 48.344,
               48.284, 48.224, 48.163, 48.106, 48.045, 47.981, 47.916, 47.857,
               47.790, 47.722, 47.651, 47.583, 47.520, 47.446, 47.378, 47.303,
               47.232, 47.167, 47.089, 47.018, 46.941, 46.867, 46.797, 46.720,
               46.647, 46.567, 46.492, 46.420, 46.339, 46.265, 46.184, 46.105,
               46.032, 45.950, 45.873, 45.791, 45.716, 45.637, 45.554, 45.474,
               45.390, 45.314, 45.235, 45.147, 45.067, 44.980, 44.906, 44.822,
               44.734, 44.651, 44.567, 44.486, 44.404, 44.313, 44.230, 44.142,
               44.062, 43.978, 43.889, 43.805, 43.723, 43.634, 43.547, 43.456,
               43.370, 43.289, 43.198, 43.110, 43.016, 42.930, 42.850, 42.756,
               42.667, 42.575, 42.486, 42.403, 42.310, 42.221, 42.126, 42.038,
               41.952, 41.858, 41.858, 41.858, 41.858, 41.858, 41.858, 41.858,
               41.858, 41.858, 41.858, 41.858, 41.858, 41.858, 41.858, 41.858,
               41.858, 41.858, 41.858, 41.858, 41.858, 41.858, 41.858, 41.858,
               41.858, 41.858, 41.858, 41.858, 41.858, 41.858, 41.858, 41.858,
               41.858, 41.858, 41.858, 41.858, 41.858, 41.858, 41.858, 41.858,
               41.858, 41.858, 41.858, 41.858, 41.858, 41.858, 41.858, 41.858,
               41.858, 41.858, 41.858, 41.858, 41.858, 41.858, 41.858, 41.858,
               41.858, 41.858, 41.858, 41.858, 41.858, 41.858, 41.858, 41.858,
               41.858, 41.858, 41.858, 41.858, 41.858, 41.858, 41.858, 41.858,
               41.858, 41.858, 41.858, 41.858, 41.858, 41.858, 41.858, 41.858,
               41.858, 41.858, 41.858, 41.858, 41.858, 41.858, 41.858, 41.858,
               41.858, 41.858, 41.858, 41.858, 41.858, 41.858, 41.858, 41.858,
               41.858, 41.858, 41.858, 41.858, 41.858, 41.858, 41.858, 41.858,
               41.858, 41.858, 41.858, 41.858, 41.858, 41.858, 41.858, 41.858,
               41.858, 41.858, 41.858, 41.858, 41.858, 41.858, 41.858, 41.858,
               41.858, 41.858, 41.858, 41.858, 41.858, 41.858, 41.858, 41.858,
               41.858, 41.858, 41.858, 41.858, 41.858, 41.858, 41.858, 41.858,
               31.858, 31.858, 31.858, 31.858, 31.858, 31.858, 31.858, 31.858])

class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = ttk.Label(tw, text=self.text, justify=tk.LEFT,
                      background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"), padding=(5, 5, 5, 5))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
	toolTip = ToolTip(widget)
	def enter(event):
		toolTip.showtip(text)
		widget.bind('<Leave>', leave)
	def leave(event):
		toolTip.hidetip()
		widget.bind('<Enter>', enter)
	widget.bind('<Enter>', enter)
	return

def getTemp(position, i):
	if position == 0: temp = demo_array[i]
	else: temp = librtd.get(0, position)
	return temp

def getRealTimeCellTemp(position):
	if position == 0: temp = 0.0
	else: temp = librtd.get(0, position)
	return temp

def getAmbientTemp(position):
	if position == 0: temp = 23.25
	else: temp = librtd.get(0, position)
	return temp

def leftDelta(i):
	left_delta = round(max(left_array[i-5: i]) - min(left_array[i-5 : i]), 2)
	return left_delta

def leftCheckThermalArrest(i):
	global lmp_line
	lmp_line=left_cell.axhline(y=0)
	MeltingPoint = 0
	transition = False
	left_delta = leftDelta(i)
	if left_delta <= data["mp_delta_t_limit"]: transition = True
	if transition == True:
		MeltingPoint = round(np.average(left_array[i-5 : i]), 2)
		left_melt_temp.set(str('{:.2f}'.format(round(MeltingPoint, 2))) + " °C")
		left_cell.set_facecolor("lightgreen")
		lmp_line=left_cell.axhline(y=MeltingPoint, color='r', linewidth=2)
		lmp_line.set()
		threading.Thread(target=beeper).start()
	return transition, MeltingPoint, left_delta

def rightDelta(i):
	right_delta = round(max(right_array[i-5: i]) - min(right_array[i-5 : i]), 2)
	return right_delta

def rightCheckThermalArrest(i):
	global rmp_line
	rmp_line=right_cell.axhline(y=0)
	MeltingPoint = 0
	transition = False
	right_delta = rightDelta(i)
	if right_delta <= data["mp_delta_t_limit"]: transition = True
	if transition == True:
		MeltingPoint = round(np.average(right_array[i-5 : i]), 2)
		right_melt_temp.set(str('{:.2f}'.format(round(MeltingPoint, 2))) + " °C")
		right_cell.set_facecolor("lightgreen")
		rmp_line=right_cell.axhline(y=MeltingPoint, color='r', linewidth=2)
		rmp_line.set()
		threading.Thread(target=beeper).start()
	return transition, MeltingPoint, right_delta

def quit_win():
	root.destroy()

def left_start():
	global j, l, left_transition, left_run, left_time, left_stop_count
	left_clear()
	left_stop_count = 0
	j = 0
	l = int(time.time())
	left_transition = False
	left_run = True
	threading.Thread(target=runindicate_left).start()
	lbutton1_2["text"]="Stop"
	lbutton1_2["command"]=left_stop
	fbutton_2_1["state"]="disabled"
	left_array.fill(0)
	left_ambient.fill(0)
	left_time=[None]*240
	left_melt_temp.set(str(""))
	llabel_2_3.grid_forget()
	return

def left_clear():
	left_cell.set_facecolor("white")
	try: lmp_line.remove()
	except: None

def left_stop():
	global left_run, lfilename
	left_run = False
	lbutton1_2["text"]="Start"
	lbutton1_2["command"]=left_start
	if not right_run: fbutton_2_1["state"]='!disabled'
	llabel_2_3.grid(row=3, column=2, columnspan=1, pady=(2,3))
	left_concat = np.column_stack((left_time, left_ambient, left_array))
	lfilename = llabel_0_1.get() + str(int(time.time())) + ".csv"
	full_filename = data["save_dir"] + lfilename
	with open(full_filename, 'w') as file:
		file.write("Sample name: " + llabel_0_1.get() + "\n")
		file.write("Melting Point: " + str(lMeltingPoint) + "\n")
		file.write("--------------------------------------------\n\n")
		writer = csv.writer(file)
		writer.writerow(["Date, Time", "Bath Temp", "Sample Temp"])
		file.write("--------------------------------------------\n")
		writer.writerows(left_concat)
	return left_run

def right_start():
	global k, m, right_transition, right_run, right_time, right_stop_count
	right_clear()
	right_stop_count = 0
	k = 0
	m = int(time.time())
	right_transition = False
	right_run = True
	threading.Thread(target=runindicate_right).start()
	rbutton1_2["text"]="Stop"
	rbutton1_2["command"]=right_stop
	fbutton_2_1["state"]='disabled'
	right_array.fill(0)
	right_ambient.fill(0)
	right_time=[None]*240
	right_melt_temp.set(str(""))
	rlabel_2_3.grid_forget()
	return

def right_clear():
	right_cell.set_facecolor("white")
	try: rmp_line.remove()
	except: None

def right_stop():
	global right_run, rfilename
	right_run = False
	rbutton1_2["text"]="Start"
	rbutton1_2["command"]=right_start
	if not left_run: fbutton_2_1["state"]='!disabled'
	rlabel_2_3.grid(row=3, column=2, columnspan=1, pady=(2,3))
	right_concat = np.column_stack((right_time, right_ambient, right_array))
	rfilename =  rlabel_0_1.get() + str(int(time.time())) + ".csv"
	full_filename = data["save_dir"] + rfilename
	with open(full_filename, 'w') as file:
		file.write("Sample name: " + rlabel_0_1.get() + "\n")
		file.write("Melting Point: " + str(rMeltingPoint) + "\n")
		file.write("--------------------------------------------\n\n")
		writer = csv.writer(file)
		writer.writerow(["Date, Time", "Bath Temp", "Sample Temp"])
		file.write("--------------------------------------------\n")
		writer.writerows(right_concat)
	return right_run

def lexport():
  src = tk.filedialog.askopenfilename(initialdir=data["save_dir"], initialfile=lfilename, title="Select File", filetypes=(("CSV files","*.csv"),("all files","*.*")))
  des = tk.filedialog.asksaveasfilename(initialdir="", defaultextension=".csv", title="Write File", filetypes=(("CSV files","*.csv"),("all files","*.*")))
  shutil.copy(src, des)
  
def rexport():
  src = tk.filedialog.askopenfilename(initialdir=data["save_dir"], initialfile=rfilename, title="Select File", filetypes=(("CSV files","*.csv"),("all files","*.*")))
  des = tk.filedialog.asksaveasfilename(initialdir="", defaultextension=".csv", title="Write File", filetypes=(("CSV files","*.csv"),("all files","*.*")))
  shutil.copy(src, des)
  
def beeper():
	z = data["beeper_count"]
	while z > 0:
		GPIO.output(beeper_GPIOheadpin, GPIO.HIGH)
		time.sleep(.5)
		GPIO.output(beeper_GPIOheadpin, GPIO.LOW)
		time.sleep(.5)
		z -= 1
  
def runindicate_left():
	global left_run, run_dot_left
	while left_run == True:
		run_dot_left = " •"
		time.sleep(.5)
		run_dot_left = "  "
		time.sleep(.5)
		
def runindicate_right():
	global right_run, run_dot_right
	while right_run == True:
		run_dot_right = " •"
		time.sleep(.5)
		run_dot_right = "  "
		time.sleep(.5)
  
def config_null():
	return

def config_app():

	def apply(confvar, value):
		data[confvar] = value
		conf_label_0_2["text"]=str(data["left_offset"])
		conf_label_1_2["text"]=str(data["left_slope"])
		conf_label_2_2["text"]=str(data["right_offset"])
		conf_label_3_2["text"]=str(data["right_slope"])
		conf_label_4_2["text"]=str(data["ambient_offset"])
		conf_label_5_2["text"]=str(data["ambient_slope"])
		conf_label_6_2["text"]=str(data["mp_delta_t_limit"])
		conf_label_7_2["text"]=str(data["sampling_delay"])
		conf_label_8_2["text"]=data["save_dir"]
		conf_label_9_2["text"]=str(data["stop_count"])
		conf_label_10_2["text"]=str(data["beeper_count"])
		save_enable()
		
	def save_enable():
		conf_save["state"]="!disabled"
	
	def app_config_save():
		response = tk.messagebox.askyesno(
			message="Are you sure that you want to save the active values?"
			)
		if response == 'no': return

		settings = {
			"theme" : pdstheme,
			"left_position" : left_position,
			"right_position" : right_position,
			"ambient_position" : ambient_position,
			"lims" : lims,
			"show_close_window" : show_close_window,
			"beeper_GPIOheadpin" : beeper_GPIOheadpin,
			"mp_delta_t_limit" : data["mp_delta_t_limit"],
			"sampling_delay" : data["sampling_delay"],
			"left_offset" : data["left_offset"],
			"left_slope" : data["left_slope"],
			"right_offset" : data["right_offset"],
			"right_slope" : data["right_slope"],
			"ambient_offset" : data["ambient_offset"],
			"ambient_slope" : data["ambient_slope"],
			"save_dir" : data["save_dir"],
			"stop_count" : data["stop_count"],
			"beeper_count": data["beeper_count"]
			}
		
		with open("/home/pds2021/Desktop/pds/config.json", 'w') as config_file:
			json.dump(settings, config_file)
		
		conf_save["state"]="disabled"
		
	def set_default():
		left_offset_temp.set("0.0")
		ls_temp.set("1.0")
		right_offset_temp.set("0.0")
		rs_temp.set("1.0")
		ambient_offset_temp.set("0.0")
		ambient_slope_temp.set("1.0")
		limit_temp.set("0.1")
		sampling_delay_temp.set("15")
		save_dir_temp.set("./samples/")
		stop_count_temp.set("240")
		beeper_count_temp.set("5")
		
	def conf_close():
		conf_frame.destroy()
		root.focus_force()
		
	# Top level frame
	conf_frame = ttk.Frame(root, padding="2 1 1 30")
	conf_frame.grid(column=0, row=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S))
	conf_frame.columnconfigure(0, weight=1)
	conf_frame.rowconfigure(0, weight=1)

	# Banner
	conf_label = ttk.Label(conf_frame, style="Title.TLabel", text="PDS® LabTech Model 87 Configuration  " + version)
	conf_label.grid(column=0, row=0, sticky=(tk.N))
	
	# Configuration Frame
	frame3=ttk.Frame(conf_frame, style="Light.TFrame", padding="5 5 5 5")
	frame3.grid(column=0, row=2)
	frame3.grid_propagate(True)
	
	conf_header0=ttk.Label(frame3, text = "Description", style="Black.TLabel")
	conf_header1=ttk.Label(frame3, text = "Entry Field", style="Black.TLabel")
	conf_header2=ttk.Label(frame3, text = "Current Value", style="Black.TLabel")
	conf_header3=ttk.Label(frame3, text = "", style="Black.TLabel")
	conf_header0.grid(row=0, column=0)
	conf_header1.grid(row=0, column=1)
	conf_header2.grid(row=0, column=2)
	conf_header3.grid(row=0, column=3)
	
	left_offset_temp=tk.DoubleVar()
	left_offset_temp.set(data["left_offset"])
	conf_label_0_0=ttk.Label(frame3, text="Left RTD intercept: ", style="White.TLabel")
	conf_label_0_1=ttk.Entry(frame3, textvariable = left_offset_temp)
	conf_label_0_2=ttk.Label(frame3, text=str(data["left_offset"]), style="White.TLabel")
	conf_label_0_3=ttk.Button(frame3, text="Apply", command = lambda: apply("left_offset", left_offset_temp.get()))
	conf_label_0_0.grid(row=1, column=0)
	conf_label_0_1.grid(row=1, column=1)
	conf_label_0_2.grid(row=1, column=2)
	conf_label_0_3.grid(row=1, column=3)
	
	ls_temp=tk.DoubleVar()
	ls_temp.set(data["left_slope"])
	conf_label_1_0=ttk.Label(frame3, text="Left RTD slope: ", style="White.TLabel")
	conf_label_1_1=ttk.Entry(frame3, textvariable = ls_temp)
	conf_label_1_2=ttk.Label(frame3, text=str(data["left_slope"]), style="White.TLabel")
	conf_label_1_3=ttk.Button(frame3, text="Apply", command = lambda: [save_enable(), apply("left_slope", ls_temp.get())])
	conf_label_1_0.grid(row=2, column=0)
	conf_label_1_1.grid(row=2, column=1)
	conf_label_1_2.grid(row=2, column=2)
	conf_label_1_3.grid(row=2, column=3)

	right_offset_temp=tk.DoubleVar()
	right_offset_temp.set(data["right_offset"])
	conf_label_2_0=ttk.Label(frame3, text="Right RTD intercept: ", style="White.TLabel")
	conf_label_2_1=ttk.Entry(frame3, textvariable=right_offset_temp)
	conf_label_2_2=ttk.Label(frame3, text=str(data["right_offset"]), style="White.TLabel")
	conf_label_2_3=ttk.Button(frame3, text="Apply", command = lambda: [save_enable(), apply("right_offset", right_offset_temp.get())])
	conf_label_2_0.grid(row=3, column=0)
	conf_label_2_1.grid(row=3, column=1)
	conf_label_2_2.grid(row=3, column=2)
	conf_label_2_3.grid(row=3, column=3)

	rs_temp=tk.DoubleVar()
	rs_temp.set(data["right_slope"])
	conf_label_3_0=ttk.Label(frame3, text="Right RTD slope: ", style="White.TLabel")
	conf_label_3_1=ttk.Entry(frame3, textvariable=rs_temp)
	conf_label_3_2=ttk.Label(frame3, text=str(data["right_slope"]), style="White.TLabel")
	conf_label_3_3=ttk.Button(frame3, text="Apply", command = lambda: [save_enable(), apply("right_slope", rs_temp.get())])
	conf_label_3_0.grid(row=4, column=0)
	conf_label_3_1.grid(row=4, column=1)
	conf_label_3_2.grid(row=4, column=2)
	conf_label_3_3.grid(row=4, column=3)
		
	ambient_offset_temp=tk.DoubleVar()
	ambient_offset_temp.set(data["ambient_offset"])
	conf_label_4_0=ttk.Label(frame3, text="Ambient RTD intercept: ", style="White.TLabel")
	conf_label_4_1=ttk.Entry(frame3, textvariable=ambient_offset_temp)
	conf_label_4_2=ttk.Label(frame3, text=str(data["ambient_offset"]), style="White.TLabel")
	conf_label_4_3=ttk.Button(frame3, text="Apply", command = lambda: [save_enable(), apply("ambient_offset", ambient_offset_temp.get())])
	conf_label_4_0.grid(row=5, column=0)
	conf_label_4_1.grid(row=5, column=1)
	conf_label_4_2.grid(row=5, column=2)
	conf_label_4_3.grid(row=5, column=3)

	ambient_slope_temp=tk.DoubleVar()
	ambient_slope_temp.set(data["ambient_slope"])
	conf_label_5_0=ttk.Label(frame3, text="Ambient RTD slope: ", style="White.TLabel")
	conf_label_5_1=ttk.Entry(frame3, textvariable=ambient_slope_temp)
	conf_label_5_2=ttk.Label(frame3, text=str(data["ambient_slope"]), style="White.TLabel")
	conf_label_5_3=ttk.Button(frame3, text="Apply", command = lambda: [save_enable(), apply("ambient_slope", ambient_slope_temp.get())])
	conf_label_5_0.grid(row=6, column=0)
	conf_label_5_1.grid(row=6, column=1)
	conf_label_5_2.grid(row=6, column=2)
	conf_label_5_3.grid(row=6, column=3)

	limit_temp=tk.DoubleVar()
	limit_temp.set(data["mp_delta_t_limit"])
	conf_label_6_0=ttk.Label(frame3, text="▲T Limit (°C): ", style="White.TLabel")
	conf_label_6_1=ttk.Entry(frame3, textvariable=limit_temp)
	conf_label_6_2=ttk.Label(frame3, text=str(data["mp_delta_t_limit"]), style="White.TLabel")
	conf_label_6_3=ttk.Button(frame3, text="Apply", command = lambda: [save_enable(), apply("limit", limit_temp.get())])
	conf_label_6_0.grid(row=7, column=0)
	conf_label_6_1.grid(row=7, column=1)
	conf_label_6_2.grid(row=7, column=2)
	conf_label_6_3.grid(row=7, column=3)

	sampling_delay_temp=tk.IntVar()
	sampling_delay_temp.set(data["sampling_delay"])
	conf_label_7_0=ttk.Label(frame3, text="Sampling delay (sec): ", style="White.TLabel")
	conf_label_7_1=ttk.Entry(frame3, textvariable=sampling_delay_temp)
	conf_label_7_2=ttk.Label(frame3, text=str(data["sampling_delay"]), style="White.TLabel")
	conf_label_7_3=ttk.Button(frame3, text="Apply", command = lambda: [save_enable(), apply("sampling_delay", sampling_delay_temp.get())])
	conf_label_7_0.grid(row=8, column=0)
	conf_label_7_1.grid(row=8, column=1)
	conf_label_7_2.grid(row=8, column=2)
	conf_label_7_3.grid(row=8, column=3)
	
	save_dir_temp=tk.StringVar()
	save_dir_temp.set(data["save_dir"])
	conf_label_8_0=ttk.Label(frame3, text="Export directory: ", style="White.TLabel")
	conf_label_8_1=ttk.Entry(frame3, textvariable=save_dir_temp)
	conf_label_8_2=ttk.Label(frame3, text=data["save_dir"], style="White.TLabel", width = 30)
	conf_label_8_3=ttk.Button(frame3, text="Apply", command = lambda: apply("save_dir", save_dir_temp.get()))
	conf_label_8_0.grid(row=9, column=0)
	conf_label_8_1.grid(row=9, column=1)
	conf_label_8_2.grid(row=9, column=2, padx=10)
	conf_label_8_3.grid(row=9, column=3)
	
	stop_count_temp=tk.IntVar()
	stop_count_temp.set(data["stop_count"])
	conf_label_9_0=ttk.Label(frame3, text="Stop count: ", style="White.TLabel")
	conf_label_9_1=ttk.Entry(frame3, textvariable=stop_count_temp)
	conf_label_9_2=ttk.Label(frame3, text=str(data["stop_count"]), style="White.TLabel")
	conf_label_9_3=ttk.Button(frame3, text="Apply", command = lambda: apply("stop_count", stop_count_temp.get()))
	conf_label_9_0.grid(row=10, column=0)
	conf_label_9_1.grid(row=10, column=1)
	conf_label_9_2.grid(row=10, column=2)
	conf_label_9_3.grid(row=10, column=3)

	beeper_count_temp=tk.IntVar()
	beeper_count_temp.set(data["beeper_count"])
	conf_label_10_0=ttk.Label(frame3, text="Beeper count: ", style="White.TLabel")
	conf_label_10_1=ttk.Entry(frame3, textvariable=beeper_count_temp)
	conf_label_10_2=ttk.Label(frame3, text=str(data["beeper_count"]), style="White.TLabel")
	conf_label_10_3=ttk.Button(frame3, text="Apply", command = lambda: apply("beeper_count", beeper_count_temp.get()))
	conf_label_10_0.grid(row=11, column=0)
	conf_label_10_1.grid(row=11, column=1)
	conf_label_10_2.grid(row=11, column=2)
	conf_label_10_3.grid(row=11, column=3)

	conf_save=ttk.Button(frame3, text="Save", command=lambda: app_config_save(), style="Black.TButton", state='disabled')
	conf_save.grid(row=20, column=0)	

	conf_default=ttk.Button(frame3, text="Default", command=set_default)
	conf_default.grid(row=20, column=1)	

	conf_cancel=ttk.Button(frame3, text="Close", command=conf_close)
	conf_cancel.grid(row=20, column=2)
	
	CreateToolTip(conf_label_0_3, text = 'Stores entry field value.\nDoes not save changes.')
	CreateToolTip(conf_label_1_3, text = 'Stores entry field value.\nDoes not save changes.')
	CreateToolTip(conf_label_2_3, text = 'Stores entry field value.\nDoes not save changes.')
	CreateToolTip(conf_label_3_3, text = 'Stores entry field value.\nDoes not save changes.')
	CreateToolTip(conf_label_4_3, text = 'Stores entry field value.\nDoes not save changes.')
	CreateToolTip(conf_label_5_3, text = 'Stores entry field value.\nDoes not save changes.')
	CreateToolTip(conf_label_6_3, text = 'Stores entry field value.\nDoes not save changes.')
	CreateToolTip(conf_label_7_3, text = 'Stores entry field value.\nDoes not save changes.')
	CreateToolTip(conf_label_8_3, text = 'Stores entry field value.\nDoes not save changes.')
	CreateToolTip(conf_label_9_3, text = 'Stores entry field value.\nDoes not save changes.')
	CreateToolTip(conf_label_10_3, text = 'Stores entry field value.\nDoes not save changes.')
	
	CreateToolTip(conf_label_8_0, text = 'Directory into which\nsample data is written.')
	CreateToolTip(conf_label_9_0, text = 'Number of additional measurements\nto take after melting point \n is determined.')
	CreateToolTip(conf_label_10_0, text = 'Number of times beeper chimes.\nSet to 0 to disable.')
	CreateToolTip(conf_save, text = 'Saves current values\nto memory.')
	CreateToolTip(conf_default, text = 'Populates entry field with\ndefault factory values.')	
	CreateToolTip(conf_cancel, text = 'Closes configuration window.\nDoes not save changes.')

# Create the main window
root = ThemedTk()
style = ttk.Style(root)
style.theme_use(pdstheme)
style.configure('.', font=('Calibri 12 bold'))
def_bold=('Calibri 14 bold')
style.configure('TFrame',  background="#233169")
style.configure('Title.TLabel', font=def_bold, foreground='white', background='#233169')
style.configure('Light.TFrame', background="#7B8CD0")
style.configure('White.TLabel', foreground='white', background="#7B8CD0")
style.configure('Black.TLabel', font=def_bold, foreground='white', background="#7B8CD0")
style.configure('White2.TLabel', foreground='white', background='#233169')
style.configure('Black.TButton', anchor="center")
root.geometry("800x480")
if platform.system() != "Windows":
	root.attributes('-fullscreen', True)
	root.resizable(False, False)
root.title("PDS® LabTech Model 87")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Top level frame
pds = ttk.Frame(root, padding="1 1 1 1")
pds.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

# Banner
label = ttk.Label(pds, style="Title.TLabel", text="PDS® LabTech Model 87")
label.grid(column=0, columnspan=4, row=0)
if show_close_window=="True":
	bbutton = ttk.Button(pds, text="X", command= quit_win, style="White2.TLabel")
	bbutton.grid(column=3, row=0, sticky="E", padx=(5,5))

# Left Cell Frame
frame1=ttk.Frame(pds, style="Light.TFrame", width=400, height=420)
frame1.grid(column=0, columnspan=2, row=1, sticky=(tk.N, tk.W, tk.E, tk.S))
frame1.grid_propagate(False)

left_sample=tk.StringVar()
left_sample.set("Left Sample")
llabel_0_0=ttk.Label(frame1, text="Sample ID:", style="White.TLabel")
llabel_0_1=ttk.Entry(frame1, textvariable=left_sample, width=22)
llabel_0_3=ttk.Label(frame1, text="ΔT:", style="White.TLabel")
if left_position==0: left_rtd="demo"
else: left_rtd=str(left_position)
llabel_1_0=ttk.Label(frame1, text="Temp:", style="White.TLabel")
left_cell_temp=tk.StringVar()
left_cell_temp.set(str('{:.2f}'.format(round(left_array[j], 2))) + " °C  ")
llabel_1_1=ttk.Label(frame1, textvar=left_cell_temp, width=8, style="White.TLabel")
lbutton1_2=ttk.Button(frame1, text="Start", command=left_start, width=5, style="Black.TButton")
llabel_1_3=ttk.Label(frame1, text="MP:", style="White.TLabel")
left_melt_temp=tk.StringVar()
left_melt_temp.set("")
left_delta=tk.StringVar()
left_delta.set("")
llabel_0_4=ttk.Label(frame1, textvar=left_delta, width=10, style="White.TLabel")
llabel_1_4=ttk.Label(frame1, textvar=left_melt_temp, width=10, style="White.TLabel")

llabel_0_0.grid(row=0, column=0, columnspan=1, sticky="E", padx=(5,5))
llabel_0_1.grid(row=0, column=1, columnspan=2, sticky="W", pady=(3,0))
llabel_0_3.grid(row=0, column=3, columnspan=1, sticky="E", padx=(5,0))
llabel_0_4.grid(row=0, column=4, columnspan=2, sticky="W", padx=(5,5))
llabel_1_0.grid(row=1, column=0, columnspan=1, sticky="E", padx=(0,5))
llabel_1_1.grid(row=1, column=1, columnspan=1, sticky="W", padx=(0,0))
lbutton1_2.grid(row=1, column=2, columnspan=1, pady=(3,3))
llabel_1_3.grid(row=1, column=3, columnspan=1, sticky="E", padx=(0,0))
llabel_1_4.grid(row=1, column=4, columnspan=1, sticky="W", padx=(5,5))

llabel_2_3=ttk.Button(frame1, text="Export", style="Black.TButton", command=lexport)

left_figure, left_cell = plt.subplots(dpi=70, facecolor="white")
left_line, = left_cell.plot(test_time, left_array, zorder=2)
left_cell.set(xlabel="Elapsed Time (s)")
left_cell.yaxis.set_major_formatter('{x:1.0f} °C')
left_cell.set_ylim(20, 90)

left_canvas = FigureCanvasTkAgg(left_figure, frame1)
left_canvas.draw()
left_canvas.get_tk_widget().config(width=390, height=320)
left_canvas.get_tk_widget().grid(row=2, column=0, columnspan=6, padx=(5,0))

CreateToolTip(lbutton1_2, text = 'Press to start/stop\nleft channel test.')
CreateToolTip(llabel_2_3, text = 'Export test data files to\nUSB memory stick/drive.')
# Right Cell Frame
frame2=ttk.Frame(pds, style="Light.TFrame", width=400, height=420)
frame2.grid(column=2, columnspan=2, row=1, sticky=(tk.N, tk.W, tk.E, tk.S))
frame2.grid_propagate(False)

right_sample=tk.StringVar()
right_sample.set("Right Sample")
rlabel_0_0=ttk.Label(frame2, text="Sample ID:", style="White.TLabel")
rlabel_0_1=ttk.Entry(frame2, textvariable=right_sample, width=22)
rlabel_0_3=ttk.Label(frame2, text="ΔT:", style="White.TLabel")
if right_position==0: right_rtd="demo"
else: right_rtd=str(right_position)
rlabel_1_0=ttk.Label(frame2, text="Temp:", style="White.TLabel")
right_cell_temp=tk.StringVar()
right_cell_temp.set(str('{:.2f}'.format(round(right_array[j], 2))) + " °C  ")
rlabel_1_1=ttk.Label(frame2, textvar=right_cell_temp, width=8, style="White.TLabel")
rbutton1_2=ttk.Button(frame2, text="Start", command=right_start, width=5, style="Black.TButton")
rlabel_1_3=ttk.Label(frame2, text="MP:", style="White.TLabel")
right_melt_temp=tk.StringVar()
right_melt_temp.set("")
right_delta=tk.StringVar()
right_delta.set("")
rlabel_0_4=ttk.Label(frame2, textvar=right_delta, style="White.TLabel")
rlabel_1_4=ttk.Label(frame2, textvar=right_melt_temp, width=10, style="White.TLabel")

rlabel_0_0.grid(row=0, column=0, columnspan=1, sticky="E", padx=(5,5))
rlabel_0_1.grid(row=0, column=1, columnspan=2, sticky="W", pady=(3,0))
rlabel_0_3.grid(row=0, column=3, columnspan=1, sticky="E", padx=(5,0))
rlabel_0_4.grid(row=0, column=4, columnspan=2, sticky="W", padx=(5,5))
rlabel_1_0.grid(row=1, column=0, columnspan=1, sticky="E", padx=(0,5))
rlabel_1_1.grid(row=1, column=1, columnspan=1, sticky="W", padx=(0,0))
rbutton1_2.grid(row=1, column=2, columnspan=1, pady=(3,3))
rlabel_1_3.grid(row=1, column=3, columnspan=1, sticky="E", padx=(0,0))
rlabel_1_4.grid(row=1, column=4, columnspan=1, sticky="W", padx=(5,5))

#rlabel_2_1=ttk.Button(pds, text="Configure", style="Black.TButton")
rlabel_2_3=ttk.Button(frame2, text="Export", style="Black.TButton", command=rexport)

right_figure, right_cell = plt.subplots(dpi=70)
right_line, = right_cell.plot(test_time, right_array, zorder=2)
right_cell.set(xlabel="Elapsed Time (s)")
right_cell.yaxis.set_major_formatter('{x:1.0f} °C')
right_cell.set_ylim(20, 90)

right_canvas = FigureCanvasTkAgg(right_figure, frame2)
right_canvas.draw()
right_canvas.get_tk_widget().config(width=390, height=320)
right_canvas.get_tk_widget().grid(row=2, column=0, columnspan=6, padx=(0,5))

CreateToolTip(rbutton1_2, text = 'Press to start/stop\nright channel test.')
CreateToolTip(rlabel_2_3, text = 'Export test data files to\nUSB memory stick/drive.')
# Footer
footerTime=tk.StringVar()
footerTime.set(time.strftime("%m/%d/%Y, %H:%M"))
footer1=ttk.Label(pds, textvariable=footerTime, style="White2.TLabel")
blockTemp=tk.StringVar()
footer2=ttk.Label(pds, textvariable=blockTemp, style="White2.TLabel")
LIMSOutput=tk.StringVar()

#footer3 = ttk.Label(pds, textvariable=LIMSOutput, style="White2.TLabel")

footer1.grid(column=0, row=2, sticky="NS")
footer2.grid(column=1, columnspan=2, row=2, sticky="NS")
fbutton_2_1=ttk.Button(pds, text="Configure", style="Black.TButton", command=config_app)
fbutton_2_1.grid(row=2, column=3, columnspan=2)

#CreateToolTip(fbutton_2_1, text = 'Set calibration and test parameters.')
#footer3.grid(column=3, row=3, sticky="S")

while True:
	ambient = (data["ambient_slope"]*getAmbientTemp(ambient_position)) + data["ambient_offset"]
	
	if left_run and int(time.time()) - l > j * data["sampling_delay"]:
		lt = getTemp(left_position, j)
		left_array[j] = (data["left_slope"] * lt) + data["left_offset"]
		left_ambient[j] = ambient
		left_time[j] = time.strftime("%m/%d/%Y, %H:%M:%S")
		if j > 4 and left_transition == False:
			left_transition, lMeltingPoint, ldelta = leftCheckThermalArrest(j)
		elif left_transition == True:
			ldelta = leftDelta(j)
			left_stop_count += 1
		else:
			ldelta = 0
		left_line.set_xdata(test_time)
		left_line.set_ydata(left_array)
		left_cell_temp.set(str('{:.2f}'.format(round(left_array[j], 2))) + " °C" + run_dot_left)
		left_delta.set(str('{:.2f}'.format(round(ldelta, 2))) + " °C")
		if left_transition == False and left_array[j] < 38:
			j = 239
			left_melt_temp.set(str('< 38 °C'))
		if left_stop_count > data["stop_count"]: j = 239
		j = j + 1
	elif left_run == True:
		left_cell_temp.set(str('{:.2f}'.format(round(left_array[j-1], 2))) + " °C" + run_dot_left)
	
	if right_run and int(time.time()) - m > k * data["sampling_delay"]:
		rt = getTemp(right_position, k)
		right_array[k] = (data["right_slope"] * rt) + data["right_offset"]
		right_ambient[k] = ambient
		right_time[k] = time.strftime("%m/%d/%Y, %H:%M:%S")
		if k > 4 and right_transition == False:
			right_transition, rMeltingPoint, rdelta = rightCheckThermalArrest(k)
		elif right_transition == True:
			rdelta = rightDelta(k)
			right_stop_count += 1
		else: rdelta = 0
		right_line.set_xdata(test_time)
		right_line.set_ydata(right_array)
		right_cell_temp.set(str('{:.2f}'.format(round(right_array[k], 2))) + " °C" + run_dot_right)
		right_delta.set(str('{:.2f}'.format(round(rdelta, 2))) + " °C")
		if right_transition == False and right_array[k] < 38:
			k = 239
			right_melt_temp.set(str('< 38 °C'))
		if right_stop_count > data["stop_count"]: k = 239
		k = k + 1
	elif right_run == True:
		right_cell_temp.set(str('{:.2f}'.format(round(right_array[k-1], 2))) + " °C" + run_dot_right)
	
	footerTime.set(time.strftime("%m/%d/%Y, %H:%M"))
	blockTemp.set("Bath Water Temp: " + str('{:.2f}'.format(round(ambient, 2))) + " °C")
	if left_run == False: 				#Display Realtime Left Cell Temp when not running
		run_dot_left = "  "
		lt = (data["left_slope"] * getRealTimeCellTemp(left_position)) + data["left_offset"] 	
		left_cell_temp.set(str('{:.2f}'.format(round(lt, 2))) + " °C" + run_dot_left)
	if right_run == False: 				#Display Realtime Right Cell Temp when not running
		run_dot_right = "  "
		rt = (data["right_slope"] * getRealTimeCellTemp(right_position)) + data["right_offset"] 
		right_cell_temp.set(str('{:.2f}'.format(round(rt, 2))) + " °C" + run_dot_right) 	
	if lims: LIMSOutput.set("LIMS Output Enabled")
	else: LIMSOutput.set("LIMS Output Disabled")
	
	left_figure.canvas.draw()
	left_figure.canvas.flush_events()
	right_figure.canvas.draw()
	right_figure.canvas.flush_events()
	
	if j > 239:
		if lMeltingPoint == 0: left_cell.set_facecolor("red")
		j = 0
		left_run = False
		left_stop()
	
	if k > 239:
		if rMeltingPoint == 0: right_cell.set_facecolor("red")
		k = 0
		right_run = False
		right_stop()

root.mainloop()
