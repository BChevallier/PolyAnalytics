import colorProcessing as cp
import numpy as np
from PIL import ImageOps, Image
import pytesseract
from MacOS_specific import startReplayOnSteam
from MacOS_specific import windowStuff as ws
from MacOS_specific import macInputs as inp
import time
import random

#function to binarize image.
#DOESN'T WORK
def binarize(img, threshold=100):
    #using point is quicker than iterating over every pixel coordinate
    return img.point(lambda p: 255 if p > threshold else 0)

#upscales PIL by a certain factor. Only helps some of the time
def upscale_image(img, factor=2):
    new_width = img.width * factor
    new_height = img.height * factor
    # Resize (upscale) the image
    upscaled_img = img.resize((new_width, new_height), Image.LANCZOS)
    return upscaled_img

# A sloppy attempt to fix ocr artifacts.
# Will return None if it doesn't manage to.
def clean_size_string(size):
    possible_sizes = {"121", "196", "256", "324", "400", "900"}
    for _ in range(3):
        if size in possible_sizes:
            return size
        elif "9" in size and len(size)>3:
            size=size.replace("9","")
        elif "9" in size:
            size=size.replace("9","2")
    return None

# A sloppy attempt to fix ocr artifacts.
# Will return None if it doesn't manage to.
def clean_type_string(type):
    possible_types={"Continents", "Lakes", "Archipelago", "Water World", "Dryland", "Pangea"}
    if type in possible_types:
        return type
    else:
        for p_type in possible_types:
            if p_type in type:
                return p_type
        return None


#returns the cropped out info about maptype and mapsize in a tuple.
#iput has to be 800x500 PIL Image object.
def get_menu_info(image):
    #cropbox for mapsize
    size_box = (330, 122, 360, 136)
    #cropbox for maptype
    type_box= (315, 152, 375, 165)
    #cropped images
    size_img=image.crop(size_box)
    type_img=image.crop(type_box)
    #greyscale images
    gray_size_img = ImageOps.grayscale(size_img)
    gray_type_img = ImageOps.grayscale(type_img)
    #invert image
    # (Works better because pytesseract was trained on black text on white mostly)
    inv_size_img=ImageOps.invert(gray_size_img)
    inv_type_img = ImageOps.invert(gray_type_img)
    # Upscale because apparently this helps
    up_size_img=upscale_image(inv_size_img)
    #up_type_img=upscale_image(inv_type_img)
    #get string and post process it
    config = '--psm 7 -c tessedit_char_whitelist=0123456789'
    size=pytesseract.image_to_string(up_size_img, config=config)
    clean_size = clean_size_string(size.replace('\n', '').strip())

    config = r'--psm 7 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    type=pytesseract.image_to_string(inv_type_img)
    clean_type = clean_type_string(type.replace('\n', '').strip())
    return (clean_size, clean_type)

#function that crops out the economic info of a replay frame.
#returns tuple with cropped images for current star count, and current revenue
def get_eco_info(image):
    cur_box=(407, 23, 437, 38)
    rev_box =(412,9,435,21)
    #cropped images
    cur_img=image.crop(cur_box)
    rev_img=image.crop(rev_box)
    #greyscale
    rev_img=ImageOps.grayscale(rev_img)
    cur_img = ImageOps.grayscale(cur_img)
    return (rev_img,cur_img)

#function to test where some coords are on an image.
#will output cropped image around specified location
#and with specified size(default=50). Pixel at given
#coordinate will be painted pink
def test_pixel_coords(img,coords, squareSize=50, show_color=False):
    hw=squareSize//2
    image=img.copy()
    if show_color:
        print(image.getpixel(coords))
    image.putpixel(coords,(255,0,255))
    box=(coords[0]-hw,coords[1]-hw,coords[0]+hw,coords[1]+hw)
    return image.crop(box)

#Looks at the exit button in a frame.
#If the button is green the game ended and it will return True.
#Else False.
def check_for_end(img):
    color=img.getpixel((740,430))
    if cp.check_if_complete(color):
        return True
    else: return False

tech_locations=np.array([
    (403, 204),
    (393, 171),
    (383, 138),
    (430, 184),
    (458, 164),
    (425, 236),
    (453, 217),
    (481, 197),
    (453, 257),
    (480, 278),
    (400, 269),
    (428, 289),
    (456, 310),
    (390, 301),
    (378, 333),
    (362, 255),
    (352, 288),
    (340, 320),
    (329, 256),
    (295, 255),
    (363, 215),
    (329, 215),
    (295, 215),
    (353, 183),
    (343, 150)
])

#uses pixel colors to get tech progression identifier out of image. A nightmare...
def get_techs(img):
    tech_progress =0
    for i,coords in enumerate(tech_locations):
        color=img.getpixel(coords)[:3]
        if cp.check_if_complete(color):
            if i % 5 == 0: tech_progress+=11* 100 ** (4-i//5)
            elif i % 5 == 1: tech_progress+= 2 * 100 ** (4-i//5) * 10
            elif i % 5 == 2: tech_progress+= 4 * 100 ** (4-i//5) * 10
            elif i % 5 == 3: tech_progress+= 2 * 100 ** (4-i//5)
            elif i % 5 == 4: tech_progress+= 4 * 100 ** (4-i//5)
        else: ...
    tech_progress=str(tech_progress)
    tech_progress="0"*(10-len(tech_progress))+tech_progress
    return tech_progress

tech2tribe = {
    "0000110000": {"Tr1"},
    "0011000000": {"Tr2"},
    "0000000011": {"Tr3","Tr14"},
    "1100000000": {"Tr4"},
    "0000001100": {"Tr5","Tr15"},
    "0000000020": {"Tr6"},
    "0000000000": {"Tr7","Tr13"},
    "0000400000": {"Tr8"},
    "0020000000": {"Tr9","Tr16"},
    "0000020000": {"Tr10"},
    "0002000000": {"Tr11"},
    "2000000000": {"Tr12"},
}

#returns Tribe corresponding to starting tech config. Can return None.
def tribe_from_tech(tech):
    global tech2tribe
    if tech in tech2tribe:
        return tech2tribe[tech]
    else:
        return {}

def get_color_from_coords(img, coords):
    """Return a list of pixel values from ``img`` at each (x, y) in ``coords``."""
    color_list = []
    for x, y in coords:
        color_list.append(img.getpixel((x, y))[:3])
    return color_list

if __name__ == "__main__":
    #startReplayOnSteam.open_replay("bb363954-782c-4c5d-40c9-08dd25c45c7b")
    time.sleep(4)
    inp.pause_game()
    for iter in range(60,70):
        time.sleep(random.randint(13, 22))
        inp.pause_game()
        print("Pause!")
        inp.mouse_diag_drag(120,120)
        time.sleep(1)
        id=ws.get_cgwindow_id("Polytopia")
        frame=ws.getWindowImg(id)
        revenue_img, current_stars_img = get_eco_info(frame)
        revenue_img.save(f"OCR_training_data/revenue{iter}.png")
        current_stars_img.save(f"OCR_training_data/currentEco{iter}.png")
        print(f"Image {iter} saved! Start again")
        time.sleep(2)
        inp.pause_game()
