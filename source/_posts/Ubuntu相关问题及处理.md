---
title: Ubuntu相关问题及处理
date: 2021-08-13
index_img: /images/fb37ca12540fb58a6073b431b513a309.webp
top_img: /images/fb37ca12540fb58a6073b431b513a309.webp
cover: /images/fb37ca12540fb58a6073b431b513a309.webp
sticky: 5
categories: 
  - Linux系统
---

# Ubuntu下root用户无法通过SSH登录？
如果你的Ubuntu是新安装的，你会发现root用户无法通过SSH登录。这是因为root权限太高可以做任何事，安全起见Ubuntu下的SSH默认不让root登录。 假如一个普通用户有sudo权限，那就可以以普通用户先SSH登录，然后在‘sudo -s’切换成root。这样可行但不是很方便。为了方便起见，我们可以通过修改SSH配置文件让root用户可以直接SSH登录。

1. 打开ssh配置文件*/etc/ssh/sshd_config*

```
vim /etc/ssh/sshd_config
```

2. 找到下面这一行

```
PermitRootLogin prohibit-password
```

3. 将 上面的prohibit-password替换成yes

```
PermitRootLogin yes
```

4. 保存退出

5. 重启sshd.service

```
$ sudo systemctl restart sshd.service
```

完成后root就可以通过SSH登录了，当然需要输入root密码。

注： 如果为了能更方便点还可以改成不需要输入密码：

```
PermitRootLogin without-password
```

# Ubuntu远程SSH无法连接问题
1. 检查虚拟机 ssh是否启动。
```
 ps -e | grep ssh
```

```
1405 ?        00:00:00 ssh-agent
```

2. 没有看到sshd就说明未启动，选择下面的一种方式手动启动就好了
```
sudo service sshd start
sudo /etc/init.d/ssh start
```
3. 正常启动没有提示（可以ps查看是否启动）。如果未安装则会报出以下错误:

```
Failed to start sshd.service: Unit sshd.service not found.
```

5. 使用下面的命令安装即可，安装过程中可能因为（openssh-client）版本不兼容的问题。
```
sudo apt update
sudo apt install openssh-server
```
6. 安装成功后默认就会启动服务。
7. 如果ssh已启动，还是无法连接，那么需要查看ssh的配置文件。监听端口号等信息是否修改
```
cat /etc/ssh/ssh_config
```

# Ubuntu添加Root用户
Ubuntu默认是没有root用户，如果需要登录root用户需要手动创建root用户
1. 输入命令：sudo passwd root
2. new password :密码
3. retype  new passwrod : 密码
4. 提示成功就可以进行切换到root用户。
5. 输入命令 su  进行切换到root用户，然后输入密码就可以登录成功。

# Ubuntu系统恢复修改的.bashrc文件
**初学Ubuntu系统,有时候在配置环境变量的时候会修改.bashrc文件,出错了,怎么办?**

**输入命令 cp /etc/skel/.bashrc ~ **

**恢复成系统缺省的.bashrc**

# 找不到该命令，因为PATH环境变量中不包含“ / snap / bin”
## 临时解决方案：
运行命令 `export PATH=$PATH:/snap/bin`
## 永久解决方案：
编辑`/etc/enviroment`并添加`/snap/bin`到列表中，然后重新启动系统。
1. 打开文件`/etc/environment`。
2. 添加`/snap/bin`到 PATH 变量的末尾并使用`:`字符连接。
   示例让我们假设文件中的 PATH 变量是： `Path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin"`
   更新后，这将如下所示： `/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/snap/bin`
3. 最后更新你的 shell 并准备好使用 PATH 变量，运行 `source /etc/environment`
4. 完毕

# Ubuntu端口命令---查看端口占用及关闭
使用lsof命令查看指定端口：
```
lsof -i:8888
```
若要关闭使用这个端口的程序，使用kill + 对应的pid
```
kill -9 PID号
```
ps：kill就是给某个进程id发送了一个信号。默认发送的信号是SIGTERM，而kill -9发送的信号是SIGKILL，即exit。exit信号不会被系统阻塞，所以kill -9能顺利杀掉进程。

# vim不能复制粘贴

远程登录上liunx服务器上，使用vim打开文本，遇到windows内容不能粘贴到文本里，文本内容不能粘贴到windows上的问题。

解决方法：

Esc退出插入模式,输入
```
set mouse=v
```
即可，但是只是临时有效，下次进入还的从新设置。

可以将设置写入vim配置文件中

配置文件是家目录下.vimc文件，然后source .vimc使配置生效

# ubuntu 连接windows远程桌面 ＆＆rdesktop 退出全屏模式

使用上了ubuntu，怎么接连上我的服务器的远程桌面呢，找了找帮助，使用终端命令就可以了：

sudo apt-get install rdesktop
rdesktop 124.42.120.174:1433

连接成功了。


-f 全屏
-a 16位色
默认端口是3389（linux 22 sh）
注意：windows 的服务中的 Terminal Servies 需要开启。我的电脑 右键 属性 远程中，勾选 允许远程用户链接到此计算机。另外，退出的时候选择注销，而不是关机！

更多参数：
-u xxxxxx 登录用户，可选
-p xxxxxx 登录密码，可选
-r clipboard:PRIMARYCLIPBOARD 重要，剪贴板可以与远程桌面交互
-a 16 颜色，可选，不过最高就是16位
-z 压缩，可选
-g 1024x768 分辨率，可选，缺省是一种比当前本地桌面低的分辨率
-P 缓冲，可选
-r disk:wj=/home/magicgod 映射虚拟盘，可选，会在远程机器的网上邻居里虚拟出一个映射盘，功能很强，甚至可以是软盘或光盘
-r sound:off 关闭声音，当然也可以把远程发的声音映射到本地来。

例：rdesktop -f 192.168.0.184 -u Test3 -p 2013@Miqilai    全屏，直接输入用户名和密码

rdesktop退出全屏模式 ：使用组合键ctrl+alt+enter进行切换。

我的配置：
rdesktop -g 960x1080 -a 16 -u aura-bd -0 192.168.62.241
1. 准备工作：


    ubuntu端：
sudo apt-get install rdesktop
Windows端：
1.计算机—属性—远程设置—远程，勾选：允许远程连接到此计算机；

    2. 远程桌面–允许

    ubuntu端,执行命令：
rdesktop -g 1200*900 -a 16 -u aura-bd -p 0 -0 192.168.62.140

# Ubuntu修改APT源

### 1. 更换软件源

由于Ubuntu默认的软件源在国外，有时候后可能会造成下载软件卡顿，这里我们更换为国内的阿里云源，其他国内源亦可。

双击打开Ubuntu20.04 LTS图标，在命令行中输入

```
# 备份原来的软件源
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
# 编辑软件源
sudo vim /etc/apt/sources.list123
```

将原来的内容替换为

```
deb http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
```
第二步：更新缓存

执行下面的命令：
```
sudo apt-get update
sudo apt-get upgrade
```

清华源：

```
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic main restricted universe multiverse
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-updates main restricted universe multiverse
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-backports main restricted universe multiverse
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-backports main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-security main restricted universe multiverse
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-security main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-proposed main restricted universe multiverse
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-proposed main restricted universe multiverse
```

中科大

```
deb https://mirrors.ustc.edu.cn/ubuntu/ bionic main restricted universe multiverse
deb-src https://mirrors.ustc.edu.cn/ubuntu/ bionic main restricted universe multiverse
deb https://mirrors.ustc.edu.cn/ubuntu/ bionic-updates main restricted universe multiverse
deb-src https://mirrors.ustc.edu.cn/ubuntu/ bionic-updates main restricted universe multiverse
deb https://mirrors.ustc.edu.cn/ubuntu/ bionic-backports main restricted universe multiverse
deb-src https://mirrors.ustc.edu.cn/ubuntu/ bionic-backports main restricted universe multiverse
deb https://mirrors.ustc.edu.cn/ubuntu/ bionic-security main restricted universe multiverse
deb-src https://mirrors.ustc.edu.cn/ubuntu/ bionic-security main restricted universe multiverse
deb https://mirrors.ustc.edu.cn/ubuntu/ bionic-proposed main restricted universe multiverse
deb-src https://mirrors.ustc.edu.cn/ubuntu/ bionic-proposed main restricted universe multiverse
```

163源

```
deb http://mirrors.163.com/ubuntu/ bionic main restricted universe multiverse
deb http://mirrors.163.com/ubuntu/ bionic-security main restricted universe multiverse
deb http://mirrors.163.com/ubuntu/ bionic-updates main restricted universe multiverse
deb http://mirrors.163.com/ubuntu/ bionic-proposed main restricted universe multiverse
deb http://mirrors.163.com/ubuntu/ bionic-backports main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ bionic main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ bionic-security main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ bionic-updates main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ bionic-proposed main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ bionic-backports main restricted universe multiverse
```

# Ubuntu中同时安装jdk8和jdk11
## 一. 安装:

```
sudo apt install openjdk-11-jdk
sudo apt install openjdk-8-jdk
```

## 二. 切换版本:

`sudo update-alternatives --config java`


若提示alternatives找不到则执行以下命令

```
update-alternatives --config java
```

### 3. 切换版本

![在这里插入图片描述](/images/f11b6d2e956b9c7f0259c8813429e4be.webp)

### 根据序号切换你想要使用的jdk

切换后使用命令检查是否生效

```
java -version
```

### 4. 错误情况

若仍然没有变化则可能是因为原本就配置了环境变量的原因
解决办法：
前往 `/etc/profile` 中 找到配置jdk环境变量的地方，全部注释
