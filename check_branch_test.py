from threading import Timer
import keyboard
import time

def goto():
    count = 0
    while (count <=10):
        keyboard.press_and_release('ctrl+c')
        time.sleep(1)
        keyboard.press_and_release('alt+tab')
        time.sleep(1)
        keyboard.press_and_release('ctrl+g')
        time.sleep(1)
        keyboard.press_and_release('ctrl+v')
        time.sleep(1)
        keyboard.press_and_release('enter')
        time.sleep(3)
        keyboard.press_and_release('alt+tab')
        time.sleep(1)
        keyboard.press_and_release('down')
        time.sleep(1)
        count+=1

a = Timer(8.0, goto)
a.start()
