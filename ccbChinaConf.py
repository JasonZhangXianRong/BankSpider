#-*-coding:utf-8-*-
"""
UTF8
"""
import urllib
import urllib2
import os
import json

class GetProvince(object):
    """
    get province
    """
    def __init__(self):
        """
        This is conf
        """
        self.provinceIdDict = {}
        self.provinceIdDict["340000"] = "安徽省"
        self.provinceIdDict["110000"] = "北京市"
        self.provinceIdDict["500000"] = "重庆市"
        self.provinceIdDict["350000"] = "福建省"
        self.provinceIdDict["620000"] = "甘肃省"
        self.provinceIdDict["440000"] = "广东省"
        self.provinceIdDict["450000"] = "广西省"
        self.provinceIdDict["520000"] = "贵州省"
        self.provinceIdDict["460000"] = "海南省"
        self.provinceIdDict["130000"] = "河北省"
        self.provinceIdDict["410000"] = "河南省"
        self.provinceIdDict["230000"] = "黑龙江"
        self.provinceIdDict["420000"] = "湖北省"
        self.provinceIdDict["430000"] = "湖南省"
        self.provinceIdDict["220000"] = "吉林省"
        self.provinceIdDict["320000"] = "江苏省"
        self.provinceIdDict["360000"] = "江西省"
        self.provinceIdDict["210000"] = "辽宁省"
        self.provinceIdDict["150000"] = "内蒙古"
        self.provinceIdDict["640000"] = "宁夏区"
        self.provinceIdDict["630000"] = "青海省"
        self.provinceIdDict["370000"] = "山东省"
        self.provinceIdDict["610000"] = "陕西省"
        self.provinceIdDict["140000"] = "山西省"
        self.provinceIdDict["310000"] = "上海市"
        self.provinceIdDict["510000"] = "四川省"
        self.provinceIdDict["120000"] = "天津市"
        self.provinceIdDict["650000"] = "新疆区"
        self.provinceIdDict["540000"] = "西藏区"
        self.provinceIdDict["530000"] = "云南省"
        self.provinceIdDict["330000"] = "浙江省"
        
    def getProvinceId(self):
        """
        This function is to get Id
        """
        data = json.dumps(self.provinceIdDict, ensure_ascii = False)
        province = json.loads(data)
        return province









        
