import os, sys, getopt
from preProcess import *
from postProcess import *
from visualizeData import visualizeStart
from dataCrawler_YahooFinance import crawlerReadFile


def main(argv):
    check = 0
    inputFile, inputFileType, timeLength = '', '', 0
    outputStr = 'mainProcess.py -a <fileType> -p -i <fileName> -l <timeLength>'
    # a: process all raw data to csv
    # p: process all post data to a single csv (with sort on score)
    # i: (without l) only process data to csv
    # i: (with l) visualize the data from csv, l for time length
    outputStr1 = 'fileName with asp  : ShowBuySaleChartData-stockNum.asp'
    outputStr2 = 'fileName with html : K_Chart-stockNum-yymmdd.html'
    outputStr3 = 'fileName with csv  : stockNum.csv'
    outputStr4 = 'fileName with txt  : stock.txt'
    fileBase1, fileBase2 = '../rawData/', '../postData/'
    try:
        opts, args = getopt.getopt(argv, "h:a:pi:l:",
                                   ["iFile=", "tFile=", "lTime="])
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
            if '.asp' in arg or '.html' in arg or '.csv' in arg or '.txt' in arg or '.TW' in arg:
                inputFile = arg
                check = 1
            else:
                print(
                    "Input file need to be a asp or html or csv or txt file.")
                sys.exit(1)
        elif opt in ("-a", "--tFile"):
            # asp : pre download asp from goodinfo and process
            # html : pre download html from goodinfo and process
            # csv : just want to renew the file from csv to csv (add new data)
            if '.asp' == arg or '.html' == arg or '.csv' == arg:
                inputFileType = arg
                check = 10
            else:
                print("Input file need to be a asp or html file.")
                sys.exit(1)
        elif opt in ("-p"):
            check = 11
        elif opt in ("-l", "--lTime"):
            try:
                timeLength = abs(int(arg))
                check = check + 2
            except:
                print("Input time length must be a positive integer.")
                sys.exit(1)
    if check > 0:
        if check == 1:
            if '.asp' in inputFile:
                preProcessASP(inputFile)
                postProcessPATH(fileBase2)
            elif '.html' in inputFile:
                preProcessHTML(inputFile)
                postProcessPATH(fileBase2)
            elif '.txt' in inputFile:
                crawlerReadFile(inputFile, ".TW")
                postProcessPATH(fileBase2)
            elif '.csv' in inputFile:
                preProcessCSV(inputFile)
                postProcessPATH(fileBase2)
        elif check == 3:
            # if '.csv' in inputFile:
            visualizeStart(fileBase2, inputFile, timeLength)
        elif check == 10:
            preProcessPATH(fileBase1, inputFileType)
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