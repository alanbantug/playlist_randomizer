import tkinter
from tkinter import *

from tkinter.ttk import *
from tkinter import messagebox

from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename

import os
import shutil
import random
import threading

from time import time, sleep
from datetime import datetime, timedelta

import subprocess as sp

class Application(Frame):

    def __init__(self, master):

        self.master = master
        self.main_container = Frame(self.master)

        # Define the source and target folder variables

        self.origin = os.getcwd()
        self.source = ""
        self.target = ""
        self.initFolders = IntVar()

        # Create main frame
        self.main_container.grid(column=0, row=0, sticky=(N,S,E,W))

        # Set Label styles
        Style().configure("M.TLabel", font="Courier 20 bold", height="20", foreground="blue", anchor="center")
        Style().configure("B.TLabel", font="Verdana 8", background="white", width='46')
        Style().configure("MS.TLabel", font="Verdana 10" )
        Style().configure("S.TLabel", font="Verdana 8" )
        Style().configure("G.TLabel", font="Verdana 8")

        # Set button styles
        Style().configure("B.TButton", font="Verdana 8", relief="ridge")

        # Set check button styles
        Style().configure("B.TCheckbutton", font="Verdana 8")
        Style().configure("B.TCheckButton", font="Verdana 8")

        Style().configure("O.TLabelframe.Label", font="Verdana 8", foreground="black")

        # Create widgets
        self.sep_a = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_b = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_c = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_d = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_e = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_f = Separator(self.main_container, orient=HORIZONTAL)
        self.mainLabel = Label(self.main_container, text="RANDOMIZE UTILITY", style="M.TLabel" )
        self.subLabelA = Label(self.main_container, text="Randomizes music files from a folder for better listening while on  ", style="S.TLabel" )
        self.subLabelB = Label(self.main_container, text="the road. Source files must be in Music Bee format NNN-Artist-Track ", style="S.TLabel" )
        self.subLabelC = Label(self.main_container, text="initially at least, for this script to work", style="S.TLabel" )

        self.sourceFolder = LabelFrame(self.main_container, text=' Source Options ', style="O.TLabelframe")
        self.selectSource = Button(self.sourceFolder, text="FOLDER", style="B.TButton", command=self.setSource)
        self.sourceLabel = Label(self.sourceFolder, text="None", style="B.TLabel" )

        self.sep_s = Separator(self.sourceFolder, orient=HORIZONTAL)
        self.sep_t = Separator(self.sourceFolder, orient=HORIZONTAL)

        self.start = Button(self.main_container, text="START", style="B.TButton", command=self.startProcess)
        self.reset = Button(self.main_container, text="RESET", style="B.TButton", command=self.resetProcess)
        self.exit = Button(self.main_container, text="EXIT", style="B.TButton", command=root.destroy)

        self.progress_bar = Progressbar(self.main_container, orient="horizontal", mode="indeterminate", maximum=50)

        # Position widgets
        self.mainLabel.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')
        self.subLabelA.grid(row=1, column=0, columnspan=3, padx=5, pady=0, sticky='NSEW')
        self.subLabelB.grid(row=2, column=0, columnspan=3, padx=5, pady=0, sticky='NSEW')
        self.subLabelC.grid(row=3, column=0, columnspan=3, padx=5, pady=0, sticky='NSEW')

        self.sep_a.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')

        self.selectSource.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky='NSEW')
        self.sourceLabel.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky='NSEW')
        self.sep_s.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')

        self.sourceFolder.grid(row=8, column=0, columnspan=3, rowspan=5, padx=5, pady=5, sticky='NSEW')

        self.start.grid(row=14, column=0, columnspan=1, padx=5, pady=0, sticky='NSEW')
        self.reset.grid(row=14, column=1, padx=5, pady=0, sticky='NSEW')
        self.exit.grid(row=14, column=2, padx=5, pady=0, sticky='NSEW')
        self.sep_d.grid(row=15, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')
        self.progress_bar.grid(row=18, column=0, columnspan=3, padx=5, pady=0, sticky='NSEW')

    def setSource(self):

        pathname = askdirectory()

        if os.path.isdir(pathname):
            # self.sourceLabel["text"] = os.path.dirname(pathname)[:30] + ".../" + os.path.basename(pathname)
            self.sourceLabel["text"] = pathname
            self.source = pathname

    def startProcess(self):

        if self.checkFolders():
            t = threading.Thread(None, self.startRandomizeProcess, ())
            t.start()

    def startRandomizeProcess(self):
        ''' start copy process
        '''

        self.processControl(1)
        
        sourceFiles = []
        sourceFolders = []

        for folder, subs, files in os.walk(self.source):

            for file in files:
                sourceFolders.append(folder)
                sourceFiles.append(os.path.join(folder, file))

        random.shuffle(sourceFiles)
        ctr = 0

        for src in sourceFiles:

            ctr += 1

            track = src.split('\\')[-1]

            if len(track.split('-')) == 3:
                track_name = track.split('-')[2]
                if track.startswith('A'):
                    start = 'B'
                else:
                    start = 'A'

            elif len(track.split('-')) == 2:
                track_name = track.split('-')[1]
                if track.startswith('A'):
                    start = 'B'
                else:
                    start = 'A'

            else:
                 track_name = track
                 start = 'A'

            new_file_name = f'{start}{ctr:03d}-{track_name}'

            if os.path.exists(src):
                
                ''' copy file to new name
                '''
                shutil.copy(src, os.path.join(self.source, new_file_name))
                
                ''' remove file name
                '''
                os.remove(src)
            else:
                print('Not found')

        self.processControl(0)
        self.progress_bar.stop()

        messagebox.showinfo("Files randomized", f"Music files randomized.")
        
    def checkFolders(self):
        ''' check if folders are selected
        '''

        if self.source == "":
            messagebox.showerror("Source not selected", "Source folder not yet selected.")
            return False

        if len(os.listdir(self.source)) == 0:
            messagebox.showerror("Source empty", "Source folder is empty.")
            return False

        return True

    def processControl(self, mode):
        ''' enable/disable buttons as needed
        '''

        if mode:
            
            # disable all buttons

            self.selectSource["state"] = DISABLED
            self.reset["state"] = DISABLED
            self.start["state"] = DISABLED
            self.exit["state"] = DISABLED

            self.progress_bar.start()

        else:
            

            # enable all buttons

            self.selectSource["state"] = NORMAL
            self.reset["state"] = NORMAL
            self.start["state"] = NORMAL
            self.exit["state"] = NORMAL

            self.progress_bar.stop()
            sleep(5)

    def resetProcess(self):
        ''' reset labels, lists and flags
        '''
        
        os.chdir(self.origin)
        self.sourceLabel["text"] = "None"
        
        self.source = ""

root = Tk()
root.title("RANDOMIZE UTILITY")

# Set size

wh = 245
ww = 450

#root.resizable(height=False, width=False)

root.minsize(ww, wh)
root.maxsize(ww, wh)

# Position in center screen

ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (ww/2)
y = (hs/2) - (wh/2)

root.geometry('%dx%d+%d+%d' % (ww, wh, x, y))

app = Application(root)

root.mainloop()
