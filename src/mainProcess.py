# version: 0.5

import os, sys, getopt
from preProcess import *
from postProcess import postProcessPATH
from dataCrawler_YahooFinance import crawlerReadFile


def main(argv):
    check = 0
    inputFile, inputFileType, timeLength = '', '', 0
    outputStr = 'mainProcess.py -a <fileType> -p -i <fileName>'
    # a: process all raw data to csv
    # p: process all post data to a single csv (with sort on score)
    # i: (without l) only process data to csv
    # i: (with l) visualize the data from csv, l for time length
    outputStr1 = 'fileName with asp  : ShowBuySaleChartData-stockNum.asp'
    outputStr2 = 'fileName with html : K_Chart-stockNum-yymmdd.html'
    outputStr3 = 'fileName with csv  : stockNum.csv'
    outputStr4 = 'fileName with txt  : stock.txt'
    fileBase1, fileBase2, fileBase3 = '../rawData/', '../postData/', '../stockNumber/'
    try:
        opts, args = getopt.getopt(argv, "ha:pi:", ["iFile=", "tFile="])
    except getopt.GetoptError:
        print(outputStr)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(outputStr + '\n' + outputStr1 + '\n' + outputStr2 + '\n' +
                  outputStr3 + '\n' + outputStr4 + '\n')
            sys.exit(1)
        elif opt in ("-i", "--iFile"):
            # asp, html, csv and txt are for preProcess
            # but txt will use crawler to download data from yahoo finance
            # .TW is for visualize the data
            if arg != '':
                inputFile = arg
                check = 1
            else:
                print("Input file name need to be given.")
                sys.exit(1)
        elif opt in ("-a", "--tFile"):
            # asp : pre download asp from goodinfo and process
            # html : pre download html from goodinfo and process
            # csv : just want to renew the file from csv to csv (add new data)
            if '.asp' == arg or '.html' == arg or '.csv' == arg:
                inputFileType = arg
                check = 10
            else:
                print("Input file need to be a asp or html or csv file.")
                sys.exit(1)
        elif opt in ("-p"):
            check = 11
    if check > 0:
        if check == 1:
            if '.asp' in inputFile:
                preProcessASP(inputFile, ".TW")
                postProcessPATH(fileBase2)
            elif '.html' in inputFile:
                preProcessHTML(inputFile, ".TW")
                postProcessPATH(fileBase2)
            elif '.txt' in inputFile:
                crawlerReadFile(fileBase3, inputFile, '.TW')
                postProcessPATH(fileBase2)
            elif '.csv' in inputFile:
                preProcessCSV(inputFile)
                postProcessPATH(fileBase2)
        elif check == 10:
            preProcessPATH(fileBase1, inputFileType, ".TW")
            postProcessPATH(fileBase2)
        elif check == 11:
            postProcessPATH(fileBase2)
    else:
        print("Argv wrong.")
        print(outputStr)
    return


def clearScreen():
    os.system('cls')


if __name__ == '__main__':
    # clearScreen()
    main(sys.argv[1:])
    exit()
