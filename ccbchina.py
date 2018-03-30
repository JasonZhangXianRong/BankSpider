"""
This is to get data by cspub
"""
import os
from thePath import rootPath
from superBank import BANK
import imp
import json
import urllib2
import urllib

class CCBCHINA(BANK):
    """
    CCBCHINA
    """
    def __init__(self):
        super(CCBCHINA, self).__init__()
        dataConf = imp.load_source("ccbChinaConf", rootPath + \
                "script/siteproc/bank/conf/ccbChinaConf.py")
        classccbConf = dataConf.GetProvince()
        self.provinceDict = classccbConf.getProvinceId()
        self.fileName = "CCBCHINA.json"
        self.ATM = "CCB_ATM.json"
        self.autoBank = "CCB_autoBank.json"

    def getCityCountyUrl(self, areaCode, searchType):
        try:
            url = ("http://www.ccb.com/tran/WCCMainPlatV5?CCB_IBSVersion=V5"
                     "&SERVLET_NAME=WCCMainPlatV5&isAjaxRequest=true"
                     "&TXCODE=NAREA1&type=" + searchType + "&areacode="
                     + areaCode)
            return url
        except Exception as e:
            print e
            return None

    def getCity(self):
        path = rootPath + "tools/cspub/" + "cityurl.list"
        urlCity = open(path, "w")
        for Prokey, Provalue in self.provinceDict.items():
            provinceName = Provalue
            url = self.getCityCountyUrl(Prokey, "2") + "\n"
            urlCity.write(url.encode("utf8"))
        urlCity.close()

    def tryExec(self, fileName):
        shellScript = "cd " + rootPath + "tools/cspub;" + \
                       "./cs_client -f " + fileName + \
                        " -c conf/user_id_386.conf > 1.txt 2> &1;" + \
                        "cat 1.txt |grep task_id"
        os.system(shellScript)
        
            
            
            
if __name__ == '__main__':
    CCBCHINA().tryExec("cityurl.list")














        
