#encoding:utf-8
'''
Created on 2016年4月15日

@author: LuoPei
'''


from numpy import *
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig
from numpy.core.fromnumeric import nonzero


class PCA(object):
    def __init__(self):
        pass
    def loadDataSet(self,fileName,delim='\t'):
        fr=open(fileName)
        stringArr=[line.strip().split(delim) for line in fr.readlines()]
        datArr=[map(float,line) for line in stringArr]
        return mat(datArr)
    def pca(self,dataMat, topNfeat=999999):
        meanVals=mean(dataMat,axis=0)#axis=0列方向。axis=1行方向。
        meanMoved=dataMat-meanVals
        covMat=cov(meanMoved,rowvar=0)
        eigVals,eigVects=linalg.eig(mat(covMat))
        eigValInd =argsort(eigVals)
        eigValInd=eigValInd[:-(topNfeat+1):-1] 
        print eigVects  ,eigValInd 
        redEigVects=eigVects[:,eigValInd]
        print redEigVects
        lowDDataMat =meanMoved*redEigVects
        reconMat=(lowDDataMat*redEigVects.T)+meanVals
        return lowDDataMat,reconMat
    def replaceNanWithMean(self):
        datMat=self.loadDataSet('secom.data', ' ')
        numFeat=shape(datMat)[1]
        for i in range(numFeat):
            meanVal=mean(datMat[nonzero(~isnan(datMat[:,i].A))[0],i])
            datMat[nonzero(isnan(datMat[:,i].A))[0],i]=meanVal
    
    def display(self,dataMat,reconMat):
        fig=plt.figure()
        ax1=fig.add_subplot(111)
        ax1.scatter(dataMat[:,0].flatten().A[0],dataMat[:,1].flatten().A[0],marker='^',s=90)
        ax1.scatter(reconMat[:,0].flatten().A[0],reconMat[:,1].flatten().A[0],marker='o',s=50,c='red')
        plt.show()
        savefig('pca.png')
        


if __name__=="__main__":
    p=PCA()
    dataMat=p.loadDataSet('testSet.txt')
    lowDDataMat,reconMat=p.pca(dataMat,1)
    p.display(dataMat, reconMat)