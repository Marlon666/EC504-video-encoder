import tkinter
from tkinter import filedialog
from tkinter import ttk
from tkinter import Listbox
from tkinter import Label
from tkinter.ttk import *
from tkinter import messagebox

top = tkinter.Tk()
top.geometry('450x450')
s = Style()
s.theme_use("classic")
s.configure("TProgressbar", thickness=35)


#CustomeList Box for Draging to reorder
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


#Methods
def startEncoding():
    tkMessageBox.showinfo("Starting Encoding", "Starting Encoding")
    progressBar.step(25)

def startDecoding():
    tkMessageBox.showinfo("Starting Decoding", "Starting Decoding")

def addFiles():
    files = tkFileDialog.askopenfiles(parent=top,mode='rb',title='Choose all of your photos')
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




#GUI Items

#Text
buttonSection = Label(top, background = "white", justify='center', text="Actions", font=("Helvetica", 20))
progressBarText = Label(top,background = "white", justify='center', text="Progress", font=("Helvetica", 20))
sliderText = Label(top, justify='center',background = "white", text="Disk Space vs. Quality", font=("Helvetica", 20))
filesText =  Label(top, justify='center',background = "white", text="Selected Files", font=("Helvetica", 20))

#Other Items
progressBar = ttk.Progressbar(top, style="TProgressbar", orient="horizontal",length=450, mode="determinate", maximum = 100.001, value = 0)
slider = Scale(top, from_=0, to=100, length=200)
listbox = CustomListBox(top, width = 450)
#Buttons
encodingButton = tkinter.Button(top, text = "Encode Photos", command = startEncoding)
decodeButton = tkinter.Button(top, text = "Decode File", command = startDecoding)
addFilesButton = tkinter.Button(top, text = "Add Files", command = addFiles)
clearFileButton = tkinter.Button(top, text = "Remove File", command = clearFile)

#Layout
buttonSection.pack()
encodingButton.pack()
decodeButton.pack()
progressBarText.pack()
progressBar.pack()
sliderText.pack()
slider.pack()
filesText.pack
listbox.pack()
addFilesButton.pack()
clearFileButton.pack()
top.mainloop()


