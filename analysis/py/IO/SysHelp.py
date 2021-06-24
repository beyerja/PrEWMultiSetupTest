""" Helper functions for dealing with system tasks.
"""

from pathlib import Path
import os
import sys

def add_to_path(dir_path):
  """ Try to add the given dir path to the system path.
      Returns true if successful (or path already included), or false if 
      directory not found.
  """
  if os.path.isdir(dir_path):
    if dir_path not in sys.path:
      sys.path.append(dir_path)
    return True
  else:
    return False

def find_PrOut():
  """ Find the PrEW output reader helper classes directory and append it to the 
      path so that it can be imported.
  """
  path_options = [
    "/home/jakob/DESY/Programming/TGCAnalysis/PrEW/source/prout",
    "/afs/desy.de/group/flc/pool/beyerjac/TGCAnalysis/PrEW/source/prout"
  ]
  
  for path_option in path_options:
    if add_to_path(path_option):
      return True
    
  # If we got here, PrOut wasn't found
  raise Exception("Couldn't find PrOut directory.")
  
def create_dir(dir):
  """ Try to create the given directory and its parents.
  """
  Path(dir).mkdir(parents=True, exist_ok=True)