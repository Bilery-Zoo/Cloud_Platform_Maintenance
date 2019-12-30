#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
create_author : Bilery Zoo(bilery.zoo@gmail.com)
create_time   : 2019-09-05
program       : *_* Authorization relevant config file *_*
"""

"""
*******************************************************************************

            　　 　 　　　　 　 |＼＿/|
            　　 　 　　　　 　 | ・x・ |
            　　 ＼＿＿＿＿＿／　　　 |
            　　 　 |　　　 　　　　　|    私もBilery Zooです...
            　　　　＼　　　　　 　ノ　
            　（（（　(/￣￣￣￣(/ヽ)

AlibabaCloud Access Info:

    To generate access info please visit Resource Access Management (RAM) service of AlibabaCloud. See also
    https://help.aliyun.com/product/28625.html?spm=a2c4g.11186623.6.540.27cb1c72p8iXmj
        AlibabaCloud_Access_Key -> AlibabaCloud Environment Access key & Secret key
        
    About AlibabaCloud available region list, see also
    https://www.alibabacloud.com/help/zh/doc-detail/40654.htm
        alibabacloud_region_list     -> AlibabaCloud region set

*******************************************************************************
"""
AlibabaCloud_Access_Key = {"ak": "",
                           "secret": "",
                           }

alibabacloud_region_list = (
    "ap-northeast-1", "cn-qingdao", "cn-beijing", "cn-zhangjiakou", "cn-huhehaote", "cn-hangzhou", "cn-shanghai",
    "cn-shenzhen", "cn-chengdu", "cn-hongkong", "ap-southeast-1", "ap-southeast-2", "ap-southeast-3", "ap-southeast-5",
    "ap-south-1", "us-west-1", "us-east-1", "eu-central-1", "eu-west-1", "me-east-1",
)

"""
*******************************************************************************

            　　 　 　　　　 　 |＼＿/|
            　　 　 　　　　 　 | ・x・ |
            　　 ＼＿＿＿＿＿／　　　 |
            　　 　 |　　　 　　　　　|    私もBilery Zooです...
            　　　　＼　　　　　 　ノ　
            　（（（　(/￣￣￣￣(/ヽ)

AWS Access Info:

    To generate access info please visit Identity & Access Management (IAM) service of AWS. See also
    https://docs.aws.amazon.com/en_pv/IAM/latest/UserGuide/introduction.html
        AWS_Access_Key -> AWS Environment Access key & Secret key

    About AWS available region list, see also
    https://docs.aws.amazon.com/en_pv/AmazonRDS/latest/UserGuide/Concepts.RegionsAndAvailabilityZones.html
        aws_region_list     -> AWS region set

*******************************************************************************
"""
AWS_Access_Key = {"aws_access_key_id": "",
                  "aws_secret_access_key": "",
                  }

aws_region_list = (
    "ap-northeast-1", "us-west-1", "us-east-1", "us-east-2", "us-west-2", "ap-south-1", "ap-northeast-2",
    "ap-southeast-1", "ap-southeast-2", "ca-central-1", "eu-central-1", "eu-west-1", "eu-west-2",
    "eu-west-3", "eu-north-1", "sa-east-1",
)

# User Auth Input
user_auth = "Please"
