import cv2
import pyautogui
import numpy
import time

firstX = 0
firstY = 0
lastX = 0
lastY = 0
choosingRectangle = False



colorLine = (0,0,255)
lineThickness = 10

def capture_event(event,x,y,flags,params):
    global firstX,firstY,lastX,lastY, choosingRectangle, colorLine, lineThickness
    #Finds top-left coordinate of chosen area
    if event == cv2.EVENT_LBUTTONDOWN:
        choosingRectangle = True
        if firstX == 0:
            firstX = x
            firstY = y
    
    elif event == cv2.EVENT_MOUSEMOVE and choosingRectangle:
        lastX = x
        lastY = y
        #Shows user where they are selecting part of the image
        imageCopy = image.copy()
        cv2.rectangle(imageCopy, (firstX,firstY), (lastX,lastY), colorLine, lineThickness)
        cv2.imshow('image', imageCopy)

    #takes screenshot of selected area
    elif event == cv2.EVENT_LBUTTONUP:
        choosingRectangle = False
        chosenImage = image[firstY:lastY, firstX:lastX]
        cv2.imshow('Chosen Image',chosenImage)
        
image = pyautogui.screenshot()
image = numpy.array(image)
image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

cv2.imshow('image', image)
cv2.setMouseCallback('image', capture_event)

cv2.waitKey(0)
cv2.destroyAllWindows
