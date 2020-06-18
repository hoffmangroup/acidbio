import os
import argparse
import tempfile
import subprocess

import fuzz


def main(metabed_path: str, command: str, n: int, out: str):
    m = command.count('BED_FILE')
    for i in range(n):
        tempdir = tempfile.TemporaryDirectory()
        fuzz.main(metabed_path, tempdir.name, m)
        files = os.listdir(tempdir.name)

        print('Test number ' + str(i + 1))
        if m == 1:
            new_command = command.replace('BED_FILE', tempdir.name + '/' + files[0])
        else:
            new_command = command
            for l in range(m):
                new_command = new_command.replace('BED_FILE' + str(l+1), tempdir.name + '/' + files[l])
        # new_command = new_command.split()
        print(new_command)
        ret = subprocess.run(new_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        print(ret.stderr.decode('ascii'))
        with open(out, 'a') as f:
            f.write('Test number ' + str(i+1) + ':\n')
            f.write('Standard output:\n')
            f.write(ret.stdout.decode('ascii'))
            f.write('\nStandard error:\n')
            f.write(ret.stderr.decode('ascii'))
            f.write('\nBED file(s):\n')
        if m == 1:
            subprocess.run(['cat', tempdir.name + '/' + files[0]], stdout=open(out, 'a'))
        else:
            for l in range(m):
                f = open(out, 'a')
                f.write('File ' + str(l+1) + ':\n')
                result = subprocess.run(['cat', tempdir.name + '/' + files[l]], stdout=subprocess.PIPE)
                f.write(result.stdout.decode('ascii'))
                f.write('\n\n')
                f.close()
        with open(out, 'a') as f:
            f.write('=================================================\n\n')
        tempdir.cleanup()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Test a tool on a generated BED file.'
    )

    parser.add_argument('-n', help="Number of tests to run. Default is 1.")
    parser.add_argument('-o', help="File to write fuzzing outputs to. Default is 'test_results.txt'")
    parser.add_argument('metabed_path', help="Location of the metabed.g4 file.")
    parser.add_argument('command', help='Full command line usage of the tool. Wherever the BED file belongs, put "BED_FILE".' +
        ' If multiple BED files are required, write BED_FILE1, BED_FILE2, ...')
    args = parser.parse_args()
    n = args.n if args.n else 1
    f = args.o if args.o else 'test_results.txt'
    main(args.metabed_path, args.command, int(n), f)
