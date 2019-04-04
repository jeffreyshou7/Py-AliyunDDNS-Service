#-*- coding:utf-8 -*-
import os

global _APP_PATH_

def getAppPath():
    global _APP_PATH_
    return _APP_PATH_

def setAppPath(app_path):
    global _APP_PATH_
    _APP_PATH_ = app_path

def getDefaultConfig():
    return  {
                "interval": "60",
                "last_ip": "",
                "last_update":"",
                "record_id":"",
                "domain":"",
                "rr":"",
                "switch":0,
                "access_key_id":"",
                "access_Key_secret":"",
                "region_id":"",
                "access_token":""
            }