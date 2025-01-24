import cv2
import pyautogui
import numpy
import time
#fix up this gross mess
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
#the other stuff is fine.
from pytesseract import pytesseract
from googletrans import Translator
import asyncio

pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

#beginning coordinates
firstX = -1
firstY = -1
lastX = -1
lastY = -1
choosingRectangle = False
translator = Translator()

#Rectangle characteristics
colorLine = (0,0,255)
lineThickness = 2

def capture_event(event,x,y,flags,params):
    global firstX,firstY,lastX,lastY, choosingRectangle, colorLine, lineThickness, image,chosenImage, translator
    #Finds starting point of area to select
    if event == cv2.EVENT_LBUTTONDOWN:
        choosingRectangle = True
        firstX = x
        firstY = y
    
    #Draw selecting area and determine end point.
    elif event == cv2.EVENT_MOUSEMOVE and choosingRectangle:
        lastX = x
        lastY = y
        #Shows user the area of selection
        rectImage = image.copy()
        cv2.rectangle(rectImage, (firstX,firstY), (lastX,lastY), colorLine, lineThickness)
        cv2.imshow('image', rectImage)

    #takes screenshot of selected area
    elif event == cv2.EVENT_LBUTTONUP:
        choosingRectangle = False
        chosenImage = image[firstY:lastY, firstX:lastX]
        cv2.destroyWindow('image')
        try:
            #Occurs if x and y cords of both points are different.
            untranslatedWords = pytesseract.image_to_string(chosenImage)
            translatedWords, predictedLanguage = asyncio.run(translate(untranslatedWords))
            print(translatedWords, predictedLanguage) #remove this eventually. for testing purposes

            #Removes old GUI elements and creates new ones to display translation and selected area.
            instructionsBtn.pack_forget(), startBtn.pack_forget(), frontName.pack_forget()
            visibleTranslation = tk.Label(gui, text= 'this is ' + translatedWords).pack()
            
            chosenImage = cv2.cvtColor(chosenImage, cv2.COLOR_BGR2RGB)
            im = ImageTk.PhotoImage(image=Image.fromarray(chosenImage))
            translatedImageTk = tk.Label(gui, image=im)
            translatedImageTk.pack()
            translatedImageTk.image = im
            gui.deiconify(), gui.update()

        except:
            #Occurs if no area is chosen/ x and y cords of both points are the same,
            #causing program to go back to GUI at the beginning.
            messagebox.showerror('Error', 'An area has not been selected. Please try again.')
            gui.deiconify()
            gui.update()

async def translate (textToTranslate):
    async with Translator() as translator:
        result = await translator.translate(textToTranslate,src='auto',dest='en')
        return result.text, result.src

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

#Centres widget on screen -- possibly need to check on other systems if it does do that.
def center_window(window):
    screen_width = gui.winfo_screenwidth()
    screen_height = gui.winfo_screenheight()
    x = (screen_width - gui.winfo_reqwidth()) // 2
    y = (screen_height - gui.winfo_reqheight()) // 2
    gui.geometry(f"+{x}+{y}")

#Instructions for how to use the program.
def loadInstructions():
    startBtn.pack_forget(), instructionsBtn.pack_forget(), frontName.pack_forget()
    thankYou = tk.Label(gui, text='Welcome and thank you using my program :)')
    instructions = tk.Label(gui, text='1. Screenshot your main monitors screen by pressing the "Screenshot" button.\n2. Click and drag your mouse from the top-left to the bottom-right of what you wish to translate.\n3. Recieve your translation!')
    thankYou.pack(), instructions.pack()

#see if this works
def retakeImage():
    cv2.imshow('image', image)
    cv2.setMouseCallback('image', capture_event)


gui = tk.Tk()
gui.title('Screenshot-to-Text Translator')
center_window(gui)

startBtn = tk.Button(gui, text="Screenshot", command=imageCreation)
instructionsBtn = tk.Button(gui, text="Instructions", command=loadInstructions)
startBtn.pack(pady=10)
instructionsBtn.pack(pady=10)

frontName = tk.Label(gui, text= 'this will be the name of the program.')
frontName.pack(pady=10)
ChangeRectangleBtn = tk.Button(gui, text='change area', command=retakeImage)
gui.mainloop()


#going to show the image taken, ask if its all good, if it isnt, then do process again.
#if it is good 


