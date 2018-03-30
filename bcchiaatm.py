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
import re
import geocoding
import threading
import multiprocessing
import datetime

class BCCHINAATM(BANK):
    """
    this class is BC ATM
    """
    def __init__(self):
        super(BCCHINAATM, self).__init__()
        readconf = imp.load_source("bcChina", rootPath + \
                "script/siteproc/bank/conf/bcchina_ATM.py")
        self.cityArr = readconf.city
        self.proArr = readconf.province
        self.fileName = "BCCHINAATM.json"
        self.userAgent = ("Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N)"\
                " AppleWebKit/537.36 (KHTML, like Gecko)"
                " Chrome/60.0.3112.113 Mobile Safari/537.36")
        self.header = {'User-Agent': self.userAgent,}
        
    def getAllUrl(self):
        """
        This is get all url
        """
        AllUrl = []
        urlList = self.getUrlList()
        for urlDetail in urlList:
            pageCount = self.getPageCount(urlDetail)
            for pageNo in range(0, int(pageCount)):
                if pageNo == 0:
                    urlData = urlDetail + "index.html"
                else:
                    urlData = urlDetail + "index_" + str(pageNo) + ".html"
                AllUrl.append(urlData)
        return AllUrl

    def mainSpider(self):
        """
        This is main spider
        """
        fileName = self.getOutFile("BC_ATM.json")
        AllUrl = self.getAllUrl()
        print "The spider is doing crael..."
        process = []
        begin = datetime.datetime.now()
        for fun in AllUrl:
            self.getData1(fun, fileName)
        end = datetime.datetime.now()
        runtime = end - begin
        print "runtime: " + str(runtime) + "\ncrawl success..."
        print fileName
    

    def getData1(self, url, outName):
        """
        This is to get page 
        """
        fp = open(outName, "a")
        htmlCode = self.getHtml(url)
        pageDiv = BeautifulSoup(htmlCode).find("table", {"id": "documentContainer"})
        for tr in pageDiv.findAll("tr"):
            item = {}
            if tr.find("th"):
                continue
            td = tr.findAll("td")
            item["province"] = td[0].get_text()
            item["city"] = td[1].get_text()
            item["addressType"] = td[2].get_text()
            item["atm_Type"] = td[3].get_text()
            item["atm_position"] = td[4].get_text()
            item["work_state"] = td[4].get_text()
            try:
                xys = self.geoPoint(item["atm_position"].encode("utf8"),\
                        item["city"].encode("utf8"))
                item["geo_lng"] = xys[0]
                item["geo_lat"] = xys[1]
            except Exception as e:
                print e
                item["geo_lng"] = ""
                item["geo_lat"] = ""
            li = json.dumps(item, ensure_ascii = False) + "\n"
            fp.write(li.encode("utf8").replace("\\t", "")\
                    .replace("\\n", "").replace("\\r", ""))
        fp.close()

    def geoPoint(self, address, admin, ipflag = 1):
        """
        geo
        """
        geostring =  geocoding.test(address.decode('utf-8').encode('gbk'), 
                admin.decode('utf-8').encode('gbk'),
                address.decode('utf-8').encode('gbk')
                + "@" + 
                admin.decode('utf-8').encode('gbk'),
                ipflag)
        pointList = geostring.split(",")
        return pointList
    
    def getUrlList(self):
        """
        This is to get url list
        """
        itemList = []
        url = "http://www.bankofchina.com/sourcedb/atmdist/"
        page = self.getHtml(url)
        pageDiv = BeautifulSoup(page).find("div", {"id": "apDiv1"}).findAll("div")
        for tableData in pageDiv:
            dataList = tableData.find("table").findAll("tr")[1].find("td").findAll("a")
            for data in dataList:
                detailUrl = url + data.attrs["href"].encode("utf8").replace("./", "")
                itemList.append(detailUrl)
        return itemList
    
    def getPageCount(self, url):
        """
        This is to get page number
        """
        pageCode = self.getHtml(url)
        pageDiv = BeautifulSoup(pageCode).find("div", {"class": "turn_page"})
        pageCount = pageDiv.find("p").get_text().encode("utf8")
        pageNumber =  re.findall(r"-?[1-9]\d*", pageCount)[0]
        return pageNumber

if __name__ == '__main__':
    ATM = BCCHINAATM()
    ATM.mainSpider()
               


















        
