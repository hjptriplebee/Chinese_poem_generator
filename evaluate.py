# coding: UTF-8
'''''''''''''''''''''''''''''''''''''''''''''''''''''
   file name: model.py
   create time: 2018年06月11日 星期一 13时53分42秒
   author: Jipeng Huang
   e-mail: huangjipengnju@gmail.com
   github: https://github.com/hjptriplebee
'''''''''''''''''''''''''''''''''''''''''''''''''''''
#evalute model, just for test
import data
from model import *

class EVALUATE_MODEL(MODEL):
    """evaluate model class"""
    def evaluate(self, reload=True):
        """evaluate model"""
        print("training...")
        gtX = tf.placeholder(tf.int32, shape=[batchSize, None])  # input
        gtY = tf.placeholder(tf.int32, shape=[batchSize, None])  # output

        logits, probs, a, b, c = self.buildModel(self.trainData.wordNum, gtX)

        targets = tf.reshape(gtY, [-1])

        # loss
        loss = tf.contrib.legacy_seq2seq.sequence_loss_by_example([logits], [targets],
                                                                  [tf.ones_like(targets, dtype=tf.float32)])
        globalStep = tf.Variable(0, trainable=False)
        addGlobalStep = globalStep.assign_add(1)

        cost = tf.reduce_mean(loss)
        trainableVariables = tf.trainable_variables()
        grads, a = tf.clip_by_global_norm(tf.gradients(cost, trainableVariables), 5) # prevent loss divergence caused by gradient explosion
        learningRate = tf.train.exponential_decay(learningRateBase, global_step=globalStep,
                                                  decay_steps=learningRateDecayStep, decay_rate=learningRateDecayRate)
        optimizer = tf.train.AdamOptimizer(learningRate)
        trainOP = optimizer.apply_gradients(zip(grads, trainableVariables))

        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            saver = tf.train.Saver()

            if not os.path.exists(evaluateCheckpointsPath):
                os.mkdir(evaluateCheckpointsPath)

            if reload:
                checkPoint = tf.train.get_checkpoint_state(evaluateCheckpointsPath)
                # if have checkPoint, restore checkPoint
                if checkPoint and checkPoint.model_checkpoint_path:
                    saver.restore(sess, checkPoint.model_checkpoint_path)
                    print("restored %s" % checkPoint.model_checkpoint_path)
                else:
                    print("no checkpoint found!")

            for epoch in range(epochNum):
                X, Y = self.trainData.generateBatch()
                epochSteps = len(X)  # equal to batch
                for step, (x, y) in enumerate(zip(X, Y)):
                    a, loss, gStep = sess.run([trainOP, cost, addGlobalStep], feed_dict={gtX: x, gtY: y})
                    print("epoch: %d, steps: %d/%d, loss: %3f" % (epoch + 1, step + 1, epochSteps, loss))
                    if gStep % saveStep == saveStep - 1:  # prevent save at the beginning
                        print("save model")
                        saver.save(sess, os.path.join(evaluateCheckpointsPath, type), global_step=gStep)

                X, Y = self.trainData.generateBatch(isTrain=False)
                print("evaluating testing error...")
                wrongNum = 0
                totalNum = 0
                testBatchNum = len(X)
                for step, (x, y) in enumerate(zip(X, Y)):
                    print("test batch %d/%d" % (step + 1, testBatchNum))
                    testProbs, testTargets = sess.run([probs, targets], feed_dict={gtX: x, gtY: y})
                    wrongNum += len(np.nonzero(np.argmax(testProbs, axis=1) - testTargets)[0])
                    totalNum += len(testTargets)
                print("accuracy: %.2f" % ((totalNum - wrongNum) / totalNum))



if __name__ == "__main__":
    trainData = data.POEMS(trainPoems, isEvaluate=True)
    MCPangHu = EVALUATE_MODEL(trainData)
    MCPangHu.evaluate()
