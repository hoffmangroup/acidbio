"""
Runs the tools in config.yaml and tests whether they can properly
parse the file format.

Outputs the results to a binary file to be visualized using combine.py
"""
import os
import sys
import subprocess
import getopt
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import pickle
from run_utils import *
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def get_file_names():
    """
    Gets a list of the names of the test files that correspond to the list of results
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


def run_all(output_file, verbose=False, failed_good_file="out/failed_good.txt", passed_bad_file="out/passed_bad.txt"):
    """
    Calls run_bad or run_good from run_utils.py to run tools against the test suite.
    Outputs the results to <output_file> as a binary file.

    output_file: the binary file containing the results
    verbose: if verbose is True, more information will be printed to the screen
    failed_good_file: the output text file containing the outputs from the tools where it failed on a good test case
    passed_bad_file: the output text file containing the outputs from the tools where it passed on a bad test case
    """
    # Clear the previous data and reinitalize it
    subprocess.call(["rm", "-f", failed_good_file, passed_bad_file])
    subprocess.call(["touch", failed_good_file, passed_bad_file])

    p = subprocess.Popen(['python', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    version = float(out.decode()[7:10]) if err.decode() == '' else float(err.decode()[7:10])

    stream = open('config.yaml', 'r')
    data = load(stream, Loader=Loader)

    command_insertions = data['settings']['file-locations']  # Locations of "constant" files
    python_versions = data['python-versions']  # Each tool with its corresponding Python version

    correct_list = []
    name_list = []

    tool_list = data['tools']
    for tool in tool_list:
        for program in list(tool.keys()):
            if python_versions[program] != version:  # Skip the tool if the wrong Python version is present
                continue

            commands = tool[program]
            
            for command, execution in commands.items():
                current_array = []  # Array of how the program performed on each test case. 0 = incorrect, 1 = correct
                title = program + " " + command
                name_list.append(title)

                m = (88 - len(title)) // 2  # m,n for aesthetic purposes only
                n = m if len(title) % 2 == 0 else m + 1

                print("*"*m + " " + title + " " + "*"*n)
                print("*"*33 + " strict good test cases " + "*"*33)
                current_array.extend(
                    run_good(execution, "./good/", title, verbose, failed_good_file, command_insertions))
                print("*"*90)
                print()
                current_array.append(0.5)  # 0.5 is a separator for heatmap purposes

                print("*"*33 + " non-strict good cases " + "*"*34)
                current_array.extend(
                    run_good(execution, "./less_good/", title, verbose, failed_good_file, command_insertions))
                print("*"*90)
                print()
                current_array.extend([0.5, 0.5, 0.5])

                print("*"*31 + " non-strict bad test cases " + "*"*32)
                current_array.extend(
                    run_bad(execution, "./less_bad/", title, verbose, passed_bad_file, command_insertions))
                print("*"*90)
                print()
                current_array.append(0.5)

                print("*"*33 + " strict bad test cases " + "*"*34)
                current_array.extend(
                    run_bad(execution, "./bad/", program + " " + command, verbose, passed_bad_file, command_insertions))
                print("*"*90)
                print()
                correct_list.append(current_array)

    num_correct = [l.count(1) for l in correct_list]  # Used for sorting purposes in combine.py
    
    with open(output_file, 'wb') as fp:  # Dump the results of these set of tools into a binary file
        pickle.dump([num_correct, correct_list, name_list], fp)

    stream.close()


def usage():
    sys.stderr.write(
    """Tester for the BED format. Tests the tools in config.yaml to see if they appropriately throw warnings or errors.
Usage: run_all.py -o [-h] [-v] [-V] [--failed-good=] [--passed-bad=]

options:
    -h, --help    Help
    -o, --output= The binary output file that contains the results lists
                  Required argument
    -v, --verbose    If set, then it prints the results from all test cases
    -V, --version The version number
    --failed-good= The output file that logs cases where a good file ran with error
                  Default: out/failed_good.txt
    --passed-bad=  The output file that logs cases where bad files ran without error or warning
                  Default: out/passed_bad.txt
""")


if __name__ == '__main__':
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "hVv:o:",
            ["help", "version", "verbose", "output=", "failed-good=", "passed-bad="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        exit(2)
    
    verbose = False
    failed_good_file = "out/failed_good.txt"
    passed_bad_file = "out/passed_bad.txt"
    output_file = None

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
        elif o in ("-v", "verbose"):
            verbose = True
        elif o in ("-o", "--output"):
            output_file = a
        else:
            assert False, "unhandled option"
    
    if output_file is None:
        sys.stderr.write("Missing required argument -o\n")
        usage()
        exit(2)
    
    run_all(output_file, verbose, failed_good_file, passed_bad_file)
