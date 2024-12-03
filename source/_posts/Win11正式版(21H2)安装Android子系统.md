---
title: Win11正式版(21H2)安装Android子系统
---

> 本教程的背景是Win11正式版本(21H2)暂未全面推送Android子系统的情况的尝鲜教程。
# 一. Win11dev版本
wsa在win11测试版本上面已经可以直接使用了，只设置区域为美国，设置->启动关闭windows功能->开启hyper-v和虚拟机平台，电脑重启后，去商店搜索Window Subsystem for Android即可使用。
# 二. Win11正式版：
### 1. 修改区域为美国
设置->时间和语言->语言&区域->国家和地区->选择美国。
![](https://upload-images.jianshu.io/upload_images/3067896-eafe6f17e1305beb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
### 2. 打开虚拟化技术
2. 菜单->启动关闭windows功能->开启hyper-v和虚拟机平台->重启电脑。
![](https://upload-images.jianshu.io/upload_images/3067896-8d6f3dad51d584ce.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
>重启的时候检查下BIOS的虚拟化是否开启Intel为VT， AMD为SVM
### 3. 下载Windows Subsystem for Android
在[](https://store.rg-adguard.net)网站，输入[](https://www.microsoft.com/store/productId/9P3395VX91NR)选择slow通道，点击对勾按钮，下载文件（在网页最下方，Msixbundle格式），
![](https://upload-images.jianshu.io/upload_images/3067896-9859a384860300c3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
>如果浏览器打不开下载地址，可用迅雷等下载工具复制其路径进行下载。

**也可以使用已经下载好的百度云盘资源包**
链接：https://pan.baidu.com/s/10DEWBH5aCvAc04aEGQDFKA 
提取码：372p

### 4. 安装Windows Subsystem for Android
##### (1.) 管理员身份运行了Powershell
![](https://upload-images.jianshu.io/upload_images/3067896-5330875f5ac02bef.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
##### (2.) 执行Add-AppxPackage -Path 刚下载的文件.Msixbundle即可。
```
Add-AppxPackage -Path D:\Download\android\MicrosoftCorporationII.WindowsSubsystemForAndroid_1.8.32822.0_neutral___8wekyb3d8bbwe.Msixbundle
```
![](https://upload-images.jianshu.io/upload_images/3067896-2a5d461759a793fa.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

如果报错可以使用我提供的资源包里面的文件进行修复:
````
Add-AppxPackage Microsoft.VCLibs.x64.14.00.Desktop.appx
````
```
Add-AppxPackage Microsoft.UI.Xaml.2.6_2.62108.18004.0_x64__8wekyb3d8bbwe.Appx
```
然后再次执行Add-AppxPackage -Path 刚下载的文件.Msixbundle即可。

##### (3.) 如果执行成功打开菜单可以看到WSA功能.
![](https://upload-images.jianshu.io/upload_images/3067896-731eabb47c888735.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 5. 通过ADB连接Android子系统
(1.)先下载好adb然后配置好环境变量(基础功能不懂百度下).
(2.)打开WSA设置中的开发人员模式设置
![](https://upload-images.jianshu.io/upload_images/3067896-0757191293d4e548.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
(3.)adb链接设备
输入"adb connect 127.0.0.1:58526"（以实际was设置中显示的为准）
### 6. 通过ADB安装应用到Android子系统
1. 下载要安装的apk。通过Adb进行安装即可
```
adb install D\download\qq.apk
```
2. 在开始菜单可以看到新安装的安卓应用。

