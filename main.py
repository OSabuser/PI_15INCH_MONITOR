import pydispmanx
import pygame
import time


floor_r_pos = (250, 200)
floor_l_pos = (100, 200)
icon_pos = (600, 200)
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

    if state[0] is not state[1]:

        redraw_need = True if (state[0] // 10) != (state[1] // 10) else False

        del floor_r_surface
        del floor_r_layer

        # Перерисовка старшего разряда в случае, если меняется десяток
        if redraw_need:
            del floor_l_surface
            del floor_l_layer
            floor_l_layer = pydispmanx.dispmanxLayer(1)
            floor_l_surface = pygame.image.frombuffer(floor_l_layer, floor_l_layer.size, 'RGBA')

        floor_r_layer = pydispmanx.dispmanxLayer(2)
        floor_r_surface = pygame.image.frombuffer(floor_r_layer, floor_r_layer.size, 'RGBA')

        if state[0] < 10:
            image = pygame.image.load(f'images/{state[0]}.png')
            floor_r_surface.blit(image, floor_r_pos)
        elif state[0] < allowable_floor_range[1] + 1:
            image = pygame.image.load(f'images/{state[0] % 10}.png')
            floor_r_surface.blit(image, floor_r_pos)
            if redraw_need:
                image = pygame.image.load(f'images/{state[0] // 10}.png')
                floor_l_surface.blit(image, floor_l_pos)

        # Обновление программного слоя в GPU
        if redraw_need:
            floor_l_layer.updateLayer()
        floor_r_layer.updateLayer()

    return state[0]


def update_mode_img(state):
    global icon_surface, icon_layer

    if state[0] != state[1]:  # Draw icon image

        del icon_surface
        del icon_layer

        icon_layer = pydispmanx.dispmanxLayer(3)
        icon_surface = pygame.image.frombuffer(icon_layer, icon_layer.size, 'RGBA')

        if state[0] == "UP":
            image = pygame.image.load('images/ARROW_UP.png')
            icon_surface.blit(image, icon_pos)
        elif state[0] == "DL":
            image = pygame.image.load('images/ARROW_DOWN.png')
            icon_surface.blit(image, icon_pos)
        elif state[0] == "XX":
            image = pygame.image.load('images/LOST_CONNECTION.png')
            icon_surface.blit(image, icon_pos)

        icon_layer.updateLayer()

    return state[0]


# Список допустимых номеров этажей
floor_list = list(map(str, range(allowable_floor_range[0], allowable_floor_range[1] + 1)))
for idx, element in enumerate(floor_list):
    floor_list[idx] = element.rjust(2, '0')

mode_list = ("NN", "DL", "UP", "XX")

floor_number, mode = '', ''
floor_state = [0, 0]
arrow_state = ["", ""]

floor_number = "03"  # Get floor number
mode = "DL"  # Get direction state
message_received = True


while True:

    # Отрисовка изображений
    if message_received:
        message_received = False
        if floor_number in floor_list:
            floor_state[0] = int(floor_number)
            # For debug purposes -- > print(f"RAW FLOOR: {floor_state[0]}")
            floor_state[1] = update_floor_img(floor_state)

        if mode in mode_list:
            arrow_state[0] = mode
            # For debug purposes -- > print(f"RAW MODE: {arrow_state[0]}")
            arrow_state[1] = update_mode_img(arrow_state)
