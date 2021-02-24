from queue import Queue, LifoQueue, PriorityQueue
import matplotlib.pyplot as plt
from sklearn.datasets.samples_generator import make_blobs
from EA01 import *
from ER01 import *
import random
from Evaluation import *
plt.rcParams['font.sans-serif']='SimHei' #改字体
import time
from reInitCluster import *
class Point:

    centerClusterPoint = -1

    def __init__(self, value):
        self.value = value
        self.centerPoint = 0

        self.edgePoint = 0
        self.Next = []
        self.ClusterPoint = []
        self.GaussianWeight = 0
        self.nearPoint = []


def maketest(pointKmeans, pointOurs, iterTest, cluster,iterTimes,MinPts,Eps,dataQueueList,initTime):
    count = 0
    X1 = []
    X2_ = []
    X3 = []
    X4=[]
    X5=[]
    X6=[]
    Y = []
    evalOurList = []
    evalKmeansList = []
    Xsilhouette_score = []
    Xcalinski_harabaz_score = []
    Xdavies_bouldin_score = []

    #Our
    OurTime=0
    OurSil=0
    OurCal=0
    OurDav=0
    OurClusterIn=0
    OurClusterOut=0

    #Other
    OtherTime=0
    OtherSil=0
    OtherCal=0
    OtherDav=0
    OtherClusterIn=0
    OtherClusterOut=0


    while count <= iterTest:
        if count>=len(dataQueueList):break
        QueueAdd = Queue(maxsize=0)
        #X2, y = make_blobs(n_samples=iterTimes, n_features=11)
        X2 = dataQueueList[count]
        for i in X2:
            QueueAdd.put(Point(i))
            pointKmeans.append(Point(i))
        time5 = time.time()
        pointOurs = EA(pointOurs, QueueAdd, 0.8, 2, cluster,MinPts,Eps)
        time6 = time.time()
        '''
        randNum = set()
        while len(randNum) < iterTimes:
            randNum.add(random.randint(0, len(pointOurs) - 1))
        QueueOne = Queue(maxsize=0)
        for i in randNum:
            QueueOne.put(pointOurs[i])
            for j in pointKmeans:
                if j.value == pointOurs[i].value:
                    pointKmeans.remove(j)
        '''
        time1 = time.time()
        #pointOurs = ER(pointOurs, QueueOne, 0.005, 2, cluster,Eps)
        time2 = time.time()

        evalKmeansList = evaluationPointKmeans(pointKmeans)
        time3 = time.time()
        labelsTest=[]

        for i in pointOurs:
            if len(i.ClusterPoint) == 0:
                continue
            elif len(i.ClusterPoint) == 1:
                labelsTest.append(i.ClusterPoint[0])
            else:
                for k in i.ClusterPoint:
                    labelsTest.append(k)

        time7=time.time()
        if(len(set(labelsTest))<=7):
            pointOursT,cluster,MinPts,Eps=reBuildCluster(pointOurs,cluster)
            pointOurs=pointOursT
            continue
        time8 = time.time()

        evalOurList = evaluationPointOur(pointOurs)
        X1.append(evalOurList[1] / evalKmeansList[1])
        X2_.append(evalOurList[3] / evalKmeansList[3])
        X3.append(  evalOurList[5]/evalKmeansList[5])
        X5.append(evalOurList[6] / evalKmeansList[6])
        X6.append(  evalOurList[7]/evalKmeansList[7])

        Xsilhouette_score.append(evalOurList[1])
        Xcalinski_harabaz_score.append(evalOurList[3])
        Xdavies_bouldin_score.append(evalOurList[5])

        OurSil+=evalOurList[1]
        OurCal+=evalOurList[3]
        OurDav+=evalOurList[5]
        OurClusterIn+=evalOurList[7]
        OurClusterOut+=evalOurList[6]
        OurTime += (time2 - time1 + time6 - time5 + time8 - time7)

        OtherSil+=evalKmeansList[1]
        OtherCal+=evalKmeansList[3]
        OtherDav+=evalKmeansList[5]
        OtherClusterIn+=evalKmeansList[7]
        OtherClusterOut+=evalKmeansList[6]
        OtherTime+=(time3-time2)

        Y.append(count + 1)
        count += 1
        print(count,"ours:",(time2-time1+time6-time5+ time8 - time7),"kmeans:",(time3-time2),";",len(pointOurs),',',len(pointKmeans),len(cluster.ClusterList))
        X4.append((time2-time1+time6-time5+ time8 - time7)/(time3-time2))

    plt.plot(Y, X1)
    plt.plot(Y, X2_)
    plt.plot(Y, X3)
    plt.plot(Y, X4)
    plt.plot(Y, X5)
    plt.plot(Y, X6)
    plt.legend(["SC",'CH','DBI','T','MD','SSE'])

    OurTime+=initTime
    print('Our轮廓',OurSil/(count-1),'Other轮廓',OtherSil/(count-1))
    print('Our哈拉巴', OurCal/(count-1),'Other哈拉巴',OtherCal/(count-1))
    print('Our戴维', OurDav/(count-1),'Other戴维',OtherDav/(count-1))
    print('Our簇内', OurClusterIn / (count - 1), 'Other簇内', OtherClusterIn / (count - 1))
    print('Our簇外', OurClusterOut / (count - 1), 'Other簇外', OtherClusterOut / (count - 1))
    print('Our时间', OurTime,'Other时间',OtherTime)
    plt.savefig("Gauss05.png",dpi=600)
    plt.show()
