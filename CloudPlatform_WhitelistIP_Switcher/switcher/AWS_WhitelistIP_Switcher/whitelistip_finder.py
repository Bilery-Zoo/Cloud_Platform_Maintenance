#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
create_author : Bilery Zoo(bilery.zoo@gmail.com)
create_time   : 2019-10-01
program       : *_* find WhitelistIP info file(AWS) *_*
"""


from . import functions
from CloudPlatform_WhitelistIP_Switcher.config.auth import aws_region_list


def get_whitelistip_info(ip, key, region=None, is_region_distinguish=False, ) -> list:
    """
    Get WhitelistIP Info.
    :param ip: IP to get info.
    :param key: AWS access key.
    :param region: AWS region name.
    :param is_region_distinguish: Whether distinguishing region or not.
    :return: List, [{}, ].
    """
    info_list = []
    region_list = aws_region_list
    if not is_region_distinguish:
        region_list = [region] if region else [aws_region_list[0]]
    # services which region not distinguish
    region = region_list[0]
    aws_find = functions.AWS(key, region)
    for waf_whitelistip in aws_find.get_waf_whitelistip_info(ip):
        info_list.append({"Region": region, "Service": "WAF Web ACLs", "IP": ip,
                         "Id": waf_whitelistip["IPSetId"], "Name": "-", "Detail": waf_whitelistip})
    for s3_whitelistip in aws_find.get_s3_whitelistip_info(ip):
        info_list.append({"Region": region, "Service": "S3 Policy", "IP": ip,
                          "Id": "-", "Name": s3_whitelistip["Bucket"], "Detail": s3_whitelistip})
    # services which region distinguish
    for region in region_list:
        aws_find = functions.AWS(key, region)
        for ec2_whitelistip in aws_find.get_ec2_whitelistip_info(ip):
            info_list.append({"Region": region, "Service": "EC2/VPC Security Groups", "IP": ip,
                              "Id": ec2_whitelistip["GroupId"], "Name": "-", "Detail": ec2_whitelistip})
    return info_list
