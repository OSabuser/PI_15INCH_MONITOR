import time
from PIL import Image, ImageDraw
from dispmanx import DispmanX


display = DispmanX(layer=1, pixel_format="RGBA", buffer_type="numpy")
display.width = 400
display.height = 400

image = Image.open('pic_4.png')
draw = ImageDraw.Draw(image)

while True:
    print(f"Work state!")
    display.update()
    time.sleep(1.0)
