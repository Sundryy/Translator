import cv2
import pyautogui
import numpy
import time
#fix up this gross mess
import tkinter as tk
from PIL import Image, ImageTk
#the other stuff is fine.
from pytesseract import pytesseract
from googletrans import Translator
import asyncio

pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

firstX = 0
firstY = 0
lastX = 0
lastY = 0
choosingRectangle = False
translator = Translator()

colorLine = (0,0,255)
lineThickness = 2

def capture_event(event,x,y,flags,params):
    global firstX,firstY,lastX,lastY, choosingRectangle, colorLine, lineThickness, image,chosenImage, translator
    #Finds top-left coordinate of chosen area
    if event == cv2.EVENT_LBUTTONDOWN:
        choosingRectangle = True
        firstX = x
        firstY = y
    
    elif event == cv2.EVENT_MOUSEMOVE and choosingRectangle:
        lastX = x
        lastY = y
        #Shows user the area of selection
        rectImage = image.copy()
        cv2.rectangle(rectImage, (firstX,firstY), (lastX,lastY), colorLine, lineThickness)
        cv2.imshow('image', rectImage)

    #takes screenshot of selected area
    elif event == cv2.EVENT_LBUTTONUP:
        cv2.destroyWindow('image')
        choosingRectangle = False
        chosenImage = image[firstY:lastY, firstX:lastX]
        cv2.imshow('Chosen Image',chosenImage)
        untranslatedWords = pytesseract.image_to_string(chosenImage)
        translatedWords = asyncio.run(translate(untranslatedWords))
        print(translatedWords)

async def translate (textToTranslate):
    async with Translator() as translator:
        result = await translator.translate(textToTranslate,src='auto',dest='en')
        return(result)

#clean up this mess
def imageCreation():
    global image
    #Removes GUI while screenshot is taken
    gui.withdraw()
    gui.update()
    #Captures screenshot, configuring for use with cv2
    image = pyautogui.screenshot()
    image = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)
    #shows image and allows input
    cv2.imshow('image', image)
    cv2.setMouseCallback('image', capture_event)


#GUI
#fix up this and actually make it my own
gui = tk.Tk()

#definitely does not centre, fix this eventually towards the end..
gui.eval('tk::PlaceWindow . center')


start_button = tk.Button(gui, text="Screenshot", command=imageCreation)
start_button.pack(pady=10)

chosen_label = tk.Label(gui, text= 'this is label')
chosen_label.pack(pady=10)

gui.mainloop()




