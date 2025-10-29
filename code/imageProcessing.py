

#returns the cropped out info about maptype and mapsize in a tuple.
#iput has to be 800x500 PIL Image object.
def get_menu_info(image):
    #cropbox for mapsize
    size_box = (330, 122, 360, 136)
    #cropbox for maptype
    type_box= (315, 152, 375, 165)
    size_img=image.crop(size_box)
    type_img=image.crop(type_box)
    return (size_img, type_img)

