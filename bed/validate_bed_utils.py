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
            sys.stdout.write("Line {}: WARNING chrom not found in the chrom sizes file\n".format(line))
        return True
    else:
        sys.stdout.write("Line {}: ERROR chrom must contain only a-z, A-Z, 0-9, and underscores only\n".format(line))
        return False


def check_chrom_start(split_line: List[str], sizes: Dict[str, int], line: int) -> bool:
    chr_name = split_line[0]
    if split_line[1].isnumeric():
        if 0 <= int(split_line[1]) <= 4294967295:
            if chr_name in sizes.keys() and sizes[chr_name] < int(split_line[1]):
                sys.stdout.write("Line {}: WARNING chromStart is bigger than the size of the chromosome\n".format(line))
            return True
        elif int(split_line[1]) < 0:
            sys.stdout.write("Line {}: ERROR chromStart is negative\n".format(line))
            return False
        else:
            sys.stdout.write("Line {}: ERROR chromStart is greater than the size of an integer\n".format(line))
            return False
    else:
        sys.stdout.write("Line {}: ERROR chromStart is not a number\n".format(line))
        return False


def check_chrom_end(split_line: List[str], sizes: Dict[str, int], line: int) -> bool:
    chr_name = split_line[0]
    start = int(split_line[1])
    if split_line[1].isnumeric():
        if start <= int(split_line[1]) <= 4294967295 :
            if chr_name in sizes.keys() and sizes[chr_name] < int(split_line[1]):
                sys.stdout.write("Line {}: WARNING chromEnd is bigger than the size of the chromosome\n".format(line))
            return True
        elif int(split_line[1]) < start:
            sys.stdout.write("Line {}: ERROR chromEnd is less than chromStart\n".format(line))
            return False
        else:
            sys.stdout.write("Line {}: ERROR chromEnd is greater than the size of an integer\n".format(line))
            return False
    else:
        sys.stdout.write("Line {}: ERROR chromEnd is not a number\n".format(line))
        return False


def check_name(split_line: List[str], sizes: Dict[str, int], line: int) -> bool:
    if re.match(r"[^\s]+", split_line[3]):
        return True
    else:
        sys.stdout.write("Line {}: ERROR name should be non-whitespace characters\n".format(line))
        return False


def check_score(split_line: List[str], sizes: Dict[str, int], line: int) -> bool:
    try:
        score = float(split_line[4])
        if not score.is_integer():
            sys.stdout.write("Line {}: WARNING score is a whole number\n".format(line))
        elif score < 0:
            sys.stdout.write("Line {}: WARNING score is less than zero\n".format(line))
        elif score > 1000:
            sys.stdout.write("Line {}: WARNING: score is greater than 1000".format(line))
        return True
    except ValueError:
        sys.stdout.write("Line {}: ERROR score should be a numeric value\n".format(line))
        return False


def check_strand(split_line: List[str], sizes: Dict[str, int], line: int) -> bool:
    return split_line[5] in ['+', '-', '.']


def check_thick_start(split_line: List[str], sizes: Dict[str, int], line: int) -> bool:
    return split_line[6].isnumeric()  and 0 <= int(split_line[6]) <= 4294967295


def check_thick_end(split_line: List[str], sizes: Dict[str, int], line: int) -> bool:
    return split_line[7].isnumeric() and 0 <= int(split_line[7]) <= 4294967295


def ignored(split_line: List[str], sizes: Dict[str, int], line: int) -> bool:
    return True


def verify_bed_line(bed_line: str, sizes: Dict[str, int], line: int) -> bool:
    """
    Verifies that a BED line is valid.
    """
    function_list = [check_chrom, check_chrom_start, check_chrom_end, check_name, check_score,
        check_score, check_strand, check_thick_start, check_thick_end, ignored, ignored, ignored, ignored]
    split_line = bed_line.split()
    for i in range(len(split_line)):
        split_line[i] = split_line[i].strip()
    for i in range(len(split_line)):
        if not function_list[i](split_line, sizes, line):
            return False
    return True
