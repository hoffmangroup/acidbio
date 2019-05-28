"""
Runs all the tests in the /bad/ directory and checks whether
the tools run raise an error or warning
"""
import sys
import subprocess
import getopt
import os


def run_bad(tool: str, verbose=False, output_file="passed_bad.txt") -> None:
    correct = 0
    total = 0
    out_file = open(output_file, 'a')

    out_file.write("**************************" + tool + "**************************\n\n")

    for directory in os.listdir("./bad/"):
        for file in os.listdir("./bad/" + directory):
            if file.endswith(".bed"):
                filepath = "./bad/" + directory + "/" + file
                execute_line = tool.replace("FILE", filepath) + " 2>&1"
                process = subprocess.run(execute_line, shell=True, stdout=subprocess.PIPE, stderr = subprocess.PIPE, universal_newlines=True)
                # print(process.stderr)
                if process.returncode != 0 or len(process.stderr) > 0:
                    correct += 1
                    if verbose:
                        print(filepath + ' failed correctly')
                        print(process.stdout)
                        print()
                else:
                    print(filepath + ' passed incorrectly')
                    if verbose:
                        print(process.stdout)
                        print()
                    out_file.write("%===========================%\n" + filepath + "\n\n")
                    out_file.write(process.stdout)
                    out_file.write("%===========================%\n\n")
                total += 1

    out_file.write("\n\nTests completed.\n" + str(correct) + " correct out of " + str(total) +
        "\n\n**************************" + tool + "**************************\n")
    out_file.close()


def usage():
    print("To be written")


if __name__ == "__main__":
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "hVv", ["help", "verbose=", "version", "output-file="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        exit(2)
    
    verbose = False
    output_file = "passed_bad.txt"

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
    
    if len(args) != 1:
        usage()
        exit(2)

    run_bad(args[1], verbose, output_file)