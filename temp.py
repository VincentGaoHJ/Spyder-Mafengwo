# -*- coding: utf-8 -*-
"""
@Date: Created on Tue Mar 26 21:25:29 2019
@Author: Haojun Gao
@Description: 用于调试代码
"""

<<<<<<< HEAD
=======
import csv

with open("test.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile)

    # 先写入columns_name
    writer.writerow(["index", "a_name", "b_name"])
    # 写入多行用writerows
    writer.writerows([[0, 1, 3], [1, 2, 3], [2, 3, 4]])

with open("test.csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    # 这里不需要readlines
    for line in reader:
        print(line)
>>>>>>> 04ae88d9ca59538b7d55c396b3bd2e35fc1cdacb
