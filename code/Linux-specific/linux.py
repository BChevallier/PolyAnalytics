#here is the part i can have fun by myself yay
# use pyvirtualdisplay with Xvfb this is without gpu !!
#
# todo: test on ubuntu server
from pyvirtualdisplay import Display
import subprocess
import time
import os
from PIL import Image
import pyscreenshot as ImageGrap
# config:
WIDTH = 800
HEIGHT= 500
URL = "https://store.steampowered.com/"
OUTFILE = "firefox_headless.png"
STEAM_APPID = 874390 # app id for polytopia
STEAM_CMD ="steam"
def start_WM():
    return subprocess.Popen(["openbox"],         stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
        env=os.environ.copy(),)
def main():
    # Start a virtual X display (Xvfb). visible=False means headless.
    with Display(visible=False, size=(WIDTH, HEIGHT), color_depth=24) as disp:
        # pyvirtualdisplay sets DISPLAY in os.environ automatically
        print(f"DISPLAY set to {os.environ.get('DISPLAY')}")
        start_WM()

        # Launch Firefox into the virtual display
        #p = subprocess.Popen(
            #["firefox", "--no-remote", "--new-instance", URL],
            #env=os.environ
        #)
        p = subprocess.Popen(["steam"], env=os.environ


        )
        try:
            # Give Firefox time to start and render
            # First launch can take longer; adjust as needed
            time.sleep(40)

            # Take a screenshot of the root window
            # You can pass bbox=(0, 0, WIDTH, HEIGHT) if you want to constrain
            img = ImageGrap.grab()  # grabs from current DISPLAY
            img = img.crop((0, 0, WIDTH, HEIGHT))  # ensure exact size
            img.save(OUTFILE)
            print(f"Saved screenshot to {OUTFILE}")
        finally:
            # Terminate Firefox and wait briefly
            p.terminate()
            try:
                p.wait(timeout=5)
            except Exception:
                p.kill()

if __name__ == "__main__":
    main()
