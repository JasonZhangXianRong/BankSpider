#-*-coding:utf-8-*-
"""
This file code is utf8
"""
from superBank import BANK
import imp
import json
import urllib2
import urllib
from bs4 import BeautifulSoup
import os
import sys
from thePath import rootPath
sys.path.append(rootPath + "tools/geo-client-py")
import geocoding

class BCCHINA(BANK):
    """
    this class is BC
    """
    def __init__(self):
        super(BCCHINA, self).__init__()
        readconf = imp.load_source("bcChina", rootPath + \
                                 "script/siteproc/bank/conf/bcChina.py")
        self.cityId = readconf.cityId
        self.cityArr = readconf.arrCity
        self.proArr = readconf.arrProvince
        self.proId = readconf.arrProviceId
        self.fileName = "BCCHINA.json"
        
    def getHtml(self, url, pageNumber):
        """
        this function is getcode
        Args:
            url,pageNumber
        Return:
            pagecode
        """
        try:
            values_getCounty = {}
            values_getCounty['page'] = pageNumber
            values_getCounty['preSWord'] = ("OPR_SSQ=(408,409,412,413,414,"
                                            "415,416,417,418,419,420,421,422,"
                                            "423,424,425,426,1571,407) and "
                                            "crtime2014.01.01")
            data_getCounty = urllib.urlencode(values_getCounty)
            request = urllib2.Request(url, data_getCounty, headers=self.headers)
            response = urllib2.urlopen(request, timeout = 60)
            pageCode = response.read()
            return pageCode
        except Exception as e:
            if hasattr(e, "reason"):
                print "error :中国银行页面请求失败，", e.reason
                return
                
    def bs4GetDataItems(self, pageCode, outFile):
        """
        This function is to get data
        Args:
            page code and outfile path
        Return:
            data item
        """
        bsObj = BeautifulSoup(pageCode)
        dataItms = {}
        for tr in bsObj.find("div", {"class":"BOC_main publish"}).find("table").findAll("tr"):
            if len(tr.findAll('td')) > 2:
                dataItms["name"] = tr.findAll('td')[0].get_text()
                dataItms["pId"] = tr.findAll('td')[1].attrs["plid"]
                dataItms["layer"] = tr.findAll('td')[2].get_text()
                dataItms["address"] = tr.findAll('td')[3].get_text()
                dataItms["tel"] = tr.findAll('td')[4].get_text()
                dataItms["state"] = tr.findAll('td')[5].get_text()
                list1 = self.getPro(dataItms["pId"].strip())
                if list1:
                    dataItms["province"] = list1
                    citygeo = self.getcity(dataItms["address"].encode("utf8"),\
                            dataItms["province"].encode("utf8"))
                    if citygeo:
                        
                        dataItms["city"] = citygeo   
                    else:
                        dataItms["city"] = 0
                else:
                    dictCity = self.getCity(dataItms["pId"].strip())
                    dataItms["province"] = dictCity["province"]
                    dataItms["city"] = dictCity["city"]
                try:
                    if dataItms["city"] == 0:
                        if dataItms["province"]:
                            admin = dataItms["province"].encode("utf8")
                        else:
                            admin = ""
                    else:
                        admin = dataItms["city"].encode("utf8")
                    address = dataItms["address"].encode("utf8").replace("•", "")\
                              .replace("、", "").replace("（", "").replace("）", "")\
                              .replace("#", "")
                    xys = self.geoPoint(address, admin)
                    dataItms["geo_lng"] = xys[0]
                    dataItms["geo_lat"] = xys[1]
                except Exception as e:
                    dataItms["geo_lng"] = ""
                    dataItms["geo_lat"] = ""
                self.saveFile(dataItms, outFile)
    
    def main_spider(self):
        """
        This is a main spider
        """
        url = ("http://srh.bankofchina.com/search/operation/search.jsp")
        outFile = self.getOutFile(self.fileName)
        for id in range(1,653):
            pageCode = self.getHtml(url, id)
            if pageCode:
                self.bs4GetDataItems(pageCode, outFile)
            else:
                continue

    def geoPoint(self, address, admin, ipflag = 1):
        """
        GEO point
        """
        geostring =  geocoding.test(address.decode('utf-8').encode('gbk'), 
                admin.decode('utf-8').encode('gbk'), 
                address.decode('utf-8').encode('gbk')
                + "@" + 
                admin.decode('utf-8').encode('gbk'),
                ipflag)
        pointList = geostring.split(",")
        return pointList
            
    def getCity(self, cId):
        """
        Get city list from city id
        """
        item = {}
        for i in range(0, len(self.cityArr)):
            for j in range(0, len(self.cityArr[i])):
                if str(cId) == self.cityId[i][j]:
                    item["province"] = self.proArr[i]
                    item["city"] = self.cityArr[i][j]
                    item = json.dumps(item)
                    item = json.loads(item)
                    return item
                    
    def getPro(self, pId):
        """
        Get province from pid
        """
        for i in range(0, len(self.proId)):
            if str(pId) == self.proId[i]:
                pro = json.dumps(self.proArr[i])
                pro = json.loads(pro)
                return pro
    
    def getcity(self, address, admin):
        """
        GEO city
        """
        addr = address.decode("utf8").encode("gbk")
        adm = admin.decode("utf8").encode("gbk")
        line = addr + '@' + adm
        addrInfo = geocoding.testCity(addr, adm,line, 1)
        if "result" in addrInfo:
            str1 = addrInfo["result"][0]["interpolation_admin"].decode("gbk")
            return str1
        
                
if __name__ == '__main__':
    spider = BCCHINA()
    spider.main_spider()
