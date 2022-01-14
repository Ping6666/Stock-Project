# version: 0.5

import os, sys, getopt

stockFiles = ['TW_my.txt', 'TW_ETF_my.txt']

for nowfile in stockFiles:
    os.system("python mainProcess.py -i " + nowfile)
