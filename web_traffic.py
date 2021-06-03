import os
import subprocess
import time


child_processes = []    
chrome =  r"C:\Program Files\Google\Chrome\Application\chrome.exe"
edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
firefox =  r"C:\Program Files\Mozilla Firefox\firefox.exe"
# http://forums.mozillazine.org/viewtopic.php?p=11508557

subprocess.run(["taskkill", "/f", "/im", os.path.basename(chrome)])
for _ in range (10):
    child_process = subprocess.Popen([chrome, "https://www.youtube.com/watch?v=LXb3EKWsInQ"], shell=False)
    #cmd =  f"{chrome} http://google.com/"
    #print(cmd)
    #child_process = subprocess.Popen(cmd, shell=True)
    # Slight delay is needed, else the pid to be killed later is not correct...
    time.sleep(.1)
    child_processes.append(child_process)

time.sleep(5)


"""
No idea why only can kill first child process pid,
And killing first child process pid will kill the rest 
if the tabs.

My guess is that the first pid is the actual pid of the
browser while the rest is just the tabs.

I have seen it spawn different windows but seems like the
killing the first pid will kill all of the spawned windows...
"""

#for process in child_processes:
pid = child_processes[0].pid
subprocess.run(f"taskkill /F /PID {pid}")
