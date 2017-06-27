# coding: UTF-8
'''''''''''''''''''''''''''''''''''''''''''''''''''''
   file name: main.py
   create time: 2017年06月23日 星期五 16时41分54秒
   author: Jipeng Huang
   e-mail: huangjipengnju@gmail.com
   github: https://github.com/hjptriplebee
'''''''''''''''''''''''''''''''''''''''''''''''''''''
import argparse
import dataPretreatment
import model
from config import *

def defineArgs():
    """define args"""
    parser = argparse.ArgumentParser(description = "Chinese_poem_generator.")
    parser.add_argument("-m", "--mode", help = "select mode by 'train' or test or head",
                        choices = ["train", "test", "head"], default = "test")
    return parser.parse_args()

if __name__ == "__main__":
    X, Y, wordNum, wordToID, words = dataPretreatment.pretreatment(trainPoems)
    args = defineArgs()
    if args.mode == "train":
        print("training...")
        model.train(X, Y, wordNum)
    else:
        if args.mode == "test":
            print("genrating...")
            poems = model.test(wordNum, wordToID, words)
        else:
            characters = input("please input chinese character:")
            print("genrating...")
            poems = model.testHead(wordNum, wordToID, words, characters)