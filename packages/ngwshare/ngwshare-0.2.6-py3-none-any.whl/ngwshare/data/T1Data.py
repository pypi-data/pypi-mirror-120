import requests
import json
import time
import traceback

from ngwshare.utils.date_util import str2datetime
from ngwshare.utils.http_util import get_ua
import pandas as pd
import datetime



def GetFinTech8FTiming(body=None):
    url = 'https://stq.niuguwang.com/factor/GetFinTech8FTiming'
    try:
        headers = {"Content-Type": "application/json","Ngw-Token":"Ngw123456",'User-Agent':get_ua()}
        response = requests.post(url,data=json.dumps(body), headers=headers).content.decode()
        # print(response)
        response_json = json.loads(response)
        # print(response_json)
        if response_json['resultCode'] == 0:
            return pd.DataFrame(response_json['data'])
        else:
            return pd.DataFrame()
    except Exception:
        print(traceback.format_exc())


def AddFinTech8FTiming(body=None):
    url = 'https://stq.niuguwang.com/factor/AddFinTech8FTiming'
    try:
        headers = {"Content-Type": "application/json","Ngw-Token":"Ngw123456",'User-Agent':get_ua()}
        response = requests.post(url,data=json.dumps(body), headers=headers).content.decode()
        response_json = json.loads(response)
        # print(response_json)
        if response_json['resultCode'] == 0:
            return response_json['data']
        else:
            return response_json['data']
    except Exception:
        print(traceback.format_exc())



def GetNorthbound(body=None):
    url = 'https://stq.niuguwang.com/factor/GetNorthbound'
    try:
        headers = {"Content-Type": "application/json","Ngw-Token":"Ngw123456",'User-Agent':get_ua()}
        response = requests.post(url,data=json.dumps(body), headers=headers).content.decode()
        # print(response)
        response_json = json.loads(response)
        # print(response_json)
        if response_json['resultCode'] == 0:
            return pd.DataFrame(response_json['data'])
        else:
            return pd.DataFrame()
    except Exception:
        print(traceback.format_exc())


def AddNorthbound(body=None):
    url = 'https://stq.niuguwang.com/factor/AddNorthbound'
    try:
        headers = {"Content-Type": "application/json","Ngw-Token":"Ngw123456",'User-Agent':get_ua()}
        response = requests.post(url,data=json.dumps(body), headers=headers).content.decode()
        response_json = json.loads(response)
        # print(response_json)
        if response_json['resultCode'] == 0:
            return response_json['data']
        else:
            return response_json['data']
    except Exception:
        print(traceback.format_exc())



if __name__ == '__main__':
    import ngwshare as ng
    t1 = time.time()
    body = {
        'start':'2021-08-01',
        'end': '2021-09-01',
    }
    data = ng.GetNorthbound(body=body)
    print(data)
    print(time.time() - t1)



    t1 = time.time()
    body = {
        'start':'2014-09-03',
        'end': '2021-09-17',
    }
    data = ng.GetFinTech8FTiming(body=body)
    print(data)
    print(time.time() - t1)





