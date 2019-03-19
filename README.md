# S2Box
This is an undergraduate's python code for my S2box in NEAU jidainyanjiuzhongxin.
## 概述
这是我本科生时在东北农业大学机电研究中心时写的代码，你看到的代码是智能喷洒模块(英文名是：Smart and Spray Box，缩写：S2Box)的视觉部分代码。
代码一共三个文件，用Python编写，个人感觉我的串口部分有一点参考价值。
### box_model.py
box_model.py是主文件。
``` python
def getnozzleGrass(mod = 2):  #定义喷草的模式
def detectGrass(cnt, area):   #检测草
def changeModel(mod,ser1):    #接收串口的信息，改变喷草模式
```
### grasscontours.py
grasscontours.py是检测草的文件，用颜色来识别，得到二值图像。
``` python
def detect(img):        #用c语言来遍历图像，并筛选所要的像素值，因为Python遍历太慢。
                        #这种方法对环境有要求，每次更换环境时要调一下c语言里遍历的代码，
                        #调整后效果很不错。
def select(img):        #通过形态学处理，滤掉较小的杂点和把一颗苗草连接起来。
```
### box_interactive_plus.py
box_interactive_plus.py是串口发送文件，用类封装。
``` python
def __init__(self, port, baudrate):
    self.__ser = serial.Serial(port, baudrate)
    self.__sent = False              #判断是否发送，防止开线程发送时有两个命令同时发送导致发送命令混在一起。
    self.__wtime = time.time()       #设置一个时间，防止对一个苗草发送两次喷洒指令，后面还会说。
    self.__position = 0              #设置一个位置，防止对一个苗草发送两次喷洒指令，后面还会说。
    self.__model = '0'               #规定喷洒模式。
    self.__parameter = ''            #用来存储距地高度(S2box摄像头旁上有一个超声波模块，用来测据地高)。
```
```python
def send(self, scmd):                #发送指令，当时队员要求我每发送一个指令时发送一个'\r\n'表示发送完毕。
    while(self.__sent):pass          #判断是否发送，防止开线程发送时有两个命令同时发送导致发送命令混在一起。
def readm(self):                     #直接读取S2box的模式。
def readp(self):                     #读取S2box的据地高度。
def bmodel(self):                    #开线程读取S2box的模式，这样读取不用主程序花时间等反馈。
def __readmodel(self):               #读取S2box的模式的私有函数。
def __mvstart(self, scmd, wait_time, nozzle_number, c_ratio=2000):
                                     #除草的私有函数。
def mvgrass(self, position, wait_time, nozzle_number, grass_size): #除草函数
    if abs(self.__position - position) >=4 and time.time() - self.__wtime >=0.3:
                                     #这个语句防止对一个苗草发送两次喷洒指令，原理是：给串口发送的苗或草的位置和时间
                                     #要与上一次串口发送的位置和时间有一定的差值。
def close(self):                     #关闭串口。
```
## 识别效果
![](doc/detection.gif)
其它图也较大，点击查看：[实验图](doc/experiment.gif)、[工作图](doc/work.gif)。
## 与我联系
如果学弟有该项目相关问题，可以发我邮箱: nutshellqian@qq.com。
