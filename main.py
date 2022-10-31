import pydispmanx, pygame, time

# Create new layer object for GPU layer 1
floor_layer = pydispmanx.dispmanxLayer(1)
icon_layer = pydispmanx.dispmanxLayer(1)

# Create pyGame surfaces linked to the layer buffers
floor_surface = pygame.image.frombuffer(floor_layer, floor_layer.size, 'RGBA')
icon_surface = pygame.image.frombuffer(icon_layer, icon_layer.size, 'RGBA')

# Creating the image surface
image = pygame.image.load('1.png')
floor_surface.blit(image, (550, 150))

# putting our image surface on display
# surface
image = pygame.image.load('8.png')
icon_surface.blit(image, (100, 150))

# Trigger the redraw of the screen from the buffer
icon_layer.updateLayer()
floor_layer.updateLayer()

while True:
    print("Work flow!")
    print(f'Layer size:{icon_layer.size}')
    time.sleep(0.5)
# Do other things, redraw layers etc

# Delete surface before layer
# del(demoSurface)
# Delete layer
# del(demolayer)
