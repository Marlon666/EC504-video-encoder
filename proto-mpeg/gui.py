import tkinter
import queue
import threading
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

top = tkinter.Tk()
top.geometry('450x450')
s = Style()
s.theme_use("classic")
s.configure("TProgressbar", thickness=35)
progBarValue = 0
sliderValue = 0.0
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

#Custom Class for Threading
class ThreadedTask(threading.Thread):
    def __init__(self, queue, setting):
        threading.Thread.__init__(self)
        self.queue = queue
        self.setting = setting
    
    def run(self):
        if (self.setting < 0):
            print("Decode - long process running")
            queue.put(50)
            time.sleep(4)
            queue.put(50)
            print("long process done")
        else:
            print("Encode - long process running")
            print("Ratio:", self.setting)
            queue.put(10)
            time.sleep(2)
            queue.put(25)
            time.sleep(3)
            queue.put(25)
            time.sleep(3)
            queue.put(15)
            time.sleep(2)
            queue.put(25)
            print("long process done")

class encodeVideo(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        import proto_mpeg_x
        img_directory = '../testing/beach_288p/'
        filenames = sorted(listdir(img_directory))
        files = [img_directory + fname for fname in filenames]
        files = files[:4]
        print("Encoding files:")
        print(*files, sep='\n')
        proto_mpeg_x.encodeVideo('output.bin', files, mot_est='none', QF=1)


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


#GUI Methods

def startEncoding():
    global queue
    global progBarValue
    global sliderValue
    print(sliderValue)
    encodeButton.configure(state = tkinter.DISABLED)
    decodeButton.configure(state = tkinter.DISABLED)
    #ThreadedTask(queue, sliderValue).start()
    encodeVideo(queue).start()
    top.after(100, process_queue, sliderValue)


def startDecoding():
    global queue
    global progBarValue
    global sliderValue
    print(sliderValue)
    encodeButton.configure(state = tkinter.DISABLED)
    decodeButton.configure(state = tkinter.DISABLED)
    ThreadedTask(queue, -1).start()
    top.after(100, process_queue, -1)

def addFiles():
    files = filedialog.askopenfiles(parent=top,mode='rb',title='Choose all of your images')
    if files != None:
        for file in files:
            data = file.read()
            file.close()
            print ("File Location: %s" % file.name)
            listbox.insert(0, file.name)

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
    print (sliderValue)
    sliderValueText.config(text=str(sliderValue))   


#GUI Items

#Text
buttonSection = Label(top, background = "white", justify='center', text="Actions", font=("Helvetica", 20))
progressBarText = Label(top,background = "white", justify='center', text="Progress", font=("Helvetica", 20))
sliderText = Label(top, justify='center',background = "white", text="Disk Space vs. Quality", font=("Helvetica", 20))
sliderValueText = Label(top, justify='center',background = "white", text="0", font=("Helvetica", 14))
sliderText = Label(top, justify='center',background = "white", text="Disk Space vs. Quality", font=("Helvetica", 20))
filesText =  Label(top, justify='center',background = "white", text="Selected Files", font=("Helvetica", 20))

#Other Items
progressBar = ttk.Progressbar(top, style="TProgressbar", orient="horizontal",length=450, mode="determinate", maximum = 100.001, value = 0)
slider = Scale(top, from_=0, to=100, length=200, command = update_value)
listbox = CustomListBox(top, width = 450)

#Buttons
encodeButton = tkinter.Button(top, text = "Encode Photos", command = startEncoding)
decodeButton = tkinter.Button(top, text = "Decode File", command = startDecoding)
addFilesButton = tkinter.Button(top, text = "Add Files", command = addFiles)
clearFileButton = tkinter.Button(top, text = "Remove File", command = clearFile)

#Layout
buttonSection.pack()
encodeButton.pack()
decodeButton.pack()
progressBarText.pack()
progressBar.pack()
sliderText.pack()
sliderValueText.pack()
slider.pack()
filesText.pack
listbox.pack()
addFilesButton.pack()
clearFileButton.pack()
top.mainloop()


