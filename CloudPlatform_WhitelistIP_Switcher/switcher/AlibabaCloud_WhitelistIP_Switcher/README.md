"""
create_author : Bilery Zoo(652645572@qq.com)
create_time   : 2019-08-30
remark       : *_* Reference Manual *_*
"""


            　　 　 　　　　 　 |＼＿/|
            　　 　 　　　　 　 | ・x・ |
            　　 ＼＿＿＿＿＿／　　　 |
            　　 　 |　　　 　　　　　|    私はBilery Zooです...
            　　　　＼　　　　　 　ノ　
            　（（（　(/￣￣￣￣(/ヽ)


About Script

        This script is to switch WhitelistIP setting for access control to cloud environment in AlibabaCloud.
    The script is mainly designed doing two jobs:
    1. Append new WhitelistIP into access control of AlibabaCloud services which has old WhitelistIP configured;
    2. Delete old WhitelistIP from access control of AlibabaCloud services which has new WhitelistIP appended.

About Files

        Module files and its notices are:
    1. functions.py
        Base functions of AlibabaCloud handlers module.
        ** May need OOP rewriting next time **
        * 2019-09-04： re-construct in OOP *
    2. log.py
        Log logging module.
        * 2019-09-04： re-construct and move to CloudPlatform_WhitelistIP_Switcher/lib *
    3. new_whitelistip_append.py
        Call file of new WhitelistIP appending.
        * 2019-09-04： re-construct and move to CloudPlatform_WhitelistIP_Switcher *
    4. old_whitelistip_delete.py
        Call file of old WhitelistIP deleting.
        * 2019-09-04： re-construct and move to CloudPlatform_WhitelistIP_Switcher *
    5. requirements.txt
        Third-party packages of Python needing to install.
        
About Deployment

        Requirements to execute this script, see below:
    1. OS
        Any.
    2. Programming Language
        Python 3.6 or upper.
            Because of using standard library `typing` released in Python v3.6 to mark data types
            of UDF arguments, Python 3.6 or upper is required.
        Third-party packages.
            Third-party packages of Python, see `requirements.txt` for reference.
    3. Others
        None.
