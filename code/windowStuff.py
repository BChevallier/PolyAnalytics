import sys
import Quartz.CoreGraphics as CG
from PIL import Image
import numpy as np
import pywinctl
import time

#this stuff probably only works on MacOS

def get_cgwindow_id(window_title_substring):
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


def capture_window_by_id(window_id):
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

    # Remove deprecated mode parameter
    img = Image.fromarray(arr)
    return img
    #img.save("pywinctl_window_capture.png")



def resize_window(window_title_substring, new_width, new_height):
    # Use pywinctl to find the window and resize it
    all = pywinctl.getAllWindows()
    print(all)
    #windows=[i.title if window_title_substring in i.title else ... for i in all]
    for i in all:
        if window_title_substring in i.title:
            window=i
            break
    else:
        print(f"Couldn't find window in the following list: {all}")
        sys.exit()

    # Resize window
    window.resizeTo(new_width, new_height)
    # Optional: Bring window to front for clean capture
    # Pause shortly to let the OS apply the resize before capture
    time.sleep(0.5)
    return window


