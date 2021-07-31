import os, time, requests
from fake_useragent import UserAgent
import pandas as pd
from io import StringIO
from preProcess import preProcessYahooFinance

# The sample of Yahoo Finance website url
# "https://query1.finance.yahoo.com/v7/finance/download/2330.TW?period1=946944000&period2=1627603200&interval=1d&events=history&includeAdjustedClose=true"
# 2330.TW
# 2000/01/04 - 2021/07/30 (不含 07/30) : 6032 - 5168 = 864 (/天)
# "https://query1.finance.yahoo.com/v7/finance/download/2330.TW?period1=946944000&period2=1627516800&interval=1d&events=history&includeAdjustedClose=true"
# 2330.TW
# 2000/01/04 - 2021/07/29 (不含 07/29) : 5168 - 4304 = 864 (/天)
# "https://query1.finance.yahoo.com/v7/finance/download/2330.TW?period1=947030400&period2=1627430400&interval=1d&events=history&includeAdjustedClose=true"
# 2330.TW
# 2000/01/05 - 2021/07/28 (不含 07/28)
# "https://query1.finance.yahoo.com/v7/finance/download/3481.TW?period1=1161648000&period2=1627516800&interval=1d&events=history&includeAdjustedClose=true"
# 3481.TW
# 2006/10/24 - 2021/07/29

# period1 可以給 小於最早日期 例如          0 (代表輸出 需涵蓋最舊資料)
# period2 可以給 大於最新日期 例如 2000000000 (代表輸出 需涵蓋最新資料)


def downloadFromYahooSingle(stockNum, countryCode=''):
    ua = UserAgent()
    userAgent = ua.random
    headers = {'User-Agent': userAgent}
    urlBase = (
        "https://query1.finance.yahoo.com/v7/finance/download/" +
        str(stockNum) + str(countryCode) +
        "?period1=0&period2=2000000000&interval=1d&events=history&includeAdjustedClose=true"
    )
    # load from the website
    response = requests.get(urlBase, headers=headers)
    RC = response.content
    RCDecode = str(RC, 'utf-8', errors='ignore')
    rawData = StringIO(RCDecode)
    df = pd.read_csv(rawData)
    preProcessYahooFinance(df, str(stockNum) + str(countryCode))
    return


def crawlerReadFile(fileName, countryCode=''):
    tmpList_ = []
    try:
        f = open(fileName, 'r', encoding='utf-8')
    except:
        print("No such file or directory : " + fileName)
        exit(1)
    tmpList = f.readlines()
    for tmp in tmpList:
        tmp_ = tmp.replace('\n', '')
        tmp_ = tmp_.split(' ')
        tmpList_.append(tmp_[0])
    print("Will crawler the list:", tmpList_, ". Total stock amount is",
          len(tmpList_), ".")
    timeWait = 1
    for i in tmpList_:
        counter = 0
        while True:
            if counter >= 2:
                break
            try:
                downloadFromYahooSingle(str(i), str(countryCode))
            except KeyboardInterrupt:
                exit()
            except:
                print("Fail when downloading stock no. " + str(i) +
                      str(countryCode) + ". Retry in {}".format(timeWait) +
                      " sec.")
                time.sleep(timeWait)
                counter = counter + 1
            else:
                break
    return
