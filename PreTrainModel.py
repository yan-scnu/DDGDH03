import numpy as np
from sklearn.cluster import KMeans
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.mixture import GaussianMixture



def ModelTrain(X,type):
    y=[]
    if type=='List':
        y = GaussianMixture(n_components=12).fit_predict(X)
    elif type=='Class':
        X2=[]
        print("Clear Cluster")
        for i in X:
            X2.append(i.value)
            i.ClusterPoint = []
        y = GaussianMixture(n_components=12).fit_predict(X2)
    return y