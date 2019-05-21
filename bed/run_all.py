# Runs all the tools in config.yaml
import subprocess
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

# Clear the previous data and reinitalize it
subprocess.call(["rm", "-f", "failed_good.txt", "passed_bad.txt"])
subprocess.call(["touch", "failed_good.txt", "passed_bad.txt"])

stream = open('config.yaml', 'r')
data = load(stream, Loader=Loader)


tool_list = data['tools'][0]

for program in list(tool_list.keys()):
    commands = tool_list[program]
    # print (commands)
    
    print("*"*18 + " " + "Cases that are supposed to pass" + " " + "*"*18)
    print('\n\n')
    for command, execution in commands.items():
        print("*"*18 + " " + command + " " + "*"*18)
        subprocess.call(["./run_good.sh", execution, program + " " + command])
        print("*"*60)
        print()
        print()
    print("*"*18 + " " + "Cases that are supposed to pass" + " " + "*"*18)
    print()
    print()
    
    print("*"*18 + " " + "Cases that are supposed to fail" + " " + "*"*18)
    print()
    print()
    for command, execution in commands.items():
        print("*"*18 + " " + command + " "+ "*"*18)
        subprocess.call(["./run_bad.sh", execution, program + " " + command])
        print("*"*60)
        print()
        print()
    print("*"*18 + " " + "Cases that are supposed to fail" + " " + "*"*18)
    
for f in data['waste']:
    subprocess.call(["rm", "-f", f])
    
stream.close()
