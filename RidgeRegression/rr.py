import tensorflow as tf
import numpy
import matplotlib.pyplot as plt

import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def regression1(coe, lmd):
    # read the data
    f = open('PET.txt', 'r')
    sample_ = []
    line = f.readline()
    line = f.readline().replace("\n", "")
    while len(line) > 50:
        tmpsample = line.split(' ')
        tmpsample_ = [float(i) for i in tmpsample]
        sample_.append(tmpsample_)
        line = f.readline().replace("\n", "")
    sample = numpy.mat(sample_)
    # print(sample)
    x = sample[:, 0:coe]
    x__= numpy.mean(x,axis=0)
    # print(x)
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            # print(str(i) + " "+str(j))
            x[i, j] -= x__[0, j]
    y = sample[:, 268]
    y__=numpy.mean(y)
    for i in range(y.shape[0]):
        y -= y__
    # print(x)

    # define the tensor
    X = tf.placeholder(tf.float32, [coe, x.shape[0]])
    Y = tf.placeholder(tf.float32, [1, x.shape[0]])
    w = tf.Variable(tf.zeros([1, coe]))
    Y_ = tf.matmul(w, X)
    cost = tf.reduce_mean(tf.matmul(Y_ - Y, (Y_-Y),transpose_b=True) + lmd * tf.matmul(w, w,transpose_b=True))  # ridge regression
    train_step = tf.train.GradientDescentOptimizer(0.001).minimize(cost)
    # start training
    sess = tf.Session()
    init = tf.global_variables_initializer()
    sess.run(init)
    for i in range(100000):
        feed = {X:x.T, Y:y.T}
        sess.run(train_step,feed_dict=feed)
        print("cost is " + str(sess.run(cost,feed_dict=feed)))


    # give prediction
    w1 = sess.run(w)
    # print(w1)
    return w1
    # for i in range(20):
    #     w1= sess.run(w)
    #     x1= x[i].T
    #     pre = numpy.matmul(w1,x1)+sess.run(b)
    #     print(pre)
    # return float(pre[0][0])


if __name__ == "__main__":
    lmd = 10
    x = numpy.linspace(1, 268, 268)
    y = regression1(268,lmd)[0]
    plt.plot(x,y)
    plt.title("lambda = "+ str(lmd))
    # y = regression1(3, 'RR')
    # plt.plot(x, y)
    # y = regression1(5, 'RR')
    # plt.plot(x, y)
    # y = regression1(10, 'RR')
    # plt.plot(x, y)
    plt.show()
# for i in range(101,101+rank):
#     y.append(regression1(i,'OLR'))
# plt.plot(x,y)
# plt.show()
