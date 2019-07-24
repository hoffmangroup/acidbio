"""
Takes the binary results array outputted from run_all.py and combines them
into one heatmap sorted by the number of correct cases.
"""
import os
import sys
import argparse
import pickle
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
from glob import glob
from numpy import spacing
from more_itertools import sort_together


def get_file_names():
    """
    Returns a list of all the test cases in the order that they were used
    """
    file_names = []
    for directory in os.listdir("./good/"):
        for file in os.listdir("./good/" + directory):
            if file.endswith(".bed"): file_names.append(file)
    file_names.append("")
    for directory in os.listdir("./less_good"):
        for file in os.listdir("./less_good/" + directory):
            if file.endswith(".bed"): file_names.append(file)
    file_names.extend(["", "", ""])
    for directory in os.listdir("./less_bad"):
        for file in os.listdir("./less_bad/" + directory):
            if file.endswith(".bed"): file_names.append(file)
    file_names.append("")
    for directory in os.listdir("./bad/"):
        for file in os.listdir("./bad/" + directory):
            if file.endswith(".bed"): file_names.append(file)
    return file_names


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Takes the results arrays containing the data obtained from" + 
        "run_all.py and combines them into a sorted heatmap")
    parser.add_argument("-V", "--version", action='version', version='0.1')
    parser.add_argument("results_file", metavar="results-array-file",
        help="result array file(s). Can be regular expressions", nargs="+")
    parser.add_argument("outfile_filepath", metavar="outfile-filepath",
        help="full filepath to output image file containing the heatmap." + 
        "(eps, pdf, png, raw, rgba, svg, jpg, jpeg, tif, tiff)")
    args = parser.parse_args()

    files = []
    for f in args.results_file:
        files.extend(glob(f))

    if len(files) == 0:
        sys.stderr.write("No files found matching the file regexps\n")
        exit(1)

    file_list = get_file_names()

    num_correct = []
    correct_list = []
    name_list = []

    for file in files:
        with open(file, 'rb') as f:
            l = pickle.load(f)
            num_correct.extend(list(l[0]))
            correct_list.extend(list(l[1]))
            name_list.extend(list(l[2]))

    # Sort the tools by number of correctly passed cases
    num_correct, correct_list, name_list = sort_together([num_correct, correct_list, name_list], key_list=[0, 2])

    # Redefine the values from the correct arrays to match with colors of the viridis colormap
    for j in range(len(correct_list)):
        for n, i in enumerate(correct_list[j]):
            if i == 0.0:  # Incorrect case mapped to blue
                correct_list[j][n] = 0.25
            elif i == 1.0:  # Correct case mapped to green
                correct_list[j][n] = 0.72
            elif i == 0.5:  # Directory separators mapped to white
                correct_list[j][n] = 0

    new_cmap = plt.get_cmap('viridis')
    new_cmap.set_under('white')
    plt.figure(figsize=(23,21))

    ax = sns.heatmap(correct_list, cmap=new_cmap, vmin=spacing(0.0), vmax=1, linewidths=.5, 
        square=True, cbar=False, xticklabels=file_list, yticklabels=name_list)

    ax.set_ylabel('TOOLS')
    ax.set_xlabel('TEST CASES')
    
    plt.title("Strict good" + " "*65 + "Non-strict good" + " "*61 + "Non-strict bad" + " "*60 + "Strict bad")
    plt.viridis()
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(args.outfile_filepath)
