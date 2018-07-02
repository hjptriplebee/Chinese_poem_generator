# Chinese_poem_generator 
[![Build Status](https://travis-ci.org/hjptriplebee/Chinese_poem_generator.svg?branch=master)](https://travis-ci.org/hjptriplebee/Chinese_poem_generator)
[![codecov](https://codecov.io/gh/hjptriplebee/Chinese_poem_generator/branch/master/graph/badge.svg)](https://codecov.io/gh/hjptriplebee/Chinese_poem_generator)
[![license](https://img.shields.io/aur/license/yaourt.svg)](https://github.com/hjptriplebee/Chinese_poem_generator/blob/master/LICENSE)

唐诗宋词生成器，MC胖虎，使用LSTM完成，先看几个demo：

一首藏头诗刀山火海送给大家！

<img src="https://raw.githubusercontent.com/hjptriplebee/Chinese_poem_generator/master/panghu1.jpg" width = "100" height = "100" alt="demo2" /> <img src="https://raw.githubusercontent.com/hjptriplebee/Chinese_poem_generator/master/demo1.png" width = "350" height = "100" alt="demo1" />

胖虎学诗，会对偶，用典故，能作出边塞、田园、离别等多种风格的诗！

<img src="https://raw.githubusercontent.com/hjptriplebee/Chinese_poem_generator/master/demo2.png" width = "45%" alt="demo2" />

## 依赖
- Python3
- tensorflow1.2+

## 用法
- "python3 main.py -m {train, test, head}" train训练, test随机写诗, head藏头诗.
- 在对深度学习有一定了解的基础上，可尝试使用evalute.py评估自己训练的模型。

## 最近一次更新(2018-06-11)
- add coverage

## 常见问题
**Q: 默认写唐诗，如何使胖虎写宋词，歌曲等其他东西？**

A: 因为仓库不宜过大，所以只放了词的训练数据而没有放训练好的模型。config.py中默认的type是poetrySong，因而训练数据用的是“./dataset/poetrySong/poetrySong.txt"，加载的checkpoint是”./checkpoints/poetrySong/checkpoint“，如想使用其他训练数据，修改config.py，比如：type = songci，然后训练至少10个epoch。

**Q: 如何训练自己的数据？**

A: 目前的训练数据来源于[https://github.com/chinese-poetry/chinese-poetry](https://github.com/chinese-poetry/chinese-poetry)，我已经将json转换成txt，训练数据格式如下，可以将自己的数据做成这种形式训练模型。将数据按照同样的形式放入dataset下自己新建的目录，修改config.py中的type即可训练。

```json
标题::作者::内容
静夜思::李白::床前看月光，疑是地上霜。举头望山月，低头思故乡。
```

## 接下来要做
- 尝试采用双向lstm模型
- 数据预处理步骤需要加强，比如：特殊符号。
- 看图写诗，苦于没有数据集。
- 引入平仄等信息，使网络更容易拟合宋不规整的数据。
- tensorboard
- 写一篇关于整个项目的博文

有时候效果不好，多生成几次一定有比较好的结果。现在看起来有点像人工智障，但是相信胖虎会越来越厉害！

**方法比较粗暴，欢迎各位大佬提出建设性意见！**
**详细的项目实现和代码说明请看[这里](http://blog.csdn.net/accepthjp/article/details/73875108)**

<img src="https://raw.githubusercontent.com/hjptriplebee/Chinese_poem_generator/master/panghu2.jpg" width = "200" height = "200" alt="demo2" />

