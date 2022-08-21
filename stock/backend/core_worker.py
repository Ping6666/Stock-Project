# version: 0.7

import os, sys

## outside the docker ##
# sys.path.insert(1, '../core/')
# from postProcess import postProcessPATH
# from dataCrawler import crawlerReadFile

## inside the docker (cause by WORKDIR in dockerfile) ##
from core.postProcess import postProcessPATH
from core.dataCrawler import crawlerReadFile


def workhouse(clean_folder, stockFiles):
    # empty the folder
    if clean_folder:
        ## outside the docker ##
        os.system("rm -r ../post_files/")
        os.mkdir("../post_files/")
        print("rm files under dir ../post_files/")

        ## inside the docker (cause by WORKDIR in dockerfile) ##
        # os.system("rm -r ./post_files/")
        # os.mkdir("./post_files/")
        # print("rm files under dir ./post_files/")

    # download list
    for nowfile in stockFiles:
        ## outside the docker ##
        fileBase2, fileBase3 = '../post_files/', '../stock_number/'

        ## inside the docker (cause by WORKDIR in dockerfile) ##
        # fileBase2, fileBase3 = './post_files/', './stock_number/'

        file_name = fileBase3 + nowfile
        # connect "core/main.py -i" api
        crawlerReadFile(fileBase3, file_name, '.TW')
        postProcessPATH(fileBase2)
