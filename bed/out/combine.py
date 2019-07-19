import sys
import os
import pickle
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
from more_itertools import sort_together


cdict = {'red':  ((0.0, 0.8, 0.8),
                  (0.5, 1.0, 1.0),
                  (1.0, 0.0, 0.0)),

        'green': ((0.0, 0.0, 0.0),
                  (0.5, 1.0, 1.0),
                  (1.0, 0.3, 0.3)),

        'blue': ((0.0, 0.0, 0.0),
                  (0.5, 1.0, 1.0),
                  (1.0, 1.0, 1.0))
       }


def get_file_names():
    file_names = []
    for directory in os.listdir("../good/"):
        for file in os.listdir("../good/" + directory):
            if file.endswith(".bed"): file_names.append(file)
    file_names.append("")
    for directory in os.listdir("../less_good"):
        for file in os.listdir("../less_good/" + directory):
            if file.endswith(".bed"): file_names.append(file)
    file_names.extend(["", "", ""])
    for directory in os.listdir("../less_bad"):
        for file in os.listdir("../less_bad/" + directory):
            if file.endswith(".bed"): file_names.append(file)
    file_names.append("")
    for directory in os.listdir("../bad/"):
        for file in os.listdir("../bad/" + directory):
            if file.endswith(".bed"): file_names.append(file)
    return file_names


if __name__ == '__main__':
    file_list = get_file_names()

    num_correct = []
    correct_list = []
    name_list = []

    files = sys.argv[1:]
    for file in files:
        with open(file, 'rb') as f:
            l = pickle.load(f)
            num_correct.extend(list(l[0]))
            correct_list.extend(list(l[1]))
            name_list.extend(list(l[2]))

    num_correct, correct_list, name_list = sort_together([num_correct, correct_list, name_list], key_list=[0, 2])

    for j in range(len(correct_list)):
        for n, i in enumerate(correct_list[j]):
            if i == 0.0:
                correct_list[j][n] = 0.25
            elif i == 1.0:
                correct_list[j][n] = 0.72
            elif i == 0.5:
                correct_list[j][n] = 0

    GnRd = colors.LinearSegmentedColormap('GnRd', cdict)

    new_cmap = plt.get_cmap('viridis')
    new_cmap.set_under('white')
    plt.figure(figsize=(23,21))

    ax = sns.heatmap(correct_list, cmap=new_cmap, vmin=np.spacing(0.0), vmax=1, linewidths=.5, 
        square=True, cbar=False, xticklabels=file_list, yticklabels=name_list)

    ax.set_ylabel('TOOLS')
    ax.set_xlabel('TEST CASES')

    plt.title("Strict good" + " "*65 + "Non-strict good" + " "*61 + "Non-strict bad" + " "*60 + "Strict bad")
    plt.viridis()
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig('results_final.png')
