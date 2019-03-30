# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 11:38:43 2018

@author: gaoha
"""

import os
import sys
import csv
import json
import copy
from random import choice
from urllib import request, parse
from proxy_github import getProxy


def head_useragent():
    """
    提供完整的headers和可供选择的User-Agent
    :return: headers & userAgent
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    }

    userAgent = [
        "Mozilla/5.0 (Linux; Android 8.1.0; PAHM00 Build/OPM1.171019.026; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.83 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x2607033B) NetType/WIFI Language/en Process/toolsmp"
        "Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 8.1.0; ALP-AL00 Build/HUAWEIALP-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/10.13 baiduboxapp/10.13.0.11 (Baidu; P1 8.1.0)",
        "Mozilla/5.0 (Linux; Android 6.0.1; OPPO A57 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/10.13 baiduboxapp/10.13.0.10 (Baidu; P1 6.0.1)",
        "Mozilla/5.0 (Linux; Android 8.1; EML-AL00 Build/HUAWEIEML-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.143 Crosswalk/24.53.595.0 XWEB/358 MMWEBSDK/23 Mobile Safari/537.36 MicroMessenger/6.7.2.1340(0x2607023A) NetType/4G Language/zh_CN",
        "Mozilla/5.0 (Linux; Android 8.0; MHA-AL00 Build/HUAWEIMHA-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044304 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070333) NetType/NON_NETWORK Language/zh_CN Process/tools",
        "Mozilla/5.0 (Linux; U; Android 4.1.2; zh-cn; HUAWEI MT1-U06 Build/HuaweiMT1-U06) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30 baiduboxapp/042_2.7.3_diordna_8021_027/IEWAUH_61_2.1.4_60U-1TM+IEWAUH/7300001a/91E050E40679F078E51FD06CD5BF0A43%7C544176010472968/1",
        "Mozilla/5.0 (Linux; Android 8.0; MHA-AL00 Build/HUAWEIMHA-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044304 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070333) NetType/4G Language/zh_CN Process/tools",
        "Mozilla/5.0 (Linux; U; Android 8.0.0; zh-CN; BAC-AL00 Build/HUAWEIBAC-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.9.4.974 UWS/2.13.1.48 Mobile Safari/537.36 AliApp(DingTalk/4.5.11) com.alibaba.android.rimet/10487439 Channel/227200 language/zh-CN",
        "Mozilla/5.0 (Linux; U; Android 8.1.0; zh-CN; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.9.4.974 UWS/2.13.1.48 Mobile Safari/537.36 AliApp(DingTalk/4.5.11) com.alibaba.android.rimet/10487439 Channel/227200 language/zh-CN",
        "Mozilla/5.0 (Linux; Android 5.1.1; vivo X6S A Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044207 Mobile Safari/537.36 MicroMessenger/6.7.3.1340(0x26070332) NetType/4G Language/zh_CN Process/tools",
    ]
    return headers, userAgent


def csv_last_line(input_file):
    """"
    读取CSV文件的最后一行
    :param input_file: 文件名
    :return: last_line
    """
    last_line = []
    with open(input_file, "r", newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            if line is not "":
                last_line = line

    return last_line


def get_list(input_file):
    """
    读取文件，将每一行的元素保存成元组放入列表
    :param input_file: 文件路径
    :return: list_loc
    """
    list_loc = []
    with open(input_file, 'r', encoding='utf-8') as f:
        next(f)
        for line in f.readlines():
            list = line.strip().split()
            list_loc.append((list[0], int(list[2]), int(list[5])))
    return list_loc


def get_url(poiid, page):
    """
    根据参数生成完整url
    :param poiid: 景点poiid
    :param page: 页数
    :return: url
    """
    get_url_base = "http://wxapp.mafengwo.cn/gonglve/poi/?jsondata="

    json_base_1 = "{%22data_style%22:%22comment_list%22,%22filter_style%22:%22comment%22,%22filter%22:{%22poiid%22:%22"
    json_base_2 = "%22,%22tag%22:0},%22page%22:{%22no%22:"
    json_base_3 = ",%22num%22:30}}"

    json_str = json_base_1 + str(poiid) + json_base_2 + str(page) + json_base_3
    url = get_url_base + json_str
    return url


def get_starter(init_file_path, file_path):
    """
    判断完整的景点目录文件是否存在，如果存在则读入;
    判断将要写入的评论文件是否存在，如果存在则读入已经爬取到的最后一个景点的poiid和这个景点评论的页数，若不存在则不用管;
    :param init_file_path: 景点信息所在文件路径
    :param file_path: 景点评论信息所在文件路径
    :return:
    """
    if os.access(init_file_path, os.F_OK):
        print("[Get_Comments]Basic file is exist.")
    else:
        print("[Get_Comments]Basic file is not exist, please run getList.py first.")
        sys.exit(0)

    list_loc = get_list(init_file_path)

    page = 0
    if os.access(file_path, os.F_OK):
        print("[Get_Comments]Given file path is exist.")
        last_line_list = csv_last_line(file_path)
        poiid = int(last_line_list[0])
        page = int(last_line_list[1])
        print("[Continue]Already Spider POI :", poiid)
        print("[Continue]Already Spider Page :", page)

        list_loc_copy = copy.deepcopy(list_loc)
        for poi in list_loc_copy:
            if poi[1] != poiid:
                list_loc.remove(poi)
            else:
                break
    else:
        print("[Get_Comments]Start Collecting Comments")

    return list_loc, page


if __name__ == "__main__":

    headers, userAgent = head_useragent()
    initFilePath = "./data/list_all_sub.txt"
    filePath = "./data/comment_all.csv"

    list_loc, page = get_starter(initFilePath, filePath)
    total_number = len(list_loc)

    ip_list = getProxy()

    for i in range(total_number):
        with open(filePath, 'a+', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)
            hasMore = True
            while hasMore:
                page += 1
                poiid = list_loc[i][1]
                full_url = get_url(poiid, page)
                headers['User-Agent'] = choice(userAgent)
                req = request.Request(full_url, headers=headers)
                proxy_handler = request.ProxyHandler(choice(ip_list))
                opener = request.build_opener(proxy_handler)
                try:
                    print("[Get_List]Try to get the answer.")
                    # 设置timeout的原因是马蜂窝不会拒绝你的链接，但是封掉IP之后不会返回任何东西
                    # 也就是connect成功但是fail to read，但是默认connect在21秒后自动报错，但是read会一直等
                    response = opener.open(req, timeout=20)
                except Exception as e:
                    print("[Get_List]Error ", e)
                    print("[Get_Comments]False to spider " + str(poiid) + " page " + str(page))
                    page -= 1
                    ip_list = getProxy()
                else:
                    response_context = response.read()
                    if any(response_context) is False:
                        print("Seccessful but nothing")
                        print(page)
                        continue
                    print(
                        "[" + str(i) + "/" + str(total_number) + "]Success to spider " + str(poiid) + " page " + str(
                            page))
                    # 返回的是一个json格式的字符串，将字符串转为dict对象
                    data_json = json.loads(response_context.decode("utf8"))
                    data = data_json.get("data")
                    if data["page"]["next"] is True:
                        for loc in data["list"]:
                            writer.writerow([poiid, data["page"]["no"], loc["comment"]])
                    else:
                        print("[Get_Comments]Done write file " + str(list_loc[i][0]) + " page number is " + str(page))
                        hasMore = False
            page = 0
