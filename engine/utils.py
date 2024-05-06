"""
utils.py - graphics

Contains utility functions for graphics manipulation.

"""

import pygame as pg

def palette_swap(surf, old_c, new_c):
    """Palette swap function"""
    c_copy = surf.copy()
    c_copy.fill(new_c)
    c_surf = surf.copy()
    c_surf.set_colorkey(old_c)
    c_copy.blit(c_surf, (0, 0))
    return c_copy


def clip(image, x, y, w, h):
    """Clip a rect from a surface"""
    return image.subsurface(pg.Rect(x, y, w, h)).convert_alpha().copy()
