# version: 0.7

# process data without the frontend and backend
import os, sys, getopt
from preProcess import preProcessPATH
from postProcess import postProcessPATH
from dataCrawler import crawlerReadFile


def main(argv):
    check, inputFile = 0, ''
    outputStr = 'main.py -a/-p/-i <fileName>'
    # a: process all raw data to csv
    # p: process all post data to a single csv (with sort on score)
    # i: download stock data in the given '.txt' file
    fileBase1, fileBase2, fileBase3 = '../raw_files/', '../post_files/', '../stock_number/'
    # arg rule
    try:
        opts, args = getopt.getopt(argv, "ha:pi:", ["iFile="])
    except getopt.GetoptError:
        print(outputStr)
        sys.exit(2)
    # parsing all arg
    for opt, arg in opts:
        if opt == '-h':
            print(outputStr + '\n' + 'fileName with csv  : stockNum.csv\n' +
                  'fileName with txt  : stock.txt\n')
            sys.exit(1)
        elif opt in ("-i", "--iFile"):
            # asp, html, csv and txt are for preProcess
            # but txt will use crawler to download data from yahoo finance
            # .TW is for visualize the data
            if '.txt' in arg:
                inputFile = arg
                check = 1
            else:
                print("Input file not given or file type wrong.")
                sys.exit(1)
        elif opt in ("-a"):
            # current version only handle '.csv' file
            check = 10
        elif opt in ("-p"):
            check = 100
    # call fun. by check
    if check > 0:
        if check == 1:
            crawlerReadFile(fileBase3, inputFile, '.TW')
            postProcessPATH(fileBase2)
        elif check == 10:
            preProcessPATH(fileBase1, '.csv', ".TW")
            postProcessPATH(fileBase2)
        elif check == 100:
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
