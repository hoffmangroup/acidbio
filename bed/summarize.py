"""
Summarize the results arrays into one-page heatmaps
"""
import argparse
import sys
import pickle
import pdb
from glob import glob

import matplotlib.pyplot as plt
import numpy as np

from more_itertools import sort_together

import seaborn as sns;

BED_NAMES = ['BED3', 'BED4', 'BED5', 'BED6', 'BED7', 'BED8', 'BED9', 'BED10',
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
    parser.add_argument('--expand', action='store_true',
                        help="Do not combine subtools together")
    parser.add_argument('--mini', action='store_true',
                        help="Make plot smaller")
    args = parser.parse_args()

    sns.set(font_scale=0.6) if args.mini else sns.set(font_scale=2.3)

    files = []
    for f in args.results_file:
        files.extend(glob(f))
    
    if len(files) == 0:
        sys.stderr.write('No files found matching the globs\n')
        exit(1)

    # max_bed_correctness is a mapping of tool names to a dictionary where
    # the number of tests is mapped to the proportion of tests passed
    # Later, the number of tests is sorted to reveal BED3, ..., BED12
    # since BED3 will have the least tests, BED12 has the most, etc.
    max_bed_correctness = {}
    min_bed_correctness = {}
    # pdb.set_trace()
    for file in files:
        with open(file, 'rb') as f:  # open each result array file
            l = pickle.load(f)
            num_correct = l[0]
            correct_list = l[1]
            name_list = l[2]
            for i in range(len(num_correct)):
                if args.expand:
                    name = name_list[i]
                    if name not in max_bed_correctness:
                        max_bed_correctness[name] = {}
                    max_bed_correctness[name][len(correct_list[i])] = \
                        num_correct[i] / (len(correct_list[i]) - 1)
                else:
                    name = name_list[i][:name_list[i].find(' ')]

                    if name not in max_bed_correctness:
                        max_bed_correctness[name] = {}
                        min_bed_correctness[name] = {}
                    if len(correct_list[i]) in max_bed_correctness[name]:
                        max_bed_correctness[name][len(correct_list[i])] = \
                            max(max_bed_correctness[name][len(correct_list[i])],
                                num_correct[i] / (len(correct_list[i]) - 1))
                        min_bed_correctness[name][len(correct_list[i])] = \
                            min(min_bed_correctness[name][len(correct_list[i])],
                                num_correct[i] / (len(correct_list[i]) - 1))
                    else:
                        max_bed_correctness[name][len(correct_list[i])] = \
                            num_correct[i] / (len(correct_list[i]) - 1)
                        min_bed_correctness[name][len(correct_list[i])] = \
                            num_correct[i] / (len(correct_list[i]) - 1)

    if args.expand:
        min_bed_correctness = max_bed_correctness

    programs = list(max_bed_correctness.keys())
    lengths = sorted(list(max_bed_correctness[programs[0]].keys()))

    # heatmap_array is a list of lists where each list is of length 10 with
    # the proportion of passing tests from BED3 to BED12 in order.
    # sorting_temp holds the sum of the proportions to rank tools from
    # overall best parser to worse parser.
    heatmap_array = []
    sorting_temp = []
    display_array = []
    for program in programs:
        heatmap_array.append(
            [(max_bed_correctness[program][length] + min_bed_correctness[program][length]) / 2 for length in lengths])
        display_array.append(
            [str(round(min_bed_correctness[program][length], 2)) + ' / ' + str(round(max_bed_correctness[program][length], 2)) for length in lengths]
        )
        sorting_temp.append(sum(heatmap_array[-1]))
    
    programs, heatmap_array, display_array, sorting_temp = sort_together(
        [programs, heatmap_array, display_array, sorting_temp], key_list=[3]
    )

    annot = True if args.expand else np.array(display_array, dtype=object)
    fmt = '.2g' if args.expand else ''

    plt.figure(figsize=(10.5,13)) if args.mini else plt.figure(figsize=(39, 50))

    sizing = {'fontsize': 12} if args.mini else {'fontsize': 48}
    ax = sns.heatmap(heatmap_array, cmap=plt.get_cmap('bwr'),
        vmin=0, vmax=1, square=False, linewidths=.5, xticklabels=BED_NAMES,
        yticklabels=programs, annot=annot, cbar=True, fmt=fmt,
        cbar_kws={"fraction": 0.03, "pad": 0.01}
    )
    # ax = sns.heatmap(heatmap_array, cmap=plt.get_cmap('bwr'),
    #     vmin=0, vmax=1, linewidths=0.3, xticklabels=BED_NAMES,
    #     yticklabels=False, cbar=True, cbar_kws={'fraction': 0.03, 'pad': 0.01}
    # )
    
    ax.set_ylabel('Tools', **sizing)
    ax.set_xlabel('Bed types', **sizing)

    # plt.title("Percentage of passing test cases for each BED type")
    plt.xticks(rotation='horizontal')
    plt.tight_layout()
    plt.savefig(args.outfile_filepath)
