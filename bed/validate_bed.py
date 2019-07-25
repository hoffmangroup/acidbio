"""
Usage: validate_bed.py [filename]
filename is the file that should be validated.
"""
import sys
import argparse
# from validate_bed_utils import *


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Verifies that a BED file conforms to the non-strict BED specification')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
        help="path to BED file to be verified")
    args = parser.parse_args()
   
    if args.infile.name[-4:] != '.bed':
        sys.stderr.write("File must be of .bed extension\n")
        exit(1)

    for bed_line in args.infile.readlines():
        bed_line = bed_line.strip()
        if bed_line == "" or bed_line[0] == '#': continue  # The line is blank or a comment
        split_line = bed_line.split()
        if split_line[0] == 'browser':
            verify_browser_line(bed_line)
        elif split_line[0] == 'track':
            verify_track_line(bed_line)
        else:
            verify_bed_line(bed_line)

    args.infile.close()
