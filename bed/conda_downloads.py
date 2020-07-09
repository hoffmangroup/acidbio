from condastats.cli import overall
from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

if __name__ == '__main__':
    stream = open('config.yaml', 'r')
    data = load(stream, Loader=Loader)

    names = []
    counts = []

    packages = data['conda-environment']
    for package in packages.keys():
        res = overall(package)
        try:
            count = res[package]
            names.append(package)
            counts.append(count)
        except:
            print(package)
    print(names, counts)
    ordered = sorted(zip(counts, names))
    for i in ordered:
        print(i)
