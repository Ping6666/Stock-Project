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


def downloadFromYahoo_Single(stockNum, countryCode=''):
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


def downloadFromYahoo(crawlerList, countryCode=''):
    timeWait, retryLimit = 1, 2
    for i in crawlerList:
        # set the countryCodeNow and stockName
        if i.find('#') == 0 or i.find('/') == 0 or i == ' ' or i == '':
            continue
        elif i.find('.') >= 0 and len(i.split('.')) == 2:
            countryCodeNow = '.' + i.split('.')[-1]
            if countryCodeNow == '.':
                countryCodeNow = ''
            stockName = i.split('.')[0]
            if stockName == '':
                continue
        else:
            countryCodeNow = countryCode
            stockName = i
        # loop to ensure download process
        for j in range(retryLimit):
            try:
                downloadFromYahoo_Single(str(stockName), str(countryCodeNow))
            except KeyboardInterrupt:
                exit()
            except:
                # for TWSE OTC
                if countryCodeNow == '.TW':
                    try:
                        downloadFromYahoo_Single(str(stockName), '.TWO')
                    except KeyboardInterrupt:
                        exit()
                    except:
                        print("Fail when downloading stock no. " +
                              str(stockName) + str(countryCodeNow) + " or " +
                              str(stockName) + ".TWO. Retry in" +
                              " {}".format(timeWait) + " sec.")
                    else:
                        break
                else:
                    print("Fail when downloading stock no. " + str(stockName) +
                          str(countryCodeNow) +
                          ". Retry in {}".format(timeWait) + " sec.")
                time.sleep(timeWait)
            else:
                break
    return


def crawlerReadFile(fileBase, fileName, countryCode=''):
    tmpList_, downloadLimit = [], 695
    try:
        f = open(fileName, 'r', encoding='utf-8')
    except:
        try:
            fullName = str(fileBase) + str(fileName)
            f = open(fullName, 'r', encoding='utf-8')
        except:
            print("No such file or directory : " + fileName + " or " +
                  fullName + ".")
            exit(1)
    tmpList = f.readlines()
    for tmp in tmpList:
        tmp_ = tmp.replace('\n', '')
        tmp_ = tmp_.split(' ')[0]
        if tmp_.find('\t') != 0:
            tmp_ = tmp_.split('\t')[0]
        tmpList_.append(tmp_)
    print("Will crawler the list:", tmpList_, ". Total stock amount is",
          len(tmpList_), ".")
    if len(tmpList_) > downloadLimit:
        print("The download amount is larger than the limit:",
              str(downloadLimit), ".")
    f.close()
    downloadFromYahoo(tmpList_, countryCode)
    return
