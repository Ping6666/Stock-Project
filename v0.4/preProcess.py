# this for pre-process from raw data and store into csv file format
import os, sys
import pandas as pd
import numpy as np
import ta


def preProcessPATH(pathBase, fileType, countryCode=''):
    fileList = []
    for dirPath, dirNames, fileNames in os.walk(pathBase):
        for i, f in enumerate(fileNames):
            if fileType in f:
                newFilePath = os.path.join(dirPath, f)
                fileList.append(newFilePath)
    for newF in fileList:
        if '.asp' in newF:
            preProcessASP(newF, countryCode)
        elif '.html' in newF:
            preProcessHTML(newF, countryCode)
        elif '.csv' in newF:
            preProcessCSV(newF)
    return


def preProcessFromStock(stockDataFrame, stockName):
    # RSI, KD
    RSI = ta.momentum.RSIIndicator(close=stockDataFrame["Close"])
    KD = ta.momentum.StochasticOscillator(high=stockDataFrame["High"],
                                          low=stockDataFrame["Low"],
                                          close=stockDataFrame["Close"])
    K = RSI.rsi() * KD.stoch() / 100
    D = RSI.rsi() * KD.stoch_signal() / 100
    # KC
    KC = ta.volatility.KeltnerChannel(high=stockDataFrame["High"],
                                      low=stockDataFrame["Low"],
                                      close=stockDataFrame["Close"])
    KC_high = KC.keltner_channel_hband()
    KC_middle = KC.keltner_channel_mband()
    KC_low = KC.keltner_channel_lband()
    # SMA
    windowList = [5, 10, 20, 60, 120, 240]
    resultList = []
    for i in windowList:
        SMA = ta.trend.SMAIndicator(close=stockDataFrame["Close"], window=i)
        resultList.append(SMA.sma_indicator())

    def shiftList(seq, n):
        return seq[n:]

    # Ichimoku Cloud
    ICH = ta.trend.IchimokuIndicator(high=stockDataFrame["High"],
                                     low=stockDataFrame["Low"],
                                     visual=True)
    ICH_a = ICH.ichimoku_a()
    ICH_b = ICH.ichimoku_b()
    ICH_base_line = ICH.ichimoku_base_line()
    ICH_conversion_line = ICH.ichimoku_conversion_line()
    # plot convert
    ICH_plot_1 = ((stockDataFrame["Close"] - ICH_conversion_line) +
                  (stockDataFrame["Close"] - ICH_base_line))
    ICH_plot_2 = (ICH_a - ICH_b)
    # plot convert
    displacement = 26
    ich_tmp_1 = shiftList(ICH_a, displacement - 1)
    ich_tmp_2 = shiftList(ICH_b, displacement - 1)
    ich_tmp_1 = stockDataFrame["Close"] - ich_tmp_1
    ich_tmp_2 = stockDataFrame["Close"] - ich_tmp_2
    ICH_plot_3 = []
    for idx in range(len(ich_tmp_1)):
        newA = ich_tmp_1[idx]
        newB = ich_tmp_2[idx]
        # magnitude
        new_ = min(abs(newA), abs(newB))
        # sign
        tmpSign = 0
        if newA > 0 and newB > 0:
            tmpSign = 1
        elif newA < 0 and newB < 0:
            tmpSign = -1
        ICH_plot_3.append(new_ * tmpSign)
    # Score - Self Index
    # > 0: buy; < 0: sell; number range 50 ~ -50
    Score = []
    # Trend Analysis
    # > 0: 漲勢; = 0: 平盤; < 0: 跌勢
    # TrendAnalysis, TrendAnalysisRaw = [], []
    # thresholdRatio = 1.5
    # tmp1MidNumber, timeLength = 5, 10  # which means 5 % and 10 days
    # Score Point
    # ScorePoint = []
    # midPoint1, midPoint2, midPoint3 = 20, 30, 50
    counter = 0
    for i in range(len(stockDataFrame['Date'])):
        if i == 0:
            Score.append(0)
            # ScorePoint.append(0)
            # TrendAnalysis.append(0)
            # TrendAnalysisRaw.append(0)
            continue
        todayScore = 0
        if D[i] < 10:
            todayScore = todayScore + 10
            if D[i] < K[i]:
                todayScore = todayScore + 5
        elif D[i] > 70:
            todayScore = todayScore - 10
            if D[i] > K[i]:
                todayScore = todayScore - 5
        tmp1, tmp1_, tmp2, tmp3, tmp4 = 0, 0, 0, 0, 0
        try:  # plot_3 Cloud Distance
            tmp1 = 100 * (float(ICH_plot_3[i]) /
                          float(stockDataFrame["Close"][i]))
        except:
            counter = counter + 1
        try:  # plot_1 Rise Potential
            tmp2 = (100 / 2) * (float(ICH_plot_1[i]) /
                                float(stockDataFrame["Close"][i]))
        except:
            counter = counter + 1
        try:  # plot_2 Cloud Protection
            tmp3 = 1 - abs(
                (float(ICH_plot_2[i]) / float(stockDataFrame["Close"][i])))
        except:
            counter = counter + 1
        try:  # plot_2 Cloud Protection
            tmp4 = 100 * ((float(ICH_plot_2[i]) - float(ICH_plot_2[i - 1])) /
                          float(stockDataFrame["Close"][i]))
        except:
            counter = counter + 1
        # TrendAnalysis
        # TrendAnalysisRaw.append(tmp1)
        # tmp1_ = tmp1
        # if tmp1_ < tmp1MidNumber and tmp1_ > -tmp1MidNumber:
        #     tmp1_ = 0
        # elif np.isnan(tmp1_):
        #     tmp1_ = 0
        # else:
        #     timeLength_ = int(timeLength * float((100 + 2 * abs(tmp1_)) / 100))
        #     length = len(TrendAnalysis)
        #     length_ = min(timeLength_, length)
        #     minTrendAnalysis, maxTrendAnalysis = 100, -100
        #     for j in range(length_):
        #         tmp_ = TrendAnalysis[length - 1 - j]
        #         if tmp_ < minTrendAnalysis:
        #             minTrendAnalysis = tmp_
        #         if tmp_ > maxTrendAnalysis:
        #             maxTrendAnalysis = tmp_
        #     if tmp1_ < 0 and tmp1_ > minTrendAnalysis:
        #         tmp1_ = -1
        #     elif tmp1_ > 0 and tmp1_ < maxTrendAnalysis:
        #         tmp1_ = 1
        #     elif tmp1_ > tmp1MidNumber * thresholdRatio and TrendAnalysis[
        #             -1] == 0:
        #         tmp1_ = 1
        #     elif tmp1_ < -tmp1MidNumber * thresholdRatio and TrendAnalysis[
        #             -1] == 0:
        #         tmp1_ = -1
        # TrendAnalysis.append(tmp1_)
        todayScore = todayScore - tmp1 - tmp2 * tmp3 + tmp4
        if ICH_plot_1[i] > ICH_plot_2[i]:
            if ICH_plot_2[i - 1] > ICH_plot_1[i - 1]:
                todayScore = todayScore + 10
        elif ICH_plot_1[i] < ICH_plot_2[i]:
            if ICH_plot_2[i - 1] < ICH_plot_1[i - 1]:
                todayScore = todayScore - 10
        Score.append(todayScore)
        # newTmp_ = 0
        # if len(Score) >= 3:
        #     if Score[-1] > Score[-2]:
        #         if Score[-1] > -midPoint2 and (Score[-2] < -midPoint3
        #                                        and Score[-3] < -midPoint3):
        #             newTmp_ = -30
        #         elif Score[-1] > -midPoint2 and (Score[-2] < -midPoint2
        #                                          and Score[-3] < -midPoint2):
        #             newTmp_ = -20
        #         elif Score[-1] > -midPoint1 and (Score[-2] + Score[-3] <
        #                                          -2 * midPoint1):
        #             newTmp_ = -10
        #     elif Score[-1] < Score[-2]:
        #         if Score[-1] < midPoint2 and (Score[-2] > midPoint3
        #                                       and Score[-3] > midPoint3):
        #             newTmp_ = 30
        #         elif Score[-1] < midPoint2 and (Score[-2] > midPoint2
        #                                         and Score[-3] > midPoint2):
        #             newTmp_ = 20
        #         elif Score[-1] < midPoint1 and (Score[-2] + Score[-3] >
        #                                         2 * midPoint1):
        #             newTmp_ = 10
        # ScorePoint.append(newTmp_)
    Score_ = pd.Series(Score)
    Score_SMA_5 = ta.trend.SMAIndicator(close=Score_, window=5)
    Score_SMA_5_ = Score_SMA_5.sma_indicator()
    if counter != 0:
        print("File process went wrong with " + str(counter) + " times.")
    # save to csv
    dfNew_ = pd.DataFrame({
        'Date': stockDataFrame["Date"],
        'Open': stockDataFrame["Open"],
        'High': stockDataFrame["High"],
        'Low': stockDataFrame["Low"],
        'Close': stockDataFrame["Close"],
        'Volume': stockDataFrame["Volume"],
        'Foreign': stockDataFrame["Foreign"],
        'Trust': stockDataFrame["Trust"],
        'Dealer': stockDataFrame["Dealer"],
        'ForeignRatio': stockDataFrame["ForeignRatio"],
        'K': K,
        'D': D,
        'KC_high': KC_high,
        'KC_middle': KC_middle,
        'KC_low': KC_low,
        'ICH_plot_1': ICH_plot_1,
        'ICH_plot_2': ICH_plot_2,
        'ICH_plot_3': ICH_plot_3,
        'SMA_5': resultList[0],
        'SMA_10': resultList[1],
        'SMA_20': resultList[2],
        'SMA_60': resultList[3],
        'SMA_120': resultList[4],
        'SMA_240': resultList[5],
        # 'TrendAnalysisRaw': TrendAnalysisRaw,
        # 'TrendAnalysis': TrendAnalysis,
        # 'ScorePoint': ScorePoint,
        'Score_SMA_5': Score_SMA_5_,
        'Score': Score
    })
    fileName = '../postData/' + str(stockName) + '.csv'
    dfNew_.to_csv(fileName, index=False)
    print("Stock number " + str(stockName) + "'s csv is completed.")
    return


def preProcessASP(inputFileName, countryCode):
    # inputFileName : ShowBuySaleChartData-stockNum.asp
    inputFileName_ = inputFileName.replace('.asp', '')
    inputList = inputFileName_.split('-')
    try:
        f1 = open(inputFileName, 'r', encoding='utf-8')
    except:
        print("No such file or directory : " + inputFileName)
        return
    # RPT_TIME, 開盤價, 最高價, 最低價, 收盤價, 成交量
    # Date, Open, High, Low, Close, Volume
    fStr = f1.read()
    # stock time
    timeList = fStr[fStr.find("RPT_TIME:["):]
    timeList = timeList[len("RPT_TIME:["):timeList.find("]")]
    timeList = timeList.replace('"', '')
    timeList = timeList.split(',')
    # stock open
    openList = fStr[fStr.find("開盤價:["):]
    openList = openList[len("開盤價:["):openList.find("]")]
    openList = openList.split(',')
    # stock high
    highList = fStr[fStr.find("最高價:["):]
    highList = highList[len("最高價:["):highList.find("]")]
    highList = highList.split(',')
    # stock low
    lowList = fStr[fStr.find("最低價:["):]
    lowList = lowList[len("最低價:["):lowList.find("]")]
    lowList = lowList.split(',')
    # stock close
    closeList = fStr[fStr.find(",收盤價:["):]
    closeList = closeList[len(",收盤價:["):closeList.find("]")]
    closeList = closeList.split(',')
    # stock volume
    volumeList = fStr[fStr.find("成交量:["):]
    volumeList = volumeList[len("成交量:["):volumeList.find("]")]
    volumeList = volumeList.split(',')
    # 外資買賣差額_不含自營商, 投信買賣差額, 自營商買賣差額
    # Foreign, Trust, Dealer
    # stock foreign
    foreignList = fStr[fStr.find("外資買賣差額:["):]
    foreignList = foreignList[len("外資買賣差額:["):foreignList.find("]")]
    foreignList = foreignList.split(',')
    # stock trust
    trustList = fStr[fStr.find("投信買賣差額:["):]
    trustList = trustList[len("投信買賣差額:["):trustList.find("]")]
    trustList = trustList.split(',')
    # stock dealer
    dealerList = fStr[fStr.find("自營商買賣差額:["):]
    dealerList = dealerList[len("自營商買賣差額:["):dealerList.find("]")]
    dealerList = dealerList.split(',')
    # 外資持股比率
    # stock foreign ratio
    foreignRatioList = fStr[fStr.find("外資持股比率:["):]
    foreignRatioList = foreignRatioList[len("外資持股比率:["):foreignRatioList.
                                        find("]")]
    foreignRatioList = foreignRatioList.split(',')
    # privent null in the list
    foreignRatioList_ = []
    for i in foreignRatioList:
        try:
            i_ = float(i)
            foreignRatioList_.append(i_)
        except:
            foreignRatioList_.append(float(0))
    f1.close()
    # pd.DataFrame
    dfNew = pd.DataFrame({
        'Date': timeList,
        'Open': [float(i) for i in openList],
        'High': [float(i) for i in highList],
        'Low': [float(i) for i in lowList],
        'Close': [float(i) for i in closeList],
        'Volume': volumeList,
        'Foreign': foreignList,
        'Trust': trustList,
        'Dealer': dealerList,
        'ForeignRatio': foreignRatioList_
    })
    # print("asp complete")
    stockName = str(inputList[1]) + str(countryCode)
    preProcessFromStock(dfNew, stockName)
    return


def preProcessHTML(inputFileName, countryCode):
    # inputFileName : K_Chart-stockNum-yymmdd.html
    inputFileName_ = inputFileName.replace('.html', '')
    inputList = inputFileName_.split('-')
    try:
        f2 = open(inputFileName, 'r', encoding='utf-8')
    except:
        print("No such file or directory : " + inputFileName)
        return
    # read from html
    df = pd.read_html(f2)
    # take out the table
    df = df[0]
    tmpList = df[0][2:]
    # time
    timeList = []
    mid = tmpList.iloc[0].split("/")
    midNum = int(mid[0]) * 100 + int(mid[1])
    for a in tmpList:
        b = a.split("/")
        # compare the date in the file table
        if int(b[0]) * 100 + int(b[1]) <= midNum:
            d = str(int(inputList[2])) + '/' + a
        else:
            d = str(int(inputList[2]) - 1) + '/' + a
        timeList.append(d)
    timeList = timeList[::-1]
    # stock price
    openList = df[1][2:][::-1]
    highList = df[2][2:][::-1]
    lowList = df[3][2:][::-1]
    closeList = df[4][2:][::-1]
    # stock volume
    volumeList = df[8][2:][::-1]
    # stock foreign
    foreignList = [
        str(i).replace('+', '').replace(',', '') for i in df[12][2:]
    ]
    foreignList = foreignList[::-1]
    # stock trust
    trustList = [str(i).replace('+', '').replace(',', '') for i in df[13][2:]]
    trustList = trustList[::-1]
    # stock dealer
    dealerList = [str(i).replace('+', '').replace(',', '') for i in df[14][2:]]
    dealerList = dealerList[::-1]
    # stock foreign ratio
    foreignRatioList = df[16][2:][::-1]
    f2.close()
    # pd.DataFrame
    dfNew = pd.DataFrame({
        'Date': timeList,
        'Open': [float(i) for i in openList],
        'High': [float(i) for i in highList],
        'Low': [float(i) for i in lowList],
        'Close': [float(i) for i in closeList],
        'Volume': [float(i) for i in volumeList],
        'Foreign': [float(i) for i in foreignList],
        'Trust': [float(i) for i in trustList],
        'Dealer': [float(i) for i in dealerList],
        'ForeignRatio': [float(i) for i in foreignRatioList]
    })
    # print("html complete")
    stockName = str(inputList[1]) + str(countryCode)
    preProcessFromStock(dfNew, stockName)
    return


def preProcessCSV(inputFileName):
    # inputFileName : stockNum.countryCode.csv, stockName.csv
    inputFileName_ = inputFileName.replace('.csv', '')
    stockName = inputFileName_.split('/')[-1]
    # stockName = str(inputList[-1]) + str(countryCode)
    try:
        df = pd.read_csv(inputFileName)
    except:
        print("No such file or directory : " + inputFileName)
        return
    try:
        # pd.DataFrame
        dfNew = pd.DataFrame({
            'Date': df['Date'],
            'Open': df['Open'],
            'High': df['High'],
            'Low': df['Low'],
            'Close': df['Close'],
            'Volume': df['Volume'],
            'Foreign': df['Foreign'],
            'Trust': df['Trust'],
            'Dealer': df['Dealer'],
            'ForeignRatio': df['ForeignRatio']
        })
    except:  # from yahoo finance
        preProcessYahooFinance(df, stockName)
        return
    preProcessFromStock(dfNew, stockName)
    return


# Did not support anymore.
"""
def preProcessTWSE_STOCKDAY(newList, stockNum):
    # pd.DataFrame
    dfNew = pd.DataFrame({
        'Date': [i[0] for i in newList],
        'Open': [float(i[1]) for i in newList],
        'High': [float(i[2]) for i in newList],
        'Low': [float(i[3]) for i in newList],
        'Close': [float(i[4]) for i in newList],
        'Volume': [float(i[5]) for i in newList],
        'Foreign': [0] * len(newList),
        'Trust': [0] * len(newList),
        'Dealer': [0] * len(newList),
        'ForeignRatio': [0] * len(newList)
    })
    preProcessFromStock(dfNew, stockNum)
    return
"""


def checkFloat(inputNum):
    if inputNum != 'null' and not np.isnan(inputNum):
        return True
    return False
    # try:
    #     inputNum = float(inputNum)
    # except:
    #     print("inputNum")
    #     return False
    # return True


def preProcessYahooFinance(dfNow, stockName):
    # if '0050' in stockName:
    #     print(dfNow['Open'].iloc[-2])
    #     print(np.isnan(dfNow['Open'].iloc[-2]))
    dfNew = pd.DataFrame({
        'Date': [i.replace('-', '/') for i in dfNow['Date']],
        'Open': [float(i) if checkFloat(i) else 0 for i in dfNow['Open']],
        'High': [float(i) if checkFloat(i) else 0 for i in dfNow['High']],
        'Low': [float(i) if checkFloat(i) else 0 for i in dfNow['Low']],
        'Close': [float(i) if checkFloat(i) else 0 for i in dfNow['Close']],
        'Volume':
        [float(i / 1000) if checkFloat(i) else 0 for i in dfNow['Volume']],
        'Foreign': [0] * (len(dfNow['Date'])),
        'Trust': [0] * (len(dfNow['Date'])),
        'Dealer': [0] * (len(dfNow['Date'])),
        'ForeignRatio': [0] * (len(dfNow['Date']))
    })
    checker = []
    for i in range(len(dfNew)):
        if (dfNew['Open'].iloc[i] == 0 and dfNew['High'].iloc[i] == 0
                and dfNew['Low'].iloc[i] == 0 and dfNew['Close'].iloc[i] == 0
                and dfNew['Volume'].iloc[i] == 0):
            checker.append(i)
    if len(dfNew) - len(checker) <= 1:
        # print("Data wrong at date no:", checker, ".")
        print("Data wrong at date with the amount:", len(checker), ".")
        print("Data that is closed TODAY was wrong.")
    dfNew.drop(index=checker, inplace=True)
    dfNew.reset_index(inplace=True, drop=True)
    preProcessFromStock(dfNew, stockName)
    return
