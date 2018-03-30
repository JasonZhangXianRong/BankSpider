#-*-coding:utf-8-*-
"""
This is base bank
"""
import os
from abcchina import ABCCHINA
from  bcchina import BCCHINA
from icbcchina import ICBCCHINA
from mbcchina import MBCCHINA
import threading
import multiprocessing
import sys
from thePath import rootPath
sys.path.append(rootPath + "lib")
from dataFormat import FORMATDATA
from dataCompare import COMPAREDATA
from dataTools import DataTools
import imp
import time
import datetime
class BANK(object):
    """
    This is base bank
    """
    def __init__(self):
        self.time = time.strftime("%Y-%m-%d")
        self.bankInfo = ["ABCCHINA", 
                          "MBCCHINA",
                          "CCB_ATM",]
        self.dateConfPath = rootPath + "data/formatData/BANK/date.txt"
        
    def runSpider(self):
        """
        This is main spider
        """
        print "The spider is doing crael..."
        process = []
        begin = datetime.datetime.now()
        func = [ABCCHINA().main_spider,
                ICBCCHINA().main_spider,
                MBCCHINA().main_spider,
        ]
        for fun in func:
            pro = threading.Thread(target = fun, args=())
            process.append(pro)
        for t in process:
            t.setDaemon(True)
            t.start()
        for t in process:
            t.join()
        end = datetime.datetime.now()
        runtime = end - begin
        print "runtime: " + str(runtime) + "\ncrawl success..."
    
    def format(self):
        """
        This is format data
        """
        print "The spider is doing format..."
        process = []
        outDir = rootPath + "data/formatData/"
        outBrand = "BANK"
        confBrand = "BANK"
        initialDataDate = time.strftime("%Y-%m-%d")
        mains = FORMATDATA()
        for bank in self.bankInfo:
            pro = threading.Thread(target = mains.test,
                  args=(outDir, outBrand, bank, confBrand, initialDataDate, bank, 0))
            process.append(pro)
        for t in process:
            t.setDaemon(True)
            t.start()
        for t in process:
            t.join()
    
    def compare(self, oldFileDate, newFileDate):
        """
        This is compare data
        """
        print "The spider is doing compare..."
        Dir = rootPath + "data/formatData/BANK/"
        lgDir = rootPath + "data/compareData/BANK/"
        mains = COMPAREDATA()
        process = []
        for bank in self.bankInfo:
            oldFile = Dir + oldFileDate + "/" + bank + ".format"
            newFile = Dir + newFileDate + "/" + bank + ".format"
            lgFileName = "lg_" + bank + ".json"
            pro = multiprocessing.Process(target = mains.test, 
                    args = (oldFile, newFile, lgDir, lgFileName))
            process.append(pro)
        for t in process:
            t.start()
        for t in process:
            t.join()

    def dataTool(self, oldFileDate, newFileDate):
        """
        This is data Tool
        """
        print "The spider is doing split..."
        process = []
        outDir = rootPath + "data/compareData/BANK/"
        oldAndNewDir = rootPath + "data/formatData/BANK/"
        mains = DataTools()
        for bank in self.bankInfo:
            oldFile = oldAndNewDir + oldFileDate + "/" + bank + ".format"
            newFile = oldAndNewDir + newFileDate + "/" + bank + ".format"
            lgFile = outDir + "/lg_" + bank + ".json"
            deleteoutName = "delete_" + bank + ".json"
            newoutName = "new_" + bank + ".json"
            pro = multiprocessing.Process(target=mains.test,
                    args=(outDir, oldFile, newFile, lgFile, deleteoutName, newoutName))
            process.append(pro)
        for t in process:
            t.start()
        for t in process:
            t.join()
    
    def mainRun(self):
        """
        This is main spider
        """
        oldFileDate = open(self.dateConfPath, "r")
        if oldFileDate:
            oldDate = oldFileDate.readline().replace("\n", "")\
                      .replace("\r", "").replace("\t", "")
        oldFileDate.close()
        self.format()
        self.compare(oldDate, self.time)
        self.dataTool(oldDate, self.time)
        updateFile = open(self.dateConfPath, "w")
        if updateFile:
            updateFile.write(self.time)
        updateFile.close()
    
    
if __name__ == '__main__':
    BANK().runSpider()

















    
