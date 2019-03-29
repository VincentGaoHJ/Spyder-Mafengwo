# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 10:03:41 2018

@author: gaoha
"""

import random
import requests
import telnetlib
from random import choice
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

userAgent = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)"]


def get_proxy(aip):
    """
    构建格式化的单个proxies
    """
    proxy_ip = 'http://' + aip
    proxy_ips = 'https://' + aip
    proxy = {'https': proxy_ips, 'http': proxy_ip}
    return proxy


def get_ip_list(url, headers):
    """ 
    从代理网站上获取代理
    """
    rand = random.randint(2, 3)
    print("[Get_IP]Randomly chose page %d to spider the valid IP" % rand)
    url = url + "/" + str(rand)
    print("[Get_IP]URL:", url)
    ip_list = []
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'lxml')
    ul_list = soup.find_all('tr')
    print("[Get_IP]The number of IPs: ", len(ul_list))
    for i in range(random.randint(1, 10), len(ul_list)):
        line = ul_list[i].find_all('td')
        ip = line[1].text
        port = line[2].text
        address = ip + ':' + port
        proxy = get_proxy(address)
        try:
            # telnetlib.Telnet(ip, port=port, timeout=20)
            requests.get('http://www.mafengwo.cn/', proxies=proxy)
        except:
            print('[Get_IP]Failed IP.')
        else:
            print('[Get_IP]Valid IP.')
            print("[Get_Valid_IP]", proxy)
            ip_list.append(proxy)
            return ip_list
    return ip_list


def recursive(url, headers):
    try:
        ip_list = get_ip_list(url, headers)
    except:
        print("Failed to get valid ips, try again...")
        ip_list = recursive(url, headers)
    return ip_list


def prepare_proxy():
    """
    准备代理IP池以及随机生成user_agent，并且验证IP可用
    """
    url = 'http://www.xicidaili.com/wt'
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    headers['User-Agent'] = choice(userAgent)
    ip_list = recursive(url, headers)

    return (ip_list)


if __name__ == "__main__":
    url = 'http://www.xicidaili.com/wt'
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    ip_list = get_ip_list(url, headers)
    print(ip_list)
