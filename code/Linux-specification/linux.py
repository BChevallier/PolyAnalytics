#here is the part i can have fun by myself yay
# use pyvirtualdisplay with Xvfb this is without gpu !!
#
# todo: test on ubuntu server
from pyvirtualdisplay import display
import subprocess
import time
import os
from PIL import Image

#start Xvfb virtual display :)
display = Display(visible=0, size=(800, 500), color_depth=24)
display.start()


p = subprocess.Popen(["firefox", "--no-remote", "--new-instance", "https://archlinux.org/"], env=os.environ)


time.sleep(6)
img = ImageGrap.grab()
im.save("firefox_headless.png")
print("It works now yay")

p.terminate()
display.stop()
