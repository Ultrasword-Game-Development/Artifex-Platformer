"""
animation.py - system

Contains utility functions for animation manipulation.

"""

import pygame as pg

from ..graphics import ImageHandler
from .. import utils

import json
import os


# -------------------------------- #
# simple animation handler
# -------------------------------- #

class AnimationHandler:
    LOADED = {}

    @classmethod
    def get_animation(cls, path: str):
        """Returns access to an AnimationHandler object"""
        if path in cls.LOADED:
            return cls.LOADED[path]
        else:
            anim = Animation(path)
            cls.LOADED[path] = anim
            return anim
    
    @classmethod
    def get_animation_registry(cls, path: str):
        """Returns a Registry to an AnimationHandler object"""
        return AnimationRegistry(cls.get_animation(path))


# -------------------------------- #
# animation registry -- allows access to buffered animations
# -------------------------------- #

# NOTE: When building signal system -- exclude animation update signals (no need + too much overhead)

class AnimationRegistry:
    def __init__(self, parent: "AnimationHandler"):
        """Creates an AnimationRegistry object"""
        self._frame = 0
        self._time = 0
        self._parent = parent

    def get_sprite(self, layer: str, dt: float):
        """
        Returns the current frame

        - entity class should have access to the 'layer' string
        """
        self._time += dt
        if self._time >= self._parent._layers[layer]._frames[self._frame]._duration:
            self._time = 0
            self._frame += 1
            if self._frame >= len(self._parent._layers[layer]):
                self._frame = 0
        
        # return the frame
        return self._parent._layers[layer]._frames[self._frame]._image
    
    def get_frame(self, layer: str):
        """Returns the current frame"""
        return self._parent._layers[layer]._frames[self._frame]
    
    def get_compressed_frame(self):
        """Returns the current frame -- all layers compressed"""
        return self._parent._layers["__compressed__"]._frames[self._frame]

    def __len__(self):
        return len(self._parent._layers["__compressed__"])

# -------------------------------- #
# animation class -- stores information about an animation
# -------------------------------- #

class Layer:
    def __init__(self, settings: dict, frames: list):
        """Creates a Layer object"""
        # layer data
        self._name = settings["name"]
        self._opacity = settings["opacity"]
        self._blend = settings["blendMode"]
        # graphics data
        self._frames = frames
    
    def get_frame(self, index: int):
        """Returns a frame object"""
        return self._frames[index]

    def __len__(self):
        return len(self._frames)

# -------------------------------- #

class Frame:
    def __init__(self, name: str, clip_rect: pg.Rect, frame_rect: pg.Rect, duration: int, _id: int, image: pg.Surface):
        """Creates a Frame object"""
        self._name = name
        self._clip_rect = clip_rect
        self._frame_rect = frame_rect
        self._duration = duration
        self._id = _id

        self._image = image

# -------------------------------- #

class Animation:
    """
    Stores information on a SINGLE animation

    - _file = the file path to the aseprite.json file
    - _rect = the dimensions of the animation
    

    clip_rect (the subsurface rectangle)
    
    """

    def __init__(self, file: str):
        """Creates an animation given a aseprite.json file"""
        self._file = file

        # parse data from the file
        with open(self._file, 'r') as f:
            data = json.load(f)

        # load the information from the json file
        self._image_rect = pg.Rect(0, 0, data["meta"]["size"]["w"], data["meta"]["size"]["h"])
        self._f_image = os.path.join(os.path.dirname(self._file), data["meta"]['image'])
        self._image = ImageHandler[self._f_image]
        self._rect = pg.Rect(0, 0, data["frames"][0]["frame"]["w"], data["frames"][0]["frame"]["h"])

        # load layers -- empty layers
        self._layers = {settings["name"]: Layer(settings, []) for settings in data["meta"]["layers"]}

        # add frames to layers (non-recommended usage in development environment)
        for f_data in data["frames"]:
            # extract data from filename string
            a_name, layer, n_frame = f_data["filename"].split("||")

            clip_rect = f_data["frame"]
            frame_rect = f_data["spriteSourceSize"]
            duration = f_data["duration"] / 1000

            # create clipped image surface
            f_clip = utils.clip(self._image, clip_rect['x'], clip_rect['y'], clip_rect['w'], clip_rect['h'])

            # create frame object
            frame = Frame(a_name, 
                        pg.Rect(clip_rect['x'], clip_rect['y'], clip_rect['w'], clip_rect['h']),
                        pg.Rect(0, 0, frame_rect['w'], frame_rect['h']), 
                        duration,
                        n_frame,
                        f_clip)

            # add to respective layer
            self._layers[layer]._frames.append(frame)

        # sort all layers
        for layer in self._layers.values():
            layer._frames.sort(key=lambda x: x._id)

        # compress all layers into one (for optional use) -- although you're pretty much only going to use this (unless you're rendering things separately)
        # assumes:
        # - all frames have same size
        # - all frames have same duration
        # - all layers are same animation length / frame count
        # - python dictionaries don't sort by key (it's true)
        key = list(self._layers.keys())[0]
        c_layer = Layer({"name": "__compressed__", "opacity": 255, "blendMode": "normal"}, [])

        for i in range(len(self._layers[key]._frames)):
            # create empty frame + render all layers onto it in accordance to size + etc
            surf = pg.Surface(self._rect.size, 0, 32).convert()
            surf.fill((0, 0, 0, 0))

            # render all layers onto surface
            for layer in self._layers.values():
                surf.blit(layer._frames[i]._image, (0, 0))

            # create frame object
            frame = Frame("compressed", 
                        pg.Rect(0, 0, self._rect.w, self._rect.h),
                        pg.Rect(0, 0, self._rect.w, self._rect.h), 
                        layer._frames[i]._duration,
                        i,
                        surf)

            # add to compressed layer
            c_layer._frames.append(frame)

        # add to the layers
        self._layers["__compressed__"] = c_layer

    def iterate_compressed_frames(self):
        """Iterates through the compressed frames"""
        for frame in self._layers["__compressed__"]._frames:
            yield frame

    def iterate_frames(self):
        """Iterates through frames, returning a list of frames"""
        for frame in range(len(self._layers["__compressed__"]._frames)):
            yield [layer._frames[frame] for layer in self._layers.values() if layer._name != "__compressed__"]

    def get_layer(self, layer: str):
        """Returns a layer object"""
        return self._layers[layer]



