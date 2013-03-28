We were curious — can you tell the tone of a movie from the hue of a frame, or 
the amplitude of the sound? We were inspired by previous film visualization 
efforts like Movie Barcodes, which compress every frame of a film to show the 
overall hue of the movie. A change of hue in certain films and television shows 
is integral to the plot — think The Wizard of Oz — and by looking at these 
visualizations, you can understand tone shifts as the narrative unfolds. By 
visualizing both hue and sound, we’d like to try and identify key events and 
tonal shifts without seeing a single frame.

You will need to install the following unix utilities:
mplayer
ffmpeg
imagemagick
sox

The script that does the work is main.py. Usage:
python main.py /path/to/movie.avi

It will do processing on the input movie and output a png.
We create this color waveform through the sound and amplitude for each frame. 
To find color per frame, we compress each frame down into a one pixel image, 
creating the average color per frame. The process is repeated for the entire 
film.

Included are some examples
