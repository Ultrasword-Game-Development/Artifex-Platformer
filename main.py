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

FPS = 120

# setup delta time
delta = 1/FPS
start = 0

pg.init()

dimensions = (1280, 720)
buf_dimensions = (dimensions[0] // 3, dimensions[1] // 3)
screen = pg.display.set_mode(dimensions, 0, 32, vsync=0)
buffer = pg.Surface(buf_dimensions)

pg.display.set_caption("Artifex")


# display fps setup

character_order = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','.','-',',',':','+','\'','!','?','0','1','2','3','4','5','6','7','8','9','(',')','/','_','=','\\','[',']','*','"','<','>',';']

def clip(surf, x, y, w, h):
    return surf.subsurface(pg.Rect(x, y, w, h)).copy()

l_font_img = pygame.image.load('assets/large_font.png')
s_font_img = pygame.image.load('assets/small_font.png')


# setup stuff
clock = pg.time.Clock()
running = True


start = time.time()
while running:
    
    # clock update
    delta = time.time() - start
    start = time.time()

    # background flush
    buffer.fill((0, 0, 0))
    # print(1/delta)

    # draw a white square
    pg.draw.rect(buffer, (255, 255, 255), (0, 0, 20, 20))
    pg.draw.line(buffer, (255, 255, 255), (100, 100), (20, 30))

    # update events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # push buffer
    screen.blit(pg.transform.scale(buffer, dimensions), (0, 0))
    # update display
    pg.display.flip()
    clock.tick(FPS)

pg.quit()
