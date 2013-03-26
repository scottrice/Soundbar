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
  
def generate_frame_images(input_file,framestep=90):
  """
  Tells mplayer to generate an image of a frame in input_file every framestep
  frames.
  
  Returns the directory containing all of these imagess
  """
  (filename,fileextension) = os.path.basename(os.path.splitext(input_file))
  # The output directory should be the directory in which
  directory = os.path.join(temp_working_directory(),filename)
  # Remove everything that was currently at the target directory
  if os.path.exists(directory):
    shutil.rmtree(directory)
  # Make the target directory
  os.makedirs(directory)
  # Move to the target directory
  os.chdir(directory)
  cmd = "mplayer -framedrop -speed 100 -vf framestep=%i -nosound -vo jpeg %s"
  cmd = cmd % (framestep,input_file)
  # Run the mplayer command
  os.system(cmd)
  return directory

def main():
	pass


if __name__ == '__main__':
  # Save the current working directory in case our application changes it
  cwd = os.getcwd()
  # Do work
	main()
	# Put the user back where they were
	os.chdir(cwd)