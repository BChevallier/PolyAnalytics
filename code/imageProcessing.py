

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