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
    thisList.append(df['Close'].iloc[len(df['Close']) - 1])
    thisList.append(df['Volume'].iloc[len(df['Volume']) - 1])
    return thisList


def scoreRank(fileList):
    scoreList = []
    for newF in fileList:
        if '.csv' in newF:
            newList = postProcessCSV(newF)
            if newList != None:
                scoreList.append(newList)
    scoreList = sorted(scoreList, key=lambda l: l[1], reverse=True)
    df = pd.DataFrame({
        'StockNumber': [i[0] for i in scoreList],
        'StockScore': [i[1] for i in scoreList],
        'StockClose': [i[2] for i in scoreList],
        'StockVolume': [i[3] for i in scoreList]
    })
    fileName = '../' + '####' + '.TW.csv'  # 'postData/' +
    try:
        df.to_csv(fileName, index=False)
        print("Stock number " + '####' + "'s csv is completed.")
        print("Stock score: higher than 30 can buy, lowwer than -30 can sell.")
    except:
        print('Permission denied: ' + fileName +
              ".\nPlease close the file and repeat again.")
        return
    return