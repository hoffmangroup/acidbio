"""
Runs all the tests in the /bad/ directory and checks whether
the tools run raise an error or warning
"""
import sys
import subprocess
import os


def run_bad(tool: str) -> None:
    correct = 0
    total = 0
    out_file = open("passed_bad.txt", 'a')

    out_file.write("**************************" + tool + "**************************\n\n")

    for directory in os.listdir("./bad/"):
        for file in os.listdir("./bad/" + directory):
            if file.endswith(".bed"):
                filepath = "./bad/" + directory + "/" + file
                execute_line = tool.replace("FILE", filepath) + " > /dev/null"
                process = subprocess.run(execute_line, shell=True, stdout=subprocess.PIPE, stderr = subprocess.PIPE, universal_newlines=True)
                # print(process.stderr)
                if process.returncode != 0 or len(process.stderr) > 0:
                    correct += 1
                else:
                    print(filepath + ' passed incorrectly')
                    out_file.write("%===========================%\n" + filepath + "\n\n")
                    out_file.write(process.stdout)
                    out_file.write("%===========================%\n\n")
                total += 1

    out_file.write("\n\nTests completed.\n" + str(correct) + " correct out of " + str(total) +
        "\n\n**************************" + tool + "**************************\n")
    out_file.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stdout.write("run_bad.py <command line tool>")
        exit(1)

    if sys.argv[1] == '-h' or sys.argv[1] == '--help':
        sys.stdout.write("run_bad.py <command line tool>")
        exit(0)

    if sys.argv[1] == '-v' or sys.argv[1] == '--version':
        sys.stdout.write("0.1")
        exit(0)

    run_bad(sys.argv[1])