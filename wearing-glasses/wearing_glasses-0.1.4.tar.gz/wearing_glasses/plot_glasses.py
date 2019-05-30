# BIG CHENG, init 2019/05/29
# codes to plot glasses on face

import os
from PIL import Image, ImageDraw
#import matplotlib.pyplot as plt
import numpy as np
import math
from numpy import (array, dot, arccos, arcsin, clip)
from numpy.linalg import norm
import random


path_predictor = './shape_predictor_68_face_landmarks.dat'
n_parts = 68

import dlib
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(path_predictor)

#from skimage import io, draw

def draw_ellipse(image, rect, rot, color, width):
  w, h = rect[2] - rect[0], rect[3] - rect[1]
  overlay = Image.new('RGBA', (w, h))
  draw = ImageDraw.Draw(overlay)
  draw.ellipse((0, 0, w, h), outline=color, fill=color)
  draw.ellipse((0+width, 0+width, w-width, h-width), outline=color, fill=(255,255,255,0))
  rotated = overlay.rotate(rot, expand=True, center=(w/2, h/2))
  
  def rc2box(rect, size):
    cx = (rect[0]+rect[2])/2
    cy = (rect[1]+rect[3])/2
    nw0 = size[0]/2
    nh0 = size[1]/2
    nw1 = size[0]-nw0
    nh1 = size[1]-nh0
    return int(cx-nw0), int(cy-nh0), int(cx+nw1), int(cy+nh1)
    
  box = rc2box(rect, (rotated.width, rotated.height))
  print ("box= ", box)
  image.paste(rotated, box, rotated)
  
  
def draw_line(draw, line, color, width):
  draw.line(line, fill=color, width=width)


def det2rect(det):
  assert(type(det)==dlib.rectangle)
  return det.left(), det.top(), det.right(), det.bottom()

## 
def detect_face(img):
  dets = detector(img, 1)
  rects = [det2rect(det) for det in dets]
  return rects, dets


def detect_fl(img, det):
  shape = predictor(img, det)
  lms = [(shape.part(i).x, shape.part(i).y) for i in range(n_parts)]
  return lms


### gen glasses

## help func.
def avg_points(lms, pts):
  l = len(pts)
  if l == 0:
    return None, None
  xs = [lms[i][0] for i in pts]
  ys = [lms[i][1] for i in pts]
  #print xs, ys
  return sum(xs)/l, sum(ys)/l

def avg_2point(pt0, pt1, ratio):
  return pt0[0]*ratio + pt1[0]*(1-ratio), pt0[1]*ratio + pt1[1]*(1-ratio)

## output "glasses" data, by ref. landmarks
def lms2glasses(lms):
  ## offset 1 to 0-based
  idx_reye0 = 37 - 1
  idx_reye1 = 42 - 1
  idx_reye2 = 40 - 1 ## end
  idx_leye0 = 43 - 1
  idx_leye1 = 48 - 1
  idx_leye2 = 46 - 1 ## end
  idx_rbow0 = 18 - 1
  idx_rbow1 = 22 - 1
  idx_lbow0 = 23 - 1
  idx_lbow1 = 27 - 1
  
  idx_nose0 = 28 - 1
  idx_nose1 = 29 - 1
  idx_rear = 1 - 1
  idx_lear = 17 - 1
  
  avg_reye = avg_points(lms, list(range(idx_reye0, idx_reye1+1)))
  avg_leye = avg_points(lms, list(range(idx_leye0, idx_leye1+1)))
  avg_rbow = avg_points(lms, list(range(idx_rbow0, idx_rbow1+1)))
  avg_lbow = avg_points(lms, list(range(idx_lbow0, idx_lbow1+1)))

  avg_nose = avg_points(lms, list(range(idx_nose0, idx_nose1+1)))
  
  ## special func. from c, w to rect
  def cw2rc(c, w_2):
    h_2 = w_2 / 1.6
    dx = 0
    return int(c[0] - w_2 - dx), int(c[1] - h_2), int(c[0] + w_2 - dx), int(c[1] + h_2)
  
  ## special func. to estimate bow-eye angle
  def cal_ang2(v0, v1):
    dv = np.array(v1) - np.array(v0)
    dv = dv/norm(dv)
    rot = -(arcsin(dv[1]) * 180 / math.pi)  ## in image, y is upside-down
    return rot

  def cal_glasses(avg_reye, avg_leye, avg_rbow, avg_lbow, avg_nose):
    rw_2 = abs(avg_reye[0] - avg_nose[0])
    lw_2 = abs(avg_leye[0] - avg_nose[0])
    
    def adj_w(rw_2, lw_2):
      mid = math.sqrt(rw_2*lw_2)
      fac = 0.85
      return math.sqrt(rw_2*mid)*fac, math.sqrt(lw_2*mid)*fac
    
    rw_2, lw_2 = adj_w(rw_2, lw_2)
    
    rect0 = cw2rc(avg_reye, rw_2)    
    rect1 = cw2rc(avg_leye, lw_2)
    rot = cal_ang2(avg_reye, avg_leye)

    return rect0, rect1, rot 
    
  rect0, rect1, rot = cal_glasses(avg_reye, avg_leye, avg_rbow, avg_lbow, avg_nose)

  def make_line0(avg_reye, avg_leye):
    x0, y0 = avg_2point(avg_reye, avg_leye, 0.35)
    x1, y1 = avg_2point(avg_reye, avg_leye, 0.65)
    return x0, y0, x1, y1

  def make_line1(pt_reye, pt_rbow, pt_rear):
    pt0 = avg_2point(pt_reye, pt_rbow, 0.5)
    x0, y0 = avg_2point(pt0, pt_rear, 0.03)
    x1, y1 = avg_2point(pt0, pt_rear, 0.78)
    return x0, y0, x1, y1

  def make_line2(pt_leye, pt_lbow, pt_lear):
    pt0 = avg_2point(pt_leye, pt_lbow, 0.5)
    x0, y0 = avg_2point(pt0, pt_lear, 0.03)
    x1, y1 = avg_2point(pt0, pt_lear, 0.78)
    return x0, y0, x1, y1
  
  line0 = make_line0(avg_reye, avg_leye)    
  line1 = make_line1(lms[idx_reye0], lms[idx_rbow0], lms[idx_rear])    
  line2 = make_line2(lms[idx_leye2], lms[idx_lbow1], lms[idx_lear])    
  #line1, line2 = make_lines_from_2rect(rect0, rect1)
  
  def make_width_auto(v0, v1):
    dv = np.array(v1) - np.array(v0)
    fac = 12.
    return max(1, int(norm(dv)/fac))
    
  width_auto = make_width_auto(avg_reye, avg_leye)
  
  return rect0, rect1, rot, line0, line1, line2, width_auto

####
def draw_glasses(image, draw, lms, color, width):
  rect0, rect1, rot, line0, line1, line2, width_auto = lms2glasses(lms)
  if width == -1:
    width = width_auto
    print ("use width auto = ", width)
  
  draw_ellipse(image, rect0, rot, color, width)  
  draw_ellipse(image, rect1, rot, color, width)  
  draw.line(line0, fill=color, width=width)
  draw.line(line1, fill=color, width=width)
  draw.line(line2, fill=color, width=width)
  
  
def plot_addon(path_name, path_to_save=None, color="#ffffff", width=3, do_random=False):
  print ("processing %s" % path_name)
  image = Image.open(path_name)
  #img = io.imread(path_name)
  img = np.array(image)
  rect_faces, dets = detect_face(img)
  draw = ImageDraw.Draw(image)

  def gen_rand_color():  
    r = lambda: random.randint(0,255)
    return '#%02X%02X%02X' % (r(),r(),r())

  def gen_rand_width():  
    return random.randint(1,10)
    
  ## draw detected landmarks
  for k, d in enumerate(dets):
    fl = detect_fl(img, d)

    ## gen glasses
    if do_random:
      color = gen_rand_color()
      width = gen_rand_width()
    
    draw_glasses(image, draw, fl, color, width)

  del draw
  
  image.save(path_to_save)


import click

@click.command()
@click.argument('dir_in')
@click.argument('dir_out')
@click.option('--color', default="#0000ff", help='color for glasses')
@click.option('--width', type=int, default=-1, help='width for glasses')
@click.option('--random', default=False, help='generate glasses w/ different color and width randomly')


def main(dir_in, dir_out, color, width, random):
  print ("begin to process")

  ## list file in dir_in
  fnames2plot = os.listdir(dir_in)
  n = len(fnames2plot)
  
  for i in range(n):
    fname2plot = fnames2plot[i]
    path2plot = os.path.join(dir_in, fname2plot)
    path2save = os.path.join(dir_out, fname2plot) ## no dir_name, should still be uniq
    plot_addon(path2plot, path2save, color, width, random)  ## save
  
  print ("done")
  
if __name__ == "__main__":

  main()
  
  


