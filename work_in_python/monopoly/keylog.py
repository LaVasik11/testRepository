from pynput import keyboard
import time

start = False
ctrl_pressed = False


def on_press(key):
    global start, ctrl_pressed

    if key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
        ctrl_pressed = True

    try:
        if key.char == 's' and ctrl_pressed:
            start = True
            return False
    except:
        pass


def on_release(key):
    global ctrl_pressed

    if key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
        ctrl_pressed = False


def wait_for_start():
    print("press Ctrl + S to start...")

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    while not start:
        time.sleep(0.05)

    listener.stop()