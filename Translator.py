import cv2
import pyautogui
import numpy
import time
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from pytesseract import pytesseract
from googletrans import Translator, LANGUAGES
import asyncio
import configparser

pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

coordinates = [0,0,0,0]
translator = Translator()
choosingRectangle = False
colorLine = (0,0,255)
lineThickness = 2

def capture_event(event,x,y,flags,params):
    global coordinates, choosingRectangle, colorLine, lineThickness, image, chosenImage, translator
    #Finds starting point of area to select
    if event == cv2.EVENT_LBUTTONDOWN:
        choosingRectangle = True
        coordinates[0] = x
        coordinates[1] = y
    
    #Draw selecting area and determine end point.
    elif event == cv2.EVENT_MOUSEMOVE and choosingRectangle:
        coordinates[2] = x
        coordinates[3] = y
        #Shows user the area of selection
        rectImage = image.copy()
        cv2.rectangle(rectImage, (coordinates[0], coordinates[1]), (coordinates[2], coordinates[3]), colorLine, lineThickness)
        cv2.imshow('image', rectImage)

    #takes screenshot of selected area
    elif event == cv2.EVENT_LBUTTONUP:
        choosingRectangle = False
        chosenImage = image[coordinates[1]:coordinates[3], coordinates[0]:coordinates[2]]
        cv2.destroyWindow('image')
        try:
            #Occurs if x and y cords of both points are different.
            untranslatedWords = pytesseract.image_to_string(chosenImage)
            translatedWords, predictedLanguage = asyncio.run(translate(untranslatedWords))
            #If no words are detected, it will return to last button press GUI state.
            if translatedWords == '': 
                raise Exception('No text detected in the selected area.')
            #Converts image for use with ImageTk
            chosenImage = cv2.cvtColor(chosenImage, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(chosenImage)
            #Ensures image fits within the GUI window
            if im.size[0] > 750:
                im = im.resize((750,im.size[1])) 
            #Ensures image fits within the GUI window
            if im.size[1] > 450:
                im = im.resize((im.size[0],450)) 

            im = ImageTk.PhotoImage(image=im)
            translatedImageTk.image = im
            #Changing GUI widgets
            translatedImageTk.config(image = im)
            translationTitle.config(text='Translation from ' + LANGUAGES[predictedLanguage].capitalize())
            visibleTranslation.config(text = translatedWords)
            instructionsBtn.place_forget(), screenShotBtn.place_forget(), frontName.place_forget()
            translatedImageTk.pack(pady=20), translationTitle.pack(), visibleTranslation.pack(), screenShotBtn.pack(side=LEFT,padx=125), reselectAreaBtn.pack(side=LEFT)
            gui.deiconify(), gui.update()
        except:
            #Occurs if no area is chosen/ x and y cords of both points are the same,
            #causing program to go back to GUI at the beginning.
            messagebox.showerror('Error', 'Words have not been detected. Please try again.')
            gui.deiconify()
            gui.update()

#Allow for translation of text w/o being stopped by the GUI
async def translate (textToTranslate):
    async with Translator() as translator:
        result = await translator.translate(textToTranslate,src='auto',dest='en')
        return result.text, result.src


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
    screenShotBtn.place_forget(), instructionsBtn.place_forget(), frontName.place_forget()
    thankYou.pack(), instructions.pack(pady=10), backBtn.pack()

#Returns GUI to start.
def back():
    thankYou.pack_forget(), instructions.pack_forget(), backBtn.pack_forget()
    frontName.place(relx=0.5, rely=0.5, anchor=CENTER)
    screenShotBtn.place(relx=0.65, rely=0.6, anchor=CENTER) 
    instructionsBtn.place(relx=0.35, rely=0.6, anchor=CENTER)

def reselectImageArea():
    cv2.imshow('image', image)
    cv2.setMouseCallback('image', capture_event)

#Creation of window
gui = Tk()
gui.title('Screenshot-to-Text Translator')
gui.geometry('850x600')
center_window(gui)
#Label widgets
frontName = Label(gui, text= 'Screenshot-to-Text Translator',font=('helvetica',50,'bold'))
thankYou = Label(gui, text='Welcome and thank you using my program :)')
instructions = Label(gui, text='1. Screenshot your main monitors screen by pressing the "Screenshot" button.\n2. Click and drag your mouse from the top-left to the bottom-right of what you wish to translate.\n3. Recieve your translation!')
translationTitle = Label(gui, text='Translation from', font=('',35))
visibleTranslation = Label(gui, font=('',15))
translatedImageTk = Label(gui)
#Button widgets
screenShotBtn = Button(gui, text="Screenshot", command=imageCreation, font=('Helvetica', 35))
instructionsBtn = Button(gui, text="Instructions", command=loadInstructions, font=('Helvetica', 35))
backBtn = Button(gui,text='Back', command=back)
reselectAreaBtn = Button(gui,text='Reselect Area', command=reselectImageArea, font=('Helvetica', 35))

#puts starting widgets into window
back()
gui.mainloop()