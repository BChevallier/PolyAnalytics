#here all keyboard inputs should be mapped the same as mac
# use pynput library
#
# Notes:
# - This uses pynput to synthesize keyboard and mouse events.
# - Coordinates are assumed to be screen (top-left origin). If you work inside a specific window

from time import sleep
from typing import Optional, Union

try:
    from pynput.keyboard import Controller as KeyboardController, Key
    from pynput.mouse import Controller as MouseController, Button
except Exception as e:
    raise RuntimeError(
        "pynput is required for linuxInputs.py. Install with: pip install pynput"
    ) from e


_keyboard = KeyboardController()
_mouse = MouseController()

# Minimal mapping of common macOS virtual key codes -> pynput Keys.
# This lets press_key(int) behave similarly to the mac implementation (which uses Quartz keycodes).
KEYCODE_MAP = {
    0x31: Key.space,       # SPACE
    0x24: Key.enter,       # RETURN
    0x30: Key.tab,         # TAB
    0x33: Key.backspace,   # DELETE (backspace)
    0x35: Key.esc,         # ESC
    0x7B: Key.left,        # Arrow Left
    0x7C: Key.right,       # Arrow Right
    0x7D: Key.down,        # Arrow Down
    0x7E: Key.up,          # Arrow Up
    # Add more if you rely on specific mac virtual key codes
}

def _press_and_release(key: Union[Key, str]) -> None:
    """Helper to press and release a key using pynput."""
    _keyboard.press(key)
    _keyboard.release(key)

def press_key(key_code: Union[int, str, Key]) -> None:
    """
    Presses a given key very briefly.

    Accepts:
      - mac-like virtual key code as int (e.g., 0x31 for SPACE),
      - a single-character string (e.g., 'a'),
      - a pynput.keyboard.Key (e.g., Key.space).

    Returns: None
    """
    key_obj: Optional[Union[Key, str]] = None

    if isinstance(key_code, int):
        key_obj = KEYCODE_MAP.get(key_code, None)
        if key_obj is None:
            # Fallback: if you pass an unmapped mac keycode, we cannot safely infer the character.
            # You can extend KEYCODE_MAP above as needed.
            raise ValueError(
                f"Unmapped mac keycode: 0x{key_code:X}. Extend KEYCODE_MAP for this key."
            )
    elif isinstance(key_code, Key):
        key_obj = key_code
    elif isinstance(key_code, str):
        if len(key_code) == 1:
            key_obj = key_code
        else:
            # Allow names like "space", "enter" as convenience
            named = {
                "space": Key.space,
                "enter": Key.enter,
                "return": Key.enter,
                "tab": Key.tab,
                "esc": Key.esc,
                "escape": Key.esc,
                "backspace": Key.backspace,
                "left": Key.left,
                "right": Key.right,
                "up": Key.up,
                "down": Key.down,
            }
            key_obj = named.get(key_code.lower())
            if key_obj is None:
                raise ValueError(f"Unsupported key name string: {key_code!r}")
    else:
        raise TypeError("key_code must be int (mac keycode), str (char/name) or pynput Key")

    _press_and_release(key_obj)

def pause_game() -> None:
    """Presses the SPACEBAR briefly (matches macInputs behavior using keycode 0x31)."""
    press_key(0x31)

def _move_mouse_abs(x: int, y: int) -> None:
    """Move mouse to absolute screen coordinates (with optional window offset)."""
    _mouse.position = (x , y)

def mouse_click_nominal(x: int, y: int) -> None:
    """
    Briefly presses the left mouse button at coordinates (x, y).

    Coordinates are assumed to be nominal top-left origin (screen space).
    """
    _move_mouse_abs(x, y)
    _mouse.press(Button.left)
    _mouse.release(Button.left)

def scroll(amount: int) -> None:
    """
    Scroll by 'amount'.

    Note:
    - In macInputs a positive amount was used for "zooming out" (scroll down).
    - In pynput on Linux, scroll(dx, dy) uses dy>0 for scroll UP. To keep the same semantics,
      we invert the sign so that positive 'amount' scrolls DOWN.
    """
    _mouse.scroll(0, -int(amount))

def mouse_diag_drag(x: int, y: int) -> None:
    """
    Drag the mouse diagonally to the bottom-right in small increments
    (mirrors macInputs logic: steps of ~30, with short sleeps).
    """
    # Start press
    _move_mouse_abs(x, y)
    _mouse.press(Button.left)
    sleep(0.5)

    for i in range(0, 300, 30):
        _move_mouse_abs(x + 2 * i, y + i)
        # small dwell to emulate realistic drag
        sleep(0.1)

    # Release at the final point
    _move_mouse_abs(x + 400, y + 200)
    _mouse.release(Button.left)

def move_turn_bar() -> None:
    """
    Emulates the macInputs.move_turn_bar behavior:
    - Press at (790, 128) then drag leftwards in chunks to (90, 128) and release.
    """
    turn_bar_height = 128
    start_x = 790
    end_x = 90

    _move_mouse_abs(start_x, turn_bar_height)
    _mouse.press(Button.left)
    sleep(0.5)

    # Move left in steps (matching mac's loop: 0..700 step 140)
    for i in range(0, 700, 140):
        _move_mouse_abs(start_x - i, turn_bar_height)
        sleep(0.1)

    _move_mouse_abs(end_x, turn_bar_height)
    _mouse.release(Button.left)

if __name__ == "__main__":
    # Small test: wait a few seconds, then attempt to move the "turn bar"
    sleep(6)
    move_turn_bar()
