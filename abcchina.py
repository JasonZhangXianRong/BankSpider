#-*-coding:utf-8-*-
"""
ABC bank spider
"""
from superBank import BANK
import imp
import json
import urllib2
import urllib
import os

class ABCCHINA(BANK):
    """
    This is ABC bank spider
    """
    def __init__(self):
        super(ABCCHINA, self).__init__()
        self.BranchBank = "ABCCHINA.json"
        self.SelfServiceBank = "ABC_autoBank.json"
        self.SelfServiceEquip = "ABC_ATM.json"
        
    def getHtml(self, url):
        """
        This is to get html
        """
        try:
            request = urllib2.Request(url, headers = self.headers)
            response = urllib2.urlopen(request, timeout = 60)
            pageCode = response.read()
            return pageCode
        except Exception as e:
            if hasattr(e, "reason"):
                print "error :页面请求失败，" + e.reason
                return None
                
    def getJsonData(self, pageCode, out_BranchBank,
            out_SelfServiceBank, out_SelfServiceEquip):
        """
        This is get json data
        """
        try:
            jsonHtml = json.loads(pageCode)
            jsonList = jsonHtml["BranchSearchRests"]
            for js1 in jsonList:
                if js1["BranchBank"]:
                    bankData = js1["BranchBank"]
                    self.saveFile(bankData, out_BranchBank)
                if js1["SelfServiceBank"]:
                    bankData = js1["SelfServiceBank"]
                    self.saveFile(bankData, out_SelfServiceBank)
                if js1["SelfServiceEquip"]:
                    bankData = js1["SelfServiceEquip"]
                    self.saveFile(bankData, out_SelfServiceEquip)
        except Exception as e:
            if hasattr(e, "reason"):
                print "error :json数据清洗错误，" + e.reason
                
    def main_spider(self):
        """
        The main function
        """
        out_BranchBank = self.getOutFile(self.BranchBank)
        out_SelfServiceBank = self.getOutFile(self.SelfServiceBank)
        out_SelfServiceEquip = self.getOutFile(self.SelfServiceEquip)
        for pageNumber in range(0, 1877):
            pageCode = self.getHtml("http://app.abchina.com/"
                                    "branch/common/BranchService.svc/"
                                    "Branch?p=-1&c=-1&b=-1&q=&t=0&i=" + str(pageNumber))
            if pageCode:
                self.getJsonData(pageCode, out_BranchBank,
                        out_SelfServiceBank, out_SelfServiceEquip)
            else:
                continue
        

if __name__ == '__main__':
    ABCCHINA().main_spider()




        
