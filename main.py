#!/usr/bin/env python
# encoding: utf-8
"""
main.py

Created by Scott on 2013-03-26.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import sys
import os
import shutil

def temp_working_directory():
  """
  Returns a working directory suitable for throwing lots of bullshit images
  """
  # TODO: Make this a much less visible location.
  return os.path.join(os.path.expanduser("~"),"JustUsTemp")
  
def create_and_enter_working_directory(input_file):
  """
  Takes a filename and creates a blank working directory for this file to use.
  """
  (filename,fileextension) = os.path.basename(os.path.splitext(input_file))
  # The output directory should be the directory in which
  directory = os.path.join(temp_working_directory(),filename)
  # Remove everything that was previously at the target directory
  if os.path.exists(directory):
    shutil.rmtree(directory)
  # Make the target directory
  os.makedirs(directory)
  # Move to the target directory
  os.chdir(directory)
  
def generate_frame_images(input_file,framestep=90):
  """
  Tells mplayer to generate an image of a frame in input_file every framestep
  frames.
  """
  cmd = "mplayer -framedrop -speed 100 -vf framestep=%i -nosound -vo jpeg %s"
  cmd = cmd % (framestep,input_file)
  # Run the mplayer command
  os.system(cmd)
  
def resize(input_file,width=1,height=1):
  """
  Resizes an image to width by height in place
  """
  pass
  
def assemble_barcode(output_file):
  """
  Converts all of the png files in the current directory into a single 
  moviebarcode.
  """
  pass

def main(input_file):
  create_and_enter_working_directory(input_file)
  generate_frame_images(input_file)
  for entry in os.listdir("."):
    if os.path.isfile(entry):
      resize(entry,1,1)
  assemble_barcode("barcode.png")
  

if __name__ == '__main__':
  # Save the current working directory in case our application changes it
  cwd = os.getcwd()
  # Do work
  # TODO: Take the input_file from the script arguments
  main("")
  # Put the user back where they were
  os.chdir(cwd)