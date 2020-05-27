import tempfile
import argparse

from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from run_all import run_all
# Do some URL stuff to get the tool name
# .
# .
# .

# Pretend that <tool> is the name of a tool from the URL parser
def get_badge(tool, save_yaml):
    
    with open(save_yaml) as f:
        saved = load(f, Loader=Loader)
        if tool in saved.keys():
            print('Generated: ' + saved[tool])
            return saved[tool]

    # Temporary file to store results, won't be used.
    trash_file = tempfile.NamedTemporaryFile()

    # Whether it passes the threshold or not for each BED version
    passing = [False for _ in range(10)]

    for i in range(3, 13):
        num_correct, correct_list, name_list = run_all(
            "BED" + str(i).zfill(2), trash_file.name, tool
        )

        if (sum(num_correct) / len(num_correct)) / (len(correct_list[0]) - 1) >= 0.7:
            passing[i-3] = True

    generated_url = "https://img.shields.io/badge/BED Parser-"
    for i in range(10):
        if passing[i]:
            generated_url += "BED{} %7C".format(i+3)
    generated_url = generated_url[:-4] + "-informational"
    print('Generated ' + generated_url)

    saved[tool] = generated_url
    with open(save_yaml, 'w') as f:
        dump(saved, f)
    return generated_url


if __name__ == '__main__':
    tool = input('Tool name: ')
    path = input('Path to saved_yaml: ')
    get_badge(tool, path)