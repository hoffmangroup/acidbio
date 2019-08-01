"""
Runs the tools in config.yaml and tests whether they can properly
parse the file format.

This code is meant to be compatible with both Python 2 and 3

Outputs the results to a binary file to be visualized using combine.py
"""
import argparse
import os
import pickle
import subprocess

from yaml import dump, load

from run_utils import *

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


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

    this_env = os.environ['CONDA_DEFAULT_ENV']

    stream = open('config.yaml', 'r')
    data = load(stream, Loader=Loader)

    command_insertions = data['settings']['file-locations']  # Locations of "constant" files
    conda_envs = data['conda-environment']  # Each tool with its corresponding Python version

    correct_list = []
    name_list = []

    tool_list = data['tools']
    for tool in tool_list:
        for program in list(tool.keys()):
            # if program != 'validatebed': continue
            if conda_envs[program] != this_env:  # Skip the tool if the wrong Python version is present
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
                current_array.extend(run_bad(execution, "./bad/", title, verbose, passed_bad_file, command_insertions))
                print("*"*90)
                print()
                correct_list.append(current_array)

    num_correct = [l.count(1) for l in correct_list]  # Used for sorting purposes in combine.py
    
    with open(output_file, 'wb') as fp:  # Dump the results of these set of tools into a binary file
        pickle.dump([num_correct, correct_list, name_list], fp)

    stream.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Tests the tools in config.yaml to see if they appropriately " + 
        "throw warnings or errors against a suite of BED files")
    parser.add_argument("outdir", help="location where all output files go")
    parser.add_argument("-V", "--version", action='version', version='0.1')
    parser.add_argument("-v", "--verbose", action='store_true', help="display all results")
    parser.add_argument("--results-array-file", metavar="RESULTS_FILENAME", help="output binary results to file",
        default="bed_test_results")
    parser.add_argument("--failed-good", metavar="GOOD_TESTS_FILENAME",
        help="output incorrect good test cases to file", default="failed_good.txt")
    parser.add_argument("--passed-bad", metavar="BAD_TESTS_FILENAME",
        help="output incorrect bad test cases to file", default="passed_bad.txt")

    args = parser.parse_args()

    run_all(args.outdir + "/" + args.results_array_file, args.verbose, args.outdir + "/" + args.failed_good,
        args.outdir + "/" + args.passed_bad)
