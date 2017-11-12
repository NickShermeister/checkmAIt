#!/usr/bin/env python2
import subprocess
import time

proc = subprocess.Popen(['python2', 'sub.py'], stdin=subprocess.PIPE)
proc.communicate("Hello World\n")

time.sleep(10)
