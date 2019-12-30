"""
create_author : Bilery Zoo(bilery.zoo@gmail.com)
create_time   : 2019-09-09
remark       : *_* README *_*
"""


            　　 　 　　　　 　 |＼＿/|
            　　 　 　　　　 　 | ・x・ |
            　　 ＼＿＿＿＿＿／　　　 |
            　　 　 |　　　 　　　　　|    私はBilery Zooです...
            　　　　＼　　　　　 　ノ　
            　（（（　(/￣￣￣￣(/ヽ)


About Script

        This script is to archive a general handler of switching WhitelistIP setting for access control to cloud environment in
    cloud platform of AWS and AlibabaCloud(Microsoft Azure's script developing task was deprecated on 2019/09/06).
    The script is mainly designed doing two jobs:
        ①. Append new WhitelistIP into access control of cloud platform services which has old WhitelistIP configured;
        ②. Delete old WhitelistIP from access control of cloud platform services which has new WhitelistIP appended.
        
        Read `Reference Manual` file for more executing information.

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
                │   └── whitelistip_switcher.py
                ├── AWS_WhitelistIP_Switcher
                │   ├── functions.py
                │   └── whitelistip_switcher.py
                └── switcher.py
    1. /config
        Config defination directory.
        Current version mainly includes authentications to connect to cloud platform.
    2. /lib
        User-define library directory.
        Current version mainly includes log logging module.
    3. /switcher
        Main program defination directory.
        Current version includes WhitelistIP switching functions of AWS and AlibabaCloud, read each sub folders for detail.
    4. aws_new_whitelistip_append.py
        Call file of new WhitelistIP appending to AWS platform.
    5. aws_old_whitelistip_delete.py
        Call file of old WhitelistIP deleting to AWS platform.
    6. aws_whitelistip_find.py
        Call file of finding WhitelistIP config info in AlibabaCloud platform(generate a .csv result file in default).
    7. alibabacloud_new_whitelistip_append.py
        Call file of new WhitelistIP appending to AlibabaCloud platform.
    8. alibabacloud_old_whitelistip_delete.py
        Call file of old WhitelistIP deleting to AlibabaCloud platform.
    9. alibabacloud_whitelistip_find.py
        Call file of finding WhitelistIP config info in AWS platform(generate a .csv result file in default).
    10. requirements.txt
        Third-party packages of Python needing to install.
        
About Deployment

        Requirements to execute this script, see below:
    ①. OS
        Unix-like.
    ②. Programming Language
        Python 3.6 or upper.
            Because of using standard library `typing` released in Python v3.6 to mark data types
            of UDF arguments, Python 3.6 or upper is required.
        Third-party packages.
            Third-party packages of Python, see `requirements.txt` for reference.
    ③. Others
        None.
