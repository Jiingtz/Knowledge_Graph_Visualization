# _*_ coding: utf-8 _*_
"""
@Time    : 2021/6/26 20:50 
@Author  : Du QiYong 
@Version : V 1.0
@File    : XLore_Apis.py
@desc    : XLORE API是为xlore.org设计开发的在线跨语言知识图谱数据服务API。
"""
import requests
from requests.exceptions import RequestException
import random


# 关键字检索
def get_word(key):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 "
        "Safari/537.36"
    }
    try:
        url = 'http://api.xlore.org/query?word={}'.format(key)
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response.encoding = "utf-8"
            return response.text
    except:
        print('访问失败！')
        return None


# 词条检索
def get_lemma(uri):
    try:
        url = 'http://api.xlore.org/query?uri={}'.format(uri)
        response = requests.get(url)
        if response.status_code == 200:
            response.encoding = "utf-8"
            return response.text
    except RequestException:
        return None


# 概念检索
def get_class(key):
    try:
        url = 'http://api.xlore.org/query?classes={}'.format(key)
        response = requests.get(url)
        if response.status_code == 200:
            response.encoding = "utf-8"
            return response.text
    except RequestException:
        return None


# 实例检索
def get_instance(key):
    try:
        url = 'http://api.xlore.org/query?instances={}'.format(key)
        response = requests.get(url)
        if response.status_code == 200:
            response.encoding = "utf-8"
            return response.text
    except RequestException:
        return None
