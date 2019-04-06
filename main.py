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
import time
import signal

class Worker(object):

    _cfg = {}
    _region_id = 'cn-hangzhou'
    _last_ip = None
    _retry = 5
    #_DDNS = object
    #_TimerWorker = object 

    @classmethod
    def resetDDNS(cls):
        cls._DDNS = DDNS.DNSWorker(cls._cfg['domain'],cls._cfg['access_key_id'],cls._cfg['access_Key_secret'],cls._region_id)
        
        if cls._DDNS.get_record_all() != None:
            AppLogger.StandLogger.infoLog('与阿里云API服务通信成功！')
            return True
        else:
            AppLogger.StandLogger.infoLog('与阿里云API服务通信失败，请检查AppID/Key或网络连接')
            return False

    @classmethod
    def getRRValue(cls):
        sIp = None

        if cls._DDNS.get_record_all() != None:
            try:
                sIp = cls._DDNS.get_record_value(cls._cfg['rr'])['Value']
            except:
                sIp = None
        return sIp

    @classmethod
    def getGatewayIP(cls):
        oIpAddress = IpInfo.IpAddress()
        sGatewayIp = oIpAddress.getGatewayIp()

        if sGatewayIp != None:
            AppLogger.StandLogger.infoLog('取得外网IP成功,ip地址为(' + sGatewayIp + ')')
            return sGatewayIp
        else:
            AppLogger.StandLogger.warningLog('取得外网IP失败，可能原因（网络未连接）')
            return None

    @classmethod
    def getCfgLastIp(cls):
        try:
            return cls._cfg['last_ip']
        except:
            return None

    @classmethod
    def WorkerInit(cls):
        cls._cfg = AppConfig.JsonConf().load()
        # 服务启动后进行一次域名解析的校验动作
        bRc = cls.resetDDNS()

        if True == bRc:
            sRRIp = cls.getRRValue()
            sGatewayIp = cls.getGatewayIP()
            sCfgIp = cls.getCfgLastIp()

            if None == sGatewayIp:
                AppLogger.StandLogger.warningLog('获取外网IP失败，网络连接有故障，请检查')
                return False

            if sRRIp == sGatewayIp:
                AppLogger.StandLogger.infoLog('(系统初始化)IP地址无变化')
                cls._last_ip = sGatewayIp

                if sGatewayIp != sCfgIp:
                    AppConfig.JsonConf().set({'last_ip':sGatewayIp})
                    AppConfig.JsonConf().set({'last_update':datetime.now().strftime("%Y-%m-%d %H:%M:%S")})                
                return True
            else:
                bUpdated = cls._DDNS.update_record(cls._cfg['rr'],sGatewayIp)

                if True == bUpdated:
                    AppLogger.StandLogger.infoLog('(系统初始化)网关IP已变化，已通过阿里云API成功更新')
                    cls._last_ip = sGatewayIp

                    if sGatewayIp != sCfgIp:
                        AppConfig.JsonConf().set({'last_ip':sGatewayIp})
                        AppConfig.JsonConf().set({'last_update':datetime.now().strftime("%Y-%m-%d %H:%M:%S")})                    
                else:
                    AppLogger.StandLogger.warningLog('(系统初始化)网关IP已变化，但通过阿里云API失败')

                return bUpdated
        else:
            return False

    @classmethod
    def start(cls):
        cls._is_inited = cls.WorkerInit()
        if True == cls._is_inited:
            AppLogger.StandLogger.infoLog('系统初始化工作成功')
        else:
            AppLogger.StandLogger.warningLog('系统初始化工作失败，将会在下一工作周期重试')

        cls._TimerWorker = TimerWorker.ScheduleTimer(datetime.now().replace( minute=3, second=0, microsecond=0),int(cls._cfg['interval']),cls.ScheduleWork)
        cls._TimerWorker.start()

    @classmethod
    def ScheduleWork(cls):
        print(datetime.now())

        while cls._retry > 0 and False == cls._is_inited:
            
            AppLogger.StandLogger.infoLog('系统再次尝试初始化工作')
            cls._is_inited = cls.WorkerInit()
            if False == cls._is_inited:
                cls._retry -= 1
                AppLogger.StandLogger.infoLog('系统将等待({second_}妙,将再重试{times_})再次尝试初始化工作'.format(second_ = 10,times = cls._retry))
                time.sleep(10)
        cls._retry = 5
        pass

        if True == cls._is_inited:
            sGatewayIp = cls.getGatewayIP()
            if sGatewayIp != cls._last_ip:
                bRc = cls.resetDDNS()

                if True == bRc:
                    bUpdated = cls._DDNS.update_record(cls._cfg['rr'],sGatewayIp)

                    if True == bUpdated:
                        AppLogger.StandLogger.infoLog('(系统轮询)网关IP已变化，已通过阿里云API成功更新')

                        cls._last_ip = sGatewayIp
                        AppConfig.JsonConf().set({'last_ip':sGatewayIp})
                        AppConfig.JsonConf().set({'last_update':datetime.now().strftime("%Y-%m-%d %H:%M:%S")})                    
                    else:
                        AppLogger.StandLogger.warningLog('(系统轮询)网关IP已变化，但通过阿里云API成功失败')
                else:
                    AppLogger.StandLogger.warningLog('(系统轮询)与阿里云API服务通信失败，请检查AppID/KeyKey或网络连接！')
            else:
                AppLogger.StandLogger.infoLog('(系统轮询)网关IP无变化！')
        '''     
        dicAliDnsRecord = cls._DDNS.get_record_value(cls._cfg['rr'])
        if dicAliDnsRecord != None:
            if dicAliDnsRecord['Value'] != cls._cfg['last_ip']:
                print(dicAliDnsRecord)
        else
        '''
        #if WordsCheck.RegexChecker.judgeLegalIpv4(cls._cfg['last_ip']) and cls._cfg['last_ip'] != sGatewayIp:
            #AppConfig.JsonConf().set({'last_ip':sGatewayIp})
    
    #@classmethod
    #def scheduleWork(cls):
        
    
pass 

def main():
    # 设置工作路径
    AppGlobal.setAppPath(os.path.split(os.path.realpath(__file__))[0])
    #oAppConfig = AppConfig.JsonConf()

    #_config = dicAppConfig = oAppConfig.load()
    #print(_config)
    #print('ok')
    #print(datetime.now().replace( minute=3, second=0, microsecond=0))
    #oTimer = TimerWorker.ScheduleTimer(datetime.now(),5,test,'p')
    #oTimer.start()

    Worker.start()
    #oDNSWorker = DDNS.DNSWorker(dicAppConfig['domain'],dicAppConfig['access_key_id'],dicAppConfig['access_Key_secret'],'cn-hangzhou')
    
    #AppLogger.StandLogger.debugLog('test')
    # print(oDNSWorker.get_record_all())
    # rc = oDNSWorker.update_record('pi','114.94.178.199')
    # print(rc)
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
    # catch term signal
    signal.signal(signal.SIGTERM, AppBase.term_sig_handler)
    signal.signal(signal.SIGINT, AppBase.term_sig_handler)
    main()