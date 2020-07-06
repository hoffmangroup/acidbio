import argparse
import subprocess
import tempfile
import random
from os import listdir

# 1. Use metabed.g4 to generate different bed.g4 files
# 2. Using the bed.g4, generate a series of BED files and concat together


def generate_bed_g4(tempdir):
    subprocess.run(['grammarinator-generate',
                    '-p', tempdir.name + '/metabedUnparser.py',
                    '-l', tempdir.name + '/metabedUnlexer.py',
                    '-o', tempdir.name + '/bedgen.g4'])


def generate_bed_file(tempdir, outdir, n):
    generate_bed_g4(tempdir)
    bedg4 = tempdir.name + '/' + listdir(tempdir.name)[1]
    subprocess.run(['grammarinator-process', '-o', tempdir.name, bedg4])
    for i in range(n):
        length = random.randint(1, 31)
        bed_dir = tempfile.TemporaryDirectory()
        subprocess.run(['grammarinator-generate',
                        '-p', tempdir.name + '/bedUnparser.py',
                        '-l', tempdir.name + '/bedUnlexer.py',
                        '-n', str(length),
                        '-o', bed_dir.name])
        generated_files = listdir(bed_dir.name)
        for j in range(len(generated_files)):
            generated_files[j] = bed_dir.name + '/' + generated_files[j]
        subprocess.run(['cat'] + generated_files,
                       stdout=open(outdir + '/test_' + str(i) + '.bed', 'w'))
        bed_dir.cleanup()


def main(metabed_path, outdir, n):
    tempdir = tempfile.TemporaryDirectory()
    subprocess.run(['grammarinator-process', '-o', tempdir.name, metabed_path])
    generate_bed_file(tempdir, outdir, n)
    tempdir.cleanup()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Generate BED files from the BED grammar."
    )

    parser.add_argument('-n',
                        help="Number of BED files to generate. Default is 1.")
    parser.add_argument('metabed_path',
                        help='Location of the metabed.g4 file.')
    parser.add_argument('outdir', help='Directory to place BED files in.')

    args = parser.parse_args()
    n = args.n if args.n else 1
    main(args.metabed_path, args.outdir, int(n))
