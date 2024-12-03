---
title: Apk构建总结之一打包流程及安装流程
date: 2019-08-01
categories: 
  - Android开发
---

# 一. 分析已经打好的apk
要了解APK的打包流程,我们首先来了解下打包完成以后APK包里面包含哪些东西。.apk文件其实就是一个压缩文件，把文件的后缀改成.zip就可以用解压软件解压了：
### 1. 将apk后缀改成rar包
![apk文件](/images/6e6a7c906151d588c5efd717072ff845.webp)
![rar文件](/images/90739fe9838162f745201f8d151f4392.webp)
### 2. 解压rar包
![目录](/images/4f590a772f52dc439b3bead52549efe0.webp)

apk是一个压缩包，里面有lib，META-INF，classes.dex，res，resources.arsc文件夹和文件。下面看看它们各自的作用。

- assets资源。
- lib不是每个apk都有的，主要看项目,文件夹里面存放的是so动态链接库，so动态链接库不需要做处理。
- META-INF是签名文件夹，里面有三个文件。
- res:除图片和 res/raw 文件夹下的文件外，其余的 xml 文件都被 aapt 编译成二进制的 xml 文件,里面还会分animator,anim,color,drawable,layout,menu和raw这几个文件夹。
- AndroidManifest.xml:经过 aapt 编译后的二进制的 xml 文件,它位于整个项目的根目录，描述了package中暴露的组件（activities, services, 等等），他们各自的实现类，各种能被处理的数据和启动位置。 除了能声明程序中的Activities, ContentProviders, Services, 和Intent Receivers,还能指定permissions和instrumentation（安全控制和测试）。这个文件是很重要的，里面有我们的Android四大组件和申请的权限。
- classes.dex是.dex文件，就是我们写的java代码经过处理得到的。如果做了拆包那么会有classes1.dex，classes2.dex ...多个classes.dex文件。
- resources.arsc记录了所有的应用程序资源目录的信息，包括每一个资源名称、类型、值、ID以及所配置的维度信息。我们可以将这个resources.arsc文件想象成是一个资源索引表，这个资源索引表在给定资源ID和设备配置信息的情况下，能够在应用程序的资源目录中快速地找到最匹配的资源。

>我们发现xml文件都不能直接被识别了这是因为:xml文件都被aapt编译成二进制的xml文件,将文本格式的xml转为二进制格式的xml原因有以下两点:二进制格式的XML文件占用空间更小;二进制格式的XML文件解析速度更快。

# 二. 打包的详细流程
### 1.编译打包流程图
Android Studio默认采用gradle组织完成打包过程，对开发者来说简单的执行相关的task即可，这种透明的打包过程也让我们忽略了很多细节。
![image.png](/images/1c43f15e6a9787dc394b14a0e66e7491.webp)
打包工具详解.
工具名称 | 功能介绍 |路径
|-|-|-|
aapt |Android资源打包工具 打包res资源文件，生成R.java、resources.arsc和res文件（二进制 & 非二进制如res/raw和pic保持原样）|{SDK_PATH}/platform-tools/{tools_version}/appt.exe
aidl |  Android接口描述语言转化为.java文件的工具 |  {SDK_PATH}/platform-tools/{tools_version}/aidl.exe
javac  |  Java Compiler java代码转class文件  |  {JDK_HOME}/javac
dex|转化.class文件为Davik VM能识别的.dex文件|{JDK_HOME}/platform-tools/{tools_version}/dx.bat
apkbuilder  |  所有没有编译的资源，如images、assets目录下资源,编译过的资源和.dex文件都会被apkbuilder工具打包到最终的.apk文件中  |  {JDK_HOME}/tools/opkbuilder
jarsigner  |  .jar文件的签名工具,一旦APK文件生成，它必须被签名才能被安装在设备上。一种是用于调试的debug.keystore 一种就是用于发布正式版本的release.keystore |  {JDK_HOME}/jarsigner
zipalign  |  字节码对齐工具,对齐的主要过程是将APK包中所有的资源文件距离文件起始偏移为4字节整数倍，这样通过内存映射访问apk文件时的速度会更快。对齐的作用就是减少运行时内存的使用。  |  {JDK_HOME}/tools/zipalign
### 2.编译打包步骤
##### （1.） 打包资源文件，生成R.java文件
打包资源文件的工具是aapt（The Android Asset Packaing Tool），目录 sdk\build-tools\25.0.0\aapt。
在这个过程中，项目中的AndroidManifest.xml文件和布局文件XML都会编译，然后生成相应的R.java，另外AndroidManifest.xml会被aapt编译成二进制。
存放在APP的res目录下的资源，该类资源在APP打包前大多会被编译，变成二进制文件，并会为每个该类文件赋予一个resource id。对于该类资源的访问，应用层代码则是通过resource id进行访问的。
Android应用在编译过程中aapt工具会对资源文件进行编译，并生成一个resource.arsc文件，resource.arsc文件相当于一个文件索引表，记录了很多跟资源相关的信息。
##### （2.） 处理aidl文件，生成相应的Java文件
处理aidl文件的工具是aidl（Android Interface Definition Language），即Android接口描述语言，目录 sdk\build-tools\25.0.0\aidl。
aidl工具解析接口定义文件然后生成相应的Java代码接口供程序调用。如果在项目没有使用到aidl文件，则可以跳过这一步。
##### （3.） 编译项目源代码，生成class文件
编译源代码使用工具是 Java编译器（javac）
项目中所有的Java代码，包括R.java和.aidl文件，都会变Java编译器（javac）编译成.class文件，生成的class文件位于工程中的bin/classes目录下。
##### （4.） 转换所有的class文件，生成classes.dex文件
这过程使用工具 dx（dex）生成可供Android系统Dalvik虚拟机执行的classes.dex文件，工具目录（sdk\build-tools\25.0.0\dx）。
任何第三方的libraries和.class文件都会被转换成.dex文件。dx工具的主要工作是将Java字节码转成 Dalvik字节码、压缩常量池、消除冗余信息等。
##### （5.） 打包生成APK文件
打包的工具apkbuilder，目录 android-sdk/tools，apkbuilder为一个脚本文件，实际调用的是（sdk\tools\lib）文件中的com.android.sdklib.build.ApkbuilderMain类。
所有没有编译的资源，如images、assets目录下资源（该类文件是一些原始文件，APP打包时并不会对其进行编译，而是直接打包到APP中，对于这一类资源文件的访问，应用层代码需要通过文件名对其进行访问）；
编译过的资源和.dex文件都会被apkbuilder工具打包到最终的.apk文件中。
##### （6.） 对APK文件进行签名
一旦APK文件生成，它必须被签名才能被安装在设备上。
在开发过程中，主要用到的就是两种签名的keystore。一种是用于调试的debug.keystore，它主要用于调试，在Eclipse或者Android Studio中直接run以后跑在手机上的就是使用的debug.keystore；
另一种就是用于发布正式版本的relese.keystore，需要开发者自己配置。
#####  （7.） 对签名后的APK文件进行对齐处理
如果你发布的apk是正式版的话，就必须对APK进行对齐处理，用到的工具是zipalign，目录 sdk\build-tools\25.0.0\zipalign。
对齐的主要过程是将APK包中所有的资源文件距离文件起始偏移为4字节整数倍，这样通过内存映射访问apk文件时的速度会更快。对齐的作用就是减少运行时内存的使用。

>综上所述， Android SDK中build-tools目录提供了各种程序， 都是独立可运行的，可以认为Android Studio编译打包过程是对这些工具的封装。

# 三.Android SDK 目录结构
通过上文可以了解到APK打包的脚本都是在SDK文件夹下面的：
![SDK目录结构](/images/c9e8b64995856ca415f5d37f826e82c8.webp)
##### 1.build-tools目录
![build-tools](/images/0449033303732721dcbfb4433bdc6ec7.webp)
编译工具目录，包含了转化为davlik虚拟机的编译工具,比如adb、和aapt、aidl、dx等文件。
##### 2.emulator目录
Android模拟器模拟器目录。
##### 3.extras目录
该文件下存放了Google提供的USB驱动，Intel提供的硬件加速附件工具包。
##### 4.platforms目录
![image.png](/images/94b50927da5a97425409e822879bec28.webp)
是每个平台SDK真正的文件，存放不同版本的Android系统。对应android studio build.gradle中的compileSdkVersion
##### 5.platform-tools目录
![platform-tools](/images/e1bdc71b744c71ef88560dd804617141.webp)
各个版本的通用工具。比如 adb、sqlite3、fastboot等.
##### 6.sources目录
![sources](/images/c00739984dfe4ca1c21b3da4c744dd62.webp)
包含了各个版本的SDK源码。
##### 7.system-images
![system-images](/images/f62add76997d1796aad8ced685538062.webp)
存放的是创建Android虚拟机时的镜像文件(已经编译好的镜像文件,模拟器可以直接加载)。

### 8.tools
tools：这个文件夹下存放了大量Android开发、调试的工具。包括测试、调试、第三方工具。模拟器、数据管理工具等。

# 四. Android Studio工程结构。
![项目主结构](/images/8d932709d5fa2da071609fb80b8d870e.webp)

### 1.gradle目录。
![gradle](/images/fdf8ad1ba3bb722c491b96a3c6c68147.webp)
gradle 运行时自动生成的目录（自动编译工具产生的文件）,版本由wrapper指定。一般情况不做修改，不需要纳入项目源代码管理中。
### 2..idea目录。
![idea](/images/add165050d9bec659e1c2504d0ad48ef.webp)
Intellij IDEA 运行时候生成的文件目录，一般情况不做修改，不需要纳入项目源代码管理中。 
### 3.app(module)目录。
![image.png](/images/19c5a71cb39e491d66a621702b37462e.webp)
- app/build：app模块编译输出的文件
- app/libs：  放置引用的类库文件
- app/src： 放置应用的主要文件目录
- app/src/androidTest：单元测试目录
- app/src/main：主要的项目目录和代码
- app/src/main/assets：放置原生文件，里面的文件会保留原有格式，文件的读取需要通过流
- app/src/main/java：项目的源代码
- app/src/main/res：项目的资源
- app/src/main/res/anim：存放动画的XML文件
- app/src/main/res/drawable：存放各种位图文件(.png，.jpg，.9png，.gif等)和drawable类型的XML文件
- app/src/main/res/drawable-v24：存放自定义Drawables类（Android API 24开始，可在XML中使用）
- app/src/main/res/layout：存放布局文件
- app/src/main/res/menu：存放菜单文件
- app/src/main/res/mipmap-hdpi：存放高分辨率图片资源
- app/src/main/res/mipmap-mdpi：存放中等分辨率图片资源
- app/src/main/res/mipmap-xdpi：存放超高分辨率图片资源
- app/src/main/res/mipmap-xxdpi：存放超超分辨率图片资源
- app/src/main/res/mipmap-xxxdpi：存放超超超高分辨率图片资源
- app/src/main/res/raw：存放各种原生资源(音频，视频，一些XML文件等)
- app/src/main/res/values： 存放各种配置资源（颜色，尺寸，样式，字符串等）
- app/src/main/res/values/attrs.xml：自定义控件时用的较多，自定义控件的属性
- app/src/main/res/values/arrays.xml：定义数组资源
- app/src/main/res/values/colors.xml：定义颜色资源
- app/src/main/res/values/dimens.xml：定义尺寸资源
- app/src/main/res/values/string.xml：定义字符串资源
- app/src/main/res/values/styles.xml：定义样式资源
- app/src/main/res/values-v11：在API 11+的设备上调用
- app/src/main/res/values-v14：在API 14+的设备上调用
- app/src/main/res/values-v21：在API 21+的设备上调用
- app/src/main/res/AndroidManifest.xml：项目的清单文件（名称、版本、SDK、权限等配置信息）
- app/src/.gitignore：忽略的文件或者目录
- app/app.iml：app模块的配置文件
- app/build.gradle：app模块的gradle编译文件
- app/proguard-rules.pro：app模块的代码混淆配置文件

### 4.gradle目录及配置项.
![image.png](/images/e0c28b2bf54d6d1c7d375ade941b0f89.webp)
- gradle/wrapper/gradle-wrapper.jar
- gradle/wrapper/gradle-wrapper.properties 主要指定了该项目需要什么版本的Gradle，从哪里下载该版本的Gradle，下载下来放到哪里
- .gitignore： 忽略的文件或者目录
- build.gradle：项目的gradle编译文件
- gradle.properties： gradle相关的全局属性设置
- gradlew： 编译脚本，可以在命令行执行打包
- gradlew.bat：windows下的gradle wrapper可执行文件
- local.properties：配置SDK/NDK所在的路径
- MyApplication.iml：保存该模块的相关信息
- settings.gradle：设置相关的gradle脚本

# 五. APk安装流程
### 1. 概述
众所周知，Android应用最终是打包成.apk格式（其实就是一个压缩包），然后安装至手机并运行的。APK即Android Package的缩写。
应用程序管理服务PackageManagerService安装应用程序的过程，其实就是解析析应用程序配置文件AndroidManifest.xml的过程，并从里面得到得到应用程序的相关信息，
例如得到应用程序的组件Activity、Service、Broadcast Receiver和Content Provider等信息，有了这些信息后，通过ActivityManagerService这个服务，我们就可以在系统中正常地使用这些应用程序了。

### 2. Android应用APK的四种安装方式
- 系统应用安装：开机时加载系统的APK和应用，没有安装界面；
- 网络下载应用安装：通过各种market应用完成，没有安装界面；
- ADB工具安装：即通过Android的SDK开发tools里面的adb.exe程序安装，没有安装界面；
- 第三方应用安装：通过SD卡里的APK文件安装(比如双击APK文件触发)，有安装界面，系统默认已经安装了一个安装卸载应用的程序，即由packageinstaller.apk应用处理安装及卸载过程的界面。

### 3. 应用安装涉及到的目录
- /system/app ：系统自带的应用程序，获得adb root权限才能删除
- /data/app ：用户程序安装的目录。安装时把apk文件复制到此目录
- /data/data ：存放应用程序的数据
- /data/dalvik-cache：将apk中的dex文件安装到dalvik-cache目录下(dex文件是dalvik虚拟机的可执行文件,当然，ART–Android Runtime的可执行文件格式为oat，启用ART时，系统会执行dex文件转换至oat文件)
- /data/system ：该目录下的packages.xml文件，类似于Windows的注册表，这个文件是在解析apk时由writeLP()创建的，里面记录了系统的permissions，以及每个apk的name,codePath,flags,ts,version,uesrid等信息，这些信息主要通apk的AndroidManifest.xml解析获取，解析完apk后将更新信息写入这个文件并保存到flash，下次开机直接从里面读取相关信息添加到内存相关列表中。当有apk升级，安装或删除时会更新这个文件。
- /data/system/packages.xml中内容详解(这里列举的标签内容不一定完整，只是列举核心内容，packages.xml的完整定义详见官方文档)：

### 4.安装流程
![](/images/162d23b9226028105f5920770e6119de.webp)
##### 拷贝apk文件到指定目录
在Android系统中，apk安装文件是会被保存起来的，默认情况下，用户安装的apk首先会被拷贝到 /data/app 目录下。
/data/app目录是用户有权限访问的目录，在安装apk的时候会自动选择该目录存放用户安装的文件，而系统出厂的apk文件则被放到了 /system 分区下,包括 /system/app，/system/vendor/app，以及 /system/priv-app 等等，该分区只有Root权限的用户才能访问，这也就是为什么在没有Root手机之前，我们无法删除系统出厂的app的原因了。
##### 解压apk，拷贝文件，创建应用的数据目录
为了加快app的启动速度，apk在安装的时候，会首先将app的可执行文件（dex）拷贝到 /data/dalvik-cache 目录，缓存起来。
然后，在/data/data/目录下创建应用程序的数据目录（以应用的包名命名），存放应用的相关数据，如数据库、xml文件、cache、二进制的so动态库等等。
##### 解析apk的AndroidManifinest.xml文件
Android系统中，也有一个类似注册表的东西，用来记录当前所有安装的应用的基本信息，每次系统安装或者卸载了任何apk文件，都会更新这个文件。这个文件位于如下目录：
/data/system/packages.xml
系统在安装apk的过程中，会解析apk的AndroidManifinest.xml文件，提取出这个apk的重要信息写入到packages.xml文件中，这些信息包括：权限、应用包名、APK的安装位置、版本、userID等等。
由此，我们就知道了为啥一些应用市场和软件管理类的app能够很清楚地知道当前手机所安装的所有的app，以及这些app的详细信息了。
另外一件事就是Linux的用户Id和用户组Id，以便他可以获得合适的运行权限。
以上这些都是由PackageServiceManager完成的，下面我们会重点介绍PackageServiceManager。
##### 显示快捷方式
这些应用程序只是相当于在PackageManagerService服务注册好了，如果我们想要在Android桌面上看到这些应用程序，还需要有一个Home应用程序，负责从PackageManagerService服务中把这些安装好的应用程序取出来，并以友好的方式在桌面上展现出来，例如以快捷图标的形式。在Android系统中，负责把系统中已经安装的应用程序在桌面中展现出来的Home应用程序就是Launcher了
##### 保存安装信息
将app的包名、版本号、安装路径等保存在data/system/packages.xml文件中，以备下次安装时再次使用；