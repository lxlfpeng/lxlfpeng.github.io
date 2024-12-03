---
title: Python使用Pyinstaller将源代码打包成exe可执行文件
---

# Pyinstaller简介
PyInstaller是Python的第三方打包库，它能够在Windows、Linux、 Mac OS X 等操作系统下将 Python 源文件进行打包，通过对源文件打包，
实现将.py扩展名的任何Python的源代码转换成Windows、Linux、Mac OS X下的可执行文件，这样 Python 程序可以在没有安装 Python 的环境中运行。
对于Windows来讲，PyInstaller可以将Python源代码打包成.exe的可执行文件，样就可以直接运行程序，不需要安装Python解释器，也不需要对计算机进行相关的环境配置。
需要注意的一点是虽然PyInstaller可以在Windows、Mac OS X和Linux上使用，但是并不是跨平台的，如果希望将python源代码打包成.exe文件，
需要在Windows系统上运行PyInstaller进行打包工作；需要打包成mac app，则需要在Mac OS上使用PyInstaller进行打包。

# 使用Pyinstaller打包exe文件

## 安装Pyinstaller模块
```
pip install pyinstaller
```
如果比较慢可以用清华源下载:
```
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pyinstaller
```

## Pyinstaller简单打包命令
如果工程里中只有.py文件，即Python代码文件，不包括视频、图片、文件等资源文件，那么使用pyinstaller打包是非常简单的，只需要下面一行命令即可：
```
pyinstaller -F test.py
```
运行完上面的命令，pyinstaller会将python源码及第三方依赖进行打包，打包结束以后会在当前目录下生成一个``test.spec``文件和两个文件夹:``build``和``dist``，其中dist里面就是最终生成的exe文件，点击.exe文件就可以执行用python写好的程序。 如果点击执行exe文件时，
控制台界面一闪而过，那么很可能代码执行完成毕导致控制台退出了，此时可以在python源代码中使用``input('Press Enter to exit…')``将线程卡住再打包运行方便查看调试信息。
通过上面的命令打包出来exe文件并没有图标，可以在打包时给exe指定图标，首先将准备好的``text_icon.icon``图标放置到项目根目录中，然后执行如下打包命令:
```
#目前该命令只在windows下生效
pyinstaller -F -i text_icon.ico test.py
```
每次执行打包好的exe文件都会出现一个控制台窗口，对于命令行程序调试这非常有用，但是如果是GUI程序中是不需要这个的，因此可以在打包时通过如下命令去掉控制台窗口:
```
pyinstaller -F -w -i text_icon.ico test.py
```

在上文中通过将python打包成单个可执行的exe文件时，会将依赖的库包等集成在一起形成一个文件，如果项目使用的依赖比较多的时候往往打包出来exe会很大，这样会导致启动较慢。因此可以将源代码打包成多文件的方式:
```
pyinstaller -D test.py
```
打包成功以后在dist目录会生成很多依赖文件，也就是把将exe和dll等分开了，找到对应的.exe启动文件则可以进行启动打包好的程序。打包多文件虽然可以增加启动速度，但也会导致其他信息被暴露出来。因此选择打包单个文件好还是多个文件需要视情况而定。

## Pyinstaller打包常用参数
除了上文种使用到的比较简单的打包参数，使用pyinstaller的参数还有如下这些:
| 参数 | 参数意义|                                                                                                                                                                                                          
|- | - |
| **-F <br> --onefile**                  |打包单个文件，产生一个文件用于部署|
| **-D<br> --onedir**                    |打包多个文件，产生一个目录用于部署(默认)|
| **--key=keys**                         |使用keys进行加密打包例：pyinstaller --key=1234 -F xx.py|
| **-K<br> --tk**                        |在部署时包含 TCL/TK    |
| **-a<br> --ascii**                     |不包含编码.在支持Unicode的python版本上默认包含所有的编码|
| **-d<br> --debug**                     |产生debug版本的可执行文件|
| **-n name <br> --name=name**           |可选的项目(产生的spec的)名字name|
| **-o dir <br> --out=dir**              |指定spec文件的生成目录dir如果没有指定切当前目录不是PyInstaller的根目录，则会输出到当前的目录下|
| **-p dir <br> --path=dir**             |用来添加程序所用到的包的所在位置，让Pyintaller自己去找程序需要的资源 |
| **-w<br> --windowed<br> --noconsole**  |表示去掉控制台窗口，使用Windows子系统执行，当程序启动的时候不会打开命令行(只对Windows有效)|
| **-c <br> --nowindowed <br> --console**|表示打开控制台窗口，使用控制台子系统执行，当程序启动的时候会打开命令行(默认)(只对Windows有效)|
| **-i<br> --icon==<file.ioc>**          |将file.ico添加为可执行文件的资源，改变程序的图标(只对Windows系统有效)|
| **--icon==<file.ioc>**                 |将file.exe的第n个图标添加为可执行文件的资源(只对Windows系统有效)|                                                                                                                                              
| **-v file<br> --version=file**         |将verfile作为可执行文件的版本资源(只对Windows系统有效)|                                                                                                                                                           
| **-s<br> --strip**                     |可执行文件和共享库将run through strip.注意Cygwin的strip往往使普通的win32 Dll无法使用|                                                                                                                 |
| **-X<br> --upx**                       |如果有UPX安装(执行Configure.py时检测)，会压缩执行文件(Windows系统中的DLL也会)(参见note)|

## Pyinstaller使用spec文件进行打包
通过上文中已知pyinstaller打包时有很多控制选项，可以通过打包命令行加上对应的参数进行打包。这种方式用来打简单的包还是比较好用的，但是用来打比较复杂的工程的包就会比较麻烦。因此，Pyinstaller
还给我们提供了.spec 配置文件来对打包参数进行配置。通过Spec文件指定这些打包参数选项，这样不需要每次通过命令控制选项了，效果上二者是等效的。spec文件会告诉pyinstaller打包时，如何处理被打包脚本，
且spec文件实际上是可执行的python代码。使用spec文件打包步骤如下:

#### 1.创建spec文件
直接通过输入如下命令后回车:
```
pyi-makespec -F -w -i favicon.ico test.py
```
其中``pyi-makespec``会生成一个test.spec文件（用于指定打包的配置）。
也可以通过打包命令:
```
pyinstaller -F -w -i favicon.ico test.py
```
程序打包结束后，发现当前目录下生成两个文件夹（bulid、dist）和一个文件test.spec（用于指定打包的配置）。

#### 2.根据自己的项目编辑spec文件
根据上文中默认生成的spec文件，可以通过修改spec文件的配置参数来实现不同的打包配置，每个参数表示的含义:
```
# -*- mode: python ; coding: utf-8 -*-


block_cipher = None  #设置 加密，需要安装tinyaes第三方库，最多16位字符，此处在使用--key= 会有变化


a = Analysis(
    ['test.py'],  # 运行的所有py文件，包括依赖的py文件 
    pathex=[],  # 搜索导入的路径列表（此列表为项目绝对路径)，包括选项给出的路径--paths，项目需要从什么地方导入自定义库
    binaries=[],  # 脚本需要的非python模块，包括--add-binary选项给出的名称，二进制数据
    datas=[],  # 应用程序中包含的非二进制文件，包括--add-data选项给出的名称，项目需要用到什么数据，比如图片，视频等。里面格式为tuple，第一个参数是文件路径，第二个是打包后所在的路径，其为一个元组：('image/*.png','data/image')
    hiddenimports=[],   # 假如打包后打开exe显示module not found，就要把该库添加到hiddenimports里面了
    hookspath=[],  
    hooksconfig={},  # 挂钩配置选项由一个字典组成
    runtime_hooks=[],  
    excludes=[],  # 假如你用的python有很多库，但是你不需要用到某个，那么就把它添加到里面去，可以压缩文件大小
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,  # 打包成EXE的脚本文件
    # a.binaries,  # 如果是单文件模式，则需要添加；多文件也可以添加
   	# a.zipfiles,
    # a.datas,
    [],
    exclude_binaries=True,  # 是否排除二进制文件，为True时，为排除二进制的文件，当文件交大时包含二进制文件运行较快，如果是单文件，则没有这个选项
    name='main',  # 打包程序的名字
    debug=False,  # 是否启用调试功能
    bootloader_ignore_signals=False,
    # runtime_tmpdir=None,  # 生成单文件时需要这个参数，定义运行时的临时文件夹
    strip=False,
    upx=True,  # 打包的时候进行压缩，False表示不压缩；要用到一个压缩程序UPX，用于压缩文件，需要单独下载
    console=True,  # 打包后的可执行文件双击运行时屏幕会出现一个cmd窗口，不影响原程序运行，等于是是否加-w参数
    disable_windowed_traceback=False,  
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    
    """添加选项，初始化时没有的"""
    icon="",  # 指定应用程序的图标，传入路径，可以相对路径
    
)
coll = COLLECT(
    """
    如果是单文件模式，不需要这个COLLECT类，同时需要将：
        a.binaries,
    	a.zipfiles,
    	a.datas,
    这些数据文件添加到EXE中
    """
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)

```

#### 3.使用pec文件进行打包
使用pec文件进行打包非常简单，命令如下:
```
pyinstaller test.spec
```
至此，打包结束。

## Pyinstaller打包资源文件
在上文中打包的python项目都是不带有音视频、文本等资源文件的，有时候我们的工程除了python文件之外还包括一些外部资源文件，如图片、配置文件等，例如在tools目录中有一个setting.json的配置文件，我们需要在 test_pyinstaller中需要读取这个配置文件，结构目录:
│─test_pyinstaller.py
└─tools
  └─setting.json

test_pyinstaller.py的代码为:
```
import json
import os
#获取配置文件路径
path = os.path.join("tools", "setting.json")
#加载配置文件
setting_file = open(path, encoding="utf-8")
setting_json=json.load(setting_file)
print("读取到的配置文件为:",setting_json)
```
这段代码在本地直接是可以运行的，但是将它通过``pyinstaller -F test_pyinstaller.py``打包成.exe文件以后，运行会报错。因为普通的打包方式并没有没有将setting.json资源文件打包到.exe文件中去。Pyinstaller给我们
提供了两种方式将资源文件打包到.exe文件中去。也就是上文说的通过命令行添加参数的的方式或者通过编辑.spec配置文件添加参数的方式进行打包。


#### 方式一:通过命令行添加参数的的方式
可以通过--add-data将``C:\Users\WIN10\Desktop\pyinstaller\tools``目录打包到目标exe中的根目录的tools目录下
```
pyinstaller -F test_pyinstaller.py --add-data "C:\Users\WIN10\Desktop\pyinstaller\tools;./tools"
```
当然也可以使用相对路径:
```
pyinstaller -F test_pyinstaller.py --add-data "./tools;./tools"
```
将当前工程目录下的tools目录，打包到目标exe中的根目录的tools目录下。

#### 方式二:通过编辑.spec配置文件方式(推荐)
```
省略部分....
a = Analysis(['test_pyinstaller.py'],
             pathex=[],
             binaries=[],
             datas=[('tools','tools')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

省略部分....
```
注意**binaries**和**datas**这两个的值，binaries接收一个元组表示将二进制文件（如.exe/.dll/.so等）打包到.exe文件中，比如``binaries=[('ci64.dll','.'),('ABDLL64.dll','.')]``。
datas接收一个元组表示将非二进制文件（如图片文件、文本文件等）打包到.exe文件中，例如：``datas=[('tools','tools’)]``。
其中元组第一个参数表示需要被打包的文件/目录路径，第二个表示打包到.exe程序中的文件/目录路径，可以枚举一个或多个。例如:
```
#下面表示将./lib/general.xml拷贝到./data文件夹下
datas=[('./lib/general.xml',r'./data')],

#还可以整个文件夹的拷贝，或者一类文件的拷贝。如下设置了多个规则的
datas= [( '/media/data', 'data' ),#/media/data文件夹下所有文件打包到data目录中
        ('/media/music/*.mp3', 'music' ) ,#将/media/music/目录中所有mp3,打包到music目录中
		( 'src/README.txt', '.' ),#将src/README.txt文件,打包到根目录中
		],
```

#### python文件路径修改
通过选择上文两种方式中的一种，就已经将资源文件打包到.exe文件种去了，此时如果使用``pyinstaller -D``打包的程序目录，可以在dist里面找到打包到里面的资源文件,程序也是可以直接运行的。
但是如果是通过``pyinstaller -F``打包的.exe单文件，此时如果执行程序会报找不到setting.json的错误。其原因就是单Exe中增加了一个类似于代理或boot的程序段，Exe运行后，会将python、第三方库、资源文件等东西解压到一个临时文件夹中，
脚本运行完毕，会丢弃临时文件。临时文件夹的路径会随着每次运行而更改，但对其位置的引用会添加到sys._MEIPASS中。程序可通过sys._MEIPASS访问临时文件夹中的资源。
然而我们在python代码中使用了相对路径去读取文件，当然就会读取不到了，因此需要在python文件种对路径进行转换。在python文件对代码中的路径进行转换处理，
当打包成exe文件时py程序里面的路径要从./xxx/yy(相对路径)换成xxx/yy (绝对路径)并且进行路径转换但如果不打包资源文件的话 最好路径还是用作./xxx/yy 并且不进行路径转换 ，修改test_pyinstaller.py代码为:
```
import json
import os
import sys
#生成资源文件目录访问路径
def resource_path(relative_path):
    if getattr(sys, 'frozen', False): #是否Bundle Resource 捆绑资源
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


#获取配置文件路径
path = resource_path(os.path.join("tools", "setting.json"))
#加载配置文件
setting_file = open(path, encoding="utf-8")
setting_json=json.load(setting_file)
print("读取到的配置文件为:",setting_json)
```
此时再打包，运行就可以获取到正确得配置文件了。

# 参考
[pyinstaller官网](http://www.pyinstaller.org/)
[pyinstaller官方帮助文档](https://pyinstaller.readthedocs.io/en/stable/)
[2个技巧，学会Pyinstaller打包的高级用法](https://juejin.cn/post/6973214749437722638)
[python使用pyinstaller打包python程序](https://blog.csdn.net/kevinshift/article/details/104880101)