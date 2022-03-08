# version: 0.5

# this for pre-process from raw data and store into csv file format
import os, sys
import pandas as pd
import numpy as np


def postProcessPATH(pathBase, fileType='.csv'):
    fileList = []
    for dirPath, dirNames, fileNames in os.walk(pathBase):
        for i, f in enumerate(fileNames):
            if fileType in f:
                newFilePath = os.path.join(dirPath, f)
                fileList.append(newFilePath)
    scoreRank(fileList)
    return


def postProcessCSV(fileName):
    try:
        df = pd.read_csv(fileName)
    except:
        print("No such file or directory : " + fileName)
        return None
    thisList = []
    # stock name
    fileName_ = fileName.replace('.csv', '')
    stockNum = fileName_.split('/')
    showingName = ''
    stockNameList = '../stockNumber/TW_all.txt'
    try:
        f = open(stockNameList, 'r', encoding='utf-8')
    except:
        print("No such file or directory : " + stockNameList + ".")
        return None
    tmpList = f.readlines()
    tmpList_ = []
    for tmp in tmpList:
        tmp_ = tmp.replace('\n', '')
        tmp_ = tmp_.split(' ')[0]
        tmpList_.append(tmp_)
    f.close()
    stockNumber = stockNum[-1].split('.')[0]
    for i in range(len(tmpList_)):
        if stockNumber == (tmpList_[i].split('\t')[0]):
            showingName = tmpList_[i].split('\t')[-1]
            break
    thisList.append(showingName)
    # stock number
    thisList.append(stockNum[-1])
    # stock score
    scoreNow = df['Score'].iloc[len(df['Score']) - 1]
    if np.isnan(scoreNow):
        scoreNow = 0
    thisList.append(scoreNow)
    # stock scorePoint
    # scorePointNow = df['ScorePoint'].iloc[len(df['ScorePoint']) - 1]
    # if np.isnan(scorePointNow):
    #     scorePointNow = 0
    # thisList.append(scorePointNow)
    # others
    thisList.append(df['Close'].iloc[len(df['Close']) - 1])
    thisList.append(df['Volume'].iloc[len(df['Volume']) - 1])
    return thisList


def scoreRank(fileList):
    # score or score point
    checker = 0
    scoreList = []
    for newF in fileList:
        if '.csv' in newF:
            newList = postProcessCSV(newF)
            if newList != None:
                scoreList.append(newList)
    scoreList = sorted(scoreList, key=lambda l: l[2], reverse=True)
    if checker == 0:
        df = pd.DataFrame({
            'StockName': [i[0] for i in scoreList],
            'StockNumber': [i[1] for i in scoreList],
            'StockScore': [i[2] for i in scoreList],
            'StockClose': [i[3] for i in scoreList],
            'StockVolume': [i[4] for i in scoreList]
        })
    else:
        df = pd.DataFrame({
            'StockName': [i[0] for i in scoreList],
            'StockNumber': [i[1] for i in scoreList],
            'StockScore': [i[2] for i in scoreList],
            'StockScorePoint': [i[3] for i in scoreList],
            'StockClose': [i[4] for i in scoreList],
            'StockVolume': [i[5] for i in scoreList]
        })
    buyList, sellList, volumeLimit = [], [], 5000
    if checker == 0:
        # ** only for score **
        for i in scoreList:
            if i[4] > volumeLimit:
                if i[2] >= 30:
                    buyList.append(i[1])
                elif i[2] <= -30:
                    sellList.append(i[1])
    else:
        # ** only for score point **
        for i in scoreList:
            if i[5] > volumeLimit:
                if i[3] > 0:
                    buyList.append(i[1])
                elif i[3] < 0:
                    sellList.append(i[1])
    fileBaseName = 'TotalScoreList'
    fileName = '../' + fileBaseName + '.csv'  # 'postData/' +
    try:
        df.to_csv(fileName, index=False)
        print("\nStock number " + fileBaseName +
              "'s csv is completed. Total sorted stock amount: " +
              str(len(scoreList)) + ".")
        print("The list below only show stock volume larger than " +
              str(volumeLimit) + ".")
        if checker == 0:
            print("\n(Stock score >= 30)  Buy list amount: " +
                  str(len(buyList)) + ".")
            print(buyList)
            print("\n(Stock score <= -30)  Sell List amount: " +
                  str(len(sellList)) + ".")
            print(sellList)
        else:
            print("\n(Stock score point > 0)  Buy list amount: " +
                  str(len(buyList)) + ".")
            print(buyList)
            print("\n(Stock score point < 0)  Sell List amount: " +
                  str(len(sellList)) + ".")
            print(sellList)
    except:
        print('Permission denied: ' + fileName +
              ".\nPlease close the file and repeat again.")
        return
    return
