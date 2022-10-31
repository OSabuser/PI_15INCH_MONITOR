import pydispmanx, pygame, time

# Create new layer object for GPU layer 1
demolayer = pydispmanx.dispmanxLayer(1)
# Create pyGame surface linked to the layer buffer
demoSurface = pygame.image.frombuffer(demolayer, demolayer.size, 'RGBA')

# Use exsisting pyGame features to draw to the surface
# Choosing red color for the rectangle
color = (255, 255, 0)

# Creating the image surface
image = pygame.image.load('pic_4.png')

# putting our image surface on display
# surface
demoSurface.blit(image, (650, 450))

# Trigger the redraw of the screen from the buffer
demolayer.updateLayer()

while True:
    print("Work flow!")
    print(f'Layer size:{demolayer.size}')
    time.sleep(0.5)
# Do other things, redraw layers etc

# Delete surface before layer
# del(demoSurface)
# Delete layer
# del(demolayer)
