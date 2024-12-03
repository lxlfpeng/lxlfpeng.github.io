---
title: 使用Shell脚本助力Linux系统自动化
---

# 一.Shell和Shell脚本
### 1.什么是Shell程序
对于图形界面例如(Windows,Ios,Android)，用户点击某个图标就能启动某个程序；对于命令行，用户输入某个程序的名字（可以看做一个命令）就能启动某个程序。这两者的基本过程都是类似的，都需要查找程序在硬盘上的安装位置，然后将它们加载到内存运行。
也就是说图形界面和命令行要达到的目的是一样的，都是让用户控制计算机。真正能够控制计算机硬件（CPU、内存、显示器等）的只有操作系统内核（Kernel）， 图形界面和命令行只是架设在用户和内核之间的一座桥梁。由于安全、复杂、繁琐等原因，
用户不能直接接触内核（也没有必要），需要另外再开发一个程序，让用户直接使用这个程序； 该程序的作用就是接收用户的操作（点击图标、输入命令），并进行简单的处理，然后再传递给内核。如此一来，用户和内核之间就多了一层“代理”，这层“代理”既简化了用户的操作，也保护了内核。
用户界面和命令行就是这个另外开发的程序，就是这层“代理”。在Linux下，这个命令行程序叫做 Shell。

Shell 除了能解释用户输入的命令，将它传递给内核，还可以：
- 调用其他程序，给其他程序传递数据或参数，并获取程序的处理结果；
- 在多个程序之间传递数据，把一个程序的输出作为另一个程序的输入；
- Shell 本身也可以被其他程序调用。

**由此可见，Shell 是将内核、程序和用户连接了起来。**

Shell 本身支持的命令并不多，但是它可以调用其他的程序，每个程序就是一个命令，这使得 Shell 命令的数量可以无限扩展，其结果就是 Shell 的功能非常强大，完全能够胜任 Linux 的日常管理工作， 如文本或字符串检索、文件的查找或创建、大规模软件的自动部署、更改系统设置、监控服务器性能、发送报警邮件、抓取网页内容、压缩文件等。

``Shell 并不是简单的堆砌命令，我们还可以在 Shell 中编程，这和使用 C/C++、Java、Python 等常见的编程语言并没有什么两样。``

Shell 虽然没有 C/C++、Java、Python 等强大，但也支持了基本的编程元素，例如：
- if...else 选择结构，switch...case 开关语句，for、while、until 循环；
- 变量、数组、字符串、注释、加减乘除、逻辑运算等概念；
- 函数，包括用户自定义的函数和内置函数（例如 printf、export、eval 等）。

站在这个角度讲，Shell 也是一种编程语言，它的编译器（解释器）是 Shell 这个程序。平时所说的 Shell，有时候是指连接用户和内核的这个程序，有时候又是指 Shell 编程。

[](https://img2020.cnblogs.com/blog/1740019/202011/1740019-20201116152628353-920362972.png)

>Shell 主要用来开发一些实用的、自动化的小工具，而不是用来开发具有复杂业务逻辑的中大型软件，例如检测计算机的硬件参数、一键搭建Web开发环境、日志分析等，Shell 都非常合适。

### 2.Shell程序的种类
常见的 Shell 有 ``sh、bash、csh、tcsh、ash`` 等。
##### (1.)sh程序
sh 的全称是 Bourne shell，由 AT&T 公司的 Steve Bourne开发，为了纪念他，就用他的名字命名了。 sh 是 UNIX 上的标准 shell，很多 UNIX 版本都配有 sh。sh 是第一个流行的 Shell。
##### (2.)bash程序
bash shell 是 Linux 的默认 shell，本教程也基于 bash 编写。 bash 由 GNU 组织开发，保持了对 sh shell 的兼容性，是各种 Linux 发行版默认配置的 shell。 bash 兼容 sh 意味着，针对 sh 编写的 Shell 代码可以不加修改地在 bash 中运行。
尽管如此，bash 和 sh 还是有一些不同之处：
- 一方面，bash 扩展了一些命令和参数；
- 另一方面，bash 并不完全和 sh 兼容，它们有些行为并不一致，但在大多数企业运维的情况下区别不大，特殊场景可以使用 bash 代替 sh。

**Shell 是一个程序，一般都是放在/bin或者/user/bin目录下，当前 Linux 系统可用的 Shell 都记录在/etc/shells文件中。/etc/shells是一个纯文本文件，你可以在图形界面下打开它，也可以使用 cat 命令查看它。**

通过 cat 命令来查看当前 Linux 系统的可用 Shell：
```
$ cat /etc/shells
/bin/sh
/bin/bash
/sbin/nologin
/usr/bin/sh
/usr/bin/bash
/usr/sbin/nologin
/bin/tcsh
/bin/csh
```
在现代的 Linux 上，sh 已经被 bash 代替，/bin/sh往往是指向/bin/bash的符号链接。

查看当前 Linux 的默认 Shell，那么可以输出 SHELL 环境变量：
```
$ echo $SHELL
/bin/bash
```
输出结果表明默认的 Shell 是 bash。通常用户登录成功后执行的shell程序为：/bin/bash

### 3.Shell脚本
任何代码最终都要被“翻译”成二进制的形式才能在计算机中执行。 有的编程语言，如 C/C++、Pascal、Go语言、汇编等，必须在程序运行之前将所有代码都翻译成二进制形式，也就是生成可执行文件，
用户拿到的是最终生成的可执行文件，看不到源码。 这个过程叫做编译（Compile），这样的编程语言叫做编译型语言，完成编译过程的软件叫做编译器（Compiler）。 而有的编程语言，如 Shell、
JavaScript、Python、PHP等，需要一边执行一边翻译，不会生成任何可执行文件，用户必须拿到源码才能运行程序。程序运行后会即时翻译，翻译完一部分执行一部分，不用等到所有代码都翻译完。
这个过程叫做解释，这样的编程语言叫做解释型语言或者脚本语言（Script），完成解释过程的软件叫做解释器。 编译型语言的优点是执行速度快、对硬件要求低、保密性好，适合开发操作系统、大型应用程序、
数据库等。脚本语言的优点是使用灵活、部署容易、跨平台性好，非常适合Web开发以及小工具的制作。 Shell 就是一种脚本语言，我们编写完源码后不用编译，直接运行源码即可。

Shell的作用是解释执行用户的命令，用户输入一条命令，Shell就解释执行一条，这种方式称为交互式（Interactive），Shell还有一种执行命令的方式称为批处理（Batch），
用户事先写一个Shell脚本（Script），其中有很多条命令，让Shell一次把这些命令执行完，而不必一条一条地敲命令。Shell脚本和编程语言很相似，也有变量和流程控制语句，
但Shell脚本是解释执行的，不需要编译，Shell程序从脚本中一行一行读取并执行这些命令，相当于一个用户把脚本中的命令一行一行敲到Shell提示符下执行。

shell程序例如bash的本质就是一个解释器，shell本身就是一门解释型、弱类型、动态语言，与python相对应，Python属于解释型、动态语言，
平时登录成功一个用户后进入的就是bash解释器的交互式环境，我们敲的命令其实都属于shell这门语言的语法
[](https://img2020.cnblogs.com/blog/1740019/202011/1740019-20201116152656622-2105686077.png)

### 4.进入Shell程序
##### (1.)进入 Linux 控制台
一种进入Shell 的方法是让 Linux 系统退出图形界面模式，进入控制台模式，这样一来，显示器上只有一个简单的带着白色文字的“黑屏”，就像图形界面出现之前的样子。这种模式称为 Linux 控制台（Console）。
##### (2.)使用终端进入Shell程序
进入 Shell 的另外一种方法是使用 Linux 桌面环境中的终端模拟包（Terminal emulation package），也就是我们常说的终端（Terminal），这样在图形桌面中就可以使用 Shell。
##### (3.)Shell程序提示符（$和#的区别）
启动终端模拟包或者从 Linux 控制台登录后，便可以看到 Shell 提示符。提示符是通往 Shell 的大门，是输入 Shell 命令的地方。
对于普通用户，Base shell 默认的提示符是美元符号$；对于超级用户（root 用户），Bash Shell 默认的提示符是井号#。该符号表示 Shell 等待输入命令。
不同的 Linux 发行版使用的提示符格式不同。例如在 CentOS 中，默认的提示符格式为：
```
[zhangsan@localhost ~]$
```
这种格式包含了以下三个方面的信息：
- 启动 Shell 的用户名，也即 zhangsan；
- 本地主机名称，也即 localhost；
- 当前目录，波浪号~是主目录的简写表示法。

### 5.第一个Shell脚本
新建一个文件，扩展名为sh（sh代表shell）.Shell脚本通常都是以.sh 为后缀名的，这个并不是说不带.sh这个脚本就不能执行，只是大家的一个习惯而已。所以，以后你发现了.sh为后缀的文件那么它一定会是一个shell脚本了。
```
#!/bin/bash
echo "Hello World !"
```
“#!” 是一个约定的标记，它告诉系统这个脚本需要什么解释器来执行，即使用哪一种Shell。echo命令用于向窗口输出文本。 

### 6.执行Shell脚本
##### (1.)作为可执行程序执行Shell脚本
将上面的代码保存为test.sh，并 cd 到相应目录：
```
chmod +x test.sh  #使脚本具有执行权限,执行之前首先要为脚本文件添加可执行权限，不然就得用root权限才能执行！
./test.sh  #执行脚本
```
注意，一定要写成./test.sh，而不是test.sh。运行其它二进制的程序也一样，直接写test.sh，linux系统会去PATH里寻找有没有叫test.sh的，而只有/bin, /sbin, /usr/bin，/usr/sbin等在PATH里，你的当前目录通常不在PATH里，所以写成test.sh是会找不到命令的，要用./test.sh告诉系统说，就在当前目录找。
通过这种方式运行bash脚本，第一行一定要写对，好让系统查找到正确的解释器。
这里的"系统"，其实就是shell这个应用程序（想象一下Windows Explorer），是方便理解，既然这个系统就是指shell，那么一个使用/bin/sh作为解释器的脚本可以可以省去第一行。
##### (2.)作为解释器参数执行Shell脚本
这种运行方式是，直接运行解释器，其参数就是shell脚本的文件名，如：
```
/bin/sh test.sh
```
它默认使用/bin/sh所指向的shell解释器来执行脚本文件，前提是脚本文件中未指定解释器。但如果在脚本文件中指定了使用哪种脚本解释器，那么它就不管/bin/sh指向哪个脚本解释器，而是使用脚本文件中所制定的那个脚本解释器。
##### (3.)脚本绝对路径执行执行Shell脚本
指定脚本文件的绝对路径，即可执行
```
 /home/xxx/shellStudy/test.sh  
```

### 7.传递参数给Shell脚本
运行脚本时传递给脚本的参数称为命令行参数。命令行参数用 $n 表示，例如，$1 表示第一个参数，$2 表示第二个参数，依次类推。
以下实例我们向脚本传递三个参数，并分别输出，其中 $0 为执行的文件名（包含文件路径）：

实例
```
#!/bin/bash
# author:菜鸟教程
# url:www.runoob.com

echo "Shell 传递参数实例！";
echo "执行的文件名：$0";
echo "第一个参数为：$1";
echo "第二个参数为：$2";
echo "第三个参数为：$3";
```
为脚本设置可执行权限，并执行脚本，输出结果如下所示：
```
$ chmod +x test.sh 
$ ./test.sh zhangsan lisi wangwu
Shell 传递参数实例！
执行的文件名：./test.sh
第一个参数为：zhangsan
第二个参数为：lisi
第三个参数为：wangwu
另外，还有几个特殊字符用来处理参数：
```
>运行脚本时传递给脚本的参数称为命令行参数。命令行参数用 $n 表示，例如，$1 表示第一个参数，$2 表示第二个参数，依次类推。

# 二.Shelle脚本的变量
在 Bash shell 中，每一个变量的值都是字符串，无论你给变量赋值时有没有使用引号，值都会以字符串的形式存储。 这意味着，Bash shell 在默认情况下不会区分变量类型，即使你将整数和小数赋值给变量，它们也会被视为字符串，这一点和大部分的编程语言不同。
如果你写了一个长达1000行的shell脚本，并且脚本中出现了某一个命令或者路径几百次。突然你觉得路径不对想换一下，那岂不是要更改几百次？你固然可以使用批量替换的命令，但是也是很麻烦，并且脚本显得臃肿了很多。变量的作用就是用来解决这个问题的。
### 1.定义变量
Shell 支持以下三种定义变量的方式：
```
variable=value
variable='value'
variable="value"
```
variable 是变量名，value 是赋给变量的值。如果 value 不包含任何空白符（例如空格、Tab缩进等），那么可以不使用引号；如果 value 包含了空白符，那么就必须使用引号包围起来。
>注意，赋值号的周围不能有空格

hell 变量的命名规范和大部分编程语言都一样：
- 变量名由数字、字母、下划线组成；
- 必须以字母或者下划线开头；
- 不能使用 Shell 里的关键字（通过 help 命令可以查看保留关键字）。

### 2.使用变量
使用一个定义过的变量，只要在变量名前面加美元符号$即可，如：
```
name="zhangsan"
echo $name
echo ${name}
```
变量名外面的花括号{ }是可选的，加不加都行，加花括号是为了帮助解释器识别变量的边界，比如下面这种情况：
```
skill="Java"
echo "I am good at ${skill}Script"
```
如果不给 skill 变量加花括号，写成echo "I am good at $skillScript"，解释器就会把 $skillScript 当成一个变量（其值为空），代码执行结果就不是我们期望的样子了。
>推荐给所有变量加上花括号{ }，这是个良好的编程习惯。

### 3.修改变量的值
已定义的变量，可以被重新赋值，如：
```
name="zhangsna"
echo ${name}
name="lisi"
echo ${lisi}
```
第二次对变量赋值时不能在变量名前加$，只有在使用变量时才能加$。

### 4.将命令的结果赋值给变量
Shell 也支持将命令的执行结果赋值给变量
例如，我在 code 目录中创建了一个名为 log.txt 的文本文件，用来记录我的日常工作。下面的代码中，使用 cat 命令将 log.txt 的内容读取出来，并赋值给一个变量，然后使用 echo 命令输出。
```
log=$(cat log.txt)
echo $log
```

### 5.只读变量
使用 readonly 命令可以将变量定义为只读变量，只读变量的值不能被改变。 
下面的例子尝试更改只读变量，结果报错：
```
#!/bin/bash
name="zhangsan"
readonly name
name="lisi"
```
运行脚本，结果如下：
```
/bin/sh: NAME: This variable is read only.
```

### 6.删除变量
使用 unset 命令可以删除变量。语法：
```
unset variable_name
```
变量被删除后不能再次使用；unset 命令不能删除只读变量。
举个例子：
```
#!/bin/sh
name="zhangsan"
unset name
echo name
上面的脚本没有任何输出。
```

### 7.变量作用域
运行shell时，会同时存在三种变量：
##### (1.)局部变量
局部变量在脚本或命令中定义，仅在当前shell实例中有效，其他shell启动的程序不能访问局部变量。
##### (2.)环境变量
所有的程序，包括shell启动的程序，都能访问环境变量，有些程序需要环境变量来保证其正常运行。必要的时候shell脚本也可以定义环境变量。
##### (3.)shell变量
shell变量是由shell程序设置的特殊变量。shell变量中有一部分是环境变量，有一部分是局部变量，这些变量保证了shell的正常运行。

# 三.Shell脚本的数组
bash支持一维数组, 不支持多维数组, 它的下标从0开始编号. 用下标[n] 获取数组元素；
### 1.定义数组
在shell中用括号表示数组，元素用空格分开。 如：
```
array_name=(value0 value1 value2 value3)
```
也可以单独定义数组的各个分量，可以不使用连续的下标，而且下标的范围没有限制。如：
```
array_name[0]=value0
array_name[1]=value1
array_name[2]=value2
```

### 2.读取数组
读取某个下标的元素一般格式为:
```
${array_name[index]}
```
读取数组的全部元素，用@或*
```
${array_name[*]}
${array_name[@]}
```

### 3.获取数组的信息
取得数组元素的个数：
```
length=${#array_name[@]}
#或
length=${#array_name[*]}
```
获取数组的下标：
```
length=${!array_name[@]}
#或
length=${!array_name[*]}
```
取得数组单个元素的长度:
```
arr_length=${#array_name[n]}
```

# 四.Shell脚本的流程控制
### 1.Shell if else语句
```
if [ 表达式 ] then  语句  fi

if [ 表达式 ] then 语句 else 语句 fi

if [ 表达式] then 语句  elif[ 表达式 ] then 语句 elif[ 表达式 ] then 语句   …… fi
```
例子：
```
a=10
b=20
if [ $a == $b ]
then
echo "a is equal to b"
else
echo "a is not equal to b"
fi
```
另外：if ... else 语句也可以写成一行，以命令的方式来运行，像这样：
```
if test $[2*3] -eq $[1+5]; then echo 'The two numbers are equal!'; fi;
```
其中，test 命令用于检查某个条件是否成立，与方括号([ ])类似。

### 2.Shell case esac语句
case ... esac 与其他语言中的 switch ... case 语句类似，是一种多分枝选择结构。case语句格式如下：
```
case 值 in
模式1)
command1
command2
command3
;;
模式2）
command1
command2
command3
;;
*)
command1
command2
command3
;;
esac
```
1. 取值后面必须为关键字 in，每一模式必须以右括号结束。取值可以为变量或常数。匹配发现取值符合某一模式后，其间所有命令开始执行直至 ;;。;; 与其他语言中的 break 类似，意思是跳到整个 case 语句的最后。
2. 如果无一匹配模式，使用星号 * 捕获该值，再执行后面的命令。

# 五.Shell脚本的循环语句
### 1.Shell脚本for循环
一般格式为：
```
for 变量 in 列表
do
command1
command2
...
commandN
done
```
>注意：列表是一组值（数字、字符串等）组成的序列，每个值通过空格分隔。每循环一次，就将列表中的下一个值赋给变量。     
顺序输出当前列表的数字：
```
for loop in 1 2 3 4 5
do
echo "The value is: $loop"
done
```
显示主目录下以 .bash 开头的文件：
```
#!/bin/bash
for FILE in $HOME/.bash*
do
echo $FILE
done
```

### 2.Shell脚本while循环
一般格式为：
```
while command
do
Statement(s) to be executed if command is true
done
```
例如：
```
COUNTER=0
while [ $COUNTER -lt 5 ]
do
COUNTER='expr $COUNTER+1'
echo $COUNTER
done
```

### 3.Shell脚本until循环
until 循环执行一系列命令直至条件为 true 时停止。until 循环与 while 循环在处理方式上刚好相反。
```
until command
do
Statement(s) to be executed until command is true
done
```
>command 一般为条件表达式，如果返回值为 false，则继续执行循环体内的语句，否则跳出循环。类似地， 在循环中使用 break 与continue 跳出循环。另外，break 命令后面还可以跟一个整数，表示跳出第几层循环。

# 六.Shell脚本的函数
格式：
```
[function] funcName()
{undefined
语句
[return 返回值]
}
```
返回值是可选的，如果没有显示return 则默认返回最后一条语句执行的结果。 Shell 函数返回值只能是整数，一般用来表示函数执行成功与否，0表示成功，其他值表示失败。如果 return 其他数据，比如一个字符串，往往会得到错误提示：“numeric argument required”。
如果一定要让函数返回字符串，那么可以先定义一个变量，用来接收函数的计算结果，脚本在需要的时候访问这个变量来获得函数返回值。 函数参数从$1到$n，$0 是文件名。
例子：
```
#!/bin/bash

#打印数字
printNum()
{
echo $1
}

for i in `seq 2 8` #seq是一个命令，顺序生成一串数字或者字符
do
printNum $i
done
```

# 七.Shell脚本的文件包含
Shell 中包含脚本可以使用：
```
. filename
```
或
```
source filename
```
两种方式的效果相同，简单起见，一般使用点号(.)，但是注意点号(.)和文件名中间有一空格。

例如，创建两个脚本，一个是被调用脚本 subscript.sh，内容如下：
```
url="hello word"
```
一个是主文件 main.sh，内容如下：
```
#!/bin/bash
. ./subscript.sh
echo $url
```
执行脚本：
```
$chomd +x main.sh
./main.sh
hello word
$
```
>注意：被包含脚本不需要有执行权限。

参考资料:
[Shell教程](http://c.biancheng.net/cpp/view/6994.html)