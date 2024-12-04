---
title: x96max+-电视盒子如何刷入EmuELEC游戏系统
date: 2021-07-11
index_img: /images/368ed8979644e82aaaaf3a9694d0d744.webp
top_img: /images/368ed8979644e82aaaaf3a9694d0d744.webp
cover: /images/368ed8979644e82aaaaf3a9694d0d744.webp
categories: 
  - 电视盒子
---

# 一. 了解相关概念
### 1. Kodi是什么?

Kodi（以前称为XBMC）是一个免费的开放源代码媒体播放器软件应用程序，它可以运行在``Linux、OSX、Windows、Android``等多种操作系统和硬件平台。它是一个优秀的**开源**的（GPL）媒体中心软件。最初为Xbox而开发，叫XBMC(全称是XBOX Media Center)，也就是XBOX平台的媒体中心。因为全世界开发者的参与，这个软件已经拥有远远超过以往的功能，这已经不能用‘一个简单播放器’来包含所有的一切了。因为这个原因，XBMC.14后更名为Kodi。
Kodi的图形用户界面让用户方便地从硬盘、光盘、局域网和互联网浏览和观看视频、图片，收听广播和音乐。Kodi项目由非营利的XBMC基金会管理，并由分布在世界各地的志愿者参与开发。不仅如此Kodi还能通过插件提供各种扩展的功能，有Kodi开发团队，也有第三方人员开发的插件。
[kodi中文网](http://www.kodiplayer.cn/)
### 2. LibreELEC是什么?

LibreELEC 是基于 Linux 的多媒体播放系统，其宗旨是在一个高度精简的 Linux 系统下通过 KODI 播放多媒体音视频，LibreELEC 是 OPENELEC 系统高度开发优化后的改版。

### 3..Lakka 是什么？
Lakka是基于LibreELEC系统开发的Linux游戏系统，在LibreELEC基础上删减掉KODI（前身为 XBOX 上的多媒体播放器 XMBC），加上 RetroArch 组合而成。


### 4. CoreELEC是什么?
CoreELEC是一个小巧的**Linux发行版系统**，是 LibreELEC 的分支，它是专为Amlogic（晶晨）芯片开发的Kodi专用Linux系统，**它的界面就是Kodi的界面**，可以**独立运行于U盘或TF卡**。有时候播放4K视频时，安卓版本下的Kodi会掉帧，但是CoreELEC就不会。可最大限度的利用硬件资源，流畅的播放视频。另外CoreELEC可以完美输出杜比全景声和dtsx，低端的安卓版本则不行。
Coreelec和libreelec都是把精简版linux与kodi集成的媒体中心系统。不过Coreelec是专门面向Amlogic芯片设备适配的，推荐s905、s912、s922系列的盒子安装使用
[CoreELEC官方网站](https://coreelec.org/)
[github地址](https://github.com/CoreELEC/CoreELEC/releases)

### 5. RetroArch 是什么？
 RetroArch 是跨操作系统的应用前台，其统合了输入、画面输出等 IO，拥有从 FC 到 NGC等各机种的模拟器核心，由于多被用来玩模拟器，可以简单认为是一个插件性质的多机种模拟器。目前大热的迷你 SFC 和迷你 FC 破解后也可以通过安装 RetroArch 模拟官方不支持的SFC、FC 游戏和 MD、街机等其他机种。

### 6. EmuELEC是什么?
EmuELEC是专为Amlogic（晶晨）S905/S912芯片的盒子开发的游戏系统，它基于**CoreELEC**系统，在CoreELEC的基础上移植了 **EmulationStation(ES)**, **RetroArch  (RA) **和众多独立模拟器程序。剥离了 CoreELEC 带的 **KODI** [影音播放](https://www.smzdm.com/fenlei/yingyinbofang/)管理系统。

- EmulationStation(ES) 是纯粹的前端，支持一些漂亮的主题和视频预览，但是不具备模拟器核心调度能力，通过外调 RetroArch  (RA)  或其它独立的模拟器运行游戏。

- RetroArch  (RA)  是自带前端的整合型模拟器，通过调用不同的 Libre 模拟内核运行游戏。

[EmuELEC的github地址](https://github.com/EmuELEC/EmuELEC)


### 7. EmuELEC 有什么优势？
EmuELEC 前身为 Sx05RE。Sx05RE 整合了 Lakka、KODI、EmulationStation，常被人简称为三合一。Sx05RE 比 Lakka 系统华丽，支持的模拟器更多（比 Lakka 多支持了速度更快效果更好的 PSP 模拟器、DC 模拟器、NDS 模拟器、OpenBOR 引擎和 ADVMAME 模拟器），支持图片预览、视频预览，无需编辑游戏列表即可显示加入的游戏，内置的 KODI 播放器支持硬解 H265 10Bit 视频（S905 盒子），它又比树莓派的 RetroPie 精简，纯净系统才500 多 MB。此外，它的输出延迟大大低于安卓系统下的模拟器，如果你可以接受破解后的迷你 SFC 玩街机游戏的输出延迟，那么一定也可以接受 EmuELEC 的延迟，因为两者都是用基于 Linux 系统下的 RetroArch 来模拟游戏，本质上无异。
因Sx05RE 项目只有墨西哥大神 Shantigilbert 一人开发，而 KODI 经常出现各种需要修复的 BUG，浪费了大神的大量时间。出于时间严重不足的考虑， Shantigilbert 决定从 Sx05RE中删除 KODI，并将系统改名成 EmuELEC，使系统专为游戏服务。针对有高清影音播放需要的玩家，Shantigilbert 提供了一个 CoreELEC 用的名为 EmuELEC 的 addon 插件。虽然插件版 EmuELEC 功能不及独立版的 EmuELEC，但是绝对秒杀 Lakka 这种弱鸡系统了。

# 二 . 电视盒子烧录EmuELEC 系统
### 1. 准备工作
- 一个u盘（根据镜像大小，建议使用高速的u盘效果会快点）。
- 镜像，这里我们用请参考b站up主 人中日月做好的镜像[EmuELEC 3.3.1 2020春节整合版详细说明](https://www.bilibili.com/read/cv4420521/)，下载合适自己机型的镜像文件。
- 写盘工具[Win32DiskImager](https://sourceforge.net/projects/win32diskimager/)。

### 2. 刷入系统
1. 将下载好的镜像文件解压会得到一个img文件。
2. 使用Win32DiskImager将解压好的img镜像文件写入你的U盘或是TF卡。
3. 查找自己机型相关的替换dtb启动文件。
4. 将烧录好的U盘或是TF卡插入盒子的USB接口上。
5.  进入adb所在目录执行adb shell reboot update，然后ADB REBOOT UPDATE即可。如果不会ADB的话，可以在安卓下安装下面的[Reboot to LibreELEC.apk ](https://pan.baidu.com/s/1CeOLXLodZ_xRkkf8PySRzg)，提取码: 8ch4，点一下就可以。

### 3. 注意事项
1. 怎样从 安卓系统 切换到 游戏系统?
在盒子的安卓系统里面安装 LibreELEC.apk 软件，打开这个软件就可以切换到游戏系统。
2. 游戏系统 切换到 安卓系统。主界面 --- 增强选项 --- 返回安卓系统
3. 在游戏中要退出，默认的快捷键是L3+R3，最好改成 SELECT + START, 不然你的手柄如果没有L3+R3，就要用USB键盘的ESC键退出。

[EmuELEC 3.3.1 2020春节整合版详细说明](https://www.bilibili.com/read/cv4420521/)
[镜像烧录](https://www.znds.com/forum.php?mod=viewthread&tid=1171738&fromuid=19486)
