import tensorflow as tf
import numpy
import matplotlib.pyplot as plt

import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def svm1():
    # read the data
    f = open('spambase.txt', 'r')
    sample_ = []
    line = f.readline()
    line = f.readline().replace("\n", "")
    while len(line) > 50:
        tmpsample = line.split(' ')
        sample_.append(tmpsample)
        line = f.readline().replace("\n", "")
    sample = numpy.mat(sample_)
    x = sample[:, 0:57]
    x = x.astype(numpy.float32)
    x__ = numpy.mean(x,axis=0)
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            x[i, j] -= x__[0, j]
    y = sample[:, 58].tolist()
    y = numpy.array([1 if i == ['"spam"'] else -1 for i in y])
    y = numpy.reshape(y,[y.shape[0],1])


    # define the tensor
    X = tf.placeholder(tf.float32, [1, x.shape[1]])
    Y = tf.placeholder(tf.float32, [1,1])

    beta = tf.Variable(tf.zeros([x.shape[1],1]))
    b = tf.Variable([[1.]])
    Y_= tf.matmul(X,beta)+b
    Y_ = tf.reshape(Y_,[1,1])
    alp = 20
    cost = tf.reduce_sum(tf.square(beta)) + alp * tf.reduce_mean(tf.maximum(0., tf.subtract(1., tf.multiply(Y,Y_))))
    train_step = tf.train.GradientDescentOptimizer(0.001).minimize(cost)

    # start training
    sess = tf.Session()
    init = tf.global_variables_initializer()
    sess.run(init)
    for i in range(y.shape[0]):
        feed = {X: x[i], Y: numpy.reshape(y[i],[1,1])}
        sess.run(train_step, feed_dict=feed)
        print("cost is " + str(sess.run(cost, feed_dict=feed)))

    beta_pre = sess.run(beta)
    b_pre = sess.run(b)
    y_pre_ = numpy.matmul(x,beta_pre)+numpy.matmul(numpy.ones([y.shape[0],1]).astype(numpy.float32),b_pre)
    y_pre = numpy.zeros([y_pre_.shape[0],1])
    for i in range(y_pre_.shape[0]):
        if(y_pre_[i]>0):
            y_pre[i][0] = 1
        else:
            y_pre[i][0] = -1
    numpy.reshape(y_pre,[y_pre_.shape[0],1])





    # check precision simple
    pre_t=0
    pre_f=0
    for i in range(x.shape[0]):
        if(y_pre[i,0]==y[i,0]):
            pre_t +=1
        else:
            pre_f +=1

    print("true predict have "+str(pre_t)+"predicts, with false predict " +str(pre_f))



if __name__ == "__main__":
    svm1()
