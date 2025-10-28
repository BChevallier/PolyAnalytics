import windowStuff as ws
from PIL import Image

def get_pixel_color(img: Image.Image, pos: tuple):
    """Return (R, G, B) tuple at a given (x, y) position."""
    return img.convert("RGB").getpixel(pos)

if __name__ == "__main__":
    coords=(10,10)
    img=ws.getWindowImg()
    img.save("Screenshot.png")
    get_pixel_color(img, coords)


