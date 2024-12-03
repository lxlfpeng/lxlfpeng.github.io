---
title: AOSP源码之编译、调试、刷机
---

# 一.准备工作 
- 系统最好是Linux或者mac OS(本文基于Ubuntu)。
- Ubuntu设置永不休眠，在setting中搜索power.blank-screen选择never。
- 一块大一点儿的硬盘，至少得有200G剩余空间。
# 二.下载Aosp源码
### 1.安装GIT
##### 首先需要安装Git，因为源码是用Git管理的。
```
sudo apt-get install git
```
##### 接下来创建一个bin文件夹，并加入到PATH中，有点像Windows的环境变量。
```
mkdir ~/bin
PATH=~/bin:$PATH
```
##### 然后初始化Git，邮箱和姓名。
```
git config --global user.email "xxx@gmail.com"
git config --global user.name "xxx"
```

### 2.安装Python环境
```
sudo apt-get install python
```

### 3.安装repo及配置
repo 是一个python 脚本(所以我们上面要配置Python环境)，因为Android源码包含数百个git库，简化帮助管理git Android版本库的工具。
##### (1.)安装curl下载的库：
```
sudo apt-get install curl
```
##### (2.)下载repo并设置可以运行权限。
```
curl https://mirrors.tuna.tsinghua.edu.cn/git/git-repo > ~/bin/repo
chmod a+x ~/bin/repo
```
##### (3.)添加下载源。
google 的AOSP 的话，因为FQ和数据量太大，且需要需要翻墙影响速度，因此优先考虑国内的镜像(本文使用的是清华的源)。
```
export REPO_URL='https://mirrors.tuna.tsinghua.edu.cn/git/git-repo/'
```

### 4.初始化及同步源码
##### (1.)创建文件夹
创建一个AOSP文件夹，cdd到文件夹里面去待会儿需要把源码下载到这里:
```
mkdir aosp
cd aosp
```
##### (2.)初始化Aosp仓库
```
repo init -u https://aosp.tuna.tsinghua.edu.cn/platform/manifest
```
##### (3.)初始化并指定版本
```
repo init -u https://aosp.tuna.tsinghua.edu.cn/platform/manifest -b android-8.0.0_r36
```
AOSP对应关系查看地址： [对应关系](https://source.android.google.cn/setup/start/build-numbers#source-code-tags-and-builds)

##### (4.)开始同步源码
```
repo sync -j4
```
-j表示并发数.

**因为Android的源码越来越大，repo sync失败的概率也越来越高。所以我们可以避开使用repo sync的方式，而采用下载预下载包的方式来实现下载源码。**

### 5.预下载包的方式
##### 1. 下载预下载包
在windows或者Linux上面通过迅雷下载``https://mirrors.tuna.tsinghua.edu.cn/aosp-monthly/aosp-latest.tar``。
```
wget -c https://mirrors.tuna.tsinghua.edu.cn/aosp-monthly/aosp-latest.tar #下载初始化包
```
##### 2. 解压预下载包
```
tar xf aosp-latest.tar
```
>cd AOSP->解压得到的 AOSP 工程目录，这时 ls 的话什么也看不到，因为只有一个隐藏的 .repo 目录
##### 3. 查看分支 
```
cd .repo/manifests 
git branch -a
```
##### 4. 在aosp目录选择需要同步的版本
```
repo init -b android-9.0.0_r55
repo sync # 正常同步一遍即可得到完整目录
```
或者直接在aosp目录设置好你要同步的分支:
```
repo init -u https://aosp.tuna.tsinghua.edu.cn/platform/manifest -b android-8.0.0_r36
repo sync  # 正常同步一遍即可得到完整目录
```
如果仅加载具体模块:
```
repo sync platform/prebuilts/clang/host/darwin-x86
```

### 6.防止下载源码执行脚本卡死
通过自定义Shell脚本启动源码下载可以有效防止，同步源码时脚本被卡死的问题。
##### (1.)在AOSP文件夹中新建down.sh文件
```
#!/bin/bash
echo “======= start repo sync =======”
cd ~/Desktop/AOSP
repo sync -j4
while [ $? == 1 ]; do
echo “====== sync failed! re-sync again =====”
sleep 3
repo sync -j4
```
##### (2.)执行down.sh文件
```
sh down.sh
```

# 三.AOSP源码目录结构
- abi Application Binary Interface 应用程序二进制接口，abi相信同学们在SO库调用上遇到过，如果不支持该平台的话就说不ABI不支持。
- art Android Runtime 安卓运行时。这个会提前把字节码编译成二进制机器码保存起来，执行的时候加载速度比较快。Dalvik虚拟机则是在加载以后再去编译的，所以速度上ART会比Dalvik快一点。牺牲空间来赢取时间。
- bionic 基础库，Android系统与Linux内核的桥梁。Bionic 音标为 bīˈänik，翻译为"仿生"。
- bootable 系统启动引导相关程序
- build 用于构建Android系统的工具，也就是用于编译Android系统的
- cts Compatibility Test Suite 兼容性测试
- dalvik dalvik虚拟机，用于解析执行dex文件的虚拟机
- developers 开发者目录
- developerment 开发目录，比如说应用，application就在里面了，apps
- devices 设备相关的配置信息，什么索尼、HTC、自己的产品，就可以定义在这个目录下了
- docs 文档
- external 开源模组相关文件
- frameworks 系统架构，Android的核心了
- hardware hal层代码，硬件抽象层
- libcore 核心库
- libnativehelper native帮助库，实现JNI的相关文件
- ndk native development kit
- out 输出目录，编译以后生成的目录，相关的产出就在这里了
- packages 应用程序包。一些系统的应用就在这里了，比如说蓝牙，Launcher，相机，拨号之类的。
- pdk Plug-in Development Kit (PDK) is designed to help you build your own pattern projects
- platform_testing 平台测试
- prebuilts x86/arm架构下预编译的文件
- sdk software development kit
- system 底层系统文件
- toolchain 工具链
- tools 工具文件
- Makefile mk文件，用于控制编译

# 四.AOSP源码整编
编译AOSP源码需要配置好JAVA环境.
### 1.安装Java编译环境
```
sudo apt-get update
sudo apt-get install openjdk-8-jdk
```

### 2.进入AOSP文件夹，进行编译

##### (1.)初始化编译环境
```
source build/envsetup.sh
```
##### (2.)删除上一次编译的结果，初次编译可以不需要这一步
```make clobber```

##### (3.)选择与设备对应的编译版本
```lunch XX```

选择与设备对应的编译版本.如:编译开发工程师的版本``lunch aosp_x86-eng``，可以方便debug
[编译版本选择](https://source.android.com/setup/build/running#selecting-device-build)

如果``lunch``命令没有加对应的编译版本则会有以下信息输出：
```
You're building on Linux

Lunch menu... pick a combo:
 1. aosp_arm-eng
 2. aosp_arm64-eng
 3. aosp_mips-eng
 4. aosp_mips64-eng
 5. aosp_x86-eng
 6. aosp_x86_64-eng
 7. full_fugu-userdebug
 8. aosp_fugu-userdebug
 9. mini_emulator_arm64-userdebug
 10. m_e_arm-userdebug
 11. m_e_mips64-eng
 12. m_e_mips-userdebug
 13. mini_emulator_x86_64-userdebug
 14. mini_emulator_x86-userdebug
 15. aosp_dragon-userdebug
 16. aosp_dragon-eng
 17. aosp_marlin-userdebug
 18. aosp_sailfish-userdebug
 19. aosp_flounder-userdebug
 20. aosp_angler-userdebug
 21. aosp_bullhead-userdebug
 22. hikey-userdebug
 23. aosp_shamu-userdebug

Which would you like? [aosp_arm-eng] 
```
这里需要选择编译目标的格式(选择前面的序号，按回车即可)，编译目标的格式组成为``BUILD-BUILDTYPE``，比如aosp_arm-eng的BUILD为aosp_arm，BUILDTYPE为eng。 其中BUILD表示编译出的镜像可以运行在什么环境，aosp代表Android开源项目，arm表示系统是运行在arm架构的处理器上。 更多参考官方文档[文档](https://source.android.google.cn/source/running.html#selecting-device-build)。
BUILDTYPE 指的是编译类型，有以下三种：
- user：用来正式发布到市场的版本，权限受限，如没有 root 权限，不能 dedug，adb默认处于停用状态。
- userdebug：在user版本的基础上开放了 root 权限和 debug 权限，adb默认处于启用状态。一般用于调试真机。
- eng：开发工程师的版本，拥有最大的权限(root等)，具有额外调试工具的开发配置。一般用于模拟器。
如果你没有Nexus设备，只想编译完后运行在模拟器查看，那么BUILD可以选择aosp_x86，BUILDTYPE选择eng。

##### (4.)开始编译
```
make -j8
```
j后面数字几就是多少线程，最多不超过你的cpu总线程，
编译成功会显示如下:
```
Creating filesystem with parameters:
    Size: 2147483648
    Block size: 4096
    Blocks per group: 32768
    Inodes per group: 8192
    Inode size: 256
    Journal blocks: 8192
    Label: system
    Blocks: 524288
    Block groups: 16
    Reserved block group size: 127
Created filesystem with 2216/131072 inodes and 199826/524288 blocks
[100% 7669/7669] Install system fs ima.../target/product/generic_x86/system.img
out/target/product/generic_x86/system.img+ maxsize=2192446080 blocksize=2112 total=2147483648 reserve=22146432

#### make completed successfully (01:24:41 (hh:mm:ss)) ####
```
会在源码跟目录out/target/product/angler目录下生成镜像文件：
- system.img：系统镜像
- ramdisk.img：根文件系统镜像
- userdata.img：用户数据镜像
- recovery.img:recovery镜像
- boot.img:启动镜像
- vendor.img:驱动镜像

最终会在 out/target/product/generic_x86/目录生成了三个重要的镜像文件： system.img、userdata.img、ramdisk.img。大概介绍着三个镜像文件：
- system.img：系统镜像，里面包含了Android系统主要的目录和文件，通过init.c进行解析并mount挂载到/system目录下。
- userdata.img：用户镜像，是Android系统中存放用户数据的，通过init.c进行解析并mount挂载到/data目录下。
- ramdisk.img：根文件系统镜像，包含一些启动Android系统的重要文件，比如init.rc。

### 3.编译错误解决
##### (1.)缺少libncurses.so.5
报错信息:
``error while loading shared libraries: libncurses.so.5: cannot open shared object file: No such file or directory``
解决方式:
```
sudo apt-get update
```

for 32-bit binaries : 
```
sudo apt-get install libncurses5:i386
```

for 64-bit binaries : 
```
sudo apt-get install libncurses5
```

##### (2.)缺少M4
报错信息:
``/bin/bash: m4: command not found``
解决方式:
```
sudo apt-get install m4
```

##### (3.)去除所有本地化设置
报错信息:
``FAILED: out/host/linux-x86/obj/EXECUTABLES/checkpolicy_intermediates/policy_scan.c``
解决方法:
```
export LC_ALL=C
```
LC_ALL=C 是为了去除所有本地化的设置，让命令能正确执行， 但是不可以修改~/.bashrc，会导致终端内中文显示为数字(应该是对应的编码)

##### (4.)jack-server的问题
**jack server交互命令:**
```
 jack-admin start-server
 jack-admin kill-server
 jack-admin list-server
 jack-admin uninstall-server
 mm -j32 showcommands &> mm.out
 jack-admin install-server jack-launcher.jar  jack-server-4.8.ALPHA.jar
 jack-admin dump-report
 jack-admin dump-re
 jack-admin server-log  查找log所在目录
```

**问题一：多用户同时编译时报错**
错误信息：

```
FAILED: setup-jack-server
/bin/bash -c "(prebuilts/sdk/tools/jack-admin install-server prebuilts/sdk/tools/jack-launcher.jar prebuilts/sdk/tools/jack-server-4.11.ALPHA.jar  2>&1 || (exit 0) ) && (JACK_SERVER_VM_ARGUMENTS=\"-Dfile.encoding=UTF-8 -XX:+TieredCompilation\" prebuilts/sdk/tools/jack-admin start-server 2>&1 || exit 0 ) && (prebuilts/sdk/tools/jack-admin update server prebuilts/sdk/tools/jack-server-4.11.ALPHA.jar 4.11.ALPHA 2>&1 || exit 0 ) && (prebuilts/sdk/tools/jack-admin update jack prebuilts/sdk/tools/jacks/jack-4.31.CANDIDATE.jar 4.31.CANDIDATE || exit 47 )"
Jack server already installed in "/home/disk/lixialong/.jack-server"
Communication error with Jack server (35), try 'jack-diagnose' or see Jack server log
SSL error when connecting to the Jack server. Try 'jack-diagnose'
SSL error when connecting to the Jack server. Try 'jack-diagnose'
```
解决方案：同时修改$HOME/.jack-settings和$HOME/.jack-server/config.properties中的端口号（比如都改为8386/8387，端口号值为0~65535，1024下的值不要用），方可支持多用户同时编译。
查看端口是否一致：cat ~/.jack-server/config.properties|grep -i port && cat ~/.jack|grep -i port|grep -v LOG &&cat ~/.jack-settings|grep -i port

1. $HOME/.jack-settings
```
SERVER_PORT_SERVICE=8386
SERVER_PORT_ADMIN=8387
```
2. $HOME/.jack-server/config.properties
```
jack.server.service.port=8386
jack.server.admin.port=8387
```
3.  $HOME/.jack
```
SERVER_PORT_SERVICE=8288
SERVER_PORT_ADMIN=8289
```

**问题二： No Jack server running. Try 'jack-admin start-server'**
错误信息
```
com.android.jack.server.api.v01.ServerException: './config.properties' musthave permission rw------- but have rwx------
Caused by: java.io.IOException: './config.properties' must have permissionrw------- but have rwx------
... 
```
解决方案：通过查看文件 $HOME/.jack-server/logs/jack-server-0-0.log：
发现是配置文件的权限不对造成的，把文件$HOME/.jack-server/config.properties的权限由rwx改为rw即可解决问题。
**问题三：未配置变量信息导致问题**
错误信息:
```
ERROR: Communication error with Jack server (52) make: *** [out/target/common/obj/JAVA_LIBRARIES/libutil_intermediates/classes.jack] Error
```
这种情况多半属于jack-admin缺少变量JACK_JAR而导致的。

解决方案：
工程根目录内执行以下三句，再进行编译。
```
export JACK_JAR=./out/host/linux-x86/framework/jack.jar

./out/host/linux-x86/bin/jack-admin stop-server

./out/host/linux-x86/bin/jack-admin start-server
```
**问题四:TLSv1， TLSv1.1 禁用**
报错信息:
```
Ensuring Jack server is installed and started
```
解决方式:
```
sudo vim /etc/java-8-openjdk/security/java.security
```
vim里面输入/搜索jdk.tls.disabledAlgorithms= 将TLSv1， TLSv1.1 光标选中输入x删除掉取消禁用.然后wq保存.
修改后:
```
jdk.tls.disabledAlgorithms=SSLv3, RC4, DES, MD5withRSA, \
    DH keySize < 1024, EC keySize < 224, 3DES_EDE_CBC, anon, NULL, \
    include jdk.disabled.namedCurves
```
aosp/prebuilts/sdk/tools/ 目录下执行./jack-admin kill-server && ./jack-admin start-server 成功。


##### (4.)xmllint的问题
报错信息:
```/bin/bash: xmllint: command not found```
解决方案:
```
sudo apt-get  install libxml2-utils
```

##### (5.)编译内存不足
报错信息
```
Try increasing heap size with java option '-Xmx<size>'错误
```
解决方案:
```
export JACK_SERVER_VM_ARGUMENTS="-Dfile.encoding=UTF-8 -XX:+TieredCompilation -Xmx4g"
```
```
jack-admin kill-server
jack-admin start-server
```

# 五.运行模拟器
### 1.启动模拟器
在编译完成之后，就可以通过以下命令运行Android虚拟机了，由于之前已经执行过source和lunch命令了，可以直接运行：
```
source build/envsetup.sh
lunch aosp_x86-eng
emulator
```
就会启动模拟器了.

### 2.启动模拟器失败
尝试使用-verbose选项（即“emulator -verbose”），这将打印模拟器正在做什么/正在探测哪些文件，并给出有关错误的更多详细信息。
``
emulator -use-system-libs
``
启动模模拟器报错:
```
emulator: ERROR: x86_64 emulation currently requires hardware acceleration!
Please ensure KVM is properly installed and usable.
CPU acceleration status: This user doesn't have permissions to use KVM (/dev/kvm)
```
1. 安装 Qemu-KVM 和 cpu-checker
```
sudo apt-get install qemu-kvm cpu-checker
sudo apt-get install qemu-kvm libvirt-bin ubuntu-vm-builder bridge-utils
```
2. 查看系统 KVM 是否可用
```
$ kvm-ok
  INFO: /dev/kvm exists
  KVM acceleration can be used
```  
3. 创建 kvm 用户组并把当前登录用户（如 peng ）添加到 kvm 用户组
``` 
sudo addgroup kvm
sudo usermod -a -G kvm peng
``` 
4. 改变 /dev/kvm 用户组为 kvm
``` 
sudo chgrp kvm /dev/kvm
``` 
5. 创建 udev rule，并写入 KERNEL=="kvm", GROUP="kvm", MODE="0660"
``` 
sudo gedit /etc/udev/rules.d/60-qemu-kvm.rules
KERNEL=="kvm", GROUP="kvm", MODE="0660"
``` 
6. 重启ubuntu系统然后运行emulator

# 六.AOSP源码编译某个单独的模块
上面的编译我们都是对整个Android系统进行编译的.如果我们要编译系统的Settings应用模块，这就属于源码单编某一个模块.
在AOSP根目录执行：
```
source build/envsetup.sh
lunch aosp_x86-eng
```
进入Settings的目录：
```
cd packages/apps/Settings
```
通过mm编译当前目录下的模块，不编译依赖模块。
```
mm
```
编译成功后会有提示生成文件的存放路径。除了Settings.odex文件，还会在out/target/product/generic_x86/system/priv-app/Settings目录下生成Settings.apk。
此外还有以下命令可以进行单编：
- mmm：编译指定目录下的模块，不编译它所依赖的其它模块。
- mma：编译当前目录下的模块及其依赖项。
- mmma：编译指定路径下所有模块，并且包含依赖。

如果对系统模块的源码进行修改，查看生成的APK文件，有两种方式：
- 通过adb push或者adb install 来安装APK。
- 使用make snod命令，重新生成 system.img，运行模拟器查看。

# 七.导入源码到AS
### 1.编译idegen模块，生成IDE项目文件
在源码中，存在idegen模块，该模块专门用来为idea工具生成系统源码的project.默认情况下aosp编译并不会生成该文件。
在开始编译该模块之前，首先确保你已经编译过Android源码了，如果没有，先要进行AOSP编译.和编译普通的模块一样，我们用mmm命令编译idegen.
在开始编译之前，检查out/host/linux-x86/framework/目录下是否存在idegen.jar文件，存在则说明你已经编译过该模块，否者，则需要编译.执行如下命令即可:
```
source build/envsetup.sh 将脚本添加到系统内
lunch 并选择要编译的项目
mmm development/tools/idegen/ 
sudo ./development/tools/idegen/idegen.sh
```

其中mmm development/tools/idegen/执行完成后会生成idegen.jar，而sodo ./development/tools/idegen/idegen.sh则会在源码目录下生成IEDA工程配置文件:android.ipr，android.iml及android.iws.

简单的说明一下这三个文件的作用:

- android.ipr:通常是保存工程相关的设置，比如编译器配置，入口，相关的libraries等
- android.iml:则是主要是描述了modules，比如modules的路径，依赖关系等.
- android.iws:则主要是包含了一些个人工作区的设置.

>"android.iml"和"android.ipr"一般是"只读"的属性，我们这里建议大家，把这两个文件改成可读可写，否则，在更改一些项目配置的时候可能会出现无法保存的情况，执行如下两条命令即可。
```
sudo chmod 777 android.iml
sudo chmod 777 android.ipr
```

### 2 导入源码到AndroidStudio
##### (1.)配置AS
IDE内存优化
因为源码数量非常多，所以导入时IDEA/AS会需要大量内存。所以我们需要编辑IDE的VM选项。配置文件为

IDEA的是IDEA_HOME/bin/idea.vmoptions
AS的是AS_HOME/bin/studio.vmoptions
注意，AS有一个64位版本的配置文件studio64.vmoptions最好一并修改了。

找到上面的配置文件，将对应的内容修改为
```
-Xms748m -Xmx748m
```
即将VM的堆内存最小和最大都设置为748m。官方要求至少在748m以上，根据实际情况进行配置即可
##### (2.)导入源码
接下来，我们导入源码:打开Android Studio，点击File->Open，选择刚才生成的android.ipr文件即可，然后就是漫长的等待，注意此时是将源码完全导入到AS中了。
如果AS运行比较慢我们就需要排除一些不需要导入的模块。

##### (3.) 排除模块
很多情况下，我们希望不导入某些模块，那么就可以在导入前修改android.iml文件，通过添加配置的方式告诉AS不导入某些模块，比如现在我不想导入art模块，那么就在android.iml文件中添加:
```
<excludeFloder url="file://$MODULE_DIR$"/abi>
```
不难发现，其格式为:``<excludeFloder url="file://$MODULE_DIR$"/模块名>``

>注:编译生成的android.iml文件中已经默认排除了一些模块，通过搜索excludeFolder关键字可找到.

如果比较关心framworks和packages模块，则保留framworks和packages模块，将其他模块全部排除，在android.iml中添加了以下配置:
```
      <excludeFolder url="file://$MODULE_DIR$/.repo" />
      <excludeFolder url="file://$MODULE_DIR$/abi" />
      <excludeFolder url="file://$MODULE_DIR$/art" />
      <excludeFolder url="file://$MODULE_DIR$/bionic" />
      <excludeFolder url="file://$MODULE_DIR$/bootable" />
      <excludeFolder url="file://$MODULE_DIR$/build" />
      <excludeFolder url="file://$MODULE_DIR$/cts" />
      <excludeFolder url="file://$MODULE_DIR$/dalvik" />
      <excludeFolder url="file://$MODULE_DIR$/developers" />
      <excludeFolder url="file://$MODULE_DIR$/development" />
      <excludeFolder url="file://$MODULE_DIR$/device" />
      <excludeFolder url="file://$MODULE_DIR$/docs" />
      <excludeFolder url="file://$MODULE_DIR$/external" />
      <excludeFolder url="file://$MODULE_DIR$/external/bluetooth" />
      <excludeFolder url="file://$MODULE_DIR$/external/chromium" />
      <excludeFolder url="file://$MODULE_DIR$/external/emma" />
      <excludeFolder url="file://$MODULE_DIR$/external/icu4c" />
      <excludeFolder url="file://$MODULE_DIR$/external/jdiff" />
      <excludeFolder url="file://$MODULE_DIR$/external/webkit" />
      <excludeFolder url="file://$MODULE_DIR$/frameworks/base/docs" />
      <excludeFolder url="file://$MODULE_DIR$/frameworks/base/extension" />
      <excludeFolder url="file://$MODULE_DIR$/hardware" />
      <excludeFolder url="file://$MODULE_DIR$/kernel" />
      <excludeFolder url="file://$MODULE_DIR$/kernel-3.18" />
      <excludeFolder url="file://$MODULE_DIR$/libcore" />
      <excludeFolder url="file://$MODULE_DIR$/libnativehelper" />
      <excludeFolder url="file://$MODULE_DIR$/ndk" />
      <excludeFolder url="file://$MODULE_DIR$/oem-release" />
      <excludeFolder url="file://$MODULE_DIR$/out" />
      <excludeFolder url="file://$MODULE_DIR$/out/eclipse" />
      <excludeFolder url="file://$MODULE_DIR$/out/host" />
      <excludeFolder url="file://$MODULE_DIR$/out/target/common/docs" />
      <excludeFolder url="file://$MODULE_DIR$/out/target/common/obj/JAVA_LIBRARIES/android_stubs_current_intermediates" />
      <excludeFolder url="file://$MODULE_DIR$/out/target/product" />
      <excludeFolder url="file://$MODULE_DIR$/pdk" />
      <excludeFolder url="file://$MODULE_DIR$/platform_testing" />
      <excludeFolder url="file://$MODULE_DIR$/prebuilt" />
      <excludeFolder url="file://$MODULE_DIR$/prebuilts" />
      <excludeFolder url="file://$MODULE_DIR$/rc_projects" />
      <excludeFolder url="file://$MODULE_DIR$/sdk" />
      <excludeFolder url="file://$MODULE_DIR$/system" />
      <excludeFolder url="file://$MODULE_DIR$/tools" />
      <excludeFolder url="file://$MODULE_DIR$/trusty" />
      <excludeFolder url="file://$MODULE_DIR$/vendor" />
```
完成之后，按照上面说的步骤，使用Android Studio选中"android.ipr"打开项目即可。
>等项目加载完成后，我们还可以通过Android Studio对Exclude的Module进行调整，所以也不用害怕这里Exclude掉了有用的代码，或少Exclude了一部分代码，在项目加载完以后再进行调整就行了。此处和在android.iml文件中添加excludeFolder 的功能是一样的；

打开"Project Structure"，中间的窗口选择"android"，在弹出的窗口中左边栏中选择"Modules"，而后在右边的窗口中选择"Sources"。
在这里我们可以看到项目的所有代码目录，我们可以选中不需要的module，并点击上面的"Excluded"按钮，当被选中的目录变为橙色，即表示完成Exclude操作；
如果想要取消对某代码目录的Exclude操作，选中该目录，再次点击"Excluded"按钮，等待目录变为蓝色即可。 
![](/images/0d5568dc0704484071c79ffafc9f4a59.webp)

##### (3.) 配置源码正确跳转
当我们导入完源码后，就可以查看整个系统的源码，但是有个问题，打开的Java代码，查看集成关系或者调用关系的时候，还是会跳转到.class文件中，而不是相应的Java类，
比如PhoneWindow.java继承了Window.java，但是我们跳转的时候却跳到了Window.class，并没有跳转到frameworks目录下对应的源码类，而是jar包中的类。
我们需要让其跳转到相应的类中。我们就需要新建一个没有任何jar库的SDK给到系统源码项目的依赖， 这里的配置JDK/SDK，是用于解决在分析和调试源码的过程，能正确地跳转到目标源码，
而非SDK中的代码。 
-  新建JDK
Project Structure -> SDKs， 新建 JDK， 其中JDK目录可选择跟原本JDK一致即可，任意取一个名字，这里取empty_jdk 然后删除这里取empty_jdk其classpath和SourcePath的内容，确保使用Android系统源码文件
![](/images/741503e98ebaf38731e46ca6a74996a9.webp)
jdk_none

-  配置SDK
Project Structure -> SDKs， 选中与自己编译的AOSP对应的SDk版本(如果没有对应的就到SDKmanager里面取下载一个对应的版本) Android API 28 Platform， 然后选择其Java SDK为前面新建的empty_jdk
![](/images/58a145d0b3b2acc11ec4d057a398cd67.webp)
sdk_none

- 选择SDK
Project Structure -> Project -> 选中Project SDK， 选择前面的Android API 28 Platform
![](/images/08d2bfa2c04cf43a3ac7b5322ac72e13.webp)
project_sdk

-  建立依赖
Project Structure -> Modules -> android -> Dependencies: Module选择我们上面编辑过的SDK。然后点击下图绿色的+号来选择Jars or directories，将 aosp/frameworks 目录添加进来，再按照同样的步骤将aosp/external 目录， 也可添加其他所关注的源码；
然后选中其他所有的依赖，点击右边的下移箭头将其他依赖移动到我们添加的目录下面。(或者将其他的所有依赖删除)
![](/images/06c6777d56a3fe108306901c3f11ddd3.webp)
   
>注意，一般我们大部分人不在ubuntu下开发app ，为了能在Windows或Mac系统下也能使用Android Studio查看源码，
可以按照上面的步骤，那样直接拷贝ubuntu下的android.iml和android.ipr文件到Windows或Mac系统下的android源码根目录下，
然后导入Adnroid Studio中，这样就可以在这两个平台上进行查看源码了。        

# 八.通过AS调试源码
### 1. 打开模拟器
要调试代码，首先要打开模拟器，注意不是Android Studio自带的模拟器，而是通过编译后的代码启动的模拟器，否则可能出现代码不对应的问题。
直接运行emulator命令是无法启动的，执行方法如下：
```
source build/envsteup.sh

lunch 6 //和编译时对应

emulator
```
接下来通过Run->Attache debugger to Android process，在弹出的Choose Process框内必须选择Show all processes，否则看不到相关的进程:然后选择system_process，就可以进行调试了。

# 九.Android刷机知识
### 1.BootLoader
机器首先要启动，CPU 最先执行的一段程序就是 BootLoader，是在操作系统内核运行之前运行的一段小程序。其实Bootloader就相当于电脑的bios。 通过这段小程序，进行硬件初始化，获取内存大小信息等，调整手机到适配状态，从而将系统的软硬件环境带到一个合适状态，以便为最终调用操作系统内核准备好正确的环境。
。很多的手机厂商都会锁住BootLoader，这样你就只能使用官方的系统，想要第三方的ROM能够运行，或者破解官方系统这时候就需要进行bootloader解锁!这是刷机的第一步， 当然也有很多手机没有bootloader锁!我们只需要知道要想刷机就得先bootloader解锁。
### 2.FastBoot
fastboot，它是bootloader后期进入的一个特殊阶段。例如小米手机开机同时按音量下建就会进入这个模式.也是一种模式。可以通过数据线与电脑连接，然后在电脑上执行一些命令，如刷系统镜像到手机上。fastboot可以理解为实现了一个简单的通信协议，接收命令并更新镜像文件，其他什么的干不了。
需使用USB数据线连接电脑和手机的一种线刷刷机模式，大部分第三方的Recovery刷入，或者救砖均是在Fastboot模式下进行，所以这种方式称为线刷。 fastboot需要bootloader的支持，所以不是每家手机都会支持这种模式。Fastboot 可以说是一个通信协议，电脑可以通过这个通信协议，直接向手机系统不同分区中写入文件（.img 文件）。
###### fastboot(bootloader)模式怎么进入？
大多数安卓手机，都可以在关机状态下，然后同时按住【电源键】+【音量+】键，大约2-3s后，就可以进入Fastboot模式。 作为开发者在开机状态下可以用下面的方式进入：
```
adb reboot bootloader
```
###### fastboot命令
然后就可以执行下面的fastboot命令了:
```
fastboot flashing unlock    #6.0以上设备 设备必须解锁，开始刷机（这个不同的手机厂商不同）
fastboot erase {partition}  # 擦除分区
fastboot  erase  frp    # 擦除 frp 分区，frp 即 Factory Reset Protection，用于防止用户信息在手机丢失后外泄
fastboot  flash  boot  boot.img    # 刷入 boot 分区
fastboot  flash  system  system.img    # 刷入 system 分区
fastboot  flash  recovery  recovery.img    # 刷入 recovery 分区
fastboot flashall    #烧写所有分区，注意：此命令会在当前目录中查找所有img文件，将这些img文件烧写到所有对应的分区中，并重新启动手机。
fastboot  format  data    # 格式化 data 分区
fastboot  flashing lock    # 设备上锁，刷机完毕
fastboot  continue    # 自动重启设备
fastboot reboot# 重启手机
fastboot reboot-bootloader# 重启到bootloader 刷机用
fastboot devices  ## 发现手机，显示当前哪些手机通过fastboot连接了
```
### 3.Recovery
如果没有进入fastboot，bootloader继续执行，如果又发现有特殊的按键组合，比如小米上是音量上键和开机键，则会进入recovery模式。它里面包含了一个kernel以及一个可执行程序recovery，以
及一些初始化文件。Recovery模式指的是一种可以对安卓机内部的数据或系统进行修改的模式，也叫工程模式，像是电脑上的小型winPE系统，winPE可以在电脑上安装操作系统，或者做些删除备份、管理的工作。
官方Recovery用处不大，所以通常会刷入一个第三方的Recovery ，Recovery 更类似于一个小型的管理系统。只不过功能简单，所做的管理有限。在recovery模式下，会加载了部分文件系统，所以才可以读sdcard中的update.zip进行刷机，当然，也可以清除cache和用户数据。
该模式可根据用户的需要进行修改，因此有官方recovery模式以及第三方recovery模式。第三方recovery模式可以识别第三方rom包，因此可以用来刷机。而官方recovery一般不能识别第三方zip文件。好用的第三方RE:TWRP 和 CWM Recovery刷机包是称为Google Update 格式。在用Recovery恢复时，刷机包通常放在SD卡里，所以这里刷机一般称为卡刷。
### 4.线刷和卡刷
- 线刷： 直接想手机硬盘写入*.img 文件，我个人觉得这种方法比较快捷，而且省事。但是必须借助电脑和数据线。
- 卡刷：就是利用recovery的从SD卡中更新系统的这个功能，如果你想刷第三方Rom，必须刷入个第三方recovery，只有fastboot模式才能刷recovery.img。卡刷有个限制，必须要把想要更新的ROM（Android系统）拷贝到SD卡上。如果手机已经是砖了。那只能用线刷了。

# 十.手机硬件驱动知识
### 1. 硬件驱动的作用
AOSP是一个由谷歌维护的开源操作系统开发项目，既然是开源项目，也就意味着任何人都可以自由地审查和贡献代码以及修复项目仓库，而谷歌引领着大方向和大部分的开发工作。AOSP会定期为Android加入最新的安全补丁，谷歌每年也会在其I/O开发者大会上公布操作系统的新功能。除了开放贡献代码外，AOSP还可以在开源许可下自由使用和修改。
比如，小米，华为等厂商根据自己的目的自由调整该项目，并开发了自己的衍生产品，包括多用途的emui和miui。需要注意的是，AOSP包含了开发者构建Android所需的一切，但它并不包括成品智能手机所需的一切。
谷歌和AOSP无法为所有硬件配置提供内核设备驱动。所谓设备驱动，是指手机硬件所需的固件，比如处理器或摄像头。手机和SoC制造商，如高通和三星，必须将这些驱动程序纳入他们的Android构建中。
这也是为什么从AOSP到实际设备的系统更新需要一定时间的原因。其次AOSP也不包含谷歌的软件应用套件，如Chrome浏览器、YouTube，甚至谷歌Play商店。
它也不包括谷歌的一些底层技术和API，而这些技术和API可以实现移动支付、语音命令和云存储等功能，这些都是作为谷歌移动服务（GMS）单独授权的。 任何厂商想要在系统中安装GMS，都必须为自己的设备获得GMS授权和移动应用分发协议（MADA），然后通过多项兼容性测试。有Android兼容性测试套件（CTS）来验证软件和硬件以及API。
正因为AOSP开源的特性，许多的硬件厂商的驱动代码并不是开源的，所以AOSP会有一个硬件抽象层 (HAL)，来保证驱动程序代码不被泄露。大多数手机厂商都是从高通等芯片厂商那里获得AOSP版本，该AOSP版本为硬件量身定坐了高通驱动程序，所以刷入真机是可以正常的运行。

### 2. 如何添加硬件驱动
在上面步骤中我们编译好了AOSP可以直接通过模拟器运行.编译aosp时也会生成system.img文件，这个文件是最终刷机用的，但是system.img文件必须依赖驱动文件生成，
如果没有放入对应的驱动就编译，那么生成的镜像也是无法正常刷机的。通过上文我们知道aosp 仅是一套源码，真机运行需要厂商的驱动，厂商的驱动是不包含在AOSP中的，
第三方ROM(如CM等)的厂家驱动是自行提取的。但是google也开源了nexus和pixel对应的AOSP版本的硬件驱动代码.如果我们有nexus或者是pixel设备就可以下载相应的驱动进行编译，
然后将编译好的系统输入到设备中去.
##### (1.)下载对应的驱动
需要根据你选择的[版本](https://source.android.com/source/build-numbers.html)
去[驱动页面](https://developers.google.com/android/nexus/drivers#shamulrx21o)下载合适的驱动。
##### (2.)生成驱动
将驱动文件下载后，解压到AOSP根目录，得到几个.sh文件，执行后，会在AOSP下创建vendor目录，里面包含了驱动。
##### (3.)编译带有驱动的AOSP
再次`` make -j4``，此次编译的结果就包含了驱动，编译出新的系统.

# 十一.ROM编译及烧录
一般定制ROM其实就是对手机内存里的system/app文件夹的内容进行自定义，系统所有的程序都在这个文件夹里，比如浏览器、拨号器、联系人等。自己安装的软件\data\文件夹中。
### 1.真机驱动下载
在上文中可以了解到厂商的驱动是不包含在AOSP中的.因此编译出来的AOSP系统源码要在真机上运行，还需要加上厂商驱动进行编译才能烧录到真机上使用.
Google提供了Nexus和Pixel这两个太子机的驱动，我们可以在驱动页面下载合适的驱动。
[Driver Binaries for Nexus and Pixel Devices](https://developers.google.com/android/drivers#walleye)

### 2.配置真机驱动到AOSP
1. 在上面链接里面,两个文件都进行下载，一个是google vendor，一个qcom。
2. 解压得到``extract-google_devices-blueline.sh``，``extract-qcom-blueline.sh``
3. 将这两个脚本放到aosp代码目录下，进行提取
   ``sh extract-google_devices-blueline.sh``
```
vendor/
vendor/google_devices/
vendor/google_devices/marlin/
vendor/google_devices/marlin/device-vendor-marlin.mk
vendor/google_devices/marlin/android-info.txt
vendor/google_devices/marlin/BoardConfigVendor.mk
vendor/google_devices/marlin/BoardConfigPartial.mk
vendor/google_devices/marlin/proprietary/
vendor/google_devices/marlin/proprietary/vendor.img
vendor/google_devices/marlin/device-partial.mk

Files extracted successfully.
```
第2个 高通驱动
``sh extract-qcom-blueline.sh``
```
vendor/
vendor/qcom/
vendor/qcom/marlin/
vendor/qcom/marlin/BoardConfigPartial.mk
vendor/qcom/marlin/proprietary/
vendor/qcom/marlin/proprietary/lib64/
vendor/qcom/marlin/proprietary/lib64/libbcc.so
vendor/qcom/marlin/proprietary/lib64/libLLVM_android.so
vendor/qcom/marlin/proprietary/lib64/libiperf.so
vendor/qcom/marlin/proprietary/lib64/libminui.so
vendor/qcom/marlin/proprietary/ATT_profiles.xml
vendor/qcom/marlin/proprietary/pktlogconf
vendor/qcom/marlin/proprietary/VZW_profiles.xml
vendor/qcom/marlin/proprietary/ROW_profiles.xml
vendor/qcom/marlin/proprietary/libclcore_neon.bc
vendor/qcom/marlin/proprietary/sanitizer-status
vendor/qcom/marlin/proprietary/libiperf.so
vendor/qcom/marlin/proprietary/qcrilhook.jar
vendor/qcom/marlin/proprietary/libminui.so
vendor/qcom/marlin/proprietary/libion.so
vendor/qcom/marlin/proprietary/iperf3
vendor/qcom/marlin/device-partial.mk
vendor/google_devices/
vendor/google_devices/marlin/
vendor/google_devices/marlin/device-vendor-marlin.mk
vendor/google_devices/marlin/android-info.txt
vendor/google_devices/marlin/BoardConfigVendor.mk

Files extracted successfully.
```
执行后，会在AOSP下创建vendor目录，里面包含了驱动。编译完成后，执行``make fastboot adb ``单独编译fastboot和adb。

### 3.编译Rom
重新对AOSP进行编译.此次编译的结果就包含了驱动，编译完成后，执行make fastboot adb 单独编译fastboot和adb。

### 4. 烧录Rom到手机
1. 手机启用开发者模式，打开 USB 调试 adb shell 能进入。
2. 开机键 + 音量- 进入 bootloader 模式。
3. 电脑上能识别出来手机并装上了驱动。
4. fastboot devices 能看到设备。
5. 再次执行./fastboot -w flashall将开始刷机，刷完会自动重启，over!

参考资料:
[Android 镜像使用帮助](https://mirrors.tuna.tsinghua.edu.cn/help/AOSP/)
[MIUI ROM适配之旅第一天——认识Android手机](https://www.xiaomi.cn/post/10984220)
[Android FrameWork 学习之Android 系统源码调试](https://www.cnblogs.com/liumce/p/8027559.html)
[从CM刷机过程和原理分析Android系统结构](https://blog.csdn.net/luoshengyang/article/details/29688041)
[Android ROM移植](https://blog.csdn.net/weixin_30924087/article/details/98030409)
[android rom移植知识普及](https://blog.csdn.net/innost/article/details/7623951)
[Android系统源码修改](https://blog.csdn.net/huil0925/category_6259725_2.html)
[android系统的分区结构](https://blog.csdn.net/uglychild/article/details/79550793)
[Android ROM的制作与烧录](https://blog.csdn.net/u010142437/article/details/72834972)
[android系统源码中添加app源码（源码部署移植）](https://blog.csdn.net/zhonglunshun/article/details/70256727)

参考资料:
[Ubentu编译Android源码（AOSP）](https://www.cnblogs.com/caoxinyu/p/10568480.html)
[AOSP源码下载/编译/刷机/调试](http://mouxuejie.com/blog/2019-11-17/aosp-setup/)
[Android rom移植一](https://blog.csdn.net/zy199701/article/details/106478670/)
[目前通用的Android拼包移植方法均是正向移植](http://blog.sina.com.cn/s/blog_b278ce3b010186bw.html)
[Android驱动开发全过程](https://blog.csdn.net/u010783226/article/details/94406309)

