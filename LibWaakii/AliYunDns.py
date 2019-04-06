# -*- coding: utf-8 -*-

import os
import json
from urllib import request
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109 import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109 import UpdateDomainRecordRequest
import LibWaakii.IpInfo as IpInfo
from LibWaakii import WordsCheck

class DNSWorker(object):
    # 阿里云Access_Key_Id和Access_Key_Secret
    access_key_id = ""
    access_key_secret = ""
    region_id = ""
    # 当前操作域名
    domain_name = ""

    # 解析记录类型，一般为A记录
    record_type = "A"
    # 配置文件路径文件名
    config_file = ""

    client = None
    record = None
    current_ip  = ''

    # 初始化，获取client实例
    def __init__(self,domain_name,access_key_id,access_key_secret,region_id = 'region_id'):
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.region_id = region_id
        self.domain_name = domain_name
        
        try:
            self.client = AcsClient(
                self.access_key_id,
                self.access_key_secret,
                self.region_id
            )
            self.record = self.getAliyunDnsRecord()
        except Exception as e:
            print(e)
            self.record = None

    def getAliyunDnsRecord(self):
        try:
            request = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
            request.set_PageSize(99)
            request.set_PageNumber(1)
            request.set_action_name("DescribeDomainRecords")
            request.set_DomainName(self.domain_name)
            # request.set_RRKeyWord(self.rr_keyword)
            request.set_TypeKeyWord(self.record_type)
            r = self.client.do_action_with_exception(request)
            return json.loads(r)
        except Exception as e:
            print(e)
            return None

    # 获取阿里云域名解析记录ID
    def get_record_all(self) :
        if self.record != None:
            return self.record["DomainRecords"]["Record"]
        else:
            return None

    # 获取域名解析记录详细信息
    def get_record_value(self,RR = '@') :
        try:
            for dicRecord in self.record["DomainRecords"]["Record"]:
                if RR == dicRecord['RR']:
                    return dicRecord
            return {}
        except:
            return None

    # 获取域名解析记录recordid
    def get_record_id(self,RR = '@') :

        try:
            return self.get_record_value(RR)['RecordId']
        except:
            return None
    
    # 修改阿里云解析记录
    def update_record(self, RR ,value):
        request = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
        request.set_action_name("UpdateDomainRecord")
        request.set_accept_format('json')
        request.set_TTL('600')
        sRecordid = self.get_record_id(RR)

        if sRecordid != None and WordsCheck.RegexChecker.judgeLegalIpv4(value):
            request.set_RecordId(sRecordid)
            request.set_Type(self.record_type)
            request.set_RR(RR)
            request.set_Value(value)
        else:
            return False
        pass
        try:
            # jsonReturn = json.load(self.client.do_action_with_exception(request))
            # rc = self.client.do_action_with_exception(request)
            if None != json.loads(self.client.do_action_with_exception(request)):
                return True
        except:
            return False
        
