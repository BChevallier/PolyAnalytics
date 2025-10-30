import sys
# Apple CoreGraphics bindings for window enumeration and capture
import Quartz.CoreGraphics as CG
from PIL import Image  # Pillow image support
import numpy as np      # NumPy for fast buffer manipulation
import pywinctl         # Cross-platform window control
import time             # Simple delays

# NOTE TO SELF:
# Mac-retina displays have a scaling factor of 2.0.
# Internally they tell every program, that they only have 1400x900.
# This is bullshit and they actually have 2800x1800.
# 1 logical pixel is = 2 actual pixels
# The following code accounts for it, so ignore it.
# The images output are scaled down their logical resolution.

# this script uses macOS-specific APIs and will not work on other platforms
def get_cgwindow_id(window_title_substring: str) -> int:
    """Return the CoreGraphics window ID for the first window whose title or
    owner name contains the given substring.  Exits the program if no match is found."""
    options = CG.kCGWindowListOptionOnScreenOnly | CG.kCGWindowListExcludeDesktopElements
    window_list = CG.CGWindowListCopyWindowInfo(options, CG.kCGNullWindowID)
    for window in window_list:
        title = window.get('kCGWindowName', '')
        owner_name = window.get('kCGWindowOwnerName', '')
        if window_title_substring in title or window_title_substring in owner_name:
            return window['kCGWindowNumber']
    print("Couldn't find window. Sorry :/")
    print(f"This is my window list: {window_list}")
    sys.exit()

def capture_window_by_id(window_id: int) -> Image.Image:
    """Render the specified window off-screen and return it as a Pillow Image."""
    image_ref = CG.CGWindowListCreateImage(
        CG.CGRectNull,
        CG.kCGWindowListOptionIncludingWindow,
        window_id,
        CG.kCGWindowImageBoundsIgnoreFraming | CG.kCGWindowImageNominalResolution
    )
    if image_ref is None:
        raise RuntimeError("Failed to capture window image")

    width = CG.CGImageGetWidth(image_ref)
    height = CG.CGImageGetHeight(image_ref)
    bpr = CG.CGImageGetBytesPerRow(image_ref)
    data_provider = CG.CGImageGetDataProvider(image_ref)
    data = CG.CGDataProviderCopyData(data_provider)
    arr = np.frombuffer(data, dtype=np.uint8)
    arr.shape = (height, bpr // 4, 4)
    # Convert BGRA to RGBA
    arr = arr[..., [2, 1, 0, 3]]
    return Image.fromarray(arr)

def resize_window(window_title_substring: str, new_width: int=800, new_height: int=500,
                  bringToFront: bool = True):
    """Find the first window containing the substring, resize it, optionally bring it to
    the front, and move it to the top-left corner. Returns the window object."""
    all_windows = pywinctl.getAllWindows()
    window = None
    for w in all_windows:
        if window_title_substring in w.title:
            window = w
            break
    if window is None:
        print(f"Couldn't find window in the following list: {all_windows}")
        sys.exit()

    window.resizeTo(new_width, new_height)
    if bringToFront:
        window.activate()
    window.moveTo(0, 0)
    time.sleep(0.5)
    return window

def getWindowImg(cg_window_id, size=(800, 500),
                 top_border_adjust: int = 28, bring_to_front: bool = True) -> Image.Image:
    """Does not resize the named window, capture it as a Pillow image, and crop off the title bar.
    ``topBorderAdjust`` is the height to remove from the top."""
    width, body_height = size
    height = top_border_adjust + body_height
    img = capture_window_by_id(cg_window_id)
    # Crop off the title bar
    box = (0, top_border_adjust, width, height)
    return img.crop(box)



#DON'T USE
#ONLY EFFICIENT FOR VERY SMALL AMOUNTS OF PIXELS
def get_single_pixel_color(window_id: int, x: int, y: int, top_border: int = 28) -> tuple:
    """Return the RGBA colour of the pixel at (x, y) inside the specified window,
    compensating for a title bar of height ``top_border``."""
    global_x = x
    global_y = y + top_border
    # Capture only a 1×1 region rather than the whole window [oai_citation:0‡gist.githubusercontent.com](https://gist.githubusercontent.com/mr-linch/d31024f931441a39c6a830328f8b5030/raw/0853a1f99ff68bc74f8599772982c9c3edeeab39/capture_darwin.py#:~:text=image%20%3D%20CG,CG.kCGWindowImageNominalResolution%2C)
    region = CG.CGRectMake(global_x, global_y, 1, 1)
    image_ref = CG.CGWindowListCreateImage(
        region,
        CG.kCGWindowListOptionIncludingWindow,
        window_id,
        CG.kCGWindowImageBoundsIgnoreFraming | CG.kCGWindowImageNominalResolution,
    )
    if not image_ref:
        raise RuntimeError("Failed to capture pixel")
    bpr = CG.CGImageGetBytesPerRow(image_ref)
    data = CG.CGDataProviderCopyData(CG.CGImageGetDataProvider(image_ref))
    arr = np.frombuffer(data, dtype=np.uint8)
    arr.shape = (1, bpr // 4, 4)
    b, g, r, a = arr[0, 0]
    return (int(r), int(g), int(b))
