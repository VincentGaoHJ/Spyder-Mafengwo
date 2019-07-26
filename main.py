# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/7/26
@Author: Haojun Gao
@Description: 
"""

from getList import get_list
from getList_subpoi import get_subpoi
from getComments import get_comments

if __name__ == '__main__':
    # 北京：10065
    # 昆明：10807
    # 贵阳：11239
    # 杭州：10156

    province_id = "10156"

    poi_path = "./data/" + province_id + "_list_all.txt"
    subpoi_path = "./data/" + province_id + "_list_all_sub.txt"
    comment_path = "./data/" + province_id + "_comment_all.csv"

    get_list(province_id, poi_path)
    get_subpoi(province_id, poi_path, subpoi_path)
    get_comments(province_id, subpoi_path, comment_path)
