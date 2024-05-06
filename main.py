# ---------------------------------------------------------------- #
# For sake of completion (on mac), write all code for the MAC
#        not windows -- not opengl (not yet)
#
#
# Artifex - Platformer
# By: Peter Zhang
# ---------------------------------------------------------------- #

import pygame as pg

import time

pg.init()

# -------------------------------- #
dimensions = (1280, 720)
buf_dimensions = (dimensions[0] // 3, dimensions[1] // 3)
screen = pg.display.set_mode(dimensions, 0, 32, vsync=0)
buffer = pg.Surface(buf_dimensions)

pg.display.set_caption("Artifex")

# -------------------------------- #

from engine.graphics import *
from engine.system import *
from engine.utils import *

# -------------------------------- #


FPS = 120
BG_COL = (0, 0, 0)
# BG_COL = (255, 255, 255)

# setup delta time
delta = 0
start = 0


# ----------------- #

large_font = PixelFont("assets/large_font.png")
large_font.alter_palette(lambda c: ((255, 255, 255, 255) if c[0] == 255 else (127, 0, 0, 255)) if c[0] != 0 else (0, 0, 0, 0))

small_font = PixelFont("assets/small_font.png")
small_font.alter_palette(lambda c: ((255, 255, 255, 255) if c[0] == 255 else (127, 0, 0, 255)) if c[0] != 0 else (0, 0, 0, 0))

# ----------------- #

v_spin_s = pg.math.Vector2(200, 100)
v_spin = pg.math.Vector2(30, 0)

animation = Animation("assets/entity/player-sprite.json")
a_regist = AnimationRegistry(animation)


# -------------------------------- #
# setup stuff
clock = pg.time.Clock()
running = True
time.sleep(0.1)
delta = 0.1

# -------------------------------- #
start = time.time()
while running:
    # -------------------------------- #
    # clock update
    delta = time.time() - start + 0.00001
    start = time.time()

    # -------------------------------- #
    # background flush
    buffer.fill(BG_COL)
    # print(1/delta)

    # for i, sprite in enumerate(animation.iterate_compressed_frames()):
    #     buffer.blit(sprite._image, (200 + i * animation._rect.w, 20))

    buffer.blit(a_regist.get_sprite("__compressed__", delta), (0, 100))

    # for i, sprites in enumerate(animation.iterate_frames()):
    #     # print(sprites)
    #     for j, sprite in enumerate(sprites):
    #         buffer.blit(sprite._image, (200 + i * animation._rect.w, 50 + j * animation._rect.h))
    

    # -------------------------------- #
    # draw a white square
    # pg.draw.rect(buffer, (255, 255, 255), (0, 0, 20, 20))
    pg.draw.line(buffer, (255, 255, 255), v_spin_s, v_spin_s + v_spin)
    v_spin.rotate_ip(30 * delta)

    # draw the fps
    large_font.render(buffer, str(round(1/delta)), (0, 0))
    small_font.render(buffer, "Hello World", (100, 100))
    # -------------------------------- #
    # update events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # -------------------------------- #
    # push buffer
    screen.blit(pg.transform.scale(buffer, dimensions), (0, 0))
    # update display
    pg.display.flip()
    clock.tick(FPS)

# -------------------------------- #
pg.quit()
