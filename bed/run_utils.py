import sys
import subprocess
import getopt
import os
import tempfile


def create_execute_line(tool, filepath, temp_file_list, insertions):
    for to_replace, replacement in insertions.items():
        tool = tool.replace(to_replace, replacement)
    for i in range(len(temp_file_list)):
        tool = tool.replace("TEMP" + str(i), temp_file_list[i].name)
    return tool.replace("FILE", filepath)


def detect_problem(out, err):
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

    return wrong_file_format or skip_line or error or invalid_bed


def run_bad(tool, path, tool_name=None, verbose=False, output_file="out/passed_bad.txt", insertions={}):
    out_file = open(output_file, 'a')
    correct_array = []
    title = tool_name if tool_name is not None else tool

    out_file.write("*"*26 + title + "*"*26 + "\n\n")

    temp_file_list = [tempfile.NamedTemporaryFile() for _ in range(tool.count("TEMP"))]

    for directory in os.listdir(path):
        for file in os.listdir(path + directory):
            if file.endswith(".bed"):
                filepath = path + directory + "/" + file
                execute_line = create_execute_line(tool, filepath, temp_file_list, insertions)
                p = subprocess.Popen(execute_line, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                out, err = p.communicate()

                if p.returncode != 0 or detect_problem(out, err):
                    correct_array.append(1)
                    print(filepath + ' failed correctly') # CHANGE BACK
                    if verbose:
                        
                        print(err)
                        print()
                else:
                    correct_array.append(0)
                    print(filepath + ' passed incorrectly')
                    if verbose:
                        print(out)
                        print()
                    # out_file.write("%===========================%\n" + filepath + "\n\n")
                    # out_file.write(out.encode('utf-8'))
                    # out_file.write("%===========================%\n\n")
    print()
    print(str(correct_array.count(1)) + " correct out of " + str(len(correct_array)))

    out_file.write("\n\nTests completed.\n" + str(correct_array.count(1)) + " correct out of " + 
        str(len(correct_array)) +"\n\n" + "*"*26 + title + "*"*26 + "\n")
    out_file.close()

    return correct_array


def run_good(tool, path, tool_name=None, verbose=False, output_file="out/failed_good.txt", insertions={}):
    out_file = open(output_file, "a")
    correct_array = []
    title = tool_name if tool_name is not None else tool

    out_file.write("*"*26 + title + "*"*26 + "\n\n")
    
    temp_file_list = [tempfile.NamedTemporaryFile() for _ in range(tool.count("TEMP"))]

    for directory in os.listdir(path):
        for file in os.listdir(path + directory):
            if file.endswith(".bed"):
                filepath = path + directory + "/" + file
                execute_line = create_execute_line(tool, filepath, temp_file_list, insertions)
                p = subprocess.Popen(execute_line, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                out, err = p.communicate()

                if p.returncode == 0 and not detect_problem(out, err):
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

    out_file.write("\n\nTests completed.\n" +  str(correct_array.count(1)) + " correct out of " +
        str(len(correct_array)) + "\n\n" + "*"*26 + title + "*"*26 + "\n")
    out_file.close()

    return correct_array
