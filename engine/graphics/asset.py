"""
asset.py -- system

Contains utility functions for asset manipulation.

File loading functionality, font loading functionality, etc.

"""

import pygame as pg


# -------------------------------- #
# image loader
# -------------------------------- #

class ImageHandler:

    LOADED = {}

    @classmethod
    def __class_getitem__(cls, path):
        """Loads an image and stores it in the loaded buffer"""
        if path in cls.LOADED:
            return cls.LOADED[path]
        else:
            img = pg.image.load(path).convert_alpha()
            cls.LOADED[path] = img
            return img


# -------------------------------- #
# font handler
# -------------------------------- #


