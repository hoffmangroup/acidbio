"""
The utilities needed to test each tool against the test suite.
"""
import os
import glob
import subprocess
import tempfile

NUM_STAR = 26
NUM_EQUAL = 27
STAR_HEADER = '*' * NUM_STAR
EQUAL_HEADER = '%{}%'.format('=' * NUM_EQUAL)
NN = '\n\n'

STDOUT_MESSAGES = ['wrong file format', 'Skipping line:', 'ERROR:', 'WARNING:']
STDERR_MESSAGES = ['Error', 'java.lang.RuntimeException', 'WARNING:',
                   'invalid BED', 'FileFormatWarning', '[W::']


def create_execute_line(tool, filepath, temp_file_list, insertions):
    """
    Replace the "MACROS" with the actual locations to the files

    tool:           the tool's command invocation as given in config.yaml
    filepath:       the location of the BED test file
    temp_file_list: list of temporary files that the tool needs
    insertions:     dictionary of each MACRO and its actual location

    Returns: the command line invocation without MACROS
    """
    for to_replace, replacement in insertions.items():
        tool = tool.replace(to_replace, replacement)
    for i in range(len(temp_file_list)):
        tool = tool.replace("TEMP" + str(i), temp_file_list[i].name)
    return tool.replace("FILE", filepath)


def detect_problem(out, err):
    """
    Searches <out> and <err> for signs of the tool finding
    something wrong with the BED file.
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
    # wrong_file_format = "wrong file format" in out
    # skip_line = "Skipping line:" in out
    # error = "Error" in err or "ERROR:" in out or \
    #         "java.lang.RuntimeException" in err or "WARNING:" in err or \
    #         "WARNING:" in out or "Command failure" in err
    # invalid_bed = "invalid BED" in er r or "FileFormatWarning" in err or \
    #               "[W::" in err
    # return wrong_file_format or skip_line or error or invalid_bed
    for msg in STDOUT_MESSAGES:
        if msg in out:
            return True
    for msg in STDERR_MESSAGES:
        if msg in err:
            return True
    return False


def run(tool, path, pass_fail, extension='bed', tool_name=None, verbose=False,
        output_filename=None, insertions={}):
    if output_filename is None or output_filename == '':
        output_filename = 'passed_bad.txt' if pass_fail == 'pass' else \
                          'failed_good.txt'
    
    out = open(output_filename, 'ab')
    detect_pass = pass_fail == 'pass'
    passing_list = []
    title = tool_name if tool_name is not None else tool

    temp_file_list = \
        [tempfile.NamedTemporaryFile() for _ in range(tool.count("TEMP"))]

    for filepath in glob.glob(path + '*.bed'):
        execute_line = create_execute_line(
            tool, filepath, temp_file_list, insertions
        )
        print(execute_line)
        p = subprocess.Popen(execute_line, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, shell=True)
        stdout, stderr = p.communicate(timeout=120)
        if not detect_pass and \
            (p.returncode != 0 or detect_problem(stdout, stderr)):
            passing_list.append(1)
            if verbose:
                print(filepath + ' failed correctly')
                print(stderr)
                print()
        elif not detect_pass:
            passing_list.append(0)
            print(filepath + ' passed incorrectly')
            if verbose:
                print(stdout)
                print()
            out.write("{}\n {}\n\n".format(EQUAL_HEADER, filepath).encode('utf-8'))
            out.write("stdout:".encode('utf-8'))
            out.write(stdout)
            out.write("stderr:".encode('utf-8'))
            out.write(stderr)
            out.write(EQUAL_HEADER.encode('utf-8'))
        elif p.returncode == 0 and not detect_problem(stdout, stderr):
            passing_list.append(1)
            if verbose:
                print(filepath + ' passed correctly')
                print(out)
                print()
        else:
            passing_list.append(0)
            print(filepath + ' failed incorrectly')
            if verbose:
                print(out)
                print()
            out.write("{}\n {}\n\n".format(EQUAL_HEADER, filepath).encode('utf-8'))
            out.write("stdout:".encode('utf-8'))
            out.write(stdout)
            out.write("stderr:".encode('utf-8'))
            out.write(stderr)
            out.write(EQUAL_HEADER.encode('utf-8'))
    print()
    print(str(passing_list.count(1)) + " correct out of " +
          str(len(passing_list)))
    return passing_list


def run_bad(tool, path, tool_name=None, verbose=False,
            output_filename="out/passed_bad.txt", insertions={}):
    """
    Runs a tool against the tests in <path> and checks whether the tool throws
    some warning or error indicating that the BED file was bad.

    tool:        the command line invocation in config.yaml
    path:        the path to the directory that contains the test suite
    tool_name:   the title of the tool
    verbose:     whether to print more information to the screen
    output_filename:
                 output text file where output from incorrect test cases will
                 be printed
    insertions:  dictionary of MACROS to their actual locations
    """
    out = open(output_filename, 'ab')
    passing_list = []  # Keep track of which test cases pass or fail
    title = tool_name if tool_name is not None else tool

    out.write('{} {} {}\n\n'.format(STAR_HEADER, title, STAR_HEADER).encode('utf-8'))

    temp_file_list = \
        [tempfile.NamedTemporaryFile() for _ in range(tool.count("TEMP"))]

    for file in glob.glob(path + '/*.bed'):
        filepath = path + "/" + file
        execute_line = create_execute_line(tool, filepath, temp_file_list,
                                           insertions)
        print(execute_line)
        p = subprocess.Popen(execute_line, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, shell=True)
        stdout, stderr = p.communicate()

        if p.returncode != 0 or detect_problem(stdout, stderr):
            passing_list.append(1)
            if verbose:
                print(filepath + ' failed correctly')
                print(stderr)
                print()
        else:
            passing_list.append(0)
            print(filepath + ' passed incorrectly')
            if verbose:
                print(stdout)
                print()
            print("{}\n {}".format(EQUAL_HEADER, filepath),
                  end=NN, file=out)
            out.write("stdout:".encode('utf-8'))
            out.write(stdout)
            out.write("stderr:".encode('utf-8'))
            out.write(stderr)
            out.write(EQUAL_HEADER.encode('utf-8'))
    print()
    print(str(passing_list.count(1)) + " correct out of " +
          str(len(passing_list)))

    out.close()

    return passing_list


def run_good(tool, path, tool_name=None, verbose=False,
             output_file="out/failed_good.txt", insertions={}):
    """
    Runs a tool against the tests in <path> and checks if the tool doesn't
    throws any warning or error indicating that the BED file was good

    tool:        the command line invocation in config.yaml
    path:        the path to the directory that contains the test suite
    tool_name:   the title of the tool
    verbose:     whether to print more information to the screen
    output_file: output text file where output from incorrect test cases will
                 be printed
    insertions:  dictionary of MACROS to their actual locations
    """
    out_file = open(output_file, "ab")
    correct_array = []  # Array for holding the results of the tests
    title = tool_name if tool_name is not None else tool

    out_file.write(('*' * 26 + title + '*' * 26 + '\n\n').encode('utf-8'))

    # Generate any temporary files for tools with intermediate operations
    temp_file_list = \
        [tempfile.NamedTemporaryFile() for _ in range(tool.count("TEMP"))]

    for file in os.listdir(path):
        if file.endswith(".bed"):
            filepath = path + "/" + file
            execute_line = create_execute_line(tool, filepath, temp_file_list,
                                               insertions)
            print(execute_line)
            p = subprocess.Popen(execute_line, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, shell=True)
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
                out_file.write(("%===========================%\n" +
                               " {} \n\n").format(filepath).encode('utf-8'))
                out_file.write("stdout:\n".encode('utf-8'))
                out_file.write(out)
                out_file.write("stderr:\n".encode('utf-8'))
                out_file.write(err)
                out_file.write(("%" + "=" * 27 + "%\n\n").encode('utf-8'))

    print()
    print(str(correct_array.count(1)) + " correct out of " +
          str(len(correct_array)))

    out_file.close()

    return correct_array
