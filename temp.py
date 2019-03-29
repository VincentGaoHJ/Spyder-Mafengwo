# -*- coding: utf-8 -*-
"""
@Date: Created on Tue Mar 26 21:25:29 2019
@Author: Haojun Gao
@Description: 用于调试代码
"""

import re
from html.parser import HTMLParser


pattern = re.compile("/poi/(.*).html", re.IGNORECASE)
sub_poi = pattern.findall("/poi/11111.html")
print(sub_poi)
