#-*- coding:utf-8 -*-
import logging
import time
import LibWaakii.AppGlobal as AppGlobal

class StandLogger(object):


    def __init__(self, log_level = logging.DEBUG, log_file = 'app.log'):
        self.oLogger = logging.getLogger('WaakiiDDNS')
        self.oLogger.setLevel(logging.DEBUG)

        self.sFormatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
        # 文件日志
        self.oFileHandler = logging.FileHandler(AppGlobal.getAppPath() + '/' + log_file,encoding ='utf-8')
        self.oFileHandler.setFormatter(self.sFormatter)  # 可以通过setFormatter指定输出格式
        self.oLogger.addHandler(self.oFileHandler)
        
    def __del__(self):
        self.oLogger.removeHandler(self.oFileHandler)

    @classmethod
    def debugLog(cls,log_info):
        oStandLogger = cls()
        oStandLogger.oLogger.debug(log_info)

    @classmethod
    def infoLog(cls,log_info):
        oStandLogger = cls()
        oStandLogger.oLogger.info(log_info)


    @classmethod
    def warningLog(cls,log_info):
        oStandLogger = cls()
        oStandLogger.oLogger.warning(log_info)

    @classmethod
    def errorLog(cls,log_info):
        oStandLogger = cls()
        oStandLogger.oLogger.error(log_info)

    @classmethod
    def criticalLog(cls,log_info):
        oStandLogger = cls()
        oStandLogger.oLogger.critical(log_info)