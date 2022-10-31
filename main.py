import pydispmanx, pygame, time

floor_r_pos = (250, 284)
floor_l_pos = (100, 284)
icon_pos = (600, 284)
allowable_floor_range = (1, 40)

# Create new layer object for GPU layer 1
floor_l_layer = pydispmanx.dispmanxLayer(1)
floor_r_layer = pydispmanx.dispmanxLayer(2)
icon_layer = pydispmanx.dispmanxLayer(3)

# Create pyGame surfaces linked to the layer buffers
floor_l_surface = pygame.image.frombuffer(floor_l_layer, floor_l_layer.size, 'RGBA')
floor_r_surface = pygame.image.frombuffer(floor_r_layer, floor_r_layer.size, 'RGBA')
icon_surface = pygame.image.frombuffer(icon_layer, icon_layer.size, 'RGBA')

def update_floor_img(state):
    global floor_l_surface, floor_r_surface, floor_l_layer, floor_r_layer
    if state[0] is not state[1]:  # Draw floor number

        del floor_l_surface
        del floor_r_surface
        del floor_l_layer
        del floor_r_layer

        floor_l_layer = pydispmanx.dispmanxLayer(1)
        floor_r_layer = pydispmanx.dispmanxLayer(2)
        floor_l_surface = pygame.image.frombuffer(floor_l_layer, floor_l_layer.size, 'RGBA')
        floor_r_surface = pygame.image.frombuffer(floor_r_layer, floor_r_layer.size, 'RGBA')


        if state[0] < 10:
            image = pygame.image.load(f'images/{state[0]}.png')
            floor_r_surface.blit(image, floor_r_pos)
        elif state[0] < allowable_floor_range[1] + 1:
            image = pygame.image.load(f'images/{state[0] % 10}.png')
            floor_r_surface.blit(image, floor_r_pos)
            image = pygame.image.load(f'images/{state[0] // 10}.png')
            floor_l_surface.blit(image, floor_l_pos)

        # Trigger the redraw of the screen from the buffer
        floor_l_layer.updateLayer()
        floor_r_layer.updateLayer()

    return state[0]


def update_mode_img(state):
    if state[0] is not state[1]:  # Draw icon image

        # Trigger the redraw of the screen from the buffer
        icon_layer.updateLayer()
        image = pygame.image.load('images/ARROW_UP.png')
        icon_surface.blit(image, icon_pos)

    return state[0]


floor_state = [0, 0]
arrow_state = [0, 0]
# Список допустимых номеров этажей
ok_list = list(map(str, range(allowable_floor_range[0], allowable_floor_range[1] + 1)))

while True:
    floor_state[1] = update_floor_img(floor_state)
    floor_state[0] += 1
    if floor_state[0] == 40:
        floor_state[0] = 1
    time.sleep(3.5)

