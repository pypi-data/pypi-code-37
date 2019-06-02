#!/bin/python3

# BS'D
# TODO
#- main.py
#- pip package
#- options
#    - durations, loop, resize, color, gradient
#    - type (rgba, rgb, greyscale)

import sys
import numpy as np
from PIL import Image, ImageSequence

im = Image.open(sys.argv[1])
length = len(list(ImageSequence.Iterator(im)))
height, width = np.array(im).shape
step = int(round(width / length))
i = 0
frames = []
for frame in ImageSequence.Iterator(im):
    image = frame.copy().convert('RGBA')
    temp = np.array(image)
    temp[-5:-1,0:(i*step + step)] = [255, 0, 0, 1]
    frames.append(Image.fromarray(temp))
    i+=1

frames[0].save(
        sys.argv[2],
        save_all=True,
        append_images=frames[1:],
        duration=50,
        loop=0
        )




