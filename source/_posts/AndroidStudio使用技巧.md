---
title: AndroidStudio使用技巧
---

# 一.Android-Studio模板文件Template
### 1.何为模板Template
当我们创建一个新的activity的时候as会有许多默认的模板供我们选择。选择这些模板会生成相应的代码,这样我们就可以少做很多的事.
![](https://upload-images.jianshu.io/upload_images/3067896-07c5b21e7b083e39.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 2.查看系统自带的Template
打开``As安装目录\plugins\android\lib\templates\activities``可以看到很多的自带模板.
![](https://upload-images.jianshu.io/upload_images/3067896-e13456831091fde4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
打开一个我们最常用的EmptyActivity
![](https://upload-images.jianshu.io/upload_images/3067896-c3f42ecb899e68e8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- template.xml：相当于Android中的布局文件，用于提供参数，布局等。
![](https://upload-images.jianshu.io/upload_images/3067896-a0a0484821d04799.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- globals.xml.ftl：主要是声明一些全局变量。
- recipe.xml.ftl:用于组合生成我们实际需要的代码文件和布局文件等。
- root/src:代码文件

# 二.Android-Studio的plugins开发
### 1.创建plugin项目
##### (1.)打开idea,创建新的项目.
![](https://upload-images.jianshu.io/upload_images/3067896-8e2b9fdfa6de9d16.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![](https://upload-images.jianshu.io/upload_images/3067896-81aa8e563f1d754a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
##### (2.)plugin.xml内容解析
![](https://upload-images.jianshu.io/upload_images/3067896-da1b418b2777e3a9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- id即为插件的id
- name为插件的名称
- version为插件的版本号
- vendor中的内容为你的邮箱以及公司名称、官网等
  ![](https://upload-images.jianshu.io/upload_images/3067896-d526fbb68f334d54.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- extensions即为产检的扩展注册
- action就是动作注册，也就是说我们安装完这个插件后，在哪里使用快捷键是什么，在哪个菜单下。

### 2.生成jar插件
![](https://upload-images.jianshu.io/upload_images/3067896-acd5853cbfabd601.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# 三.Android-Studio去除多余的导包
1. 单个文件
   右键单击文件 选择optimize imports
   ![](https://upload-images.jianshu.io/upload_images/3067896-b461c4efbb346d85.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

2. 整个文件包
   右键单击文件夹或者是文件包 选择optimize imports。
   ![](https://upload-images.jianshu.io/upload_images/3067896-eba2761ad31bf0b8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# 四.Android-Studio去除无用的文件
### 1.删除多余的资源文件
1. 点击analyze在弹出菜单中，选择run inspection by name:
![](https://upload-images.jianshu.io/upload_images/3067896-b98880b2b7ef5129.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![](https://upload-images.jianshu.io/upload_images/3067896-e7a6f9111889f396.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![](https://upload-images.jianshu.io/upload_images/3067896-01c1627fe669b761.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
2. 单个资源文件删除:
![](https://upload-images.jianshu.io/upload_images/3067896-718428f4eb89b77f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![](https://upload-images.jianshu.io/upload_images/3067896-00db7f289fc77007.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
3. 多个资源文件删除:
将不需要的删除的资源文件exclude掉，然后在将所有的无用资源文件删除掉。
   
### 2.删除多余的JAVA文件
查找java文件，选择“Unused declaration”:
![image](https://upload-images.jianshu.io/upload_images/2706635-552882ff495c2cac.png?imageMogr2/auto-orient/strip|imageView2/2/w/566/format/webp)
根据这个选择框，我们可以选择查找范围，以及想要查找的成员，下面的options里，不仅仅能查找class类，而且还有字段，方法，参数，变量等等。因此，删除unused class也只是其中的一部分，这对于优化代码，是非常方便的。
![image](https://upload-images.jianshu.io/upload_images/2706635-3eb5e888344472ec.png?imageMogr2/auto-orient/strip|imageView2/2/w/1045/format/webp)
控制台输入了相对应的问题，同时也给出了对应的解决方案，简洁明了。
