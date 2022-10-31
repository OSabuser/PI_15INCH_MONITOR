import time
from PIL import Image, ImageDraw, ImageShow
from dispmanx import DispmanX
import numpy

display = DispmanX(layer=33, pixel_format="RGBA", buffer_type="numpy")

image = Image.open('1.png')
draw = ImageDraw.Draw(image)
numpy.copyto(display.buffer, image)

display.update()

while True:
    print(f"Work state!")
    time.sleep(1.0)
