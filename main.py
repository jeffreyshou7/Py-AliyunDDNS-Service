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
import json

def main():
    AppGlobal.setAppPath(os.path.split(os.path.realpath(__file__))[0])

    oIpAddress = IpInfo.IpAddress()
    print(oIpAddress.getGatewayIp())
    AppLogger.StandLogger.debugLog('debug-log')
    AppLogger.StandLogger.infoLog('info-log')
    AppLogger.StandLogger.warningLog('warning-log')

    data = {
        'interval':'60',
        'last_ip':'',
    }

    oAppConfig = AppConfig.JsonConf()
    #oAppConfig.store(data)
    loadData = oAppConfig.load()
    print(loadData)
    #oAppConfig.set({'last_ip':'114.114.114.114'})
    
if __name__ == '__main__':
    main()