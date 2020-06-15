import os
import argparse
import tempfile
import subprocess

import fuzz


def main(metabed_path, command: str, n: int):
    tempdir = tempfile.TemporaryDirectory()

    m = command.count('BED_FILE')

    fuzz.main(metabed_path, tempdir.name, n * m)
    files = os.listdir(tempdir.name)
    for i in range(n):
        print('Test number ' + str(i + 1))
        if m == 1:
            new_command = command.replace('BED_FILE', tempdir.name + '/' + files[i])
        else:
            new_command = command
            for l in range(m):
                new_command = new_command.replace('BED_FILE' + str(l+1), tempdir.name + '/' + files[i * m + l])
        new_command = new_command.split()
        print(new_command)
        ret = subprocess.run(new_command, capture_output=True, text=True)
        with open('test' + str(i + 1) + '.txt', 'w') as f:
            f.write('Generated input:\n')
            f.write('Standard output:\n')
            f.write(ret.stdout)
            f.write('Standard error:\n')
            f.write(ret.stderr)
            f.write('\nBED file:\n')
        if m == 1:
            subprocess.run(['cat', tempdir.name + '/' + files[i]], stdout=open('test' + str(i + 1) + '.txt', 'a'))
        else:
            
            for l in range(m):
                f = open('test' + str(i + 1) + '.txt', 'a')
                subprocess.run(['cat', tempdir.name + '/' + files[i * m + l]], stdout=f)
                f.write('\n\n')
    tempdir.cleanup()
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Test a tool on a generated BED file.'
    )

    parser.add_argument('-n', help="Number of tests to run. Default is 1.")
    parser.add_argument('metabed_path', help="Location of the metabed.g4 file.")
    parser.add_argument('command', help='Full command line usage of the tool. Wherever the BED file belongs, put "BED_FILE".' +
        ' If multiple BED files are required, write BED_FILE1, BED_FILE2, ...')
    args = parser.parse_args()
    n = args.n if args.n else 1
    main(args.metabed_path, args.command, int(n))
