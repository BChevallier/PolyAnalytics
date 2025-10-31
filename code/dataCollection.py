from MacOS_specific import windowStuff as ws
import imageProcessing as ipro
from MacOS_specific import startReplayOnSteam
import colorProcessing as cpro
import datahandling
from MacOS_specific import macInputs as inp
import time
import pandas as pd
import numpy as np
import sys


if __name__ == "__main__":
    win_id=ws.get_cgwindow_id("Polytopia")
    window = ws.resize_window("Polytopia")
    for i in range(10):
        columns=["mType","mSize","TribeA","TribeB","1v1","Winner"]
        batch=datahandling.takebatch(i)
        #batch=["0ad7b170-68d8-496e-3fea-08dd25c45c7b"]
        df=pd.DataFrame(index=batch, columns=columns)
        for id in batch:
            startReplayOnSteam.open_replay(id) #start replay
            window.activate(win_id) #activate Polytopia window
            time.sleep(0.8) #wait for replay to launch
            inp.pause_game()
            inp.mouse_diag_drag(120,120) #move camera to avoid messy background

            inp.mouse_click_nominal(640,430) #open menu
            time.sleep(1.5) #very important
            frame=ws.getWindowImg(win_id) #screenshot
            mSize, mType = ipro.get_menu_info(frame) #extract maptype and mapsize
            df.at[id, "mSize"] = mSize
            df.at[id, "mType"] = mType
            inp.press_key(53)#escape menu

            #see player 1
            for Player in ["A","B"]:
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
                else:
                    df.at[id, f"Tribe{Player}"] = np.nan
                inp.press_key(53) #press escape
                time.sleep(0.2)

            inp.press_key(20)#press 3 to see if more than 2 player
            time.sleep(0.3)
            frame = ws.getWindowImg(win_id)
            if ipro.get_color_from_coords(frame,[(9,33)])[0]==player_color:
                df.at[id, "1v1"] = True
            else:
                df.at[id, "1v1"] = False
            if df.loc[id].iloc[:4].isnull().all(): sys.exit()
            time.sleep(30)

            if df.at[id,"1v1"]==True:
                ...#get winner when function is implemented
        df.to_csv(f"collected_data/Batch{i}.csv")
        print(df)

















