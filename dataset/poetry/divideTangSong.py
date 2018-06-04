# coding: UTF-8
'''''''''''''''''''''''''''''''''''''''''''''''''''''
   file name: divideTangSong.py
   create time: 2018年06月04日 星期一 19时29分55秒
   author: Jipeng Huang
   e-mail: huangjipengnju@gmail.com
   github: https://github.com/hjptriplebee
'''''''''''''''''''''''''''''''''''''''''''''''''''''
# divide tang and song poem

import os
import re
import shutil

if not os.path.exists("./tang"):
    os.mkdir("tang")
if not os.path.exists("./song"):
    os.mkdir("song")

for file in os.listdir("."):
    if os.path.isfile(os.path.join("./", file)) and re.match('(.*)(\.)(json)', file) != None:
        shutil.copyfile(os.path.join("./", file), os.path.join("./", file.split(".")[1], file))
