import imageProcessing as ipro
import colorProcessing as cpro
import dataHandling
import time
import pandas as pd
import numpy as np
import sys
import os
#check for the os you run the code on:
if platform.system() == 'Linux'
    from  Linux_specific import linux
    from Linux_specific import linuxInputs as inp
elif platform.system() == 'Darwin'
    from MacOS_specific import windowStuff as ws
    from MacOS_specific import startReplayOnSteam
    from MacOS_specific import macInputs as inp
    mac = True
else:
    raise Exception("something went wrong, because your os is not recognized properly")
if __name__ == "__main__":
    win_id=ws.get_cgwindow_id("Polytopia")
    window = ws.resize_window("Polytopia")
    for i in range(1,2):
        columns=["mType","mSize","TribeA","TribeB","1v1","Winner"]
        batch=dataHandling.takebatch(i)
        #batch=["0ad7b170-68d8-496e-3fea-08dd25c45c7b"]
        df=pd.DataFrame(index=batch, columns=columns)
        for id in batch:
            startReplayOnSteam.open_replay(id) #start replay
            window.activate(win_id) #activate Polytopia window
            time.sleep(0.8) #wait for replay to launch
            inp.pause_game()
            inp.mouse_diag_drag(120,120) #move camera to avoid messy background

            print("Getting menu infos")
            inp.mouse_click_nominal(640,430) #open menu
            time.sleep(1.5) #very important
            frame=ws.getWindowImg(win_id) #screenshot
            mSize, mType = ipro.get_menu_info(frame) #extract maptype and mapsize
            df.at[id, "mSize"] = mSize
            df.at[id, "mType"] = mType
            inp.press_key(53)#escape menu

            #identify Tribes
            for Player in ["A","B"]:
                print(f"Identifying tribe of Player {Player}")
                inp.press_key(18 if Player=="A" else 19) #press 1 or 2
                time.sleep(0.1)
                frame = ws.getWindowImg(win_id)
                player_color=ipro.get_color_from_coords(frame,[(9,33)])[0] #[0] important because it returns a list
                tribe_by_color=cpro.identify_tribe(player_color)

                inp.mouse_click_nominal(700,430) #open tech tree
                time.sleep(0.1)
                inp.scroll(-50) #zoom out
                time.sleep(0.2)
                frame = ws.getWindowImg(win_id) #screenshot
                starting_tech=ipro.get_techs(frame) #get starting techs
                tribes_by_techs=ipro.tribe_from_tech(starting_tech) #get tribe corresponding to those techs

                if tribe_by_color in tribes_by_techs:
                    df.at[id, f"Tribe{Player}"] = tribe_by_color
                    print(f"Player {Player} has color: {player_color}")
                else:
                    df.at[id, f"Tribe{Player}"] = np.nan
                inp.press_key(53) #press escape
                time.sleep(0.2)
            inp.press_key(20)#press 3 to see if there is a third player
            time.sleep(0.2)
            frame = ws.getWindowImg(win_id)
            if ipro.get_color_from_coords(frame,[(9,33)])[0]==player_color:
                df.at[id, "1v1"] = True
            else:
                df.at[id, "1v1"] = False
            if df.loc[id].iloc[:4].isnull().all(): sys.exit(f"Got for None values in a row at id{id}")
            #winner detection for 1v1 games
            if df.at[id,"1v1"]==True:
                inp.press_key(29)
                counter=0
                is_at_end = False
                print("Scrolling to the end")
                while not is_at_end: #scroll to the end
                    counter+=1
                    inp.move_turn_bar()
                    time.sleep(0.5)
                    frame=ws.getWindowImg(win_id)
                    is_at_end=ipro.check_for_end(frame)
                    time.sleep(0.5)
                    if counter==40: sys.exit("Scrolled 40 times without finding the end")
                color_at_end=ipro.get_color_from_coords(frame, [(9,33)])[:3][0]
                print(f"Color at end is:{color_at_end}")
                if color_at_end == player_color:
                    df.at[id,"Winner"]="B"
                else:
                    print(f"Seen color: {ipro.get_color_from_coords(frame, [(740,430)])[:3]}")
                    print(f"Saved Color for Player B: {player_color}")
                    df.at[id, "Winner"]="A"
            time.sleep(8)
        df.to_csv(f"collected_data/Batch{i}.csv")
        print(df)
