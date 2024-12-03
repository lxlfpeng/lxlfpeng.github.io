---
title: Android APK反编译及逆向工程
---

# 一. 分析已经打好的apk.
首先来简单的说明下Apk文件本质上其实是一个zip包。我们直接进行解压就能看到其中的目录。
![目录](/images/91cbf5f8d83bfb7ef4641b57775dfd34.webp)
#### 1. 目录说明
*   AndroidManifest.xml：应用的全局配置文件
*   classes.dex：源代码编译成class后，转成jar，再压缩成dex文件，dex是可以直接在Android虚拟机上运行的文件。
*   lib文件夹：引用的第三方sdk的so文件。
*   META-INF文件夹：Apk签名文件。
*   res文件夹：资源文件，包括了布局、图片等等。
*   resources.arsc：记录资源文件和资源id的映射关系。
*   其中还有一个没有显示就是→assets文件夹：原始资源文件夹，对应着Android工程的assets文件夹，一般用于存放原始的网页、音频等等。

上述的这些说明 简单的说明了一个apk基本包含的东西，直接把apk解压是没有办法进行阅读的，在打包这个过程中经过了build-tools处理了。

其实反编译Apk的目的就是Apk拆成我们可以阅读的文件。通过反编译，我们一般想要得到里面的AndroidManifest.xml文件、res文件和java代码。

xml文件都不能直接被识别了这是因为:xml文件都被aapt编译成二进制的xml文件,将文本格式的xml转为二进制格式的xml原因有以下两点:二进制格式的XML文件占用空间更小;二进制格式的XML文件解析速度更快。

# 二. 反编译工具
### 1.使用ApkTool 反编译APK获取清单文件及布局文件
可以利用[ApkTool](https://ibotpeaches.github.io/Apktool/)，获取AndroidManifest和res等资源文件:
功能：拆解Apk文件，反编译其中的资源文件，将它们反编译为可阅读的AndroidManifest.xml文件和res文件。因为直接把Apk文件当做zip解压，得到的xml资源文件，都是无法直接用文本编辑器打开阅读的，因为它们在打包时经过了build-tools的处理变成了二进制的XML。
##### (1.) 安装ApkTool
[ApkTool](https://ibotpeaches.github.io/Apktool/install/) 需要的环境是jdk 1.7以上
-   下载apktool-2（[最新](https://bitbucket.org/iBotPeaches/apktool/downloads/)）。
-   将下载的jar重命名为 apktool.jar。
-   将这两个文件（apktool.jar＆apktool.bat）移动到您的Windows目录（通常C://Windows）。
-   如果没有访问权限C://Windows，可以将这两个文件放在任何位置，然后将该目录添加到您的环境变量系统PATH变量。
-   尝试apktool通过命令提示符运行。
##### (2.) 使用ApkTool
完成安装的步骤以后，上述说到如果你把文件移动到其他的位置，就需要配置环境变量。首先进入到你想要 反编译的apk 目录下，这里就放置到一起了。
![](/images/d70ebb6a90dad8e1a058c1559bb32e8e.webp)
通过``java -jar apktool.jar d xx.apk``命令执行jar程序，可以从下图看到反编译出来的具体内容：
![](/images/6dcaacbc12335b34ed5219557600d610.webp)
已经得到一个可以用文本编辑器打开的阅读的AndroidManifest.xml文件、assets文件夹、res文件夹、smali文件夹等等。这样，我们就可以查看到这个Apk文件的package包名、Activity组件、程序所需要的权限、xml布局、图标等等信息。smali文件夹是反编译出来的代码，需要进行相应的学习才能看懂。

```
java -jar apktool.jar d xx.apk
```
- -f 如果目标文件夹已存在，强制删除现有文件夹
- -o 指定反编译的目标文件夹的名称（默认会将文件输出到以Apk文件名命名的文件夹中）
- -s 保留classes.dex文件（默认会将dex文件解码成smali文件）
- -r 保留resources.arsc文件（默认会将resources.arsc解码成具体的资源文件）
> 注意`apktool.jar`是刚才下载后的jar的名称，`d`参数表示decode，在这个命令后面还可以添加像`-o -s`之类的参数，例如java -jar apktool.jar d yourApkFile.apk -o destiantionDir -s。

[更多详细用法参考官方文档](https://ibotpeaches.github.io/Apktool/documentation/)

### 2. 使用dex2jar反编译dex文件，得到java源代码
##### (1. )dex2jar的功能
上文通过apkTool反编译获得apk 等资源文件，获得的smali需要进行系统的学习才能看懂。如果想获取能看懂的源代码，这时候就需要dex2jar登场了。
dex2jar的作用就是将dex格式的文件，转换成jar文件。dex文件是Android虚拟机上面可以执行的文件，jar文件大家都是知道，其实就是java的class文件。在[官网](https://github.com/pxb1988/dex2jar)有详细介绍。
工具地址： [dex2jar](https://github.com/pxb1988/dex2jar)
##### (2. )dex2jar的安装
打开下载的文件进行解压后进入/dex2jar目录下，里面有脚本，进入终端后，输入命令就可以使用。
利用终端进入到你的dex2jar目录下，输入命令进行获取
![](/images/4bb8534afe1a73b07866991f0ef05024.webp)
把apk解压下来就能获得classes.dex文件，之后赋值到dex2jar目录下 ，执行命令。

这个时候又有人问我了（怎么这么多人问我），我怎么看生成的这个jar包呀。这个时候就需要 jd-gui了

### 3. 使用jd-gui查看jar里面的java源代码
[jd-gui](https://github.com/java-decompiler/jd-gui)用法： 下载完成后直接打开，把生成的classes-dex2jar.jar 文件直接拖到里面就可以查看了
![](/images/bd10e1068adb7395c19c540512bdd0fd.webp)

### 4.使用jadx反编译Apk，得到可以阅读的.java源代码
##### (1.)jadx介绍
jadx可以直接对Apk进行反编译直接生成.java文件，相当于是apktool+dex2jar+jd-gui反编译的组合。jadx具有以下两个优点：
- 可以直接反编译出.java文件。
-   查看源码时直接显示资源名称，而不是像jd-gui里显示的资源ID。

工具官方地址 ：
-   github: [https://github.com/skylot/jadx/releases](https://github.com/skylot/jadx/releases)
-   sourceforge: [http://sourceforge.net/projects/jadx/files/](http://sourceforge.net/projects/jadx/files/)
##### (2.)jadx安装使用
下载完成后进行解压，进入bin目录下执行jadx-gui.bat，jadx也有GUI，进入后选中然将要反编译的apk即可，运行效果如下：

![](/images/eda469651332ab1af4612de13d9e70e6.webp)

如果要保存源码，选择File->Save ALL即可保存文件，然后就可以导入Android Studio等IDE中。我们也可以直接使用命令行反编译apk文件：
- jadx -d out classes.dex #直接输出.java文件到out目录
- jadx-gui classes.dex #使用gui打开

>使用jadx大大简化了反编译流程，不过获取资源等文件还是建议使用ApkTool。

### 5. 使用ClassyShark对APK反编译
[ClassyShark](https://github.com/google/android-classyshark/releases)是Google发布的一款可以查看Android可执行文件的浏览工具，支持.dex, .aar, .so, .apk, .jar, .class, .xml 等文件格式，分析里面的内容包括classes.dex文件，包、方法数量、类、字符串、使用的NativeLibrary等。
```
打开apk文件java -jar ClassyShark.jar -open xx
```

# 三. Android 逆向工程.
![总览](/images/045dbc43eb855db9d2fe4210a4dd964f.webp)

### 1. 新建一个app在MainActivity中输出一个toast,然后打包出来用于反编译,。
```
public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Toast.makeText(this, "未修改之前!", Toast.LENGTH_SHORT).show();
    }
}
```
### 2. ApkTool进行反编译,修改文件,然后打包.
##### (1.) 下载apktool
[ApkTool的github地址](https://github.com/iBotPeaches/Apktool)
##### (2.) 将apktool.jar和需要反编译的apk放到同一个文件夹下面,shift+鼠标右键,选择在此处打开命令提示符。
```
java -jar apktool.jar d test.apk
```
![image.png](/images/b3795a54bb877ce9c89ecf06374909bf.webp)
`d`参数表示decode
在这个命令后面还可以添加像`-o -s`之类的参数，例如// java -jar apktool.jar d yourApkFile.apk -o
- -o 指定反编译的目标文件夹的名称（默认会将文件输出到以Apk文件名命名的文件夹中）
- -s 保留classes.dex文件（默认会将dex文件解码成smali文件）
- -r 保留resources.arsc文件（默认会将resources.arsc解码成具体的资源文件）  
  ![image.png](/images/44bbec2e5e12134b6dfa3efcdbf8692e.webp)
##### (3. )我们可以从下图看到反编译出来的具体内容:
![Android反编译工具总结](/images/637fd7a0ca6c03c3f3e3253a204df524.webp)
我们已经得到一个可以用文本编辑器打开的阅读的AndroidManifest.xml文件、assets文件夹、res文件夹、smali文件夹等等。original文件夹是原始的AndroidManifest.xml文件，res文件夹是反编译出来的所有资源，smali文件夹是反编译出来的代码。
这时，我们已经可以文本编辑器打开AndroidManifest.xml文件和res下面的layout文件了。这样，我们就可以查看到这个Apk文件的package包名、Activity组件、程序所需要的权限、xml布局、图标等等信息。

##### (4. )修改smail文件.找到MainActivity.smail文件里吐司输出的内容,进行替换
![image.png](/images/fabef00d952aebc4f6b2dd5e7e92fdc4.webp)
![image.png](/images/8965743abe6ab0866c421e25380a86e4.webp)

##### (5. )使用打包命令对源码进行打包.**
```
apktool b app -o other.apk（app 指需要打包的文件夹，-o other.apk 表示生产新文件）
```
##### (6. )对apk进行签名.然后安装。**
![image.png](/images/308ebabafbb083398be7888ab2f43a91.webp)
![image.png](/images/7b9cbb90cc07c3ca4ae0b8f0e16ba0e2.webp)

# 四. APK加固脱壳.
众所周知，Android应用开发完成后，除了使用Google官方的混淆外，还需要使用一些第三方的安全软件的加壳处理，比较出名的有腾讯乐固、360加固和爱加密等。加固工具的出现，让反编译的难度更大。但是有了加固技术，就会有反加固技术。
经过加固后的apk，通过dex2jar反编译：
腾讯乐固：
![](/images/854eebe31f9c20fca32322b1ce92f336.webp)

360加固：
![](/images/e740ebbfc2e599982c168f7879e1a6c9.webp)
从上面可以看出，经过加固后的apk，通过常规方法反编译无法获取到源码。

所谓Apk加固，就是给目标Apk加一层保护程序，把重要数据信息隐藏起来。加壳程序可以有效 阻止对程序的反编译和逆向分析。Apk加固本质的功能就是实现类加载器。系统先执行加固壳代码，然后将加了密的dex进行解密操作，再加载到系统内存中运行。

>由于加固方式会不断的升级，因此加固脱壳技术也是有时效性的，必须要要与时俱进才能完成反编译，因此本文暂不对加固脱壳方法进行着墨。有兴趣可以去如下论坛找寻相关资料进行阅读：
[看雪论坛](https://bbs.pediy.com/forum-161.htm)
[吾爱破解](https://www.52pojie.cn)
[Android APK脱壳--腾讯乐固、360加固一键脱壳](https://www.jianshu.com/p/138c9de2c987)