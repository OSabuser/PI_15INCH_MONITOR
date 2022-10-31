import pydispmanx
import pygame
import serial
from serial import SerialException

floor_r_pos = (250, 284)
floor_l_pos = (100, 284)
icon_pos = (600, 284)
allowable_floor_range = (1, 40)
uart0_port_name = "/./dev/ttyAMA0"
uart0_baud = 115200

# Create new layer object for GPU layer 1
floor_l_layer = pydispmanx.dispmanxLayer(1)
floor_r_layer = pydispmanx.dispmanxLayer(2)
icon_layer = pydispmanx.dispmanxLayer(3)

# Create pyGame surfaces linked to the layer buffers
floor_l_surface = pygame.image.frombuffer(floor_l_layer, floor_l_layer.size, 'RGBA')
floor_r_surface = pygame.image.frombuffer(floor_r_layer, floor_r_layer.size, 'RGBA')
icon_surface = pygame.image.frombuffer(icon_layer, icon_layer.size, 'RGBA')

while True:
    try:
        ser = serial.Serial(port=uart0_port_name, baudrate=uart0_baud)  # open serial port
    except SerialException:
        print('Serial port connection error!\n')
        pass
    else:
        break


def update_floor_img(state):
    global floor_l_surface, floor_r_surface, floor_l_layer, floor_r_layer

    if state[0] is not state[1]:  # Draw floor number

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

        # Trigger the redraw of the screen from the buffer
        if redraw_need:
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


# Список допустимых номеров этажей
ok_list = list(map(str, range(allowable_floor_range[0], allowable_floor_range[1] + 1)))
floor_number, mode = '', ''
floor_state, arrow_state = [0, 0], [0, 0]
message_received = False

while True:

    # UART message handling from MCU
    if ser.inWaiting() > 0:
        # read the bytes and convert from binary array to ASCII
        data_str = ser.read(ser.inWaiting()).decode('ascii')
        # For debug purposes -- > print(data_str)
        if len(data_str) == 6:
            floor_number = data_str[1:3]  # Get floor number
            mode = data_str[3:5]  # Get direction state
            message_received = True
            print(f"Floor: {floor_number}, mode: {mode}")

    #if message_received:
       # message_received = False
        #floor_state[1] = update_floor_img(floor_state)