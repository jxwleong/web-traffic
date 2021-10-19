import argparse
import os
import subprocess
import signal
import time

import validators

child_processes = []
chrome =  r"C:\Program Files\Google\Chrome\Application\chrome.exe"
edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
firefox =  r"C:\Program Files\Mozilla Firefox\firefox.exe"
# http://forums.mozillazine.org/viewtopic.php?p=11508557

arg_value = {
    "number_of_instances": 10,
    "timeout": 10,
    "browser_exe": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "url": "https://www.youtube.com/watch?v=39UFSQvZPd8",
}

def valid_path(path):
    """
    Check whether the path is valid, if it is then will return the
    path, else will raise exception
    """
    if os.path.exists(path):    
        return path
    else: 
        raise argparse.ArgumentTypeError(
                f"Invalid path '{path}' given.") 

def valid_url(url):
    """
    Return the url if the url format isvalid else raise exception
    """
    if validators.url(url):
        return url
    else:
        raise argparse.ArgumentTypeError(
                f"Invalid URL received '{url}', please check the syntax.")

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
                        help="Timeout in seconds to kill the browser spawned (10).")
    parser.add_argument("-b", "--browser_exe",
                        type=valid_path,
                        help="Path to the browser exe, "
                             "(C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe).")
    parser.add_argument("-u", "--url",
                        type=valid_url,
                        help="URL to be browse, "
                             "(https://www.youtube.com/watch?v=39UFSQvZPd8.")    
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
    if args.browser_exe is not None:
        arg_value["browser_exe"] =  args.browser_exe
    if args.url is not None:
        arg_value["url"] = args.url

def handler(signal_received, frame):
    """
    Reference: https://www.devdungeon.com/content/python-catch-sigint-ctrl-c
    Catch SIGINT/CTRL-C signal and kill the spawned processes.
    """
    global child_processes
    if len(child_processes) != 0:
        print("Killing spanwed processes...")
        for process in child_processes:
            process.terminate()
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)

def main():
    signal.signal(signal.SIGINT, handler)
    args = arg_init()
    process_arg(args)
    print(arg_value)

    subprocess.run(["taskkill", "/f", "/im", os.path.basename(arg_value["browser_exe"])])
    for _ in range (arg_value["number_of_instances"]):
        child_process = subprocess.Popen([arg_value["browser_exe"], arg_value["url"]], shell=False)
        # Slight delay is needed, else the pid to be killed later is not correct...
        time.sleep(1)
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

    From the question I asked on stackoverflow, https://stackoverflow.com/q/67836707
    looks like the first pid is the parent and if you kill
    the parent then the child will be dead which make sense.
    """
   # parent = child_processes[0]
   # parent.terminate()
    #print(dir(parent))
    subprocess.run(["taskkill", "/f", "/im", os.path.basename(arg_value["browser_exe"])])
    #for process in child_processes:
        #process.terminate()
        

if __name__ == "__main__":
    main()