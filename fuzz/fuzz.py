import argparse
import subprocess
import tempfile
import random
from os import listdir
from os.path import isfile, join

# 1. Use metabed.g4 to generate different bed.g4 files
# 2. Using the bed.g4, generate a series of BED files and concat together

def generate_bed_g4(tempdir):
    subprocess.run(['grammarinator-generate', '-p', tempdir.name + '/metabedUnparser.py',
     '-l', tempdir.name + '/metabedUnlexer.py', '-o', tempdir.name + '/bedgen.g4'])


def generate_bed_file(tempdir, outfile_obj, n):
    for i in range(n):
        length = random.randint(1, 100)
        bed_dir = tempfile.TemporaryDirectory()
        generate_bed_g4(tempdir)
        bedg4 = tempdir.name + '/' + listdir(tempdir.name)[1]
        subprocess.run(['grammarinator-process', '-o', tempdir.name, '--no-actions', bedg4])
        for _ in range(length):
            subprocess.run(['grammarinator-generate', '-p', tempdir.name + '/bedUnparser.py',
             '-l', tempdir.name + '/bedUnlexer.py', '-o', bed_dir.name])
        generated_files = listdir(bed_dir.name)
        for j in range(len(generated_files)):
            generated_files[j] = bed_dir.name + '/' +  generated_files[j]
        subprocess.run(['cat'] + generated_files, stdout=outfile_obj)


if __name__ == '__main__':
    metabed_path = './metabed.g4'
    tempdir = tempfile.TemporaryDirectory()
    subprocess.run(['grammarinator-process', '-o', tempdir.name, '--no-actions', metabed_path])
    outfile_obj = open('./test.bed', 'w')
    generate_bed_file(tempdir, outfile_obj , 1)
    tempdir.cleanup()
