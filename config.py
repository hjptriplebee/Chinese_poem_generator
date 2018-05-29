# coding: UTF-8
'''''''''''''''''''''''''''''''''''''''''''''''''''''
   file name: config.py
   create time: 2017年06月25日 星期日 10时56分55秒
   author: Jipeng Huang
   e-mail: huangjipengnju@gmail.com
   github: https://github.com/hjptriplebee
'''''''''''''''''''''''''''''''''''''''''''''''''''''
import tensorflow as tf
import numpy as np
import argparse
import os
import random
import time

batchSize = 64

learningRateBase = 0.001
learningRateDecayStep = 1000
learningRateDecayRate = 0.95

epochNum = 500                    # train epoch
generateNum = 1                   # number of generated poems per time

trainPoems = "dataset/shijing/shijing.txt" # training file location
checkpointsPath = "./checkpoints/shijing" # checkpoints location

saveStep = 500