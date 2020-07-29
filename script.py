import os
import argparse
import importlib

def main(directory, module, input, output):
  module = importlib.import_module('.' + module.strip(), package='repo')
  module.run(directory[0].strip(), input.strip(), output.strip())

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('FILE_DIRECTORY', nargs='*')
  parser.add_argument('-m', '--module', help='Pipe line module for low to high ROI.', required=True)
  parser.add_argument('-i', '--input', help='Input mount partition path.', required=True)
  parser.add_argument('-o', '--output', help='Output mount partition path.', required=True)
  kwargs = vars(parser.parse_args())
  directory = kwargs.pop('FILE_DIRECTORY')
  main(directory, **kwargs)