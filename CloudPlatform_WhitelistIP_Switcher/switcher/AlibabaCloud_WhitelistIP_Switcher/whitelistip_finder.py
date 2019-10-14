#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
create_author : Bilery Zoo(652645572@qq.com)
create_time   : 2019-10-01
program       : *_* find WhitelistIP info file(AlibabaCloud) *_*
"""


from . import functions
from CloudPlatform_WhitelistIP_Switcher.config.auth import alibabacloud_region_list
from aliyunsdkcore.acs_exception.exceptions import ClientException, ServerException


def get_whitelistip_info(ip, region=None, is_region_distinguish=False, ) -> list:
    """
    Get WhitelistIP Info.
    :param ip: IP to get info.
    :param region: AlibabaCloud region name.
    :param is_region_distinguish: Whether distinguishing region or not.
    :return: List, [{}, ].
    """
    info_list = []
    region_list = alibabacloud_region_list
    if not is_region_distinguish:
        region_list = [region] if region else [alibabacloud_region_list[0]]
    try:
        # services which region not distinguish
        region = region_list[0]
        alibabacloud_find = functions.AlibabaCloud(region)
        for cdn_whitelistip in alibabacloud_find.get_cdn_whitelistip_info(ip):
            info_list.append({"Region": region, "Service": "CDN(Access Control)", "IP": ip,
                              "Id": '-', "Name": cdn_whitelistip["DomainNames"], "Detail": cdn_whitelistip})
        # services which region distinguish
        for region in region_list:
            alibabacloud_find = functions.AlibabaCloud(region)
            for slb_whitelistip in alibabacloud_find.get_slb_whitelistip_info(ip):
                info_list.append({"Region": region, "Service": "SLB(Access Control)", "IP": ip,
                                  "Id": slb_whitelistip["AclId"], "Name": slb_whitelistip["AclName"], "Detail": slb_whitelistip})
            for rds_whitelistip in alibabacloud_find.get_rds_whitelistip_info(ip):
                info_list.append({"Region": region, "Service": "RDS(Data Security)", "IP": ip,
                                 "Id": rds_whitelistip["DBInstanceId"], "Name": rds_whitelistip["DBInstanceIPArrayName"], "Detail": rds_whitelistip})
    except (ClientException, ServerException):
        pass
    return info_list
