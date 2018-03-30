#-*-coding:utf-8-*-
"""
This is ICBC CHINA 
"""
from superBank import BANK
import imp
import json
import urllib2
import urllib
import os
from thePath import rootPath
class ICBCCHINA(BANK):
    """
    ICBC spider
    """
    def __init__(self):
        super(ICBCCHINA, self).__init__()
        dataConf = imp.load_source("ccbChinaConf", rootPath + \
                                  "script/siteproc/bank/conf/ccbChinaConf.py")
        classccbConf = dataConf.GetProvince()
        self.provinceDict = classccbConf.getProvinceId()
        self.fileName = "CCBCHINA.json"
        self.ATM = "CCB_ATM.json"
        self.autoBank = "CCB_autoBank.json"
        
    def getCityCountyList(self, areaCode, searchType):
        """
        This function is to get city list
        """
        try:
            url = ("http://www.ccb.com/tran/WCCMainPlatV5?CCB_IBSVersion=V5"
                   "&SERVLET_NAME=WCCMainPlatV5&isAjaxRequest=true"
                   "&TXCODE=NAREA1&type=" + searchType + "&areacode="
                   + areaCode)
            request = urllib2.Request(url, headers = self.headers)
            response = urllib2.urlopen(request, timeout = 60)
            pageCode = response.read()
            code = pageCode.replace("\\", "-")
            jsonHtml = json.loads(code, strict = False)
            return jsonHtml
        except Exception as e:
            if hasattr(e, "reason"):
                print "error :页面请求失败，", e.reason
                return 
                
    def getCityId(self, cityHtml):
        """
        This function is to get city id
        """
        items = []
        for city in cityHtml["arealist"]:
            item = {}
            if city:
                item["cityId"] = city["areacode"]
                item["cityName"] = city["NET_NAME"]
                items.append(item)
        return items
        
    def getCountyId(self, CountyHtml):
        """
        This function is to get county id
        """
        items = []
        for county in CountyHtml["arealist"]:
            item = {}
            if county:
                item["CountyId"] = county["areacode"]
                item["CountyName"] = county["NET_NAME"]
                items.append(item)
        return items
        
    def getPageCount(self, countyId):
        """
        This function is to get page county
        """
        try:
            url = ("http://www.ccb.com/tran/WCCMainPlatV5?"
                   "CCB_IBSVersion=V5&SERVLET_NAME=WCCMainPlatV5"
                   "&isAjaxRequest=true&TXCODE=NZX001&AREA_NAME"
                   "=" + str(countyId) +
                   "&NET_KEYWORD=&NET_FLAG=4&CURRENT_PAGE=1")
            request = urllib2.Request(url, headers = self.headers)
            try:
                response = urllib2.urlopen(request, timeout = 60)
            except Exception as e:
                return 
            else:
                pageCode = response.read()
                code = pageCode.replace("\\", "-")
                code = code.replace("\r", "")
                code = code.replace("\t", "")
                code = code.replace("\n", "")
                code = code.replace("\"佳源中心广场\"", "(佳源中心广场)")
                code = code.replace("\"棕榈泉国际花园\"", "(棕榈泉国际花园)")
                code = code.replace("\"书香大第\"", "(书香大第)")
                code = code.replace("\"NET_NAME\":\"\"泉州市", "\"NET_NAME\":\"泉州市")
                code = code.replace("\"NET_AREA\":\"\"泉州市", "\"NET_AREA\":\"泉州市")
                code = code.replace("\"\"柘荣县", "\"柘荣县")
                code = code.replace("\"金湖帝景\"", "(金湖帝景)")
                code = code.replace("\"NET_NAME\":\"\"410", "\"NET_NAME\":\"410")
                code = code.replace("\"NET_AREA\":\"\"410", "\"NET_AREA\":\"410")
                html = json.loads(code, strict = False)
                return html["TOTAL_PAGE"]
        except Exception as e:
            if hasattr(e, "code"):
                print e.code
                return 
            if hasattr(e, "reason"):
                print e.reason
                return 
                
    def getData(self, countyId, pageNumber):
        """
        This is to wash data
        """
        try:
            url = ("http://www.ccb.com/tran/WCCMainPlatV5?"
                    "CCB_IBSVersion=V5&SERVLET_NAME=WCCMainPlatV5"
                    "&isAjaxRequest=true&TXCODE=NZX001&AREA_NAME"
                    "=" + str(countyId) +
                    "&NET_KEYWORD=&NET_FLAG=4&CURRENT_PAGE=" + str(pageNumber))
            request = urllib2.Request(url, headers = self.headers)
            try:
                response = urllib2.urlopen(request, timeout = 60)
            except Exception as e:
                return
            else:
                pageCode = response.read()
                code = pageCode.replace("\\", "-")
                code = code.replace("\r", "")
                code = code.replace("\n", "")
                code = code.replace("\t", "")
                code = code.replace("\"佳源中心广场\"", "(佳源中心广场)")
                code = code.replace("\"棕榈泉国际花园\"", "(棕榈泉国际花园)")
                code = code.replace("\"书香大第\"", "(书香大第)")
                code = code.replace("\"NET_NAME\":\"\"泉州市", "\"NET_NAME\":\"泉州市")
                code = code.replace("\"NET_AREA\":\"\"泉州市", "\"NET_AREA\":\"泉州市")
                code = code.replace("\"\"柘荣县", "\"柘荣县")
                code = code.replace("\"金湖帝景\"", "(金湖帝景)")
                code = code.replace("\"NET_NAME\":\"\"410", "\"NET_NAME\":\"410")
                code = code.replace("\"NET_AREA\":\"\"410", "\"NET_AREA\":\"410")
                html = json.loads(code, strict = False)
                return html
        except Exception as e:
            if hasattr(e, "code"):
                print e.code
                return 
            if hasattr(e, "reason"):
                print e.reason
                return
        
    def main_spider(self):
        """
        This is main spider
        """
        #从省得到市
        bankFile = self.getOutFile(self.fileName)
        ATM = self.getOutFile(self.ATM)
        autoBank = self.getOutFile(self.autoBank)
        for Prokey, Provalue in self.provinceDict.items():
            provinceName = Provalue
            jsonCityObj = self.getCityCountyList(Prokey, "2")
            if jsonCityObj:
                cityDictList = self.getCityId(jsonCityObj)
                for cityDict in cityDictList:
                    cityName = cityDict["cityName"]
                    cityId = cityDict["cityId"].encode("utf8")
                    jsonCountyObj = self.getCityCountyList(cityId, "3")
                    if jsonCountyObj:
                        CountyDictList = self.getCountyId(jsonCountyObj)
                        for countyDict in CountyDictList:
                            countyId = countyDict["CountyId"]
                            countyName = countyDict["CountyName"]
                            pageCount1 = self.getPageCount(countyId)
                            if not pageCount1:
                                continue
                            else:
                                pageNumber = int(pageCount1)
                                for pageNo in range(1, pageNumber + 1):
                                    bankInfo = self.getData(countyId, pageNo)
                                    if bankInfo:
                                        for bank in bankInfo["ARRAY_CMG001"]:
                                            if bank:
                                                bank["Province"] = provinceName
                                                bank["cityName"] = cityName
                                                bank["countyName"] = countyName
                                                bank = json.dumps(bank)
                                                bank = json.loads(bank)
                                                if bank["NET_FLAG"].encode("utf8") == "1":
                                                    self.saveFile(bank, bankFile)
                                                elif bank["NET_FLAG"].encode("utf8") == "2":
                                                    self.saveFile(bank, autoBank)
                                                else:
                                                    self.saveFile(bank, ATM)

    
if __name__ == '__main__':
    ICBCCHINA().main_spider()

                
    

        
