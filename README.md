# GORF-Controller-Image-Encoder
ENCODER.PY
Gorf Controller Image Encoder v1.0

A valid version of Python 3.x must be installed on your computer in order to run
this program. Python is a free popular programming language for general tasks and
can be downloaded from www.python.org

encoder.py will translate a png into a byte array that the arduino will understand.
To use it, simply double click the encoder.py, and it will prompt for a filename of
an image in this directory. That includes the file extension, ".png". 
It can also be run directly from the command line with usage "encoder.py gorf.png"

New images can be based off of template.png - please be careful to not edit gray pixels
and to only use the given black, dark red, and red colors. The program uses the
exact color code to encode them as it only stores bright, dim, and off values for
the pixels, and it uses the gray pixels as guidelines.

The program will spit out properly formatted arduino C++ code containing a byte 
array, which can simply be copied and pasted into the arduino program. Pressing
enter after this will close the window.
