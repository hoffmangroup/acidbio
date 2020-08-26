import tempfile
import argparse
import os

from yaml import load, dump
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from run_all import run_all

PASSING_PERCENTAGE_URL = "https://img.shields.io/badge/BED{}--BED{}-{}%25-{}"


# Pretend that <tool> is the name of a tool from the URL parser
def get_badge(tool, save_yaml, bed_start, bed_end):
    if os.path.exists(save_yaml):
        with open(save_yaml) as f:
            saved = load(f, Loader=Loader)
            if saved is None:
                saved = dict()
            if tool in saved.keys() and bed_start in saved[tool] and \
                    bed_end in saved[tool][bed_start]:
                print('BED parser URL:', saved[tool][bed_start][bed_end][0])
                print('BED passing rate URL:',
                      saved[tool][bed_start][bed_end][1])
                return saved[tool][bed_start][bed_end]
    else:
        saved = dict()

    # Temporary file to store results, won't be used.
    trash_file = tempfile.NamedTemporaryFile()

    # Whether it passes the threshold or not for each BED version
    passing = [False for _ in range(10)]

    # Pass rates
    passing_rates = [None for _ in range(10)]

    for i in range(bed_start + 3, bed_end + 4):
        num_correct, correct_list, name_list = run_all(
            "BED" + str(i).zfill(2), trash_file.name, tool
        )
        summed_passing_rate = sum(num_correct) / len(num_correct)
        tools_in_package = len(correct_list[0]) - 1

        if summed_passing_rate / tools_in_package >= 0.7:
            passing[i-3] = True
        passing_rates[i-3] = summed_passing_rate / tools_in_package

    bed_parser_url = "https://img.shields.io/badge/BED Parser-"
    for i in range(10):
        if passing[i]:
            bed_parser_url += "BED{} %7C".format(i+3)
    bed_parser_url = bed_parser_url[:-4] + "-informational"
    print('BED parser URL: ' + bed_parser_url)

    passing_rate = round(sum(passing_rates[bed_start:bed_end+1]) /
                            (bed_end - bed_start + 1), 2) * 100
    if passing_rate == 1:
        color = 'green'
    elif passing_rate >= 0.5:
        color = 'yellow'
    else:
        color = 'red'
    bed_passing_url = PASSING_PERCENTAGE_URL.format(
        bed_start+3, bed_end+3, passing_rate, color
    )
    print('BED passing rate URL: ', bed_passing_url)

    if tool not in saved:
        saved[tool] = dict()
        saved[tool][bed_start] = dict()
        saved[tool][bed_start][bed_end] = [bed_parser_url, bed_passing_url]
    elif bed_start not in saved[tool]:
        saved[tool][bed_start] = dict()
        saved[tool][bed_start][bed_end] = [bed_parser_url, bed_passing_url]
    elif bed_end not in saved[tool][bed_start]:
        saved[tool][bed_start][bed_end] = [bed_parser_url, bed_passing_url]
    with open(save_yaml, 'w') as f:
        dump(saved, f)
    return bed_parser_url


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Get BED badge URLs")
    parser.add_argument('tool', help='Tool name')
    parser.add_argument('path',
                        help='Path to YAML file with saved tools and badges')
    parser.add_argument('start',
                        help='First BED variant to consider. e.g. BED3')
    parser.add_argument('end', help='Last BED variant to consider. e.g. BED6')
    args = parser.parse_args()
    bed_start = int(args.start[3:]) - 3
    bed_end = int(args.end[3:]) - 3

    get_badge(args.tool, args.path, bed_start, bed_end)
