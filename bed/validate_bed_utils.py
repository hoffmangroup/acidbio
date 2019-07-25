"""
Utilities for verifying non-strict BED
"""
import re
import sys
from typing import List, Dict


def verify_browser_line(browser_line):
    return False


def verify_track_line(track_line):
    return False


def check_chrom(split_line: List[str], sizes: Dict[str, int], line: int) -> bool:
    """
    Verifies the chrom field
    """
    chr_name = split_line[0]
    if re.match(r"\w+", chr_name):
        if chr_name not in sizes.keys():
            sys.stdout.write("Line {} WARNING: chrom not found in the chrom sizes file\n".format(line))
        return True
    else:
        sys.stdout.write("Line {} ERROR: chrom must contain only a-z, A-Z, 0-9, and underscores only\n".format(line))
        return False


def check_chrom_start(split_line: List[str], sizes: Dict[str, int], line: int) -> bool:
    chr_name = split_line[0]
    if split_line[1].isnumeric():
        if 0 <= int(split_line[1]) <= 4294967295:
            if chr_name in sizes.keys() and sizes[chr_name] < int(split_line[1]):
                sys.stdout.write("Line {} WARNING: chromStart is bigger than the size of the chromosome\n".format(line))
            return True
        elif int(split_line[1]) < 0:
            sys.stdout.write("Line {} ERROR: chromStart is negative\n".format(line))
            return False
        else:
            sys.stdout.write("Line {} ERROR: chromStart is greater than the size of an integer\n".format(line))
            return False
    else:
        sys.stdout.write("Line {} ERROR: chromStart is not a number\n".format(line))
        return False


def check_chrom_end(split_line: List[str], sizes: Dict[str, int], line: int) -> bool:
    chr_name = split_line[0]
    start = int(split_line[1])
    if split_line[2].isnumeric():
        if start <= int(split_line[2]) <= 4294967295 :
            if chr_name in sizes.keys() and sizes[chr_name] < int(split_line[1]):
                sys.stdout.write("Line {} WARNING: chromEnd is bigger than the size of the chromosome\n".format(line))
            return True
        elif int(split_line[2]) < start:
            sys.stdout.write("Line {} ERROR: chromEnd is less than chromStart\n".format(line))
            return False
        else:
            sys.stdout.write("Line {} ERROR: chromEnd is greater than the size of an integer\n".format(line))
            return False
    else:
        sys.stdout.write("Line {} ERROR: chromEnd is not a number\n".format(line))
        return False


def check_name(split_line: List[str], sizes: Dict[str, int], line: int) -> bool:
    if re.match(r"[^\s]+", split_line[3]):
        return True
    else:
        sys.stdout.write("Line {} ERROR: name should be non-whitespace characters\n".format(line))
        return False


def check_score(split_line: List[str], sizes: Dict[str, int], line: int) -> bool:
    try:
        score = float(split_line[4])
        if not score.is_integer():
            sys.stdout.write("Line {} WARNING: score is a whole number\n".format(line))
        elif score < 0:
            sys.stdout.write("Line {} WARNING: score is less than zero\n".format(line))
        elif score > 1000:
            sys.stdout.write("Line {} WARNING:: score is greater than 1000".format(line))
        return True
    except ValueError:
        sys.stdout.write("Line {} ERROR: score should be a numeric value\n".format(line))
        return False


def check_strand(split_line: List[str], sizes: Dict[str, int], line: int) -> bool:
    if split_line[5] in ['+', '-', '.']:
        return True
    else:
        sys.stdout.write("Line {} ERROR: strand should be one of + or - or .\n".format(line))
        return False


def check_thick_start(split_line: List[str], sizes: Dict[str, int], line: int) -> bool:
    start = int(split_line[1])
    end = int(split_line[2])
    if split_line[6].isnumeric():
        if int(split_line[6]) < start:
            sys.stdout.write("Line {} WARNING: thickStart is less than chromStart\n".format(line))
        elif int(split_line[6]) > end:
            sys.stdout.write("Line {} WARNING: thickStart is greater than chromEnd\n".format(line))
        return True
    else:
        sys.stdout.write("Line {} ERROR: thickStart is not a number\n".format(line))
        return False
    

def check_thick_end(split_line: List[str], sizes: Dict[str, int], line: int) -> bool:
    start = int(split_line[1])
    end = int(split_line[2])
    thickstart = int(split_line[6])
    if split_line[6].isnumeric():
        if int(split_line[7]) < thickstart:
            sys.stdout.write("Line {} WARNING: thickEnd is less than thickStart\n".format(line))
        elif int(split_line[7]) < start:
            sys.stdout.write("Line {} WARNING: thickEnd is less than chromStart\n".format(line))
        elif int(split_line[7]) > end:
            sys.stdout.write("Line {} WARNING: thickEnd is greater than chromEnd\n".format(line))
        return True
    else:
        sys.stdout.write("Line {} ERROR: thickEnd is not a number\n".format(line))
        return False


def check_itemrgb(split_line: List[str], sizes: Dict[str, int], line: int) -> bool:
    rgb = split_line[8]
    if rgb == '0':
        pass
    elif re.match(r"^[0-9]+,[0-9]+,[0-9]+$", rgb):
        r,g,b = map(int, rgb.split(','))
        if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
            sys.stdout.write("Line {} WARNING: itemRgb values are invalid\n".format(line))
    else:
        sys.stdout.write("Line {} WARNING: itemRgb is invalid. Value should be either 0 or three numbers".format(line) +
            " between 0 and 255 inclusive separated by commas\n")
    return True


def check_blockcount(split_line: List[str], sizes: Dict[str, int], line: int) -> bool:
    if split_line[9].isnumeric():
        if int(split_line[9]) <= 0:
            sys.stdout.write("Line {} WARNING: blockCount should be greater than 0\n".format(line))
    else:
        sys.stdout.write("Line {} WARNING: blockCount should be a whole number\n".format(line))
    return True


def check_blocksizes(split_line: List[str], sizes: Dict[str, int], line: int) -> bool:
    start = int(split_line[1])
    end = int(split_line[2])
    if split_line[9].isnumeric():
        if not re.match("^([0-9]+,){{{}}}[0-9]+,?$".format(int(split_line[9]) - 1), split_line[10]):
            sys.stdout.write("Line {} WARNING: inconsistent number of blocks in list and blockCount\n".format(line))
    sizelist = split_line[10].split(',')
    for s in sizelist:
        if s.isnumeric():
            if int(s) < 0:
                sys.stdout.write("Line {} WARNING: blockSize less than zero\n".format(line))
            elif int(s) > end - start:
                sys.stdout.write("Line {} WARNING: blockSize greater than length of annotation\n".format(line))
        else:
            sys.stdout.write("Line {} WARNING: blockSize is not a number\n".format(line))
    return True

# TODO: Still figure out how to do the overlapping blocks part
def check_blockstarts(split_line: List[str], sizes: Dict[str, int], line: int) -> bool:
    start = int(split_line[1])
    end = int(split_line[2])
    if split_line[9].isnumeric():
        if not re.match("^([0-9]+,){{{}}}[0-9]+,?$".format(int(split_line[9]) - 1), split_line[11]):
            sys.stdout.write("Line {} WARNING: inconsistent number of starts in list and blockCount\n".format(line))
    sizelist = split_line[10].split(',')
    startlist = split_line[11].split(',')
    is_all_numeric = True
    for s in startlist:
        if s.isnumeric():
            if int(s) < 0:
                sys.stdout.write("Line {} WARNING: blockStart less than zero\n".format(line))
            elif int(s) > end - start:
                sys.stdout.write("Line {} WARNING: blockStart greater than length of annotation\n".format(line))
        else:
            is_all_numeric = False
            sys.stdout.write("Line {} WARNING: blockStart is not a number\n".format(line))
    if startlist[0] != '0':
        sys.stdout.write("Line {} WARNING: first blockStart must be 0\n".format(line))
    if sizelist[-1].isnumeric() and startlist[-1].isnumeric() and int(sizelist[-1]) + int(startlist[-1]) != end - start:
        sys.stdout.write("Line {} WARNING: last block should end at chromEnd\n".format(line))
    if is_all_numeric and not all(sizelist[i] <= sizelist[i+1] for i in range(len(sizelist)-1)):
        sys.stdout.write("Line {} WARNING: blockStarts are not sorted\n".format(line))
    return True


def verify_bed_line(bed_line: str, sizes: Dict[str, int], line: int) -> bool:
    """
    Verifies that a BED line is valid.
    """
    function_list = [check_chrom, check_chrom_start, check_chrom_end, check_name, check_score, check_strand,
        check_thick_start, check_thick_end, check_itemrgb, check_blockcount, check_blocksizes, check_blockstarts]
    split_line = bed_line.split()
    if len(split_line) < 3:
        sys.stdout.write("Line {} ERROR: Fewer than 3 fields found\n".format(line))
        return False
    elif len(split_line) > 12:
        sys.stdout.write("Line {} ERROR: More than 12 fields found\n".format(line))
    for i in range(len(split_line)):
        split_line[i] = split_line[i].strip()
    for i in range(len(split_line)):
        if not function_list[i](split_line, sizes, line):
            return False
    return True
