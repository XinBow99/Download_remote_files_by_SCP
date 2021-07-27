from posix import listdir
import shutil
import os
from typing import Mapping
import alert
# read yaml config
import yaml
# download file
import scpDownloader


class checkPathAndFile:
    def __init__(self):
        alert.console("INIT", "初始化中...", alert.fontColors.OKBLUE)
        self.loadConfig()
        alert.console("hr", "-----------------", alert.fontColors.OKBLUE)
        self.checkPath()
        alert.console("hr", "-----------------", alert.fontColors.OKBLUE)
        self.checkFile()
        alert.console("FILES", "completed all steps!", alert.fontColors.OKGREEN)
        alert.console("hr", "-----------------", alert.fontColors.OKBLUE)

    def loadConfig(self):
        alert.console("Config", "Loading...", alert.fontColors.WARNING)
        with open("config.yaml", "r") as configYaml:
            self.config = yaml.load(configYaml, Loader=yaml.FullLoader)
        alert.console("Config", "Loading complete!", alert.fontColors.OKGREEN)

    def checkPath(self):
        alert.console("check", "CorrectFiles main path", alert.fontColors.OKCYAN)
        if not (os.path.exists(self.config["LoaclCorrectFilesPath"]["Main"])):

            alert.console("PATH", "Create Main Path", alert.fontColors.WARNING)
            os.mkdir(self.config["LoaclCorrectFilesPath"]["Main"])

            alert.console("PATH", "Create Web Path", alert.fontColors.WARNING)
            os.mkdir(self.config["LoaclCorrectFilesPath"]["Main"] +
                     self.config["LoaclCorrectFilesPath"]["Web"])

            alert.console("PATH", "Create Temp Path", alert.fontColors.WARNING)
            os.mkdir(self.config["LoaclCorrectFilesPath"]["Main"] +
                     self.config["LoaclCorrectFilesPath"]["Temp"])
            alert.console("PATH", "Create all path done!",
                          alert.fontColors.OKGREEN)
            return True
        alert.console("check", "CorrectFiles web path", alert.fontColors.OKCYAN)
        if not (os.path.exists(self.config["LoaclCorrectFilesPath"]["Main"]+self.config["LoaclCorrectFilesPath"]["Web"])):
            os.mkdir(
                self.config["LoaclCorrectFilesPath"]["Main"] +
                self.config["LoaclCorrectFilesPath"]["Web"]
            )
            alert.console("PATH", "Create Web Path done!",
                          alert.fontColors.OKGREEN)

        alert.console("check", "CorrectFiles temp path", alert.fontColors.OKCYAN)
        if not (os.path.exists(self.config["LoaclCorrectFilesPath"]["Main"]+self.config["LoaclCorrectFilesPath"]["Web"])):
            os.mkdir(
                self.config["LoaclCorrectFilesPath"]["Main"] +
                self.config["LoaclCorrectFilesPath"]["Temp"]
            )
            alert.console("PATH", "Create Temp path done!",
                          alert.fontColors.OKGREEN)
        alert.console("check", "All path checking done!",
                      alert.fontColors.OKGREEN)

    def checkFile(self):
        alert.console("check", "Correct files", alert.fontColors.OKCYAN)
        alert.console("check", "Keys:{}".format(
            self.config["LoaclCorrectFilesPath"]["FilesKey"]), alert.fontColors.OKCYAN)
        alert.console("check", "Keys in web path check...",
                      alert.fontColors.OKCYAN)

        webPath = self.config["LoaclCorrectFilesPath"]["Main"] + \
            self.config["LoaclCorrectFilesPath"]["Web"]
        tempPath = self.config["LoaclCorrectFilesPath"]["Main"] + \
            self.config["LoaclCorrectFilesPath"]["Temp"]

        alert.console("FILES", "Web files:{}".format(os.listdir(webPath)),
                      alert.fontColors.OKCYAN)
        # 都沒有
        if len(os.listdir(webPath)) == 0 and len(os.listdir(tempPath)) == 0:
            # SCP download
            scpDownloader.getRemoteSSHInfo()
            self.checkFile()
            alert.console("FILES", "Clone file done!", alert.fontColors.OKCYAN)
        alert.console("FILES", "Web and Temp folder done checking", alert.fontColors.OKGREEN)
        # webpath沒有
        if len(os.listdir(webPath)) == 0:
            tempFiles = os.listdir(tempPath)
            for file in tempFiles:
                shutil.move(tempPath + file, webPath)
            self.checkFile()
            alert.console("FILES", "Move file done!", alert.fontColors.OKCYAN)
        # temp沒有 取最新
        if len(os.listdir(tempPath)) == 0:
            tempFiles = os.listdir(tempPath)
            scpDownloader.getRemoteSSHInfo()
            alert.console("FILES", "Get new {} done!".format(self.config["LoaclCorrectFilesPath"]["FileType"]), alert.fontColors.OKCYAN)
        #判斷Web跟Temp是否一樣 如果不一樣TempToWeb
        if sorted(listdir(tempPath)) != sorted(listdir(webPath)):
            for wFile in listdir(webPath):
                os.remove(webPath + wFile)
            alert.console("FILES", "Remove all Web {} file complete!".format(self.config["LoaclCorrectFilesPath"]["FileType"]), alert.fontColors.OKCYAN)
            self.checkFile()
        #清除Temp
        if len(os.listdir(tempPath)) > 0:
            for tFile in listdir(tempPath):
                os.remove(tempPath + tFile)
            alert.console("FILES", "Remove temp {} done!".format(self.config["LoaclCorrectFilesPath"]["FileType"]), alert.fontColors.OKCYAN)
    def getWebFiles(self):
        alert.console("Web{}".format(self.config["LoaclCorrectFilesPath"]["FileType"]), "Get web files...", alert.fontColors.OKCYAN)
        webPath = self.config["LoaclCorrectFilesPath"]["Main"] + \
            self.config["LoaclCorrectFilesPath"]["Web"]
        returnFiles = {
            'good':'',
            'bad':'',
            'total':'',
            'date':''
        }
        if len(os.listdir(webPath)) > 0:
            for wFile in listdir(webPath):
                returnFiles[wFile.split('_')[0]] = wFile
        returnFiles['date'] = returnFiles['total'].replace('.{}'.format(self.config["LoaclCorrectFilesPath"]["FileType"]),"").split('_')[1:]
        alert.console("FILES", "Get Files!", alert.fontColors.OKGREEN)
        alert.console("RETURN", returnFiles,alert.fontColors.HEADER)
        return returnFiles

if __name__ == "__main__":
    main = checkPathAndFile()
    main.getWebFiles()
