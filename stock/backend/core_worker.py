# version: 0.7

import os

from core.postProcess import postProcessPATH
from core.dataCrawler import crawlerReadFile


def workhouse(clean_folder, stockFiles):
    fileBase2 = "./post_files/"
    # empty the folder
    if clean_folder:
        os.system("rm -r " + fileBase2)
        os.mkdir(fileBase2)
        print("rm files under dir " + fileBase2)

    # download list
    fileBase3 = "./stock_number/"
    for nowfile in stockFiles:
        file_name = fileBase3 + nowfile
        # connect "core/main.py -i" api
        crawlerReadFile(fileBase3, file_name, '.TW')
    postProcessPATH(fileBase2)
    return


## use subprocess.Popen() in app_flask ##
workhouse(True, ['TW_my.txt', 'US_my.txt'])
