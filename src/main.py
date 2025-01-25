import tkinter.ttk
from moviepy import VideoFileClip
import pygame

from tkinter import *
from tkinter import messagebox, filedialog , ttk #, simpledialog


# GLOBAL VARIABLES
inFiles = []
outFiles = []

outPath: str

def truncateText(text: str, length: int, fromBack = False):
    if (len(text) <= length): 
        return text
    
    if fromBack:
        return "..." + text[::-1][:length][::-1]
    else:
        return text[:length] + "..."

def extractAudio(inFile: str, outfile: str):

    video_clip = VideoFileClip(inFile)

    # Extract the audio from the video clip
    audio_clip = video_clip.audio

    audio_clip.write_audiofile(outfile)

    # Close the video and audio clips
    audio_clip.close()
    video_clip.close()

    print("Audio extraction successful!")

def clearAll(fileList: Listbox):
    fileList.delete(0, END)
    inFiles.clear()
    outFiles.clear()

def clearSelected(fileList: Listbox, index: int):
    try:
        fileList.delete(index)
        inFiles.pop(index)
    except TclError:
        pass

def selectFolder(displayLabel: Label):
    outPath = filedialog.askdirectory()
    displayLabel.config(text=truncateText(outPath, 15, True))

def selectFiles(fileList: Listbox):
    pass

def UI():
    main = Tk()
    main.resizable(False, False)

    fileList = Listbox(main)
    fileList.grid(column=1, row=0)

    toolBar = ttk.Frame(main)
    ttk.Button(toolBar, text="OPEN").grid(column=0, row=0, sticky="NSEW", pady=20)
    ttk.Button(toolBar, text="REMOVE", command=lambda fileList = fileList, index = fileList.curselection() : clearSelected(fileList, index)).grid(column=0, row=1, sticky="NSEW")
    ttk.Button(toolBar, text="CLEAR", command= lambda fileList = fileList : clearAll(fileList)).grid(column=0, row=2, sticky="NSEW")
    ttk.Button(toolBar, text="EXTRACT").grid(column=0, row=3, sticky="NSEW", pady=15)
    toolBar.grid(column=0, row=0)

    progressBar = ttk.Progressbar(main)
    progressBar.grid(column=0, row=1, columnspan=2, sticky="NSEW")

    progressDisplay = ttk.Frame(main)

    outPathDisplay = ttk.Label(progressDisplay, text="...")
    outPathDisplay.grid(column=1, row=1, sticky="NSEW")

    ttk.Button(progressDisplay, text="OUT", command= lambda : selectFolder(outPathDisplay)).grid(column=0, row=1)

    progressDisplay.grid(column=0, row=2, columnspan=2, sticky="NSEW")

    main.mainloop()

# Main loop
UI()