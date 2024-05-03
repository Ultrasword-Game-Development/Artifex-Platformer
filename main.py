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
buf_dimensions = (dimensions[0] // 2, dimensions[1] // 2)
screen = pg.display.set_mode(dimensions, 0, 32, vsync=0)
buffer = pg.Surface(buf_dimensions)

pg.display.set_caption("Artifex")

# -------------------------------- #

from engine.graphics import *


# -------------------------------- #


FPS = 120

# setup delta time
delta = 1/FPS
start = 0


# ----------------- #

large_font = PixelFont("assets/large_font.png")
large_font.alter_palette(lambda c: ((255, 255, 255, 255) if c[0] == 255 else (127, 0, 0, 255)) if c[0] != 0 else (0, 0, 0, 0))

small_font = PixelFont("assets/small_font.png")
small_font.alter_palette(lambda c: ((255, 255, 255, 255) if c[0] == 255 else (127, 0, 0, 255)) if c[0] != 0 else (0, 0, 0, 0))

# ----------------- #

v_spin_s = pg.math.Vector2(200, 100)
v_spin = pg.math.Vector2(30, 0)

# -------------------------------- #
# setup stuff
clock = pg.time.Clock()
running = True
time.sleep(0.01)

# -------------------------------- #
start = time.time()
while running:
    # -------------------------------- #
    # clock update
    delta = time.time() - start
    start = time.time()

    # -------------------------------- #
    # background flush
    buffer.fill((0, 0, 0))
    # print(1/delta)

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
