"""
Runs all the tests in the /good/ directory and checks whether
the tools run without error
"""
import sys
import subprocess
import os

def run_good(tool: str) -> None:
    correct = 0
    total = 0
    out_file = open("failed_good.txt", "a")

    out_file.write("**************************" + tool + "**************************\n\n")

    for directory in os.listdir("./good/"):
        for file in os.listdir("./good/" + directory):
            if file.endswith(".bed"):
                filepath = "./good/" + directory + "/" + file
                execute_line = tool.replace("FILE", filepath) + " 2>&1"
                # exit_value = subprocess.call(execute_line, shell=True)
                process = subprocess.run(execute_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                if process.returncode == 0:
                    correct += 1
                else:
                    print(filepath + ' failed incorrectly')
                    out_file.write("%===========================%\n" + filepath + "\n\n")
                    # reexecute_line = sys.argv[1].replace("FILE", filepath) + " 2>&1"
                    # process = subprocess.run(reexecute_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                    out_file.write(process.stdout)
                    out_file.write("%===========================%\n\n")
                total += 1

    out_file.write("\n\nTests completed.\n" + str(correct) + " correct out of " + str(total) +
        "\n\n**************************" + tool + "**************************\n")
    out_file.close()

if __name__ == "__main__":

    if len(sys.argv) != 2:
        sys.stderr.write("run_good.py <command line tool>")
        exit(1)

    if sys.argv[1] == '-h' or sys.argv[1] == '--help':
        sys.stdout.write("run_good.py <command line tool>")
        exit(0)

    if sys.argv[1] == '-v' or sys.argv[1] == '--version':
        sys.stdout.write("0.1")
        exit(0)
    
    run_good(sys.argv[1])