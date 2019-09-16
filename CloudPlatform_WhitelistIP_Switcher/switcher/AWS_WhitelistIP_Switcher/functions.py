#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-


"""
create_author : Bilery Zoo(652645572@qq.com)
create_time   : 2019-09-04
program       : *_* base functions of AWS handlers module *_*
"""

import re
import json
import typing

import boto3
import botocore

from CloudPlatform_WhitelistIP_Switcher.config.auth import AWS_Access_Key
from CloudPlatform_WhitelistIP_Switcher.lib.log import LOG, log

logger = LOG().logger()


class AWS(object):
    def __init__(self, region, ):
        """
        Init construct.
        :param region: AWS region name.
        """
        self.AWS_Access_Key = AWS_Access_Key
        self.region_name = region

    def __repr__(self):
        repr_str = "AWS client built under:\n\t{'Region': %s}" % self.region_name
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
    def get_service_client(self, service, ):
        """
        Get AWS service client. See also:
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/index.html
        :param service: AWS service name.
        :return: AWS service client object.
        """
        return boto3.client(service, region_name=self.region_name, **self.AWS_Access_Key)

    @log(logger=logger, if_exit=True)
    def get_ec2_whitelistip_info(self, ip, ) -> typing.Generator:
        """
        Get WhitelistIP info of EC2 / VPC Security Group.
        :param ip: IP to get info.
        :return: Dict, {"GroupId": ..., }.
        """
        client = self.get_service_client("ec2")
        response = client.describe_security_groups(
            Filters=[
                {
                    "Name": "ip-permission.cidr",
                    "Values": [
                        "{ip}/32".format(ip=ip),
                    ]
                },
            ],
        )
        for detail in response["SecurityGroups"]:
            for cidr_ip in detail["IpPermissions"][0]["IpRanges"]:
                if re.search(self.get_ip_pattern(ip), cidr_ip["CidrIp"]):
                    detail["IpPermissions"][0]["IpRanges"] = [cidr_ip]
                    break
            whitelistip_info = {"GroupId": detail["GroupId"], "IpPermissions": detail["IpPermissions"], }
            logger.info("get_ec2_ip_info:\n\t{whitelistip_info}".format(whitelistip_info=whitelistip_info))
            yield whitelistip_info

    @log(logger=logger, if_exit=True)
    def get_waf_whitelistip_info(self, ip, ) -> typing.Generator:
        """
        Get WhitelistIP info of WAF IP addresses.
        :param ip: IP to get info.
        :return: Dict, {"IPSetId": ..., }.
        """
        client = self.get_service_client("waf")
        response = client.list_ip_sets()
        for detail in response["IPSets"]:
            ip_sets = client.get_ip_set(IPSetId=detail["IPSetId"])
            if re.search(self.get_ip_pattern(ip), str(ip_sets)):
                for ip_set in ip_sets["IPSet"]["IPSetDescriptors"]:
                    if re.search(self.get_ip_pattern(ip), ip_set["Value"]):
                        whitelistip_info = {"IPSetId": ip_sets["IPSet"]["IPSetId"], "IPSetDescriptor": ip_set}
                        logger.info("get_waf_whitelistip_info:\n\t{whitelistip_info}".format(
                            whitelistip_info=whitelistip_info))
                        whitelistip_info["duplicate_check"] = ip_sets["IPSet"]["IPSetDescriptors"]
                        yield whitelistip_info
                        break

    @log(logger=logger, if_exit=True)
    def get_s3_whitelistip_info(self, ip, ) -> typing.Generator:
        """
        Get WhitelistIP info of S3 Bucket Policy.
        :param ip: IP to get info.
        :return: Dict, {"Bucket": ..., }.
        """
        client = self.get_service_client("s3")
        response = client.list_buckets()
        for detail in response["Buckets"]:
            try:
                bucket_policy = client.get_bucket_policy(Bucket=detail["Name"])["Policy"]
            except botocore.exceptions.ClientError:
                pass
            else:
                if re.search(self.get_ip_pattern(ip), str(bucket_policy)):
                    whitelistip_info = {"Bucket": detail["Name"], "Policy": bucket_policy}
                    logger.info("get_s3_whitelistip_info:\n\t{whitelistip_info}".format(
                        whitelistip_info=whitelistip_info))
                    yield whitelistip_info

    @log(logger=logger, if_exit=True)
    def add_ec2_whitelistip_info(self, ip, new_ip, ):
        """
        Add WhitelistIP info into AWS Security Group. See also:
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.authorize_security_group_ingress
        :param ip: IP to get info.
        :param new_ip: IP to add info.
        :return: Python built-in exit code.
        """
        client = self.get_service_client("ec2", )
        for whitelistip_info in self.get_ec2_whitelistip_info(ip):
            whitelistip_info["IpPermissions"] = eval(
                re.sub(self.get_ip_pattern(ip), new_ip, str(whitelistip_info["IpPermissions"])
                       )
                )
            try:
                client.authorize_security_group_ingress(**whitelistip_info)
            except botocore.exceptions.ClientError:
                continue
            else:
                logger.warning("add_ec2_whitelistip_info:\n\t{info}".format(info=str(whitelistip_info)))

    @log(logger=logger, if_exit=True)
    def remove_ec2_whitelistip_info(self, ip, ):
        """
        Remove WhitelistIP info from AWS Security Group. See also:
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.revoke_security_group_ingress
        :param ip: IP to get info and remove.
        :return: Python built-in exit code.
        """
        client = self.get_service_client("ec2", )
        for whitelistip_info in self.get_ec2_whitelistip_info(ip):
            logger.warning("remove_ec2_whitelistip_info:\n\t{info}".format(info=str(whitelistip_info)))
            client.revoke_security_group_ingress(**whitelistip_info)

    @log(logger=logger, if_exit=True)
    def modify_waf_whitelistip_info(self, ip, modify_mode, new_ip=None, ):
        """
        Modify WhitelistIP info of AWS IP addresses. See also:
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf.html#WAF.Client.update_ip_set
        :param ip: IP to modify(remove).
        :param new_ip: IP to add info.
        :param modify_mode: modify mode(valid values: INSERT, DELETE).
        :return: Python built-in exit code.
        """
        assert modify_mode == "INSERT" or modify_mode == "DELETE"
        client = self.get_service_client("waf", )
        for whitelistip_info in self.get_waf_whitelistip_info(ip):
            if modify_mode == "INSERT" and re.search(self.get_ip_pattern(new_ip),
                                                     str(whitelistip_info["duplicate_check"])):
                continue
            del whitelistip_info["duplicate_check"]
            if modify_mode == "INSERT":
                whitelistip_info["IPSetDescriptor"]["Value"] = re.sub(self.get_ip_pattern(ip), new_ip,
                                                                      whitelistip_info["IPSetDescriptor"]["Value"])
            whitelistip_info["Updates"] = [
                {"Action": modify_mode, "IPSetDescriptor": whitelistip_info["IPSetDescriptor"], }]
            whitelistip_info["ChangeToken"] = client.get_change_token()["ChangeToken"]
            del whitelistip_info["IPSetDescriptor"]
            logger.warning("modify_waf_whitelistip_info:\n\t{info}".format(info=str(whitelistip_info)))
            client.update_ip_set(**whitelistip_info)

    @log(logger=logger, if_exit=True)
    def modify_s3_whitelistip_info(self, ip, modify_mode, new_ip=None, ):
        """
        Modify WhitelistIP info of S3 Bucket Policy. See also:
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_policy
        :param ip: IP to modify(remove).
        :param new_ip: IP to add info.
        :param modify_mode: modify mode(valid values: INSERT, DELETE).
        :return: Python built-in exit code.
        """
        assert modify_mode == "INSERT" or modify_mode == "DELETE"
        client = self.get_service_client("s3", )
        for whitelistip_info in self.get_s3_whitelistip_info(ip):
            if modify_mode == "INSERT" and re.search(self.get_ip_pattern(new_ip), str(whitelistip_info)):
                continue
            policy_info = eval(whitelistip_info["Policy"])
            for policy_statement in policy_info["Statement"]:
                for ip_set in policy_statement["Condition"]["IpAddress"]["aws:SourceIp"]:
                    if re.search(self.get_ip_pattern(ip), ip_set):
                        if modify_mode == "INSERT":
                            policy_statement["Condition"]["IpAddress"]["aws:SourceIp"].append(re.sub(
                                self.get_ip_pattern(ip), new_ip, ip_set))
                        else:
                            policy_statement["Condition"]["IpAddress"]["aws:SourceIp"].remove(ip_set)
            whitelistip_info["Policy"] = json.dumps(policy_info)
            logger.warning("modify_s3_whitelistip_info:\n\t{info}".format(info=str(whitelistip_info)))
            whitelistip_info["ConfirmRemoveSelfBucketAccess"] = False
            client.put_bucket_policy(**whitelistip_info)
