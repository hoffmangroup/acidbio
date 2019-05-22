import re

def verify_browser_line(line: str) -> bool:
    """Verifies if a browser line is of proper format
    """
    line = line.strip()
    if line in ['browser hide all', 'browser dense all', 'browser pack all', 'browser squish all', 'browser full all']:
        return True
    split = line.split()
    if len() != 3:  # There are always three words in a browser line.
        return False
    if split[1] not in ['position', 'hide', 'dense', 'pack', 'squish', 'full']:
        return False
    if split[1] == 'position':
        if re.match("chr\d+:\d+-\d+", line) is not None:
            return True
        return False
    return True


def verify_track_line(line: str) -> bool:
    """Verifies if a track line is of proper format
    """
    pass


def verify_bed_line(line: str) -> bool:
    """Verifies if a bed line is of proper format
    """
    split = line.split("\t")


def check_chrom(attribute: str) -> bool:
    return re.match(r"^[0-9a-zA-Z]+$", attribute.strip()) is not None


def check_chrom_start_end(start: str, end: str) -> bool:
    if not start.isdigit() or not end.isdigit():  # Checks if they are integers
        return False
    start = int(start)
    end = int(end)
    return not (start < 0 or end < 0 or start > end)

def check_name(name: str) -> bool:
    return name.count(" ") == 0  # It just cannot contain spaces


def check_score(score: str) -> bool:
    if score == '.':
        return True
    elif not score.isdigit():
        return False
    return 0 <= score <= 1000

def check_strand(strand: str) -> bool:
    return strand in ['+', '-', '.']


def check_thick_start_end(start: str, end: str, chrom_start: str, chrom_end: str) -> bool:
    # It is inferred that chrom_start and chrom_end are both nonnegative integers since they would have already
    # passed the check_chrom_start_end test
    chrom_start = int(chrom_start)
    chrom_end = int(chrom_end)
    if not start.isdigit():
        return False
    start = int(start)
    if end is None:
        return chrom_start <= start <= chrom_end
    if not end.isdigit():
        return False
    end = int(end)
    return start <= end and end <= chrom_end


def check_itemRgb(rgb: str) -> bool:
    try:
        red, blue, green = rgb.split(',')
        if not red.isdigit() or not blue.isdigit() or not green.isdigit():
            return False
    except ValueError:
        return False
    
    
