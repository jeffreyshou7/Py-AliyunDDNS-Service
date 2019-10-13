#-*- coding:utf-8 -*-
 
import requests
#from bs4 import BeautifulSoup
import re
import LibWaakii.AppLoggerLite as AppLogger
import time
import LibWaakii.AppConfig as AppConfig

class IpAddress(object):
    
    #def getIpServiceContent(self, url = r'http://www.ip138.com/'):
    def getIpServiceContent(self, url = 'https://ifconfig.me/ip'):
        try:
            r = requests.get(url)
            return r.text
        except:
            return None

   # 获取外网IP
    def getGatewayIp(self):
        return self.getIpServiceContent()
