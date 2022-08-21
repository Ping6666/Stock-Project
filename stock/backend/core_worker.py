# version: 0.7

import os

stockFiles = ['TW_my.txt', 'US_my.txt']

for nowfile in stockFiles:
    os.system("python ../core/main.py -i " + "../stock_number/" + nowfile)
