from moviepy import VideoFileClip
import pygame
from tkinter import *

def extractAudio(inFile: str, outfile: str):

    video_clip = VideoFileClip(inFile)

    # Extract the audio from the video clip
    audio_clip = video_clip.audio

    audio_clip.write_audiofile(outfile)

    # Close the video and audio clips
    audio_clip.close()
    video_clip.close()

    print("Audio extraction successful!")

def UI():
    main = Tk()

    main.mainloop()

# Main loop
UI()