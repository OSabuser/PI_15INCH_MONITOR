# 28_10_2022 AKIMOV DMITRY, MACH UNIT LLC

import pyglet
from pyglet import image
from pyglet.media import Player
from pyglet.window import Window
from pyglet.sprite import Sprite
from pyglet.gl import *


# TODO: 1. try, except на критически важные блоки кода
# TODO: 2. Статические изображения + анимации
pyglet.options['search_local_libs'] = True

path_to_video = "test_1024x768.mp4"

if __name__ == '__main__':
    # Set alpha blending config
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    background = pyglet.graphics.OrderedGroup(0)
    foreground = pyglet.graphics.OrderedGroup(1)

    player = pyglet.media.Player()
    mp4_file = pyglet.media.load(path_to_video)
    player.queue(mp4_file)
    player.loop = True
    player.play()

    pic_img = Sprite(image.load('pic_4.png'), x=50, y=200, group=foreground)
    floor_img = Sprite(image.load('1.png'), x=750, y=300, group=foreground)

    win = Window(width=1024, height=768, fullscreen=False)
   # win.set_mouse_visible(visible=False)

    floor_state = ['0', '0']
    arrow_state = ['0', '0']
    ok_list = ('1', '2', '3', '4', '5')
    can_refresh = False
    floor_number = ''
    direction = ''
    pic_img.visible = True
    player.play()

    def draw_everything(dt):
        if player.source and player.source.video_format:
            player.get_texture().blit(0, 0)
        pic_img.draw()
        floor_img.draw()

    @win.event
    def on_draw():
        draw_everything(None)

    pyglet.clock.schedule_interval(draw_everything, 1 / 60)
    pyglet.app.run()
