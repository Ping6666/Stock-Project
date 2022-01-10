# version: 0.1

# import os, sys, getopt
import time, requests
import pandas as pd
from io import StringIO
from ..main.preProcess import *

# 瀏覽網址
# "https://www.twse.com.tw/zh/page/trading/exchange/STOCK_DAY.html"
# 下載網址
# "https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=csv&date=20210701&stockNo=2330"
# 110年07月 2330 台積電 (月/檔案)
# date = yyyymm01
# stockNo = number
# 99年1月4日 起開始提供 (20100101)

# 瀏覽網址
# "https://www.twse.com.tw/zh/page/trading/exchange/BFIAMU.html"
# 下載網址
# "https://www.twse.com.tw/exchangeReport/BFIAMU?response=csv&date=20210728"
# 110年07月28日各類指數日成交量值 (日/檔案)
# date = yyyymmdd
# 93年7月9日 起開始提供 (未開市則無資料)

# 瀏覽網址
# "https://www.twse.com.tw/zh/page/trading/exchange/BWIBBU.html"
# 下載網址
# "https://www.twse.com.tw/exchangeReport/BWIBBU?response=csv&date=20210701&stockNo=2330"
# 110年07月 2330 台積電 個股日本益比、殖利率及股價淨值比 (月/檔案)
# date = yyyymm01
# stockNo = number
# 94年09月01日 起開始提供 (20050901)


def downloadFromTWSE_STOCKDAY_Single(Date, stockNum, returnList):
    # 日期 成交股數 成交金額 開盤價 最高價 最低價 收盤價 漲跌價差 成交筆數
    # 110/07/01 18,719,706 11,116,195,742 596 597 591 593 -2 20,565
    time.sleep(2)
    headers = {
        'User-Agent':
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.6) Gecko/20070802 SeaMonkey/1.1.4'
    }
    urlBase = "https://www.twse.com.tw/exchangeReport/STOCK_DAY?" + "response=csv&date=" + str(
        Date) + "01&stockNo=" + str(stockNum)
    # load from the website
    response = requests.get(urlBase, headers=headers)
    RC = response.content
    RCDecode = str(RC, 'utf-8', errors='ignore')
    rawData = StringIO(RCDecode)
    df = pd.read_csv(rawData)
    # take out from rawData
    rangeNum = len(df.iloc[:]) - 4
    for i in range(rangeNum):
        if i == 0:
            continue
        returnListNow = []
        # 日期
        returnListNow.append(df.iloc[i].name[0])
        # 開盤價
        returnListNow.append(float(df.iloc[i].name[3]))
        # 最高價
        returnListNow.append(float(df.iloc[i].name[4]))
        # 最低價
        returnListNow.append(float(df.iloc[i].name[5]))
        # 收盤價
        returnListNow.append(float(df.iloc[i].name[6]))
        # 成交股數
        returnListNow.append(
            float(float(df.iloc[1].name[1].replace(',', '')) / 1000))
        returnList.append(returnListNow)
    # print(returnList)
    return returnList


def downloadFromTWSE_STOCKDAY(yearNow, monthNow, stockNum):
    returnList = []
    yearTmp, monthTmp = '2021', '01'
    # yearTmp, monthTmp = '2010', '01'  # valid data after this particular time
    target = 100 * int(yearNow) + 1 * int(monthNow)
    tmp = True
    while tmp:
        current = 100 * int(yearTmp) + 1 * int(monthTmp)
        if current > target:
            tmp = False
            break
        DateTmp = str(yearTmp) + str(monthTmp)
        # print(DateTmp)
        try:
            returnList = downloadFromTWSE_STOCKDAY_Single(
                DateTmp, stockNum, returnList)
        except KeyboardInterrupt:
            exit(3)
        except:
            print("BAD thing happen when process stock no. " + str(stockNum) +
                  " date " + str(DateTmp) + ".")
        if monthTmp != '12':
            monthTmp = str("%02d" % (int(monthTmp) + 1))
        else:
            monthTmp = '01'
            yearTmp = str(int(yearTmp) + 1)
    print("Finish downloading stock no. " + str(stockNum) + ".")
    preProcessTWSE_STOCKDAY(returnList, stockNum)
    return


downloadFromTWSE_STOCKDAY('2021', '07', '2330')
