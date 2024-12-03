---
title: 使用Appuim+Python脚本实现Android应用自动化
date: 2020-06-01
categories: 
  - Android开发
  - 自动化
---

# 一.引言
众所周知在App应用开发时我们会有不同的服务器环境来进行开发调试，例如测试环境，预发布环境，正式服环境.由于环境众多所以在测试工程师反馈问题时总要不断的去登录不同的服务器环境进行验证和调试。
流程如下:
1. 打开应用
2. 登录界面输入不同环境的账户密码
3. 登录验证

通过这三部才能进入App中进行调试。这三部的过程的执行重复率非常高，作为程序与我们能不能通过程序简化人工的操作呢?笔者将在本文中通过分析和实践来实现这一功能。

# 二.Appuim的安装和配置
对于Android手机屏幕的自动化控制有很多种方案。本文中将选择appuim来进行实现。

### 1.安装JDK环境和Android环境
安装配置appuim首先需要配置好JDK环境和Android Sdk环境。这两点不必多说，网上面大把的相关教程。

### 2.安装appium环境
下载[appium-desktop](https://github.com/appium/appium-desktop/releases)文件，点击进行安装。

### 3.配置appium
1。 安装好appium，打开程序，需要进行配置，host与port默认即可.
![](/images/d0f712c364c8a3d054af062e1f9c262f.webp)
2. 配置JDK环境和Android Sdk环境。
![image.png](/images/e95578bc216a6335f08f5dda715b6435.webp)
填写Android_home及Java_home后，Save and Restart，
3. 重启以后回到主界面，点击Start Server vX.X.X按钮。进入控制台日志界面，看到Appium REST http interface listener started on 0.0.0.0:4723就表示启动成功了。
接着点击“start inspector session”进行配置。
![image.png](/images/101a9e35ee5fce59554f46bb943f6d53.webp)
4. 配置inspector
![image.png](/images/b23373ccfeaf2f1fac77515f8b42b36e.webp)
重点是要配置相关参数可以通过键值对进行配置也可以通过右侧的Json文件进行配置:
- platformName:声明是ios还是android系统
- platformVersion:Android内核版本号，可通过命令adb shell getprop ro.build.version.release查看
- deviceName：连接的设备名称，通过命令adb devices -l中model查看
- appPackage：apk的包名
- appActivity：apk的launcherActivity，通过命令adb shell dumpsys activity | findstr “mResume”查看（需先打开手机应用）

Json配置文件示例:
{
“platformName”: “Android”，
“platformVersion”: “8.0.0”，
“appPackage”: “com.example.myapplication”，
“appActivity”: “.MainActivity”
}

5. 配置完成以后点击start session按钮，进入到操作面板功能中。
![image.png](/images/3a1f5f85e1d8e8b27e46f136eee00a14.webp)

# 三.使用appuim的录制功能生成自动化代码
生成的自动化代码脚本有很多语言可以选择，当然人生苦短我选Python。
![image.png](/images/4c33421cdc0627919ffc112c01005f24.webp)
基本制作步骤
- 开始录制
- 选择控件
- 对目标控件进行操作。
- 停止录制
- 切换脚本到具体工具可执行模式
- 拷贝脚本到其他工具中执行

# 四.Python执行appuim生成的自动化脚本
1. 首先通过Pip安装Selenium依赖库。
```
pip install Appium-Python-Client Selenium
```
2. 编写Python脚本，将上一步生成的Python自动化脚本复制进来。
```
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# appium服务监听地址
server='http://localhost:4723/wd/hub'
# app启动参数
desired_caps={
  "platformName": "Android"，
  "deviceName": "HWEVA"，
  "appPackage": "com.tencent.mm"，
  "appActivity": ".ui.LauncherUI"
}

# 驱动
driver = webdriver.Remote(server，desired_caps)
wait = WebDriverWait(driver，30)
# 获取手机号文本框
phone_text = wait.until(EC.presence_of_element_located((By.ID，"com.xxx.mm:id/phone")))
# 填写手机号文本框
phone_text.send_keys("18888888888")

# 获取手机号文本框
pwd_text = wait.until(EC.presence_of_element_located((By.ID，"com.xxx.mm:id/pwd")))
# 填写手机号文本框
pwd_text.send_keys("123456789")

# 获取登录按钮
login_btn = wait.until(EC.presence_of_element_located((By.ID，"com.xxx.mm:id/drp")))
# 点击登录按钮
login_btn.click()
```
当然Appium-Python-Client继承自Selenium所以使用方法和selenium是很类似的，我们可以通过手写的方式完成脚本的编写.更多api操作见：https://github.com/appium/python-client
3. 执行python脚本，就可以看到，完成了登录功能.需要注意的是使用python脚本来进行appium自动化测试的时候，需要开启appium服务。


# 五.将Python脚本文件转成window执行文件
### 1.使用bat脚本执行Python文件
1. 新建：appuim.bat文件。
2. 文件内容：
```
cd F:\appuim
call python appuim.py
```
3. 点击appuim.bat文件就能执行调用Python执行appuim.py。
### 2.将Python脚本打包成.exe文件
打包工具：[pyinstaller](http://www.pyinstaller.org/)
1. 安装 pyinstaller：
```
pip install pyinstaller
```
如果因为网络问题无法加载，可以下载源码安装；

2. 进入cmd下，执行下面命令：
```
Pyinstaller -F -w C:\Users\WIN10\Desktop\appuim.py --distpath C:\Users\WIN10\Desktop
```
distpath为打包后目录，在该目录中找到test.exe文件，直接双击即可。

-F 表示生成单个可执行文件。
-w 表示去掉控制台窗口，这在GUI界面时非常有用。
-p 表示你自己自定义需要加载的类路径。
-i 表示可执行文件的图标。

更多打包命令需要参考说明文档，这里不再详细描述。