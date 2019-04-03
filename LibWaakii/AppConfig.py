#-*- coding:utf-8 -*-
import json 
import os
import logging
import LibWaakii.AppGlobal as AppGlobal

class JsonConf:
    '''json配置文件类'''

    def __init__(self,config_file = "config.json"):
        self.config_file = config_file

  
    def store(self,data):
        with open(AppGlobal.getAppPath() + '/' + self.config_file, 'w') as json_file:
            json_file.write(json.dumps(data, indent=4))

    def load(self):
        if not os.path.exists(AppGlobal.getAppPath() + '/' + self.config_file):
            with open(AppGlobal.getAppPath() + '/' + self.config_file, 'w') as json_file:
                pass       
        with open(AppGlobal.getAppPath() + '/' + self.config_file) as json_file:
            try:
                data = json.load(json_file)
            except:
                data = {}
            return data
        
   
    def set(self,data_dict):
        try:
            json_obj = self.load()
            for key in data_dict:
                json_obj[key] = data_dict[key]
            self.store(json_obj)
            return True
        except:
            return False