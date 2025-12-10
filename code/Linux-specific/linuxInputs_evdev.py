# Hardware-level input simulation using evdev/uinput
# Works on both X11 and Wayland, appears as real hardware to Steam
# Requires: pip install evdev python-evdev

from time import sleep
from typing import Optional, Union
import os

try:
    import evdev
    from evdev import UInput, ecodes as e
except ImportError as exc:
    raise RuntimeError(
        "evdev is required for hardware-level input. Install with: pip install evdev"
    ) from exc


# Global virtual devices - initialized on first use
_keyboard_device = None
_mouse_device = None


def _init_keyboard():
    """Initialize virtual keyboard device."""
    global _keyboard_device
    if _keyboard_device is None:
        # Define capabilities for a keyboard
        cap = {
            e.EV_KEY: list(range(e.KEY_ESC, e.KEY_UNKNOWN)),
            e.EV_MSC: [e.MSC_SCAN],
        }
        _keyboard_device = UInput(cap, name='PolyAnalytics-Keyboard', version=0x3)
        sleep(0.1)  # Give udev time to process
    return _keyboard_device


def _init_mouse():
    """Initialize virtual mouse device."""
    global _mouse_device
    if _mouse_device is None:
        # Define capabilities for a mouse with absolute positioning
        cap = {
            e.EV_KEY: [e.BTN_LEFT, e.BTN_RIGHT, e.BTN_MIDDLE],
            e.EV_ABS: [
                (e.ABS_X, evdev.AbsInfo(0, 0, 65535, 0, 0, 0)),
                (e.ABS_Y, evdev.AbsInfo(0, 0, 65535, 0, 0, 0)),
            ],
            e.EV_REL: [e.REL_WHEEL, e.REL_HWHEEL],
        }
        _mouse_device = UInput(cap, name='PolyAnalytics-Mouse', version=0x3)
        sleep(0.1)
    return _mouse_device


# Minimal mapping of common macOS virtual key codes -> Linux keycodes
KEYCODE_MAP = {
    0x31: e.KEY_SPACE,
    0x24: e.KEY_ENTER,
    0x30: e.KEY_TAB,
    0x33: e.KEY_BACKSPACE,
    0x35: e.KEY_ESC,
    0x7B: e.KEY_LEFT,
    0x7C: e.KEY_RIGHT,
    0x7D: e.KEY_DOWN,
    0x7E: e.KEY_UP,
}

# String name mappings
KEY_NAMES = {
    'space': e.KEY_SPACE,
    'enter': e.KEY_ENTER,
    'return': e.KEY_ENTER,
    'tab': e.KEY_TAB,
    'esc': e.KEY_ESC,
    'escape': e.KEY_ESC,
    'backspace': e.KEY_BACKSPACE,
    'left': e.KEY_LEFT,
    'right': e.KEY_RIGHT,
    'up': e.KEY_UP,
    'down': e.KEY_DOWN,
}


def _char_to_keycode(char: str) -> tuple:
    """Convert single character to Linux keycode and shift flag."""
    # Simple ASCII mapping
    char_map = {
        'a': e.KEY_A, 'b': e.KEY_B, 'c': e.KEY_C, 'd': e.KEY_D, 'e': e.KEY_E,
        'f': e.KEY_F, 'g': e.KEY_G, 'h': e.KEY_H, 'i': e.KEY_I, 'j': e.KEY_J,
        'k': e.KEY_K, 'l': e.KEY_L, 'm': e.KEY_M, 'n': e.KEY_N, 'o': e.KEY_O,
        'p': e.KEY_P, 'q': e.KEY_Q, 'r': e.KEY_R, 's': e.KEY_S, 't': e.KEY_T,
        'u': e.KEY_U, 'v': e.KEY_V, 'w': e.KEY_W, 'x': e.KEY_X, 'y': e.KEY_Y,
        'z': e.KEY_Z,
        '0': e.KEY_0, '1': e.KEY_1, '2': e.KEY_2, '3': e.KEY_3, '4': e.KEY_4,
        '5': e.KEY_5, '6': e.KEY_6, '7': e.KEY_7, '8': e.KEY_8, '9': e.KEY_9,
    }
    
    lower = char.lower()
    needs_shift = char.isupper()
    
    if lower in char_map:
        return char_map[lower], needs_shift
    
    raise ValueError(f"Unsupported character: {char!r}")


def press_key(key_code: Union[int, str]) -> None:
    """
    Presses a key using hardware-level evdev injection.
    
    Accepts:
      - mac-like virtual key code as int (e.g., 0x31 for SPACE)
      - a single-character string (e.g., 'a', 'A')
      - a key name string (e.g., 'space', 'enter')
    """
    kbd = _init_keyboard()
    
    linux_keycode = None
    needs_shift = False
    
    if isinstance(key_code, int):
        linux_keycode = KEYCODE_MAP.get(key_code)
        if linux_keycode is None:
            raise ValueError(f"Unmapped mac keycode: 0x{key_code:X}")
    elif isinstance(key_code, str):
        if len(key_code) == 1:
            linux_keycode, needs_shift = _char_to_keycode(key_code)
        else:
            linux_keycode = KEY_NAMES.get(key_code.lower())
            if linux_keycode is None:
                raise ValueError(f"Unsupported key name: {key_code!r}")
    else:
        raise TypeError("key_code must be int or str")
    
    # Press shift if needed
    if needs_shift:
        kbd.write(e.EV_KEY, e.KEY_LEFTSHIFT, 1)
        kbd.syn()
    
    # Press and release key
    kbd.write(e.EV_KEY, linux_keycode, 1)  # Press
    kbd.syn()
    sleep(0.02)  # Brief hold
    kbd.write(e.EV_KEY, linux_keycode, 0)  # Release
    kbd.syn()
    
    # Release shift if used
    if needs_shift:
        kbd.write(e.EV_KEY, e.KEY_LEFTSHIFT, 0)
        kbd.syn()


def pause_game() -> None:
    """Presses the SPACEBAR briefly."""
    press_key(0x31)


# Screen size for coordinate conversion (adjust to your display)
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800


def _screen_to_abs(x: int, y: int) -> tuple:
    """Convert screen coordinates to absolute device coordinates (0-65535)."""
    abs_x = int((x / SCREEN_WIDTH) * 65535)
    abs_y = int((y / SCREEN_HEIGHT) * 65535)
    return abs_x, abs_y


def mouse_click_nominal(x: int, y: int) -> None:
    """Click left mouse button at screen coordinates (x, y)."""
    mouse = _init_mouse()
    
    abs_x, abs_y = _screen_to_abs(x, y)
    
    # Move to position
    mouse.write(e.EV_ABS, e.ABS_X, abs_x)
    mouse.write(e.EV_ABS, e.ABS_Y, abs_y)
    mouse.syn()
    sleep(0.05)
    
    # Click
    mouse.write(e.EV_KEY, e.BTN_LEFT, 1)
    mouse.syn()
    sleep(0.02)
    mouse.write(e.EV_KEY, e.BTN_LEFT, 0)
    mouse.syn()


def scroll(amount: int) -> None:
    """Scroll by amount (positive = down, negative = up)."""
    mouse = _init_mouse()
    # Invert to match mac behavior (positive = scroll down)
    mouse.write(e.EV_REL, e.REL_WHEEL, -int(amount))
    mouse.syn()


def mouse_diag_drag(x: int, y: int) -> None:
    """Drag mouse diagonally from (x,y) to bottom-right."""
    mouse = _init_mouse()
    
    # Move to start position
    abs_x, abs_y = _screen_to_abs(x, y)
    mouse.write(e.EV_ABS, e.ABS_X, abs_x)
    mouse.write(e.EV_ABS, e.ABS_Y, abs_y)
    mouse.syn()
    sleep(0.05)
    
    # Press button
    mouse.write(e.EV_KEY, e.BTN_LEFT, 1)
    mouse.syn()
    sleep(0.5)
    
    # Drag in increments
    for i in range(0, 300, 30):
        abs_x, abs_y = _screen_to_abs(x + 2 * i, y + i)
        mouse.write(e.EV_ABS, e.ABS_X, abs_x)
        mouse.write(e.EV_ABS, e.ABS_Y, abs_y)
        mouse.syn()
        sleep(0.1)
    
    # Final position and release
    abs_x, abs_y = _screen_to_abs(x + 400, y + 200)
    mouse.write(e.EV_ABS, e.ABS_X, abs_x)
    mouse.write(e.EV_ABS, e.ABS_Y, abs_y)
    mouse.syn()
    mouse.write(e.EV_KEY, e.BTN_LEFT, 0)
    mouse.syn()


def move_turn_bar() -> None:
    """Drag the turn bar from right to left."""
    mouse = _init_mouse()
    
    turn_bar_height = 128
    start_x = 790
    end_x = 90
    
    # Move to start
    abs_x, abs_y = _screen_to_abs(start_x, turn_bar_height)
    mouse.write(e.EV_ABS, e.ABS_X, abs_x)
    mouse.write(e.EV_ABS, e.ABS_Y, abs_y)
    mouse.syn()
    sleep(0.05)
    
    # Press
    mouse.write(e.EV_KEY, e.BTN_LEFT, 1)
    mouse.syn()
    sleep(0.5)
    
    # Drag left
    for i in range(0, 700, 140):
        abs_x, abs_y = _screen_to_abs(start_x - i, turn_bar_height)
        mouse.write(e.EV_ABS, e.ABS_X, abs_x)
        mouse.write(e.EV_ABS, e.ABS_Y, abs_y)
        mouse.syn()
        sleep(0.1)
    
    # Final position and release
    abs_x, abs_y = _screen_to_abs(end_x, turn_bar_height)
    mouse.write(e.EV_ABS, e.ABS_X, abs_x)
    mouse.write(e.EV_ABS, e.ABS_Y, abs_y)
    mouse.syn()
    mouse.write(e.EV_KEY, e.BTN_LEFT, 0)
    mouse.syn()


def cleanup():
    """Cleanup virtual devices."""
    global _keyboard_device, _mouse_device
    if _keyboard_device:
        _keyboard_device.close()
        _keyboard_device = None
    if _mouse_device:
        _mouse_device.close()
        _mouse_device = None


if __name__ == "__main__":
    import sys
    
    # Check permissions
    if not os.access('/dev/uinput', os.W_OK):
        print("ERROR: No write access to /dev/uinput")
        print("Run with sudo or add user to 'input' group:")
        print("  sudo usermod -a -G input $USER")
        print("  sudo chmod 660 /dev/uinput")
        sys.exit(1)
    
    try:
        print("Testing hardware-level input...")
        sleep(3)
        mouse_diag_drag(12, 4)
        sleep(6)
        move_turn_bar()
        print("Test complete!")
    finally:
        cleanup()
