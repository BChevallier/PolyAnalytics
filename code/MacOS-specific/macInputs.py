import AppKit
import Quartz

#presses a given key very briefly. The keycodes are Carbon/Quartz codes.
# Finding them online is messy
def press_key(key_code):
    event = Quartz.CGEventCreateKeyboardEvent(None, key_code, True)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)
    event = Quartz.CGEventCreateKeyboardEvent(None, key_code, False)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)
    return None

#presses the SPACEBAR very briefly.
def pause_game():
    #keycode 0x31 is SPACEBAR on US keyboard
    press_key(0x31)
    return None


def mouse_click_nominal(x, y):
    menu_bar_height = 28
    y+= menu_bar_height
    # Convert nominal y (top-left origin) to Quartz bottom-left origin
    tap_location = Quartz.kCGHIDEventTap
    left_mouse_button = Quartz.kCGMouseButtonLeft
    # Create and post mouse down event
    mouse_down = Quartz.CGEventCreateMouseEvent(
        None,
        Quartz.kCGEventLeftMouseDown,
        (x, y),
        left_mouse_button
    )
    Quartz.CGEventPost(tap_location, mouse_down)

    # Create and post mouse up event
    mouse_up = Quartz.CGEventCreateMouseEvent(
        None,
        Quartz.kCGEventLeftMouseUp,
        (x, y),
        left_mouse_button
    )
    Quartz.CGEventPost(tap_location, mouse_up)

if __name__=="__main__":
    print("Hello")