
from pynput.mouse import Controller
from pynput import mouse
from pynput import keyboard
import threading
import cv2
import pyautogui



key_held = False


#finds initial cursor position,
def on_press(key):
    global key_held, initialX, initialY
    
    if key.char == '-' and key_held == False:
        moving  = Controller()
        position = moving.position
        initialX = position[0]
        initialY = position[1]
        print('pressed')
        print(initialX)
        print(initialY)
        key_held = True

#Determines final position of cursor
def on_release(key):
    global key_held
    #if key_held == True:
    moving = Controller()
    position = moving.position
    lastX = position[0]
    lastY = position[1]
    print(lastX)
    print(lastY)
    key_held = False

#determines position of cursor movement, allowing changing box
def on_move(x,y):
    global initialX, initialY
    moving = Controller()
    position = moving.position
    print(position)


   # image =  cv2.rectangle(image, (initialX,initialY), (x,y), color=(0,255,0))
    #cv2.imshow(image)


def start_listeners():
    # Start the keyboard listener
    keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    keyboard_thread = threading.Thread(target=keyboard_listener.start)
    keyboard_thread.start()

    # Start the mouse listener
    mouse_listener = mouse.Listener(on_move=on_move)
    mouse_thread = threading.Thread(target=mouse_listener.start)
    mouse_thread.start()

    # Join threads to keep them running
    keyboard_thread.join()
    mouse_thread.join()

if __name__ == "__main__":
    start_listeners()
    

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

with mouse.Listener(on_move=on_move) as listener:
    listener.join()

