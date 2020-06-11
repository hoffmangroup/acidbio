import os
import argparse
import tempfile
import subprocess

import fuzz


def main(metabed_path, command: str, n: int):
    tempdir = tempfile.TemporaryDirectory()
    fuzz.main(metabed_path, tempdir.name, n)
    i = 1
    for bed_file in os.listdir(tempdir.name):
        print('Test number ' + str(i))
        new_command = command.replace('BED_FILE', tempdir.name + '/' + bed_file)
        new_command = new_command.split()
        subprocess.call(new_command)
        i += 1
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Test a tool on a generated BED file.'
    )

    parser.add_argument('-n', help="Number of tests to run. Default is 1.")
    parser.add_argument('metabed_path', help="Location of the metabed.g4 file.")
    parser.add_argument('command', help='Full command line usage of the tool. Wherever the BED file belongs, put "BED_FILE"')
    args = parser.parse_args()
    n = args.n if args.n else 1
    main(args.metabed_path, args.command, int(n))
