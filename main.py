import pydispmanx, pygame, time

floor_r_pos = (250, 284)
floor_l_pos = (100, 284)
icon_pos = (600, 284)

# Create new layer object for GPU layer 1
floor_l_layer = pydispmanx.dispmanxLayer(1)
floor_r_layer = pydispmanx.dispmanxLayer(2)
icon_layer = pydispmanx.dispmanxLayer(3)

# Create pyGame surfaces linked to the layer buffers
floor_l_surface = pygame.image.frombuffer(floor_l_layer, floor_l_layer.size, 'RGBA')
floor_r_surface = pygame.image.frombuffer(floor_r_layer, floor_r_layer.size, 'RGBA')
icon_surface = pygame.image.frombuffer(icon_layer, icon_layer.size, 'RGBA')

image = pygame.image.load('images/6.png')
floor_r_surface.blit(image, floor_r_pos)

image = pygame.image.load('images/9.png')
floor_l_surface.blit(image, floor_l_pos)

image = pygame.image.load('images/ARROW_UP.png')
icon_surface.blit(image, icon_pos)

# Trigger the redraw of the screen from the buffer
icon_layer.updateLayer()
floor_l_layer.updateLayer()
floor_r_layer.updateLayer()
while True:
    print("Work flow!")
    print(f'Layer size:{icon_layer.size}')
    time.sleep(0.5)
# Do other things, redraw layers etc

# Delete surface before layer
# del(demoSurface)
# Delete layer
# del(demolayer)
