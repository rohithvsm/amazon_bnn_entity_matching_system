#!/usr/bin/python2.7

import os
import subprocess

num_tries = 0

while True:
    os.system('./sampler.py tableC.csv 300')
    num_lines = int(subprocess.check_output("cat tableG.csv | awk -F',' '{print $NF}' | grep 1 | wc -l", shell=True))
    #os.system("export NUM_LINES=`cat tableG.csv | awk -F',' '{print $NF}' | grep 1 | wc -l`")
    print os.getenv('NUM_LINES')

    #num_lines = int(str(os.getenv('NUM_LINES')))
    num_tries += 1
    if num_lines > 40:
        break
    if num_tries > 1000:
        break
