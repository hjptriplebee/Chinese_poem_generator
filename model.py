# coding: UTF-8
'''''''''''''''''''''''''''''''''''''''''''''''''''''
   file name: model.py
   create time: 2017年06月25日 星期日 10时47分48秒
   author: Jipeng Huang
   e-mail: huangjipengnju@gmail.com
   github: https://github.com/hjptriplebee
'''''''''''''''''''''''''''''''''''''''''''''''''''''
import tensorflow as tf
import numpy as np
from config import *

gtX = tf.placeholder(tf.int32, shape=[batchSize, None])  # input
gtY = tf.placeholder(tf.int32, shape=[batchSize, None])  # output

def buildModel(wordNum, hidden_units = 128, layers = 2):
    """build rnn"""
    with tf.variable_scope("embedding"): #embedding
        embedding = tf.get_variable("embedding", [wordNum, hidden_units], dtype = tf.float32)
        input = tf.nn.embedding_lookup(embedding, gtX)

    basicCell = tf.contrib.rnn.BasicLSTMCell(hidden_units, state_is_tuple = True)
    stackCell = tf.contrib.rnn.MultiRNNCell([basicCell] * layers)
    initState = stackCell.zero_state(batchSize, tf.float32)
    outputs, finalState = tf.nn.dynamic_rnn(stackCell, input, initial_state = initState)
    outputs = tf.reshape(outputs, [-1, hidden_units])

    with tf.variable_scope("softmax"):
        w = tf.get_variable("w", [hidden_units, wordNum])
        b = tf.get_variable("b", [wordNum])
        logits = tf.matmul(outputs, w) + b

    probs = tf.nn.softmax(logits)
    return logits, probs, stackCell, initState, finalState

def train(X, Y, wordNum, reload=True):
    """train model"""

    logits, probs, a, b, c = buildModel(wordNum)
    targets = tf.reshape(gtY, [-1])
    loss = tf.contrib.legacy_seq2seq.sequence_loss_by_example([logits], [targets],
                                                              [tf.ones_like(targets, dtype=tf.float32)], wordNum)
    cost = tf.reduce_mean(loss)
    tvars = tf.trainable_variables()
    grads, a = tf.clip_by_global_norm(tf.gradients(cost, tvars), 5)
    learningRate = learningRateBase
    optimizer = tf.train.AdamOptimizer(learningRate)
    trainOP = optimizer.apply_gradients(zip(grads, tvars))
    globalStep = 0

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        saver = tf.train.Saver()
        if reload:
            checkPoint = tf.train.get_checkpoint_state(".")
            # if have checkPoint, restore checkPoint
            if checkPoint and checkPoint.model_checkpoint_path:
                saver.restore(sess, checkPoint.model_checkpoint_path)
                print("restored %s" % checkPoint.model_checkpoint_path)
            else:
                print("no checkpoint found!")

        for epoch in range(epochNum):
            if globalStep % learningRateDecreaseStep == 0: #learning rate decrease by epoch
                learningRate = learningRateBase * (0.97 ** epoch)
            epochSteps = len(X) # equal to batch
            for step, (x, y) in enumerate(zip(X, Y)):
                globalStep = epoch * epochSteps + step
                a, loss = sess.run([trainOP, cost], feed_dict = {gtX:x, gtY:y})
                print("epoch: %d steps:%d/%d loss:%3f" % (epoch,step,epochSteps,loss))
                if globalStep%1000==0:
                    print("save model")
                    saver.save(sess,"poem",global_step=epoch)


def probsToWord(weights, words):
    """probs to word"""
    t = np.cumsum(weights)
    s = np.sum(weights)
    sample = int(np.searchsorted(t, np.random.rand(1) * s))
    return words[sample]

def test(wordNum, wordToID, words):
    """generate poem"""
    logits, probs, stackCell, initState, finalState = buildModel(wordNum)
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        saver = tf.train.Saver()
        checkPoint = tf.train.get_checkpoint_state(".")
        # if have checkPoint, restore checkPoint
        if checkPoint and checkPoint.model_checkpoint_path:
            saver.restore(sess, checkPoint.model_checkpoint_path)
            print("restored %s" % checkPoint.model_checkpoint_path)
        else:
            print("no checkpoint found!")

        state = sess.run(stackCell.zero_state(1, tf.float32))
        x = np.array([[wordToID['[']]])
        probs, state = sess.run([probs, finalState], feed_dict={gtX: x, initState: state})
        word = probsToWord(probs, words)
        poem = ''
        while word != ']':
            poem += word
            x = np.array([[wordToID[word]]])
            #ins = tf.stack(state)
            probs, state = sess.run([probs, finalState], feed_dict={gtX: x, initState: state})
            word = probsToWord(probs, words)
        print(poem)
        return poem







