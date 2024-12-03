---
title: Python语法总结
---

# 一.python的基本数据类型。
Python常见的数据类型:Number（数字）、String（字符串）、List（列表）、Tuple（元组）、Set（集合）、Dictionary（字典）。
- type(xx)              #获取类型,返回值就是数据类型
- isinstance(xx, yy )   #判断是否属于某一种类型,属于返回true,不属于返回false  
### 1.Number（数字）
Python3 支持** int、float、bool、complex（复数）**。
```
>>> a, b, c, d = 20, 5.5, True, 4 + 3j#定义多个变量
>>> print(type(a), type(b), type(c), type(d))#输出变量的类型
<class 'int'> <class 'float'> <class 'bool'> <class 'complex'>
```

### 1.String（字符串）
Python中的字符串用单引号 ' 或双引号 " 括起来，同时使用反斜杠 \ 转义特殊字符。
```
>>> a="hello"
>>> b='hi'
>>> print(type(a),type(b))

<class 'str'> <class 'str'>
```

##### (1)字符串切片
- str[:] 提取从开头（默认位置0）到结尾（默认位置-1）的整个字符串
- str[start:] 从start 提取到结尾
- str[:end] 从开头提取到end 负数
- str[start:end] 从start 提取到end 负数
- str[start:end:step] 从start 提取到end - 1，每step 个字符提取一个

##### (2)字符串连接
-  +：字符串连接
```
>>> a="hello"
>>> b='python'
>>> print(a+b)

hellopython
```

##### (3)字符串大小写转换
```
>>> str = "Python"
 
>>> str.upper()                #转大写
'PYTHON'
 
>>> str.lower()                #转小写 
'python'
 
>>> str.capitalize()           #字符串首为大写，其余小写
'Python'
 
>>> str.swapcase()             #大小写对换 
'pYTHON'
 
>>> str.title()                #以分隔符为标记，首字符为大写，其余为小写
'Python'
```



##### (4)字符串条件判断
```
>>> str = '01234'
 
>>> str.isalnum()                #是否全是字母和数字，并至少有一个字符
True
>>> str.isdigit()                #是否全是数字，并至少有一个字符
True      
 
>>> str = 'string'
 
>>> str.isalnum()                  #是否全是字母和数字，并至少有一个字符
True
>>> str.isalpha()                  #是否全是字母，并至少有一个字符 
True
>>> str.islower()                  #是否全是小写，当全是小写和数字一起时候，也判断为True
True
 
>>> str = "01234abcd"
 
>>> str.islower()                  #是否全是小写，当全是小写和数字一起时候，也判断为True
True
 
>>> str.isalnum()                  #是否全是字母和数字，并至少有一个字符
True
 
>>> str = ' '
>>> str.isspace()                  #是否全是空白字符，并至少有一个字符
True
 
>>> str = 'ABC'
 
>>> str.isupper()                  #是否全是大写，当全是大写和数字一起时候，也判断为True
True
 
>>> str = 'Aaa Bbb'
 
>>> str.istitle()                  #所有单词字首都是大写，标题 
True
 
 
>>> str = 'string learn'
 
>>> str.startswith('str')          #判断字符串以'str'开头
True
 
>>> str.endswith('arn')            #判读字符串以'arn'结尾
True
```
##### (5)字符串搜索定位与替换
```
>>> str='string lEARn'
 
>>> str.find('z')              #查找字符串，没有则返回-1，有则返回查到到第一个匹配的索引
-1
 
>>> str.find('n')              #返回查到到第一个匹配的索引
4
 
>>> str.rfind('n')             #返回的索引是最后一次匹配的
11
 
>>> str.index('a')             #如果没有匹配则报错 
Traceback (most recent call last):
  File "<input>", line 1, in <module>
ValueError: substring not found
  
>>> str.index("n")            #同find类似,返回第一次匹配的索引值
4
 
>>> str.rindex("n")           #返回最后一次匹配的索引值
11
 
>>> str.count('a')            #字符串中匹配的次数
0
 
>>> str.replace('EAR','ear')  #匹配替换
'string learn'
 
>>> str.replace('n','N')
'striNg lEARN'
 
>>> str.replace('n','N',1)
'striNg lEARn'
 
>>> str.strip('n')          #删除字符串首尾匹配的字符，通常用于默认删除回车符 
   
'string lEAR' 
   
>>> str.lstrip('n')        #左匹配 
   
'string lEARn' 
   
>>> str.rstrip('n')        #右匹配 
   
'string lEAR' 
 
>>> str = " tab"
 
>>> str.expandtabs()       #把制表符转为空格
' tab'
 
>>> str.expandtabs(2)      #指定空格数
' tab'
```

##### (6)字符串编码与解码
```
>>> str = "字符串学习"
>>> str
'\xe5\xad\x97\xe7\xac\xa6\xe4\xb8\xb2\xe5\xad\xa6\xe4\xb9\xa0'
 
>>> str.decode('utf-8')                                               #解码过程，将utf-8解码为unicode
u'\u5b57\u7b26\u4e32\u5b66\u4e60'
 
>>> str.decode("utf-8").encode('gbk')                                 #编码过程，将unicode编码为gbk
'\xd7\xd6\xb7\xfb\xb4\xae\xd1\xa7\xcf\xb0'
 
>>> str.decode('utf-8').encode('utf-8')                               #将unicode编码为utf-8 
'\xe5\xad\x97\xe7\xac\xa6\xe4\xb8\xb2\xe5\xad\xa6\xe4\xb9\xa0'
```

##### (7)字符串分割变换
```
>> str = "Learn string"
 
>>> '-'.join(str) 
'L-e-a-r-n- -s-t-r-i-n-g'
 
>>> li = ['Learn','string']
 
>>> '-'.join(li)
'Learn-string'
 
>>> str.split('n')
['Lear', ' stri', 'g']
 
>>> str.split('n',1)
['Lear', ' string']
 
>>> str.rsplit('n')
['Lear', ' stri', 'g']
 
>>> str.rsplit('n',1)
['Learn stri', 'g']
 
>>> str.splitlines()
['Learn string']
 
>>> str.partition('n')
('Lear', 'n', ' string')
 
>>> str.rpartition('n')
('Learn stri', 'n', 'g')
```

### 3.List（列表）
列表List可以包含不同类型的数据对像，同时它是一个有序的集合"python 集合"
```
list = [ 'abcd', 66 , 6.66, 'lisi', 76.2 ]
```
列表可以包含不同类型对像，也支持嵌套：
```
a = ['a',5867,['cc',4,],(1,2)]
```
##### (1)列表增加新的元素
```
list.append()            #在list 末尾增加一个元素

list.insert(n,'4')       #在指定位置添加元素，如果指定的下标不存在，那么就是在末尾添加

list1.extend(list2)      #合并两个list   list2中仍有元素
```

##### (2)删除list 中的元素
```
list.pop()                  #删最后一个元素

list.pop(n)                 #指定下标，删除指定的元素，如果删除一个不存在的元素会报错

list.remove(xx)             #删除list 里面的一个元素，有多个相同的元素，删除第一个 

print(list.pop())           #有返回值

print(list.remove())        #无返回值

list.clear()                #清空list

del  list[n]                #删除指定下标对应的元素 

del list                    #删除整个列表， list删除后无法访问

```

##### (3)查看列表中的值
```
print(list)                  #遍历列表输出

print(list[n])               #使用下标索引来访问列表中的值，同样你也可以使用方括号的形式截取字符

print(list.count(xx))        #查看某个元素在这个列表里的个数，如果改元素不存在，那么返回0

print(list.index(xx))        #找到这个元素的角标，如果有多个，返回第一个，如果找一个不存在的元素会报错

````

##### (4)列表排序和反转
```
list.reverse()              #将列表反转

list.sort()                 #排序，默认升序

list.sort(reverse=True)     #降序排列
```
>注：list 中有字符串，数字时不能排序，排序针对同类型

##### (5)列表操作的函数
```
len(list)                   #列表元素个数 

max(list)                   #返回列表元素最大值 

min(list)                   #返回列表元素最小值 

list(seq)                   #将元组转换为列表
```

### 4.Tuple（元组）
元组（tuple）与列表类似，**不同之处在于元组的元素不能修改**。元组写在小括号 () 里，元素之间用逗号隔开，元组中的元素类型也可以不相同。定义元组后，如果想要访问其中的元素，也可像访问列表中的值一样使用索引访问。
```
tuple = ('hi', 666, 6.23, 'python', 760.2)
```
特点:
- 与字符串一样，元组的元素不能修改。
- 元组也可以被索引和切片，方法和列表一样。
- 元组也可以使用+操作符进行拼接。

### 5.Set(集合)
集合（set）是由一个或数个形态各异的大小整体组成的，构成集合的事物或对象称作元素或是成员。可以使用大括号 { } 或者 set() 函数创建集合。集合里面的元素不能重复(语法上面写了重复的数据也会自动去重)，且元素无序的可变的数据组织形式。


```
>>> a = {1,3,5,8,1,3,5,8}
>>> print(a)

{8, 1, 3, 5}
```
##### (1)集合添加元素
```
>>> set1 = {1,3}
>>> set1.add(2)
>>> print(set1)
```


##### (2)删除集合元素
```
set.pop()       #pop会从集合中随机删除一个元素
set.remove(x)   #删除x元素
set.discard(x)  #与remove（）用法相同，但是如果元素不存在，不会报错。
set.clear()     #删除所有元素
```
##### (3)集合运算
```
set1.intersection(set2)     #取set1和set2的交集
set1.union(set2)            #取set1和set2的并集
set1.difference(set2)       #取set1和set2的差集
```

>注意：创建一个空集合必须用 set() 而不是 { }，因为 { } 是用来创建一个空字典。集合没有重复元素，且无序的数据类型,且不能通过索引来引用集合中的元素。
>

### 6.Dictionary（字典）
字典由多个键和其对应的值构成的键—值对组成，键和值中间以冒号：隔开，项之间用逗号隔开，整个字典是由大括号{}括起来的。这种结构类型通常也被称为映射，或者叫关联数组，也有叫哈希表的。
```
d = { "xx" : '666' , 'cat' : '999' , 'lxf' : '333' }
#字典里面也可以嵌套字典
d1 = {
    "k1": 18,
    "k2": True,
    "k3": ['Su', {
        'kk1': 'vv1',
        'kk2': 'vv2',
        'kk3': (11, 22),
    }
           ],
    1527: (11, 22, 33, 44)
}
```


Python字典内置函数：
- cmp(dict1, dict2)：比较两个字典元素。
- len(dict)：计算字典元素个数，即键的总数。
- str(dict)：输出字典可打印的字符串表示。
- type(variable)：返回输入的变量类型，如果变量是字典就返回字典类型。
- dictionary.clear()：删除字典内所有元素
- dictionary.copy()：返回一个字典的浅复制
- dictionary.fromkeys()：创建一个新字典，以序列seq中元素做字典的键，val为字典所有键对应的初始值
- dictionary.get(key, default=None)：返回指定键的值，如果值不在字典中返回default值
- dictionary.has_key(key)：如果键在字典dict里返回true，否则返回false
- dictionary.items()：以列表返回可遍历的(键, 值) 元组数组
- dictionary.keys()：以列表返回一个字典所有的键
- dictionary.setdefault(key, default=None)：和get()类似, 但如果键不已经存在于字典中，将会添加键并将值设为default
- dictionary.update(dict2)：把字典dict2的键/值对更新到dict里
- dictionary.values()：以列表返回字典中的所有值

# 二.Python运算符。
### 1.算术运算符
运算符 |	描述  |	实例
--|--|--
+	| 加 - 两个对象相加	| a + b 输出结果 30
-	| 减 - 得到负数或是一个数减去另一个数 |	a - b 输出结果 -10
*	|乘 - 两个数相乘或是返回一个被重复若干次的字符串 |	a * b 输出结果 200
/	|除 - x除以y |	b / a 输出结果 2
%	|取模 - 返回除法的余数 |	b % a 输出结果 0
**	|幂 - 返回x的y次幂|	a**b 为10的20次方， 输出结果 100000000000000000000

### 2.比较运算符
运算符 |	描述 |	实例
--|--|--
==|	等于 - 比较对象是否相等 |	(a == b) 返回 False。
!= |	不等于 - 比较两个对象是否不相等	|(a != b) 返回 true.
<>	| 不等于 - 比较两个对象是否不相等	|(a <> b) 返回 true。这个运算符类似 != 。
>	| 大于 - 返回x是否大于y	|(a > b) 返回 False。
<	| 小于 - 返回x是否小于y。所有比较运算符返回1表示真，返回0表示假。这分别与特殊的变量True和False等价。	|(a < b) 返回 true。
>=	| 大于等于	- 返回x是否大于等于y。	| (a >= b) 返回 False。
<=	| 小于等于 -	返回x是否小于等于y。|	(a <= b) 返回 true。

### 3.赋值运算符
运算符 |	描述  |	实例
--|--|--
= |	简单的赋值运算符|	c = a + b 将 a + b 的运算结果赋值为 c
+= |	加法赋值运算符|	c += a 等效于 c = c + a
-= |	减法赋值运算符|	c -= a 等效于 c = c - a
*= |	乘法赋值运算符|	c *= a 等效于 c = c * a
/= |	除法赋值运算符|	c /= a 等效于 c = c / a
%= |	取模赋值运算符|	c %= a 等效于 c = c % a
**= |	幂赋值运算符|	c **= a 等效于 c = c ** a
//= |	取整除赋值运算符|	c //= a 等效于 c = c // a

### 4.逻辑运算符
运算符|	逻辑表达式|	描述|	实例
--|--|--|--
and|	x and y|	布尔"与" - 如果 x 为 False，x and y 返回 False，否则它返回 y 的计算值。|	(a and b) 返回 20。
or|	x or y	|布尔"或"	- 如果 x 是非 0，它返回 x 的值，否则它返回 y 的计算值。	|(a or b) 返回 10。
not|	not x|	布尔"非" - 如果 x 为 True，返回 False 。如果 x 为 False，它返回 True。|	not(a and b) 返回 False

# 三.Python条件判断
### 1.Python中的if语句
```
if 判断条件:
    执行语句……
```

### 2.Python中的if..else语句
```
if 判断条件:
    执行语句……
else:
    执行语句……
```

### 3.Python中的if..elif语句
```
if 判断条件1:
    执行语句1……
elif 判断条件2:
    执行语句2……
elif 判断条件3:
    执行语句3……
else:
    执行语句4……
```
>注:False，None，0，""，()，[]，{}值在作为布尔表达式时，会被解释器看作假。其他都为真。

# 四.Python循环结构
### 1. while循环
循环的作用就是让指定的代码重复的执行，while 循环最常用的应用场景就是让执行的代码按照指定的次数重复执行
```
while 条件():    
    条件满足时，做的事情    
    ......
```

### 2. for循环
for 循环的语法格式如下：
```
for 迭代变量 in 字符串|列表|元组|字典|集合：
    代码块
```

### 3.循环中的一些中止指令
- break语句:在语句块执行过程中终止循环，并且跳出整个循环。
- continue语句:在语句块执行过程中终止当前循环，跳出该次循环，执行下一次循环。
- pass语句:pass是空语句，是为了保持程序结构的完整性。

# 五.Python函数
函数最只要的目的就是封装一个功能。函数有两个优点:减少代码重复率。增强代码可阅读性。在调用函数的时候，如果传入的参数数量不对，会报TypeError的错误。如果传入的参数数量是对的，但参数类型不能被函数所接受，也会报TypeError的错误.
### 1.Python定义函数
在Python中，定义一个函数要使用def语句，依次写出函数名、括号、括号中的参数和冒号:，然后，在缩进块中编写函数体，函数的返回值用return语句返回。
```
def test(x):
    if x >= 0:
        return x
    else:
        return -x
```

### 2.Python定义空函数
如果想定义一个什么事也不做的空函数，作用是可以用来作为占位符，比如现在还没想好怎么写函数的代码，就可以先放一个pass，让代码能运行起来。
```
def test():
    pass
```

### 3.Python参数
函数的参数在调用时，如果没有设置默认参数那么是必传的，调用函数时不传会报错。如果一个函数设置了默认参数,那么在调用的时候就可以不传入该参数,也可以使用默认值调用该函数。
```
def person(name, gender, age=6, city='Beijing'):
    print('name:', name)
    print('gender:', gender)
    print('age:', age)
    print('city:', city)
```
>函数定义时必传参数在前，默认参数在后，否则Python的解释器会报错。

### 4.Python函数返回值
return语句：程序退出该函数，并返回到函数被调用的地方。return语句返回的值传递给调用程序
Python函数的返回值有两种形式：
##### (1)函数返回一个值
```
def test(x,y):
    return x+y;
```
##### (2)函数返回多个值
函数可以同时返回多个值，但其实就是一个元组。
```
def test(x,y):
    return x,y;
```
- 当函数执行到return的时候，就会马上终止函数执行。
- 函数中可以出现多个return，但有且只有一个return会被执行。
- return 后面可以不跟值，return 单独使用等价于return None。

# 六.Python面向对象之类
### 1.python定义类
面向对象最重要的概念就是类（Class）和实例（Instance）
```
class Preson(object):
    pass
```
class后面紧接着是类名，类名通常是大写开头的单词。紧接着是(object)，表示该类是从哪个类继承下来的,通常，如果没有合适的继承类，就使用object类，这是所有类最终都会继承的类。

### 2.python创建类的实例
创建实例是通过类名+()实现的：
```
xiaomin= Preson()
```

### 3.python类init方法
所有类都有一个名为 __init__() 的函数，它始终在启动类时执行。使用 __init__() 函数将值赋给对象属性，或者在创建对象时需要执行的其他操作。__init__函数第一个参数永远是实例变量self，表示创建的类实例本身。在创建实例的时候。就可以将属性绑定上去。
```
class Preson(object):
    def __init__(self, name, age):
        self.name = name
        self.age= age
  ```
>注:和普通的函数相比，在类中定义的函数只有一点不同，就是第一个参数永远是实例变量self，表示创建的类实例本身。并且，调用时，不用传递该参数。除此之外，类的方法和普通函数没有什么区别，所以，你仍然可以用默认参数、可变参数、关键字参数和命名关键字参数。

### 4.python类的实例方法
通常情况下，在类中定义的普通方法即为类的实例方法，实例方法第一个参数是 self（self 是一种约定习惯） 代表实例本身，当调用某个实例方法时，该实例的对象引用作为第一个参数 self 隐式的传递到方法中。
一种方式调用:实例对象调用。
```
class Person:
    age = 30
    # 类构造方法也是实例方法
    def __init__(self):
        self.name = "张三"
    # 实例方法
    def say(self):
        print('my name is'+self.name+"age is"+str(self.age))

# 实例化
person = Person()
# 调用实例方法
person.say()
```

### 5.python类的类方法
类方法必须需要使用 @classmethod 装饰器申明。类的类方法也必须包含一个参数，通常约定为 cls ，cls 代表 类本身（注意不是实例本身，是有区别的），python 会自动将类本身传给 cls，所有这个参数也不需要我们传值，类方法不能获取构造函数定义的变量(类方法可以访问类变量，但不能访问实例变量)，Python中使用比较少。
两种方式调用：类.方法名 和 实例对象调用。

```

class Person:
    age = 30
    # 类构造方法也是实例方法
    def __init__(self):
        self.name = "张三"
    # 实例方法
    @classmethod
    def say(cls):
        print('my age is'+str(cls.age))

# 实例化
person = Person()
# 调用实例方法
person.say()

# 类.方法名调用
Person.say()
```

### 6.python类的静态方法
静态方法需要使用 @staticmethod 装饰器声明。类的静态方法和我们自定义的函数基本没什么区别，没有 self，且不能访问类属性。使用静态方法的好处是，不需要定义实例即可使用这个方法，Python中使用比较少，因为可以使用普通函数替代。
有两种调用方式：类.方法名和实例对象调用 。

```
class Person:
    age = 30
    # 类构造方法也是实例方法
    def __init__(self):
        self.name = "张三"
    # 实例方法
    @staticmethod
    def say():
        print('静态方法')

# 实例化
person = Person()
# 调用实例方法
person.say()

# 类.方法名调用
Person.say()
```

### 7.类属性访问限制
在python中可以给一个类实例绑定很多属性，拿到类的实例以后还是可以自由地修改一个实例的name、age属性的值。如果有些属性不希望被外部访问，就需要对这些属性进行访问限制。Python中没有访问控制的关键字，例如private、protecte和public等。如果要让内部属性不被外部访问，可以把属性的名称前加上两个下划线__，在Python中，实例的变量名如果以__开头，就变成了一个私有变量（private），只有内部可以访问，外部不能访问。
```
class Preson():
    __nikeName = "钢蛋"
    def __init__(self, name, age):
        self.__name = name
        self.__age = age

    def say(self):
        print('%s: %s' % (self.__name, self.__age))
    def get_nick_name(self):
        return self.__nikeName

person=Preson("zhangsan",30)
person.say()

print(person.nikeName)          #无法直接访问属性

print(person.get_nick_name())   #通过方法访问属性
```

# 七.Python面向对象之继承
在OOP程序设计中，当我们定义一个class的时候，可以从某个现有的class继承，新的class称为子类（Subclass），而被继承的class称为基类、父类或超类（Base class、Super class）。继承机制经常用于创建和现有类功能类似的新类，又或是新类只需要在现有类基础上添加一些成员（属性和方法），但又不想直接将现有类代码复制给新类。也就是说，通过使用继承这种机制，可以轻松实现类的重复使用。
```
class Animal:
    def eat(self):
        print (self.name+"吃")
    def drink(self):
        print (self.name+"喝" )
class Cat(Animal):
    def __init__(self, name):
        self.name = name
 
    def shout(self):
        print(self.name+'喵喵叫') 
 
class Dog(Animal):
 
    def __init__(self, name):
        self.name = name
 
    def shout(self):
        print(self.name+'汪汪叫')
 
c1 = Cat('波斯猫')
c1.eat()
 
c2 = Cat('橘猫')
c2.drink()
 
d1 = Dog('哈士奇')
d1.eat()
d1.shout()
```
- 在Python中，如果父类和子类都重新定义了构造方法init( )，在进行子类实例化的时候，子类的构造方法不会自动调用父类的构造方法，必须在子类中显示调用。 
- Python的类可以继承多个类，Java和C#中则只能继承一个类 。
- Python的类如果继承了多个类，那么其寻找方法的方式有两种，分别是：深度优先和广度优先 。
- 当类是经典类时，多继承情况下，会按照深度优先方式查找，当类是新式类时，多继承情况下，会按照广度优先方式查找。
>建议大家尽量不要使用多继承。

# 八.Python 模块和包
### 1.Python中的模块
Python中为了实现某种逻辑将相关联的函数写在同一个文件里，使逻辑更清楚，这就是一个模块，在python中文件以.py 结尾，这个.py文件就可以称之为模块。Python本身就内置了很多非常有用的模块，只要安装完毕，这些模块就可以立刻使用。

### 2.Python中的包
为了方便管理模块，python 中引入了包的概念,包是由关联的多个模块组成的目录，在每一个包下而都有一个__init__.py文件，这个文件必须存在,否则，Python就把这个目录当成普通目录，而不是一个包，init.py 可以是空文件，也可是有python代码，因为__init__.py本身就是一个模块

### 3.Python导入其他模块
```
import modea
```
```
from modea import test # 从 modea中导入test方法
```
```
import modea as moa #导入modea并且将命名空间变成moa
```
第一次导入后就将模块名加载到内存了，后续的import语句仅是对已经加载大内存中的模块对象增加了一次引用，不会重新执行模块内的语句）

### 4.Python导入不同包下的模块
![image.png](https://img-blog.csdnimg.cn/img_convert/cc6fd6dcc51260c9246e4714c4ddf3c2.png)
需要在不同的包里面加int方法
```
import test.mode_b
```

# 九.Python 第三方模块包
### 1.Python手动引入第三方模块包(源码安装)
很多第三方库都是开源的，几乎都可以在[github](https://github.com/) 或者 [pypi](https://pypi.org/)上找到源码。找到源码格式大概都是 zip 、 tar.zip、 tar.bz2格式的压缩包。
1. 下载好后将其解压后复制到Python安装目录的：C:\python\Lib\site-packages文件夹里即可:
- windows默认路径在 C:\Python2.7\Lib\site-packages。
- Linux默认路径在 /usr/local/lib/python2.7/dist-packages。
- Mac默认路径在 /Library/Python/2.7/site-packages。
2. 打开cmd命令窗口，进入到包所在的目录里，执行：``python setup.py install`` 即可，用此方法安装包时都执行此命令，因为下载的压缩包里有setup.py文件，并且已经进入此包的文件夹中，所以不必写包的名字。
3. 到此就安装成功了。在Python的交互界面用import 包名，验证是否成功安装，不报错即安装成功。
> 想要卸载这些库也很简单，进入 site-packages，直接删掉库文件就可以了。

### 2.Python通过包管理工具(Pip)引入第三方模块包
1. 首先确定你的Python已经安装了pip;(Python3在安装的过程中自动为用户安装了pip)。
2. 确保电脑是联网状态，输入命令``pip install + 要安装的模块名称``直接安装即可。
3. 使用pip是会自动的为你识别到Python3的安装目录。

**常用的pip命令：**
1. pip自身的升级：
```
python -m pip  install --upgrade pip
```
2. pip安装/卸载包：
```
pip install 包名             （安装）
pip uninstall 包名           （卸载）
```
3. pip检查哪些软件需要更新：
```
pip list --outdated
```
4. pip查看已经安装的包：
```
pip list
或：
pip freeze
```
5. pip升级软件包：
```
pip install --upgrade 包名
```
6. pip搜索包：
```
pip search "包名"               （包名用双引号括起来）
```
7. pip查看某个包的详细信息：
```
pip show 包名
```
8. pip安装指定版本的包：（安装指定版本的包是，可通过使用==, >=, <=, >, <来指定一个版本号）
```
pip install 包名==版本号

例如：
pip install nose==1.3.1
pip install 'Markdown<2.0'
pip install 'Markdown>2.0,<2.0.3'
```
9. 查看pip版本：
```
pip.exe -V             （V：大写）
```

### 3.查看Python包安装的路径
命令行模式下输入：
```
>>> import sys
>>> sys.path
['', 'C:\\Python27\\Lib\\idlelib', ...]
```

# 十.Python多进程
进程是计算机中的程序关于某数据集合上的一次运行活动，是系统进行资源分配和调度的基本单位.
### 1:启动多进程
##### (1)multiprocessing启动多进程.
multiprocessing是一个跨平台的python包，因此我们使用该工具包进行多进程的开发.
```
from multiprocessing import Process
#子进程需要执行的代码
def run(str):
   while True:
       # os.getpid()获取当前进程id号
       # os.getppid()获取当前进程的父进程id号
       print(" %s--%s--%s"%(str, os.getpid(),os.getppid()))
       sleep(1)
#创建子进程
#target说明进程执行的任务
p = Process(target=run, args=("test",))
#启动进程
p.start()

#父进程的结束不能影响子进程，让父进程等待子进程结束再执行父进程
process.join()
```
##### (2)利用进程池生成进程
开多进程是为了并发，通常有几个cpu核心就开几个进程，但是进程开多了会影响效率，主要体现在切换的开销，所以引入进程池限制进程的数量。进程池内部维护一个进程序列，当使用时，则去进程池中获取一个进程，初始化一个Pool时，可以指定一个最大进程数，如果超过这个数，那么请求就会等待，直到池中有进程结束，才会创建新的进程来执行

```
rom multiprocessing import Pool
mport os, time, random
ef run(name):
   print("子进程%d启动--%s" % (name, os.getpid()))
f __name__ == "__main__":
   #创建多个进程
   #进程池
   #表示可以同时执行的进程数量
   #Pool默认大小是CPU核心数
   pp = Pool(2)
   for i in range(3):
       #创建进程，放入进程池同意管理
       pp.apply_async(run,args=(i,))

   #在调用join之前必须先调用close,调用close之后就不能再继续添加新的进程了
   pp.close()
   #进程池对象调用join，会等待进程池中所有的子进程结束完毕再去执行父进程
   pp.join()
```

### 2.多进程之间的通信
进程彼此之间互相隔离，要实现进程间通信（IPC），multiprocessing模块支持两种形式：队列和管道，这两种方式都是使用消息传递的。
##### (1)使用进程队列queue实现多进程之间的通信
```
from multiprocessing import Process, Queue
import os, time

def write(q):
    print("启动写子进程%s" % (os.getpid()))
    q.put("A")
    print("结束写子进程%s" % (os.getpid()))

def read(q):
    print("启动读子进程%s" % (os.getpid()))
    while True:
        value = q.get(True)
        print("value = " + value)
    print("结束读子进程%s" % (os.getpid()))


if __name__ == "__main__":
    #父进程创建队列，并传递给子进程
    q = Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))

    pw.start()
    pr.start()

    pw.join()
    #pr进程里是个死循环，无法等待其结束，只能强行结束
    pr.terminate()

    print("父进程结束")

```
##### (2)使用进程队列Manager().Queue()实现多进程之间的通信
如果使用进程池pool创建进程的话，就需要使用Manager().Queue()
```
from multiprocessing import Manager, Process, Pool
import threading
import random, time,os

# queue，实现多进程之间的数据传递，其实就是个消息队列

def write(q):
    print('---write thread is %s' % os.getpid())
    for value in ['A', 'B', 'C']:
        print("put %s to queue" % value)
        q.put(value)


def read(q):
    print('---read thread is %s' % os.getpid())
    for i in range(q.qsize()):
        print("Get value is %s" % q.get(True))


if '__main__' == __name__:
    print('---main thread is %s' % os.getpid())
    q = Manager().Queue()
    po = Pool()
    po.apply(write, args=(q,))
    po.apply(read, args=(q,))
    po.close()
    po.join()
    print('---end---')
```

# 十一.Python多线程
### 1.线程的概念
在一个进程的内部，要同时干多件事，就需要同时运行多个“子任务”，我们把进程内的这些“子任务”叫做线程。这些线程的运行顺序是不确定的、随机的、不可预测的。Python中提供了两个模块帮助实现多线程:
1. _thread模块属于低级模块。
2. threading模块高级模块，对_thread进行了封装

### 2.Python启动线程
在线程里面setDaemon（）和join（）方法都是常用的启动线程方式.
- join ()方法：主线程A中，创建了子线程B，并且在主线程A中调用了B.join()，那么，主线程A会在调用的地方等待，直到子线程B完成操作后， 才可以接着往下执行，那么在调用这个线程时可以使用被调用线程的join方法。join([timeout]) 里面的参数时可选的，代表线程运行的最大时间，即如果超过这个时间，不管这个此线程有没有执行完毕都会被回收，然后主线程或函数都会接着执行的，如果线程执行时间小于参数表示的 时间，则接着执行，不用一定要等待到参数表示的时间。
- setDaemon()方法。主线程A中，创建了子线程B，并且在主线程A中调用了B.setDaemon(),这个的意思是，把主线程A设置为守护线程，这时候，要是主线程A执行结束了，就不管子线程B是否完成，一并和主线程A退出.这就是setDaemon方法的含义，这基本和join是相反的。此外，还有个要特别注意的：必须在start()方法调用之前设置，如果不设置为守护线程，程序会被无限挂起，只有等待了所有线程结束它才结束。
```
import threading,time


def run(num):
    print("子线程(%s)开始" % (threading.current_thread().name))

    #实现线程的功能
    time.sleep(2)
    print("打印", num)
    time.sleep(2)

    print("子线程(%s)结束" % (threading.current_thread().name))

if __name__ == "__main__":
    #任何进程默认就会启动一个线程，称为主线程，主线程可以启动新的子线程
    #current_thread()：返回返回当前线程的实例
    print("主线程(%s)启动" % (threading.current_thread().name))

    #创建子线程                     线程的名称
    t = threading.Thread(target=run, name="runThread", args=(1,))
    t.start()
    #t.setDaemon(True)#设置为后台线程，这里默认是Fal#se，设置为True之后则主线程不用等待子线程
    #等待线程结束
    t.join()

    print("主线程(%s)结束" % (threading.current_thread().name))

```

### 3.Python多线程共享数据
多线程和多进程最大的不同在于，多进程中，同一个变量，各自有一份拷贝存在每个进程中，互不影响。而多线程中，所有变量都由所有线程共享。所以，任何一个变量都可以被任意一个线程修改，因此，线程之间共享数据最大的危险在于多个线程同时修改一个变量，容易把内容改乱了。
##### (1)多线程造成数据混乱
```
import threading
num = 0

def run(n):
    global num
    for i in range(10000000):
        num = num + n    
        num = num - n    

if __name__ == "__main__":
    t1 = threading.Thread(target=run, args=(6,))
    t2 = threading.Thread(target=run, args=(9,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    print("num =",num)

```
##### (2)线程锁解决多线程数据混乱
```
#锁对象
lock = threading.Lock()

num = 0
def run(n):
    global num

    for i in range(10000000):
        # 锁
        # 确保了这段代码只能由一个线程从头到尾的完整执行
        # 阻止了多线程的并发执行，包含锁的某段代码实际上只能以单线程模式执行，所以效率大大滴降低了
        # 由于可以存在多个锁，不同线程持有不同的锁，并试图获取其他的锁，可能造成死锁，导致多个线程挂起。只能靠操作系统强制终止
        '''
        lock.acquire()
        try:
            num = num + n    #  15 = 9 + 6
            num = num - n    #  9
        finally:
            #修改完一定要释放锁
            lock.release()
        '''

        #与上面代码功能相同，with lock可以自动上锁与解锁
        with lock:
            num = num + n
            num = num - n

if __name__ == "__main__":
    t1 = threading.Thread(target=run, args=(6,))
    t2 = threading.Thread(target=run, args=(9,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print("num =",num)
```
##### (3)ThreadLocal解决多线程数据混乱
ThreadLocal 主要用来为各个线程管理其内部数据，它本身是一个全局变量，但是每个线程却可以利用它来保存属于自己的私有数据，这些私有数据对其他线程也是不可见的。
```
import threading

num = 0
#创建一个全局的ThreadLocal对象
#每个线程有独立的存储空间
#每个线程对ThreadLocal对象都可以读写，但是互不影响
local = threading.local()

def run(x, n):
    x = x + n
    x = x - n

def func(n):
    #每个线程都有local.x，就是线程的局部变量
    local.x = num
    for i in range(1000000):
        run(local.x, n)
    print("%s-%d"%(threading.current_thread().name, local.x))

if __name__ == "__main__":
    t1 = threading.Thread(target=func, args=(6,))
    t2 = threading.Thread(target=func, args=(9,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    print("num =",num)

```



# 十二.Python文件操作

### 1.Python读取文件 
```
f = open('file.txt','r',encoding='utf-8')
data = f.read()#一次性读取文件的全部内容
#f.readline(n)#最多读取n个字节的内容
#f.readlines()#一次读取文件的全部内容，并按行返回list
print(data)
```
权限说明:
符 | 说明
--|--
| r	| 以只读方式打开文件。文件的指针将会放在文件的开头。这是默认模式。 |
| rb	|以二进制格式打开一个文件用于只读。文件指针将会放在文件的开头。这是默认模式。 |
| r+	|打开一个文件用于读写。文件指针将会放在文件的开头。 |
| rb+	|以二进制格式打开一个文件用于读写。文件指针将会放在文件的开头。 |
| w	|打开一个文件只用于写入。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。 |
| wb	|以二进制格式打开一个文件只用于写入。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。 |
| w+	|打开一个文件用于读写。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。 |
| wb+	|以二进制格式打开一个文件用于读写。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。 |
| a	|打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。 |
| ab	|以二进制格式打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。 |
| a+	|打开一个文件用于读写。如果该文件已存在，文件指针将会放在文件的结尾。文件打开时会是追加模式。如果该文件不存在，创建新文件用于读写。 |
| ab+	|以二进制格式打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。如果该文件不存在，创建新文件用于读写。 |


### 2.Python写入文件
```
#覆盖内容
f = open('file.txt2','w',encoding='utf-8') #文件句柄,使用w时事实上是创建了一个新文件，如果源文件存在，会覆盖
f.write("新文件") 
#追加内容
f = open('file.txt2','a',encoding='utf-8') #文件句柄
f.write("See you,tomorrow!")
f_new.close()#关闭文件流
```


### 3.with open方法打开文件
因实际开发过程中，打开文件很容易忘记关闭文件，造成内存不能释放，所以一般可以选择使用with open方法打开文件:
```
with open("test.txt","r",encoding="utf-8") as f:
    print(f.read())
```