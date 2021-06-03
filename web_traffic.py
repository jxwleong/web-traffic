import os
import subprocess
import time
import os
import signal
import psutil

child_processes = []    
chrome =  r"C:\Program Files\Google\Chrome\Application\chrome.exe"
edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
for _ in range (10):
    child_process = subprocess.Popen([edge, "https://www.youtube.com/watch?v=LXb3EKWsInQ"], shell=False)
    #cmd =  f"{chrome} http://google.com/"
    #print(cmd)
    #child_process = subprocess.Popen(cmd, shell=True)
    # Slight delay is needed, else the pid to be killed later is not correct...
    time.sleep(.1)
    child_processes.append(child_process)

time.sleep(10)


"""
No idea why only can kill first child process pid,
And killing first child process pid will kill the rest 
if the tabs.

My guess is that the first pid is the actual pid of the
browser while the rest is just the tabs
"""
pid = child_processes[0].pid
subprocess.run(f"taskkill /F /PID {pid}")
