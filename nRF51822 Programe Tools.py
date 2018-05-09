from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import Menu
from tkinter.ttk import *
from tkinter import ttk

from pynrfjprog import API, Hex
import serial
import serial.tools.list_ports

import threading
import platform
import os

"""
nRF51822 Programe Tools，Use Nordic nRF5x-Pynrfjprog。
"""

#-------------------------------------------------------------------------

softdevice_file_dir = os.getcwd()
bootload_file_dir = os.getcwd()
app_file_dir = os.getcwd()

def about():
    messagebox.showinfo('About', 'nRF51822 Programe Tools V1.0.0\nAuthor：Hellogz 2018/5/9')

def get_softdevice_file():
    global softdevice_file, softdevice_file_dir

    filename = filedialog.askopenfilename(initialdir=softdevice_file_dir, \
        title='Choice SoftDevice File', \
        defaultextension='.config', \
        filetypes = [('Hex File', '.hex')])
    if filename:
        softdevice_file_dir = os.path.dirname(filename)
        SoftDevicePath.set(filename)

def get_app_file():
    global app_file, app_file_dir

    filename = filedialog.askopenfilename(initialdir=app_file_dir, \
        title='Choice App Firmware File', \
        defaultextension='.config', \
        filetypes = [('Hex File', '.hex')])
    if filename:
        app_file_dir = os.path.dirname(filename)
        AppPath.set(filename)

def get_bootload_file():
    global bootload_file, bootload_file_dir

    filename = filedialog.askopenfilename(initialdir=bootload_file_dir, \
        title='Choice Bootload File', \
        defaultextension='.config', \
        filetypes = [('Hex File', '.hex')])
    if filename:
        bootload_file_dir = os.path.dirname(filename)
        BootloadPath.set(filename)

def get_jlink_list(jlink_obj):

    if not jlink_1.is_open():
        jlink_1.open()
    jlink_list = ['Choice ID']
    for device in jlink_obj.enum_emu_snr():
        jlink_list.append(device)

    if len(jlink_list) != 1:
        return jlink_list
    else:
        return ["No J-Link Device"]

def refresh_jlink_list():
    global jlink_1, JLinkDeviceList

    if not jlink_1.is_open():
        jlink_1.open()
    JLinkDeviceList = get_jlink_list(jlink_1)
    JLinkDevice_OP.set_menu(*JLinkDeviceList)

def programe_file_thread(jlink_obj, progress_obj, file_1, file_2, file_3):
    try:
        if not jlink_obj.is_open():
            jlink_obj.open()
        jlink_1.connect_to_emu_with_snr(int(JLinkDevice.get()))
        
        progress_obj["maximum"] = 3
        if file_1:
            jlink_1.erase_all()
            for segment in Hex.Hex(file_1):
                jlink_obj.write(segment.address, segment.data, True)
        progress_obj["value"] = 1
        if file_2:
            for segment in Hex.Hex(file_2):
                jlink_obj.write(segment.address, segment.data, True)
        progress_obj["value"] = 2
        if file_3:
            for segment in Hex.Hex(file_3):
                jlink_obj.write(segment.address, segment.data, True)
        progress_obj["value"] = 3
        # Reset device, run
        jlink_1.sys_reset()
        jlink_1.go()

        # Close API
        jlink_1.close()
    except API.APIError as exc:
        messagebox.showerror('Programe Status', str(exc))
    else:
        messagebox.showinfo('Programe Status', 'Programe Successed.')


def programe_file():
    global jlink_1, JLinkDevice

    if Check_1.get() or Check_2.get() or Check_3.get():
        if Check_1.get():
            sd_file = SoftDevicePath.get()
        else:
            sd_file = None
        if Check_2.get():
            app_file = AppPath.get()
        else:
            app_file = None
        if Check_3.get():
            bootload_file = BootloadPath.get()
        else:
            bootload_file = None

        if JLinkDevice.get() != "No J-Link Device" and JLinkDevice.get() != "Choice ID":
            download_progress["value"] = 0
            threading.Thread(target = programe_file_thread, args = [jlink_1, download_progress, sd_file, app_file, bootload_file]).start()
        else:
            messagebox.showerror('Programe Status', 'Programe Failed.\nNo %s.' %(JLinkDevice.get()))
    else:
        messagebox.showerror('Programe Status', 'Must choice one file.')
    


#------------------------------------------------------------------------- 
root = Tk() # create a top-level window
jlink_1 = API.API(API.DeviceFamily.NRF51)
#-------------------------------------------------------------------------
SoftDevicePath = StringVar()
AppPath = StringVar()
BootloadPath = StringVar()

Check_1 = IntVar()
Check_2 = IntVar()
Check_3 = IntVar()

JLinkDevice = StringVar()
JLinkDeviceList = get_jlink_list(jlink_1)

if platform.release() == 'XP':
    w = 860 # width for the Tk root
    h = 595 # height for the Tk root
else:
    w = 860 # width for the Tk root
    h = 145 # height for the Tk root

# get screen width and height
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

# set the dimensions of the screen 
# and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

root.title('nRF51822 Program Tools') # title for top-level window
root.resizable(width=False, height=False)
# quit if the window is deleted
root.protocol("WM_DELETE_WINDOW", root.quit)

frame = Frame(root, name='main-frame')

menubar = Menu(root)
menubar.add_command(label='about', command=about)
root.config(menu=menubar)
#-------------------------------------------------------------------------

choice_files_frame = LabelFrame(frame, text="Files")

Checkbutton(choice_files_frame, text="SoftDevice File", variable=Check_1).grid(row=0, column=0, padx=5, pady=5, stick=W)
SoftDevicePathEnter = Entry(choice_files_frame, width=45, textvariable=SoftDevicePath)
SoftDevicePathEnter.grid(row=0, column=1, padx=5, pady=5, stick=E)
Button(choice_files_frame, text='...', command=get_softdevice_file, width=3).grid(row=0, column=2, padx=5, pady=5, stick=E)

Checkbutton(choice_files_frame, text="App File", variable=Check_2).grid(row=1, column=0, padx=5, pady=5, stick=W)
SoftDevicePathEnter = Entry(choice_files_frame, width=45, textvariable=AppPath)
SoftDevicePathEnter.grid(row=1, column=1, padx=5, pady=5, stick=E)
Button(choice_files_frame, text='...', command=get_app_file, width=3).grid(row=1, column=2, padx=5, pady=5, stick=E)

Checkbutton(choice_files_frame, text="Bootload File", variable=Check_3).grid(row=2, column=0, padx=5, pady=5, stick=W)
SoftDevicePathEnter = Entry(choice_files_frame, width=45, textvariable=BootloadPath)
SoftDevicePathEnter.grid(row=2, column=1, padx=5, pady=5, stick=E)
Button(choice_files_frame, text='...', command=get_bootload_file, width=3).grid(row=2, column=2, padx=5, pady=5, stick=E)

choice_files_frame.grid(row=0, padx=5, pady=5, stick=W)

multi_download_frame = LabelFrame(frame, text="Programe")
if platform.release() == 'XP':
    w = 52
else:
    w = 37

Label(multi_download_frame, text='SEGGER to use:').grid(row=0, column=0, padx=5, pady=5, stick=W)
JLinkDevice_OP = OptionMenu(multi_download_frame, JLinkDevice, *JLinkDeviceList)
JLinkDevice_OP.config(width=13)
JLinkDevice_OP.grid(row=0, column=1, padx=5, pady=5)
Button(multi_download_frame, text='Refresh', command=refresh_jlink_list).grid(row=0, column=2, padx=5, pady=5, stick=E+W+N+S)

Label(multi_download_frame, text='Programe choice file:').grid(row=1, column=0, padx=5, columnspan=2, pady=5, stick=W)
Button(multi_download_frame, text='Programe', command=programe_file).grid(row=1, column=2, padx=5, pady=5)

download_progress = Progressbar(multi_download_frame, orient="horizontal", length=325, mode="determinate")
download_progress.grid(row=2, column=0, columnspan=4, padx=5, pady=5)

multi_download_frame.grid(row=0, column = 1, padx=5, pady=5, stick=E+W+N+S)

frame.pack()

#-------------------------------------------------------------------------

#-------------------------------------------------------------------------
# start the app
if __name__ == "__main__":
	root.mainloop() # call master's Frame.mainloop() method.
