---
title: Win10及11安装Wsl2
---

# 一.安装Wsl2
## 环境要求
必须运行 Windows 10 版本 2004 及更高版本（内部版本 19041 及更高版本）或 Windows 11。 WSL2 是 WSL 1 的升级版，带来的主要优势：
* 提高文件系统性能
* 支持完全的系统调用兼容性

WSL2 使用了 hyper-v 虚拟化技术，它就是一个你感知不到的虚拟机（VM），比以前的版本性能更高。

## 安装步骤
### 1.启用虚拟机平台和 Linux 子系统功能
**方式一:使用控制面板**

打开控制面版，再点击程序与功能—>启用或关闭Windows功能:
- 适用于Linux的Windows子系统
- 虚拟机平台
- hyper-v
  重启电脑。

**方式二:使用命令行工具**
以管理员权限启动PowerShell或者cmd，然后输入以下命令启用虚拟机平台：
```
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```
然后输入以下命令启用 Linux 子系统功能：
```
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
```

### 2.设置wsl默认版本为Wsl2
将 WSL 2 设置为默认版本，再打开的powershell窗口中输入如下命令：
```
wsl --set-default-version 2
```

### 3.安装一个Linux发行版
**方式一:wsl下载**
1. 查看可安装版本
```
wsl --list --online // 列出所有可安装的linux版本
```
2. 开始安装
```
wsl --install -d Ubuntu-20.04 // 安装Ubuntu-20.04
```

**方式二:windows应用商店下载**
打开微软商店应用，在搜索框中输入“Linux”或者“ubuntu”然后搜索，你可以看到搜索结果中有很多的 Linux 发行版可以选择。选择一个你喜欢的 Linux 发行版本然后安装。

### 4.启动Ubuntu
- 可以通过开始菜单 像运行本地程序一样运行Ubuntu ，直接运行开始菜单里的 Ubuntu 20.04 LTS即可。
- 在命令提示符中 输入 WSL

# 二.发行版本WSL1升级至WSL2
## 1.检查发行版的wsl版本
首先，我们要确认发行版本是否是1.0版本执行以下命令：

```
wsl -l -v
```

显示结果如下：

```
NAME            STATE           VERSION
* Ubuntu-20.04    Stopped         1
```

即代表目前的版本是1.0，可以升级。

## 2.升级发行版至Wsl2版本
执行命令：

```
wsl --set-version 分发版名称 版本号
```

例如：

```
wsl --set-version Ubuntu-20.04 2
```

>WSL2 是基于虚拟机的，所以可以在后台运行各种任务，比如 Docker 等等，但是带来的相应问题就是会占用一部分内存，使用 wsl --shutdown <分发版名称> 可以再不使用的时候停止它，以节约资源。

# 三.导入导出Linux发行版
通过使用tar文件导入导出Linux发行版，可使其在任意地方安装Linux发行版或者共享自己的Linux发行版：

1. 查看已安装的Linux发行版

```
wsl -l --all -v
```
如果Linux发行版处于运行状态使用下面的命令关闭:
```
wsl --shutdown
```

2. 导出Linux发行版tar文件到D盘
```
wsl --export Ubuntu-20.04 d:/wsl-ubuntu-20.04.tar
```
3. 卸载当前Linux发行版
```
wsl --unregister Ubuntu-20.04
```
4. 重新导入并安装WSL2到D盘
```
wsl --import Ubuntu-20.04 d:/wsl-ubuntu-20.04 d:/wsl-ubuntu-20.04.tar --version 2
```
5. 设置默认登录用户为安装时用户名
```
ubuntu2004 config --default-user USERNAME
```

>此时导出的wsl-ubuntu-20.04.tar文件即可共享给任何使用Wsl2的开发人员使用。在协同开发中使用更多，为每个开发者提供一致统一的开发环境。

# 四.发行版本安装桌面及远程控制
发行版本中可以根据自己的喜好安装 KDE、Gnome、xfce、lxde 等桌面环境。个人比较喜欢Xfce。 它是一种快速，稳定且轻巧的桌面环境，非常适合在远程服务器上使用。也可以使用Gnome，Gnome是 Ubuntu 的默认桌面上环境，
也是多数发行版的默认桌面环境。

### 1.安装Xfce桌面(建议)

Gnome与xfce相比，xfce由于其轻巧，它可以安装在低端台式机上。Xfce优雅的外观，增强了用户体验，它对用户非常友好，性能优于其他桌面环境，它提供了许多可定制的接触点以供灵活使用。

```
sudo apt update
sudo apt install xfce4
```

### 2.安装Gnome桌面

Gnome与xfce相比，Gnome它具有简单但有效的用户界面。用户在屏幕上有更多动态的工作区域。它具有内置的恢复功能，可帮助用户保持工作的连续性非常适合初学者浏览所有功能并学习。它为开发着的应用程序的运行提供了一个完美的兼容平台。

```
sudo apt update
sudo apt install ubuntu-desktop
或者
sudo apt install ubuntu-gnome-desktop
```

### 3.通过Xrdp远程控制桌面

##### 安装Xrdp远程控制服务
Xrdp 是一个微软远程桌面协议（RDP）的开源实现，它允许你通过图形界面控制远程系统。通过 RDP，你可以登录远程机器，并且创建一个真实的桌面会话，就像你登录本地机器一样。Xrdp包含在默认的Ubuntu存储库中。 要安装它，请运行：
```
sudo apt install xrdp
```
安装完成后，Xrdp 服务将会自动启动。你可以输入下面的命令，验证它是否再运行，有running代表服务成功运行。：
```
sudo systemctl status xrdp
```
如果您的电脑未安装systemctl命令则可以使用:
```
sudo service xrdp status
```
或者:
```
sudo /etc/init.d/xrdp start
```
xrdp默认使用的端口号是3389，如果要改用其他的端口号，则可以再/etc/xrdp/xrdp.ini配置文件中进行修改:
```
sudo vim /etc/xrdp/xrdp.ini
```
编辑xrdp.ini 把port从3389改成3390，然后重新启动xrdp:
```
sudo systemctl restart xrdp
```

或者使用命令的方式直接修改对应的端口号。
```
sudo sed -i 's/3389/3390/g' /etc/xrdp/xrdp.ini
```

##### 远程连接接Xrdp服务
配置好Xrdp服务以后，如果是 Windows 电脑，你可以使用默认的 RDP 客户端。在 Windows 搜索栏输入“remote”(远程桌面连接)，并且点击“Remote Desktop Connection”。这将会打开一个 RDP 客户端。在“Computer”区域输入远程服务器 IP地址，并且点击“Connect”。 在登录屏幕，输入你的用户名和密码，点击“OK”。登录成功后，你将看到默认的 Gnome 或者 Xfce 桌面。如果使用的是 macOS，
可以从Mac App Store安装 Microsoft Remote Desktop应用。 Linux 用户则可以使用一个 RDP 客户端，例如 Remmina 或者 Vinagre来进行连接使用。
>建议使用root账户登录，以免某些版本导致的登录失败等问题。XRDP在xfce下工作良好，但在ghome等其他桌面环境可能无法运行，因此优先选择xfce。

##### Xrdp连接出现闪退的问题
闪退的原因是安装远程桌面时.xsession文件可能被修改，所以就出现远程桌面闪退情况。

需要在该用户目录创建一个.xsession 不懂没关系，在SSH中输入：

```
touch .xsession
```
根据自己的电脑上的运行的桌面环境来确定执行哪个:
```
# gnome桌面
echo gnome-session > ~/.xsession
```
```
# xfce桌面
echo xfce4-session >~/.xsession
```
然后把它放到用户目录下

```
sudo chown username:username .xsession
```
然后重新启动xrdp:
```
sudo systemctl restart xrdp
```

### 4.通过Xming远程控制桌面
1. 在Windos电脑上下载并安装[Xming](https://sourceforge.net/projects/xming/)
2. 安装完成后启动Xming，选择one window->下一步->start no client-> 下一步->勾选No Access Control->下一步，这样Xming就监听，等待连接了。
3. 回到linux系统中在.bashrc文件中添加一行，地址是Xming监听应用设备的IP地址。
    ```
    vim ~/.bashrc
    export DISPLAY=172.17.208.1:0
   ```
4. 配置好保存退出后 使用``source ~/.bashrc ``使配置生效。
5. unbunt 执行 ``startxfce4``或者是``gnome-session``

# 五.WSL2与Windows之间文件访问

### WSL/WSL2在windows的哪个目录
1. WSL2所在目录。
```
C:\Users\用户名\AppData\Local\Packages\CanonicalGroupLimited.Ubuntu20.04onWindows_79rhkp1fndgsc\LocalState
```
wsl中linux的文件系统整个是个镜像文件，我们可以看到上面目录中有个ext4.vhdx文件
2. WSL所在目录。
```
C:\Users\用户名\AppData\Local\Packages\CanonicalGroupLimited.Ubuntu20.04onWindows_79rhkp1fndgsc\LocalState\rootfs
```

### Windows访问Linux目录
上文说到在windows中有一个Wsl2的对应目录里面有ext4.vhdx文件。启动Wsl系统后，这个文件系统映射到了`` \\wsl$\系统名 ``下面，在浏览器输入``\\wsl$\Ubuntu-20.04\``可以查看文件。

### Linux子系统访问Windows目录

进入linux后，windows的硬盘被挂载在/mnt下，通过``cd /mnt``可以直接访问。

**小技巧：可在Windows中指定位置创建一个share文件夹，在WSL2使用`ln -s /mnt/xx/share ~/share`方式可快速在Windows和Wsl2中共享文件。**

# 六.清空重置linux发行版
要在 Windows Subsystem for Linux 2 上重置 Linux 发行版，请使用以下步骤：
1. 在 Windows 10 上打开设置。
2. 单击应用程序。
3. 单击应用程序和功能。
4. 选择您的 Linux 发行版并单击高级选项链接。
5. 单击重置按钮。

# 七.使用VS Code连接到WSL2 Linux发行版
vscode和其他程序一样，可以访问linux，通过\wsl$\。 在win上安装vscode，打上Remote-WSL插件，就能通过vscode直接使用wsl的环境了，相当方便。

# 八.wsl2 内存限制

在`C:\Users\<UserName>\.wslconfig`创建一个文件，配置如下所示。

```
[wsl2]
memory=4GB
swap=8GB
```

> swap类似于Windows的虚拟内存，从硬盘中划分出一个分区，在物理内存不够时，就会将硬盘空间虚拟成内存使用，用于解决内存不足的情况。

配置格式：

```
[wsl2]
memory=<size>              
processors=<number>       
swap=<size>                
localhostForwarding=<bool>
```

在配置设置完之后，执行`wsl --shutdown`命令进行关闭，随后执行`wsl`命令再次启动即可。

* memory：限制内存
* swap：交换分区
* processors：限制核心数
* localhostForwarding：关闭默认连接，将WSL2本地主机绑定到Windows本地主机

# 九.wsl常用命令

## 安装默认发行版本

```
wsl --install
```

安装 WSL 和 Linux 的 Ubuntu 发行版。 [了解详细信息](https://learn.microsoft.com/zh-cn/windows/wsl/install)。

## 安装特定的 Linux 发行版

```
wsl --install --distribution <Distribution Name>
```

通过将 `<Distribution Name>` 替换为发行版名称，指定除默认发行版 (Ubuntu) 之外的 Linux 发行版进行安装。 此命令也可输入为：`wsl -d <Distribution Name>`。

## 列出可用的 Linux 发行版

```
wsl --list --online
```

查看可通过在线商店获得的 Linux 发行版列表。 此命令也可输入为：`wsl -l -o`。

## 列出已安装的 Linux 发行版

```
wsl --list --verbose
```

查看安装在 Windows 计算机上的 Linux 发行版列表，其中包括状态（发行版是正在运行还是已停止）和运行发行版的 WSL 版本（WSL 1 或 WSL 2）。 [比较 WSL 1 和 WSL 2](https://learn.microsoft.com/zh-cn/windows/wsl/compare-versions)。 此命令也可输入为：`wsl -l -v`。 可与 list 命令一起使用的其他选项包括：`--all`（列出所有发行版）、`--running`（仅列出当前正在运行的发行版）或 `--quiet`（仅显示发行版名称）。

## 将 WSL 版本设置为 1 或 2

```
wsl --set-version <distribution name> <versionNumber>
```

若要指定运行 Linux 发行版的 WSL 版本（1 或 2），请将 `<distribution name>` 替换为发行版的名称，并将 `<versionNumber>` 替换为 1 或 2。 [比较 WSL 1 和 WSL 2](https://learn.microsoft.com/zh-cn/windows/wsl/compare-versions)。

## 设置默认 WSL 版本

```
wsl --set-default-version <Version>
```

若要将默认版本设置为 WSL 1 或 WSL 2，请将 `<Version>` 替换为数字 1 或 2，表示对于安装新的 Linux 发行版，你希望默认使用哪个版本的 WSL。 例如，`wsl --set-default-version 2`。 [比较 WSL 1 和 WSL 2](https://learn.microsoft.com/zh-cn/windows/wsl/compare-versions)。

## 设置默认 Linux 发行版

```
wsl --set-default <Distribution Name>
```

若要设置 WSL 命令将用于运行的默认 Linux 发行版，请将 `<Distribution Name>` 替换为你首选的 Linux 发行版的名称。

## 将目录更改为主页

```
wsl ~
```

`~` 可与 wsl 一起使用，以在用户的主目录中启动。 若要在 WSL 命令提示符中从任何目录跳回到主目录，可使用命令 `cd ~`。

## 通过 PowerShell 或 CMD 运行特定的 Linux 发行版

```
wsl --distribution <Distribution Name> --user <User Name>
```

若要通过特定用户运行特定 Linux 发行版，请将 `<Distribution Name>` 替换为你首选的 Linux 发行版的名称（例如 Debian），将 `<User Name>` 替换为现有用户的名称（例如 root）。 如果 WSL 发行版中不存在该用户，你将会收到一个错误。 若要输出当前用户名，请使用 `whoami` 命令。

## 更新 WSL

```
wsl --update
```

手动更新 WSL Linux 内核的版本。 还可以使用 `wsl --update rollback` 命令回滚到 WSL Linux 内核的上一版本。

## 检查 WSL 状态

```
wsl --status
```

查看有关 WSL 配置的常规信息，例如默认发行版类型、默认发行版和内核版本。

## Help 命令

```
wsl --help
```

查看 WSL 中可用的选项和命令列表。

## 以特定用户的身份运行

```
wsl -u <Username>`, `wsl --user <Username>
```

若要以指定用户身份运行 WSL，请将 `<Username>` 替换为 WSL 发行版中存在的用户名。

## 更改发行版的默认用户

```
<DistributionName> config --default-user <Username>
```

更改用于发行版登录的默认用户。 用户必须已经存在于发行版中才能成为默认用户。

例如：`ubuntu config --default-user johndoe` 会将 Ubuntu 发行版的默认用户更改为“johndoe”用户。



如果在确定发行版名称时遇到问题，请使用命令 `wsl -l`。



此命令不适用于导入的发行版，因为这些发行版没有可执行启动器。 可以改为使用 `/etc/wsl.conf` 文件来更改导入的发行版的默认用户。 请参阅[高级设置配置](https://learn.microsoft.com/zh-cn/windows/wsl/wsl-config#user-settings)文档中的“自动装载”选项。

## 关闭

```
wsl --shutdown
```

立即终止所有正在运行的发行版和 WSL 2 轻量级实用工具虚拟机。 在需要重启 WSL 2 虚拟机环境的情形下，例如[更改内存使用限制](https://learn.microsoft.com/zh-cn/windows/wsl/vhd-size)或更改 [.wslconfig 文件](https://learn.microsoft.com/zh-cn/windows/wsl/manage#)，可能必须使用此命令。

## Terminate

```
wsl --terminate <Distribution Name>
```

若要终止指定的发行版或阻止其运行，请将 `<Distribution Name>` 替换为目标发行版的名称。

## 将发行版导出到 TAR 文件

```
wsl --export <Distribution Name> <FileName>
```

将分发版导出到 tar 文件。 在标准输出中，文件名可以是 -。

## 导入新发行版

```
wsl --import <Distribution Name> <InstallLocation> <FileName>
```

导入指定的 tar 文件作为新的分发版。 在标准输入中，文件名可以是 -。 `--version` 选项还可与此命令一起使用，用于指定导入的发行版将在 WSL 1 还是 WSL 2 上运行。

## 注销或卸载 Linux 发行版

尽管可以通过 Microsoft Store 安装 Linux 发行版，但无法通过 Store 将其卸载。

注销并卸载 WSL 发行版：

```
wsl --unregister <DistributionName>
```

如果将 `<DistributionName>` 替换为目标 Linux 发行版的名称，则将从 WSL 取消注册该发行版，以便可以重新安装或清理它。  **警告：** 取消注册后，与该分发版关联的所有数据、设置和软件将永久丢失。 从 Store 重新安装会安装分发版的干净副本。 例如：`wsl --unregister Ubuntu` 将从可用于 WSL 的发行版中删除 Ubuntu。 运行 `wsl --list` 将会显示它不再列出。

还可以像卸载任何其他应用商店应用程序一样卸载 Windows 计算机上的 Linux 发行版应用。 若要重新安装，请在 Microsoft Store 中找到该发行版，然后选择“启动”。
