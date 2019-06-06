# Runs all the tools in config.yaml
import sys
import subprocess
import getopt
from run_bad import run_bad
from run_good import run_good
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def run_all(verbose=False, failed_good_file="failed_good.txt", passed_bad_file="passed_bad.txt"):
    # Clear the previous data and reinitalize it
    subprocess.call(["rm", "-f", failed_good_file, passed_bad_file])
    subprocess.call(["touch", failed_good_file, passed_bad_file])

    stream = open('config.yaml', 'r')
    data = load(stream, Loader=Loader)


    tool_list = data['tools']
    for tool in tool_list:
        for program in list(tool.keys()):
            commands = tool[program]
            
            
            print("*"*18 + " Cases that are supposed to pass " + "*"*18)
            print('\n\n')
            for command, execution in commands.items():
                if command != 'merge':
                    continue
                print("*"*18 + " " + program + " " + command + " " + "*"*18)
                run_good(execution, program + " " + command, verbose, failed_good_file)
                print("*"*60)
                print()
                print()
            print("*"*18 + " Cases that are supposed to pass " + "*"*18 + "\n\n")

            print("*"*18 + " Cases that are supposed to fail " + "*"*18 + "\n\n")

            for command, execution in commands.items():
                if command != 'merge':
                    continue
                print("*"*18 + " " + program + " " + command + " "+ "*"*18)
                run_bad(execution, program + " " + command, verbose, passed_bad_file)
                print("*"*60 + "\n\n")
            print("*"*18 + " Cases that are supposed to fail " + "*"*18)
            
    stream.close()


def usage():
    print(
    """Tester for the BED format. Tests the tools in config.yaml to see if they appropriately throw warnings or errors.
Usage: run_all.py [-h] [-V] [-v] [--failed-good] [--passed-bad]
    options:
      -h, --help    Help
      -v, --verbose=    If True, it prints the results and outputs from all tests
      -V, --version The version number
      --failed-good The output file that logs cases where a good file ran with error
      --passed-bad  The output file that logs cases where bad files ran without error or warning
    """)


if __name__ == '__main__':
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "hVv:", ["help", "version", "verbose=", "failed-good=", "passed-bad="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        exit(2)
    
    verbose = False
    failed_good_file = "failed_good.txt"
    passed_bad_file = "passed_bad.txt"

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
        elif o in ("-v", "--verbose"):
            if a.lower() not in ('true', 'false'):
                usage()
                exit(2)
            verbose = True if a.lower() == 'true' else False
        else:
            assert False, "unhandled option"
    
    run_all(verbose, failed_good_file, passed_bad_file)