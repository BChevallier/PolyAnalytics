import pyautogui
import time
from pynput import keyboard

color_detection_on = False  # Boolean to toggle color detection
delay = 0
boxsize = 20
output_in_hex = False   # If True output hex color, if False output RGB tuple
screenshot_enabled = False  # Toggle to enable/disable saving screenshots

def rgb_to_hex(r, g, b):
    return '#{:02X}{:02X}{:02X}'.format(r, g, b)

def detect_color_at_cursor():
    x, y = pyautogui.position()
    x = round(x)
    y = round(y)
    if color_detection_on:
        time.sleep(delay)  # Delay to move cursor away

        left = int(max(x - boxsize // 2, 0))
        top = int(max(y - boxsize // 2, 0))

        screenshot = pyautogui.screenshot(region=(left, top, boxsize, boxsize))
        center_x = boxsize // 2
        center_y = boxsize // 2
        color = screenshot.getpixel((center_x, center_y))[:3]  # Ignore alpha if present

        if output_in_hex:
            color_output = rgb_to_hex(*color)
        else:
            color_output = color

        if screenshot_enabled:
            screenshot.save(f"screenshot_{color_output}.png")
            print(f"Screenshot of {boxsize}x{boxsize} area around ({x}, {y}) saved as screenshot_{color_output}.png")

        print(f"Color at cursor ({x}, {y}): {color_output}")

        # Explicitly delete image and collect garbage to free memory
        del screenshot
    else:
        print("Color detection off!")

def on_press(key):
    global color_detection_on
    try:
        if key == keyboard.Key.space:
            color_detection_on = not color_detection_on
            state = "ON" if color_detection_on else "OFF"
            print(f"Color detection toggled {state}")
        elif key.char == 's':  # Trigger detection on pressing s
            detect_color_at_cursor()
    except AttributeError:
        pass

if __name__ == "__main__":
    with keyboard.Listener(on_press=on_press) as keyboard_listener:
        keyboard_listener.join()
