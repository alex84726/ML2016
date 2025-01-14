# coding=utf-8
import numpy as np

#parse training data
dataset = np.loadtxt('./data/train.csv',dtype='string',skiprows=1,delimiter=',')
#delete first three column
dataset = np.delete(dataset,(0,1,2),1)
feature_num = 18
days = 20
#data is modified data
months = 12
data = []

#start classifying
for m in range(months):
    month = np.empty((18,0))
    for d in range(days):
        #parse NR to -1    
        for h in range(24):
            if(dataset[10,h] == 'NR'):
                dataset[10,h] = -1
        month = np.append(month,dataset[0:feature_num,:].astype(np.float),1)
        dataset = np.delete(dataset,np.arange(feature_num),0)
    data.append(month)
#print np.asarray(data).shape
np.save('training_data',np.asarray(data))


