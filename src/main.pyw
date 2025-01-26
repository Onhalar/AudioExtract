import tkinter.ttk as ttk
from moviepy import VideoFileClip
import os

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

def clearAll(fileList: Listbox, clearData = True):
    fileList.delete(0, END)
    if clearData:
        inFiles.clear()
        outFiles.clear()

def clearSelected(fileList: Listbox):
    indexes = fileList.curselection()[::-1]
    try:
        for index in indexes:
            fileList.delete(index)
            inFiles.pop(index)
    except TclError:
        pass

def selectFolder(displayLabel: Label):
    outPath = filedialog.askdirectory()
    displayLabel.config(text=truncateText(outPath, 15, True))

def getFileName(filePath: str):
    return os.path.basename(filePath)

def selectFiles(fileList: Listbox):
    inFiles.extend(filedialog.askopenfilenames(filetypes=[("Video files", "*.mp4;*.avi;*.mov")]))

    duplicateFound = False
    for file in inFiles:
        if inFiles.count(file) > 1:
            inFiles.remove(file)
            duplicateFound = True
    
    if duplicateFound:
        messagebox.showerror("Duplicate", "Duplicate file detected. Only the first occurrence will be processed.")
    
    clearAll(fileList, False)
    for file in inFiles:
        fileList.insert(END, truncateText(os.path.basename(file), 17))

def extractAll(fileList: Listbox, progressBar: ttk.Progressbar):
    progressBar.config(maximum= len(inFiles) - 1)
    for i in range(len(inFiles)):

        outFile = os.path.splitext(inFiles[i])[0] + ".mp3"

        outFiles.append(outFile)

        extractAudio(inFiles[i], outFile)

        progressBar.step()
        

        updatedItem = fileList.get(i) + " EX"
        fileList.delete(i)
        fileList.insert(i, updatedItem)
    

def UI():
    main = Tk()
    main.resizable(False, False)
    
    fileList = Listbox(main, selectmode="extended")
    fileList.grid(column=1, row=0)

    progressBar = ttk.Progressbar(main)
    progressBar.grid(column=0, row=1, columnspan=2, sticky="NSEW")

    progressDisplay = ttk.Frame(main)

    outPathDisplay = ttk.Label(progressDisplay, text="...")
    outPathDisplay.grid(column=1, row=1, sticky="NSEW")

    ttk.Button(progressDisplay, text="OUT", command= lambda : selectFolder(outPathDisplay)).grid(column=0, row=1)

    progressDisplay.grid(column=0, row=2, columnspan=2, sticky="NSEW")

    toolBar = ttk.Frame(main)
    ttk.Button(toolBar, text="OPEN", command= lambda : selectFiles(fileList)).grid(column=0, row=0, sticky="NSEW", pady=20)
    ttk.Button(toolBar, text="REMOVE", command=lambda fileList = fileList: clearSelected(fileList)).grid(column=0, row=1, sticky="NSEW")
    ttk.Button(toolBar, text="CLEAR", command= lambda fileList = fileList : clearAll(fileList)).grid(column=0, row=2, sticky="NSEW")
    ttk.Button(toolBar, text="EXTRACT", command= lambda fileList = fileList, progressBar = progressBar : extractAll(fileList, progressBar)).grid(column=0, row=3, sticky="NSEW", pady=15)
    toolBar.grid(column=0, row=0)

    main.mainloop()

# Main loop
if __name__ == '__main__':
    UI()