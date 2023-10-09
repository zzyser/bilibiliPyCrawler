import json
import re
import csv
import requests
import jsonpath
import numpy as np
import pandas as pd


def GetNeighborList(uid):
    gznum = 0
    headers = {
        'referer': f'https://space.bilibili.com/{uid}/fans/follow',  # 防盗链
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    user_url = f'https://api.bilibili.com/x/space/acc/info?mid={uid}&jsonp=jsonp'

    try:
        user_info = requests.get(user_url, headers=headers).text  # 获取用户信息
        user_name = re.findall('\"name\":\"(.*?)\"', user_info)[0]  # 正则匹配当前用户名称
        # user_level = re.findall('\"level\":\d', user_info)[0].split(':')[1]  # 正则匹配当前用户名称

        # . 匹配任意字符（除了\n）
        # * 匹配前一个字符0次或无限次
        # ? 表示前面字符的0次或1次重复
        # .*? 表示匹配任意数量的重复，但是在能使整个匹配成功的前提下使用最少的重复
        # \ 转义符
    except:
        user_name = 'NoConnet'
        user_level = ''
    unames = []
    mids = []

    for page_number in range(1, 6):
        try:
            fans_url = f'https://api.bilibili.com/x/relation/followings?vmid={uid}&pn={page_number}&ps=50&order=desc&jsonp=jsonp&callback=__jp3'
            fans_info = requests.get(fans_url, headers=headers).text  # 获取关注列表
            # print('\n',fans_info)
            fan_info = json.loads(re.findall('__jp3\((.*)\)', fans_info)[0])  # 正则匹配被关注用户信息  格式是json的
            uname = jsonpath.jsonpath(fan_info, '$..uname')  # 从根节点开始，获取所有key为uname的值
            mid = jsonpath.jsonpath(fan_info, '$..mid')  # 从根节点开始，获取所有key为mid的值
            unames.extend(uname)
            mids.extend(mid)
        except:
            pass
    mids_unique = list(np.unique(mids))
    unames_unique = []
    for mid in mids_unique:
        unames_unique.append(unames[mids.index(mid)])
    for i in mids_unique:
        gznum = gznum + 1

    return user_name, mids_unique, unames_unique


