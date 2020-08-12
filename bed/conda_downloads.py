from condastats.cli import overall
from yaml import load
import os

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

if __name__ == '__main__':
    stream = open('config.yaml', 'r')
    data = load(stream, Loader=Loader)

    names = []
    counts = []

    # packages = data['conda-environment']
    packages = os.listdir('./bioconda-recipes-master/recipes')
    res = overall(packages)
    for package in packages:
        try:
            count = res[package]
            names.append(package)
            counts.append(count)
        except:
            print(package)
    # print(names, counts)
    ordered = sorted(zip(counts, names))
    with open('top_tools_overall.txt', 'w') as f:
        for i in reversed(ordered):
            print(i, file=f)
