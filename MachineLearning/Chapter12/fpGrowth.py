#-*- encoding: utf-8 -*-
'''
Created on 2016-04-14

@author: Administrator

'''

class TreeNode(object):
    def __init__(self,nameValue,numOccur,parentNode):
        self.name=nameValue
        self.count=numOccur
        self.nodeLink=None
        self.parent=parentNode
        self.children={}
        
    def inc(self,numOccur):
        self.count += numOccur
    
    def display(self,ind=1):
        print ' '*ind,self.name,' ',self.count
        for child in self.children.values():
            child.display(ind+1)
            
    def createFPTree(self,dataSet,minSup=1):
        headerTable={}
        for trans in dataSet.keys():
            for item in trans:
                headerTable[item]=headerTable.get(item,0)+dataSet[trans]
        for key in headerTable.keys():
            if headerTable[key]<minSup:
                del(headerTable[key])
        freqItemSet=set(headerTable.keys())
        if(len(freqItemSet)==0): return None,None
        for k in headerTable.keys():
            headerTable[k]=[headerTable[k],None]
        retTree=TreeNode('Null set',1,None)
        for transSet, count in dataSet.items():
            localD={}
            for item in transSet:
                if item in freqItemSet:
                    localD[item]=headerTable[item][0]
            if (len(localD)>0):
                orderedItems=[v[0] for v in sorted(localD.items(),key=lambda p:p[1],reverse=True)]
#                 ordered=[v for v in sorted(localD.items(),key=lambda p:p[1],reverse=True)]
#                 print ordered
                self.updateTree(orderedItems, retTree, headerTable,count)
        return retTree, headerTable
    
    def updateTree(self,items,inTree, headerTable, count):
        if items[0] in inTree.children:
            inTree.children[items[0]].inc(count)
        else:
            inTree.children[items[0]]=TreeNode(items[0],count,inTree)
            if headerTable[items[0]][1]==None:
                headerTable[items[0]][1]=inTree.children[items[0]]
            else:
                self.updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
        if len(items)>1:
            self.updateTree(items[1::], inTree.children[items[0]], headerTable, count)
            
    def updateHeader(self,nodeToTest, taegetNode):
        while(nodeToTest.nodeLink!=None):
             nodeToTest= nodeToTest.nodeLink 
        nodeToTest.nodeLink= taegetNode          
            
    def loadSimpleDat(self):
       simpDat=[['r','z','h','j','p'],
                ['z','y','x','w','v','u','t','s'],
                ['z'],
                ['r','x','n','o','s'],
                ['y','r','x','z','q','t','p'],
                ['y','z','x','e','q','s','t','m']]  
       return simpDat
   
    def createInitSet(self,dataSet):
        retDict={}
        for trans in dataSet:
           retDict[frozenset(trans)]=1
        return retDict
    
    
    def ascendTree(self,leafNode,prefixPath):
        if leafNode.parent!=None:
            prefixPath.append(leafNode.name)
            self.ascendTree(leafNode.parent, prefixPath)
    def findPredixPath(self,baseSet, treeNode):
        condPats={}
        while treeNode!=None:
            prefixPath=[]
            self.ascendTree(treeNode, prefixPath)
            if(len(prefixPath)>1):
                condPats[frozenset(prefixPath[1:])]=treeNode.count
            treeNode=treeNode.nodeLink
        return condPats 
       
    def minTree(self,inTree,headerTable,minSup,preFix,freqItemList):
        bigL=[v[0] for v in sorted(headerTable.items(),key =lambda p:p[1],reverse=True)]
        
        for basePat in bigL:
            newFreqSet=preFix.copy()
            newFreqSet.add(basePat)
            freqItemList.append(newFreqSet)
            condPattBases=self.findPredixPath(basePat,headerTable[basePat][1])
            myCondTree,myHead=self.createFPTree(condPattBases, minSup)
            print 'conditional tree for :' ,newFreqSet
            if(myCondTree!=None):
                myCondTree.display(1)
            if myHead!=None:
                self.minTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)

if __name__ == '__main__':
    
    fp=TreeNode('null',0,None)
    dataSet=fp.loadSimpleDat()
    print dataSet
    initSet=fp.createInitSet(dataSet)
    print initSet
    myFPtree,myHeaderTab=fp.createFPTree(initSet, 3)
    myFPtree.display()
    condPats=fp.findPredixPath('x', myHeaderTab['x'][1])
    print condPats
    freqItems=[]
    fp.minTree(myFPtree, myHeaderTab, 3, set([]), freqItems)
    print len(freqItems)

