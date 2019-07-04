# Runs all the tools in config.yaml
import os
import sys
import subprocess
import getopt
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from more_itertools import sort_together
from run_bad import run_bad
from run_good import run_good
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


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
    for directory in os.listdir("./good/"):
        for file in os.listdir("./good/" + directory):
            if file.endswith(".bed"): file_names.append(file)
    file_names.append("")
    for directory in os.listdir("./bad/"):
        for file in os.listdir("./bad/" + directory):
            if file.endswith(".bed"): file_names.append(file)
    return file_names


def run_all(verbose=False, failed_good_file="out/failed_good.txt", passed_bad_file="out/passed_bad.txt"):
    # Clear the previous data and reinitalize it
    subprocess.call(["rm", "-f", failed_good_file, passed_bad_file])
    subprocess.call(["touch", failed_good_file, passed_bad_file])

    p = subprocess.Popen(['python', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    version = float(out.decode()[7:10]) if err.decode() == '' else float(err.decode()[7:10])

    stream = open('config.yaml', 'r')
    data = load(stream, Loader=Loader)

    command_insertions = data['settings']['file-locations']
    python_versions = data['python-versions']

    correct_list = []
    name_list = []

    tool_list = data['tools']
    for tool in tool_list:
        for program in list(tool.keys()):
            if python_versions[program] != version:
                continue
            # if program != 'bedtools': continue
            # if program != 'bedtools': continue
            if program[0] not in ['a']: continue
            commands = tool[program]
            
            for command, execution in commands.items():
                current_array = []
                name_list.append(program + " " + command)
                print("*"*18 + " " + program + " " + command + " " + "*"*18)
                print("*"*18 + " good test cases " + "*"*18)
                current_array.extend(run_good(execution, program + " " + command, verbose, failed_good_file, command_insertions))
                print("*"*60)
                print()
                current_array.append(0.5)
                print("*"*18 + " bad test cases " + "*"*18)
                current_array.extend(run_bad(execution, program + " " + command, verbose, passed_bad_file, command_insertions))
                print("*"*60)
                print()
                correct_list.append(current_array)
            
    stream.close()

    num_correct = [l.count(1) for l in correct_list]
    file_list = get_file_names()

    num_correct, correct_list, name_list = sort_together([num_correct, correct_list, name_list], key_list=[0])

    GnRd = colors.LinearSegmentedColormap('GnRd', cdict)
    # print(correct_list)
    plt.figure(figsize=(24,8))
    ax = sns.heatmap(correct_list, cmap=GnRd, linewidths=.5, square=True, cbar=False, xticklabels=file_list, yticklabels=name_list)
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig('out/results.png')


def usage():
    print(
    """Tester for the BED format. Tests the tools in config.yaml to see if they appropriately throw warnings or errors.
Usage: run_all.py [-h] [-V] [-v] [--failed-good] [--passed-bad]
    options:
      -h, --help    Help
      -v, --verbose=    If True, it prints the results and outputs from all tests
      -V, --version The version number
      --failed-good The output file that logs cases where a good file ran with error
      --passed-bad  The output file that logs cases where bad files ran without error or warning
    """)


if __name__ == '__main__':
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "hVv:", ["help", "version", "verbose=", "failed-good=", "passed-bad="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        exit(2)
    
    verbose = False
    failed_good_file = "out/failed_good.txt"
    passed_bad_file = "out/passed_bad.txt"

    for o, a in optlist:
        if o in ("-h", "--help"):
            usage()
            exit(0)
        elif o in ("-V", "--version"):
            print("0.1")
            exit(0)
        elif o in ("--failed-good"):
            failed_good_file = a
        elif o in ("--passed-bad"):
            passed_bad_file = a
        elif o in ("-v", "--verbose"):
            if a.lower() not in ('true', 'false'):
                usage()
                exit(2)
            verbose = True if a.lower() == 'true' else False
        else:
            assert False, "unhandled option"
    
    run_all(verbose, failed_good_file, passed_bad_file)