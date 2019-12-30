#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
create_author : Bilery Zoo(bilery.zoo@gmail.com)
create_time   : 2019-09-05
program       : *_* Old WhitelistIP deleting call file of AlibabaCloud *_*
"""


from CloudPlatform_WhitelistIP_Switcher.switcher import switcher
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
old_whitelistip = "127.0.0.0"

"""

    key
        -> Access key(set in `/config/auth.py` file) to the specified AlibabaCloud platform account
    old_whitelistip
        -> Whitelistip to remove(******Warning: this script does the removing action)

************************************************************************************************************************
"""


switcher.switcher(cloud_platform="AlibabaCloud", modify_mode="delete", old_whitelistip=old_whitelistip,
                  key=key, is_region_distinguish=False)
