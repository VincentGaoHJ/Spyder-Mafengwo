# -*- coding: utf-8 -*-
"""
@Date: Created on Tue Mar 26 21:50:19 2019
@Author: Haojun Gao
@Description: 
"""

import re
import os
import sys
import json
import copy
from random import choice
from urllib import request
from proxy_github import getProxy
from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    """
    获得html中的子景点的poiid，子景点的中文名字，以及由多少人去过这个景点。
    """

    def __init__(self):
        HTMLParser.__init__(self)
        self.href = []
        self.target = []
        self.people = []
        self.a_text = False

    def handle_starttag(self, tag, attrs):
        # print "Encountered the beginning of a %s tag" % tag
        # 获得html中的子景点的poiid，子景点的中文名字
        if tag == "a":
            if len(attrs) == 0:
                pass
            else:
                for (variable, value) in attrs:
                    if variable == "href":
                        self.href.append(value)
                    if variable == "title":
                        self.target.append(value)
        # 获得html中的子景点有多少人去过这个景点
        if tag == "em":
            self.a_text = True

    def handle_endtag(self, tag):
        if tag == 'em':
            self.a_text = False

    def handle_data(self, data):
        if self.a_text:
            self.people.append(data)


def head_useragent():
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


def get_last_line(input_file):
    file_size = os.path.getsize(input_file)
    block_size = 1024
    dat_file = open(input_file, 'rb')
    last_line = ""
    if file_size > block_size:
        max_seek_point = (file_size // block_size)
        dat_file.seek((max_seek_point - 1) * block_size)
    elif file_size:
        dat_file.seek(0, 0)
    lines = dat_file.readlines()
    if lines:
        last_line = lines[-1].strip()
    dat_file.close()
    return last_line


def get_list(input_file):
    list_loc = []
    with open(input_file, 'r', encoding='utf-8') as f:
        next(f)
        for line in f.readlines():
            line_list = line.strip().split()
            list_loc.append((line_list[0], line_list[1], line_list[2], line_list[3], line_list[4], line_list[5]))
    return list_loc


def get_url(poi, sub_page):
    """
    用来构建一个完整的请求url
    :param poi: 父景点的poiid
    :param sub_page: 要爬取父景点的子景点页数
    :return: url_complete(一个完整的请求url)
    """
    get_url_base = "http://pagelet.mafengwo.cn/poi/pagelet/poiSubPoiApi"

    json_base_1 = "?params=%7B%22poi_id%22%3A%22"
    json_base_2 = "%22%2C%22page%22%3A"
    json_base_3 = "%7D"

    json_str = json_base_1 + str(poi) + json_base_2 + str(sub_page) + json_base_3
    url_complete = get_url_base + json_str

    return url_complete


if __name__ == "__main__":

    headers, userAgent = head_useragent()

    # 判断不带子景点的景点目录文件是否存在，如果存在则读入
    initFilePath = "./data/list_all.txt"
    if os.access(initFilePath, os.F_OK):
        print("[Get_Comments]Basic file is exist.")
    else:
        print("[Get_Comments]Basic file is not exist, please run getList.py first.")
        sys.exit(0)

    list_loc = get_list(initFilePath)

    # 判断带子景点的景点目录是否存在，如果不存在则创建并且写入表头，如果存在则读入写入的位置
    filePath = "./data/list_all_sub.txt"
    fatherId = 0
    sub_page = 0
    if os.access(filePath, os.F_OK):
        print("[Get_List]Given file path is exist.")
        # 默认最后一行是子景点，读入此景点的父节点以及父景点写入的子景点页数（从1开始）
        # 读入已经爬取到的父景点所在页数，父景点的子景点页数以及父景点的ID
        sub_page_byte = get_last_line(filePath).split()[-1]
        # 判断是否只有表头没有数据
        if sub_page_byte.decode(encoding='utf-8') == "data":
            print("[Get_List]The file is exist but no data.")
        else:
            fatherId_byte = get_last_line(filePath).split()[-2]
            page_byte = get_last_line(filePath).split()[5]
            page = int(page_byte.decode(encoding='utf-8'))
            sub_page = int(sub_page_byte.decode(encoding='utf-8'))
            fatherId = int(fatherId_byte.decode(encoding='utf-8'))
            # 判断最后一行内容是子景点还是父景点，如果是父景点，则将fatherId置为该景点
            if fatherId == 0:
                fatherId_byte = get_last_line(filePath).split()[2]
                fatherId = int(fatherId_byte.decode(encoding='utf-8'))
            print("[Get_List]Already spider page :", page)
            print("[Get_List]Already spider sub_page :", sub_page)
    else:
        with open(filePath, 'a+', encoding='utf-8') as f:
            f.write("name\ttype_id\tid\tlat\tlng\tpage\tfather_name\tfather_id\tsub_page\n")

    # 删掉之前爬过的父景点
    if fatherId != 0:
        list_loc_copy = copy.deepcopy(list_loc)
        for poi in list_loc_copy:
            if poi[2] != str(fatherId):
                list_loc.remove(poi)
            else:
                break
    print(list_loc)

    ip_list = getProxy()

    # 循环对每一个景点判断是否有子景点
    for poi in list_loc:
        print("[Get_List]Start to spider:" + str(poi[2] + " Page " + str(poi[-1])))
        with open(filePath, 'a+', encoding='utf-8') as f:
            # 天才的想法：
            # 如果不是第一次进这个循环（fatherId就是列表第一项），那么需要输入父节点信息；
            # 如果是第一次进来，但是文件只有表头（fatherId == 0），也需要输入父节点信息；
            if poi[2] != str(fatherId):
                f.write(str(poi[0]) + "\t" + str(poi[1]) + "\t" +
                        str(poi[2]) + "\t" + str(poi[3]) + "\t" +
                        str(poi[4]) + "\t" + str(poi[5]) + "\t0\t0\t0\n")
        hasMore = True  # 判断该父景点是否还有下一页子景点
        while hasMore:
            # 准备请求内容以及请求URL
            sub_page += 1
            url = get_url(poi[2], sub_page)
            headers['User-Agent'] = choice(userAgent)
            req = request.Request(url, headers=headers)
            proxy_handler = request.ProxyHandler(choice(ip_list))
            opener = request.build_opener(proxy_handler)

            # 判断该景点（父景点）是否有子景点，如果有则继续，没有则跳过
            try:
                response = opener.open(req)
            except Exception as e:
                print("[Get_List]Error ", e)
                print("[Get_List]False to spider " + str(poi[2]) + " Page " + str(poi[-1]) + " sub_page " + str(
                    sub_page))
                sub_page -= 1
                ip_list = getProxy()
            else:
                # 返回的是一个json格式的字符串，将字符串转为dict对象
                data_json = json.loads(response.read().decode("utf8"))
                data_all = data_json.get("data")
                html = data_all["html"]
                # 如果没有controller_data说明该景点（分类不是景点的）没有子景点
                if "controller_data" not in data_all:
                    print("[Get_List]This location has no sub-locations")
                    break
                controller_data = data_all["controller_data"]
                # 判断是否该父景点是否还有下页
                hasMore = controller_data["hasMore"]
                # 得到当前父景点爬的子景点的页数
                curPage = controller_data["curPage"]
                hp = MyHTMLParser()
                hp.feed(html)
                hp.close()
                # 分类是景点但是没有子景点的有controller_data，但是html中没有相应数据
                if len(hp.href) == 0:
                    print("[Get_List]This location has no sub-locations")
                    break

                if not len(hp.href) == len(hp.target) == len(hp.people):
                    raise Exception("[Get_List]子景点信息不匹配")

                for i in range(len(hp.href)):
                    # 子景点去过的人数少于5个就不写入文件中
                    if int(hp.people[i]) <= 5:
                        continue
                    pattern = re.compile("/poi/(.*).html", re.IGNORECASE)
                    sub_poi = pattern.findall(hp.href[i])[0]
                    with open(filePath, 'a+', encoding='utf-8') as f:
                        f.write(str(hp.target[i]) + "\t" + str(poi[1]) + "\t" +
                                str(sub_poi) + "\t" + str(poi[3]) + "\t" +
                                str(poi[4]) + "\t" + str(poi[5]) + "\t" +
                                str(poi[0]) + "\t" + str(poi[2]) + "\t" +
                                str(sub_page) + "\n")

                print("[Get_List]Success to spider " + str(poi[2]) +
                      " Page " + str(poi[-1]) +
                      " sub_page " + str(sub_page))
        # 爬完该父景点的所有子景点之后将sub_page置零，不放在循环开始因为第一次进入循环的时候sub_page不为零。
        sub_page = 0
        print("[Get_List]Finish to spider:" + str(poi[2] + " Page " + str(poi[-1])))
    print("[Get_List]Done spider all the list")
