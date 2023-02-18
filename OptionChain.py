import time

import requests
import pandas as pd
from matplotlib import animation as animation, pyplot as plt2, pyplot as plt1, cm
import datetime as dt
import matplotlib.animation as animation

import numpy as np


StpClist = np.array([42000, 42100, 42200, 42400, 42500])
StpPlist = np.array([41500, 41600, 41700, 41800, 41900])

datacall=[]
datacalltime=[]
dfcall = pd.DataFrame(datacall, columns=StpClist)
dfcall.loc[:, "Time"] =[]
dfput = pd.DataFrame(datacall, columns=StpClist)
dfput.loc[:, "Time"] =[]
# Python3 program to find Closest number in a list

def closest(lst, K):
    # element to which nearest value is to be found
    print("Value to which nearest element is to be found: ", K)

    # calculate the difference array
    difference_array = np.absolute(lst - K)

    # find the index of minimum element from the array
    index = difference_array.argmin()
    return index

def CEStrike(optionchain):
    a = np.array(optionchain['STRIKE PRICE'])
    datacall = []
    t = time.localtime()
    current_time = time.strftime("%H:%M", t)
    print(dfcall)
    for stp in StpClist:
        index = np.where(a == stp)[0][0]
        datacall.append(optionchain['CALL OI'][index])
    datacall.append(current_time)
    dfcall.loc[len(dfcall.index)] = datacall
    return dfcall
def PEStrike(optionchain):
    a = np.array(optionchain['STRIKE PRICE'])
    datacall = []
    t = time.localtime()
    current_time = time.strftime("%H:%M", t)
    print(dfput)
    for stp in StpClist:
        index = np.where(a == stp)[0][0]
        datacall.append(optionchain['CALL OI'][index])
    datacall.append(current_time)
    dfput.loc[len(dfput.index)] = datacall
    return dfput
def dataframe():
    url = 'https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY'

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9'
    }
    session = requests.session()
    request = session.get(url, headers=headers)
    cookies = dict(request.cookies)
    response = session.get(url, headers=headers, cookies=cookies).json()
    rawdata = pd.DataFrame(response)
    rawop = pd.DataFrame(rawdata["filtered"]["data"]).fillna(0)

    data = []
    arr = np.array(rawop['strikePrice'])
    underlyingValue = rawop['CE'][0]['underlyingValue']
    startIndex = closest(arr, underlyingValue) - 15
    endIndex = closest(arr, underlyingValue) + 15
    print(f"startIndex in OI:{startIndex}")
    print(f"endIndex in OI:{endIndex}")
    print(f"BankNifty price:{underlyingValue}")
    for i in range(startIndex, endIndex):
        calloi = putoi = callcoi = putcoi = putltp = callltp = 0
        stp = rawop['strikePrice'][i]
        underlyingValue = rawop['CE'][i]['underlyingValue']
        expirydate = rawop['expiryDate'][i]
        if (rawop['CE'][i] == 0):
            calloi = callcoi = 0
        else:
            calloi = rawop['CE'][i]['openInterest']
            callcoi = rawop['CE'][i]['changeinOpenInterest']
            callltp = rawop['CE'][i]['lastPrice']
        if (rawop['PE'][i] == 0):
            putoi = putcoi = 0
        else:
            putoi = rawop['PE'][i]['openInterest']
            putcoi = rawop['PE'][i]['changeinOpenInterest']
            putltp = rawop['PE'][i]['lastPrice']

        opdata = {
            'CALL OI': calloi, 'CCOI': callcoi, 'CLTP': callltp, 'STRIKE PRICE': stp,
            'PLTP': putltp, 'CPOI': putcoi, 'PUT OI': putoi, 'BNF': underlyingValue
        }
        data.append(opdata)

    optionchain = pd.DataFrame(data)
    totcallOI = optionchain['CALL OI'].sum()
    totputOI = optionchain['PUT OI'].sum()

    PCR = totputOI / totcallOI
    print(f"PCR: {PCR}")
    return optionchain

# function to add value labels
def addlabels(x,y1, y2, y3, y4):
    for i in range(len(x)):
        plt2.text(i, y1[i], y1[i], rotation=90, ha='left', va='bottom')
        plt2.text(i, y2[i], y2[i], rotation=90, ha='right', va='bottom')
        #plt.text(i, y3[i], y3[i], rotation=90, ha='left', va='bottom')
        #plt.text(i, y4[i], y4[i], rotation=90, ha='left', va='bottom')

def chartPECE(optionchain):
    # create data
    X = np.array(optionchain['STRIKE PRICE'])
    y1 = np.array(optionchain['CALL OI'])
    y2 = np.array(optionchain['PUT OI'])
    y3 = np.array(optionchain['CCOI'])
    y4 = np.array(optionchain['CPOI'])
    width = 0.20
    X_axis = np.arange(len(X))
    # plot data in grouped manner of bar type
    plt2.bar(X_axis + 0.2, y1, width, facecolor="green", label='CALL')
    plt2.bar(X_axis + 0.4, y3, width, facecolor="green", label='CHG CALL', alpha=0.5)
    plt2.bar(X_axis - 0, y2, width, facecolor="red", label='PUT')
    plt2.bar(X_axis - 0.2, y4, width, facecolor="red", label='CHG PUT', alpha=0.5)

    plt2.xticks(X_axis, X, rotation=90)
    plt2.xlabel("Strike Price")

    # calling the function to add value labels
    addlabels(X, y1, y2, y3, y4)

    plt2.ylabel("OI")
    plt2.title(f"BankNifty Spot Price: {optionchain['BNF'][0]}")
    plt2.legend()
    plt2.grid()
    plt2.show()


def chartPECEline(optionchain):
    colors = ['red','green','cyan', 'blue', 'black']
    dfCEOIwithTime = CEStrike(optionchain)
    print(f'call:{dfCEOIwithTime}')
    dfCEOIwithTime.plot(color=colors, title='call')

    dfPEOIwithTime = PEStrike(optionchain)
    print(f'put:{dfPEOIwithTime}')
    dfPEOIwithTime.plot(color=colors, title='put')
    plt1.grid()
    plt1.show()


while True:
    optionchain = dataframe()

    print(optionchain)
    chartPECE(optionchain)
    chartPECEline(optionchain)
    time.sleep(300)
