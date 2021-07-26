# this for pre-process from raw data and store into csv file format
import os, sys
import pandas as pd


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
    try:
        thisList = []
        # stock number
        fileName_ = fileName.replace('.csv', '')
        stockNum = fileName_.split('/')
        thisList.append(stockNum[-1])
        # stock score
        thisList.append(df['Score'][len(df['Score']) - 1])
    except:
        # print("This file has wrong content.")
        return None
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
        'StockNum': [i[0] for i in scoreList],
        'StockScore': [i[1] for i in scoreList]
    })
    fileName = '../postData/' + '####' + '.TW.csv'
    try:
        df.to_csv(fileName, index=False)
        print("Stock number " + '####' + "'s csv is completed.")
        print("Stock score: higher than 30 can buy, lowwer than -30 can sell.")
    except:
        print('Permission denied: ' + fileName +
              ".\nPlease close the file and repeat again.")
        return
    return