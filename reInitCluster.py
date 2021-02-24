from sklearn.cluster import KMeans
from multiprocessing.dummy import Pool as ThreadPool
from initData import *
from PreTrainModel import *
import  Gaus

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
        for i in pointList:
            if i.value in self.ClusterList[label]:
                i.ClusterPoint.remove(label)
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


def reBuildCluster(pointList,cluster):
    y=ModelTrain(pointList,'Class')
    for i,j in zip(pointList,y):
        i.ClusterPoint.append(j)

    cluster=Cluster()
    cluster.numCluster=len(y)
    clusterMaxWeightNum={}
    for i in set(y):
        cluster.ClusterList[i]= []
        cluster.ClusterMaxWeight[i]=-1
        cluster.ClusterMinPts[i]=9999

    for y1,point in zip(y,pointList):
        cluster.ClusterList[y1].append(point.value)
        if point.GaussianWeight>cluster.ClusterMaxWeight[y1]:
            cluster.ClusterMaxWeight[y1]=point.GaussianWeight
            cluster.ClusterMaxRecord[y1]=point.value
            clusterMaxWeightNum[y1] = pointList.index(point)

    for i in clusterMaxWeightNum:
        pointList[clusterMaxWeightNum[i]].centerClusterPoint=i
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

    return pointList,cluster,MinPts,Eps