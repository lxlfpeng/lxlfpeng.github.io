---
title: 黑苹果引导软件之OpenCore
date: 2022-01-10
categories: 
  - 黑苹果
---

# 一.OpenCore简介
笔者在17年写过一篇黑苹果安装教程：[黑苹果系统安装通用教程(Clover引导)](https://blog.csdn.net/unreliable_narrator/article/details/64438619)，不过该文章用的是基于Clover引导的MacOs系统。目前随着黑苹果的另一款引导工具OpenCore不断成熟，使用OC是大势所趋。众多黑苹果驱动的作者已经停止对Clover的兼容支持，改向Opencore的兼容。OpenCore是类似于Clover的UEFI的引导器，OpenCore提供了详细的日志系统，帮助黑[苹果](https://pinpai.smzdm.com/1687/)排错；其次OpenCore以更先进的方法注入第三方Kext，不破坏系统的SIP；再次，OpenCore支持读取NVRAM等一系列特性，可以让黑苹果变得更“原生”，诸如选择启动器、Command Ctrl互换，原生开启Option键特性都可以实现。

# 二.OpenCore引导MacOS

### 🦮第一步 准备工作

- 一个8G以上的U盘。
- MacOS系统镜像包、Etcher（刻录工具）、DiskGenius（分区工具）、适合自己电脑的EFI驱动文件。

### 🐕‍第二步 确认硬盘分区表格式

黑苹果的安装和使用需要EFI分区进行引导，因此安装黑苹果的硬盘**必须使用GPT分区表**，如果您的磁盘使用的是MBR分区表，那么需要先将硬盘数据进行备份，然后使用分区工具将硬盘重新使用GPT分区表分区。可以通过下文提供的两种方法或者通过[DiskGenius](http://www.diskgenius.cn/) 看看分区表是否为GPT分区表。

##### 方法一：使用磁盘管理查看MBR和GPT分区类型

1. 鼠标右击**此电脑**，点击**“管理”**。
   ![](/images/0dd3d9ffbec0e85784c21cb49fc8a630.webp)

2. 在计算机管理中点击**“磁盘管理”**。
   ![](/images/f339191dff4b7223adccb6fbed1687f7.webp)

3. 进入**磁盘管理**可以看到磁盘分区情况，右键点击**“磁盘0”**选择查看**“属性”**。
   ![](/images/9c4377933e42476b9f3ce2f7f10fd7b8.webp)

4. 在**属性**界面，点击**“卷”**就可以看到此磁盘的基本信息了，我们可以在**“磁盘分区形式”**看到磁盘0为**GPT**磁盘分区类型，如何查看硬盘分区是MBR还是GPT问题轻松解决。
   ![](/images/c7e1a4977f42ec3d6c1037069e44ec01.webp)

##### 方法二：使用命令提示符查看MBR和GPT分区类型

1. 按**“Windows + R”**键，在弹出的运行对话框中输入**“diskpart”**，并按**回车**键启动diskpart实用程序。
   ![](/images/3e5e147436fee2e15fdc767ffccc5d6a.webp)
2. 输入**“list disk”**命令，然后按**回车**，查看磁盘信息。
   ![](/images/3d61a372ddb93eb41873389b8fbe73e0.webp)
3. 在命令行中的**“Gpt”**列下方，带有一个星号（*）为GPT磁盘类型。没有星号（*）为MBR磁盘类型。所以上图中，磁盘0为GPT磁盘类型，磁盘1为MBR磁盘类型，如何查看硬盘分区是MBR还是GPT问题轻松解决。

### 🐆第三步 MBR分区表转换成GPT分区表

如果硬盘分区是GPT分区表可以略过这一步操作。如果硬盘分区不是GPT分区表。那么你需要将硬盘数据进行备份，然后使用分区工具对硬盘重新分区。微软官方有[MBR转GPT的教程](https://link.zhihu.com/?target=https%3A//docs.microsoft.com/zh-cn/windows-server/storage/disk-management/change-an-mbr-disk-into-a-gpt-disk)。也可以进入到PE下打开DiskGenius分区工具，选定硬盘然后将硬盘分区表转换成类型为GUID-也就是GPT分区表。

### 🦌第四步 硬盘划分安装MacOS分区

通常我们在安装黑苹果系统的场景有如下两种：

- 整盘安装：在电脑中存在多块硬盘的条件下，选择某块硬盘单独作为Mac系统的安装盘。并且将苹果系统的引导文件放到该硬盘下，这样可以和其他的系统独立起来使用，此时你需要在该硬盘上新建EFI分区存放黑苹果引导文件。你可以使用分区工具自行创建，需要注意的是，EFI分区需要大于200M。

- 分区安装：在一块已经装有 Windows（或其它操作系统）的硬盘上安装 MacOS 系统的磁盘为基础，通过压缩磁盘空间划出的一个新的分区用来安装Mac系统。此时你可以直接使用已有的EFI分区，并将MacOS引导文件复制于此。

#### 整盘安装(多硬盘多系统)

黑苹果的安装和使用需要EFI分区进行引导，因此在对硬盘进行GPT分区的同时，需要创建新的空白分区并格式化为EFI分区格式。可以使用 DiskGenius，在你要安装 MacOS 的空闲硬盘分出两个区，其中一个区需要为 FAT16/FAT32 格式，且大小大于 200MB即可用来放置EFI引导文件，另一个分区用来安装黑苹果系统。

#### 分区安装(单硬盘多系统)

如果你的电脑已经安装了 Windows 系统且预留的 ESP 分区大于200MB，那么无需任何操作，直接划分一个黑苹果的安装分区进行安装系统既可，如果ESP 分区小于 200MB，那么你需要扩大 ESP 分区，或重建 ESP 分区。这一步需要在 Windows PE 环境下操作，请首先刻录好Windows PE U盘。

1. 需要将已有的 ESP 分区删除，然后再磁盘末尾空闲空间重建一个 200M 以上的 ESP 分区（你可以从你准备安装 MacOS 的那部分空间中划分出来一些），操作完成后你的分区结构会类似下图（Windows 在前，200m+ 的 ESP 分区和 MacOS安装分区在后）。然后按下文的指引重建引导。
   ![](/images/4c6a4a0242eed59d7ae20d5391c205ec.webp)

2. 由于上一步我们将ESP分区删除了，因此里面的系统引导文件也丢失了，此时是无法正确的引导进入操作系统的，因此需要重建 Windows UEFI 引导。 在 PE 下找到你的 Windows 安装分区和 ESP 分区的盘符，确保这两个分区在文件资源管理器中可见（如果不可见请为 DiskGenius工具为不可见的分区分配盘符）。 下面我们假设 Windows 安装分区盘符为 C:，ESP 分区盘符 V:
   ![](/images/6c68a7cbc6a1a80c8d2f91238722d4d4.webp)

3. 打开命令提示符（cmd），执行以下命令：`bcdboot 你的系统盘盘符:\Windows /s 你的ESP分区盘符 /f uefi /l zh-cn`，如：
   ```
    bcdboot c:\windows /s d: /f uefi /l zh-cn
    Copied!
   ```
   ![](/images/4c09026458c93b8d0b1da4f88726f036.webp)
   将 C: 和 V: 分别替换为你的盘符即可。

4. 去掉ESP分区的盘符，重启即可。

**当然你也可以使用 PE 下的图形化工具修复引导。**

> 几乎所有 2012 年后生产的计算机都支持引导 UEFI，而且不再执行以前的 “Legacy” 标准。这些计算机需要一个 ESP 分区来引导。ESP 代表 EFI 系统分区，使用 FAT32/FAT16 文件系统。ESP 负责存储固件启动时使用的EFI 引导加载程序和其他实用程序。如果您不小心删除了这个分区，您的系统将无法再引导。为了安全起见，ESP 是默认隐藏的，因此它没有驱动器号。

### 🐃第五步 制作MacOs安装启动U盘

1. 将您的U盘插入电脑(备份好u盘数据)。
2. 打开Etcher软件(Windows10及以上需要以管理员权限运行)，点击“Select image”选择下载好的MacOS安装镜像；
   ![image.png](/images/93204a10980b136578bd66dbdd6b8ff3.webp)
3. 然后点击“Select drive”选择你的U盘，如果你直插有一个U盘，软件会自动选择该u盘；
   ![image.png](/images/14d9fc5ac1bdbe5704d29586d81854c4.webp)
4. 接着点击“Flsh！”开始刻录黑苹果安装镜像到U盘；
5. 等到提示“Flash Complete！”Successful device 就完成安装镜像的制作了。
   ![image.png](/images/67e571948cbd86d4e6754153bab0dfa4.webp)
6. 替换自己的EFI文件。
7. 重启电脑到Bios设置中。

> 黑果小兵的镜像包里面含有三个独立的EFI引导分区，同时支持 OpenCore / CLOVER / WEPE引导，这里建议先不要做替换EFI的操作，先用提供的EFI安装好一同以后再将EFI替换称自己的即可。

### 🦣第六步 调整主板Bios设置

1. 重启按F2进入BIOS（电脑不一样，按键也不一样，就看自己电脑型号）;

2. Bios设置禁用清单(根据自己的Bios调整)

    * `Fast Boot` - 快速启动
    * `VT-d` (can be enabled if you set DisableIoMapper to YES) - VT-d（如果DisableIOMapper Quicks设置为YES，则可以启用）
    * `CSM` - CSM 兼容性支持模块
    * `Thunderbolt` - 雷雳
    * `Intel SGX` - 英特尔SGX
    * `Intel Platform Trust`- 英特尔平台信任
    * `CFG Lock` (MSR 0xE2 write protection) - CFG锁（MSR 0xE2写保护）（必须关闭，如果找不到该选项，则在OpenCore的config-内核-> Quirks下启用与CFG Lock相关选项）
    * `ecure Boot` - 安全启动
    * `Parallel Port` - 并口
    * `Serial/COM Port` - 串行/COM端口

3. Bios设置启用清单(根据自己的Bios调整)

    * `VT-x` - VT-x
    * `UEFI Boot Mode` UEFI启动模式。请不要使用Legacy
    * 硬盘模式：改为`AHCI`。不能用IDE和RST RAID。
    * `Above 4G decoding` - 大于4G地址空间解码
    * `Hyper-Threading` - 超线程
    * `Execute Disable Bit` - 执行禁用位
    * `EHCI/XHCI Hand-off` - EHCI / XHCI接手控制
    * `OS type`: `Windows 8.1/10 UEFI Mode` - 操作系统类型：Windows 8.1 / 10 UEFI模式
    * `DVMT Pre-Allocated`(iGPU Memory): DVMT预分配（iGPU内存）：`64MB`（如果能设Max就设）
    * `Legacy RTC Device` - 传统RTC设备

4. 设置USB接入的U盘为第一启动项:
   ![image.png](/images/5ee1fdd5a54ec8acdda7016c150d3e9e.webp)

5. 保存Bios设置，重启电脑。

### 🐘第七步 建立MacOS磁盘文件系统

1. 开始引导MacOS系统，这个过程需要1-2分钟，耐心等待进入安装程序，会出现语言选择界面:
   ![image.png](/images/85e9dc734fbe1e2000a1ddad981bb229.webp)

2. 语言选择选择简体中文即可:
   ![](/images/aafc7d7f9072ba5cc6a49a5aa92564a2.webp)

3. MacOS实用工具界面，选择磁盘工具:
   ![](/images/21608f286cc1803fa19690e8d96834da.webp)

4. 选择`显示所有设备`:
   ![](/images/f7eba96317032765d334c34bd74477ba.webp)

5. 选择你需要安装MacOS的分区，点击`抹掉`按钮，选择默认的`APFS`或者是`Mac OS扩展(日志型)`名称随意，点击`抹掉`按钮:
   ![image.png](/images/e2d1e23968c82123aeed9eb833c85e05.webp)

6. 抹盘成功后，如果所有的硬盘都没有EFI分区那么它会自动生成一个200MB的EFI分区，这样做的好处是不会出现安装过程中的由于EFI分区尺寸小于200MB而引起的无法安装的错误:
   ![](/images/e4ea28dfd69d482d1c0d192e4dd37ced.webp)

7. 到这里，磁盘工具的动作就已经结束了，找到左上角，点击「磁盘工具」选择「退出磁盘工具」即可退出，进入安装界面，进行系统的安装了。
   ![](/images/5f651944264f5926042ec4771b35da7f.webp)

### 🦨第八步 安装MacOS系统

1. 进入安装界面，进行安装，系统会多次重启，耐心等待即可。
   ![](/images/a71f978c658e27b84bb4b384f70a0277.webp)

2. MacOS初始化设置，按照自己需求的情况进行配置即可(略过)。
   ![](/images/1d804dd2a28f8ed9976215295c7116f4.webp)

### 🐿️第九步 完善MacOS引导

现在MacOS 系统已经安装好了，但是必须要通过我们的U盘进行引导，才能进入MacOS系统。我们现在要做的就是将我们已经配置好的EFI启动引导文件放在硬盘中就可以了，这一步在 MacOS 和 在 Windows 下操作都是可以的。如果你在 Windows 下操作，一般需要使用 DiskGenius这个工具来辅助操作。当然对于整盘安装(多硬盘多系统)和分区安装(单硬盘多系统)处理的方式也是不一样的。

#### 整盘安装(多硬盘多系统)

整盘安装的情况处理起来就比较简单了，Windows引导放到Windows盘的引导ESP分区，Mac系统的OpenCore引导放到Mac盘的EFI引导分区，引导各自放各自的引导，完成后回到BISO，设置带OpenCore引导的硬盘为第一启动项即可。

例如：

* 磁盘 A：安装了 Windows
* 磁盘 B：安装了 MacOS

这种情况下无需手动使用工具添加引导项也可以，直接将 OC 的 EFI 引导文件拷贝到 **磁盘B** 的 EFI 引导分区下，然后在 BIOS 里面将 **磁盘 B**的引导设置第 1 启动即可。

#### 分区安装(单硬盘多系统)

在一块硬盘上面装了多个操作系统，例如windows，MacOs等系统的情况。

例如：

* 磁盘 A：安装了 Windows 和 MacOS两个系统

这种情况下，首先直接将 OC 的 EFI 引导文件拷贝到 **磁盘B** 的 EFI 引导分区下以后还得使用下面的 DG 或者 EasyUEFI 手动添加引导。这里讲一下EasyIUEFI方法，DG方式同理。

1. 下载[EasyUEFI 破解版下载地址](https://sqlsec.lanzouw.com/i4amxzmj1cj)

1. 绿色版本点击即可使用， 打开后的主界面：
   ![](/images/5d7120291d79a1419dc2306a87bfdfae.webp)

2. 选择「管理 EFI 启动项」：
   ![](/images/5c941f61e108e59a799b1eadba9ee8f2.webp)

3. 首先点击「创建新项」：
   ![](/images/f1d9656342b57d77652f33f579f1c3b5.webp)

4. 操作系统类型选择「Linux 或者其他操作系统」，描述随便写一个，目标分区选择「硬盘的第一个 ESP 引导分区」，然后点击「浏览数据」，选择 EFI/OC/ 目录下的 OpenCpre.efi后，点击确定：
   ![](/images/eef7b53837d4a1a49dfb43e7adaff31f.webp)

5. 接着将刚刚添加的启动项，「上移」到第一位：
   ![](/images/4bd5065e6ea82faa0ec5aeb1bc07a218.webp)

6. 最终的效果，拔掉 U 盘后，每次开机选择操作系统的界面如下：
   ![](/images/bd3f0260224c5c1d2a8b536a663bfaef.webp)

> 如果使用了 DG 或者 EasyUEFI 手动添加引导但是依然没有 OC 为第 1 启动的话，很简单，直接 **BIOS** 里面将你手动添加的引导设置为第 1 启动即可。

# 三.配置OpenCore的EFI

### 1. 获取OpenCore的EFI

上文说到可以在网络上找到很多大佬制作的跟你机型相同的EFI，直接拿来使用就可以了，可以通过以下方式找到适合自己机型配置的的EFI文件:

- [Hackintosh黑苹果长期维护机型整理清单](https://blog.daliansky.net/Hackintosh-long-term-maintenance-model-checklist.html)黑果小兵提供的长期维护机型。
- [GitHub](https://github.com/search?utf8=%E2%9C%93&q=)在GitHub上搜索自己的机型。
- 通过论坛等形式找到合适自己的EFI。


### 2. 下载OpenCore的EFI
如果通过上面的方法也没有找到自己型号的EFI亦或者是找到的EFI引导以后都会出现或多或少的一些问题，如果你追求完美那么可以下载原版的OpenCore进行配置即可:

1. 打开[OpenCore](https://dortania.github.io/OpenCore-Install-Guide/ktext.html#firmware-drivers)官网。

2. 找到[OpenCore的下载链接](https://github.com/acidanthera/OpenCorePkg/releases) 下载`open core`:
   ![](/images/a21049f32517e455671a0ddfc7e97e90.webp)

3. 复制出EFI，解压以后X64\EFI是我们需要的文件。
   ![](/images/1c0d998d4a64afb15528b408ac0107f9.webp)

### 3. OpenCore的EFI文件结构

已经配置好的 OpenCore 的文件结构， 在 EFI 分区 (/Volumes/EFI/) 下面， 有一个 EFI 文件夹， 内容如下

```
EFI
│   ├── BOOT
│   │   └── BOOTx64.efi
│   └── OC
│       ├── ACPI
│       │   ├── SSDT-PLUG.aml
│       ├── Drivers
│       │   ├── ApfsDriverLoader.efi
│       │   ├── FwRuntimeServices.efi
│       │   ├── HFSPlus.efi
│       ├── Kexts
│       │   ├── AppleALC.kext
│       │   ├── IntelMausi.kext
│       │   ├── Lilu.kext
│       │   ├── SMCProcessor.kext
│       │   ├── SMCSuperIO.kext
│       │   ├── VirtualSMC.kext
│       │   └── WhateverGreen.kext
│       ├── OpenCore.efi
│       ├── Tools
│       │   └── Shell.efi
│       └── config.plist
```

- EFI/BOOT/BOOTx64.efi：电脑启动的时候支持UEFI的主板会去读取这个文件。
- EFI/OC OpenCore： 存放目录。
- ACPI： 存放自定义的ssdt aml文件， 比如 (aml为二进制文件， 是我们需要的最终文件. dsl为源文件， 需要用 MaciASL打开另存为aml.)。
    - SSDT-PLUG.dsl： 开启硬件变频功能， 作用于CPU， iGPU， dGPU. 需要自行编译为 aml。
    - SSDT-AWAC.dsl： 300系列的主板用最近更新的 BIOS 后， RTC 失效， 这个 SSDT 作用是启用 RTC， 需要自行编译为 aml。
    - SSDT-EC-USBX.dsl： Fake EC 和 USBX， 给 MacOS 提供一个虚假的EC设备， 同时提供 USB 大电流支持， 需要自行编译为 aml。
- Drivers：存放文件系统驱动文件， 比如:
    - ApfsDriverLoader.efi：用于加载 MacOS 内置的 apfs.efi ， 读取APFS分区， 必要文件。
    - FwRuntimeServices.efi：提供模拟 nvram 等其他功能， 必要文件。
    - HFSPlus.efi： 提供HFS+文件系统的支持， 读取MacOS的安装U盘以及Recovery分区需要此efi， 必要文件。
- Kexts： 存放各种设备和硬件的驱动或者补丁。
    - Lilu.kext：一个框架式的kext，自身单独使用没有作用， 是其他kext的依赖， 必须第一个被加载. 必要文件。
    - AppleALC.kext： 让MacOS可以正确识别大部分主板上的集成声卡。
    - VirtualSMC.kext： 模拟SMC， 必要文件。
    - WhateverGreen.kext： 解决集成/独立显卡的各种问题 必要文件 其他的几个kext， 根据需要使用， 比如:
    - IntelMausi.kext： Intel 有线网卡驱动。
    - RealtekR1000SL.kext： Realtek 有线网卡驱动。
    - SMCProcessor.kext SMCSuperIO.kext： 让MacOS下的监控软件可以读取主板上的传感器信息温度，频率等。
- Tools ：工具类efi， 这些工具在 OpenCore 启动界面可以看到， 目前只有下面2个工具， 不可以放入Drivers文件夹。
    - CleanNvram.efi ：作用为清空nvram， 新版本 OpenCore 已经用内置的选项 AllowNvramReset=YES 取代这个 efi， 等效于启动到MacOS恢复模式之后， 运行 nvram -c。
    - Shell.efi ：一个修改版的 UEFI SHELL， 可以做很多有趣的事情。
    - VerifyMsrE2： 检查主板是否有 CFG LOCK。
- OpenCore.efi ：OpenCore的主引导文件。
- config.plist ：OpenCore的主要配置文件， 可以使用 PlistEdit Pro 或者 ProperTree 可视化编辑. 所以， OC下面总共有4个文件夹， 1个主文件， 和一个配置文件， 是不是非常简洁。

### 4. OpenCore的EFI配置编辑工具

因为 OpenCore 的核心配置文件是 .plist 结尾的，所以需要专门的编辑器来编辑，常见的 OC 编辑器有如下:

##### 🐒MacOS平台可用EFI配置编辑工具

- [OCC编辑器(注意需要和版本对应起来)](https://www.mfpud.com/opencore/occ/)
- [Hackintool](https://github.com/headkaze/Hackintool/releases)

##### 🐕全平台可用EFI配置编辑工具

- [QtOpenCoreConfig(全平台可用)](https://github.com/ic005k/QtOpenCoreConfig/releases)
- [OCAuxiliaryTools](https://heipg.cn/tag/ocauxiliarytools)
- [opencoreconfiguratoronline(在线)](https://galada.gitee.io/opencoreconfiguratoronline)
- [opencoreconfiguratoronline_gitee(在线)](https://gitee.com/galada/OpenCoreConfiguratorOnline)
- [ProperTree](https://github.com/corpnewt/ProperTree)

### 5. 查看OpenCore版本

- 方式一：Hackintool 黑苹果必备工具。
- 方式二：命令查询 ``nvram 4D1FDA02-38C7-4A6A-9CC6-4BCCA8B30102:opencore-version 1``

# 四.黑苹果注入三码洗白

### 1. 为什么黑苹果要注入三码洗白？

经常用苹果设备的应该知道苹果很多在线服务形成了一个生态圈，简单来说就是在手机上浏览的东西可以推送到苹果电脑上继续浏览，电话、短信都可以通过这些服务在苹果电脑上展示出来，当然了这里说的是白苹果即苹果出售并提供支持的电脑。 那黑苹果能不能享受这些服务呢?答案是可以的。MacOS黑苹果需要通过注入三码解决iMessage，FaceTime，iCloud等苹果在线服务。注入三码后，可以正常登陆App Store下载app，iCloud可以正常同步，可以正常使用隔空投送，接力，iMessage，随航等功能。 三码不对的话，有可能无法登陆App Store，甚至导致Apple ID被拉黑。目前，苹果三码编写规则已经被摸的较为透彻（尤其是机型序列号），可以使用 OCC编辑器、Hackintool等黑苹果工具自动生成。

### 2. 使用OCC注入三码洗白

1. 在开始之前，先登录苹果 [iCloud.com](https://heipg.cn/link/aHR0cHM6Ly93d3cuaWNsb3VkLmNvbS8=)，进入“查找我的iPhone”，选择“所有设备”清除所有登录过的黑苹果，如果你没有打开过“查找我的Mac”，则这一步可以省略。
2. 在[OpenCore-configurator官网](https://mackie100projects.altervista.org/opencore-configurator/) 下载对应版本的OpenCore-configurator进行安装。
3. 安装**OpenCore-configurator**后，挂载efi 打开分区 使用**OpenCore-configurator**打开你的config，选择`Platformlnfo-机型平台设置`进入机型平台设置:
   ![](/images/baf0c9a57a261d12782643eb159f5ca2.webp)

4. 选择和你机型相像的配置，会自动生成id:
   ![](/images/6c9a63ae89564c77b6e2526a4b9406c5.webp)

5. 复制Serial Number前往[Apple官网](https://checkcoverage.apple.com/cn/zh/)查询序列号，如果显示有购买日期和机型等保修信息，说明这个序列号别人在用，不建议使用，点击Generate New生成新的Serial Number，然后继续进行查询，直到查询三码出现提示：很抱歉，这个序列号无效。请检查您的信息并再试一次，（一般都提示这个）即可:
   ![](/images/75f05c789f8739ff33cb5e6d95453526.webp)
   如果你运气特别好，有可能生成出来官方正版且未被激活的白苹果序列号
   ![](/images/5a2ad6047af54e706b1916ec79eafcc0.webp)
6. 使用OpenCore-configurator保存即可。
# 五.Windows和MacOS系统时间不匹配的问题

装了Mac和Windows的双系统之后会发现进入MacOs系统以后，再重启进Windows就会出现时间不同步的问题，Windows下的时间比Mac下晚8小时，出现这个问题的主要原因是因为mac和win基准识别时间不同。

1. 打开C盘>Windows>System32，找到cmd.exe，右键以管理员的身份运行。 （或者使用WIN+R组合键后输入CMD）
2. 然后输入以下命令：

  ```
  Reg add HKLM\SYSTEM\CurrentControlSet\Control\TimeZoneInformation /v RealTimeIsUniversal /t REG_DWORD /d 1
  ```

3. 回车搞定！重启试试！

> 命令的原理其实就是通过修改注册表让windows识别硬件时间为UTC-0而不是现在的UTC+8 。也可以在注册表（WIN+R输入regedit）里直接操作``HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\TimeZoneInformation\``中添加一项数据类型为REG_DWORD，名称为RealTimeIsUniversal，值设为1即可。

参考资料:

[完善引导](https://apple.sqlsec.com/5-%E5%AE%9E%E6%88%98%E6%BC%94%E7%A4%BA/5-6.html)

[EFI分区——折腾黑苹果必须弄懂的硬盘那点事](https://post.smzdm.com/p/a9gvx9p5/)

[单双硬盘装Windows/Mac双系统用OpenCore引导菜单添加Windows引导项，设定OC文件WINOS DISK 路径教学](http://imacos.top/2020/04/06/1559/)

[黑苹果入门完全指南](https://astrobear.top/2020/02/14/Introduction_to_hackintosh/)

[黑苹果安装及新手指导](https://www.bilibili.com/read/cv12696678/)

[open core安装教程](https://post.smzdm.com/p/a259rv2d/)

[原版黑苹果安装教程【OC 引导 + Big Sur】](https://macx.top/5673.html)

[OpenCore文档](https://github.com/cattyhouse/oc-guide)

[单双硬盘装Windows/Mac双系统用OpenCore引导菜单添加Windows引导项，设定OC文件WINOS DISK 路径教学](http://imacos.top/2020/04/06/1559/)

[驱动英特尔核显，让黑苹果流畅运行「OpenCore专门篇」](https://heipg.cn/tutorial/patching-intel-igpu-opencore.html)

[OpenCor_Clover通用Intel英特尔核显驱动完整教程（英特尔集成显卡与核显仿冒ID速查表显卡驱动）](http://imacos.top/2020/09/03/2216/)

[【黑苹果显卡驱动】通过Device/properties 给Framebuffer打补丁一点经验](https://juejin.cn/post/6844903848633434120)

[【黑苹果显卡驱动】通过Device/properties 给Framebuffer打补丁一点经验](https://blog.csdn.net/weixin_33998125/article/details/91463629)

[黑苹果注入显示器EDID解决部分核显独显黑屏花屏颜色不对等一系列问题](http://k61.org/fix-edid-on-hackintosh.html)

[使用黑苹果过程中一些问题的解决方法](https://www.derrors.cn/index.php/hackintosh/solution.html)

[UHD630核显驱动方法及驱动后闪屏严重问题解决记录](https://blog.csdn.net/weixin_33882452/article/details/91447219)

[使用 OpenCore 引导黑苹果](https://blog.xjn819.com/post/opencore-guide.html)

[精解OpenCore](https://blog.daliansky.net/OpenCore-BootLoader.html)

[【图文教程】使用Hackintool.app驱动核显-帧缓冲区补丁](http://imacos.top/2020/09/03/2216/)

[WhateverGreen](https://github.com/acidanthera/WhateverGreen/blob/master/Manual/FAQ.IntelHD.cn.md#%E4%BD%BF%E7%94%A8-weg-%E8%87%AA%E5%AE%9A%E4%B9%89-fb-%E5%92%8C-%E7%AB%AF%E5%8F%A3-%E8%A1%A5%E4%B8%81)

[给黑苹果注入三码，避免封号，解锁iCloud/FaceTime/iMessage/随航！](https://heipg.cn/tutorial/inject-identifier-for-hackintosh.html)

[在你的硬盘上建立第二个 EFI 分区](http://www.imacosx.cn/330.html)

[EFI分区——折腾黑苹果必须弄懂的硬盘那点事](http://app.myzaker.com/news/article.php?pk=61ae34888e9f090dd15cf4dc)

[OpenCor_Clover通用Intel英特尔核显驱动完整教程（英特尔集成显卡与核显仿冒ID速查表显卡驱动）](http://imacos.top/2020/09/03/2216/)

[WhateverGreen核显驱动详解](https://www.jianshu.com/p/764ae0e46fc5)

[ProperTree](https://github.com/corpnewt/ProperTree)

[黑苹果注入三码洗白教程](https://www.songbingjia.com/jingpin/show-36793.html)

[黑苹果自动获取与注入三码的方法，附相关工具，解锁iCloud变白果！](https://imacosx.com/scb/5078.html)

[为自己的黑苹果生成随机三码](https://sleele.com/2019/03/21/smbios/)

[使用Hackintool工具生成全新的序列号及更改黑苹果SN三码序列号教程](https://www.mfpud.com/topics/977/)

