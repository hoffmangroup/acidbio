"""
Summarize the results arrays into one-page heatmaps
"""
import argparse
import sys
import pickle
from glob import glob

import matplotlib.pyplot as plt

from more_itertools import sort_together

import seaborn as sns; sns.set(font_scale=2.3)

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
    args = parser.parse_args()

    files = []
    for f in args.results_file:
        files.extend(glob(f))
    
    if len(files) == 0:
        sys.stderr.write('No files found matching the globs\n')
        exit(1)

    # bed_correctness is a mapping of tool names to a dictionary where
    # the number of tests is mapped to the proportion of tests passed
    # Later, the number of tests is sorted to reveal BED3, ..., BED12
    # since BED3 will have the least tests, BED12 has the most, etc.
    bed_correctness = {}
    for file in files:
        with open(file, 'rb') as f:  # open each result array file
            l = pickle.load(f)
            num_correct = l[0]
            correct_list = l[1]
            name_list = l[2]
            for i in range(len(num_correct)):
                # this version aggregates over the main tool, using
                # the best performing subtool as the representative
                name = name_list[i][:name_list[i].find(' ')]

                if name not in bed_correctness:
                    bed_correctness[name] = {}
                if len(correct_list) in bed_correctness[name]:
                    bed_correctness[name][len(correct_list[i])] = \
                        max(bed_correctness[name][len(correct_list[i])],
                            num_correct[i] / (len(correct_list[i]) - 1))
                else:
                    bed_correctness[name][len(correct_list[i])] = \
                        num_correct[i] / (len(correct_list[i]) - 1)

    programs = list(bed_correctness.keys())
    lengths = sorted(list(bed_correctness[programs[0]].keys()))

    # heatmap_array is a list of lists where each list is of length 10 with
    # the proportion of passing tests from BED3 to BED12 in order.
    # sorting_temp holds the sum of the proportions to rank tools from
    # overall best parser to worse parser.
    heatmap_array = []
    sorting_temp = []
    for program in programs:
        heatmap_array.append(
            [bed_correctness[program][length] for length in lengths])
        sorting_temp.append(sum(heatmap_array[-1]))
    
    programs, heatmap_array, sorting_temp = sort_together(
        [programs, heatmap_array, sorting_temp], key_list=[2]
    )
    
    plt.figure(figsize=(39, 50))

    sizing = {'fontsize': 48}
    ax = sns.heatmap(heatmap_array, cmap=plt.get_cmap('bwr'),
        vmin=0, vmax=1, square=False, linewidths=.5, xticklabels=BED_NAMES,
        yticklabels=programs, annot=True, cbar=True,
        cbar_kws={"fraction": 0.03, "pad": 0.01}
    )
    
    ax.set_ylabel('Tools', **sizing)
    ax.set_xlabel('Bed types', **sizing)

    # plt.title("Percentage of passing test cases for each BED type")
    plt.xticks(rotation='horizontal')
    plt.tight_layout()
    plt.savefig(args.outfile_filepath)
