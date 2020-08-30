import os
from PIL import Image

def run(file, inputMount, outputMount):
  inputPath = os.path.join(inputMount, file.split('/')[-1])
  outputPath = os.path.join(outputMount, file.split('/')[-1])
  size = (128, 128)
  try:
    with Image.open(inputPath) as im:
      im.thumbnail(size)
      im.save(outputPath)
  except OSError:
    print("cannot create thumbnail for", file)