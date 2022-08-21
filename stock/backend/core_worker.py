# version: 0.7

import os
from subprocess import call

clean_folder = True
stockFiles = ['TW_my.txt', 'US_my.txt']

if clean_folder:
    os.system("rm -r ../post_files/")
    os.mkdir("../post_files/")
    print("rm files under dir ../post_files/")

for nowfile in stockFiles:
    file_name = "../stock_number/" + nowfile
    try:
        os.system("python3 ../core/main.py -i " + file_name)
    except:
        os.system("python ../core/main.py -i " + file_name)
