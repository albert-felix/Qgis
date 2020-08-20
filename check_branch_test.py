from threading import Timer
import keyboard
import time

def goto():
    count = 0
    while (count <=10):
        keyboard.press_and_release('ctrl+c')
        time.sleep(0.2)
        keyboard.press_and_release('alt+tab')
        time.sleep(0.2)
        keyboard.press_and_release('ctrl+g')
        time.sleep(0.3)
        keyboard.press_and_release('ctrl+v')
        time.sleep(0.2)
        keyboard.press_and_release('enter')
        #keyboard.wait('esc')
        time.sleep(3)
        keyboard.press_and_release('alt+tab')
        time.sleep(0.2)
        keyboard.press_and_release('down')
        time.sleep(0.2)
        count+=1

a = Timer(8.0, goto)
a.start()
