# -*- encoding: utf-8 -*-
'''
Created on 2016年4月15日

@author: LuoPei
'''
from numpy import *

class SVD(object):
    def __init__(self, *args, **kwargs):
        object.__init__(self, *args, **kwargs)
        
    def loadExData(self):
        return [[1,1,1,2,0],
                [2,2,2,0,0],
                [1,1,1,0,0],
                [5,5,5,0,0],
                [4,4,0,2,2],
                [4,0,0,3,3],
                [4,0,0,1,1]]
    
    
    
    #相似度计算的三种方法   
    def eculdSim(self,inA,inB):
        return 1.0/(1.0+linalg.norm(inA-inB))
    
    def pearsSim(self,inA,inB):
        if(len(inA)<3):return 1.0
        return 0.5+0.5*corrcoef(inA, inB, rowvar=0)[0][1]
    
    def cosSim(self,inA,inB):
        num=float(inA.T*inB)
        denom=linalg.norm(inA)*linalg.norm(inB)
        return 0.5+0.5*(num/denom)
    
    #基于物品相似度的推荐引擎
    def standEst(self,dataMat,user,simMeas,item):
        n=shape(dataMat)[1]
        simTotal=0.0;ratSimTotal=0.0
        for j in range(n):
            userRating =dataMat[user,j]
            if userRating==0: continue
            overLap=nonzero(logical_and(dataMat[:,item].A>0,dataMat[:,j].A>0))[0]
            if len(overLap)==0:similarity=0
            else: similarity=simMeas(dataMat[overLap,item],dataMat[overLap,j])
            
            print 'the %d and %d similarity is :%f' %(item,j,similarity)
            simTotal +=similarity
            ratSimTotal +=similarity*userRating
        if simTotal==0: return 0
        else: return ratSimTotal/simTotal
        
        
    #基于SVD的评分估计
    def svdEst(self,dataMat,user,simMeas,item):
        n=shape(dataMat)[1]
        simTotal=0.0;ratSimTotal=0.0
        U,Singma,VT=linalg.svd(dataMat)
        Sig4=mat(eye(4)*Singma[:4])
        xformedItems=dataMat.T*U[:,:4]*Sig4.I
        print "xformedItems",xformedItems
        for j in range(n):
            userRating =dataMat[user,j]
            if userRating==0 or j==item: continue
            similarity=simMeas(xformedItems[item,:].T,xformedItems[j,:].T)
            
            print 'the %d and %d similarity is :%f' %(item,j,similarity)
            simTotal +=similarity
            ratSimTotal +=similarity*userRating
        if simTotal==0: return 0
        else: return ratSimTotal/simTotal   
        
        
        
    def recommand(self,dataMat,user,N=3,simMeas=cosSim,estMethod=standEst):
        unratedItems =nonzero(dataMat[user,:].A==0)[1]
        if len(unratedItems)==0: return 'you rated everything'
        itemScores=[]
        for item in unratedItems:
            estimatedScore=estMethod(dataMat,user,simMeas,item)
            itemScores.append((item,estimatedScore))
        return sorted(itemScores,key=lambda jj:jj[1],reverse=True)[:N]
    
    #基于SVD的图像压缩
    def printMat(self,inMat,thresh=0.8):
        for i in range(32):
            for k in range(32):
                if float(inMat[i,k])>thresh:
                    print 1
                else: print 0
            print ' '
            
    def imgCompress(self,numSV=3,thresh=0.8):
        myl=[]
        for line in open('0_5.txt').readlines():
            newRow=[]
            for i in range(32):
                newRow.append(int(line[i]))
            myl.append(newRow)
        myMat=mat(myl)
        print "***original matrix******"
        self.printMat(myMat,thresh)
        U,Sigma,VT=linalg.svd(myMat)
        SigRecon=mat(zeros((numSV,numSV)))
        for k in range(numSV):
            SigRecon[k,k]=Sigma[k]
        reconMat=U[:,:numSV]*SigRecon*VT[:numSV,:]
        print "***** reconstructed matrix using %d Singular values*********"
        self.printMat(reconMat, thresh)
        
if __name__=="__main__":
   s=SVD()
   Data=s.loadExData()
   U,Singma,VT=linalg.svd(mat(Data))
   myDat=mat(Data)
   sData=s.pearsSim(myDat[:,0], myDat[:,4])
   print sData
   Sig3=mat([[Singma[0],0,0],[0,Singma[1],0],[0,0,Singma[2]]])
   U=U[:,:3]*Sig3*VT[:3,:]
   print  U
   ss=s.recommand(myDat, 6,simMeas=s.pearsSim,estMethod=s.standEst)
   print ss