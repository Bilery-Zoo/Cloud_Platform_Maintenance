#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
create_author : Bilery Zoo(652645572@qq.com)
create_time   : 2019-09-05
program       : *_* switch WhitelistIP call file(AWS) *_*
"""


from . import functions


def new_whitelistip_append(region, old_whitelistip, new_whitelistip, ):
    """
    Append new WhitelistIP.
    :param region: AWS region name.
    :param old_whitelistip: IP to get info.
    :param new_whitelistip: IP to add info.
    :return: Python built-in exit code.
    """
    aws_switch = functions.AWS(region)
    aws_switch.add_ec2_whitelistip_info(old_whitelistip, new_whitelistip)
    aws_switch.modify_waf_whitelistip_info(old_whitelistip, "INSERT", new_ip=new_whitelistip)
    aws_switch.modify_s3_whitelistip_info(old_whitelistip, "INSERT", new_ip=new_whitelistip)


def old_whitelistip_delete(region, old_whitelistip, ):
    """
    Delete old WhitelistIP.
    :param region: AWS region name.
    :param old_whitelistip: IP to get info.
    :return: Python built-in exit code.
    """
    aws_switch = functions.AWS(region)
    aws_switch.remove_ec2_whitelistip_info(old_whitelistip)
    aws_switch.modify_waf_whitelistip_info(old_whitelistip, "DELETE")
    aws_switch.modify_s3_whitelistip_info(old_whitelistip, "DELETE")
