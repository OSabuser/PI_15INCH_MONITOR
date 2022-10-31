import time
from PIL import Image, ImageDraw
from dispmanx import DispmanX


display = DispmanX(pixel_format="RGBA", buffer_type="auto")

image = Image.open('pic_4.png')
draw = ImageDraw.Draw(image)
display.update()

while True:
    print(f"Work state!")
    time.sleep(1.0)
