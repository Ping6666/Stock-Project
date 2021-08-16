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
    # stock number
    fileName_ = fileName.replace('.csv', '')
    stockNum = fileName_.split('/')
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
    scoreList = sorted(scoreList, key=lambda l: l[1], reverse=True)
    if checker == 0:
        df = pd.DataFrame({
            'StockNumber': [i[0] for i in scoreList],
            'StockScore': [i[1] for i in scoreList],
            'StockClose': [i[2] for i in scoreList],
            'StockVolume': [i[3] for i in scoreList]
        })
    else:
        df = pd.DataFrame({
            'StockNumber': [i[0] for i in scoreList],
            'StockScore': [i[1] for i in scoreList],
            'StockScorePoint': [i[2] for i in scoreList],
            'StockClose': [i[3] for i in scoreList],
            'StockVolume': [i[4] for i in scoreList]
        })
    buyList, sellList, volumeLimit = [], [], 5000
    if checker == 0:
        # ** only for score **
        for i in scoreList:
            if i[3] > volumeLimit:
                if i[1] >= 30:
                    buyList.append(i[0])
                elif i[1] <= -30:
                    sellList.append(i[0])
    else:
        # ** only for score point **
        for i in scoreList:
            if i[4] > volumeLimit:
                if i[2] > 0:
                    buyList.append(i[0])
                elif i[2] < 0:
                    sellList.append(i[0])
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