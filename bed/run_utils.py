"""
The utilities needed to test each tool against the test suite.
"""
import os
import subprocess
import sys
import tempfile


def create_execute_line(tool, filepath, temp_file_list, insertions):
    """
    Replace the "MACROS" with the actual locations to the files

    tool: the tool's command invocation as given in config.yaml
    filepath: the location of the BED test file
    temp_file_list: list of temporary files that the tool needs
    insertions: dictionary of each MACRO and its actual location

    Returns: the command line invocation without MACROS
    """
    for to_replace, replacement in insertions.items():
        tool = tool.replace(to_replace, replacement)
    for i in range(len(temp_file_list)):
        tool = tool.replace("TEMP" + str(i), temp_file_list[i].name)
    return tool.replace("FILE", filepath)


def detect_problem(out, err):
    """
    Searches <out> and <err> for signs of the tool finding something wrong with the BED file.
    <out> and <err> should be in encoded form.

    out: stdout of the tool
    err: stderr of the tool
    """
    try:
        out = out.decode('UTF-8')
    except UnicodeDecodeError:
        out = "Non-unicode characters present in output"
    try:
        err = err.decode('UTF-8')
    except UnicodeDecodeError:
        err = "Non-unicode characters present in output"
    wrong_file_format = "wrong file format" in out
    skip_line = "Skipping line:" in out
    error = "Error" in err or "ERROR:" in out or "java.lang.RuntimeException" in err or "WARNING:" in err or "WARNING:" in out
    invalid_bed = "invalid BED" in err or "FileFormatWarning" in err

    return wrong_file_format or skip_line or error or invalid_bed


def run_bad(tool, path, tool_name=None, verbose=False, output_file="out/passed_bad.txt", insertions={}):
    """
    Runs a tool against the tests in <path> and checks whether the tool throws some warning or error
    indicating that the BED file was bad.

    tool: the command line invocation in config.yaml
    path: the path to the directory that contains the test suite
    tool_name: the title of the tool
    verbose: whether to print more information to the screen
    output_file: output text file where output from incorrect test cases will be printed
    insertions: dictionary of MACROS to their actual locations
    """
    out_file = open(output_file, 'ab')
    correct_array = []
    title = tool_name if tool_name is not None else tool

    out_file.write('************************** {} **************************\n\n'.format(title).encode('utf-8'))

    temp_file_list = [tempfile.NamedTemporaryFile() for _ in range(tool.count("TEMP"))]

    for file in os.listdir(path):
        if file.endswith(".bed"):
            filepath = path + "/" + file
            execute_line = create_execute_line(tool, filepath, temp_file_list, insertions)
            p = subprocess.Popen(execute_line, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            out, err = p.communicate()

            if p.returncode != 0 or detect_problem(out, err):
                correct_array.append(1)
                if verbose:
                    print(filepath + ' failed correctly')
                    print(err)
                    print()
            else:
                correct_array.append(0)
                print(filepath + ' passed incorrectly')
                if verbose:
                    print(out)
                    print()
                out_file.write("%===========================%\n {} \n\n".format(filepath).encode('utf-8'))
                out_file.write("stdout:\n".encode('utf-8'))
                out_file.write(out)
                out_file.write("stderr:\n".encode('utf-8'))
                out_file.write(err)
                out_file.write("%===========================%\n\n".encode('utf-8'))
    print()
    print(str(correct_array.count(1)) + " correct out of " + str(len(correct_array)))

    out_file.close()

    return correct_array


def run_good(tool, path, tool_name=None, verbose=False, output_file="out/failed_good.txt", insertions={}):
    """
    Runs a tool against the tests in <path> and checks if the tool doesn't throws any warning or error
    indicating that the BED file was good

    tool: the command line invocation in config.yaml
    path: the path to the directory that contains the test suite
    tool_name: the title of the tool
    verbose: whether to print more information to the screen
    output_file: output text file where output from incorrect test cases will be printed
    insertions: dictionary of MACROS to their actual locations
    """
    out_file = open(output_file, "ab")
    correct_array = []  # Array for holding the results of the tests
    title = tool_name if tool_name is not None else tool

    out_file.write('************************** {} **************************\n\n'.format(title).encode('utf-8'))
    
    # Generate any temporary files that a tool needs for intermediate operations
    temp_file_list = [tempfile.NamedTemporaryFile() for _ in range(tool.count("TEMP"))]

    for file in os.listdir(path):
        if file.endswith(".bed"):
            filepath = path + "/" + file
            execute_line = create_execute_line(tool, filepath, temp_file_list, insertions)
            p = subprocess.Popen(execute_line, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            out, err = p.communicate()

            if p.returncode == 0 and not detect_problem(out, err):
                correct_array.append(1)
                if verbose:
                    print(filepath + ' passed correctly')
                    print(out)
                    print()
            else:
                correct_array.append(0)
                print(filepath + ' failed incorrectly')
                if verbose:
                    print(out)
                    print()
                out_file.write("%===========================%\n {} \n\n".format(filepath).encode('utf-8'))
                out_file.write("stdout:\n".encode('utf-8'))
                out_file.write(out)
                out_file.write("stderr:\n".encode('utf-8'))
                out_file.write(err)
                out_file.write("%===========================%\n\n".encode('utf-8'))

    print()
    print(str(correct_array.count(1)) + " correct out of " + str(len(correct_array)))

    out_file.close()

    return correct_array
