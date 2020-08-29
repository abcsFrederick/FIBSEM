import os
from PIL import Image

import sys
import torch
import numpy as np

import monai
from monai.transforms import ThresholdIntensity, Rotate90

def run(file, inputMount, outputMount):
  inputPath = os.path.join(inputMount, file.split('/')[-1])
  outputPath = os.path.join(outputMount, file.split('/')[-1])
  print("attempting to threshold a new image")
  try:
    with Image.open(inputPath) as im_image:
      im = np.array(im_image)
      # MONAI transforms always take channel-first data: [channel x H x W]
      im_data = np.moveaxis(im, -1, 0)  # make them channel first
      # create a MONAI threshold transform. The threshold value is fixed for simplicity.
      # it could be a parameter
      threshold_xform = ThresholdIntensity( threshold=175,above=False, cval=0.0)
      # threshold image to remove background
      thresh_im = threshold_xform(im_data)
      # the output image was rotated during the read, so fix this rotation
      # using numpy transformations
      rot_im = np.rot90(thresh_im,-1)
      flip_im = np.flip(rot_im,1)
      # convert back to image and save as TIFF
      out_image = Image.fromarray(flip_im)
      out_image.save(outputPath, "TIFF")
  except OSError:
      print("cannot create threshold image for", file)
