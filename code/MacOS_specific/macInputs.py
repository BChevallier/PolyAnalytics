import AppKit
import Quartz
import time

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

#briefly presses mouse button at coordinates
#coordinates are given in x,y inside the standard polytopia window (800x500 starting at 0,0)
def mouse_click_nominal(x, y):
    menu_bar_height = 28
    y+= menu_bar_height +28
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


def scroll(amount):
    # amount: positive integer for zooming out
    tap_location = Quartz.kCGHIDEventTap
    # Create a scroll wheel event for vertical scrolling
    scroll_event = Quartz.CGEventCreateScrollWheelEvent(
        None,  # No source
        Quartz.kCGScrollEventUnitLine,  # Scroll in lines
        1,  # Number of wheels (vertical only)
        amount  # Scroll amount (positive for down)
    )
    # Post the scroll event
    Quartz.CGEventPost(tap_location, scroll_event)
    return None

if __name__=="__main__":
    ...