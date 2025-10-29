import windowStuff as ws
import startReplayOnSteam as startReplay
import time
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

if __name__ == "__main__":
    replay_id="0ad7b170-68d8-496e-3fea-08dd25c45c7b"
    ws.resize_window("Polytopia")
    win_id=ws.get_cgwindow_id("Polytopia")
    startReplay.open_replay(replay_id)
    pause_game()
    #keycode 0x13 is '2' key on US keyboard
    press_key(0x13)
    img=ws.getWindowImg(win_id)
    img.save("Screenshot.png")



