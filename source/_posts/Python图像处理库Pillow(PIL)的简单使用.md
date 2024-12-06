---
title: Python图像处理库Pillow(PIL)的简单使用
date: 2020-11-16
categories: 
  - Python开发
---

# 一.PIL和Pillow图像处理库
图像库PIL(Python Image Library)是Python的第三方图像处理库，但是由于其强大的功能与众多的使用人数，几乎已经被认为是python官方图像处理库了。PIL原来是只支持python2的版本，后来出现了移植到python3的库pillow，pillow其功能和PIL差不多。 PIL 软件包提供了基本的图像处理功能，如：改变图像大小，旋转图像，图像格式转换，色场空间转换，图像增强，直方图处理，插值和滤波等等。

# 二.安装Pillow
Pillow 的安装非常简单，不过需要注意 Pillow 和 PIL 不能共存在相同的环境中，因此在安装 Pillow 之前，先要卸载 PIL。命令行下通过 pip 安装：
```
pip install pillow
```

安装完成之后，可以在 Python 的开发环境输入以下代码，测试 Pillow 是否安装成功，以及查看相应的版本号。
```
from PIL import Image

print(Image.VERSION)
```
>注意，虽然使用的是 Pillow，但是导入的包依然是 PIL。

# 三.Image类使用
Image是PIL中最重要的模块之一，任何一张图片都可以使用Image对象来表示。 可以通过多种方式来创建 Image 类的实例，比如：从文件中加载图像、处理其它图像或从头开始创建图像。
### 1.使用Image类打开本地图片
要从文件中加载图像创建 Image 类的实例，可以使用 Image 模块的 `open()` 方法。

```
from PIL import Image

img = Image.open(r"./test.jpg")

```
执行成功，`Image.open()` 函数会返回一个 Image 对象。如果图像文件打开错误，则会抛出 OSError 错误。
>注意在使用交互式处理图片文件时，应该使用文件的全路径，如果运行py文件，还是建议采用相对路径。

### 2.使用Image类从URL读取图像
读取网络图形需要配合网络请求工具，通过网络请求工具将图片变成流然后通过Image类进行打开。
```
from PIL importImage
import requests

url ='https://xxxxxx.jpg'
resp = requests.get(url, stream=True).raw
img =Image.open(resp)
img.save('xxxx.jpg','jpeg')
```
>该示例从 URL 读取图像并将其保存在磁盘上。

### 3.使用Image类查看图片信息
通过Image 类的实例可以使用实例的属性来检查文件内容。

```
from PIL import Image
img = Image.open(r"./test.jpg")

print(img.format)
# JPEG
print(img.size)
# (1080, 1920)
print(img.mode)
# RGB
```
* format: 返回图像文件的格式（JPG, PNG, BMP, None, etc.）。用来标识图片的格式或来源，如果图片并不是通过读取文件得到的，那么值就是None。
* size: 返回图像的尺寸。以二元组的形式返回图像的宽度和高度（以像素为单位）；
* mode: 返回图像的色彩模式（L, RGB, CMYK, etc.）。L 为灰度图像，RGB 为真彩色图像，CMYK 为印刷图像；

### 4.使用Image类显示图片
Image 类实例有很多方法，如果想要查看图像，可以使用 `show()` 方法。

```
from PIL import Image
img = Image.open(r"./test.jpg")
img.show()
```
>show() 方法效率不高，因为它会将图像保存到临时文件中，并且调用你电脑中的图像程序来显示图像。如果你的电脑中没有安装显示图像的应用程序，show() 方法甚至不能工作。

### 5.使用Image类保存图片
Pillow 保存一个图像 语法为:
```
Image.save(fp, format=None, **params)
```
- fp - 文件名（字符串）、pathlib.Path对象或文件对象。
- format - 可选的格式重写。如果省略，使用的格式是由文件名扩展名决定的。如果使用文件对象而不是文件名，应该总是使用这个参数。
- options - 图像写入器的额外参数。
- 返回值 - 无
- KeyError - 如果不能从文件名确定输出格式，使用格式选项来解决这个问题。
- IOError - 如果文件不能被写入，文件可能已经被创建，可能包含部分数据。

>注意:保存的时候，如果没有指定图片格式的话，那么Pollow会根据输入的后缀名决定图片的格式。

### 6.Image类常用图片转换功能

##### 获取图片信息
```
from PIL import Image
im = Image.open(r"./test.jpg")
print(im.format)  # JPEG
```
##### 获取大小
```
from PIL import Image
im = Image.open(r"./test.jpg")
print(im.size)  # (960, 626)
```
##### 图像缩放
```
from PIL import Image
im = Image.open(r"./test.jpg")
# 缩放为原来的1/2
im = im.resize((im.size[0] // 2, im.size[1] // 2))
```
##### 图像翻转
```
from PIL import Image
im = Image.open(r"./test.jpg")
# 填入角度，按照逆时针进行翻转
im = im.rotate(90)
```

##### 图像模糊
```
from PIL import Image
im = Image.open(r"./test.jpg")
# 图像模糊
im = im.filter(ImageFilter.BLUR)
```

##### 图像增强（细节突出）
```
from PIL import Image
im = Image.open(r"./test.jpg")
im = im.filter(ImageFilter.DETAIL)
```

##### 图像边缘提取
```
from PIL import Image
im = Image.open(r"./test.jpg")
im = im.filter(ImageFilter.FIND_EDGES)
```

##### 浮雕效果
```
from PIL import Image
im = Image.open(r"./test.jpg")
im = im.filter(ImageFilter.EMBOSS)
```
##### 锐化效果
```
from PIL import Image
im = Image.open(r"./test.jpg")
im = im.filter(ImageFilter.SHARPEN)
```

# 四.Pillow压缩图片大小
### 1.quality 方式
使用PIL模块的 quality方法来进行压缩
```
from PIL import Image
 
#读取img文件
img_file = './test.jpg'
im = Image.open(img_file)
 
#quality 是设置压缩比
im.save('pico-ouo.jpg',quality = 20)
```

### 2.thumbnail方式
用PIL的 thumbnail方式进行图片压缩

```
from PIL import Image,ImageFile
 
#防止图片超过178956970 pixels 而报错
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None
 
#读取img文件
img_file = './test.jpg'
im = Image.open(img_file)
 
#获取原尺寸图片大小
w,h = im.size
#图片进行50%的压缩
im.thumbnail  = ((w // 2, h // 2))
#保存
im.save('test.jpg')

```

# 五.Pillow的绘图功能
PIL的ImageDraw提供了一系列绘图方法，让我们可以直接绘图。篇幅有限，本文暂时先不做探讨。

参考资料:
[PIL：图像处理模块，功能强大、简单易用](https://www.cnblogs.com/traditional/p/11111770.html)