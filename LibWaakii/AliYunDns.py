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

class DNSWorker(object):
    # 阿里云Access_Key_Id和Access_Key_Secret
    access_key_id = ""
    access_key_secret = ""
    region_id = ""
    # 当前操作域名
    domain_name = ""
    # 填入二级域名的RR值
    rr_keyword = ""
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
        
        self.client = AcsClient(
            self.access_key_id,
            self.access_key_secret,
            self.region_id
        )
        self.record = self.getAliyunDnsRecord()

    def getAliyunDnsRecord(self):
        request = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
        request.set_PageSize(10)
        request.set_PageNumber(1)
        request.set_action_name("DescribeDomainRecords")
        request.set_DomainName(self.domain_name)
        request.set_RRKeyWord(self.rr_keyword)
        request.set_TypeKeyWord(self.record_type)
        r = self.client.do_action_with_exception(request)
        return json.loads(r)

    # 获取阿里云域名解析记录ID
    def get_record_id(self) :
        return self.record["DomainRecords"]["Record"][0]["RecordId"]

    def get_record_id_all(self) :
        return self.record["DomainRecords"]["Record"]

    # 获取当前域名解析记录
    def get_record_value(self) :
        return self.record["DomainRecords"]["Record"][0]["Value"]
    
    def get_record_value_all(self) :
        return self.record["DomainRecords"]["Record"]

        
