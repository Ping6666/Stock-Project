# version: 0.5

import os, sys, getopt

stockFiles = ['TW_my.txt', 'US_my.txt']

for nowfile in stockFiles:
    os.system("python mainProcess.py -i " + nowfile)
