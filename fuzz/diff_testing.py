import os
import argparse
import tempfile
import subprocess

import fuzz


STDOUT_MESSAGES = ['wrong file format', 'Skipping line:', 'ERROR:', 'WARNING:']
STDERR_MESSAGES = ['Error', 'java.lang.RuntimeException', 'WARNING:',
                   'invalid BED', 'FileFormatWarning', '[W::']
CHROM_SIZES_LOCATION = '../bed/data/hg38.chrom.sizes'
INVOCATION = 'bedToBigBed {} {} {}'


def detect_problem(out, err):
    """
    Searches <out> and <err> for signs of the tool finding
    something wrong with the BED file.
    <out> and <err> should be in encoded form.

    out: stdout of the tool
    err: stderr of the tool
    """
    try:
        out = out.decode('UTF-8')
    except UnicodeDecodeError:
        out = "Non-unicode characters present in output"
    try:
        err = err.decode('UTF-8')
    except UnicodeDecodeError:
        err = "Non-unicode characters present in output"
    for msg in STDOUT_MESSAGES:
        if msg in out:
            return True
    for msg in STDERR_MESSAGES:
        if msg in err:
            return True
    return False


def bb_check(tmpdir, files):
    tmpfile = tempfile.NamedTemporaryFile()
    bb_out = tempfile.NamedTemporaryFile()
    for file in files:
        subprocess.run('sort -k1,1 -k2,2n {} > {}'.format(
            tmpdir.name + '/' + file, tmpfile.name), shell=True)

        ret = subprocess.run(
            INVOCATION.format(tmpfile.name, CHROM_SIZES_LOCATION, bb_out.name),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )
        if ret.returncode != 0:
            return False
    return True


def write_to_log(ret, out, tmpdir, files, m, i):
    print(ret.stderr.decode('ascii'))
    with open(out, 'a') as f:
        f.write('Test number ' + str(i+1) + ':\n')
        f.write('Standard output:\n')
        f.write(ret.stdout.decode('ascii'))
        f.write('\nStandard error:\n')
        f.write(ret.stderr.decode('ascii'))
        f.write('\nBED file(s):\n')
    if m == 1:
        subprocess.run(
            ['cat', tmpdir.name + '/' + files[0]], stdout=open(out, 'a')
        )
    else:
        for l in range(m):
            f = open(out, 'a')
            f.write('File ' + str(l+1) + ':\n')
            result = subprocess.run(
                ['cat', tmpdir.name + '/' + files[l]],
                stdout=subprocess.PIPE
            )
            f.write(result.stdout.decode('ascii'))
            f.write('\n\n')
            f.close()
    with open(out, 'a') as f:
        f.write('End of test number ' + str(i+1) + '\n\n')


def main(metabed_path: str, command: str, n: int, out: str):
    m = command.count('BED_FILE')
    for i in range(n):
        tmpdir = tempfile.TemporaryDirectory()
        fuzz.main(metabed_path, tmpdir.name, m)
        files = os.listdir(tmpdir.name)

        print('Test number ' + str(i + 1))
        if m == 1:
            new_command = command.replace(
                'BED_FILE', tmpdir.name + '/' + files[0]
            )
        else:
            new_command = command
            for l in range(m):
                new_command = new_command.replace(
                    'BED_FILE' + str(l+1), tmpdir.name + '/' + files[l]
                )
        print(new_command)
        ret = subprocess.run(new_command, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, shell=True)
        bed_valid = bb_check(tmpdir, files)
        tool_valid = not detect_problem(ret.stdout, ret.stderr) \
            and ret.returncode == 0
        print(bed_valid, tool_valid)
        if bed_valid != tool_valid:
            write_to_log(ret, out, tmpdir, files, m, i)
        tmpdir.cleanup()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Test a tool on a generated BED file.'
    )

    parser.add_argument('-n', help="Number of tests to run. Default is 1.")
    parser.add_argument(
        '-o',
        help="File to write fuzzing outputs to. Default is 'test_results.txt'"
    )
    parser.add_argument(
        'metabed_path',
        help="Location of the metabed.g4 file."
    )
    parser.add_argument(
        'command',
        help='Full command line usage of the tool. Wherever the BED file' +
        ' belongs, put "BED_FILE". If multiple BED files are required,' +
        ' write BED_FILE1, BED_FILE2, ...'
    )
    args = parser.parse_args()
    n = args.n if args.n else 1
    f = args.o if args.o else 'test_results.txt'
    main(args.metabed_path, args.command, int(n), f)
