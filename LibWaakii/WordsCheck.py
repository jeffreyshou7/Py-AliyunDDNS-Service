# -*- coding: utf-8 -*-

import re

class RegexChecker(object):
   
    @staticmethod
    def judgeLegalIpv4(ip_str):
        '''
        判断一个字符串是否是合法IP地址
        '''
        oRe = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
        try:
            if oRe.match(ip_str):  
                return True  
            else:  
                return False
        except:
            return False