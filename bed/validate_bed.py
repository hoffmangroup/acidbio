"""
Usage: validate_bed.py [filename]
filename is the file that should be validated.
"""

import sys
from validate_bed_utils import *


if len(sys.argv) != 2:
    sys.stderr.write("Usage: validate_bed.py [filename]\n")
    quit(1)

filename = sys.argv[1]
if filename[-4:] != '.bed':
    sys.stderr.write("File must be of .bed extension\n")
    quit(1)

bed_file = open(filename, 'r')

for bed_line in bed_file.readlines():
    if bed_line[0] == '#':  # The line is a comment 
        continue
    split_line = bed_line.split()
    if split_line[0] == 'browser':
        verify_browser_line(bed_line)
    elif split_line[0] == 'track':
        verify_track_line(bed_line)
    else:
        verify_bed_line(bed_line)

bed_file.close()

