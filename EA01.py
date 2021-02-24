from queue import Queue, LifoQueue, PriorityQueue
import Gaus

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

def isSame(i, j):
    if i.value == j.value:
        return True
    else:
        return False


def isRemark(i, Remark):
    if Remark==[]:return False
    for k in Remark:
        if i.value == k.value:
            return True
    return False

def stateChangeEA(i, t ,pointList,Eps):
    TempER = []
    if i.GaussianWeight >= 0.1*Eps:
        if i.centerClusterPoint!=-1:
            return 0
        else:
            return 1  # 建簇
    else:
        return 1


def addPoint(pointList ,A, MinPts):
    sum=0
    for i in pointList:
        tempSum=Gaus.GaussianFunc(i.value, A.value, 2.5, 2, 0.001, 0.8)
        sum+=(tempSum)
        if abs(tempSum)>=MinPts:
            A.nearPoint.append(i)
    A.GaussianWeight=sum
    pointList.append(A)
    return pointList,A

def addToCluster(point,cluster):
    for i in cluster.ClusterMaxRecord.keys():
        Gaus2=Gaus.GaussianFunc(point.value, cluster.ClusterMaxRecord[i], 2.5, 2, 0.001,0.8)
        if Gaus2 >= cluster.ClusterMinPts[i] and point.ClusterPoint != []:
            if i not in point.ClusterPoint and i in cluster.ClusterList:
                cluster.ClusterList[i].append(point)
                point.ClusterPoint.append(i)



def EA(pointList, QueueOne, q,iter, cluster,MinPts,Eps):
    QueueCount = Queue(maxsize=0)
    num = QueueOne.qsize()
    for i in range(0, num):
        QueueCount.put(1)
    Remark = []
    Array = []

    n = 0
    t = 1.1
    while QueueOne.qsize() != 0:
        Array=[]
        Flag = 0
        A = QueueOne.get()
        count = QueueCount.get()

        if n < num:
            # pointList,A = removePoint(pointList, A)
            pointList,A = addPoint(pointList, A,MinPts)

        addToCluster(A,cluster)
        for i in A.nearPoint:
            if count >= iter + 1:
                Flag = 1
                break
            i.GaussianWeight += (Gaus.GaussianFunc(A.value, i.value, 2.5, 2, 0.001, 0.8))
            Array.append(i)

        for i in Array:
            if Flag == 1: break
            if isRemark(i,Remark)==0 :continue
            if stateChangeEA(i, t,Eps) == 1:
                cluster.createCluster(i)
                QueueOne.put(i)
                QueueCount.put(count + 1)
                Remark.append(i)
                Array.remove(i)

        n += 1
    return pointList
