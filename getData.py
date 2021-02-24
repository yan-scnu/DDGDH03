import pandas as pd
import  numpy as np
from queue import Queue, LifoQueue, PriorityQueue

def GetData(filename,count,add):
    data= pd.read_csv(filename, encoding='utf-8')
    data = np.array(data).tolist()
    dataFirst=data[:count]
    dataQueueList = []
    # dataQ.append(data[:500])
    Length = len(data)
    #count = 500
    while True:
        dataQueue = []
        if count + add <= Length:
            #for i in range(count,count + 15):
            #    dataQueue.put(data[i])
            dataQueue=data[count:count + add]
            count += add
        else:
            #for i  in range(count,Length-1):
            #    dataQueue.put(data[i])
            dataQueue=data[count:]
            break
        dataQueueList.append(dataQueue)
    return dataFirst,dataQueueList


if __name__ == "__main__":
    main()