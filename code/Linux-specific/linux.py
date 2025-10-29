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
USE_VIRTUALGL = firefox_headless
STEAM_APPID = 874390 # app id for polytopia
STEAM_CMD ="steam"
def start_display():

    dis = Display(visible=0, size=(WIDTH, HEIGHT), color_depth=24)
    dis.start()

    os.environ.get["DISPLAY"] =dis.display
    return dis

p = subprocess.Popen(["firefox", "--no-remote", "--new-instance", "https://archlinux.org/"], env=os.environ)


time.sleep(20)
img = ImageGrap.grab()
img.save("firefox_headless.png")
print("It works now yay")

p.terminate()
display.stop()
