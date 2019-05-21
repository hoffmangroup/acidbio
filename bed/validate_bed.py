"""
Usage: validate_bed.py [filename]
filename is the file that should be validated.
"""

import sys

def verify_browser_line(line: str) -> bool:
    """Verifies if a browser line is of proper format
    """
    pass


def verify_track_line(line: str) -> bool:
    """Verifies if a track line is of proper format
    """
    pass


def verify_bed_line(line: str) -> bool:
    """Verifies if a bed line is of proper format
    """
    pass


if len(sys.argv) != 2:
    sys.stderr.write("Usage: validate_bed.py [filename]\n")
    quit(1)

filename = sys.argv[1]
if filename[-4:] != '.bed':
    sys.stderr.write("File must be of .bed extension\n")
    quit(1)

bed_file = open(filename, 'r')

for bed_line in bed_file.readlines():
    bed_line = bed_line.strip()
    split_line = bed_line.split()
    if split_line[0] == 'browser':
        verify_browser_line(bed_line)
    elif split_line[0] == 'track':
        verify_track_line(bed_line)
    else:
        verify_bed_line(bed_line)

bed_file.close()
