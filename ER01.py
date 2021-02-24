from queue import Queue, LifoQueue, PriorityQueue
import Gaus

def stateChangeER(i, t,Eps):
    if i.GaussianWeight >= 0.7*Eps:
        return -1
    else:
        if i.centerClusterPoint!=-1:
            return 1
        else:
            return -1


def isSame(i, j):
    if i.value == j.value:
        return True
    else:
        return False


def isRemark(i, Remark):
    Flag=0
    if Remark==[]:return False
    for k in Remark:
        if i.value == k.value:
            return True

    return False


def removePoint(pointList, A):
    for i in pointList:
        if i.value == A.value:
            pointList.remove(i)
    return pointList,i


def ER(pointList, QueueOne, popo,iter, cluster,Eps):
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
            pointList,A = removePoint(pointList, A)

        for i in A.nearPoint:
            if count >= iter + 1:
                Flag = 1
                break
            i.GaussianWeight -= (Gaus.GaussianFunc(A.value, i.value, 2.5, 2, 0.001,0.8))
            Array.append(i)

        for i in Array:
            if Flag == 1: break
            if isRemark(i,Remark):continue
            if (stateChangeER(i, t,Eps) == 1):
                cluster.destroyCluster(i.centerClusterPoint,pointList)
                i.centerClusterPoint = -1
                QueueOne.put(i)
                QueueCount.put(count + 1)
                Remark.append(i)
                Array.remove(i)

        n += 1
    return pointList