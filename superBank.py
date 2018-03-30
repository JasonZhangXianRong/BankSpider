#-*-coding:utf-8-*-
"""
This is base modoul bank
"""
import imp
import json
import urllib2
import urllib
import os
import time
import sys
from thePath import rootPath
class BANK(object):
    """
    Base class
    """
    def __init__(self):
        self.useragent = (
                "Mozilla/5.0 (Linux; Android 6.0;"
                " Nexus 5 Build/MRA58N) AppleWebKit/537.36"
                " (KHTML, like Gecko) "
                "Chrome/60.0.3112.113 Mobile Safari/537.36"
                )
        self.headers={'User-Agent': self.useragent}
        self.time = time.strftime("%Y-%m-%d")
 
    def getHtml(self, url):
        """
        This is to get html code
        """
        try:
            request = urllib2.Request(url, headers = self.headers)
            response = urllib2.urlopen(request, timeout = 60)
            pageCode = response.read()
            return pageCode
        except urllib2.URLError as e:
            if hasattr(e, "reason"):
                return None
                
    def getOutFile(self, fileName):
        """
        The function is to get outfile
        """
        outFile = self.getDirectory() + fileName
        if os.path.exists(outFile):
            os.system("rm " + outFile)
        return outFile
        
    def getDirectory(self):
        """
        The function is to get directory
        """
        backdir = (rootPath + \
                "data/primaryData/BANK/")
        Datedir = backdir + self.time + "/"
        if not os.path.exists(Datedir):
            try:
                os.makedirs(Datedir)
            except OSError as e:
                return Datedir
        return Datedir
            
    def saveFile(self, item, outFile):
        """
        The function is to save file
        """
        fp = open(outFile, 'a+')
        li = json.dumps(item, ensure_ascii=False) + '\n'
        fp.write(li.encode('utf8').replace("\\r", "-").replace("\\n","-")\
                .replace("\\", "-").replace("\\t","-"))
        fp.close()

        
