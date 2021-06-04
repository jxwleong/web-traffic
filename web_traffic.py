import argparse
import os
import subprocess
import time


child_processes = []
chrome =  r"C:\Program Files\Google\Chrome\Application\chrome.exe"
edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
firefox =  r"C:\Program Files\Mozilla Firefox\firefox.exe"
# http://forums.mozillazine.org/viewtopic.php?p=11508557

arg_value = {
    "number_of_instances": 10,
    "timeout": 10,
}

def arg_init():
    """
    Initialize arguments and return the argument parsed (namespace)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--number_of_instances",
                        type=int,
                        help="Number of browser to be spawned (10).")
    parser.add_argument("-t", "--timeout",
                        type=int,
                        help="Timeout in seconds to kill the browser spawned(10).")
    return parser.parse_args()

def process_arg(args):
    """
    Process the arguments parsed by parser in arg_init()
    """
    global arg_value
    if args.number_of_instances is not None:
        arg_value["number_of_instances"] = args.number_of_instances
    if args.timeout is not None:
        arg_value["timeout"] = args.timeout        

args = arg_init()
process_arg(args)
print(arg_value)

subprocess.run(["taskkill", "/f", "/im", os.path.basename(chrome)])
for _ in range (arg_value["number_of_instances"]):
    child_process = subprocess.Popen([chrome, "https://www.youtube.com/watch?v=LXb3EKWsInQ"], shell=False)
#    child_process = subprocess.Popen([firefox, '-p',  'foo', '-no-remote', "https://www.youtube.com/watch?v=LXb3EKWsInQ"], shell=False),
    # Slight delay is needed, else the pid to be killed later is not correct...
    time.sleep(.5)
    child_processes.append(child_process)

time.sleep(arg_value["timeout"])


"""
No idea why only can kill first child process pid,
And killing first child process pid will kill the rest 
if the tabs.

My guess is that the first pid is the actual pid of the
browser while the rest is just the tabs.

I have seen it spawn different windows but seems like the
killing the first pid will kill all of the spawned windows...

Well, it's because once I have existing browser window
the PID spawned is invalid...
"""

for process in child_processes:
    process.terminate()
#pid = child_processes[0].pid
#subprocess.run(f"taskkill /F /PID {pid}")

# https://stackoverflow.com/questions/19037216/how-to-get-a-name-of-default-browser-using-python