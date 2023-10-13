import json

class RotoConfig:
    def __init__(self):
        self.config=None
        try:
            with open('config.json','r') as jsonfile:
                self.config = json.load(jsonfile)
        except Exception as ex:
            raise ex

    def getConfig(self,key):
        try:
            value = self.config[key]
            return value
        except Exception as ex:
            raise ex
        
    def setConfig(self,key,value):
        try:
            self.config[key]=value
            with open('config.json','w') as jsonfile:
                json.dump(self.config,jsonfile)
        except Exception as ex:
            raise ex
