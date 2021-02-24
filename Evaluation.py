import numpy as np
from sklearn.cluster import KMeans
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.mixture import GaussianMixture
import  numpy as np

def EducDistance(X,labels):
    EducDic={}
    EducCenter={}

    Length=len(X[0])
    sumArray=np.zeros(Length)
    sumCenterArray = np.zeros(Length)
    CenterDis=0
    resultEduc=0
    resultEducList=[]
    for i in labels:
        EducDic[i]=[]
    for i,j in zip(X,labels):
        EducDic[j].append(np.array(i))
    for i in EducDic:
        for j in EducDic[i]:
            sumArray+=j
        EducCenter[i]=sumArray/len(EducDic[i])
    for i in EducDic:
        for j in EducDic[i]:
            resultEduc+=np.linalg.norm(j - EducCenter[i])
        resultEducList.append(resultEduc/len(EducDic[i]))
    for i in EducCenter:
        sumCenterArray+=EducCenter[i]
    sumCenterArray=sumCenterArray/len(EducCenter)
    for i in EducDic:
        CenterDis+= np.linalg.norm(j - EducCenter[i])
    return CenterDis,sum(resultEducList)/len(resultEducList)

def evaluationPointOur(pointList):
    X=[]
    labels=[]
    for i in pointList:
        if len(i.ClusterPoint)==0:continue
        elif len(i.ClusterPoint)==1:
            X.append(i.value)
            labels.append(i.ClusterPoint[0])
        else:
            for k in i.ClusterPoint:
                X.append(i.value)
                labels.append(k)
    print(len(set(labels)))
    return evaluationResult(X,labels)+list(EducDistance(X,labels))

def evaluationPointKmeans(pointList):
    X=[]
    y=[]
    for i in pointList:
        X.append(i.value)
    #y = KMeans(n_clusters=10).fit_predict(X)
    y = GaussianMixture(n_components=10).fit_predict(X)
    #y = DBSCAN(eps=0.334, min_samples=8).fit_predict(X)
    return evaluationResult(X, y)+list(EducDistance(X,y))



def evaluationResult(X,labels):
    result=[]
    result.append('轮廓系数')
    result.append(metrics.silhouette_score(X, labels, metric='euclidean'))
    result.append('哈拉巴斯指数')
    result.append(metrics.calinski_harabaz_score(X, labels))
    result.append('戴维森堡丁指数')
    result.append(metrics.davies_bouldin_score(X, labels))
    return result

