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

#start Xvfb virtual display :)
display = Display(visible=0, size=(800, 500), color_depth=24)
display.start()

disp = os.environ.get("DISPLAY")
print(disp)

p = subprocess.Popen(["firefox", "--no-remote", "--new-instance", "https://archlinux.org/"], env=os.environ)


time.sleep(20)
img = ImageGrap.grab()
img.save("firefox_headless.png")
#currently this prints out a blackscreen
print("It works now yay")

p.terminate()
display.stop()
