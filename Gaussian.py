from math import exp,pi

def exponentFunc(pointRelate,pointMain,a,n,k,t):
    sum=0
    for i in range(0,n):
        sum+=(-(pointRelate[i]-pointMain[i])**(n-1)/(t*(2*a)**(n-1))-k**((n-1))*t**1)
    #print(sum)
    #print(type(sum))
    return exp(abs(sum)*(-1))

def coefficientFunc(a,n,t):
    #resultTemp=8*np.pi*t*(a**(3*(n-1)/2))*((np.pi*t)**(1/2))
    resultTemp=(2*a*(pi*t)**(1/2))**n
    return 1/resultTemp

def GaussianFunc(pointRelate,pointMain,a,n,k,t):
    return coefficientFunc(a,n,t)*exponentFunc(pointRelate,pointMain,a,n,k,t)
