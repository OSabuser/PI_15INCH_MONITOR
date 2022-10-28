# 28_10_2022 AKIMOV DMITRY, MACH UNIT LLC

import pyglet
from pyglet import image
from pyglet.media import Player, load
from pyglet.window import Window
from pyglet.sprite import Sprite
from pyglet.gl import *

pyglet.options['search_local_libs'] = True

path_to_video = "test_1024x768.mp4"

if __name__ == '__main__':
    # Set alpha blending config
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    background = pyglet.graphics.OrderedGroup(0)
    foreground = pyglet.graphics.OrderedGroup(1)

    player = Player()
    mp4_file = load(path_to_video)
    player.queue(mp4_file)
    player.loop = True

    pic_img = Sprite(image.load('pic_4.png'), x=50, y=200, group=foreground)
    floor_img = Sprite(image.load('1.png'), x=750, y=300, group=foreground)

    win = Window(width=1024, height=768, fullscreen=False)
    win.set_mouse_visible(visible=False)

    floor_state = ['0', '0']
    arrow_state = ['0', '0']
    ok_list = ('1', '2', '3', '4', '5')
    can_refresh = False
    floor_number = ''
    direction = ''
    pic_img.visible = True
    player.play()

    def draw_everything(dt):
        win.clear()
        if player.source and player.source.video_format:
            player.get_texture().blit(0, 0)
        #pic_img.draw()
        #floor_img.draw()

    @win.event
    def on_draw():
        draw_everything(None)

    pyglet.clock.schedule_interval(draw_everything, 1 / 30)
    pyglet.app.run()
