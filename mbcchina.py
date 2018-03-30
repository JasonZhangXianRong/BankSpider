#-*-coding:utf-8-*-
"""
utf8
"""
from superBank import BANK
import imp
import json
import urllib2
import urllib
import os

class MBCCHINA(BANK):
    """
    MBC bank
    """
    def __init__(self):
        """
        super class is bank
        """
        super(MBCCHINA, self).__init__()
        self.fileName = "MBCCHINA.json"
        self.ATM = "MBC_ATM.json"
        self.autoBank = "MBC_autoBank.json"
        
    def getCityList(self, url, bankFile, ATM, autoBank):
        """
        get city list
        """
        try:
            request = urllib2.Request(url, headers = self.headers)
            response = urllib2.urlopen(request, timeout = 60)
            pageCode = response.read()
            str1 = pageCode.split("cityxml")
            str2 = str1[1][8:len(str1) - 165]
            PCJsonList = json.loads(str2)
            for PCJson in PCJsonList["provinces"]:
                provinceName = PCJson["provname"]
                for cityJsonInfo in PCJson["cities"]:
                    cityName = cityJsonInfo["cityname"]
                    uniStr = cityName.encode("unicode_escape")
                    urlCode = uniStr.replace("\\", "%")
                    for type in ["A", "B", "C"]:
                        DataCode = self.getData(urlCode, type)
                        strData = str(DataCode.strip().strip("\n").strip("\r"))
                        josnObj = json.loads(strData, strict = False)
                        for fDataJson in josnObj["branches"]:
                            fDataJson["Pro"] = provinceName
                            fDataJson["City"] = cityName
                            if fDataJson["type"].encode("utf8") == "B":
                                self.saveFile(fDataJson, bankFile)
                            elif fDataJson["type"].encode("utf8") == "A":
                                self.saveFile(fDataJson, ATM)
                            else:
                                self.saveFile(fDataJson, autoBank)
        except Exception as e:
            if hasattr(e, "reason"):
                print "error :页面请求失败，", e.reason
                return 
        
    def getData(self, cityName, type):
        """
        Gte json data
        """
        try:
            url = ("http://map.cmbchina.com/Service/branch.aspx?city=" +
                    cityName + "&type=" + type + "&_=1505887706093&{}")
            request = urllib2.Request(url, headers = self.headers)
            response = urllib2.urlopen(request, timeout = 60)
            pageCode = response.read()
            return pageCode
        except Exception as e:
            if hasattr(e, "reason"):
                print "error :页面请求失败，", e.reason
                return
    
    def main_spider(self):
        """
        This is main spider
        """
        bankFile = self.getOutFile(self.fileName)
        ATM = self.getOutFile(self.ATM)
        autoBank = self.getOutFile(self.autoBank)
        cityJsonList = self.getCityList("http://map.cmbchina.com/", bankFile, ATM, autoBank)
         
            
if __name__ == '__main__':
    spider = MBCCHINA()
    spider.main_spider()
