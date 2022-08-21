# version: 0.7

import os, sys

## outside the docker ##
# sys.path.insert(1, '../core/')
# from postProcess import postProcessPATH
# from dataCrawler import crawlerReadFile

## inside the docker (cause by WORKDIR in dockerfile) ##
from stock.core.postProcess import postProcessPATH
from stock.core.dataCrawler import crawlerReadFile


def workhouse(clean_folder, stockFiles):
    # empty the folder
    if clean_folder:
        os.system("rm -r ../post_files/")
        os.mkdir("../post_files/")
        print("rm files under dir ../post_files/")
    # download list
    for nowfile in stockFiles:
        file_name = "../stock_number/" + nowfile
        # connect "core/main.py -i" api
        fileBase2, fileBase3 = '../post_files/', '../stock_number/'
        crawlerReadFile(fileBase3, file_name, '.TW')
        postProcessPATH(fileBase2)
