import pyautogui
import keyboard
import time

time.sleep(5)

while True:
    if keyboard.is_pressed("c"):
        print("停止しました")
        break

    pyautogui.press("tab")
    pyautogui.press("tab")
    pyautogui.press("space")
    # time.sleep(0.1)
