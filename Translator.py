import cv2
import pyautogui
import numpy
import time

firstX = 0
firstY = 0
lastX = 0
lastY = 0
choosingRectangle = False

topLeft = (firstX,firstY)
bottomRight = (lastX,lastY)
colorLine = (0,0,255)
lineThickness = 10

def capture_event(event,x,y,flags,params):
    global firstX,firstY,lastX,lastY, choosingRectangle, topLeft, bottomRight, colorLine, lineThickness
    if event == cv2.EVENT_LBUTTONDOWN:
        choosingRectangle = True
        firstX = x
        firstY = y
        print(x)
    
    elif event == cv2.EVENT_MOUSEMOVE and choosingRectangle:
        lastX = x
        lastY = y
        print(lastX)
        #for some reason i cant get the red rectangle to appear...
        imageCopy = image.copy()
        cv2.rectangle(imageCopy,
                      topLeft,
                      bottomRight,
                      colorLine,
                      lineThickness)
        cv2.imshow('image2', imageCopy)


    #takes new screenshot of contents within coordinates
    elif event == cv2.EVENT_LBUTTONUP:
        choosingRectangle = False
        
        print('dog')
        newImage = image[firstY:lastY, firstX:lastX]
        cv2.destroyAllWindows
        cv2.imshow('new',newImage)
    
image = pyautogui.screenshot()
image = numpy.array(image)
image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

cv2.imshow('image', image)
cv2.setMouseCallback('image', capture_event)

cv2.waitKey(0)
cv2.destroyAllWindows
