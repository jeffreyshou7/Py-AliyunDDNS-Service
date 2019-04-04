#!/usr/bin/env python
# -*- coding: UTF-8 -*-
 
import json
import os
import re
import sys
import urllib
from datetime import datetime
import LibWaakii.IpInfo as IpInfo
import LibWaakii.AppLoggerLite as AppLogger
import LibWaakii.AppGlobal as AppGlobal
import LibWaakii.AppConfig as AppConfig
from LibWaakii import WordsCheck
from LibWaakii import AppBase
from LibWaakii import TimerWorker
import json
import LibWaakii.AliYunDns as DDNS

class Worker(object):

    @staticmethod
    def startWork():
        return True
pass

def main():
    # 设置工作路径
    AppGlobal.setAppPath(os.path.split(os.path.realpath(__file__))[0])
    oAppConfig = AppConfig.JsonConf()

    _config = dicAppConfig = oAppConfig.load()
    #print(_config)
    print('ok')
    #print(datetime.now().replace( minute=3, second=0, microsecond=0 ))
    oTimer = TimerWorker.ScheduleTimer(datetime.now(),5,test,'p')
    oTimer.start()
    oDNSWorker = DDNS.DNSWorker(dicAppConfig['domain'],dicAppConfig['access_key_id'],dicAppConfig['access_Key_secret'],'cn-hangzhou')
    # print(oDNSWorker.get_record_all())
    rc = oDNSWorker.update_record('pi','114.94.178.199')
    print(rc)
pass

def test(v):
    print(str(datetime.now()) + str(v))

def main1():
    # a = (2,3)

    # AppBase.appExit()
    AppGlobal.setAppPath(os.path.split(os.path.realpath(__file__))[0])

    oIpAddress = IpInfo.IpAddress()
    print(oIpAddress.getGatewayIp())
    #AppLogger.StandLogger.debugLog('debug-log')
    #AppLogger.StandLogger.infoLog('info-log')
    #AppLogger.StandLogger.warningLog('warning-log')

    data = {
        'interval':'60',
        'last_ip':'',
    }

    oAppConfig = AppConfig.JsonConf()
    #oAppConfig.store(data)
    loadConfig = oAppConfig.load()
    # print(loadConfig)
    #oAppConfig.set({'last_ip':'114.114.114.114'})
    
    oDNSWorker = DDNS.DNSWorker("solab.com.cn",loadConfig['access_key_id'],loadConfig['access_Key_secret'],'cn-hangzhou')
    # print(oDNSWorker.getAliyunDnsRecord())
    # print(oDNSWorker.get_record_id())
    print(oDNSWorker.get_record_value())
    # print(oDNSWorker.get_record_value())

    print(WordsCheck.RegexChecker.judgeLegalIpv4('114.114.112.111'))

if __name__ == '__main__':
    main()