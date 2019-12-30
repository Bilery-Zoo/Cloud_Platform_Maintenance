#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
create_author : Bilery Zoo(bilery.zoo@gmail.com)
create_time   : 2019-10-01
program       : *_* Get WhitelistIP info call file of AlibabaCloud *_*
"""


import csv
from CloudPlatform_WhitelistIP_Switcher.switcher.AlibabaCloud_WhitelistIP_Switcher import whitelistip_finder
from CloudPlatform_WhitelistIP_Switcher.config.auth import AlibabaCloud_Access_Key


"""
************************************************************************************************************************

Self-definition Config Variable Area, you can modify these values as you need.

            　　 　 　　　　 　 |＼＿/|
            　　 　 　　　　 　 | ・x・ |
            　　 ＼＿＿＿＿＿／　　　 |
            　　 　 |　　　 　　　　　|    私はBilery Zooです...
            　　　　＼　　　　　 　ノ　
            　（（（　(/￣￣￣￣(/ヽ)
"""

key = AlibabaCloud_Access_Key
ip_list: list = ["127.0.0.0", "127.0.0.1", ]

"""

    key
        -> Access key(set in `/config/auth.py` file) to the specified AlibabaCloud platform account
    ip_list
        -> IP(s) which is used for browsing info

************************************************************************************************************************
"""


data_info = []
for ip in ip_list:
    for ip_info in whitelistip_finder.get_whitelistip_info(ip, key, is_region_distinguish=True):
        data_info.append(ip_info)

data_header: list = ["Region", "Service", "IP", "Id", "Name", "Detail"]
with open("./AlibabaCloud_GIP_Check_Result.csv", 'w') as f:
    csv_out = csv.DictWriter(f, data_header)
    csv_out.writeheader()
    csv_out.writerows(data_info)
