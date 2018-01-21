# -*- coding: utf-8 -*-

# @Author  : Skye
# @Time    : 2018/1/8 20:38
# @desc    : python 3 , 答题闯关辅助，截屏 ，OCR 识别，百度搜索

import io
import urllib.parse
import webbrowser
import requests
import base64
from config.settings import SUPPORT_APP_TYPE,REGION_DICT,POS_DICT
from PIL import Image
import os

# 百度OCR API  ，在 https://cloud.baidu.com/product/ocr 上注册新建应用即可
api_key = ''
api_secret = ''

def pull_screenshot():
    os.system('adb shell screencap -p /sdcard/screenshot.png')
    os.system('adb pull /sdcard/screenshot.png .')

def getquestion(img):
    region = img.crop((50, 350, 1000, 600))
    # 获取token
    host =  'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+api_key+'&client_secret='+api_secret
    headers = {
        'Content-Type':'application/json;charset=UTF-8'
    }
    res = requests.get(url=host,headers=headers).json()
    token = res['access_token']
    imgByteArr = io.BytesIO()
    region.save(imgByteArr, format='PNG')
    image_data = imgByteArr.getvalue()
    base64_data = base64.b64encode(image_data)
    r = requests.post('https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic',
                  params={'access_token': token}, data={'image': base64_data})
    # result 即为问题
    result = ''
    for i in r.json()['words_result']:
        result += i['words']
    return result

def getchoices(img):
    region = img.crop((75, 615, 990, 1200))
    # 获取token
    host =  'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+api_key+'&client_secret='+api_secret
    headers = {
        'Content-Type':'application/json;charset=UTF-8'
    }
    res = requests.get(url=host,headers=headers).json()
    token = res['access_token']
    imgByteArr = io.BytesIO()
    region.save(imgByteArr, format='PNG')
    image_data = imgByteArr.getvalue()
    base64_data = base64.b64encode(image_data)
    r = requests.post('https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic',
                  params={'access_token': token}, data={'image': base64_data})
    # result 即为问题
    result = []
    for i in r.json()['words_result']:
        result.append(i['words'])
    return result

#  为提高效率，将question和choices一起送往baidu-ocr
def get_question_and_choices(img,app_type):
    pos = 0
    if app_type in SUPPORT_APP_TYPE :
        region = img.crop(REGION_DICT[app_type])
        pos = POS_DICT[app_type]
    else :
        region = img.crop(REGION_DICT["default"])
        pos = POS_DICT["default"]
    # 获取token
    host =  'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+api_key+'&client_secret='+api_secret
    headers = {
        'Content-Type':'application/json;charset=UTF-8'
    }
    res = requests.get(url=host,headers=headers).json()
    token = res['access_token']
    imgByteArr = io.BytesIO()
    region.save(imgByteArr, format='PNG')
    image_data = imgByteArr.getvalue()
    base64_data = base64.b64encode(image_data)
    r = requests.post('https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic',
                  params={'access_token': token}, data={'image': base64_data})
    choices = []
    question = ''
    count = r.json()['words_result_num']
    for i in r.json()['words_result']:
        if count > 3 :
            question += i['words']
            count = count - 1
        else :
            choices.append(i['words'][pos:])
            #  if app_type in SUPPORT_APP_TYPE:
                #  choices.append(i['words'][2:])
            #  else :
                #  choices.append(i['words'])
    return question,choices
# searching from baidu
def search_from_baidu(question):
    result = urllib.parse.quote(question)
    webbrowser.open('https://baidu.com/s?wd='+result)

