#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
create_author : Bilery Zoo(652645572@qq.com)
create_time   : 2019-09-05
program       : *_* base functions of AlibabaCloud handlers module *_*
"""

import re
import json
import typing

from aliyunsdkcore.client import AcsClient
from aliyunsdkslb.request.v20140515 import DescribeAccessControlListsRequest, DescribeAccessControlListAttributeRequest
from aliyunsdkslb.request.v20140515 import AddAccessControlListEntryRequest, RemoveAccessControlListEntryRequest
from aliyunsdkcdn.request.v20180510 import DescribeUserDomainsRequest, DescribeCdnDomainConfigsRequest
from aliyunsdkcdn.request.v20180510 import BatchSetCdnDomainConfigRequest
from aliyunsdkrds.request.v20140815 import DescribeDBInstancesRequest, DescribeDBInstanceIPArrayListRequest
from aliyunsdkrds.request.v20140815 import ModifySecurityIpsRequest

from CloudPlatform_WhitelistIP_Switcher.config.auth import AlibabaCloud_Access_Key
from CloudPlatform_WhitelistIP_Switcher.lib.log import LOG, log

logger = LOG().logger()


class AlibabaCloud(object):
    def __init__(self, region, ):
        """
        Init construct.
        :param region: AlibabaCloud region name.
        """
        self.AlibabaCloud_Access_Key = AlibabaCloud_Access_Key
        self.region_id = region

    def __repr__(self):
        repr_str = "AlibabaCloud client built at:\n\t{'Region': %s}" % self.region_id
        logger.info(repr_str)
        return repr_str

    @staticmethod
    def get_ip_pattern(ip):
        """
        Get strictly `re` matching compile pattern of IP.
        :param ip: IP to get pattern.
        :return: `re` compile pattern.
        """
        return re.compile(ip.replace('.', '[.]'))

    @log(logger=logger, if_exit=True)
    def get_cloud_client(self, ):
        """
        Get AlibabaCloud client. See also:
            https://www.alibabacloud.com/help/zh/doc-detail/67117.htm?spm=a2c63.p38356.b99.3.17cd664b0ByM3l
        :return: AlibabaCloud client object.
        """
        return AcsClient(region_id=self.region_id, **self.AlibabaCloud_Access_Key)

    @log(logger=logger, if_exit=True)
    def get_slb_whitelistip_info(self, ip, ) -> typing.Generator:
        """
        Get WhitelistIP info of SLB Access Control.
        :param ip: IP to get info.
        :return: Dict, {"AclId": ..., }.
        """
        client = self.get_cloud_client()
        request = DescribeAccessControlListsRequest.DescribeAccessControlListsRequest()
        response = client.do_action_with_exception(request)
        for instance in json.loads((response.decode("utf-8")))["Acls"]["Acl"]:
            request_sub = DescribeAccessControlListAttributeRequest.DescribeAccessControlListAttributeRequest()
            request_sub.set_AclId(instance["AclId"])
            response_sub = client.do_action_with_exception(request_sub)
            whitelistip_info = json.loads((response_sub.decode("utf-8")))
            if re.search(self.get_ip_pattern(ip), str(whitelistip_info)):
                logger.info("get_slb_whitelistip_info:\n\t{whitelistip_info}".format(whitelistip_info=whitelistip_info))
                yield whitelistip_info

    @log(logger=logger, if_exit=True)
    def get_cdn_whitelistip_info(self, ip, ) -> typing.Generator:
        """
        Get WhitelistIP info of SLB Access Control.
        :param ip: IP to get info.
        :return: Dict, {"DomainNames": ..., }.
        """
        client = self.get_cloud_client()
        request = DescribeUserDomainsRequest.DescribeUserDomainsRequest()
        response = client.do_action_with_exception(request)
        for instance in json.loads((response.decode("utf-8")))["Domains"]["PageData"]:
            request_sub = DescribeCdnDomainConfigsRequest.DescribeCdnDomainConfigsRequest()
            request_sub.set_DomainName(instance["DomainName"])
            response_sub = client.do_action_with_exception(request_sub)
            data_sub = json.loads((response_sub.decode("utf-8")))
            if re.search(self.get_ip_pattern(ip), str(data_sub)):
                for config in data_sub["DomainConfigs"]["DomainConfig"]:
                    if config["FunctionName"] == "ip_allow_list_set":
                        whitelistip_info = {"DomainNames": instance["DomainName"],
                                            "ip_allow_list_set": config["FunctionArgs"]["FunctionArg"][0]["ArgValue"]}
                        logger.info(
                            "get_cdn_whitelistip_info:\n\t{whitelistip_info}".format(whitelistip_info=whitelistip_info))
                        yield whitelistip_info
                        break

    @log(logger=logger, if_exit=True)
    def get_rds_whitelistip_info(self, ip, ) -> typing.Generator:
        """
        Get WhitelistIP info of RDS Data Security.
        :param ip: IP to get info.
        :return: Dict, {"DBInstanceId": ..., }.
        """
        client = self.get_cloud_client()
        request = DescribeDBInstancesRequest.DescribeDBInstancesRequest()
        response = client.do_action_with_exception(request)
        for instance in json.loads((response.decode("utf-8")))["Items"]["DBInstance"]:
            request_sub = DescribeDBInstanceIPArrayListRequest.DescribeDBInstanceIPArrayListRequest()
            request_sub.set_DBInstanceId(instance["DBInstanceId"])
            response_sub = client.do_action_with_exception(request_sub)
            data_sub = json.loads((response_sub.decode("utf-8")))
            if re.search(self.get_ip_pattern(ip), str(data_sub)):
                for config in data_sub["Items"]["DBInstanceIPArray"]:
                    if re.search(self.get_ip_pattern(ip), str(config)):
                        whitelistip_info = {"DBInstanceId": instance["DBInstanceId"],
                                            "DBInstanceIPArrayName": config["DBInstanceIPArrayName"],
                                            "DBInstanceIPArrayAttribute": config["DBInstanceIPArrayAttribute"],
                                            "WhitelistNetworkType": config["WhitelistNetworkType"],
                                            "SecurityIPType": config["SecurityIPType"],
                                            "CheckInfo": config}
                        logger.info(
                            "get_rds_whitelistip_info:\n\t{whitelistip_info}".format(whitelistip_info=whitelistip_info))
                        yield whitelistip_info
                        break

    @log(logger=logger, if_exit=True)
    def add_slb_whitelistip_info(self, ip, new_ip, comment, ):
        """
        Add WhitelistIP info into SLB Access Control. See also:
            https://www.alibabacloud.com/help/zh/doc-detail/70023.htm
        :param ip: IP to get info.
        :param new_ip: IP to add info.
        :param comment: comment of `new_ip` to add info.
        :return: Python built-in exit code.
        """
        client = self.get_cloud_client()
        add_entry = [{"entry": "{new_ip}/32".format(new_ip=new_ip), "comment": comment}, ]
        for whitelistip_info in self.get_slb_whitelistip_info(ip):
            if re.search(self.get_ip_pattern(new_ip), str(whitelistip_info)):
                continue
            acl_id = whitelistip_info["AclId"]
            logger.warning("add_slb_whitelistip_info:\n\t{info}".format(info=str(
                {"acl_id": acl_id, "add_entry": add_entry, }
            )))
            request = AddAccessControlListEntryRequest.AddAccessControlListEntryRequest()
            request.set_accept_format('json')
            request.set_AclId(acl_id)
            request.set_AclEntrys(str(add_entry))
            client.do_action_with_exception(request)

    @log(logger=logger, if_exit=True)
    def remove_slb_whitelistip_info(self, ip, ):
        """
        Remove WhitelistIP info into SLB Access Control. See also:
            https://www.alibabacloud.com/help/zh/doc-detail/70055.htm
        :param ip: IP to get info and remove.
        :return: Python built-in exit code.
        """
        client = self.get_cloud_client()
        remove_entry = [{"entry": "{old_ip}/32".format(old_ip=ip), }, ]
        for whitelistip_info in self.get_slb_whitelistip_info(ip):
            acl_id = whitelistip_info["AclId"]
            logger.warning("remove_slb_whitelistip_info:\n\t{info}".format(info=str(
                {"acl_id": acl_id, "remove_entry": remove_entry, }
            )))
            request = RemoveAccessControlListEntryRequest.RemoveAccessControlListEntryRequest()
            request.set_accept_format('json')
            request.set_AclId(acl_id)
            request.set_AclEntrys(str(remove_entry))
            client.do_action_with_exception(request)

    @log(logger=logger, if_exit=True)
    def modify_cdn_whitelistip_info(self, ip, modify_mode, new_ip=None, ):
        """
        Modify WhitelistIP info into CDN Access Control. See also:
            https://www.alibabacloud.com/help/zh/doc-detail/90915.htm
        :param ip: IP to modify(remove).
        :param new_ip: IP to add info.
        :param modify_mode: modify mode(valid values: Append, Delete).
        :return: Python built-in exit code.
        """
        assert modify_mode == "Append" or modify_mode == "Delete"
        client = self.get_cloud_client()
        for whitelistip_info in self.get_cdn_whitelistip_info(ip):
            if modify_mode == "Append" and re.search(self.get_ip_pattern(new_ip),
                                                     whitelistip_info["ip_allow_list_set"]):
                continue
            if modify_mode == "Append":
                modify_info = re.sub(self.get_ip_pattern(ip), "{ip}/32,{new_ip}".format(ip=ip, new_ip=new_ip),
                                     whitelistip_info["ip_allow_list_set"])
            else:
                modify_info = re.sub("{ip}/32,".format(ip=ip), '', whitelistip_info["ip_allow_list_set"])
            modify_entry = [{"functionArgs": [{"argName": "ip_list", "argValue": modify_info}, ],
                             "functionName": "ip_allow_list_set"}]
            domain_name = whitelistip_info["DomainNames"]
            logger.warning("modify_cdn_whitelistip_info:\n\t{info}".format(info=str(
                {"domain_name": domain_name, "modify_entry": modify_entry, }
            )))
            request = BatchSetCdnDomainConfigRequest.BatchSetCdnDomainConfigRequest()
            request.set_accept_format('json')
            request.set_DomainNames(domain_name)
            request.set_Functions(modify_entry)
            client.do_action_with_exception(request)

    @log(logger=logger, if_exit=True)
    def modify_rds_whitelistip_info(self, ip, modify_mode, new_ip=None, ):
        """
        Modify WhitelistIP info into RDS Data Security. See also:
            https://www.alibabacloud.com/help/zh/doc-detail/26242.htm?spm=a2c63.p38356.879954.54.6eb34542JGBoSp
        :param ip: IP address to modify.
        :param new_ip: IP to add info.
        :param modify_mode: modify mode(valid values: Append, Delete, Cover).
        :return: Python built-in exit code.
        """
        assert modify_mode == "Append" or modify_mode == "Delete"
        client = self.get_cloud_client()
        for whitelistip_info in self.get_rds_whitelistip_info(ip):
            if modify_mode == "Append" and re.search(self.get_ip_pattern(new_ip), str(whitelistip_info["CheckInfo"])):
                print(self.get_ip_pattern(ip), str(whitelistip_info["CheckInfo"]))
            del whitelistip_info["CheckInfo"]
            logger.warning("modify_rds_whitelistip_info:\n\t{info}".format(info=str(
                {"db_instance_id": whitelistip_info["DBInstanceId"],
                 "ip_array_name": whitelistip_info["DBInstanceIPArrayName"],
                 "modify_mode": modify_mode, "modify_ip": ip, }
            )))
            request = ModifySecurityIpsRequest.ModifySecurityIpsRequest()
            request.set_accept_format('json')
            if modify_mode == "Append":
                request.set_SecurityIps(new_ip)
            else:
                request.set_SecurityIps(ip)
            request.set_ModifyMode(modify_mode)
            request.set_DBInstanceId(whitelistip_info["DBInstanceId"])
            request.set_DBInstanceIPArrayName(whitelistip_info["DBInstanceIPArrayName"])
            request.set_DBInstanceIPArrayAttribute(whitelistip_info["DBInstanceIPArrayAttribute"])
            request.set_SecurityIPType(whitelistip_info["SecurityIPType"])
            request.set_WhitelistNetworkType(whitelistip_info["WhitelistNetworkType"])
            client.do_action_with_exception(request)
