#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
create_author : Bilery Zoo(652645572@qq.com)
create_time   : 2019-09-05
program       : *_* switch WhitelistIP call file(AlibabaCloud) *_*
"""


from . import functions
from CloudPlatform_WhitelistIP_Switcher.config.auth import alibabacloud_region_list


def new_whitelistip_append(old_whitelistip, new_whitelistip, comment, region=None, is_region_distinguish=False, ):
    """
    Append new WhitelistIP.
    :param old_whitelistip: IP to get info.
    :param new_whitelistip: IP to add info.
    :param comment: comment of `new_ip` to add info.
    :param region: AlibabaCloud region name.
    :param is_region_distinguish: Whether distinguishing region or not.
    :return: Python built-in exit code.
    """
    region_list = alibabacloud_region_list
    if not is_region_distinguish:
        region_list = [region] if region else [alibabacloud_region_list[0]]
    # services which region not distinguish
    region = region_list[0]
    alibabacloud_switch = functions.AlibabaCloud(region)
    alibabacloud_switch.modify_cdn_whitelistip_info(old_whitelistip, "Append", new_ip=new_whitelistip)
    # services which region distinguish
    for region in region_list:
        alibabacloud_switch = functions.AlibabaCloud(region)
        alibabacloud_switch.add_slb_whitelistip_info(old_whitelistip, new_whitelistip, comment=comment)
        alibabacloud_switch.modify_rds_whitelistip_info(old_whitelistip, "Append", new_ip=new_whitelistip)


def old_whitelistip_delete(old_whitelistip, region=None, is_region_distinguish=False, ):
    """
    Delete old WhitelistIP.
    :param old_whitelistip: IP to get info.
    :param region: AlibabaCloud region name.
    :param is_region_distinguish: Whether distinguishing region or not.
    :return: Python built-in exit code.
    """
    region_list = alibabacloud_region_list
    if not is_region_distinguish:
        region_list = [region] if region else [alibabacloud_region_list[0]]
    # services which region not distinguish
    region = region_list[0]
    alibabacloud_switch = functions.AlibabaCloud(region)
    alibabacloud_switch.modify_cdn_whitelistip_info(old_whitelistip, "Delete")
    # services which region distinguish
    for region in region_list:
        alibabacloud_switch = functions.AlibabaCloud(region)
        alibabacloud_switch.remove_slb_whitelistip_info(old_whitelistip)
        alibabacloud_switch.modify_rds_whitelistip_info(old_whitelistip, "Delete")
