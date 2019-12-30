#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
create_author : Bilery Zoo(bilery.zoo@gmail.com)
create_time   : 2019-09-05
program       : *_* switch WhitelistIP call file(AWS) *_*
"""


from . import functions
from CloudPlatform_WhitelistIP_Switcher.config.auth import aws_region_list


def new_whitelistip_append(old_whitelistip, new_whitelistip, key, region=None, is_region_distinguish=False, ):
    """
    Append new WhitelistIP.
    :param old_whitelistip: IP to get info.
    :param new_whitelistip: IP to add info.
    :param key: AWS access key.
    :param region: AWS region name.
    :param is_region_distinguish: Whether distinguishing region or not.
    :return: Python built-in exit code.
    """
    region_list = aws_region_list
    if not is_region_distinguish:
        region_list = [region] if region else [aws_region_list[0]]
    # services which region not distinguish
    region = region_list[0]
    aws_switch = functions.AWS(key, region)
    aws_switch.modify_waf_whitelistip_info(old_whitelistip, "INSERT", new_ip=new_whitelistip)
    aws_switch.modify_s3_whitelistip_info(old_whitelistip, "INSERT", new_ip=new_whitelistip)
    # services which region distinguish
    for region in region_list:
        aws_switch = functions.AWS(key, region)
        aws_switch.add_ec2_whitelistip_info(old_whitelistip, new_whitelistip)


def old_whitelistip_delete(old_whitelistip, key, region=None, is_region_distinguish=False, ):
    """
    Delete old WhitelistIP.
    :param old_whitelistip: IP to get info.
    :param key: AWS access key.
    :param region: AWS region name.
    :param is_region_distinguish: Whether distinguishing region or not.
    :return: Python built-in exit code.
    """
    region_list = aws_region_list
    if not is_region_distinguish:
        region_list = [region] if region else [aws_region_list[0]]
    # services which region not distinguish
    region = region_list[0]
    aws_switch = functions.AWS(key, region)
    aws_switch.modify_waf_whitelistip_info(old_whitelistip, "DELETE")
    aws_switch.modify_s3_whitelistip_info(old_whitelistip, "DELETE")
    # services which region distinguish
    for region in region_list:
        aws_switch = functions.AWS(key, region)
        aws_switch.remove_ec2_whitelistip_info(old_whitelistip)
