from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import Menu
from tkinter.ttk import *
from tkinter import ttk

import pynrfjprog
from pynrfjprog import API, Hex

import threading
import platform
import os

"""
nRF5x Programe Tools，Use Nordic nRF5x-Pynrfjprog。
pyinstaller.py nrf5x_jtag_tool.py -F -w create exe file. -w is no console.
"""

#-------------------------------------------------------------------------

softdevice_file_dir = os.getcwd()
bootloader_file_dir = os.getcwd()
app_file_dir = os.getcwd()

def about():
    messagebox.showinfo('About', 'nRF5x Programe Tools V1.1.2\nAuthor：Hellogz 2018/11/23')

def get_softdevice_file():
    global softdevice_file, softdevice_file_dir

    filename = filedialog.askopenfilename(initialdir=softdevice_file_dir, \
        title='Choice SoftDevice File', \
        defaultextension='.hex', \
        filetypes = [('Hex File', '.hex')])
    if filename:
        softdevice_file_dir = os.path.dirname(filename)
        SoftDevicePath.set(filename)

def get_app_file():
    global app_file, app_file_dir

    filename = filedialog.askopenfilename(initialdir=app_file_dir, \
        title='Choice App Firmware File', \
        defaultextension='.hex', \
        filetypes = [('Hex File', '.hex')])
    if filename:
        app_file_dir = os.path.dirname(filename)
        AppPath.set(filename)

def get_bootloader_file():
    global bootloader_file, bootloader_file_dir

    filename = filedialog.askopenfilename(initialdir=bootloader_file_dir, \
        title='Choice Bootloader File', \
        defaultextension='.hex', \
        filetypes = [('Hex File', '.hex')])
    if filename:
        bootloader_file_dir = os.path.dirname(filename)
        BootloadPath.set(filename)

def get_jlink_list():

    if 1 == device_family.get():
        jlink_obj = API.API(API.DeviceFamily.NRF51)
    else:
        jlink_obj = API.API(API.DeviceFamily.NRF52)

    if not jlink_obj.is_open():
        jlink_obj.open()
    jlink_list = ['Choice ID']
    if jlink_obj.enum_emu_snr():
        for device in jlink_obj.enum_emu_snr():
            jlink_list.append(device)

    jlink_obj.close()
    if len(jlink_list) != 1:
        return jlink_list
    else:
        return ["No J-Link Device"]

def refresh_jlink_list():
    global JLinkDeviceList

    JLinkDeviceList = get_jlink_list()
    JLinkDevice_OP.set_menu(*JLinkDeviceList)

def programe_file_thread(jlink_obj, progress_obj, file_1, file_2, file_3):
    try:
        if not jlink_obj.is_open():
            jlink_obj.open()
        jlink_obj.connect_to_emu_with_snr(int(JLinkDevice.get()))

        progress_obj["maximum"] = 3
        if file_1:
            State.set("State: write SoftDevice...")
            for segment in Hex.Hex(file_1):
                jlink_obj.write(segment.address, segment.data, True)
        progress_obj["value"] = 1
        if file_2:
            State.set("State: write App...")
            for segment in Hex.Hex(file_2):
                jlink_obj.write(segment.address, segment.data, True)
        progress_obj["value"] = 2
        if file_3:
            State.set("State: write Bootload...")
            for segment in Hex.Hex(file_3):
                jlink_obj.write(segment.address, segment.data, True)

        State.set("State: config protection...")
        if 1 == device_family.get():
            if 1 == read_back_protection.get():
                jlink_obj.readback_protect('ALL')
        else:
            if 1 == read_back_protection.get():
                jlink_obj.write_u32(0x10001208, 0xFFFFFF00, True)
        
        # Reset device, run
        jlink_obj.sys_reset()
        jlink_obj.go()
        # Close API
        jlink_obj.close()

        State.set("State: Done.")
        progress_obj["value"] = 3
    except API.APIError as exc:
        jlink_obj.close()
        progress_obj["value"] = 0
        messagebox.showerror('Programe Status', str(exc))
    else:
        messagebox.showinfo('Programe Status', 'Programe Successed.')


def programe_file():
    global JLinkDevice

    if Check_1.get() or Check_2.get() or Check_3.get():
        if 1 == device_family.get():
            jlink_obj = API.API(API.DeviceFamily.NRF51)
        else:
            jlink_obj = API.API(API.DeviceFamily.NRF52)
        if Check_1.get():
            sd_file = SoftDevicePath.get()
        else:
            sd_file = None
        if Check_2.get():
            app_file = AppPath.get()
        else:
            app_file = None
        if Check_3.get():
            bootloader_file = BootloadPath.get()
        else:
            bootloader_file = None

        if JLinkDevice.get() != "No J-Link Device" and JLinkDevice.get() != "Choice ID":
            download_progress["value"] = 0
            threading.Thread(target = programe_file_thread, args = [jlink_obj, download_progress, sd_file, app_file, bootloader_file]).start()
        else:
            messagebox.showerror('Programe Status', 'Must choice one J-Link')
    else:
        messagebox.showerror('Programe Status', 'Must choice one file.')
    
def restart_device():
    if JLinkDevice.get() != "No J-Link Device" and JLinkDevice.get() != "Choice ID":
        try:
            if 1 == device_family.get():
                jlink_obj = API.API(API.DeviceFamily.NRF51)
            else:
                jlink_obj = API.API(API.DeviceFamily.NRF52)
            if not jlink_obj.is_open():
                jlink_obj.open()
            jlink_obj.connect_to_emu_with_snr(int(JLinkDevice.get()))
            jlink_obj.sys_reset()
            jlink_obj.go()
            jlink_obj.close()
            State.set("State: Restart Device Done.")
        except (API.APIError, pynrfjprog.API.APIError) as exc:
            jlink_obj.close()
            State.set("State: Restart Device Failed.")
            messagebox.showerror('Device Restart', str(exc))
    else:
        messagebox.showerror('Device Restart', 'Must choice one J-Link.')

def get_device_mac():
    if JLinkDevice.get() != "No J-Link Device" and JLinkDevice.get() != "Choice ID":
        try:
            if 1 == device_family.get():
                jlink_obj = API.API(API.DeviceFamily.NRF51)
            else:
                jlink_obj = API.API(API.DeviceFamily.NRF52)
            if not jlink_obj.is_open():
                jlink_obj.open()
            jlink_obj.connect_to_emu_with_snr(int(JLinkDevice.get()))
            ble_addr = jlink_obj.read(0x100000A4, 6)
            addr_string = "%02x:%02x:%02x:%02x:%02x:%02x" %(ble_addr[5] | 0xC0, ble_addr[4], ble_addr[3], ble_addr[2], ble_addr[1], ble_addr[0])
            jlink_obj.sys_reset()
            jlink_obj.go()
            jlink_obj.close()
        except (API.APIError, pynrfjprog.API.APIError) as exc:
            jlink_obj.close()
            State.set("State: Read Device MAC Address Failed.")
            messagebox.showerror('Read Device MAC Address', str(exc))
        else:
            State.set("State: Read Device MAC Address Successed.")
            messagebox.showinfo('Read Device MAC Address', addr_string)
    else:
        messagebox.showerror('Read Device MAC Address', 'Must choice one J-Link.')

def device_recover():
    if JLinkDevice.get() != "No J-Link Device" and JLinkDevice.get() != "Choice ID":
        try:
            if 1 == device_family.get():
                jlink_obj = API.API(API.DeviceFamily.NRF51)
            else:
                jlink_obj = API.API(API.DeviceFamily.NRF52)
            if not jlink_obj.is_open():
                jlink_obj.open()
            jlink_obj.connect_to_emu_with_snr(int(JLinkDevice.get()))
            jlink_obj.recover()
            jlink_obj.close()
        except (API.APIError, pynrfjprog.API.APIError) as exc:
            jlink_obj.close()
            State.set("State: Device Recover Failed.")
            messagebox.showerror('Device Recover', str(exc))
        else:
            State.set("State: Device Recover Successed.")
    else:
        messagebox.showerror('Device Recover', 'Must choice one J-Link.')

def device_erase_all():
    if JLinkDevice.get() != "No J-Link Device" and JLinkDevice.get() != "Choice ID":
        try:
            jlink_obj = None
            if 1 == device_family.get():
                jlink_obj = API.API(API.DeviceFamily.NRF51)
            else:
                jlink_obj = API.API(API.DeviceFamily.NRF52)
            if not jlink_obj.is_open():
                jlink_obj.open()
            jlink_obj.connect_to_emu_with_snr(int(JLinkDevice.get()))
            jlink_obj.erase_all()
            jlink_obj.close()
        except (API.APIError, pynrfjprog.API.APIError) as exc:
            jlink_obj.close()
            State.set("State: Device Erase All Failed.")
            messagebox.showerror('Device Erase All', str(exc))
        else:
            State.set("State: Device Erase All Successed.")
    else:
        messagebox.showerror('Device Erase All', 'Must choice one J-Link.')

#------------------------------------------------------------------------- 
root = Tk() # create a top-level window

#-------------------------------------------------------------------------
SoftDevicePath = StringVar()
AppPath = StringVar()
BootloadPath = StringVar()

Check_1 = IntVar()
Check_2 = IntVar()
Check_3 = IntVar()

if platform.release() == 'XP':
    w = 500 # width for the Tk root
    h = 270 # height for the Tk root
else:
    w = 550 # width for the Tk root
    h = 310 # height for the Tk root

# get screen width and height
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

# set the dimensions of the screen 
# and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

root.title('nRF5x Program Tools') # title for top-level window
root.resizable(width=False, height=False)
# quit if the window is deleted
root.protocol("WM_DELETE_WINDOW", root.quit)

frame = Frame(root, name='main-frame')

device_family = IntVar()
device_family.set(1)

read_back_protection = IntVar()
read_back_protection.set(2)

menubar = Menu(root)
setting_menu = Menu(menubar, tearoff=False)
setting_menu.add_radiobutton(label='nRF51', variable=device_family, value=1)
setting_menu.add_radiobutton(label='nRF52', variable=device_family, value=2)
protection_menu = Menu(menubar, tearoff=False)
protection_menu.add_radiobutton(label='protection enable', variable=read_back_protection, value=1)
protection_menu.add_radiobutton(label='protection disable', variable=read_back_protection, value=2)
menubar.add_cascade(label='setting nRF5x', menu=setting_menu)
menubar.add_cascade(label='protection', menu=protection_menu)
menubar.add_command(label='about', command=about)
root.config(menu=menubar)
#-------------------------------------------------------------------------

choice_files_frame = LabelFrame(frame, text="Files")

Checkbutton(choice_files_frame, text="SoftDevice File", variable=Check_1).grid(row=0, column=0, padx=5, pady=5, stick=W)
SoftDevicePathEnter = Entry(choice_files_frame, width=51, textvariable=SoftDevicePath)
SoftDevicePathEnter.grid(row=0, column=1, padx=5, pady=5, stick=E)
Button(choice_files_frame, text='...', command=get_softdevice_file, width=3).grid(row=0, column=2, padx=5, pady=5, stick=E)

Checkbutton(choice_files_frame, text="App File", variable=Check_2).grid(row=1, column=0, padx=5, pady=5, stick=W)
SoftDevicePathEnter = Entry(choice_files_frame, width=51, textvariable=AppPath)
SoftDevicePathEnter.grid(row=1, column=1, padx=5, pady=5, stick=E)
Button(choice_files_frame, text='...', command=get_app_file, width=3).grid(row=1, column=2, padx=5, pady=5, stick=E)

Checkbutton(choice_files_frame, text="Bootloader File", variable=Check_3).grid(row=2, column=0, padx=5, pady=5, stick=W)
SoftDevicePathEnter = Entry(choice_files_frame, width=51, textvariable=BootloadPath)
SoftDevicePathEnter.grid(row=2, column=1, padx=5, pady=5, stick=E)
Button(choice_files_frame, text='...', command=get_bootloader_file, width=3).grid(row=2, column=2, padx=5, pady=5, stick=E)

choice_files_frame.grid(row=0, padx=5, pady=5, stick=W)

multi_download_frame = LabelFrame(frame, text="Programe")
if platform.release() == 'XP':
    w = 37
else:
    w = 37

JLinkDevice = StringVar()
JLinkDeviceList = get_jlink_list()
State = StringVar()
State.set("State: waiting")

Label(multi_download_frame, text='SEGGER to use:').grid(row=0, column=0, padx=5, pady=5, stick=W)
JLinkDevice_OP = OptionMenu(multi_download_frame, JLinkDevice, *JLinkDeviceList)
JLinkDevice_OP.config(width=13)
JLinkDevice_OP.grid(row=0, column=1, padx=5, pady=5)
Button(multi_download_frame, text='Refresh', command=refresh_jlink_list).grid(row=0, column=2, padx=5, pady=5, stick=E+W+N+S)
Button(multi_download_frame, text='Restart', command=restart_device).grid(row=0, column=3, padx=5, pady=5, stick=E+W+N+S)
Button(multi_download_frame, text='Recover', command=device_recover).grid(row=0, column=4, padx=5, pady=5, stick=E+W+N+S)

Label(multi_download_frame, text='Programe choice file:').grid(row=1, column=0, padx=5, columnspan=2, pady=5, stick=W)
Button(multi_download_frame, text='Programe', command=programe_file).grid(row=1, column=2, padx=5, pady=5)
Button(multi_download_frame, text='Get MAC', command=get_device_mac).grid(row=1, column=3, padx=5, pady=5, stick=E+W+N+S)
Button(multi_download_frame, text='Erase All', command=device_erase_all).grid(row=1, column=4, padx=5, pady=5, stick=E+W+N+S)

if platform.release() == 'XP':
    download_progress = Progressbar(multi_download_frame, orient="horizontal", length=460, mode="determinate")
else:
    download_progress = Progressbar(multi_download_frame, orient="horizontal", length=520, mode="determinate")

download_progress.grid(row=2, column=0, columnspan=5, padx=5, pady=5)

Label(multi_download_frame, textvariable=State).grid(row=3, column=0, columnspan=5, padx=5, pady=5, stick=W)

multi_download_frame.grid(row=1, column = 0, padx=5, pady=5, stick=E+W+N+S)

frame.pack()

#-------------------------------------------------------------------------

#-------------------------------------------------------------------------
# start the app
if __name__ == "__main__":
	root.mainloop() # call master's Frame.mainloop() method.
	root.destroy() # if mainloop quits, destroy window
