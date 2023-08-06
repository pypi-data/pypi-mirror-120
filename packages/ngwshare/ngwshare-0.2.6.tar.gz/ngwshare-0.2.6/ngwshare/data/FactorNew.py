import requests
import pandas as pd
import json
import urllib3
from ngwshare.utils.http_util import get_ua
import traceback

def getRiskFactor(body=None):
    pd.set_option('precision', 34)
    url = "https://stq.niuguwang.com/NorthJg/GetNorthJg/getriskdata"
    # url = 'http://127.0.0.1:5000/NorthJg/GetNorthJg/getriskdata'
    headers = {"Content-Type": "application/json", "Ngw-Token": "Ngw123456", 'User-Agent': get_ua()}
    urllib3.disable_warnings()
    # s = time.time()
    res = requests.post(url, data=json.dumps(body), headers=headers, verify=False, timeout=600)  # 发送请求
    text = res.text
    dict = json.loads(text)["data"]
    column = ["Date", "InnerCode", "Name", "StockCode"]
    column.extend(body["field_list"])
    df = pd.DataFrame(dict, columns=column)
    return df




def getStyleFactor(body=None):
    # url = 'http://127.0.0.1:5000/NorthJg/GetNorthJg/getstyledata'
    url = "https://stq.niuguwang.com/NorthJg/GetNorthJg/getstyledata"
    headers = {"Content-Type": "application/json", "Ngw-Token": "Ngw123456", 'User-Agent': get_ua()}
    urllib3.disable_warnings()
    # s = time.time()
    res = requests.post(url, data=json.dumps(body), headers=headers, verify=False, timeout=600)  # 发送请求
    text = res.text
    dict = json.loads(text)["data"]
    column = ["Date", "InnerCode", "Name", "StockCode"]
    column.extend(body["field_list"])
    df = pd.DataFrame(dict, columns=column)
    return df




def getCSResidual(body=None):
    # url = 'http://127.0.0.1:5000/NorthJg/GetNorthJg/getresidualedata'
    url = "https://stq.niuguwang.com/NorthJg/GetNorthJg/getresidualedata"
    headers = {"Content-Type": "application/json", "Ngw-Token": "Ngw123456", 'User-Agent': get_ua()}
    urllib3.disable_warnings()
    # s = time.time()
    res = requests.post(url, data=json.dumps(body), headers=headers, verify=False, timeout=600)  # 发送请求
    text = res.text
    dict = json.loads(text)["data"]
    column = ["Date", "InnerCode", "Name", "StockCode"]
    column.extend(body["field_list"])
    df = pd.DataFrame(dict, columns=column)
    return df





def getSpecificRisk(body=None):
    # url = 'http://127.0.0.1:5000/factor/getnonfactordata'
    url = "https://stq.niuguwang.com/NorthJg/GetNorthJg/getnonfactordata"
    headers = {"Content-Type": "application/json", "Ngw-Token": "Ngw123456", 'User-Agent': get_ua()}
    urllib3.disable_warnings()
    # s = time.time()
    res = requests.post(url, data=json.dumps(body), headers=headers, verify=False, timeout=600)  # 发送请求
    text = res.text
    dict = json.loads(text)["data"]
    column = ["Date", "InnerCode", "Name", "StockCode"]
    column.extend(body["field_list"])
    df = pd.DataFrame(dict, columns=column)
    return df




def getAlphaFactor(body=None):
    # url = 'http://127.0.0.1:5000/NorthJg/GetNorthJg/getalphadata'
    url = "https://stq.niuguwang.com/NorthJg/GetNorthJg/getalphadata"
    headers = {"Content-Type": "application/json", "Ngw-Token": "Ngw123456", 'User-Agent': get_ua()}
    urllib3.disable_warnings()
    # s = time.time()
    res = requests.post(url, data=json.dumps(body), headers=headers, verify=False, timeout=600)  # 发送请求
    text = res.text
    dict = json.loads(text)["data"]
    column = ["Date", "InnerCode", "Name", "StockCode"]
    column.extend(body["field_list"])
    df = pd.DataFrame(dict, columns=column)
    return df



def getCSFactorReturns(body=None):
    # url = 'http://127.0.0.1:5000/NorthJg/GetNorthJg/getcsfactor'
    url = "https://stq.niuguwang.com/NorthJg/GetNorthJg/getcsfactor"
    headers = {"Content-Type": "application/json", "Ngw-Token": "Ngw123456", 'User-Agent': get_ua()}
    urllib3.disable_warnings()
    # s = time.time()
    res = requests.post(url, data=json.dumps(body), headers=headers, verify=False, timeout=600)  # 发送请求
    text = res.text
    dict = json.loads(text)["data"]
    df = pd.DataFrame(dict, columns=json.loads(text)["col_name"])
    return df




def getCovMatrix(body=None):
    # url = 'http://127.0.0.1:5000/NorthJg/GetNorthJg/getcovmatrix'
    url = "https://stq.niuguwang.com/NorthJg/GetNorthJg/getcovmatrix"
    headers = {"Content-Type": "application/json", "Ngw-Token": "Ngw123456", 'User-Agent': get_ua()}
    urllib3.disable_warnings()
    # s = time.time()
    res = requests.post(url, data=json.dumps(body), headers=headers, verify=False, timeout=600)  # 发送请求
    text = res.text
    dict = json.loads(text)["data"]
    df = pd.DataFrame(dict, columns=json.loads(text)["col_name"])
    return df




def getCovMatrixCol(body=None):
    # url = 'http://127.0.0.1:5000/NorthJg/GetNorthJg/getcovmatrixcol'
    url = "https://stq.niuguwang.com/NorthJg/GetNorthJg/getcovmatrixcol"
    # url = "http://dev-www.test.niuguwang/NorthJg/GetNorthJg/hsweight"
    headers = {"Content-Type": "application/json", "Ngw-Token": "Ngw123456", 'User-Agent': get_ua()}
    urllib3.disable_warnings()
    # s = time.time()
    res = requests.post(url, data=json.dumps(body), headers=headers, verify=False, timeout=600)  # 发送请求
    text = res.text
    dict = json.loads(text)["data"]
    df = pd.DataFrame(dict, columns=json.loads(text)["col_name"])
    return df



def getStrategyData(body=None):
    url = "https://stq.niuguwang.com/NorthJg/GetNorthJg/getstrategydata"
    # url = 'http://127.0.0.1:5000/NorthJg/GetNorthJg/getstrategydata'
    headers = {"Content-Type": "application/json", "Ngw-Token": "Ngw123456", 'User-Agent': get_ua()}
    urllib3.disable_warnings()
    # s = time.time()
    try:
        res = requests.post(url, data=json.dumps(body), headers=headers, verify=False, timeout=600)  # 发送请求
        text = res.text
        datas = json.loads(text)["data"]
        # print(datas)
        index_list = []
        value_list = []
        for data in datas:
            date = data["Date"]
            msg_list = json.loads(data[body["info"][0] + "_" + body["info"][1]])
            if not msg_list:
                continue
            value_list.append(list(msg_list.values()))
            index_list.append(date)
        df = pd.DataFrame(value_list, index=index_list, columns=list(msg_list.keys()))
        return df
    except:
        print(traceback.format_exc())


def get_north_moni():
    url = "https://stq.niuguwang.com/NorthJg/GetNorthJg/getnorthmoni"
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'Spam': 'Eggs',
        'Connection': 'close'
    }
    urllib3.disable_warnings()
    res = requests.post(url, headers=headers, verify=False, timeout=600)  # 发送请求
    text = res.text
    dict = json.loads(text)
    df = pd.DataFrame(dict)
    return df





def getMktRawData(body=None):
    def getMongoDataSpecifiedConditions(body=None):
        url = "https://stq.niuguwang.com/NorthJg/GetNorthJg/getmongospecifiedcond"
        headers = {"Content-Type": "application/json", "Ngw-Token": "Ngw123456", 'User-Agent': get_ua()}
        urllib3.disable_warnings()
        # s = time.time()
        res = requests.post(url, data=json.dumps(body), headers=headers, verify=False, timeout=600)  # 发送请求
        text = res.text
        dict = json.loads(text)["data"]
        df = pd.DataFrame(dict)
        return df
    new_body = {
        'schema_name':'StockT1Data',
        'collection_name':body['collection_name'],
        'condition':'trade_date',
        'search_value':{'$gte':body['sdate'], '$lte':body['edate']}
    }
    df = getMongoDataSpecifiedConditions(new_body)
    return df




def getMktRawDateMax(collection_name):
    def GetMongoDataConditionsMax(body=None):
        url = "https://stq.niuguwang.com/NorthJg/GetNorthJg/getmongocondmax"
        headers = {"Content-Type": "application/json", "Ngw-Token": "Ngw123456", 'User-Agent': get_ua()}
        urllib3.disable_warnings()
        res = requests.post(url, data=json.dumps(body), headers=headers, verify=False, timeout=600)  # 发送请求
        text = res.text
        res = json.loads(text)["data"]
        return res
    new_body = {
        'schema_name': 'StockT1Data',
        'collection_name':collection_name,
        'condition':'trade_date',
    }
    res = GetMongoDataConditionsMax(new_body)
    return res




if __name__ == '__main__':
    import ngwshare as ng
    import time

    # body = {
    #     'stock_list': ['002509.SZ'],
    #     'start': '2016-08-10',
    #     'end': ' 2016-08-10',
    #     'field_list': ['IndustrySW_vsZZ500inZZ500']
    # }
    # data = ng.getRiskFactor(body=body)
    # print(data)
    # # print("getRiskFactor:", data)
    #
    #
    #
    # body = {
    #     'stock_list': ['600276.SH', '002081.SZ', '600176.SH'],
    #     'start': '2015-01-05',
    #     'end': '2015-01-05',
    #     'field_list': ['Industry_vsHS300inHS300', "Size_vsHS300inHS300"]
    # }
    # data = ng.getStyleFactor(body=body)
    # print(data)
    # # print("getStyleFactor", data)
    #
    #
    # body = {
    #     'stock_list': ['000725.SZ','000793.SZ', '000839.SZ'],
    #     'start': '2015-01-06',
    #     'end': '2015-01-06',
    #     'field_list': ['value']
    # }
    # data = ng.getCSResidual(body=body)
    # print(data)
    # # print("getCSResidual", data)
    #
    #
    # body = {
    #     'stock_list': ['000157.SZ','000425.SZ', '000559.SZ'],
    #     'start': '2016-01-13',
    #     'end': '2016-01-13',
    #     'field_list': ['value']
    # }
    # data = ng.getSpecificRisk(body=body)
    # print(data)
    # # print("getSpecificRisk", data)
    #
    #
    # body = {
    #     'stock_list': ['000027.SZ','000402.SZ', '000559.SZ'],
    #     'start': '2015-01-05',
    #     'end': '2015-01-06',
    #     'field_list': ['Liquidity_HS300', 'alpha3_HS300']
    # }
    # data = ng.getAlphaFactor(body=body)
    # print(data)
    # # print("getAlphaFactor", data)
    #
    #
    #
    # body = {
    #     'start': '2015-01-06',
    #     'end': '2015-01-07',
    #     'field_list': ['ZZ500_1']
    # }
    # data = ng.getCSFactorReturns(body=body)
    # print(data)
    # # print("getCSFactorReturns", data)
    #
    #
    #
    # body = {
    #     'start': '2016-01-13',
    #     'end': '2016-01-14',
    #     'field_list': ['ZZ500_1']
    # }
    # data = ng.getCovMatrix(body=body)
    # print(data)
    # # print("getCovMatrix", data)
    #
    #
    # body = {
    #     'start': '2016-01-13',
    #     'end': '2016-01-14',
    #     'field_list': ['HS300_1']
    # }
    # data = ng.getCovMatrixCol(body=body)
    # print(data)
    # # print("getCovMatrixCol", data)


    # body = {
    #     'start': '2021-07-10',
    #     'end': '2021-07-20',
    #     # "info": ['HS300_v1_PF00', 'RebIdys']
    #     # "info": ['HS300_v1_PF00', 'RebTks']
    #     # "info": ['HS300_v1_PF00', 'RebWts']
    #     "info": ['ZZ500_v1', 'PF00_RebAEs']
    # }
    # data = getStrategyData(body=body)
    # print("getStrategyData:", data)
    # print(data)



    # t1 = time.time()
    # df = ng.get_north_moni()
    # print("get_north_moni", df)
    # print(t1-time.time())


    t1 = time.time()
    body = {
        'collection_name':'mkt_raw_data', ##index_daily / mkt_raw_data
        'sdate':'20210910',
        'edate':'20210922'
    }
    data = ng.getMktRawData(body)
    print(data)
    print(time.time()-t1)


    t1 = time.time()
    data = ng.getMktRawDateMax('mkt_raw_data')
    print(data) #index_daily/mkt_raw_data
    print(time.time()-t1)



