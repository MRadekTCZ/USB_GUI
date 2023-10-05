# This is a sample Python script.
import tkinter
from tkinter import ttk
from PIL import Image, ImageTk
import serial
import keyboard

#Searching for availible COM ports
ports = []
#usb_port = serial.Serial(port="COM3", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

for i in range(1,15):
    try:
        usb_port = serial.Serial(port=("COM"+str(i)))
        ports.append("COM"+str(i))
    except:
        error = 1
usb_port.close()
print(ports)

#Button Functions
def btn_send_Click():
    global recv_message
    recv_message= send_entry.get()
    usb_port.write(recv_message.encode('Ascii'))
    #recv_text.insert(tkinter.END, usb_port.read(4).decode('Ascii'))
def btn_recv_Click():
    recv_text.insert(tkinter.END, usb_port.read(8).decode('Ascii'))
def COM_Port_connect():
    global usb_port
    usb_port.close()
    usb_port = serial.Serial(port=port_combobox.get(), baudrate=baud_combobox.get(), bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    btn_send.config(state="active")
    btn_recv.config(state="active")
    btn_setfreq.config(state="active")
    btn_softstart.config(state="active")
    btn_softstop.config(state="active")
    btn_on.config(state="active")
    btn_off.config(state="active")
    btn_refreshfreq.config(state="active")
    btn_setramp.config(state="active")
def MRB_ON():
    usb_port.write('AA11'.encode('Ascii'))
    recv_text.insert(tkinter.END, usb_port.read(8).decode('Ascii'))
def MRB_OFF():
    usb_port.write('AA22'.encode('Ascii'))
    recv_text.insert(tkinter.END, usb_port.read(8).decode('Ascii'))
def SOFT_START():
    usb_port.write('CD10'.encode('Ascii'))
    recv_text.insert(tkinter.END, usb_port.read(8).decode('Ascii'))
def SOFT_STOP():
    usb_port.write('CE10'.encode('Ascii'))
    recv_text.insert(tkinter.END, usb_port.read(8).decode('Ascii'))
def SET_FREQ():
    print(len(freq_entry.get()))
    if (len(freq_entry.get()) == 3):
        usb_port.write(('B'+freq_entry.get()).encode('Ascii'))
        recv_text.insert(tkinter.END, usb_port.read(8).decode('Ascii'))
def REFRESH_FREQ():
    global actual_freq_received
    usb_port.write('CC11'.encode('Ascii'))
    actual_freq_received = usb_port.read(8).decode('Ascii')
    for i in range(0,7):
        actual_freq.delete(0)
    actual_freq.insert(0, actual_freq_received)
    actual_freq.delete(0)
def RAMP_START():
    if (len(ramp_end_freq_entry.get()) == 3) and (len(ramp_time_entry.get()) == 3):
        usb_port.write(('D'+ramp_end_freq_entry.get()).encode('Ascii'))
        recv_text.insert(tkinter.END, usb_port.read(8).decode('Ascii'))
        usb_port.write(('E'+ramp_time_entry.get()).encode('Ascii'))
        recv_text.insert(tkinter.END, usb_port.read(8).decode('Ascii'))
        usb_port.write('DDEE'.encode('Ascii'))
        recv_text.insert(tkinter.END, usb_port.read(8).decode('Ascii'))

#GUI start
window = tkinter.Tk()
window.title("MRB Serial port")

frame = tkinter.Frame(window)
frame.pack()
frame.config(bg="#26242f")

#GUI look - port frame
usb_gui_frame_port = tkinter.LabelFrame(frame, text='Serial Port Connection', )
usb_gui_frame_port.grid(row=0, column=0, padx=20, pady=20)
usb_gui_frame_port.config(bg="#65555f")
usb_gui_frame_port.config(width=100, height=100)

port_label = tkinter.Label(usb_gui_frame_port , text='Port', bg="#65555f", fg='#ffffff')
port_combobox = ttk.Combobox(usb_gui_frame_port , values=ports)
baud_label = tkinter.Label(usb_gui_frame_port , text='Baudrate', bg="#65555f", fg='#ffffff')
baud_combobox = ttk.Combobox(usb_gui_frame_port , values=['9600', '19200', '38400', '57600', '115200', '128000', '256000'])

port_label.grid(row=0, column=0)
baud_label.grid(row=1, column=0)
port_combobox.grid(row=0, column=1)
baud_combobox.grid(row=1, column=1)

btn_recv = tkinter.Button(usb_gui_frame_port, text='Connect', command=COM_Port_connect)
btn_recv.grid(row=0, column=2, padx=10, pady=10)


send_label = tkinter.Label(usb_gui_frame_port, text='Send', bg="#65555f", fg='#ffffff')
send_label.grid(row=2, column=0)
send_entry = tkinter.Entry(usb_gui_frame_port)
send_entry.grid(row=2, column=1)
btn_send = tkinter.Button(usb_gui_frame_port, text='Send', command=btn_send_Click)
btn_send.grid(row=2, column=2, padx=0, pady=10)
btn_send.config(state="disabled")

recv_label = tkinter.Label(usb_gui_frame_port, text='Receive', bg="#65555f", fg='#ffffff')
recv_label.grid(row=3, column=0)
recv_text = tkinter.Text(usb_gui_frame_port, height=6, width=15)
recv_text.grid(row=3, column=1)
#btn_recv = tkinter.Button(usb_gui_frame_port, text='Receive', command=btn_recv_Click)
#btn_recv.grid(row=3, column=2, padx=0, pady=10)
#btn_recv.config(state="disabled")





#GUI look - frame basic control
usb_gui_frame_basiccntrl = tkinter.LabelFrame(frame, text='Basic control')
usb_gui_frame_basiccntrl.grid(row=0, column=1, padx=20, pady=20)
usb_gui_frame_basiccntrl.config(bg="#65555f")
onoff_label = tkinter.Label(usb_gui_frame_basiccntrl, text='On / Off', bg="#65555f", fg='#ffffff')
onoff_label.grid(row=0, column=0)
btn_on = tkinter.Button(usb_gui_frame_basiccntrl, text='On', command=MRB_ON)
btn_on.grid(row=1, column=0, padx=0, pady=10)
btn_off = tkinter.Button(usb_gui_frame_basiccntrl, text='Off', command=MRB_OFF)
btn_off.grid(row=1, column=1, padx=0, pady=10)
btn_on.config(state="disabled")
btn_off.config(state="disabled")

freq_entry = tkinter.Entry(usb_gui_frame_basiccntrl)
freq_entry.grid(row=4, column=0, pady=10)
btn_setfreq = tkinter.Button(usb_gui_frame_basiccntrl, text='Set frequency', command=SET_FREQ)
btn_setfreq.grid(row=4, column=1, padx=10, pady=10)
act_freq_label = tkinter.Label(usb_gui_frame_basiccntrl, text='Actual frequency', bg="#65555f", fg='#ffffff')
act_freq_label.grid(row=5, column=0)
btn_refreshfreq = tkinter.Button(usb_gui_frame_basiccntrl, text='Refresh frequency', command=REFRESH_FREQ)
btn_refreshfreq.grid(row=6, column=1, padx=10, pady=10)
btn_refreshfreq.config(state="disabled")
actual_freq = tkinter.Entry(usb_gui_frame_basiccntrl)
actual_freq.grid(row=6, column=0, pady=0)
soft_label = tkinter.Label(usb_gui_frame_basiccntrl, text='Soft Start / Stop', bg="#65555f", fg='#ffffff')
soft_label.grid(row=7, column=0, pady=0)
btn_softstart = tkinter.Button(usb_gui_frame_basiccntrl, text='Soft Start', command=SOFT_START)
btn_softstart.grid(row=8, column=0, padx=0)
btn_softstop = tkinter.Button(usb_gui_frame_basiccntrl, text='Soft Stop', command=SOFT_STOP)
btn_softstop.grid(row=8, column=1, pady=0)
btn_setfreq.config(state="disabled")
btn_softstart.config(state="disabled")
btn_softstop.config(state="disabled")

#GUI look - frame with png
usb_gui_frame_cmdlist = tkinter.LabelFrame(frame, text='Command List')
usb_gui_frame_cmdlist.grid(row=1, column=0, padx=20, pady=20)
img_cmdlist = Image.open("COMMAND_LIST.png").resize((150,150), Image.LANCZOS)
img_cmdlist_gui = ImageTk.PhotoImage(img_cmdlist)
img_cmdlist_label = tkinter.Label(usb_gui_frame_cmdlist, image=img_cmdlist_gui)
img_cmdlist_label.grid(row=1, column=1, padx=20, pady=0)

usb_gui_frame_Ramp = tkinter.LabelFrame(frame, text='Ramp')
usb_gui_frame_Ramp.grid(row=1, column=1, padx=20, pady=20)
usb_gui_frame_Ramp.config(bg="#65555f")

#GUI look - ramp frame
end_freq_label = tkinter.Label(usb_gui_frame_Ramp, text='Set end frequency', bg="#65555f", fg='#ffffff')
end_freq_label.grid(row=0, column=1, padx=10)
ramp_time_label = tkinter.Label(usb_gui_frame_Ramp, text='Set ramp time', bg="#65555f", fg='#ffffff')
ramp_time_label.grid(row=1, column=1, padx=10)
ramp_end_freq_entry = tkinter.Entry(usb_gui_frame_Ramp)
ramp_end_freq_entry.grid(row=0, column=0, padx=10)
ramp_time_entry = tkinter.Entry(usb_gui_frame_Ramp)
ramp_time_entry.grid(row=1, column=0, padx=10)
btn_setramp = tkinter.Button(usb_gui_frame_Ramp, text='Set frequency', command=RAMP_START)
btn_setramp.grid(row=2, column=0, padx=20, pady=20)
btn_setramp.config(state="disabled")







window.mainloop()