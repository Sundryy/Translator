import cv2
import pyautogui
import numpy
import time
#fix up this gross mess
import tkinter as tk
from tkinter import Button, Label
from PIL import Image, ImageTk

firstX = 0
firstY = 0
lastX = 0
lastY = 0
choosingRectangle = False



colorLine = (0,0,255)
lineThickness = 2

def capture_event(event,x,y,flags,params):
    global firstX,firstY,lastX,lastY, choosingRectangle, colorLine, lineThickness, image, imageCopy
    #Finds top-left coordinate of chosen area
    if event == cv2.EVENT_LBUTTONDOWN:
        choosingRectangle = True
        firstX = x
        firstY = y
    
    elif event == cv2.EVENT_MOUSEMOVE and choosingRectangle:
        lastX = x
        lastY = y
        
        #Shows user where they are selecting part of the image
        tempImage = imageCopy.copy()
        cv2.rectangle(tempImage, (firstX,firstY), (lastX,lastY), colorLine, lineThickness)
        cv2.imshow('image', tempImage)

    #takes screenshot of selected area
    elif event == cv2.EVENT_LBUTTONUP:
        choosingRectangle = False
        chosenImage = image[firstY:lastY, firstX:lastX]
        cv2.imshow('Chosen Image',chosenImage)
        cv2.destroyWindow('image')

#clean up this mess
def imageCreation():
    global image, imageCopy
    image = pyautogui.screenshot()
    image = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)
    imageCopy = image.copy()

    cv2.imshow('image', image)
    cv2.setMouseCallback('image', capture_event)


#fix up this and actually make it my own
root = tk.Tk()
root.title("Screenshot Tool")
root.geometry("500x500")

start_button = Button(root, text="Start Screenshot", command=imageCreation)
start_button.pack(pady=10)

chosen_label = Label(root)
chosen_label.pack(pady=10)

root.mainloop()

