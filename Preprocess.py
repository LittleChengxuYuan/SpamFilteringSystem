import jieba
import os
import pickle
from bayes.Bayes import Bayes

from MySVM.MySVM import MySVM

class Preprocess:
    __stopList = []
    __hamDict = {}
    __spamDict = {}
    __spamFileNum = 0
    __hamFileNum = 0
    __spamFilePath = ''
    __hamFilePath = ''

    def __init__(self, hamFilePath, spamFilePath, stopWordsFilePath):
        __stopList = open(stopWordsFilePath, encoding="utf8").read().split()
        # self.__hamDict = self.__getWordDict(hamFilePath, __stopList)
        # self.__spamDict = self.__getWordDict(spamFilePath, __stopList)
        # self.__hamFileNum = len(os.listdir(hamFilePath))
        # self.__spamFileNum = len(os.listdir(spamFilePath))
        # self.__spamFilePath = spamFilePath
        # self.__hamFilePath = hamFilePath
        # Dict = [self.__hamDict,self.__spamDict,self.__hamFileNum,self.__spamFileNum,self.__spamFilePath,hamFilePath]
        # f = open("./File/Dict_data.bin","wb")
        # pickle.dump(Dict,f,True)
        # f.close()
        Dict = pickle.load(open("./File/Dict_data.bin","rb"))
        self.__hamDict = Dict[0]
        self.__spamDict = Dict[1]
        self.__hamFileNum = Dict[2]
        self.__spamFileNum = Dict[3]
        self.__spamFilePath = Dict[4]
        self.__hamFilePath = Dict[5]
    # 针对单一文件的单一算法
    def getResult_1(self, algs, file):
        global result
        fileDict = self.__getTestDict(file, self.__stopList)
        if algs == "bayes":
            bayes = Bayes()
            result = bayes.getResult(fileDict, self.__spamDict, self.__hamDict, self.__spamFileNum, self.__hamFileNum)

        elif algs == "SVM":
            mySVM = MySVM()
            # result = mySVM.train2file(self.__spamDict, self.__hamDict, self.__spamFilePath, self.__hamFilePath)
            result = mySVM.myPredict(fileDict)

        elif algs == "KNN":
            pass
        return result

    # 将传入的字符串分割为单词并保存在列表里，使用结巴分词
    # 计算wordList中单词出现的频数，并将其保存在字典中，该方法对各形式的邮件通用
    def __getWordDict(self, filePath, stopList):
        wordDict = {}
        fileList = os.listdir(filePath)
        for fileName in fileList:
            file_object = open(filePath + '/' + fileName, encoding="utf8").read()
            res_list = jieba.lcut(file_object)
            for i in res_list:
                if i not in stopList and i.strip() != '' and i != None:
                    if i in wordDict.keys():
                        wordDict[i] += 1
                    else:
                        wordDict.setdefault(i, 1)
        return wordDict

    def __getTestDict(self, file, stopList):
        wordDict = {}
        res_list = open(file,encoding="utf8").read().split()
        for i in res_list:
            if i not in stopList and i.strip() != '' and i != None:
                if i in wordDict.keys():
                    wordDict[i] += 1
                else:
                    wordDict.setdefault(i, 1)
        return wordDict
