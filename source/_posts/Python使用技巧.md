---
title: Python使用技巧
date: 2018-08-11
categories: 
  - Python
---

# Python拼接字符串的几种方式


```
"""
1. 使用加号“+”连接字符串

    用加号“+”连接两个字符串，连接后这两个字符串将连接成一个字符串。但需注意的是，
不能用“+”连接字符串和数字，需要把数字使用str()函数转换成字符串，或者直接在数字两侧加带引号，再进行连接、
"""
```

```
str11 = "hello"
str12 = "world"
str13 = str11 + str12
print(str13)         # helloworld
```

> ```
> """ 注： 但在python中，尽量少用加号“+”连接字符串，原因如下：在python中，String对象是定长对象，一旦创建，长度就不可变化，若是使用+号连接两个字符串，则会新开辟一段长度总和长度的内存，再将两个字符串memcpy进去。如果要连接N个String对象，则要进行N-1次内存申请和拷贝。 官方推荐的是使用字符串的join方法，该方法对于连接一个list或tuple中的元素非常有效，它会先统计所有元素的长度，申请内存，然后拷贝。 """
> ```

```
"""
2. 使用逗号连接字符串
    python可用逗号“，”将多个字符串连接为一个元组，再通过join()方法将元组中的各个元素连接为一个字符串，
从而达到连接字符串的目的。若是直接将字符串逗号连接后print，字符串之间会多一个空格。
"""
```

```
str21 = "hello"
str22 = "world"
str23 = str21, str22

print(str21, str22)       # hello world

print(str23)              # ('hello', 'world')
print(''.join(str23))
```

```
"""
3. 直接连接字符串
    python独有的方法。只要把两个字符串放在一起，无论中间有空白或没有空白，
两个字符串将自动连接为一个字符串(空格不会自动去掉).
"""
```

```
print("hello" "world")      # helloworld
```

```
"""
4. 格式化方式拼接（ % ， format）
   符号“%”,{} 连接一个字符串和一组变量，字符串中的特殊标记会被自动用右边变量组中的变量进行替换.
（字符串之间会有空格隔开）
"""
```

```
print('%s %s %s' % ('我', '是', '中国人'))     # 我 是 中国人

print("{} {} {}".format('我', '是', '中国人'))
```

```
"""
5. 通过join()函数连接字符串
   利用字符串函数 join()，它是 split() 方法的逆方法。这个函数接收一个列表，
然后用字符串依次连接列表中每一个元素，其类似方法2的最后一步
"""
```

```
lists = ['hello', 'world']
print('_'.join(lists))       # hello_world
```

# 在Python中，是否有方法删除字符串中除字母以外的所有字符？
使用regex的解决方案在这里非常简单：
```
import re
newstring = re.replace(r"[^a-zA-Z]+", "", string)
```
其中，string是字符串，newstring是没有非字母字符的字符串。这样做的目的是用空字符串替换不是字母的每个字符，从而删除它。


正则表达式

```
import re
cop = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9]") # 匹配不是中文、大小写、数字的其他字符
string1 = '@ad&*jfad张132（www）。。。'
string1 = cop.sub('', string1) #将string1中匹配到的字符替换成空字符
```

# Python字符串去除空格和回车
## 1、去除Python字符串中的空格

**strip** ： 用来去除头尾字符、空白符(包括`\n`、`\r`、`\t`、`' '`，即：换行、回车、制表符、空格)

**lstrip** ：用来去除开头字符、空白符(包括`\n`、`\r`、`\t`、`' '`，即：换行、回车、制表符、空格)

**rstrip** ：用来去除结尾字符、空白符(包括`\n`、`\r`、`\t`、`' '`，即：换行、回车、制表符、空格)

使用示例：

```
print("   cjavapy   ".strip())            # returns "cjavapy"  
print("   cjavapy   ".lstrip())           # returns "cjavapy   "  
print("   cjavapy   ".rstrip())           # returns "   cjavapy"  
print("  c javapy py  ".replace(' ', '')) # returns "cjavapy"
```

## 2、去除Python字符串中换行符(\r,\n)

`\r`和`\n`都是以前的那种打字机传承来的。

`\r` 代表回车，也就是打印头归位，回到某一行的开头。

`\n`代表换行，就是走纸，下一行。

linux只用`\n`换行。

win下用`\r\n`表示换行。

使用 `.strip()`只能够去除字符串首尾的换行符，不能够去除中间的换行符，还需要使用 `.replace()`来替换`\r`和`\n`换行符。

1）去除换行符

```
.replace('\n', '').replace('\r', '')
```

2）去除制表符(\t)

```
.replace('\t', '')
```

3）其它特殊字符去除，也使用同样.replace()的方法替换即可
```
# 去除首位字符串空格,中间空格，回车符，换行符
print(str.strip().replace(' ', '').replace('\n', '').replace('\r', ''))
```

# python中实现字符串分割的方法有哪些？
**方法一：str.split**

split() 方法可以实现将一个字符串按照指定的分隔符切分成多个子串，通过该分割操作后，会返回一个列表。

```
s='abc'
s=s.split('')
print(list(filter(lambdax:x!='',s)))
```

**注意：** split()一次只可以使用一个符号进行字符串分割操作，

**方法二：re.split**

如若需要在一个字符串中进行多个字符的分割，可以使用import re模块进行字符串多种字符的分割。

```
>>>e="852317006@qq.com"
>>>importre
>>>re.split('@|\.',e)
['852317006','qq','com']
```

**方法三：str.partition**

利用字符串函数partition或者rpartition实现字符串分割。

将目标字符串分割为两个部分，返回一个三元元组（head,sep,tail），包含分割符。

```
>>>str
'abc,123efg,567'
>>>str.partition(',')
('abc',',','123efg,567')
>>>str.rpartition(',')
('abc,123efg',',','567')
```

# python读取文件夹下所有文件

```
import os

def readDir(dirPath):
    if dirPath[-1] == '/':
        print u'文件夹路径末尾不能加/'
        return
    allFiles = []
    if os.path.isdir(dirPath):
        fileList = os.listdir(dirPath)
        for f in fileList:
            f = dirPath+'/'+f
            if os.path.isdir(f):
                subFiles = readDir(f)
                allFiles = subFiles + allFiles #合并当前目录与子目录的所有文件路径
            else:
                allFiles.append(f)
        return allFiles
    else:
        return 'Error,not a dir'
```

# Python 下载图片的三种方法


```
import os
os.makedirs('./image/', exist_ok=True)
IMAGE_URL = "http://image.nationalgeographic.com.cn/2017/1122/20171122113404332.jpg"

def urllib_download():
    from urllib.request import urlretrieve
    urlretrieve(IMAGE_URL, './image/img1.png')     

def request_download():
    import requests
    r = requests.get(IMAGE_URL)
    with open('./image/img2.png', 'wb') as f:
        f.write(r.content)                      

def chunk_download():
    import requests
    r = requests.get(IMAGE_URL, stream=True)    
    with open('./image/img3.png', 'wb') as f:
        for chunk in r.iter_content(chunk_size=32):
            f.write(chunk)

urllib_download()
print('download img1')
request_download()
print('download img2')
chunk_download()
print('download img3')
```

# 如何在Python中获取当前时间戳？

在Python中，有多种方法可以获得当前时间戳。如果希望在Python中获得时间戳，可以使用来自模块time、datetime或calendar的函数。

**使用模块time**

模块time是提供各种与时间相关的功能。其中之一是time，它返回从历元开始的秒数。
```
import time;
ts = time.time()
print(ts)
# 1553577699.47 `
```
**使用模块datetime**

模块datetime提供了以更面向对象的方式操作日期和时间的类。其中之一是date .datetime。现在返回历元之后的秒数。
```
import datetime;
ts = datetime.datetime.now().timestamp()
print(ts)
# 1553577699.47
```

**使用模块calendar**

获取当前时间戳的另一种方法是从多个模块组合多个函数。Python还提供calendar模块。在本例中，我们将使用函数calendar。转换表示当前时间的元组。
```
import calendar;
import time;
ts = calendar.timegm(time.gmtime())
print(ts)
# 1553577699`
```

几种常见的时间格式，因为返回的是字符串，有时可以通过列表索引的方式截取需要的部分：

**2020-03-01 14:15:59**

```
import time
time.strftime("%Y-%m-%d %H:%M:%S")
12
```

**2020-03-01**

```
import time
time.strftime("%Y-%m-%d")
12
```

**2020/03/01**

```
import time
time.strftime("%Y/%m/%d")
12
```

**20200301**

```
import time
time.strftime("%Y%m%d")
12
```

**14:15:59**

```
import time
time.strftime("%H:%M:%S")
12
```

**141559**

```
import time
time.strftime("%H%M%S")
12
```

**Mar 01, 2020 Sun**

```
import time
time.strftime("%b %d, %Y %a")
12
```

**2020/03/01 Sun**

```
import time
time.strftime("%Y/%m/%d %a")
12
```

**2020年03月01日**

```
import time
time.strftime("%Y{y}%m{m}%d{d}").format(y="年", m="月", d="日")
12
```

**02:38:42 PM**

```
import time
time.strftime("%I:%M:%S %p")
```

### 秒级

```
import time

now = time.time() #返回float数据
#  获取当前时间戳---秒级级
print(int(now))
```

### 毫秒级

```
import time

now = time.time() #返回float数据

#毫秒级时间戳
print(int(round(now * 1000)))
```

# python 字符串里是否包含列表里的字符串
```
if any(list_element  in str for list_element in list):
    pass
else:
    pass
```

# 在python的dict中判断key是否存在

方法一：使用自带函数实现
```
dict = {'a': {}, 'b': {}, 'c': {}}
print(dict.__contains__("b"))         返回：True
print(dict.__contains__("d"))         返回：False
```
第二种方法：使用in方法
```
#生成一个字典
d = {'a':{}, 'b':{}, 'c':{}}
#打印返回值，其中d.keys()是列出字典所有的key
print 'a' in d.keys()
print 'a' in d
```
字典的`in`关系表达式允许我们查询字典中一个键是否存在。

语法

```
key in dict
```

示例

```
d = {'名字': '王路飞', '标志': '草帽', '武器': '拖鞋'}
print(d['名字'])
# 判断'绝招'(key)是否在字典d中
print('绝招' in d)
if not '绝招' in d:
    print('"绝招"(key)不在字典d中')
```

```vbnet
王路飞
False
"绝招"(key)不在字典d中
```

# 运行python脚本时传入参数的几种方法

**如果在运行python脚本时需要传入一些参数，例如`name`与age，可以使用如下方式。**

```delphi
python script.py '逍遥子,乔峰,孙悟空'  888
python test.py --name '逍遥子,乔峰,孙悟空' --age 888
```

这三种格式对应不同的参数解析方式，分别为**`sys.argv`、`argparse、` `tf.app.run，`** 前两者是python自带的功能，后者是`tensorflow`提供的便捷方式。

### 1.**`sys.argv`**

```undefined
特点:最简单,数据格式为列表,获取到的数据有点乱
```

代码:

```
# -*- coding: utf-8 -*-
import sys
arg=sys.argv
print(arg)

# 执行:python test.py 123 456 789
# ['test.py', '123', '456', '789']
```

### 2.**`argparse`**

```undefined
特点:简单,可以定义输入类型和默认值,获取到的数据整洁
```

代码:

```
# -*- coding: utf-8 -*-
import argparse

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument("--name", type=str, default="0", help='input name')
parser.add_argument("--age", type=int, default=32,help='input total age')
args = parser.parse_args()
print(args.name)
print(args.age)

# 执行:python test.py --name '逍遥子,乔峰,孙悟空' --age 888
# 逍遥子,乔峰,孙悟空
# 888

add_argument() 方法详解:
    name or flags - 一个命名或者一个选项字符串的列表，例如 foo 或 -f, --foo。
    action - 当参数在命令行中出现时使用的动作基本类型。
    nargs - 命令行参数应当消耗的数目。
    const - 被一些 action 和 nargs 选择所需求的常数。
    default - 当参数未在命令行中出现时使用的值。
    type - 命令行参数应当被转换成的类型。
    choices - 可用的参数的容器。
    required - 此命令行选项是否可省略 （仅选项可用）。
    help - 一个此选项作用的简单描述。
    metavar - 在使用方法消息中使用的参数值示例。
    dest - 被添加到 parse_args() 所返回对象上的属性名。
```

*注意:`parser.add_argument` 方法的`type`参数理论上可以是任何合法的类型， 但有些参数传入格式比较麻烦，例如list，所以一般使用`bool`, `int`, `str`, `float`这些基本类型就行了，更复杂的需求可以通过`str`传入，然后手动解析。`bool`类型的解析比较特殊，传入任何值都会被解析成`True`，传入空值时才为`False.`*

### 3.**tf.app.run**

```undefined
特点:定义比较麻烦,和argparser功能基本一样,可以定义输入类型和默认值
```

代码:

```
# -*- coding: utf-8 -*-
import tensorflow as tf
tf.app.flags.DEFINE_string('name', None, 'input name')
tf.app.flags.DEFINE_integer('age', 5, 'input total age')

FLAGS = tf.app.flags.FLAGS

def main(_):
    print(FLAGS.name)
    print(FLAGS.age)

if __name__=="__main__":
    tf.app.run()
```

# 三种方法获取Python 列表最后一个元素


三种方法获取Python 列表最后一个元素

```
>>> list1 = [1, 2, 3, 4, 5]
>>> print(list1[len(list1)-1])
5
>>> print(list1[-1])
5
>>> print(list1.pop())
5
>>>
```

# Python导入类的三种方法

### 导入模块就是为了使用模块中的类

---

> 当我们在写代码时，经常会遇到一种情况：我们要用到的一些功能已经在别的模块里定义过了，如果我们重新写一遍这个功能必然会使得代码冗长且效率低下。于是我们使用导入的方法将其它模块里的功能导入到自己的代码里，让我们在编写代码时能够使用。

---

### 导入整个模块（所有类）

导入整个模块的语句为：

```haskell
import ModuleName
```

通常这个模块就是要导入的那个类所在的文件`*.py`，所以调用类的方法为:

1. `object = ModuleName.ClassName()`
2. `object.属性`
3. `object.方法`

导入整个模块时将这个模块里所有的类都导入了，所以都可以调用。我们在导入时就一定要知道我们需要的这个类或方法属于这个模块。

---

### 导入单个或多个类

导入单个或多个类的语句为：

```typescript
from ModuleName import ClassName1,ClassName2,...
```

调用类的属性和方法的语句为：

1. `object = ClassName()`
2. `object.属性`
3. `object.方法`

在这种方法中，若导入的类名相同，则后面导入的类将会覆盖前面导入的类。

---

### 导入模块中所有的类：

导入模块中所有的类的语句为：

```typescript
from ModuleName import *
```

调用类的属性和方法的语句为：

1. `object = ClassName()`
2. `object.属性`
3. `object.方法`

在这种方法中，若导入的模块中含有名字相同的类，则类与类之间也会产生覆盖。

---

**总结一句话：就是当你只导入一个模块，没有导入模块中的类的时候，如果想用这个模块中的类来创建对象，一定要加上模块名；如果是按照模块中的类来导入的，那就只使用类名创建对象就好了。**

# 【Python】json与string相互转化


1 json->string

```
# -*- coding: utf-8 -*-
import json

student = {"id":"123", "name":"122", "age":18}
print(type(student))
print(student)

print('-'*10)

result = json.dumps(student)
print(type(result))
print(result)
123456789101112
```

2 string->json

2.2 json类

```
import json
str = '{"key": "wwww", "word": "qqqq"}'
j = json.loads(str)
print(j)
print(type(j))
12345
```

2.1 ast类

```
import ast 
a = "{1: 'a', 2: 'b'}"
b = ast.literal_eval(a)
type(b)
dict
```

# Python开启一个简单的Http文件服务器
有时你需临时搭建一个简单的 Web Server，但你又不想去安装 Apache、Nginx 等这类功能较复杂的 HTTP 服务程序时。这时可以使用 Python 内建的 SimpleHTTPServer 模块快速搭建一个简单的 HTTP 服务器。

SimpleHTTPServer 模块可以把你指定目录中的文件和文件夹以一个简单的 Web 页面的方式展示出来
熟悉Python的朋友们都知道，python自带了一个Simple HTTP Server，可以使用一行代码完成文件的局域网共享操作。
首先进入你需要设置的http服务器目录 (我以自己电脑路径：F:/Working~Study) ，即进入到该目录下，然后：
```
python2: python -m SimpleHTTPServer port
python3: python -m http.server port
```

1. 在需要发送的文件的路径上打开cmd，输入``python -m http.server 8080（端口可以自定义）--bind 0.0.0.0``
-m表示的是以模块引入，m表示module，在这里的作用是让编译器自行查找http.server的文件位置；当然也可以找到这个模块的绝对路径再直接用python ...运行，但这样会变得很麻烦,如果需要
2. 在接收端浏览器中直接访问``主机地址:8080``即可查看发送的文件，点击需要的文件下载

通过一行代码，我们完成了文件共享的http服务，但这个服务有几个问题，仅提供了下载功能无法上传，最重要的是没有权限控制功能，这就极其不安全了！

有时你需临时搭建一个简单的 Web Server，但你又不想去安装 Apache、Nginx 等这类功能较复杂的 HTTP 服务程序时。这时可以使用 Python 内建的 SimpleHTTPServer 模块快速搭建一个简单的 HTTP 服务器。

SimpleHTTPServer 模块可以把你指定目录中的文件和文件夹以一个简单的 Web 页面的方式展示出来

# Python Ftp服务器搭建
模块安装
python没有内置ftp模块，但要使用它却很简单，我们只需要简单的通过pip安装即可：
pip install pyftpdlib

简单共享
模块安装完成后，我们找到需要共享的目录，然后启动cmd后，输入：
```
python -m pyftpdlib -p 21
```
之后浏览器登陆ftp://ip:port,这样就开启了一个最简单的ftp共享服务。

有时当你想快速搭建一个 `FTP` 服务器来临时实现文件上传下载时，这是特别有用的。我们这里利用 `Python` 的 `Pyftpdlib` 模块可以快速的实现一个 `FTP` 服务器的功能。

首先安装 `Pyftpdlib` 模块

```
$ sudo pip install pyftpdlib
```

通过 `Python` 的 `-m` 选项将 `Pyftpdlib` 模块作为一个简单的独立服务器来运行，假设我们需要共享目录 `/Users/Mike/Docker`，只需要以下这个命令行就可以轻松实现：

```
cd /Users/Mike/Docker
python -m pyftpdlib
```

至此一个简单的 `FTP` 服务器已经搭建完成，访问 `ftp://IP:PORT` 即可。例如类似下面的 URL：

```
ftp://192.168.100.49:2121
```

> - 默认 IP 为本机所有可用 IP，端口为 2121。
> - 默认登陆方式为匿名。
> - 默认权限是只读。

如果你要建一个有认证且可写的 `FTP` 服务器，可使用类似以下指令：

```
$ python -m pyftpdlib -i 192.168.100.49 -w -d /tmp/ -u mike -P 123456
```

> 小插曲：测试时一直使用密码 `000000` 这样的弱密码做认证密码，在客户端登陆时一直提示认证失败。看来 `Pyftpdlib` 模块还做了基本的安全策略哟，不错的！

常用可选参数说明:

```
-i 指定IP地址（默认为本机所有可用 IP 地址）
-p 指定端口（默认为 2121）
-w 写权限（默认为只读）
-d 指定目录 （默认为当前目录）
-u 指定登录用户名
-P 指定登录密码
```


# Python调用系统命令的四种方法（os.system、os.popen、commands、subprocess）



### 一、os.system方法

这个方法是直接调用标准C的system() 函数，仅仅在一个子终端运行系统命令，而不能获取命令执行后的返回信息。

os.system[cmd]的返回值。如果执行成功，那么会返回0，表示命令执行成功。否则，则是执行错误。

使用os.system返回值是脚本的退出[状态码]，该方法在调用完shell脚本后，返回一个16位的二进制数，低位为杀死所调用脚本的信号号码，高位为脚本的退出状态码。

os.system()返回值为0 linux命令返回值也为0。

os.system()返回值为256，十六位[二进制]数示为：00000001，00000000，高八位转成十进制为 1 对应 linux命令返回值 1。

os.system()返回值为512，十六位二进制数示为：00000010，00000000，高八位转成十进制为 2 对应 linux命令返回值 2。

```
import os
result = os.system('cat /etc/passwd')
print(result)      
# 0
```

### 二、os.popen方法

os.popen()方法不仅执行命令而且返回执行后的信息对象(常用于需要获取执行命令后的返回信息)，是通过一个管道文件将结果返回。通过 os.popen() 返回的是 file read 的对象，对其进行读取 read() 的操作可以看到执行的输出。

```
import os
result = os.popen('cat /etc/passwd')
print(result.read())
```
当然还有其它类似命令：
```
import os
os.system("ls")
os.system("cd test && mkdir test1")
```

### 三、commands模块

```
import commands
status = commands.getstatus('cat /etc/passwd')
print(status)
output = commands.getoutput('cat /etc/passwd')
print(output)
(status, output) = commands.getstatusoutput('cat /etc/passwd')
print(status, output)
```

>commands模块在Python3中已废弃。
### 四、subprocess模块

Subprocess是一个功能强大的子进程管理模块，是替换os.system,os.spawn* 等方法的一个模块。
当执行命令的参数或者返回中包含了中文文字，那么建议使用subprocess。

```
import subprocess
res = subprocess.Popen('cat /etc/passwd', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) # 使用管道
print res.stdout.read()  # 标准输出
for line in res.stdout.readlines():
    print line
res.stdout.close()         # 关闭
```

### 五、总结：

os.system：获取程序执行命令的返回值。
os.popen： 获取程序执行命令的输出结果。
commands：获取返回值和命令的输出结果。


# python通过正则匹配指定字符开头与结束提取中间内容

## 一、提取包含始末字符

1、起始字符串固定

```
a = re.findall('起始字符串.*结束字符串',str)
```

2、起始字符串不固定（即从首字符串提取到固定的字符串结束），用^指定从首字符串开始

```
a = re.findall('^.*结束字符串',str)
```

## 二、不包含始末字符串

```
#方法1
a = re.findall('(?<=始字符串).*?(?=末字符串)',str)
#方法2
a = re.findall('始字符串(.*?)末字符串',str)
```

1. 在 re.findall()的方法中 '始字符串. *末字符串’ 可以匹配到相同的值直到最后一个值；如果参数为 '始字符串.* ?末字符串’则只匹配到第一个值。
2. 其实使用.*和.+都能提取特定始末字符串中间的内容，下面顺便说下两者的区别。

## 三、.*和.+正则提取的区别

.：匹配任意字符
*：匹配0个或多个字符
?：非贪婪模式，在符合的条件下，尽可能少的匹配(尽可能短的匹配)

```
str2 = "aabab"
a = re.findall('a.*?b',str2)	#结果：['aab', 'ab']
b = re.findall('a.+?b',str2)	#结果：['aab']
```

.*?：匹配aab和ab ，因为*可以匹配0个字符，所以可以匹配得到ab
.+?：匹配aab，因为+必须a和b中间至少有一个字符，所以排除了ab

## 四、起始有无^的区别

```
str2 = "aabab"
c = re.findall('.*',str2)	#结果：['aabab', '']
d = re.findall('^.*',str2)	#结果：['aabab']
```

## 五、[pandas](https://so.csdn.net/so/search?q=pandas&spm=1001.2101.3001.7020)对具体列的内容通过正则表达式进行数据提取

1. 使用前要确保该列的类型统一，str或者float格式，最好事先通过astype强制转换一下
2. df[‘新列名’]=df[‘提取的列名’].str.extract(‘正则表达式’, expand = True)

## 六、遇到的报错

报错：pattern contains no capture groups
（翻译：模式不包含捕获组）
解决：根据docs ，您需要为 str.extract 指定一个捕获组(即括号)好，提取。

参考文章：[https://www.cnblogs.com/ZhangHT97/p/13427325.html](https://www.cnblogs.com/ZhangHT97/p/13427325.html)
[https://www.cnblogs.com/YouJeffrey/p/15209895.html](https://www.cnblogs.com/YouJeffrey/p/15209895.html)
[https://blog.csdn.net/dudu3332/article/details/111555572](https://blog.csdn.net/dudu3332/article/details/111555572)


# python之Pyftpdlib第三方库在本机搭建FTP服务器

## 前言

1、在同一个局域网的多台电脑，传递文件时可以通过搭建web服务器，设置目录浏览的方式快速分享。如果上传就比较麻烦了，通过QQ/微信会产生很多文件记录，通过teamviewer太慢，其实FTP服务器倒是一个不错的选择。

2、FTP服务器软件在日常开发中，基本不会用到。还涉及 macOS、 Windows的环境差异，非常麻烦。虽然有免费开源的 filezzila，配置还是很繁琐的。

3、Python语言 + **pyftpdlib** 库实现局域网文件互传：一般来说，开发机都会安装Python环境，再安装 **pyftpdlib** 库就可以搭建在本地计算机搭建一个FTP服务。从而实现局域网内的文件互传。

4、通常Linux主机都是使用vsftp，pureftp来搭建FTP服务器，但配置很复杂。如果在工作中或者项目上只是临时使用FTP服务器，可以用python的 **pyftpdlib** 库。

## 下载与安装

```
pip install pyftpdlib
```

## FTP服务器环境搭建

### 1、一行代码实现FTP服务器：

通过Python的 **-m** 选项作为一个简单的独立服务器来运行，当你想快速共享一个目录的时候，这是特别有用的。

在需要共享的目录下打开终端执行如下命令即可把当前目录共享出去（匿名登录）

```
python -m pyftpdlib
```
至此，一个简单的FTP服务器已经搭建完成，访问 ftp://127.0.0.1:2121 即可，如下：（默认FTP的IP为 127.0.0.1 、端口为 2121 ）

### 2、命令行可选参数：

* ** -i** ： 指定IP地址（默认为本机的IP地址）
* **-p** ： 指定端口（默认为2121）
* **-w** ：写权限（默认为只读）
* **-d** ： 指定目录 （默认为当前目录）
* **-u** ：指定用户名登录
* **-P** ：设置登录密码

#### 带参数命令行方式运行FTP服务器：

```
python -m pyftpdlib -w -d [PATH] -u [USER] -P [PASSWORD]
```

例如：

```
python -m pyftpdlib -w -d ~/Desktop -u admin -P 123456
```
## 搭建一个功能强大完善的FTP服务

### 1、上述的一行命令已经可以实现一个简单的FTP服务器，但是要搭建一个功能强大完善的FTP服务所涉及到的配置较多，这时需要使用 **Pyftpdlib** 库提供的 API 来编写。

### 2、名词解释：

**pyftpdlib.ftpservers.FTPServer**  : 接收客户端连接，然后分发给对应的程序。

**pyftpdlib.handlers.FTPHandler**  : 一个表示服务器协议解释器的类，每次出现一个新的连接FTPServer将创建一个新的FTPHandler实例来处理当前PI会话。

**pyftpdlib.handlers.ActiveDIP** 和 **pyftpdlib.handlers.PassiveDIP**  : 主动模式和被动模式的基础类。

**pyftpdlib.handlers.DTPHandler**  : 这个类处理的是数据传输进程。

**pyftpdlib.authorizers.DummyAuthorizer**  : 处理FTP的认证和权限的处理类，用于处理用户密码，获取用户的家目录和权限，DummyAuthorizer 是基础的认证模块的类，提供平台无关接口的基础授权程序类
用于管理虚拟用户。

**pyftpdlib.filesystems.AbstractedFS**  : 类用于与文件系统交互，提供了一个高级的，跨平台接口兼容Windows和UNIX风格文件系统。

### 3、实例如下：

[![复制代码](/images/48304ba5e6f9fe08f3fa1abda7d326ab.webp)](javascript:void(0); "复制代码")

```
#!/usr/bin/env python3
# coding:utf-8

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os

global author


def ftp_server(username, password, directory):
    """
    启动一个ftp的server进程

    :param username: 需要添加用户的用户名
    :param password: 用户的密码
    :param directory: 用户的家目录，也就是FTP服务器的数据目录
    :return:
    """

    # 如果目录不存在，就创建目录

    global author
    if not os.path.exists(directory):
        os.mkdir(directory)

    try:
        # 实例化DummyAuthorizer来创建ftp用户
        author = DummyAuthorizer()
        # 参数：用户名，密码，目录，权限
        author.add_user(username, password, directory, perm="elradfmw")

        # 匿名登录
        # authorizer.add_anonymous(directory)
    except OSError as e:
        if "Address already in use" in e:
            print("21号端口被占用")

    # 初始化ftp句柄
    handler = FTPHandler
    handler.authorizer = author

    # 添加被动端口范围
    handler.passive_ports = range(2000, 2400)

    # 启动server，本地执行，监听21号端口（参数：IP，端口，handler）
    server = FTPServer(('0.0.0.0', 21), handler)
    server.serve_forever()


if __name__ == '__main__':
    ftp_server(username="zhanghao", password="aixocm", directory="/data/zhanghao")
```
### 6、用户权限：

**读取权限：**

* "e" ：更改目录（CWD，CDUP命令）
* "l" ：列表文件（LIST，NLST，STAT，MLSD，MLST，SIZE命令）
* "r" ：从服务器检索文件（RETR命令）

**写入权限：**

* "a" ：将数据追加到现有文件（APPE命令）
* "d" ：删除文件或目录（DELE，RMD命令）
* "f" ：重命名文件或目录（RNFR，RNTO命令）
* "m" ：创建目录（MKD命令）
* "w" ：将文件存储到服务器（STOR，STOU命令）
* "M"：更改文件模式/权限（SITE CHMOD命令）
* "T"：更改文件修改时间（SITE MFMT命令）


