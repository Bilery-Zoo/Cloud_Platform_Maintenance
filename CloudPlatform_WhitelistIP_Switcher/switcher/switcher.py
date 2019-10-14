#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
create_author : Bilery Zoo(652645572@qq.com)
create_time   : 2019-09-06
program       : *_* switch WhitelistIP call file(main interface) *_*
"""


from CloudPlatform_WhitelistIP_Switcher.config.auth import user_auth
from CloudPlatform_WhitelistIP_Switcher.switcher.AWS_WhitelistIP_Switcher import whitelistip_switcher as aws_switcher
from CloudPlatform_WhitelistIP_Switcher.switcher.AlibabaCloud_WhitelistIP_Switcher import whitelistip_switcher as alibabacloud_switcher
from aliyunsdkcore.acs_exception.exceptions import ClientException, ServerException


def switcher(cloud_platform, modify_mode, old_whitelistip,
             new_whitelistip=None, region=None, is_region_distinguish=False, comment="汐留GIP", ):
    """
    Main interface of WhitelistIP switching for cloud platforms.
    :param cloud_platform: Cloud platform(valid values: AWS, AlibabaCloud).
        * Microsoft Azure's script developing task was deprecated on 2019/09/06 *
    :param modify_mode: Modify mode(valid values: append, delete).
    :param old_whitelistip: IP to get info and remove.
    :param new_whitelistip: IP to add info.
    :param region: Region name.
    :param is_region_distinguish: Whether distinguishing region or not.
    :param comment: Comment of `new_ip` to add info into AlibabaCloud SLB.
    :return: Python built-in exit code.
    """

    assert cloud_platform == "AWS" or cloud_platform == "AlibabaCloud"
    assert modify_mode == "append" or modify_mode == "delete"

    trace_info = "Program will doing action >>>\n"
    trace_info += "\n\tCloud Platform: %s" % cloud_platform
    if modify_mode == "append":
        trace_info += "\n\tAction: new WhitelistIP appending"
        trace_info += "\n\tAppending IP: %s" % new_whitelistip
    elif modify_mode == "delete":
        trace_info += "\n\tAction: old WhitelistIP deleting"
        trace_info += "\n\tDeleting IP: %s" % old_whitelistip
    trace_info += "\n\nPlease enter `%s` to make sure the action!!!\n" % user_auth
    user_input = input(trace_info)

    if user_input != user_auth:
        print("Get invalid command, program exit...")
    else:
        if cloud_platform == "AWS":
            if modify_mode == "append":
                aws_switcher.new_whitelistip_append(region, old_whitelistip, new_whitelistip,
                                                    is_region_distinguish=is_region_distinguish)
            elif modify_mode == "delete":
                aws_switcher.old_whitelistip_delete(region, old_whitelistip,
                                                    is_region_distinguish=is_region_distinguish)

        elif cloud_platform == "AlibabaCloud":
            try:
                if modify_mode == "append":
                    alibabacloud_switcher.new_whitelistip_append(region, old_whitelistip, new_whitelistip, comment,
                                                                 is_region_distinguish=is_region_distinguish)
                elif modify_mode == "delete":
                    alibabacloud_switcher.old_whitelistip_delete(region, old_whitelistip,
                                                                 is_region_distinguish=is_region_distinguish)
            except (ClientException, ServerException):
                pass
