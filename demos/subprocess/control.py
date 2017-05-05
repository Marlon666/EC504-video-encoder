import subprocess
import sys


'''
This script shows how to launch new python scripts and capture their output in REAL TIME.
we try to be careful to capture the correct python executable ('python' vs. 'python3' etc.)
we also must be careful to decode the stdout buffer using the correct character set

Adapted from: http://stackoverflow.com/a/17701672/7081944

'''

print("Executable path is", sys.executable)
print("System encoding is", sys.stdout.encoding)

proc = subprocess.Popen([sys.executable, '-u', 'runnable.py'], stdout=subprocess.PIPE, bufsize=1)

'''
# This seems to work too
for line in proc.stdout:
    print(line)
'''

for line in iter(proc.stdout.readline, b''):
    print("Bytes representation:", line)
    print(line.decode(sys.stdout.encoding), end='')