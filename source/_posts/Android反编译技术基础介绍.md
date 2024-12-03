---
title: Android反编译技术基础介绍
---

# 一.APK简介
APK的全称是Android application package，它是Android平台的应用程序包。我们可以在网上下载到各种各样的apk文件，然后将APK文件安装到安卓设备以后就可以打开运行APP程序。
从本质上来说Apk文件其实就是一个压缩文件，类似zip和rar包，它里面包含编译过后的**代码**，**图片，视频，音频等媒体**和**资源文件**等内容。
## 安卓APK打包流程
那么APK文件是如何打包的呢？安卓开发将应用程序开发完成以后，会通过google官方提供的打包脚本对源代码和资源文件进行编译打包，打包完成以后我们才可以将打包好的APK文件分发到各个应用市场和分发平台，具体的打包的流程如下图所示:
![安卓打包流程图](/images/619d48b75672cc67f830ef426a3069f8.webp)
1. 通过**aapt/aapt2**工具打包资源文件
   在这个过程中项目中的AndroidManifest.xml文件和XML布局文件都会被编译，然后生成相应的R.java文件，AndroidManifest.xml和res目录下的xml资源文件会被aapt工具编译成二进制文件。并生成一个resource.arsc文件，resource.arsc文件相当于一个文件索引表，记录了很多跟资源相关的信息。
2. 通过**aidl工具**处理aidl文件，生成相应java文件
   这一过程中aidl工具解析接口定义文件然后生成相应的Java代码接口供程序调用。如果在项目没有使用到aidl文件，则可以跳过这一步。
3. 通过**javac**工具编译工程源代码，生成相应class文件
   项目中所有的Java代码，包括R.java和.aidl文件，都会被Java编译器（javac）编译成.class文件。
4. 通过**dx工具**转换所有class文件，生成classes.dex文件
   dx工具的主要工作是将Java字节码转成成Dalvik字节码、压缩常量池、消除冗余信息等。任何第三方的libs和.class文件都会被转换成.dex文件。
5. 通过**apkbuilder**工具打包生成apk
   所有没有被编译的资源，如images、assets目录下资源编译过的资源和.dex文件都会被打包到最终的.apk文件中。
6. 通过**jarsigner/apksigner**对apk文件进行签名
   一旦APK文件生成，它必须被签名才能被安装在设备上。签名确保APK文件的完整性和安全性。
7. 通过**zipalign**对apk文件对齐
   将apk包进行对齐处理，使apk包中的所有资源文件距离文件起始偏移为4字节整数倍，这样通过内存映射访问apk文件时速度会更快

通过上文我们了解到打包过程就是一个编译、加密和打包的过程，因此逆向工程技术就是解压和解密APK包的过程。

# 二.什么是Android反编译技术?
Android反编译技术是一种针对于安卓平台的**逆向工程技术**，通过对第三方应用进行“**逆向分析、研究**”工作，推测出APP的算法、原理、结构、逻辑、敏感数据等核心要素，在某些特定情况下可能推导出源代码逻辑。
上文我们提到了Apk文件本身就是一个包含编译过的源代码，图片，视频，音频等资源文件的压缩包。那么我们是否可以使用解压缩软件对其进行解压缩呢？答案是肯定的，可以将apk文件后缀改为rar，用解压工具就能将apk文件解压了，解压完成目录如下如图所示。
![apk解压目录](/images/95c7f97352d2e77d8d58feb473be1e06.webp)

>需要注意的是：不同的apk文件解压后的内容不尽相同，但分析的思路都是一样的，有些使用了加壳措施的apk，由于加壳方案不一样，所以资源文件和dex文件的处理会有差异。

* assets目录：包含资源文件，如声音、字体等等。
* lib目录：存放用C/C++编写用NDK编译生成的so文件，供java/kotlin端调用。
* META-INF目录：存放apk签名信息，用来保证包的完整性和系统的安全。在IDE编译生成一个apk包时，会对里面所有的文件做一个校验计算，并把计算结果存放在META-INF文件夹内，apk在安装的时候，系统会按照同样的算法对apk包里面的文件做校验，如果结果与META-INF里面的值不一样，系统就不会安装这个apk，这就保证了apk包里的文件不能被随意替换。比如拿到一个apk包后，如果想要替换里面的一幅图片，一段代码， 或一段版权信息，想直接解压缩、替换再重新打包，那么就不能够覆盖安装了。如此一来就给病毒感染和恶意修改增加了难度，有助于保护系统的安全。
* res目录：存放资源文件，包括icon，xml文件包括了布局、图片等等。
* AndroidManifest.xml文件： 应用配置文件，它描述了应用的包名、名字、版本、权限以及注册的组件等。
* classes.dex文件：
  - 可以直接在Dalvik虚拟机上加载运行的文件，由java/kotlin文件经过编译生成。
  - Dalvik虚拟机的指令码不是标准的Jvm指令码，而是使用了自己独有的一套指令集。
  - dex文件中共用了很多类名称，常量字符串，使它的体积更小，运行效率更高。
  - 为了突破65536个方法数的限制，所以可能会有多个classes.dex。
* resources.arsc文件：二进制资源文件，包括字符串等，记录了资源文件和资源id的映射关系。

虽然通过直接解压缩，我们能看到apk包里面的内容，但是我们直接用文本编辑器打开这些xml文件会发现都是些乱码，没法直接阅读。这是因为xml文件都被aapt编译成二进制的xml文件，这么做的原因有以下两点:二进制格式的XML文件占用空间更小;二进制格式的XML文件解析速度更快。

>所以如果需要查看apk的所有文件内容，必需用到反编译工具对其进行解包才行。

# 三.APK反编译工具及使用
## 常用的APK反编译工具
- [Apktool](https://apktool.org/docs/install/) ： APKTool是一个开源的、跨平台的反编译、回编译 Android 应用程序的工具。它能够将 APK 文件解压并还原成 Android 应用程序的资源文件和 Smali 代码，还能将修改后的资源文件和 Smali 代码重新打包成 APK 文件。
- [dex2jar](https://ibotpeaches.github.io/Apktool/install/)： 能将 dex 转化为 jar 文件。
- [jd-gui](https://sourceforge.net/projects/dex2jar/files/)： 能将 jar 文件反编译为便于阅读的java源代码。
- [jadx](https://github.com/skylot/jadx/releases)： 一款图形化的APK反编译工具，操作简便，集成了Apktool + dex2jar + jd-gui这三个工具的功能。
- [AndroidKiller](https://github.com/liaojack8/AndroidKiller)：Android Killer是一款为用户提供图形化界面的反编译工具，它集成了APK反编译、APK签名、编码转换、APK文件打包等多种功能。

下面就通过ApkTools来实现两个比较简单的反编译例子：
## 实例一: 修改APK的名称然后再次打包
1. 首先使用ApkTools进行解包:
    ```
    java -jar apktool.jar d test.apk -o <output_dir>
    ```
    其中<output_dir>指定输出目录，默认为源文件名。

2. 修改应用名称
   反编译完成后，我们可以尝试修改 apk 内容了，我们这里尝试修改 App 名字，方法也简单，在直接修改清单文件的属性值
    ```
    <?xml version="1.0" encoding="utf-8" standalone="no"?>
    <manifest
        xmlns:android="http://schemas.android.com/apk/res/android"
        package="com.xxx.xxx"
        platformBuildVersionCode="25"
        platformBuildVersionName="7.1.1">
        
        <uses-permission android:name="android.permission.SYSTEM_ALERT_WINDOW"/>
        
        <application 
            android:allowBackup="true"
            android:icon="@mipmap/ic_launcher"
            android:label="我是被反编译修改过的名字"
            android:supportsRtl="true"
            android:theme="@android:style/Theme.Holo.Light.DarkActionBar">
        </application>
    </manifest>
    ```
3. 再次通过使用ApkTools进行回编成APK包:
    ```
    java -jar apktool.jar b <input_dir> -o <output.apk> 
    ```
    其中<input_dir>就是上面反编译输出的目录，<ouput.apk>是编译的输出结果，默认为input_dir.apk

4. 使用签名工具对Apk包进行签名:
   ```
   apksigner sign --ks peng.jks --ks-key-alias peng --out app-release-change-signed.apk app-release-change.apk
   ```
   这里使用的apksigner脚本来对APK再次进行签名操作。

5. 安装运行

   将重新打包签名过后的APK安装到Android设备上就可以发现app的名称被修改了 。

## 实例二: 修改源代码里面的原有逻辑
1. 首先使用ApkTools进行解包:
    ```
    java -jar apktool.jar d test.apk -o <output_dir>
    ```
    其中<output_dir>指定输出目录，默认为源文件名。

2. 找到需要替换逻辑的地方:
   
   需要注意的是解包出来的代码是Smali代码。Smali是一种基于Dalvik虚拟机的汇编语言，用于描述Android应用程序的字节码。

3. 再次通过使用ApkTools进行回编成APK包:
    ```
    java -jar apktool.jar b <input_dir> -o <output.apk> 
    ```
    其中<input_dir>就是上面反编译输出的目录，<ouput.apk>是编译的输出结果，默认为input_dir.apk

4. 使用签名工具对Apk包进行签名:
   ```
   apksigner sign --ks peng.jks --ks-key-alias peng --out app-release-change-signed.apk app-release-change.apk
   ```
   这里使用的apksigner脚本来对APK再次进行签名操作。

5. 安装运行

   将重新打包签名过后的APK安装到Android设备上就可以发现之前的代码逻辑被替换成我们新的了。


# 四.Android反编译技术的应用
通过上面两个实例我们成功实现了对第三方APK的反编译工作，不但修改了资源文件还对原有的代码逻辑进行了修改。一般反编译还可以运用在如下的这些方面:

### 1.参考竞品的代码实现逻辑
在开发中我们难免会参考竞品来实现自身的业务功能逻辑，很多时候我们制定实现方案的时候，可以反编译竞品APP看下它的布局和代码实现逻辑方案，这样可以节省很多的成本和时间。

### 2.屏蔽应用的广告
在使用APP的时候各种开屏广告，弹窗广告，让人不厌其烦，而且很多APP并不提供关闭这些广告的设置功能，这时我们可以通过反编译解包找出广告相关的逻辑代码，然后进行屏蔽，再重新编译打包，这样烦人的广告就彻底被消灭掉了。

### 3.制作汉化应用
很多国外的工具类APP，不但品质非常高，而且功能比较强大，但是很多这类型的APP并没有提供汉语的多语言设置，例如Re文件管理器，这对于国内玩家来说显然是不够友好，我们也可以通过反编译找到字符串资源文件，然进行翻译替换，再重新编译打包，这样就实现了汉化的功能。

### 4.通过修改包名制作应用分身
在Android设备上，同一个包名的应用只能允许安装一个，如果我们想要实现应用的分身，除了在系统层面的支持，还可以通过反编译修改包名，然后再重新编译打包来实现，这样便获得了两个相同内容但是不同包名的APP，可以互相使用并不会造成冲突。

### 5.制作破解包
一些需要授权或者收费的游戏和应用，可以通过反编译找到授权或者收费的逻辑，进行绕过，这样便可以免费使用。

### 6.制作山寨换皮应用
新闻经常报道一些不法分子会通过修改应用图标和应用程序名称实现个性化应用，甚至可以通过修改应用程序配置参数（内置统计参数、支付平台参数、广告参数）、植入病毒代码等方式把别人的应用变为自己的应用，重新打包然后上传到应用分发平台进行牟利。不明真相的用户将带病毒广告的apk下载下来进行安装使用，甚至因此造成利益损失。所以我们下载应用的时候一定要注意去正规的app分发渠道进行下载。

# 五.如何防止APK包被别人反编译?
既然通过反编译可以做这么多的事情，那么作为软件开发厂商要如何防止自己辛辛苦苦开发的应用尽量不被别人偷窥和窃取呢?

## 1.做代码混淆
混淆代码（Code obfuscation）：混淆代码是一种常见的反编译防护方法。混淆工具将源代码中的标识符（变量、方法、类名等）进行重命名，使其变得难以理解和推断。这样，即使应用被反编译，攻击者也很难理解代码的含义和逻辑。如下便是没有混淆过的代码和有混效果的代码的区别:

![代码未混淆](/images/937549e9f163af5640888e91afec438d.webp)

![代码已混淆](/images/649692124c68e61767e208c82777e6aa.webp)

## 2.使用加固技术进行加固
加固的核心原理是对dex文件进行加密操作，然后替换掉应用程序自己的启动类，在App启动的时候，再通过密钥对dex等文件进行解密，然后再使用ClassLoader加载解密出来的代码，因此，一般做了加固操作的应用冷启动时间都会变长，市场主流加固方案：腾讯乐固、爱加密、360、梆梆加固等厂商提供相对应的方案。

## 3.将保密逻辑使用C/C++进行编写
该方案是使用.so动态库技术，该技术实现是将重要核心代码全部放在C/C++文件中，利用NDK技术，将核心代码编译成.so动态库，再用JNI进行调用。相比较于java写的核心逻辑本地语言更难被破解。

## 4.使用签名验校防止应用被重新打包
在上文中虽然我们可以对APk解包然后回编，但是我们拿不到应用本身的签名文件对APK进行签名，只能用自己的签名文件对apk进行签名，因此我们通过对签名文件的指纹进行验证，来判断APk是否被再次编译打包过。

# 总结
需要注意的是上述的方案作用主要是提高ApK的逆向成本，降低软件被破解的几率，并不能保证一定不会被破解，因为客户端经过分发出去以后，每个人都可以拿到客户端的包，因此想要对其进行攻破只是时间长度问题，而要攻破服务器端则是相当困难，所以将重要的逻辑放在服务端处理，做好容灾，就算是客户端被破解了，也不会造成大的损失。



Android 逆向工程技术是一门非常庞大的知识体系(如下图)，今天只是和大家分享了一下入门知识和概念。
![逆向工程](/images/98ae3b9f3fa45afc696644cac56ccdbc.webp)

