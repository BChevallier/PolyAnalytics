from MacOS_specific import windowStuff as ws
import imageProcessing as ip




if __name__ == "__main__":
    replay_id="0ad7b170-68d8-496e-3fea-08dd25c45c7b"
    win_id=ws.get_cgwindow_id("Polytopia")
    img=ws.getWindowImg(win_id)
    cimg=ip.test_pixel_coords(img, (378,333), 50,True)
    cimg.save("Box.png")





