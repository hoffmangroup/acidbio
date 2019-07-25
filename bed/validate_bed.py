"""
Usage: validate_bed.py [filename]
filename is the file that should be validated.
"""
import sys
import argparse
import subprocess
import tempfile
from validate_bed_utils import *


def parse_sizes(size_file):
    sizes = {}
    for line in size_file.readlines():
        chr_name, size = line.strip().split()
        sizes[chr_name] = int(size)
    return sizes


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Verifies that a BED file conforms to the non-strict BED specification')
    parser.add_argument('chrom_sizes', metavar='chrom-sizes', type=argparse.FileType('r'),
        help="path to chrom sizes file")
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
        help="path to BED file to be verified. Default stdin")
    
    args = parser.parse_args()
   
    if args.infile.name[-4:] != '.bed':
        sys.stderr.write("File must be of .bed extension\n")
        exit(1)

    # First check if it satisfies strict BED. If so, then we don't need to check for non-strict
    temp = tempfile.NamedTemporaryFile()
    p = subprocess.Popen(['bedToBigBed', args.infile.name, args.chrom_sizes.name, temp.name],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _, err = p.communicate()

    if p.returncode == 0:
        sys.stdout.write("Your file conforms to the strict BED definition.\n")
        exit(0)

    sizes = parse_sizes(args.chrom_sizes)
    args.chrom_sizes.close()
    temp.close()

    i = 1
    correct = True
    for bed_line in args.infile.readlines():
        bed_line = bed_line.strip()
        if bed_line == "" or bed_line[0] == '#': continue  # The line is blank or a comment
        split_line = bed_line.split()
        if split_line[0] == 'browser':
            # verify_browser_line(bed_line)
            pass
        elif split_line[0] == 'track':
            # verify_track_line(bed_line)
            pass
        else:
            correct = correct and verify_bed_line(bed_line, sizes, i)
        i += 1
    
    if correct:
        sys.stdout.write("\nYour file conforms to non-strict BED, but not strict BED\n")
    else:
        sys.stdout.write("\nYour file does not conform to non-strict BED\n")
