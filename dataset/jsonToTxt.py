# coding: UTF-8
'''''''''''''''''''''''''''''''''''''''''''''''''''''
   file name: main.py
   create time: 2017年05月28日 星期一 11时08分54秒
   author: Jipeng Huang
   e-mail: huangjipengnju@gmail.com
   github: https://github.com/hjptriplebee
'''''''''''''''''''''''''''''''''''''''''''''''''''''
# Function: json dataset to txt
# change parameters to transfer new json file
# @typeName: name of dir
# @titleField: title in json
# @contentField: content in json
# @author: author in json
# generate a typeName.txt file in typeName dir.

import json
import os
import re

typeName = "poetrySong"

titleField = "title"
contentField = "paragraphs"
authorField = "author"

jsonPath = "./" + typeName
saveFile = open(os.path.join(jsonPath, typeName + ".txt"), "w")

for file in os.listdir(jsonPath):
    if os.path.isfile(os.path.join(jsonPath,file)) and re.match('(.*)(\.)(json)', file) != None:
        print("processing file: %s" % file)
        poems = json.load(open(os.path.join(jsonPath,file), "r"))
        for singlePoem in poems:
            content = "".join(singlePoem[contentField])
            title = singlePoem[titleField]
            author = singlePoem[authorField]
            saveFile.write(title + "::" + author + "::" + content + "\n")

saveFile.close()
