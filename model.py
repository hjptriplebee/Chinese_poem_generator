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

def buildModel(wordNum, gtX, hidden_units = 128, layers = 2):
    """build rnn"""
    with tf.variable_scope("embedding"): #embedding
        embedding = tf.get_variable("embedding", [wordNum, hidden_units], dtype = tf.float32)
        inputbatch = tf.nn.embedding_lookup(embedding, gtX)

    basicCell = tf.contrib.rnn.BasicLSTMCell(hidden_units, state_is_tuple = True)
    stackCell = tf.contrib.rnn.MultiRNNCell([basicCell] * layers)
    initState = stackCell.zero_state(np.shape(gtX)[0], tf.float32)
    outputs, finalState = tf.nn.dynamic_rnn(stackCell, inputbatch, initial_state = initState)
    outputs = tf.reshape(outputs, [-1, hidden_units])

    with tf.variable_scope("softmax"):
        w = tf.get_variable("w", [hidden_units, wordNum])
        b = tf.get_variable("b", [wordNum])
        logits = tf.matmul(outputs, w) + b

    probs = tf.nn.softmax(logits)
    return logits, probs, stackCell, initState, finalState

def train(X, Y, wordNum, reload=True):
    """train model"""
    gtX = tf.placeholder(tf.int32, shape=[batchSize, None])  # input
    gtY = tf.placeholder(tf.int32, shape=[batchSize, None])  # output
    logits, probs, a, b, c = buildModel(wordNum, gtX)
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
                learningRate = learningRateBase * (0.95 ** epoch)
            epochSteps = len(X) # equal to batch
            for step, (x, y) in enumerate(zip(X, Y)):
                #print(x)
                #print(y)
                globalStep = epoch * epochSteps + step
                a, loss = sess.run([trainOP, cost], feed_dict = {gtX:x, gtY:y})
                print("epoch: %d steps:%d/%d loss:%3f" % (epoch,step,epochSteps,loss))
                if globalStep%1000==0:
                    print("save model")
                    saver.save(sess,"poem",global_step=epoch)

def probsToWord(weights, words):
    """probs to word"""
    t = np.cumsum(weights) #prefix sum
    s = np.sum(weights)
    coff = np.random.rand(1)
    index = int(np.searchsorted(t, coff * s)) # large margin has high possibility to be sampled
    return words[index]

def test(wordNum, wordToID, words):
    """generate poem"""
    gtX = tf.placeholder(tf.int32, shape=[1, None])  # input
    logits, probs, stackCell, initState, finalState = buildModel(wordNum, gtX)
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

        poems = []
        for i in range(generateNum):
            state = sess.run(stackCell.zero_state(1, tf.float32))
            x = np.array([[wordToID['[']]])
            probs1, state = sess.run([probs, finalState], feed_dict={gtX: x, initState: state})
            word = probsToWord(probs1, words)
            poem = ''
            while word != ']':
                poem += word
                if word == '。':
                    poem += '\n'
                x = np.array([[wordToID[word]]])
                probs2, state = sess.run([probs, finalState], feed_dict={gtX: x, initState: state})
                word = probsToWord(probs2, words)
            print(poem)
            poems.append(poem)
        return poems

def testHead(wordNum, wordToID, words, characters):
    gtX = tf.placeholder(tf.int32, shape=[1, None])  # input
    logits, probs, stackCell, initState, finalState = buildModel(wordNum, gtX)
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
        flag = 1
        endSign = {-1: "，", 1: "。"}
        poem = ''
        for c in characters:
            state = sess.run(stackCell.zero_state(1, tf.float32))
            word = c
            flag = -flag
            while word != ']' and word != '，' and word != '。':
                poem += word
                x = np.array([[wordToID[word]]])
                probs2, state = sess.run([probs, finalState], feed_dict={gtX: x, initState: state})
                word = probsToWord(probs2, words)
            poem += endSign[flag]
            if endSign[flag] == '。':
                poem += '\n'
        print(characters)
        print(poem)
        return poem
