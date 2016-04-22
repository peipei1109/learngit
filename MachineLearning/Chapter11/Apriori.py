# encoding: utf-8
'''
Created on 2016年4月13日

@author: LuoPei
'''
from test.test_audioop import datas

class Apriori(object):
    def __init__(self, *args, **kwargs):
        pass
    
    def loadDataSet(self):
        return [[1,3,4],[2,3,5],[1,2,3,5],[2,5]]
    
    def createC1(self,dataSet):
        C1=[]
        for transaction in dataSet:
            for item in transaction:
                if not [item] in C1:
                    C1.insert(0, [item])
        C1.sort()
        return map(frozenset, C1)
    
    def scanD(self,D,CK, minSupport):
        ssCnt={}
        for tid in D:
            for can in CK:
                if can.issubset(tid):
                    if not ssCnt.has_key(can):ssCnt[can]=1
                    else: ssCnt[can]+=1
                    
        numItems=float(len(D))
        retList=[]
        supportdata={}
        for key in ssCnt.keys():
            support=ssCnt[key]/numItems
            if support >=minSupport:
                retList.insert(0, key)
            supportdata[key]=support
        return retList,supportdata
    
    def aprioriGen(self,LK,k):
        retList=[]
        lenLK=len(LK)
        for i in range(lenLK):
            for j in range(i+1,lenLK):
                L1=list(LK[i])[:k-2];L2=list(LK[j])[:k-2]
                L1.sort();L2.sort()
                if L1==L2:
                    retList.append(LK[i]|LK[j])
        return retList
    
    def apriori(self,dataSet,minSupport=0.5):
        C1=self.createC1(dataSet);
        D=map(set,dataSet)
        L1,supportData=self.scanD(D, C1, minSupport)
        L=[L1]
        k=2;
        while(len(L[k-2])>0):
            CK=self.aprioriGen(L[k-2], k);
            LK,supK=self.scanD(D, CK, minSupport)
            supportData.update(supK)
            L.append(LK)
            k=k+1
        return L,supportData
            
    def calcConf(self,freqSet,H,supportData,br1,minConf):     
        prunedH=[]
        for conseq in H:
            conf=supportData[freqSet]/supportData[freqSet-conseq]
            
            if conf>=minConf:
                print freqSet-conseq, '-->', conseq, 'conf:',conf
                br1.append((freqSet-conseq,conseq,conf))
                prunedH.append(conseq)
        return prunedH
    
    def rulesFromConseq(self,freqSet, H, supportData, br1,minConf=0.7):
        m=len(H[0])
        print "m:",m
        if(len(freqSet)>m+1):
            Hmp1=self.aprioriGen(H, m+1)
            print Hmp1,freqSet
            
            Hmp1=self.calcConf(freqSet, Hmp1, supportData, br1, minConf)
            print Hmp1
            if(len(Hmp1)>1):
                self.rulesFromConseq(freqSet, Hmp1, supportData, br1, minConf)
        
        
           
    def generateRules(self,L,supportData, minConf=0.7):
        bigRuleList=[]
        for i in range(1,len(L)):
            for freqSet in L[i]:
                H1=[frozenset([item]) for item in freqSet]
                if(i>1):
                    H1=self.calcConf(freqSet, H1, supportData, bigRuleList, minConf)#原书没有这一行，这是原书上面的一个bug
                    self.rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
                else:
                    self.calcConf(freqSet, H1, supportData, bigRuleList, minConf)
                    
                    
        return bigRuleList

if __name__=="__main__":
    ap=Apriori()
    dataSet=ap.loadDataSet()
    L,supportdata=ap.apriori(dataSet)
    print L[:-1]
    rules=ap.generateRules(L,supportdata,0.5)