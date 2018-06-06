# coding: UTF-8
'''''''''''''''''''''''''''''''''''''''''''''''''''''
   file name: data.py
   create time: 2017年06月23日 星期五 17时17分36秒
   author: Jipeng Huang
   e-mail: huangjipengnju@gmail.com
   github: https://github.com/hjptriplebee
'''''''''''''''''''''''''''''''''''''''''''''''''''''
from config import *

class POEMS:
    "poem class"
    def __init__(self, filename):
        """pretreatment"""
        poems = []
        file = open(filename, "r")
        for line in file:  #every line is a poem
            title, author, poem = line.strip().split("::")  #get title and poem
            poem = poem.replace(' ','')
            if len(poem) < 10 or len(poem) > 512:  #filter poem
                continue
            if '_' in poem or '《' in poem or '[' in poem or '(' in poem or '（' in poem:
                continue
            poem = '[' + poem + ']' #add start and end signs
            poems.append(poem)
            #print(title, author, poem)
        print("学习样本总数： %d" % len(poems))
        #counting words
        allWords = {}
        for poem in poems:
            for word in poem:
                if word not in allWords:
                    allWords[word] = 1
                else:
                    allWords[word] += 1
        # erase words which are not common
        # erase = []
        # for key in allWords:
        #     if allWords[key] < 2:
        #         erase.append(key)
        # for key in erase:
        #     del allWords[key]

        allWords[" "] = -1
        wordPairs = sorted(allWords.items(), key = lambda x: -x[1])
        self.words, freq = zip(*wordPairs)
        self.wordNum = len(self.words)

        self.wordToID = dict(zip(self.words, range(self.wordNum))) #word to ID
        self.poemsVector = [([self.wordToID[word] for word in poem]) for poem in poems] # poem to vector

    def generateBatch(self):
        #padding length to batchMaxLength
        random.shuffle(self.poemsVector)
        batchNum = (len(self.poemsVector) - 1) // batchSize
        X = []
        Y = []
        #create batch
        for i in range(batchNum):
            batch = self.poemsVector[i * batchSize: (i + 1) * batchSize]
            maxLength = max([len(vector) for vector in batch])
            temp = np.full((batchSize, maxLength), self.wordToID[" "], np.int32)
            for j in range(batchSize):
                temp[j, :len(batch[j])] = batch[j]
            X.append(temp)
            temp2 = np.copy(temp) #copy!!!!!!
            temp2[:, :-1] = temp[:, 1:]
            Y.append(temp2)
        return X, Y

