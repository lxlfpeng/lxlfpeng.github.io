---
title: AndroidStudio使用技巧
date: 2020-11-02
categories: 
  - Android开发
---

# 一.Android-Studio模板文件Template
### 1.何为模板Template
当我们创建一个新的activity的时候as会有许多默认的模板供我们选择。选择这些模板会生成相应的代码,这样我们就可以少做很多的事.
![](/images/54d5874631080ca90cc4102af739f29f.webp)

### 2.查看系统自带的Template
打开``As安装目录\plugins\android\lib\templates\activities``可以看到很多的自带模板.
![](/images/5704f62e0f11e9d04d045685c07a8f05.webp)
打开一个我们最常用的EmptyActivity
![](/images/dfee980be98c02cd0383f43b9d9512fd.webp)
- template.xml：相当于Android中的布局文件，用于提供参数，布局等。
![](/images/60fc8fb7f78739e8da667d1e66d42abe.webp)
- globals.xml.ftl：主要是声明一些全局变量。
- recipe.xml.ftl:用于组合生成我们实际需要的代码文件和布局文件等。
- root/src:代码文件

# 二.Android-Studio的plugins开发
### 1.创建plugin项目
##### (1.)打开idea,创建新的项目.
![](/images/df03fb6e2391e7644e2842ba4d554ce6.webp)
![](/images/c485245c573a98b4142e26023a00bc34.webp)
##### (2.)plugin.xml内容解析
![](/images/6394fc52d4d8eb0633fc9f7df0f097dc.webp)
- id即为插件的id
- name为插件的名称
- version为插件的版本号
- vendor中的内容为你的邮箱以及公司名称、官网等
  ![](/images/ae8383d8e04a1bd5cbe155399dba8979.webp)
- extensions即为产检的扩展注册
- action就是动作注册，也就是说我们安装完这个插件后，在哪里使用快捷键是什么，在哪个菜单下。

### 2.生成jar插件
![](/images/001c1d0a24001f525cbe3d587f6c3134.webp)

# 三.Android-Studio去除多余的导包
1. 单个文件
   右键单击文件 选择optimize imports
   ![](/images/c79fbad1b9f1ed0b83216b7902a900bb.webp)

2. 整个文件包
   右键单击文件夹或者是文件包 选择optimize imports。
   ![](/images/04a93b75075f51b1c935e298170a8961.webp)

# 四.Android-Studio去除无用的文件
### 1.删除多余的资源文件
1. 点击analyze在弹出菜单中，选择run inspection by name:
![](/images/f3079d9e007359b948b63b39705ca82e.webp)
![](/images/8fa39fd598f74a771fdb80bd953bfa8c.webp)
![](/images/04304fec409424bf263f3cb3d5dd8cab.webp)
2. 单个资源文件删除:
![](/images/34f7576d39ff98e42d047ea6083ec8cc.webp)
![](/images/ec19902ed7436cc114c68b01d8594966.webp)
3. 多个资源文件删除:
将不需要的删除的资源文件exclude掉，然后在将所有的无用资源文件删除掉。
   
### 2.删除多余的JAVA文件
查找java文件，选择“Unused declaration”:
![image](/images/67cb98113399c4efb67cfeee1f4d5a3a.webp)
根据这个选择框，我们可以选择查找范围，以及想要查找的成员，下面的options里，不仅仅能查找class类，而且还有字段，方法，参数，变量等等。因此，删除unused class也只是其中的一部分，这对于优化代码，是非常方便的。
![image](/images/e988b91ea246f6e2dda0a3079613832a.webp)
控制台输入了相对应的问题，同时也给出了对应的解决方案，简洁明了。
