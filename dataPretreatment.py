# coding: UTF-8
'''''''''''''''''''''''''''''''''''''''''''''''''''''
   file name: dataPretreatment.py
   create time: 2017年06月23日 星期五 17时17分36秒
   author: Jipeng Huang
   e-mail: huangjipengnju@gmail.com
   github: https://github.com/hjptriplebee
'''''''''''''''''''''''''''''''''''''''''''''''''''''
from config import *
import numpy as np

def pretreatment(filename):
    """pretreatment"""
    poems = []
    file = open(filename, "r")
    for line in file:  #every line is a poem
        #print(line)
        title, poem = line.strip().split(":")  #get title and poem
        poem = poem.replace(' ','')
        if '_' in poem or '《' in poem or '[' in poem or '(' in poem or '（' in poem:
            continue
        if len(poem) < 10 or len(poem) > 128:  #filter poem
            continue
        poem = '[' + poem + ']' #add start and end signs
        poems.append(poem)

    print("唐诗总数： %d"%len(poems))
    #counting words
    allWords = {}
    for poem in poems:
        for word in poem:
            if word not in allWords:
                allWords[word] = 1
            else:
                allWords[word] += 1
    #'''
    # erase words which are not common
    erase = []
    for key in allWords:
        if allWords[key] < 2:
            erase.append(key)
    for key in erase:
        del allWords[key]
    #'''
    wordPairs = sorted(allWords.items(), key = lambda x: -x[1])
    words, a= zip(*wordPairs)
    #print(words)
    words += (" ", )
    wordToID = dict(zip(words, range(len(words)))) #word to ID
    wordTOIDFun = lambda A: wordToID.get(A, len(words))
    poemsVector = [([wordTOIDFun(word) for word in poem]) for poem in poems] # poem to vector
    #print(poemsVector)
    #padding length to batchMaxLength
    batchNum = (len(poemsVector) - 1) // batchSize
    X = []
    Y = []
    #create batch
    for i in range(batchNum):
        batch = poemsVector[i * batchSize: (i + 1) * batchSize]
        maxLength = max([len(vector) for vector in batch])
        temp = np.full((batchSize, maxLength), wordTOIDFun(" "), np.int32)
        for j in range(batchSize):
            temp[j, :len(batch[j])] = batch[j]
        X.append(temp)
        temp2 = np.copy(temp) #copy!!!!!!
        temp2[:, :-1] = temp[:, 1:]
        Y.append(temp2)

    return X, Y, len(words) + 1, wordToID, words


