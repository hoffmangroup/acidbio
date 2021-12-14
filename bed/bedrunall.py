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
import sys

from yaml import load

from bedrunutils import run

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


HEADER = '*' * 90
PASS_HEADER = "*"*33 + " good test cases " + "*"*34
FAIL_HEADER = "*"*33 + " bad test cases " + "*"*34


def run_all(bed_type, output_file, specific_tool=None, exclude_tool=None,
            verbose=False, failed_good_file="out/failed_good.txt",
            passed_bad_file="out/passed_bad.txt"):
    """
    Calls run_bad or run_good from run_utils.py to run tools against the
    test suite.
    Outputs the results to <output_file> as a binary file.

    output_file: the binary file containing the results
    verbose: if verbose is True, more information will be printed to the screen
    failed_good_file: the output text file containing the outputs from the
                      tools where it failed on a good test case
    passed_bad_file: the output text file containing the outputs from the tools
                     where it passed on a bad test case
    """
    # Clear the previous data and reinitalize it
    if os.path.exists(failed_good_file):
        os.remove(failed_good_file)
    if os.path.exists(passed_bad_file):
        os.remove(passed_bad_file)
    with open(failed_good_file, 'w') as f1, open(passed_bad_file, 'w') as f2:
        pass  # Creates the two new files

    this_env = os.environ['CONDA_DEFAULT_ENV']

    stream = open('config.yaml', 'r')
    data = load(stream, Loader=Loader)

    # Locations of "constant" files
    command_insertions = data['settings']['file-locations']
    # Replace with the correct intersection file
    command_insertions['INTERSECT'] = command_insertions['INTERSECT'].replace(
        'intersect_file', 'intersect_file' + bed_type[-2:])
    # Each tool with its corresponding Python version
    conda_envs = data['conda-environment']

    passing_list = []
    name_list = []

    tool_list = data['tools']
    for tool in tool_list:
        for program in list(tool.keys()):
            # If <specific_tool> is defined, then skip all other tools
            if specific_tool is not None and program != specific_tool:
                continue

            if exclude_tool is not None and program == exclude_tool:
                continue

            # Skip the tool if the wrong Python version is present
            if conda_envs[program] != this_env:
                continue

            commands = tool[program]

            for command, execution in commands.items():
                # Array of how the program performed on each test case.
                # 0 = incorrect, 1 = correct
                current_list = []
                title = program + " " + command
                name_list.append(title)

                m = (88 - len(title)) // 2  # m,n for aesthetic purposes only
                n = m if len(title) % 2 == 0 else m + 1

                print("*"*m + " " + title + " " + "*"*n)
                print(PASS_HEADER)
                current_list.extend(
                    run(execution, bed_type + "/good/", "pass", tool_name=title,
                       verbose=verbose, output_filename=failed_good_file,
                       insertions=command_insertions)
                )
                print(HEADER)
                print()
                # 0.5 is a separator for heatmap purposes
                current_list.append(0.5)

                print(FAIL_HEADER)
                current_list.extend(
                    run(execution, bed_type + "/bad/", "fail",
                        tool_name=title, verbose=verbose,
                        output_filename=passed_bad_file,
                        insertions=command_insertions)
                )
                print(HEADER)
                print()
                passing_list.append(current_list)


    # Used for sorting purposes in combine.py
    num_correct = [l.count(1) for l in passing_list]

    # Dump the results of these set of tools into a binary file
    with open(output_file, 'wb') as fp:
        pickle.dump([num_correct, passing_list, name_list], fp)

    stream.close()
    return num_correct, passing_list, name_list


def main():
    parser = argparse.ArgumentParser(
        description="Tests the tools in config.yaml to see if they " +
        "appropriately throw warnings or errors against a suite of BED files")
    parser.add_argument("bed_version", metavar="bed-version",
                        help="Which BED type to test. Must be one of BED03," +
                        " BED04, ..., BED12")
    parser.add_argument("outdir", help="location where all output files go")
    parser.add_argument("-V", "--version", action='version', version='0.1')
    parser.add_argument("-v", "--verbose", action='store_true',
                        help="display all results")
    parser.add_argument("-t", "--tool", help="test a specific program. If" +
                        " unspecified, all tools in config.yaml will be" +
                        " tested.")
    parser.add_argument("-e", "--exclude", help="test all tools except for" +
                        " this tool. If unspecified, all tools will be tested")
    parser.add_argument("--results-array-file", metavar="RESULTS_FILENAME",
                        help="output binary results to file",
                        default="bed_test_results")
    parser.add_argument("--failed-good", metavar="GOOD_TESTS_FILENAME",
                        help="output incorrect good test cases to file",
                        default="failed_good.txt")
    parser.add_argument("--passed-bad", metavar="BAD_TESTS_FILENAME",
                        help="output incorrect bad test cases to file",
                        default="passed_bad.txt")

    args = parser.parse_args()

    run_all(args.bed_version, args.outdir + "/" + args.results_array_file,
            args.tool, args.exclude, args.verbose,
            args.outdir + "/" + args.failed_good,
            args.outdir + "/" + args.passed_bad)


if __name__ == '__main__':
    sys.exit(main())
    