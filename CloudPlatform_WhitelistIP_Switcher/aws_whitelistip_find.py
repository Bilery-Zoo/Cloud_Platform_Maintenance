#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
create_author : Bilery Zoo(652645572@qq.com)
create_time   : 2019-10-01
program       : *_* Get WhitelistIP info call file of AWS *_*
"""


import csv
from CloudPlatform_WhitelistIP_Switcher.switcher.AWS_GIP_Switcher import whitelistip_finder


"""
*******************************************************************************
Unit test button
            　　 　 　　　　 　 |＼＿/|
            　　 　 　　　　 　 | ・x・ |
            　　 ＼＿＿＿＿＿／　　　 |
            　　 　 |　　　 　　　　　|    私もBilery Zooです...
            　　　　＼　　　　　 　ノ　
            　（（（　(/￣￣￣￣(/ヽ)
"""
UT_FLAG: bool = True
"""
Default `True` for script testing
Set to `False` when production using
*******************************************************************************
"""

ip_list: list = ["127.0.0.0", ] if UT_FLAG else ["127.0.0.0", "127.0.0.1", ]

data_info = []
for ip in ip_list:
    for ip_info in whitelistip_finder.get_whitelistip_info(account, ip, is_region_distinguish=True):
        data_info.append(ip_info)

data_header: list = ["Account", "Region", "Service", "IP", "Id", "Name", "Detail"]
with open("./AWS_GIP_Check_Result.csv", 'w') as f:
    csv_out = csv.DictWriter(f, data_header)
    csv_out.writeheader()
    csv_out.writerows(data_info)
