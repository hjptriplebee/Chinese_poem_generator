# Chinese_poem_generator 
[![Build Status](https://travis-ci.org/hjptriplebee/Chinese_poem_generator.svg?branch=master)](https://travis-ci.org/hjptriplebee/Chinese_poem_generator)
[![codecov](https://codecov.io/gh/hjptriplebee/Chinese_poem_generator/branch/master/graph/badge.svg)](https://codecov.io/gh/hjptriplebee/Chinese_poem_generator)
[![license](https://img.shields.io/aur/license/yaourt.svg)](https://github.com/hjptriplebee/Chinese_poem_generator/blob/master/LICENSE)

唐诗生成器，MC胖虎，使用LSTM完成，先看几个demo：

一首藏头诗刀山火海送给大家！

<img src="https://raw.githubusercontent.com/hjptriplebee/Chinese_poem_generator/master/panghu1.jpg" width = "100" height = "100" alt="demo2" /> <img src="https://raw.githubusercontent.com/hjptriplebee/Chinese_poem_generator/master/demo1.png" width = "350" height = "100" alt="demo1" />

胖虎学诗3万首，会对偶，用典故，经常能作出边塞、田园、离别等多种风格的诗，信手拈来，好不好！

<img src="https://raw.githubusercontent.com/hjptriplebee/Chinese_poem_generator/master/demo2.png" width = "850" height = "350" alt="demo2" />

## 依赖
- Python3
- tensorflow1.0+

## 用法
- "python3 main.py -m {train, test, head}" train训练, test随机写诗, head藏头诗. 

## 最近一次更新(2018-05-17)
- 加入Travis CI持续集成

## 接下来要做
- 数据预处理步骤需要加强，比如：繁体字、特殊符号。
- 使用更全更优质的唐诗数据训练。[https://github.com/chinese-poetry/chinese-poetry](https://github.com/chinese-poetry/chinese-poetry)
- 修复有时出现的死循环。
- 看图写诗，苦于没有数据集。

有时候效果不好，多生成几次一定有比较好的结果。现在看起来有点像人工智障，但是相信胖虎会越来越厉害！

**方法比较粗暴，欢迎各位大佬提出建设性意见！**
**详细的项目实现和代码说明请看[这里](http://blog.csdn.net/accepthjp/article/details/73875108)**

<img src="https://raw.githubusercontent.com/hjptriplebee/Chinese_poem_generator/master/panghu2.jpg" width = "200" height = "200" alt="demo2" />

