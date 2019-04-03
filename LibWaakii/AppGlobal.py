#-*- coding:utf-8 -*-
import os

global _APP_PATH_

def getAppPath():
    global _APP_PATH_
    return _APP_PATH_

def setAppPath(app_path):
    global _APP_PATH_
    _APP_PATH_ = app_path