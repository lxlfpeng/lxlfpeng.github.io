---
title: Android调试桥(ADB)
---

# 一.ADB概念
### 1. 什么是ADB?
ADB全称Android Debug Bridge(安卓调试桥)，在PC端安装ADB并且配置好ADB环境变量。就可以通过DOS命令行窗口输入命令的方式来对Android设备进行调试。

### 2. ADB的作用?
ADB的主要左右有两大类，一类是直接对Android进行调试。二类是通过``adb shell``进入到shell模式以后用linux命令行 对设备进行操作。
1. 对应用进行调试
   - 安装卸载应用。
   - 将文件从pc推到Android设备中,从Android设备中拉取图片。
   - 获取截图,录屏,获取正在显示的Activity等功能。

2. 安卓系统是基于Linux系统开发，也就支持常见的Linux的命令。通过``adb shell``来执行这些命令。

# 二.ADB的环境配置(Win10版)
为了ADB能够在PC端全局任意位置使用DOS命令行进行操作，首先要在PC端配置环境变量。
### 1.下载ADB文件到PC
[ADB And Fastboot for Windows](https://dl.google.com/android/repository/platform-tools-latest-windows.zip)

### 2.配置环境变量
在win10中依次打开我的电脑->属性->高级系统设置->环境变量->Path
![](https://upload-images.jianshu.io/upload_images/3067896-7c2dba4296555a86.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
配置完成以后打开DOS命令行,输入``adb version``如果能看到ADB的版本则说明ADB安装成功了。
```
Android Debug Bridge version 1.0.41
Version 30.0.5-6877874
Installed as C:\sdk\platform-tools\adb.exe
```

# 三.ADB连接Android设备
### 1.准备工作
- 一台Android设备。
- 数据线(最好是原装的,部分奸商卖的的数据线只能充电,要注意)。
- 打开Android设备的开发者选项.勾选usb调试。

### 2.通过手机数据线进行连接
手机通过数据线连接电脑.如果没有驱动可以下载驱动精灵,驱动精灵,或者豌豆荚安装好驱动。
启动ADB:
```
adb start-server
```
如果出现如下内容则说明ADB被正常启动了:
```
* daemon not running; starting now at tcp:5037
* daemon started successfully
```

### 3. 解决端口被占用的问题
如果在win10启动ADB有时候会提示5037端口被占用，导致启动失败。提示如下:
```
* daemon not running. starting it now on port 5037 *
ADB server didn't ACK 
* failed to start daemon *daemon
```
目前有两种方案解决该问题:一是将占用ADB端口的应用杀死。二则是修改ADB的端口(推荐)。
##### (1.)方式一
- 查看当前哪个进程占用了这个端口
  ```
  netstat -ano | findstr "5037"
  ```
- 杀掉占用的进程即可
  ```
  taskkill /f /pid xxx
  ```
##### (2.)方式二
系统环境变量中定义 ANDROID_ADB_SERVER_PORT 的值即可。数值尽量选择一个不常用的端口，如11223等
右键计算机 -> 属性 ->高级计算机设置 ->环境变量 ->新建 ->变量名：ANDROID_ADB_SERVER_PORT ->值：11223(任意)
重启ADB即可。

### 4.ADB通过wifi连接Android设备
1. Android设备和Pc必须处于同一个内网中。
2. 通过数据线连接Android设备,ADB打开5555端口:
  ```
  adb tcpip 5555  //restarting in TCP mode port: 5555
  ```
3. 连接Android设备在内网中的地址:
  ```
  adb connect 192.168.1.104
  ```

# 四.ADB常用指令
``adb start_server`` 启动ADB服务

``adb kill-server`` 关闭ADB服务

`` adb devices `` //列出所有的连接设备

`` adb install xxx.apk `` //安装apk 一共有lrtsdg六个选项
- -l 锁定该应用程序
- -r 替换已存在的应用程序，也就是说强制安装
- -t 允许测试包
- -s 把应用程序安装到sd卡上
- -d 允许进行将见状，也就是安装的比手机上带的版本低
- -g 为应用程序授予所有运行时的权限

`` adb install -r xxx.apk  ``//强制安装apk

`` adb -s 设备1  install -r xxx.apk  ``// 选择设备进行安装

`` adb shell pm list packages  ``//列出所有的安装的包名

`` adb shell pm path com.android.search ``// 列出指定包名对应的apk路径

`` adb shell pm clear com.android.search ``// 清空指定包名对应的应用的数据和缓存文件，开发时很有用

`` adb shell dumpsys window w |findstr \/ |findstr name=  ``//查看前台进程和前台activity

`` adb shell ps  ``//列出设备里面所有的进程

`` adb shell ps |findstr baidu   ``//查看包含关键字的进程,如baidu

`` adb shell service list  ``//查看Service列表

``adb shell top``列出进程的信息
- -d 表示刷新的时间(单位秒).
- -m 表示显示进程最大数.
- |grep (进程名称) 抓取进程名的进程显示它的子线程情况
- -p pid 显示某个进程的信息.如果是多个进程都好分割:pid1,pid2,pid3

参考:
[Google官方文档之ADB](https://developer.android.google.cn/studio/command-line/adb)