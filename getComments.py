# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 11:38:43 2018

@author: gaoha
"""

import os
import sys
import json
import urllib
from random import choice
from proxy import prepare_proxy
from proxy_github import getProxy


headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
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


def get_last_line(inputfile):
    filesize = os.path.getsize(inputfile)
    blocksize = 1024
    dat_file = open(inputfile, 'rb')
    last_line = ""
    if filesize > blocksize:
        maxseekpoint = (filesize // blocksize)
        dat_file.seek((maxseekpoint - 1) * blocksize)
    elif filesize:
        # maxseekpoint = blocksize % filesize
        dat_file.seek(0, 0)
    lines = dat_file.readlines()
    if lines:
        last_line = lines[-1].strip()
    # print "last line : ", last_line
    dat_file.close()
    return last_line


def get_list(inputfile):
    list_loc = []
    with open(inputfile, 'r',encoding='utf-8') as f:
        next(f)
        for line in f.readlines():
            list = line.strip().split()
            list_loc.append((list[0],list[2],list[5]))
    #print(list_loc)
    return list_loc


get_url_base = "http://wxapp.mafengwo.cn/gonglve/poi/?jsondata="

json_base_1 = "{%22data_style%22:%22comment_list%22,%22filter_style%22:%22comment%22,%22filter%22:{%22poiid%22:%22"
json_base_2 = "%22,%22tag%22:0},%22page%22:{%22no%22:"
json_base_3 = ",%22num%22:30}}"

initFilePath = "./data/list_all.txt"
if os.access(initFilePath, os.F_OK):
    print ("[Get_Comments]Basic file is exist.")
else:
    print ("[Get_Comments]Basic file is not exist, please run getList.py first.")
    sys.exit(0)


list_loc = get_list(initFilePath)


page = 0

filePath = "./data/comment_all.txt"
if os.access(filePath, os.F_OK):
    print ("[Get_Comments]Given file path is exist.")
    last_line_list = get_last_line(filePath).split()
    poiid = int(last_line_list[0].decode(encoding='utf-8'))
    page = int(last_line_list[1].decode(encoding='utf-8'))
    print ("[Continue]Already Spider POI :",poiid)
    print ("[Continue]Already Spider Page :",page)
    for i in range(len(list_loc)):
        if int(list_loc[0][1]) != poiid:
            del list_loc[0]
        else:
            break
else:
    print("[Get_Comments]Start Collecting Comments")
        
        
ip_list = getProxy()

total_number = len(list_loc)

for i in range(total_number):
    with open(filePath, 'a+',encoding='utf-8') as f:
        while(page < 21):
            page += 1
            poiid = list_loc[i][1]
            json_str = json_base_1 + str(poiid) + json_base_2 + str(page) + json_base_3
            get_url = get_url_base + json_str
            headers['User-Agent'] = choice(userAgent)
            req = urllib.request.Request(get_url, headers=headers)
            proxy_handler = urllib.request.ProxyHandler(choice(ip_list))
            opener = urllib.request.build_opener(proxy_handler)
            try:
                response = opener.open(req)
            except:
                print("[Get_Comments]False to spider "+str(poiid)+" page "+str(page))
                page -= 1
                ip_list = getProxy()
            else:
                response_context = response.read()
                if any(response_context) == False:
                    print("Seccessful but nothing")
                    print(page)
                    continue
                print("["+str(i)+"/"+str(total_number)+"]Success to spider "+str(poiid)+" page "+str(page))
                # 返回的是一个json格式的字符串，将字符串转为dict对象
                data_json = json.loads(response_context.decode("utf8"))
                data = data_json.get("data")
                if data["page"]["next"] == True:
                    for loc in data["list"]:
                        f.write(str(poiid) + "\t" + str(data["page"]["no"]) + "\t" + 
                                str(loc["comment"]) + "\n")
                else:
                    print("[Get_Comments]Done write file "+str(list_loc[i][0])+" page number is "+str(page))
                    break
        page = 0

