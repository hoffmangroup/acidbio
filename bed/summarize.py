"""
Summarize the results arrays into one-page heatmaps
"""
import argparse
import sys
import pickle
from glob import glob

import matplotlib.pyplot as plt

from more_itertools import sort_together

import seaborn as sns; sns.set()

BED_NAMES = ['BED3', 'BED4', 'BED5', 'BED6', 'BED7', 'BED8', 'BED9',
             'BED11', 'BED12']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Summarizes results arrays into a concise heatmap")
    parser.add_argument('-V', '--version', action='version', version='0.1')
    parser.add_argument('results_file', metavar='results-array-file',
        help='result array file(s). Can be glob patterns', nargs='+')
    parser.add_argument("outfile_filepath", metavar="outfile-filepath",
        help="full filepath to output image file containing" +
        " the heatmap. (eps, pdf, png, raw, rgba, svg, jpg," +
        " jpeg, tif, tiff)")
    args = parser.parse_args()

    files = []
    for f in args.results_file:
        files.extend(glob(f))
    
    if len(files) == 0:
        sys.stderr.write('No files found matching the globs\n')
        exit(1)

    bed_correctness = {}
    for file in files:
        with open(file, 'rb') as f:
            l = pickle.load(f)
            num_correct = l[0]
            correct_list = l[1]
            name_list = l[2]
            for i in range(len(num_correct)):
                name = name_list[i]
                if name not in bed_correctness:
                    bed_correctness[name] = {}
                bed_correctness[name][len(correct_list[i])] = \
                    num_correct[i] / (len(correct_list[i]) - 1)

    programs = list(bed_correctness.keys())
    lengths = sorted(list(bed_correctness[programs[0]].keys()))
    print(lengths)
    heatmap_array = []
    sorting_temp = []
    for program in programs:
        # print(program)
        # print(bed_correctness[program])
        heatmap_array.append(
            [bed_correctness[program][length] for length in lengths])
        sorting_temp.append(sum(heatmap_array[-1]))
    # print(sorting_temp)
    
    programs, heatmap_array, sorting_temp = sort_together(
        [programs, heatmap_array, sorting_temp], key_list=[2]
    )
    
    plt.figure(figsize=(39, 50))

    ax = sns.heatmap(heatmap_array, cmap=plt.get_cmap('bwr'),
        vmin=0, vmax=1, square=False, linewidths=.5, xticklabels=BED_NAMES,
        yticklabels=programs, annot=True, cbar=False
    )

    ax.set_ylabel('Tools')
    ax.set_xlabel('Bed types')

    # plt.title("Percentage of passing test cases for each BED type")
    plt.xticks(rotation='horizontal')
    plt.tight_layout()
    plt.savefig(args.outfile_filepath)
