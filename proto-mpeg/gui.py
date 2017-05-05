import tkinter
import queue
# import threading
import math
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import Listbox
from tkinter import Label
from tkinter.ttk import *
from tkinter import messagebox
import time
from os import listdir
import subprocess

top = tkinter.Tk()
top.geometry('600x500')
s = Style()
s.theme_use("classic")
s.configure("TProgressbar", thickness=35)
progBarValue = DoubleVar()
sliderValue = 1
queue = queue.Queue()

#CustomList Box for Draging to reorder
class CustomListBox(tkinter.Listbox):
    def __init__(self, top, **kw):
        kw['selectmode'] = tkinter.SINGLE
        tkinter.Listbox.__init__(self, top, kw)
        self.bind('<Button-1>', self.changeCurrent)
        self.bind('<B1-Motion>', self.reorderSelected)
        self.curIndex = None
    
    def changeCurrent(self, e):
        self.curIndex = self.nearest(e.y)
    
    def reorderSelected(self, e):
        i = self.nearest(e.y)
        if i < self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i+1, x)
            self.curIndex = i
        elif i > self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i-1, x)
            self.curIndex = i

'''
#Completion Methods
def completeFunction(setting):
    encodeButton.configure(state = tkinter.NORMAL)
    decodeButton.configure(state = tkinter.NORMAL)
    progressBar.step(0.002)
    if (setting < 0):
        messagebox.showinfo("Decoding Finished", "Images have been decoded!")
    else:
        messagebox.showinfo("Encoding Finished", "Images have been encoded!")

#Handle the queue for threading
def process_queue(setting):
    try:
        step = queue.get(0)
        print(step)
        global progBarValue
        progressBar.step(step)
        progBarValue += step
        if (progBarValue < 100):
            top.after(100, process_queue, setting)
        else:
            progBarValue = 0
            top.after(1000, completeFunction, setting)
    except:
        #queue is currently empty, try again in 100ms
        top.after(100, process_queue, setting)
'''

#GUI Methods

def startEncoding():
    global queue
    global progBarValue
    global sliderValue

    files = listbox.get(0, END)
    num_frames = len(files)
    if num_frames == 0:
        print("No images selected to encode.")
        return
    i = -1
    progBarValue.set(0)

    encodeButton.configure(state=tkinter.DISABLED)
    decodeButton.configure(state=tkinter.DISABLED)

    QF = int(sliderValue)

    proc = subprocess.Popen([sys.executable, '-u', 'encode.py', '--qf', str(QF)] + list(files), stdout=subprocess.PIPE, bufsize=1)
    for line in iter(proc.stdout.readline, b''):
        print(line.decode(sys.stdout.encoding), end='')
        if i >= 0:
            progBarValue.set(i/num_frames*100)
        top.update()
        i += 1

    encodeButton.configure(state=tkinter.ACTIVE)
    decodeButton.configure(state=tkinter.ACTIVE)


def startDecoding():
    global queue
    global progBarValue
    global sliderValue

    files = listbox.get(0, END)
    num_videos = len(files)
    if num_videos == 0:
        print("No video selected to decode.")
        return


    encodeButton.configure(state=tkinter.DISABLED)
    decodeButton.configure(state=tkinter.DISABLED)

    for file in files:

        tot_frames = None
        i = -2
        progBarValue.set(0)

        proc = subprocess.Popen([sys.executable, '-u', 'decode.py', '--realtime', file], stdout=subprocess.PIPE, stdin=subprocess.PIPE, bufsize=1)
        for line in iter(proc.stdout.readline, b''):
            decoded_line = line.decode(sys.stdout.encoding)
            print(decoded_line, end='')
            if decoded_line.startswith('Total frames: '):
                tot_frames = int(decoded_line[len('Total frames: '):])
                # print("grabbed total frames:", tot_frames)

            if i > 0 and tot_frames != None:
                progBarValue.set(i/tot_frames*100)

            top.update()
            i += 1

    encodeButton.configure(state=tkinter.ACTIVE)
    decodeButton.configure(state=tkinter.ACTIVE)


def addFiles():
    files = filedialog.askopenfiles(parent=top,mode='rb',title='Choose all of your images')
    if files != None:
        for file in files:
            data = file.read()
            file.close()
            #print ("File Location: %s" % file.name)
            listbox.insert(END, file.name)

    else:
        print ("No files selected")

def clearFile():
    selection = listbox.curselection()
    if selection != ():
        pickedIndex = int(selection[0])
        listbox.delete(pickedIndex, pickedIndex)

def update_value(v):
    global sliderValue
    sliderValue = math.floor(float(v))
    #print (sliderValue)
    sliderValueText.config(text=str(sliderValue))

def clearAll():
    listbox.delete(0, END)

#GUI Items

#Text
#buttonSection = Label(top, background = "white", justify='center', text="Actions", font=("Helvetica", 20))
buttonSection = Label(top, justify='center', text="Actions", font=("Helvetica", 12))
progressBarText = Label(top,background = "white", justify='center', text="Progress", font=("Helvetica", 12))

QF_frame = Frame(master=top)
sliderText = Label(QF_frame, justify='center', text="Quantization factor:", font=("Helvetica", 12))
sliderValueText = Label(QF_frame, justify='center', text="0", font=("Helvetica", 12))

ft_frame = Frame(master=top)
filesText = Label(ft_frame, justify='center', text="Selected Files:", font=("Helvetica", 12))

#Other Items
progressBar = ttk.Progressbar(top, style="TProgressbar", orient="horizontal",length=450, mode="determinate", maximum = 100.001, value = 0, variable=progBarValue)
slider = Scale(QF_frame, from_=1, to=4, length=200, command = update_value)
listbox = CustomListBox(top, width = 450, height=20)

#Buttons
actions_frame = Frame(master=top)
encodeButton = tkinter.Button(actions_frame, text = "Encode video", command = startEncoding)
decodeButton = tkinter.Button(actions_frame, text = "Decode video", command = startDecoding)
fr = Frame(master=top)
addFilesButton = tkinter.Button(fr, text = "Add files(s)", command = addFiles)
clearFileButton = tkinter.Button(fr, text = "Remove selected file", command = clearFile)
clearAllButton = tkinter.Button(fr, text = "Clear all", command = clearAll)

#Layout

#progressBarText.pack()

separator1 = Frame(master=top, height=10)
separator1.pack()

filesText.pack(side=LEFT)
ft_frame.pack(fill=X, padx=5)
listbox.pack(fill=X, padx=5)

clearAllButton.pack(side=RIGHT)
clearFileButton.pack(side=RIGHT)
addFilesButton.pack(side=RIGHT)
fr.pack(fill=X)

separator = Frame(master=top, height=10)
separator.pack()

sliderText.pack(side=LEFT, padx=5)
slider.pack(side=LEFT, padx=5)
sliderValueText.pack(side=LEFT, padx=5)
QF_frame.pack(fill=X)

encodeButton.pack(side = LEFT)
decodeButton.pack(side = LEFT)
actions_frame.pack(pady=10)


progressBar.pack(fill=X, pady=10, padx=5)

top.title("EC504 Video Encoder/Decoder")

slider.set(1)
update_value(slider.get())

top.mainloop()


