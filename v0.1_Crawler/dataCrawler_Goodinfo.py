import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


def downloadData(stockID, year):
    time.sleep(10)
    FilePath_ = "D:/Programming/StockProject/code/v0.1_Crawler/chromedriver.exe"
    urlOriginal_ = "https://goodinfo.tw/StockInfo/ShowK_Chart.asp?STOCK_ID=" + str(
        stockID) + "&CHT_CAT2=DATE"
    # Options
    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')
    userAgent = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
    options.add_argument("user-agent={}".format(userAgent))
    options.add_experimental_option(
        "prefs", {
            "download.default_directory":
            r"D:\Programming\StockProject\code\rawData",
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
    # webdriver.Chrome
    new_ = webdriver.Chrome(FilePath_, options=options)
    new_.minimize_window()
    new_.get(urlOriginal_)
    try:
        new_.execute_script(
            "ReloadReport('ShowK_Chart.asp?STOCK_ID=" + str(stockID) +
            "&CHT_CAT2=DATE&STEP=DATA&PERIOD='" +
            "+encodeURIComponent(365),divK_ChartDetail,txtK_ChartDetailLoading);"
        )
    except KeyboardInterrupt:
        exit(3)
    except:
        print("When process stock no. " + str(stockID) +
              " BAD thing was happened.")
        return
    # check data has been loaded
    tmp = True
    while tmp:
        try:
            element = new_.find_element_by_id('txtK_ChartDetailLoading')
            tmp = element.is_displayed()
        except:
            tmp = False
            break
    # download data
    new_.execute_script(
        "export2html(divPriceDetail.innerHTML,'K_Chart.html');")
    tmp = True
    while tmp:
        tmp = not os.path.exists("../rawData/K_Chart.html")
    newName = '../rawData/K_Chart-' + str(stockID) + '-' + str(year) + '.html'
    os.rename('../rawData/K_Chart.html', newName)
    # close window
    new_.close()
    return


def listProcess(newList):
    for new_ in newList:
        try:
            downloadData(str(new_), '2021')
        except KeyboardInterrupt:
            exit(3)
        except:
            print("Some Error occur when processing stock no. " + str(new_) +
                  ".")
    return


def readFromFile(fileName):
    tmpList_ = []
    f = open(fileName, 'r', encoding='utf-8')
    tmpList = f.readlines()
    for tmp in tmpList:
        tmp_ = tmp.replace('\n', '')
        tmpList_.append(tmp_)
    return tmpList_


currentList = readFromFile('../stockNumber/stock.txt')
# print(currentList)
listProcess(currentList)