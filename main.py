import numpy as np
#rom Gaussian import *
from ER01 import *
from Evaluation import *
from showFig import *
from EA01 import *
import random
from makeTest import *
from multiprocessing.dummy import Pool as ThreadPool
import Gaus
from sklearn.cluster import DBSCAN
from sklearn.mixture import GaussianMixture
from getData import *

import time


class Point:
    # self.labelPoint
    centerClusterPoint = -1

    def __init__(self, value):
        self.value = value
        self.centerPoint = 0

        self.edgePoint = 0
        self.Next = []
        self.ClusterPoint = []
        self.GaussianWeight = 0
        self.nearPoint = []

class Cluster:


    numCluster = 0

    def __init__(self):
        self.ClusterList = {}
        self.ClusterMaxWeight = {}
        self.ClusterMaxRecord = {}
        self.ClusterMinPts={}

    def destroyCluster(self, label,pointList):
        if label==-1:return
        #print(self.ClusterList)
        for i in pointList:
            if i.value in self.ClusterList[label]:
                i.ClusterPoint.remove(label)
                i.centerClusterPoint = -1
        del self.ClusterList[label]

    def SearchCenter(self, pointList):
        ListWeight = list(self.ClusterMaxWeight.values())
        ListNum = list(self.ClusterMaxWeight.keys())
        for i in pointList:
            if i.value in ListWeight:
                num1 = ListWeight.index(i.value)
                num2 = ListNum.index(num1)
                i.centerClusterPoint = num2

    def createCluster(self, i):
        self.numCluster += 1
        i.centerClusterPoint = self.numCluster
        self.ClusterList[self.numCluster] = []
        self.ClusterList[self.numCluster].append(i)
        self.ClusterMaxWeight[self.numCluster] = i.GaussianWeight
        self.ClusterMinPts[self.numCluster]=999999
        self.ClusterMaxRecord[self.numCluster]=i.value
        for j in i.nearPoint:
            j.ClusterPoint.append(self.numCluster)
            self.ClusterList[self.numCluster].append(j)
            if j.GaussianWeight<self.ClusterMinPts[self.numCluster]:
                self.ClusterMinPts[self.numCluster]=j.GaussianWeight


FirstCount=500
AddCount=15
dataFirst,dataQueueList=GetData("2013-08-01.csv",FirstCount,AddCount)

X=dataFirst
#y=DBSCAN(eps = 0.334, min_samples = 8).fit_predict(X)
#y= KMeans(n_clusters=10).fit_predict(X)
#y=DBSCAN(eps = 0.05, min_samples = 20).fit_predict(X)
y = GaussianMixture(n_components=10).fit_predict(dataFirst)
y=y.tolist()

initialBegin=time.time()
PointList=[]
for i,j in zip(X,y):
    TempPoint=Point(i)
    TempPoint.ClusterPoint.append(j)
    PointList.append(TempPoint)

def GausCalculate_1(point):
    result=[]
    pointNearNumList=[]
    for i in PointList:
        if i.value==point.value:
            result.append(-1)
        else:
            Gaus2=Gaus.GaussianFunc(i.value,point.value,2.5,2, 0.001, 0.8)
            result.append(Gaus2)


    return result

def GausCalculate_2(GausList):
    sum=0
    for i in GausList:
        if i==-1:continue
        else:
            sum+=i
    return sum
pool = ThreadPool(12)
GausList=list(pool.map(GausCalculate_1,PointList))
WeightList=list(pool.map(GausCalculate_2,GausList))


count=0
for i in PointList:
    i.GaussianWeight=WeightList[count]
    count += 1
    '''
    if len(i.nearPoint)>=Eps:
        i.centerPoint=1
        for k in i.nearPoint:
            k.edgePoint=1
    
    '''
print(1)
cluster=Cluster()
cluster.numCluster=len(y)
clusterMaxWeightNum={}
for i in set(y):
    cluster.ClusterList[i]= []
    cluster.ClusterMaxWeight[i]=-1
    cluster.ClusterMinPts[i]=9999

for y1,point in zip(y,PointList):
    #print(cluster.ClusterList[y1])
    cluster.ClusterList[y1].append(point.value)
    if point.GaussianWeight>cluster.ClusterMaxWeight[y1]:
        cluster.ClusterMaxWeight[y1]=point.GaussianWeight
        cluster.ClusterMaxRecord[y1]=point.value
        clusterMaxWeightNum[y1] = PointList.index(point)

for i in clusterMaxWeightNum:
    PointList[clusterMaxWeightNum[i]].centerClusterPoint=i
    '''
    for k in PointListRe[clusterMaxWeightNum[i]].nearPoint:
        k.edgePoint = 1
    '''
for i in y:
    for j in cluster.ClusterList[i]:
        GausMinPts=abs(Gaus.GaussianFunc(j, cluster.ClusterMaxRecord[i], 2.5, 2, 0.001,0.8))
        if GausMinPts<cluster.ClusterMinPts[i]:
            cluster.ClusterMinPts[i]=GausMinPts

MinMinPts=99
MinEps=99


for i,j in zip(cluster.ClusterMaxWeight,cluster.ClusterMinPts):
    if cluster.ClusterMaxWeight[i]<MinEps:
        MinEps=cluster.ClusterMaxWeight[i]
    if cluster.ClusterMinPts[j]<MinMinPts:
        MinMinPts=cluster.ClusterMinPts[j]

MinPts=MinMinPts
Eps=MinEps

for i in PointList:
    for j in GausList[PointList.index(i)]:
        if j>MinPts:
            i.nearPoint.append(PointList[GausList[PointList.index(i)].index(j)])


initialEnd=time.time()
print(MinPts,',',Eps,',',initialEnd-initialBegin)
pointKmeans=PointList.copy()
pointOurs=PointList.copy()

iterTimes=450
ChooseChangeNum=15
maketest(pointKmeans, pointOurs,iterTimes, cluster,ChooseChangeNum,MinPts,Eps,dataQueueList,initialEnd-initialBegin)

