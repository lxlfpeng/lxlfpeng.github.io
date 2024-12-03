---
title: Linux部署Android打包环境
---

# 一.配置JDK、Gradle、Git环境
### 1.安装Java环境
##### (1.)通过apt-get安装Java环境
```
apt-get update
apt-get install openjdk-8-jdk
```
##### (2.)通过软件包安装Java环境
1. 下载[JDK下载地址](https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html)。
2. 解压安装包。
3. 配置环境变量。
```
$ mv jdk1.8.0_161 /usr/local/
$ ln -s /usr/local/jdk1.8.0_161 /usr/local/jdk
$ vim /etc/profile     #配置JDK的环境变量

export JAVA_HOME=/usr/local/jdk
export PATH=$JAVA_HOME/bin:$JAVA_HOME/jre/bin:$PATH
export CLASSPATH=.$CLASSPATH:$JAVA_HOME/lib:$JAVA_HOME/jre/lib:$JAVA_HOME/lib/tools.jar

$ source /etc/profile    #重新加载系统环境变量
$ java -version    #查看java版本
```
>如果vim无法粘贴文本可以用shift+insert试试
### 2.安装Gradle环境
1. 创建安装文件夹。
```
mkdir gradle
```
2. 进入Gradle文件夹下载Gradle。
```
wget https://downloads.gradle-dn.com/distributions/gradle-6.5-bin.zip
```
3. 解压。
```
unzip gradle-6.5-bin.zip
```
4. 配置环境变量。
```
$ vim /etc/profile     #配置Gradle的环境变量

export GRADLE_HOME=/gradle
export PATH=$PATH:$GRADLE_HOME/gradle-6.5/bin

$ source /etc/profile    #重新加载系统环境变量
$ gradle -v              #查看gradle版本
```
>注意gradle版本发布太快,每一个版本都需要配置一个环境变量,因此实际开发中我们一般使用gradle_wrapper来对gradle进行配置。
### 3.安装git环境
1. 安装git。
```
apt install git
```
2. 查看git版本。
```
git --version
```

# 二.配置Android环境
配置android编译环境有两种方式:
1. 将Android编译需要用到的工具在宿主机上面下载好,通过xftp等方式复制到容器中然后配置。
2. 在docker容器中自行下载配置。
**第一种方式非常简单我们这里详细讲解一下第二种方式。**
### 1. 进入Dokcer容器
以root用户登录docker容器:
```
sudo docker exec -it -u root ec33c19230ca /bin/bash
```

### 2.创建Android_Sdk安装文佳夹
在合适的目录创建文件夹(例如根目录)创建文件夹 /android/sdk:
```
mkdir -p /android/sdk
cd /android/sdk
```

### 3.安装wget下载包
1. Debian/Ubuntu系统安装wget:
```
apt-get update
apt-get -y install wget
```
2. CentOS系统安装wget:
```
yum install wget -y
```

### 4.下载sdkmanager工具包
```
wget https://dl.google.com/android/repository/commandlinetools-linux-7583922_latest.zip
```
查看最新版本
[官网](https://developer.android.google.cn/studio)

### 5.解压缩sdkmananger工具包
```
unzip xxxxxxxx.zip 
```
解压完成我们会看到有一个cmdline-tools文件夹,此时的目录结构为:
```
/android/sdk/cmdline-tools
```

### 6.调整目录结构
如果解压以后直接cd到``/cmdline-tools/bin/``执行``./sdkmanager --version``会报以下错误:
```
Warning: Could not create settings
java.lang.IllegalArgumentException
    at com.android.sdklib.tool.sdkmanager.SdkManagerCliSettings.(SdkManagerCliSettings.
    at com.android.sdklib.tool.sdkmanager.SdkManagerCliSettings.createSettings(SdkManagerCliSettings.
    at com.android.sdklib.tool.sdkmanager.SdkManagerCliSettings.createSettings(SdkManagerCliSettings.
    at com.android.sdklib.tool.sdkmanager.SdkManagerCli.main(SdkManagerCli.
    at com.android.sdklib.tool.sdkmanager.SdkManagerCli.main(SdkManagerCli
```
因此我们需要对目录结构做一些调整:
```
mv /android/sdk/cmdline-tools /android/sdk/last
mkdir -p /android/sdk/cmdline-tools
mv /android/sdk/last /android/sdk/cmdline-tools/last
```
最终如下目录结构如下:
```
/android/sdk/cmdline-tools/last
```

### 7.修改环境变量
因为没有配置sdkmanager的环境变量,所以每次都要进入``cmdline-tools/last/bin``文件夹才能执行sdkmanager脚本的操作,因此我们需要先对sdkmanager进行环境变量的配置:
1. 打开环境变量文件
```
vim /etc/profile 
```
2. 添加sdkmanager的环境变量
```
export ANDROID_HOME=/android/sdk
export PATH=$PATH:$ANDROID_HOME/cmdline-tools/last/bin
```
3. 刷新环境变量
```
source /etc/profile 
```
4. 查看环境变量
```
echo $PATH 
```
配置好以后就可以在任何地方都可以使用sdkmanager脚本了.

### 8.下载android_sdk
[sdkmanager](https://developer.android.google.cn/studio/command-line/sdkmanager)
``sdkmanager --list``:可以看到列出的AndroidSDK一系列工具包，包括已安装和未安装的包。
如果要安装某个包，比如platform下的android-29的版本的包:
```
sdkmanager "build-tools;29.0.0" "platforms;android-29" "platform-tools" 
```
如果要删除已经下载的包，比如platform下的android-29的版本的包:
``` 
sdkmanager --uninstall "platforms;android-29"
```
如果国内下载速度太慢,可以配置一下国内的镜像:大连东软信息学院镜像服务器地址: http://mirrors.neusoft.edu.cn 端口：80
```
sdkmanager --list --no_https --proxy=http --proxy_host=mirrors.neusoft.edu.cn --proxy_port=80
```
此时sdk目录下的文件结构如下:
```
├── build-tools
│ └── 30.0.0
├── cmdline-tools
│  └── last
├── emulator
│  ├── LICENSE
│  ├── NOTICE.csv
│  ├── NOTICE.txt
│  ├── android-info.txt
│  ├── bin64
│  ├── emulator
│  ├── emulator-check
│  ├── emulator64-crash-service
│  ├── goldfish-webrtc-bridge
│  ├── lib
│  ├── lib64
│  ├── mksdcard
│  ├── package.xml
│  ├── perfetto-protozero-protoc-plugin
│  ├── qemu
│  ├── qemu-img
│  ├── qsn
│  ├── resources
│  └── source.properties
├── licenses
│  └── android-sdk-license
├── patcher
│  └── v4
├── platform-tools
│  ├── NOTICE.txt
│  ├── adb
│  ├── dmtracedump
│  ├── e2fsdroid
│  ├── etc1tool
│  ├── fastboot
│  ├── hprof-conv
│  ├── lib64
│  ├── make_f2fs
│  ├── make_f2fs_casefold
│  ├── mke2fs
│  ├── mke2fs.conf
│  ├── package.xml
│  ├── sload_f2fs
│  ├── source.properties
│  ├── sqlite3
│  └── systrace
├── platforms
│  └── android-30
└── tools
    ├── NOTICE.txt
    ├── android
    ├── bin
    ├── emulator
    ├── emulator-check
    ├── lib
    ├── mksdcard
    ├── monitor
    ├── package.xml
    ├── proguard
    ├── source.properties
    └── support
```

### 9.配置Android打包工具及sdk的环境变量
1. 打开环境变量文件:
```
vim /etc/profile 
```
2. 添加sdkmanager的环境变量:
```
export ANDROID_HOME=/android/sdk
export PATH=$PATH:$ANDROID_HOME/cmdline-tools/last/bin:$ANDROID_HOME/build-tools:$ANDROID_HOME/platfrom-tools:$ANDROID_HOME/tools
```
3. 刷新环境变量(新开终端生效，或者手动source /etc/profile生效):
```
source /etc/profile 
```
4. 查看环境变量:
```
echo $PATH 
```
查看android环境变量:
```
android
```

至此Android打包环境就配置好了。

>如果Android项目工程的sdk版本众多,无需给每一个版本都配置一个环境变量,只需要创建 local.properties文件在里面写上sdk的目录,则会gradle自动会去sdk目录找合适的sdk版本。

# 三.打包Android安装包
### 通过全局Gradle打包
1. 通过git将代码工程拉下来,进入项目的根目录，执行打包命令：
```
gradle assembleRelease（打包成Release版本）
gradle assembleDebug（打包成Debug版本）
```
2. 打包编译完成，在项目的app/build/outputs/apk中可以找到debug版本或者是release版本。

### Android项目用GradleWapper打包
进入Android项目根目录,有三个文件:
|文件|	含义|
|-|-|
|gradlew	|Unix脚本(支持Linux/MacOS)|
|gradlew.bat	|Win脚本|
|gradle/wrapper/gradle-wrapper.jar	|gradle-wrapper核心jar|
|gradle/wrapper/gradle-wrapper.properties	|gradle-wrapper配置文件。|
linux:
```
./ gradlew version
```
windows:
```
gradlew version
```
如果linux报错:
```            
./gradlew: Permission denied
```
运行: 
```
chmod +x gradlew #添加所有用户都有执行gradlew的权限
```
``Gradle Wrapper（以下简写为“Wrapper”）``用于管理当前项目的Gradle版本，Gradle官方强烈推荐使用Wrapper构建项目。多人协作时，必须规定项目的Gradle版本，并以此版本的Gradle作为项目的构建工具，由于每个人在本地安装的Gradle版本可能并不一致（也没有必要一致），因此有必要在项目中统一管理Gradle版本。
Wrapper的文件结构如下（项目根目录中）：
```
├── build.gradle
├── settings.gradle
├── gradle
│   └── wrapper
│       ├── gradle-wrapper.jar
│       └── gradle-wrapper.properties
├── gradlew
└── gradlew.bat
```
包括一个gradle文件和两个可执行的脚本文件gradlew（macOS等平台用）和gradlew.bat（Windows平台用）。

- gradle-wrapper.jar:用于下载所需版本的Gradle。
- gradle-wrapper.properties:配置Gradle的版本号、本地存储地址等。各属性说明请见官方文档。
- gradlew, gradlew.bat:Wrapper的执行脚本，用于替代gradle命令来构建项目。
>注意：gradle-wrapper.properties中有一个distributionUrl属性，用于定义Gradle版本地下载URL，如distributionUrl=https\://services.gradle.org/distributions/gradle-4.0-all.zip，版本号后面有个“-all”，有时你也可能看到“-bin”，是什么意思?"-all"表示会下载此版本Gralde的所有的资源，包括二进制运行时文件、示例代码和相关文档。“-bin”表示只下载二进制运行时文件。

**Wrapper 构建项目时，其工作流程如下：**
1. 检查规定的Gradle版本，如果没有则去服务器下载。
2. 下载的Gradle版本存储在Gradle的用户目录中。如macOS中默认存储所有的Gradle版本到/Users/yourname/.gradle/wrapper/dists/中。
3. 使用解压后的Gradle版本来构建项目。





