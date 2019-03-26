# -*- coding: utf-8 -*-
"""
@Date: Created on Tue Dec 11 13:40:14 2018
@Author: Haojun Gao
@Description: 
"""

import json
import telnetlib
import requests
import random


def get_proxy(host,port,type):
    """
    构建格式化的单个proxies
    """
    if type == "http":
        proxy_ip = 'http://' + str(host) + ':' + str(port)
    else:
        proxy_ip = 'https://' + str(host) + ':' + str(port)
    proxy = {type: proxy_ip}
    return proxy


def getProxy():
    proxy_url = 'https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list'
    print("[Get_IP]URL:",proxy_url)
    response = requests.get(proxy_url)
    proxies_list = response.text.split('\n')
    print("[Get_IP]The number of IPs: ",len(proxies_list))
    skip = random.randint(1, 20)
    for i in range(len(proxies_list)):
        proxy_json = json.loads(proxies_list[i+skip])
        host = proxy_json['host']
        port = proxy_json['port']
        type = proxy_json['type']
        proxy = get_proxy(host,port,type)
        ip_list = []
        try:
            #telnetlib.Telnet(ip, port=port, timeout=20)
            requests.get('http://www.mafengwo.cn/', proxies=proxy)
        except:
            print ('[Get_IP]Failed IP.')
        else:
            print ('[Get_IP]Valid IP.')
            print ("[Get_Valid_IP]",proxy)
            ip_list.append(proxy)
            return ip_list


if __name__ == '__main__':
    getProxy()