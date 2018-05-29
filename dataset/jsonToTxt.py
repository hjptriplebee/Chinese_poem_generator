# coding: UTF-8
'''''''''''''''''''''''''''''''''''''''''''''''''''''
   file name: main.py
   create time: 2017年05月28日 星期一 11时08分54秒
   author: Jipeng Huang
   e-mail: huangjipengnju@gmail.com
   github: https://github.com/hjptriplebee
'''''''''''''''''''''''''''''''''''''''''''''''''''''
import json

jsonPath = "./shijing/shijing.json"
titleField = "title"
contentField = "content"
authorField = "section"
fileName = jsonPath.split('/')[-1].split('.')[0]

poems = json.load(open(jsonPath, "r"))
saveFile = open(fileName + ".txt", "w")
for singlePoem in poems:
    content = "".join(singlePoem[contentField])
    title = singlePoem["title"]
    saveFile.write(title + ":" + content + "\n")

saveFile.close()
