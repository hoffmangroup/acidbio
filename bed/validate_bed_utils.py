"""
Utilities for verifying non-strict BED
"""
import re
import decimal
import sys
from typing import List, Dict


def verify_rgb(rgb: str) -> bool:
    if re.match(r"^[0-9]+,[0-9]+,[0-9]+$", rgb):
        r,g,b = map(int, rgb.split(','))
        return 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255
    else:
        return False


def verify_browser_line(browser_line: str, sizes: Dict[str, int], line: int) -> bool:
    split = browser_line.split()[1: ]
    if split[0] not in ['hide', 'dense', 'pack', 'squish', 'full', 'position']:
        sys.stdout.write("Line {} WARNING: invalid browser line option\n".format(line))
    elif split[0] == 'position':
        if not re.match(r"^chr\w+:\d+-\d+$", split[1]):
            sys.stdout.write("Line {} WARNING: browser position not of form chromosome:start-end\n".format(line))
        else:
            chrom, interval = split[1].split(':')
            start, end = map(int, interval.split('-'))
            if start < 0:
                sys.stdout.write("Line {} WARNING: browser start position is negative\n".format(line))
            elif start > 4294967295:
                sys.stdout.write("Line {} WARNING: browser start position is larger than integer size\n".format(line))
            if chrom not in sizes.keys():
                sys.stdout.write("Line {} WARNING: chrom not found in the chrom sizes file\n".format(line))
                if end > 4294967295:
                    sys.stdout.write("Line {} WARNING: browser end position is larger than integer size\n".format(line))
            elif end > sizes[chrom]:
                sys.stdout.write("Line {} WARNING: browser end position is larger than chrom size\n".format(line))
            if start > end:
                sys.stdout.write("Line {} WARNING: start position greater than end position\n".format(line))
    return True


def verify_track_line(browser_line: str, sizes: Dict[str, int], l: int) -> bool:
    line = browser_line[browser_line.index(' ') + 1:]
    r= re.compile('([^ =]+) *= *("[^"]*"|[^ ]*)')

    d= {}
    # print(r.findall(line))
    for k, v in r.findall(line):
        if v[:1]=='"':
            d[k]= v[1:-1]
        elif not v.isnumeric():
            d[k] = v
        else:
            d[k]= float(v)
    for k, v in d.items():
        if k == 'name' and len(v) > 15:
            sys.stdout.write("Line {} WARNING: track name too long\n".format(l))
        elif k == 'description' and len(v) > 60:
            sys.stdout.write("Line {} WARNING: description too long\n".format(l))
        elif k == 'type' and isinstance(v, str) and v.lower() not in ['bam', 'bed detail', 'bedgraph', 'bigbarchart',
            'bigbed', 'bigchain', 'biggenepred', 'biginteract', 'bignarrowpeak', 'bigmaf', 'bigpsl', 'bigwig',
            'broadpeak', 'cram', 'interact', 'narrowpeak', 'microarray', 'vcf', 'wig', 'bed']:
            sys.stdout.write("LINE {} WARNING: invalid track type\n".format(l))
        elif k == 'visibility' and isinstance(v, float) and int(v) not in [0, 1, 2, 3, 4]:
            sys.stdout.write("Line {} WARNING: invalid track visibility\n".format(l))
        elif k == 'visibility' and isinstance(v, str) and v not in ['hide', 'dense', 'full', 'pack', 'squish']:
            sys.stdout.write("Line {} WARNING: invalid track visibility\n".format(l))
        elif k == 'color' and isinstance(v, str) and not verify_rgb(v):
            sys.stdout.write("Line {} WARNING: track color invalid\n".format(l))
        elif k == 'itemRgb' and isinstance(v, str) and v.lower() != 'on':
            sys.stdout.write('Line {} WARNING: itemRgb track attribute should be "On" or not set\n'.format(l))
        elif k == 'colorByStrand' and isinstance(v, str):
            color1, color2 = v.split(' ')
            if not (verify_rgb(color1) and verify_rgb(color2)):
                sys.stdout.write('Line {} WARNING: colorByStrand has invalid colors\n'.format(l))
        elif k == 'useScore' and isinstance(v, float) and int(v) not in [0, 1]:
            sys.stdout.write("Line {} WARNING: invalid useScore attribute\n".format(l))
        elif k in ['color', 'itemRgb', 'colorByStrand', 'type', 'group', 'db', 'url', 'htmlUrl',
         'bigDataUrl'] and not isinstance(v, str):
            sys.stdout.write("Line {} WARNING: Attribute expected to be a string\n".format(l))
        elif k in ['maxItems', 'offset', 'priority', 'useScore'] and not isinstance(v, float):
            sys.stdout.write("Line {} WARNING: Attribute expected to be a number\n".format(l))
        elif k not in ['name', 'description', 'type', 'visibility', 'color', 'itemRgb', 'colorByStrand',
            'useScore', 'group', 'priority', 'db', 'offset', 'maxItems', 'url', 'htmlUrl', 'bigDataUrl']:
            sys.stdout.write("Line {} WARNING: Invalid track attribute\n".format(l))
    return True


def check_chrom(split_line: List[str], sizes: Dict[str, int], line: int) -> bool:
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
    l = split_line[10].strip(',')
    sizelist = l.split(',')
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
    if is_all_numeric and not all(int(startlist[i]) <= int(startlist[i+1]) for i in range(len(startlist)-1)):
        sys.stdout.write("Line {} WARNING: blockStarts are not sorted\n".format(line))
    elif is_all_numeric and len(sizelist) == len(startlist):  # sorted and of same size
        prev = 0
        for i in range(len(sizelist)):
            if int(startlist[i]) < prev:
                sys.stdout.write("Line {} WARNING: overlapping blocks\n".format(line))
            prev = int(sizelist[i]) + int(startlist[i])
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
