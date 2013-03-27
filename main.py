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
import commands
import math

first_filename = "00000000.jpg"
execute_location = os.path.abspath(__file__)

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
  
def add_image_height_hack_image():
  # Get the directory of the executing file
  directory = os.path.dirname(execute_location)
  hack_location = os.path.join(directory,first_filename)
  shutil.copy(hack_location,first_filename)
  
def get_framerate(input_file):
  (status,output) = commands.getstatusoutput("ffprobe \"%s\"" % input_file)
  for l in output.split("\n"):
    l = l.strip()
    if l.startswith("Stream"):
      # We are on the line which has our data, find it!
      probe_data = l.split(",")
      for datapoint in probe_data:
        datapoint = datapoint.strip()
        if datapoint.endswith("fps"):
          separator_index = datapoint.find(" ")
          fps = float(datapoint[:separator_index])
          int_fps = int(fps)
          if int_fps == fps:
            return fps
          else:
            return int_fps + 1
  return 24
  
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
  cmd = "ffmpeg -i \"%s\" -ab 160k -ac 1 -ar 44100 -vn audio.mp3"
  cmd = cmd % (input_file)
  # Run the ffmpeg command #yolo
  os.system(cmd)
  return "audio.mp3"
  
def convert_audio_to_data_file(audio_file):
  """
  Converts an MP3 into a text file which contains the amplitude information
  
  returns the path to the data file
  """
  cmd = "sox \"%s\" -r 1 audio.dat"
  cmd = cmd % (audio_file)
  os.system(cmd)
  return "audio.dat"
  
def adjust_data_value(current):
  current = abs(current)
  # Found through trial and error
  current = 44.693 * math.log((10000000 * current) + 1,10)
  return current
  
def parse_data_file(audio_data_file):
  """
  Converts a text file containing audio data into an array of audio information
  which can be used by our application
  """
  data = []
  audio_data = open(audio_data_file)
  for data_line in audio_data:
    if data_line.startswith(";"):
      continue
    current = data_line.strip().split()[1]
    current = float(current)
    data.append(adjust_data_value(current))
  return data
  
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
  add_image_height_hack_image()
  framerate = get_framerate(input_file)
  generate_frame_images(input_file,framerate)
  audio_data = generate_audio_data(input_file)
  for entry in os.listdir("."):
    if os.path.isfile(entry) and entry.endswith("jpg"):
      # Turn a filename of the form 000032.jpg to 32
      seconds = int(os.path.splitext(entry)[0])
      # Hack to get around the image being smaller until it hits the max value
      if seconds == 0:
        final_height = 720
      else:
        try:
          final_height = int(audio_data[seconds-1]) + 1
        except:
          # If something goes wrong, just make it unnoticeable
          final_height = 1
      resize(entry)
      resize(entry,1,final_height)
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
