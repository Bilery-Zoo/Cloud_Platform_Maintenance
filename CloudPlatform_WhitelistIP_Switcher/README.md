"""
create_author : Bilery Zoo(652645572@qq.com)
create_time   : 2019-09-09
remark       : *_* Reference Manual *_*
"""


            　　 　 　　　　 　 |＼＿/|
            　　 　 　　　　 　 | ・x・ |
            　　 ＼＿＿＿＿＿／　　　 |
            　　 　 |　　　 　　　　　|    私はBilery Zooです...
            　　　　＼　　　　　 　ノ　
            　（（（　(/￣￣￣￣(/ヽ)


About Script

        This script is to perform a general handler of switching WhitelistIP setting for access control to cloud environment in
    cloud platform of AWS and AlibabaCloud(Microsoft Azure's script developing task was deprecated on 2019/09/06).
    The script is mainly designed doing two jobs:
        ①. Append new WhitelistIP into access control of cloud platform services which has old WhitelistIP configured;
        ②. Delete old WhitelistIP from access control of cloud platform services which has new WhitelistIP appended.

About Files

        Module folders, files and its notices are:
            ├── alibabacloud_new_whitelistip_append.py
            ├── alibabacloud_old_whitelistip_delete.py
            ├── aws_new_whitelistip_append.py
            ├── aws_old_whitelistip_delete.py
            ├── config
            │   ├── auth.py
            ├── lib
            │   └── log.py
            ├── README.md
            ├── requirements.txt
            └── switcher
                ├── AlibabaCloud_WhitelistIP_Switcher
                │   ├── functions.py
                │   ├── README.md
                │   ├── requirements.txt
                │   └── whitelistip_switcher.py
                ├── AWS_WhitelistIP_Switcher
                │   ├── functions.py
                │   ├── README.md
                │   ├── requirements.txt
                │   └── whitelistip_switcher.py
                └── switcher.py
    ①. /config
        Config defination directory.
        Current version mainly includes authentications to connect to cloud platform.
    ②. /lib
        User-define library directory.
        Current version mainly includes log logging module.
    ③. /switcher
        Main program defination directory.
        Current version includes WhitelistIP switching functions of AWS and AlibabaCloud, read each sub folders for detail.
    ④. aws_new_whitelistip_append.py
        Call file of new WhitelistIP appending to AWS platform.
    ⑤. aws_old_whitelistip_delete.py
        Call file of old WhitelistIP deleting to AWS platform.
    ⑥. alibabacloud_new_whitelistip_append.py
        Call file of new WhitelistIP appending to AlibabaCloud platform.
    ⑦. alibabacloud_old_whitelistip_delete.py
        Call file of old WhitelistIP deleting to AlibabaCloud platform.
    ⑧. requirements.txt
        Third-party packages of Python needing to install.
        
About Deployment

        Requirements to execute this script, see below:
    ①. OS
        Any.
    ②. Programming Language
        Python 3.6 or upper.
            Because of using standard library `typing` released in Python v3.6 to mark data types
            of UDF arguments, Python 3.6 or upper is required.
        Third-party packages.
            Third-party packages of Python, see `requirements.txt` for reference.
    ③. Others
        None.
