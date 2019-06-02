#!/usr/bin/env python

# BS'D
# TODO
#- main.py
#- pip package
#- options
#    - durations, loop, resize, color, gradient
#    - type (rgba, rgb, greyscale)

import sys
import numpy as np
import argparse
from PIL import Image, ImageSequence

parser = argparse.ArgumentParser(description='Add a loader bar to your GIF.')
parser.add_argument(
    '-s', '--source-image',
    dest="SOURCE",
    required=True,
    help='<Required> The source image'
)
parser.add_argument(
    '-o', '--output-image',
    dest="DEST",
    required=True,
    help='<Required> The output image'
)
parser.add_argument(
    '-d' '--duration',
    default=50,
    dest="duration",
    nargs='?',
    type=int,
    help='The amount of time in milliseconds per frame'
)
parser.add_argument(
    '-c', '--color',
    default=[254, 0, 0, 1],
    nargs='+',
    action='store',
    dest='color',
    help='The RGBA color of the loading bar'
)
parser.add_argument(
    '-l', '--loop',
    dest="loop",
    default=0,
    type=int,
    nargs='?',
    help='The source image'
)

args = parser.parse_args()
print(args)

im = Image.open(args.SOURCE)
length = len(list(ImageSequence.Iterator(im)))
height, width = np.array(im).shape
step = int(round(width / length))
i = 0
frames = []
for frame in ImageSequence.Iterator(im):
    image = frame.copy().convert('RGBA')
    temp = np.array(image)
    temp[-5:-1,0:(i*step + step)] = args.color
    frames.append(Image.fromarray(temp))
    i+=1

frames[0].save(
        args.DEST,
        save_all=True,
        append_images=frames[1:],
        duration=args.duration,
        loop=args.loop
        )




