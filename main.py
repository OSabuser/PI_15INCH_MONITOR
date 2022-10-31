import pydispmanx, pygame, time
# Create new layer object for GPU layer 1
demolayer = pydispmanx.dispmanxLayer(1)
# Create pyGame surface linked to the layer buffer
demoSurface = pygame.image.frombuffer(demolayer, demolayer.size, 'RGBA')

# Use exsisting pyGame features to draw to the surface
# Choosing red color for the rectangle
color = (255, 255, 0)

# Drawing Rectangle
pygame.draw.circle(demoSurface, (255,0,0), (int(demolayer.size[0]/2), int(demolayer.size[1]/2)), int(min(demolayer.size)/4), 0)

# Trigger the redraw of the screen from the buffer
demolayer.updateLayer()

while True:
    print("Work flow!")
    print(f'Layer size:{demolayer.size}')
    time.sleep(0.5)
# Do other things, redraw layers etc

# Delete surface before layer
#del(demoSurface)
# Delete layer
#del(demolayer)
