---
title: Android虚拟机之Dalvik和ART
---

# 一.Java平台的虚拟机Jvm
### 1.Jvm的作用
Java语言的一个非常重要的特点就是``与平台的无关性(跨平台性)``，经常会听到一句关于java特性的话："一次编译到处执行"。由于机器只能识别机器码，所以需要通过Java 编译器将 .java 文件转换成 .class文件，也就是字节码文件，最后将字节码提供给 JVM，由 JVM 将它转换成机器码。
![](https://upload-images.jianshu.io/upload_images/3067896-eaee09f21a9c3fc3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 2.Jvm分析
Jvm相关知识体系过于庞大，有兴趣可以看本人之前的文章:[JAVA JVM详解](https://blog.csdn.net/unreliable_narrator/article/details/97135880)
# 二.Dalvik虚拟机
### 1.为什么Android平台不使用标准的Jvm虚拟机?
由于 Androd 运行在移动设备上，内存以及电量等诸多方面跟一般的 PC 设备都有本质的区别 ，一般的 JVM 没法满足移动设备的要求，所以Android 团队一开始就打造了一个符合移动设备的可以执行 Java 代码的虚拟机，这就是说的 Dalvik 虚拟机 。

### 2. Android平台Dalvik虚拟机的特点
- 体积小，占用内存空间小。
- 专有的DEX可执行文件格式，体积更小，执行速度更快。
- 基于寄存器架构，并拥有一套完整的指令系统。
  
>android为每个应用程序提供一个Dalvik虚拟机，可以使每个app都运行在独立的虚拟机运行环境，使稳定性提高。使得应用代码和核心的操作系统分开。即使任意一个程序中包含恶意的代码也不会直接影响系统文件。这使得 Android 操作系统更稳定可靠。


### 3.Jvm和Dalvik比较
##### (1.)Jvm和Dalvik的相同点
- 都是解释执行。
- 都是每个 OS 进程运行一个 VM，并运行一个单独的程序。
- （Android Froyo / Sun JDK 1.5）都实现了相当程度的 JIT compiler（即时编译） 用于提速。JIT（Just In Time，即时编译技术）对于热代码（使用频率高的字节码）直接转换成汇编代码；

##### (2.)Jvm和Dalvik的不同点
- Dalvik执行的是.dex格式文件，Jvm执行的是.class文件。多个class文件转变成一个dex文件会引发一些问题，具体如下：
  1. 方法数受限：多个class文件变成一个dex文件所带来的问题就是方法数超过65535时报错，由此引出MultiDex技术。
  2. class文件去冗余：class文件存在很多的冗余信息，dex工具会去除冗余信息(多个class中的字符串常量合并为一个，比如对于Ljava/lang/Oject字符常量，每个class文件基本都有该字符常量，存在很大的冗余)，并把所有的.class文件整合到.dex文件中。减少了I/O操作，提高了类的查找速度。

- JVM是基于栈，Dalvik指令集是基于寄存器的架构。具体如下：
  1. Dalvik速度快！寄存器存取速度比栈快的多，Dalvik可以根据硬件实现最大的优化，比较适合移动设备。JAVA虚拟机基于栈结构，程序在运行时虚拟机需要频繁的从栈上读取写入数据，这个过程需要更多的指令分派与内存访问次数，会耗费很多CPU时间。
  2. 指令数小！Dalvik基于寄存器，所以它的指令是二地址和三地址混合，指令中指明了操作数的地址；Jvm基于栈，它的指令是零地址，指令的操作数对象默认是操作数栈中的几个位置。这样带来的结果就是Dalvik的指令数相对于Jvm的指令数会小很多，Jvm需要多条指令而Dalvik可能只需要一条指令。
  3. Jvm基于栈带来的好处是可以做的足够简单，真正的跨平台，保证在低硬件条件下能够正常运行。而dvm操作平台一般指明是ARM系统，所以采取的策略有所不同。需要注意的是Dalvik基于寄存器，但是这也是个映射关系，如果硬件没有足够的寄存器，Dalvik将多出来的寄存器映射到内存中。

![](https://upload-images.jianshu.io/upload_images/3067896-421f10fd05b70b6f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 4.JIT编译
Dalvik虚拟机可以看做是一个Java VM(虚拟机)， Android系统初期，每次运行程序的时候，Dalvik负责将dex翻译为机器码交由系统调用。这样有一个缺陷：每次执行代码，都需要Dalvik将dex代码翻译为微处理器指令，然后交给系统处理，这样效率不高。为了解决上述问题，Google在Android2.2版本添加了JIT编译器。

JIT编译器的作用是：当App运行时，每当遇到一个新类，JIT编译器就会对这个类进行编译，经过编译后的代码，会被优化成相当精简的原生型指令码（即native code），这样在下次执行到相同逻辑的时候，速度就会更快。
![](https://upload-images.jianshu.io/upload_images/3067896-4abb497d80e7faa6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

>当然使用JIT也不一定加快执行速度，如果大部分代码的执行次数很少，那么编译花费的时间不一定少于执行dex的时间。Google当然也知道这一点，所以JIT不对所有dex代码进行编译，而是只编译执行次数较多的dex为本地机器码。有一点需要注意，那就是dex字节码翻译成本地机器码是发生在应用程序的运行过程中的，并且应用程序每一次重新运行的时候，都要做重做这个翻译工作，所以这个工作并不是一劳永逸，每次重新打开App，都需要JIT编译。JIT 编译器可以对执行次数频繁的 dex/odex 代码进行编译与优化，将 dex/odex 中的 Dalvik Code（Smali 指令集）翻译成相当精简的 Native Code 去执行。

### 5.JIT编译的缺点
- 每次启动应用都需要重新编译（没有缓存）。
- 运行时比较耗电，耗电量大。

# 三.ART虚拟机
### 1.ART虚拟机和AOT编译
JIT是运行时编译，是动态编译，可以对执行次数频繁的dex代码进行编译和优化，减少以后使用时的翻译时间，虽然可以加快Dalvik运行速度，但是有一个很大的问题：将dex翻译为本地机器码也要占用时间，这会拖慢应用的运行效率。 所以Google在4.4推出了全新的虚拟机运行环境ART（Android RunTime），用来替换Dalvik（4.4上ART和Dalvik共存，用户可以手动选择，5.0 后Dalvik被替换）。在ART 环境中，应用在第一次安装的时候，字节码就会预先编译成机器码，使其成为真正的本地应用。这个过程叫做预编译AOT（Ahead-Of-Time）。这样，应用的启动(首次)和执行都会变得更加快速。

``ART虚拟机直接执行本地机器码；而Dalvik虚拟机运行的是DEX字节码需要通过解释器执行。``安卓运行时从Dalvik虚拟机替换成ART虚拟机，并不要求开发者重新将自己的应用直接编译成目标机器码，应用程序仍然是一个包含dex字节码的apk文件，这主要得益于AOT技术，AOT（Ahead Of Time）是相对JIT（Just In Time）而言的；也就是在APK运行之前，就对其包含的Dex字节码进行翻译，得到对应的本地机器指令，于是就可以在运行时直接执行了。ART应用安装的时候把dex中的字节码将被编译成本地机器码，之后每次打开应用，执行的都是本地机器码。去除了运行时的解释执行，效率更高，启动更快。

### 2.ART缺点
- 应用安装需要更长的时间，因为 DEX 字节码需要在安装时就翻译成机器码。
- 由于在安装时时生成的 native 机器码是存储在内部存储器上，所以需要更多的内部存储空间。

### 3. JIT和AOT共存
由于Art虚拟机有上述的缺点，所以在Android 7.0/7.1的ART引入了全新的Hybrid模式(JIT + AOT)
- app在安装的时候dex不会再被编译，所以安装速度快。
- 应用在运行时 dex 文件先通过解析器（Interpreter）后会被直接执行（这一步骤跟 Android 2.2 - Android 4.4之前的行为一致），与此同时，热点函数（Hot Code）会被识别并被 JIT 编译后存储在 jit code cache 中并生成 profile 文件以记录热点函数的信息。
- 手机进入 IDLE（空闲） 或者 Charging（充电） 状态的时候，系统会每隔一段时间扫描App目录下profile文件，并执行AOT编译(Google官方称之为profile-guided compilation)。

##### (1.) JIT+AOT优点
App安装速度快，占用存储少(只编译热点函数)。

##### (2.) JIT+AOT缺点
前几次运行会较慢， 只有用户操作得次数越多，jit 和AOT编译后， 性能才会跟上来。

# 四.Android虚拟机总结
![](https://upload-images.jianshu.io/upload_images/3067896-567f658452e54ede.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

参考资料:
[Android学习笔记——虚拟机](http://mouxuejie.com/blog/2018-05-12/learning-notes-vm/)
[JVM原理最全、清晰、通俗讲解](https://blog.csdn.net/csdnliuxin123524/article/details/81303711)
