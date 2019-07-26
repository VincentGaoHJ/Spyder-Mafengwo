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


def get_last_line(input_file):
    """
    读取文件的最后一行
    :param input_file: 文件名
    :return: last_line
    """
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
    """
    读取文件，将每一个景点（父景点）的所有信息作为一个元组保存入列表中
    :param input_file: 文件路径
    :return: list_loc（所有父景点的列表）
    """
    list_loc = []
    with open(input_file, 'r', encoding='utf-8') as f:
        next(f)
        for line in f.readlines():
            line_list = line.strip().split()
            item_list = []
            for item in line_list:
                item_list.append(item)
            list_loc.append(tuple(item_list))
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


def get_starter(init_file_path, file_path):
    """
    判断不带子景点的景点目录文件是否存在，如果存在则读入;
    判断带子景点的景点目录是否存在，如果不存在则创建并且写入表头，如果存在则读入写入的位置;
    删掉之前爬过的父景点
    :param init_file_path: 父景点所在文件路径
    :param file_path: 将要将所有景点保存入的文件路径
    :return:
        list_location：待爬的父景点列表
        father_id：已经爬到的最后一个父景点的poiid（如果最后一行是表头，那么father_id=0）
        subpage：已经爬到的最后一个父景点的子景点页数（如果最后一行是父景点或者表头，那么subpage=0）
    """
    # 判断不带子景点的景点目录文件是否存在，如果存在则读入
    if os.access(init_file_path, os.F_OK):
        print("[Get_Comments]Basic file is exist.")
    else:
        print("[Get_Comments]Basic file is not exist, please run getList.py first.")
        sys.exit(0)

    list_location = get_list(init_file_path)

    # 判断带子景点的景点目录是否存在，如果不存在则创建并且写入表头，如果存在则读入写入的位置
    father_id = 0
    subpage = 0
    if os.access(file_path, os.F_OK):
        print("[Get_List]Given file path is exist.")
        # 默认最后一行是子景点，读入此景点的父节点以及父景点写入的子景点页数（从1开始）
        # 读入已经爬取到的父景点所在页数，父景点的子景点页数以及父景点的ID
        sub_page_byte = get_last_line(file_path).split()[-1]
        # 判断是否只有表头没有数据
        if sub_page_byte.decode(encoding='utf-8') == "data":
            print("[Get_List]The file is exist but no data.")
        else:
            father_id_byte = get_last_line(file_path).split()[-2]
            page_byte = get_last_line(file_path).split()[5]
            page = int(page_byte.decode(encoding='utf-8'))
            subpage = int(sub_page_byte.decode(encoding='utf-8'))
            father_id = int(father_id_byte.decode(encoding='utf-8'))
            # 判断最后一行内容是子景点还是父景点，如果是父景点，则将fatherId置为该景点
            if father_id == 0:
                father_id_byte = get_last_line(file_path).split()[2]
                father_id = int(father_id_byte.decode(encoding='utf-8'))
            print("[Get_List]Already spider page :", page)
            print("[Get_List]Already spider sub_page :", subpage)
    else:
        with open(file_path, 'a+', encoding='utf-8') as f:
            f.write("name\ttype_id\tid\tlat\tlng\tpage\tfather_name\tfather_id\tsub_page\n")

    # 删掉之前爬过的父景点
    if father_id != 0:
        list_loc_copy = copy.deepcopy(list_location)
        for poi in list_loc_copy:
            if poi[2] != str(father_id):
                list_location.remove(poi)
            else:
                break

    return list_location, father_id, subpage


<<<<<<< HEAD
def prepare_request(poiid, sub_page, ip_list, userAgent, headers):
=======
def prepare_request(poiid, sub_page, ip_list):
>>>>>>> 04ae88d9ca59538b7d55c396b3bd2e35fc1cdacb
    """
    构建opener对象以及完整的请求内容，其中包括参数，headers和代理IP
    :param poiid: 请求参数：子景点poiid
    :param sub_page: 请求参数：子景点页数
    :param ip_list: 可用的代理IP
    :return: opener, req
    """

    # 构建请求内容
    url = get_url(poiid, sub_page)
    headers['User-Agent'] = choice(userAgent)
    req = request.Request(url, headers=headers)

    # 构建opener
    # 基本的urlopen()方法不支持代理、cookie等其他的HTTP/HTTPS高级功能
    # 需要通过urllib2.build_opener()方法来使用这些处理器对象
    proxy_handler = request.ProxyHandler(choice(ip_list))
    opener = request.build_opener(proxy_handler)
    return opener, req


def clean_file(file_path):
    """
    清理一遍文档，因为有些景点本身就是一个父景点，还是其他父景点的子景点
    :param file_path: 文件路径
    :return: 无
    """
    loc_list = get_list(file_path)
    print(loc_list)

    loc_list_clean = []
    loc_poi_clean = []
    for poi_tuple in loc_list:
        if poi_tuple[2] not in loc_poi_clean:
            loc_poi_clean.append(poi_tuple[2])
            loc_list_clean.append(poi_tuple)

    with open(file_path, 'w+', encoding='utf-8') as file:
        file.truncate()
        file.write("name\ttype_id\tid\tlat\tlng\tpage\tfather_name\tfather_id\tsub_page\n")
        for poi_tuple in loc_list_clean:
            file.write(str(poi_tuple[0]) + "\t" + str(poi_tuple[1]) + "\t" +
                       str(poi_tuple[2]) + "\t" + str(poi_tuple[3]) + "\t" +
                       str(poi_tuple[4]) + "\t" + str(poi_tuple[5]) + "\t" +
                       str(poi_tuple[6]) + "\t" + str(poi_tuple[7]) + "\t" +
                       str(poi_tuple[8]) + "\n")


<<<<<<< HEAD
def get_subpoi(province_id, initFilePath, filePath):
    headers, userAgent = head_useragent()

    initFilePath = "./data/" + province_id + "_list_all.txt"
    filePath = "./data/" + province_id + "_list_all_sub.txt"
=======
if __name__ == "__main__":

    headers, userAgent = head_useragent()

    initFilePath = "./data/list_all.txt"
    filePath = "./data/list_all_sub.txt"
>>>>>>> 04ae88d9ca59538b7d55c396b3bd2e35fc1cdacb

    list_loc, fatherId, sub_page = get_starter(initFilePath, filePath)

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
<<<<<<< HEAD
            opener, req = prepare_request(poi[2], sub_page, ip_list, userAgent, headers)
=======
            opener, req = prepare_request(poi[2], sub_page, ip_list)
>>>>>>> 04ae88d9ca59538b7d55c396b3bd2e35fc1cdacb

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
                # 严谨，防止信息不匹配
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

    # 因为有的景点可能既是一个独立的景点，又同时属于某一个景点的子景点，那么它就会存在两次
    clean_file(filePath)
<<<<<<< HEAD


if __name__ == "__main__":
    province_id = "11239"

    get_subpoi(province_id)
=======
>>>>>>> 04ae88d9ca59538b7d55c396b3bd2e35fc1cdacb
