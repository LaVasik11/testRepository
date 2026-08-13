import keyboard
from pynput.mouse import Controller

mouse = Controller()

def print_mouse_position():
    x, y = mouse.position
    print(f"Mouse position: {x}, {y}")

keyboard.add_hotkey('ctrl+shift+]', print_mouse_position)

print("Нажмите Ctrl+Shift+] для вывода координат мыши. Esc для выхода.")
keyboard.wait('esc')

