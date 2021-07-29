# this for pre-process from raw data and store into csv file format
import os, sys
import pandas as pd
import ta


def preProcessPATH(pathBase, fileType):
    fileList = []
    for dirPath, dirNames, fileNames in os.walk(pathBase):
        for i, f in enumerate(fileNames):
            if fileType in f:
                newFilePath = os.path.join(dirPath, f)
                fileList.append(newFilePath)
    for newF in fileList:
        if '.asp' in newF:
            preProcessASP(newF)
        elif '.html' in newF:
            preProcessHTML(newF)
        elif '.csv' in newF:
            preProcessCSV(newF)
    return


def preProcessFromStock(stockDataFrame, stockNumber):
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
    Score = []
    # > 0: buy; < 0: sell; number range 50 ~ -50
    counter = 0
    for i in range(len(stockDataFrame['Date'])):
        if i == 0:
            Score.append(0)
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
        tmp1, tmp2, tmp3, tmp4 = 0, 0, 0, 0
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
        todayScore = todayScore - tmp1 - tmp2 * tmp3 + tmp4
        if ICH_plot_1[i] > ICH_plot_2[i]:
            if ICH_plot_2[i - 1] > ICH_plot_1[i - 1]:
                todayScore = todayScore + 10
        elif ICH_plot_1[i] < ICH_plot_2[i]:
            if ICH_plot_2[i - 1] < ICH_plot_1[i - 1]:
                todayScore = todayScore - 10
        Score.append(todayScore)
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
        'Score': Score
    })
    fileName = '../postData/' + str(stockNumber) + '.TW.csv'
    dfNew_.to_csv(fileName, index=False)
    print("Stock number " + str(stockNumber) + "'s csv is completed.")
    return


def preProcessASP(inputFileName):
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
    preProcessFromStock(dfNew, inputList[1])
    return


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


def preProcessHTML(inputFileName):
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
    preProcessFromStock(dfNew, inputList[1])
    return


def preProcessCSV(inputFileName):
    # inputFileName : stockNum.TW.csv
    inputFileName_ = inputFileName.replace('.TW.csv', '')
    inputList = inputFileName_.split('/')
    try:
        df = pd.read_csv(inputFileName)
    except:
        print("No such file or directory : " + inputFileName)
        return
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
    # print("html complete")
    preProcessFromStock(dfNew, inputList[-1])
    return
