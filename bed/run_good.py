"""
Runs all the tests in the /good/ directory and checks whether
the tools run without error
"""
import sys
import getopt
import subprocess
import os
import tempfile


def create_execute_line(tool, filepath, temp_file_list, insertions):
    for to_replace, replacement in insertions.items():
        tool = tool.replace(to_replace, replacement)
    for i in range(len(temp_file_list)):
        tool = tool.replace("TEMP" + str(i), temp_file_list[i].name)
    return tool.replace("FILE", filepath)


def run_good(tool, tool_name=None, verbose=False, output_file="out/failed_good.txt", insertions={}):
    out_file = open(output_file, "a")
    correct_array = []
    title = tool_name if tool_name is not None else tool

    out_file.write("**************************" + title + "**************************\n\n")
    
    temps = tool.count("TEMP")
    temp_file_list = [tempfile.NamedTemporaryFile() for _ in range(temps)]

    for directory in os.listdir("./good/"):
        for file in os.listdir("./good/" + directory):
            if file.endswith(".bed"):
                filepath = "./good/" + directory + "/" + file
                execute_line = create_execute_line(tool, filepath, temp_file_list, insertions)
                p = subprocess.Popen(execute_line, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                out, err = p.communicate()
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
                error = "Error" in err or "ERROR:" in out or "java.lang.RuntimeException" in err or "WARNING:" in err
                invalid_bed = "invalid BED" in err or "FileFormatWarning" in err

                if p.returncode == 0 and not (wrong_file_format or skip_line or error or invalid_bed):
                    print(filepath + ' passed correctly') # CHANGE BACK
                    correct_array.append(1)
                    if verbose:
                        print(out)
                        print()
                else:
                    correct_array.append(0)
                    print(filepath + ' failed incorrectly')
                    if verbose:
                        print(out)
                        print()
                    # out_file.write("%===========================%\n" + filepath + "\n\n")
                    # out_file.write(out.encode('utf-8'))
                    # out_file.write("%===========================%\n\n")
    print()
    print(str(correct_array.count(1)) + " correct out of " + str(len(correct_array)))

    out_file.write("\n\nTests completed.\n" +  str(correct_array.count(1)) + " correct out of " + str(len(correct_array)) +
        "\n\n**************************" + title + "**************************\n")
    out_file.close()

    return correct_array


def usage():
    print("""Runs all the good test files against a tool and records the failing cases.
Usage: run_good.py tool [-h] [-V] [-v] [--output-file]
    options:
      tool  The full command line to call the tool being tested. However, replace the input with "FILE" and if
        there are any temporary files needed to be created such as a sorted file, use TEMP1 or TEMP2. The
        command line must be all in one line. If multiple lines are needed, use ; to separate them.
      -h, --help    Help
      -v, --verbose=    If True, it prints the results and outputs from all tests. Default is False
      -V, --version The version number
      --output-file The output file that logs cases where the tool ran with error. Default is failing_good.txt
    """)


if __name__ == "__main__":
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "hVv", ["help", "verbose=", "version", "output-file="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        exit(2)
    
    verbose = False
    output_file = "out/failed_good.txt"
    tool_name = None

    for o, a in optlist:
        if o in ("-V", "--version"):
            print("0.1")
            exit(0)
        elif o in ("-h", "--help"):
            usage()
            exit(0)
        elif o in ("-v", "--verbose"):
            if a.lower() not in ('true', 'false'):
                usage()
                exit(2)
            verbose = True if a.lower() == 'true' else False
        elif o == "--output-file":
            output_file = a
        else:
            assert False, "unhandled option"

    if len(args) == 2:
        tool_name = args[2]
    
    if len(args) > 2 or len(args) == 0:
        usage()
        exit(2)
    
    run_good(args[0], tool_name, verbose, output_file)


# Previous python3 code:
#
# process = subprocess.run(execute_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
# if process.returncode == 0:
#     if verbose:
#         print(filepath + ' passed correctly')
#         print(process.stdout)
#         print()
#     correct += 1
# else:
#     print(filepath + ' failed incorrectly')
#     if verbose:
#         print(process.stdout)
#         print()
#     out_file.write("%===========================%\n" + filepath + "\n\n")
#     out_file.write(process.stdout)
#     out_file.write("%===========================%\n\n")