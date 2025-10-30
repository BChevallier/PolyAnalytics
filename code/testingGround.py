from MacOS_specific import windowStuff as ws
import imageProcessing as ip
import pytesseract

if __name__ == "__main__":
    replay_id="0ad7b170-68d8-496e-3fea-08dd25c45c7b"
    #ws.resize_window("Polytopia")
    win_id=ws.get_cgwindow_id("Polytopia")
    img=ws.getWindowImg(win_id)
    rev, cur=ip.get_eco_info(img)
    print(rev)
    print(cur)





