import pydispmanx, pygame
# Create new layer object for GPU layer 1
demolayer = pydispmanx.dispmanxLayer(1)
# Create pyGame surface linked to the layer buffer
demoSurface = pygame.image.frombuffer(demolayer, demolayer.size, 'RGBA')

# Use exsisting pyGame features to draw to the surface
# Choosing red color for the rectangle
color = (255, 255, 0)

# Drawing Rectangle
pygame.draw.rect(demoSurface, color,
                 pygame.Rect(30, 30, 60, 60))

# Trigger the redraw of the screen from the buffer
demolayer.updateLayer()

# Do other things, redraw layers etc

# Delete surface before layer
#del(demoSurface)
# Delete layer
#del(demolayer)
