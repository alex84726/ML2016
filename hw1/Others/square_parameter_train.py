import numpy as np
import random
import math

#load data and validation data
data = np.load('training_data.npy')
test_data = np.load('test_data.npy')
test_data_ans = np.load('test_data_answer.npy')

#weight = np.random.rand(1,324)
weight = np.load("2order_weight_rand_ada-2_200000.npy")
#weight = np.zeros((1,324))
#bias = random.uniform(0,0.5)
bias = np.load("2order_bias_rand_ada-2_200000.npy")
#utility function for calcuating

def loss_unit(loss):
    ans = np.square(loss)
    return np.sum(ans)

def diff_Wunit(loss, data):
    xT = np.transpose(data)
    return (-2)*(np.dot(loss,xT))

def diff_Bunit(loss):
    ans = (-2)*loss
    return np.sum(ans)

#learning_rate = 0.000000000000003

#adagrad
rate = 0.01
learn_rate = np.zeros((1,162*2))
learn_rate_b = rate
learn_rate.fill(rate)
#denominator = np.zeros((1,162*2))
#denominator_b = 0.0
denominator = np.load("2order_denominator_rand_ada-2_200000.npy")
denominator_b = np.load("2order_denominator_b_rand_ada-2_200000.npy")
learning_rate = np.zeros((1,162*2))
learning_rate_b = 0.0

iteration = 200000
test_num = 240
lamda = 0
#validation
min_loss = 1000000000
min_weight = weight
min_bias = bias

#arrange input data
inputdata = []
for m in range (12):
    drawer = np.empty((324,0))
    for d in range(471):
        temp = data[m][0:18,d:d+9].reshape(162,1)
        squ_temp = np.square(temp)
        temp = np.append(temp,squ_temp,0)
        drawer = np.append(drawer,temp,1)
    inputdata.append(drawer)

testdata = []
for i in range(test_num):
    temp = test_data[i].reshape(162,1)
    squ_temp = np.square(temp)
    temp = np.append(temp,squ_temp,0)
    testdata.append(temp)

#updating
for i in range(iteration):
    print "iteration  " + str(i)
    loss = 0
    diff_w = 0
    diff_b = 0
    loss_val = 0
    for m in range(12):
        bi = np.zeros((1,471))
        bi.fill(bias)
        lo = data[m][9,9:480].reshape(1,471) - bi - np.dot(weight,inputdata[m])
        loss = loss+loss_unit(lo)
        diff_w = diff_w+diff_Wunit(lo,inputdata[m])
        diff_b = diff_b+diff_Bunit(lo)
    
    for i in range(test_num):
        predict_ans = bias + float(np.dot(weight,testdata[i]))
        loss_val = loss_val+(test_data_ans[i]-predict_ans)**2

    #regularization
    loss =loss+lamda*(np.sum(np.square(weight)))
    diff_w =diff_w + 2*lamda*(weight)

    
    #adagrad
    denominator = np.sqrt(np.square(denominator)+np.square(diff_w))
    learning_rate = np.divide(learn_rate,denominator)
    denominator_b = math.sqrt((denominator_b**2)+(diff_b**2))
    learning_rate = np.divide(learn_rate,denominator)
    learning_rate_b = learn_rate_b / denominator_b
    weight = weight - learning_rate*diff_w
    bias = bias - learning_rate_b*diff_b
    
    #weight = weight - learning_rate*diff_w
    #bias = bias - learning_rate*diff_b

    if loss_val<min_loss :
        print "update~~~~~~~~~~~~~~~~~~~~~~"
        min_weight = weight
        min_bias = bias
        min_loss = loss_val
    print "training loss : " + str(math.sqrt(loss/5652) )
    print "validation loss : " + str(math.sqrt(loss_val/test_num))


np.save("2order_weight_rand_ada-2_200000",min_weight)
np.save("2order_bias_rand_ada-2_200000",min_bias)
np.save("2order_denominator_rand_ada-2_200000",denominator)
np.save("2order_denominator_b_rand_ada-2_200000",denominator_b)
