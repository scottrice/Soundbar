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
import random

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
  (filename,fileextension) = os.path.splitext(input_file)
  filename = os.path.basename(filename)
  # The output directory should be the directory in which
  directory = os.path.join(temp_working_directory(),filename)
  # Remove everything that was previously at the target directory
  if os.path.exists(directory):
    shutil.rmtree(directory)
  # Make the target directory
  os.makedirs(directory)
  # Move to the target directory
  os.chdir(directory)
  
def generate_frame_images(input_file,framestep=90,imagetype="jpeg"):
  """
  Tells mplayer to generate an image of a frame in input_file every framestep
  frames.
  """
  cmd = "mplayer -framedrop -speed 100 -vf framestep=%i -nosound -vo %s \"%s\""
  cmd = cmd % (framestep,imagetype,input_file)
  # Run the mplayer command
  os.system(cmd)
  
def extract_audio(input_file):
  """
  Uses FFMpeg to extract the audio from a video file into a separate mp3
  
  returns the path to the created audio file
  """
  pass
  
def convert_audio_to_data_file(audio_file):
  """
  Converts an MP3 into a text file which contains the amplitude information
  
  returns the path to the data file
  """
  pass
  
def parse_data_file(audio_data_file):
  """
  Converts a text file containing audio data into an array of audio information
  which can be used by our application
  """
  pass
  
def generate_audio_data(input_file):
  audio_file = extract_audio(input_file)
  audio_data_file = convert_audio_to_data_file(audio_file)
  return parse_data_file(audio_data_file)
  
  
def resize(input_file,width=1,height=1):
  """
  Resizes an image to width by height in place
  """
  cmd = "convert %s -resize %ix%i\! %s"
  cmd = cmd % (input_file,width,height,input_file)
  os.system(cmd)
  
def assemble_barcode(output_file,imagetype="jpg"):
  """
  Converts all of the png files in the current directory into a single 
  moviebarcode.
  """
  cmd = "montage -geometry +0+0 -background \"rgb(221,221,220)\" -tile x1 *.%s \"%s\""
  cmd = cmd % (imagetype,output_file)
  os.system(cmd)

def main(input_file):
  (input_filename,_) = os.path.splitext(os.path.basename(input_file))
  create_and_enter_working_directory(input_file)
  generate_frame_images(input_file,45)
  audio_data = generate_audio_data(input_file)
  for entry in os.listdir("."):
    if os.path.isfile(entry):
      resize(entry)
      resize(entry,1,random.choice(range(500)))
  assemble_barcode("barcode.png")
  output_filename = "%s (Soundbar).png" % input_filename
  output_filepath = os.path.join(os.path.dirname(input_file),output_filename)
  shutil.copy("barcode.png",output_filepath)
  

if __name__ == '__main__':
  # Save the current working directory in case our application changes it
  cwd = os.getcwd()
  # Do work
  if len(sys.argv):
    main(os.path.expanduser(sys.argv[1]))
  # Put the user back where they were
  os.chdir(cwd)