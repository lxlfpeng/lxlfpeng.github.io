---
title: Linux系统基础总结
date: 2019-07-04 
categories: 
  - Linux系统
---

# 一.Linux系统
Linux 是一套自由和开放源码的类 Unix 操作系统，是基于 POSIX 和 UNIX 的多用户、多任务、支持多线程和多 CPU 的操作系统。Linux 的设计与 UNIX 类似，但经过不断变革，它已可以在各种硬件上运行(从手机到超级计算机)。每个基于 Linux 的操作系统都包含 Linux 内核（管理着硬件资源）和一组软件包（构成了操作系统的其余部分）。
### 1.Linux内核
[linux](https://github.com/torvalds/linux)内核kernel是操作系统的关键组件。它借助进程间通信和系统调用，在硬件级别上充当应用程序和数据处理之间的桥梁。每当将操作系统加载到内存中时，首先，将加载内核并将其保留在那里，直到操作系统关闭。 内核负责处理低级任务，例如任务管理，内存管理，风险管理等。
Linux内核版本有两种：稳定版和开发版 ，Linux内核版本号由3组数字组成：第一个组数字、第二组数字、第三组数字。
- 第一个组数字：目前发布的内核主版本。
- 第二个组数字：偶数表示稳定版本；奇数表示开发中版本。
- 第三个组数字：错误修补的次数。

### 2.Linux发行版
Linux是一种开放源代码的操作系统内核，Linux操作系统包括Linux内核和Linux用户态程序，Linux内核和Linux用户态程序都是开放源代码的，有相应的开发者来开发及维护。它们绝大多数软件代码遵循GPL协议，
任何人拿到这些代码都可以对这些代码进行修改和分发。由于Linux上代码的高度自由，很多公司和组织都推出了自己的Linux操作系统，这些Linux操作系统我们就叫做Linux发行版。也就是说Linux 的发行版就是将 Linux 内核与应用软件做一个打包。
目前市面上较知名的发行版有：Ubuntu、RedHat、CentOS、Debian、Fedora、SuSE、OpenSUSE、Arch Linux、SolusOS 等，这些众多发行版可能是基于不同的内核版本构建的。
# 二.Linux常用命令
### 1.Linux系统命令
- uname -a                      # 查看内核信息  
- cat /proc/version             # 当前操作系统版本信息
- cat /etc/issue                # 或cat /etc/redhat-release:（Linux查看版本当前操作系统发行版信息）
- hostname                      # 查看计算机名 
- lsmod                         # 列出加载的内核模块 
- shutdown -h now               # 立刻关机
- shutdown -h 5                 # 5分钟后关机
- poweroff                      # 立刻关机
- shutdown -r now               # 立刻重启
- shutdown -r 5                 # 5分钟后重启
- reboot                        # 立刻重启

### 2.Linux资源查看命令
- free -m                       # 选项是以MB为单位来展示内存使用信息; 
  1. total                      # 总计物理内存的大小。
  2. used                       # 已使用多大。
  3. free                       # 可用有多少。
  4. Shared                     # 多个进程共享的内存总额。
  5. Buffers/cached             # 磁盘缓存的大小。
  6. -/+ buffers/cached)
  7. used                       # 已使用多大;
  8. free                       # 可用有多少。
- free -h                       # 选项则是以人类(human)可读的单位来展示。
- grep MemTotal /proc/meminfo   # 查看内存总量 
- grep MemFree /proc/meminfo    # 查看空闲内存量 
- df -h                         # 查看各分区使用情况 
- du -sh <目录名>                # 查看指定目录的大小 
- du -sh                        # 查看当前目录总共占的容量。而不单独列出各子项占用的容量 
- du -lh --max-depth=1          # 查看当前目录下一级子文件和子目录占用的磁盘容量。
- du -sh * | sort -n            # 统计当前文件夹(目录)大小，并按文件大小排序
- du -sk filename               # 查看指定文件大小

### 3.Linux进程查看命令
- ps -ef                   # 查看所有进程 
- top                      # 实时显示进程状态
- top:                     # top命令可以看到总体的系统运行状态和cpu的使用率 。
  1. PID：                 # 当前运行进程的ID
  2. USER：                # 进程属主
  3. PR：                  # 每个进程的优先级别
  4. NInice：              # 反应一个进程“优先级”状态的值，其取值范围是-20至19，一共40个级别。这个值越小，表示进程”优先级”越高，而值越大“优先级”越低。一般会把nice值叫做静态优先级
  5. VIRT：                # 进程占用的虚拟内存
  6. RES：                 # 进程占用的物理内存
  7. SHR：                 # 进程使用的共享内存
  8. S：                   # 进程的状态。S表示休眠，R表示正在运行，Z表示僵死状态，N表示该进程优先值为负数
  9. %CPU：                # 进程占用CPU的使用率
  10. %MEM：               # 进程使用的物理内存和总内存的百分比
  11. TIME+：              # 该进程启动后占用的总的CPU时间，即占用CPU使用时间的累加值。
  12. COMMAND：            # 进程启动命令名称
  
  

### 4.Linux网络及防火墙命令
-  ifconfig                     # 查看所有网络接口的属性 
-  ip addr                      # 查看ip地址
-  iptables -L                  # 查看防火墙设置 
-  route -n                     # 查看路由表 
-  netstat -lntp                # 查看所有监听端口 
-  netstat -antp                # 查看所有已经建立的连接 
-  netstat -s                   # 查看网络统计信息

### 5.Linux文件操作命令
##### (1.)进入文件夹

- cd /home                      # 进入'/ home' 目录' 
- cd ..                         # 返回上一级目录 
- cd ../..                      # 返回上两级目录 
- cd ~                          # 进入个人的主目录 
- cd ~user1                     # 进入个人的主目录 
- cd -                          # 返回上次所在的目录 
##### (2.)列出文件
- ls -a                            # 显示所有文件及目录 (包括以“.”开头的隐藏文件)
- ls -l                            # 使用长格式列出文件及目录信息
- ls -r                            # 将文件以相反次序显示(默认依英文字母次序)
- ls -t                            # 根据最后的修改时间排序
- ls -A                            # 同 -a ，但不列出 “.” (当前目录) 及 “..” (父目录)
- ls -S                            # 根据文件大小排序
- ls -R                            # 递归列出所有子目录
- tree                             # 显示文件和目录由根目录开始的树形结构
- lstree                           # 显示文件和目录由根目录开始的树形结构

##### (3.)复制文件或者文件夹:
- cp -f                              # 若目标文件已存在，则会直接覆盖原文件
- cp -i                              # 若目标文件已存在，则会询问是否覆盖
- cp -p                              # 保留源文件或目录的所有属性
- cp -r                              # 递归复制文件和目录
- cp -d                              # 当复制符号连接时，把目标文件或目录也建立为符号连接，并指向与源文件或目录连接的原始文件或目录
- cp -l                              # 对源文件建立硬连接，而非复制文件
- cp -s                              # 对源文件建立符号连接，而非复制文件
- cp -b                              # 覆盖已存在的文件目标前将目标文件备份
- cp -v                              # 详细显示cp命令执行的操作过程
- cp -a                              # 等价于“dpr”选项

##### (4.)创建文件夹
- mkdir dirName                     # 递归创建多级目录
- mkdir -p parentDir/childDir       # 递归创建多级目录

##### (5.)创建文件
- touch xxx                          # 创建一个xxx的文件
- car > xxx                          # 创建一个xxx并且进入编辑模式

##### (6.)查找文件
- find . -name test.txt              # 在当前目录查找test.txt文件. 代表当前目录
- find / -name test.txt              # 全局查找test.txt文件./代表根目录
- find /usr/tmp -name a*             # 查找/usr/tmp目录下的所有以a开头的目录或文件
- find ./ -name *.log                # 在当前目录查找 以 .log 结尾的文件。 . 代表当前目录

##### (7.)移动或改名文件
- mv -i                              # 若存在同名文件，则向用户询问是否覆盖
- mv -f                              # 覆盖已有文件时，不进行任何提示
- mv -b                              # 当文件存在时，覆盖前为其创建一个备份
- mv -u                              # 当源文件比目标文件新，或者目标文件不存在时，才执行移动此操作

##### (8.)显示当前位置
- pwd                                # 显示当前路径
- pwd -L                             # 显示逻辑路径

##### (9.)删除文件
- rm -f file1                      # 删除一个叫做 'file1' 的文件' 
- rm -rf dirName                   # 删除整个文件夹
- rmdir dir1                       # 删除一个叫做 'dir1' 的目录' 

### 6.Linux用户和群组管理命令
- whoami	                                                            # 查看当前用户
- passwd test	                                                        # 给test用户设置用户密码
- groupadd group_name                                                   # 创建一个新用户组 
- groupdel group_name                                                   # 删除一个用户组 
- groupmod -n new_group_name old_group_name                             # 重命名一个用户组 
- useradd -c "Name Surname " -g admin -d /home/user1 -s /bin/bash user1 # 创建一个属于 "admin" 用户组的用户 
- useradd user1                                                         # 创建一个新用户 
- userdel -r user1                                                      # 删除一个用户 ( '-r' 排除主目录) 
- usermod -c "User FTP" -g system -d /ftp/user1 -s /bin/nologin user1   # 修改用户属性 
- passwd                                                                # 修改口令 
- passwd user1                                                          # 修改一个用户的口令 (只允许root执行) 
- chage -E 2005-12-31 user1                                             # 设置用户口令的失效期限 
- pwck                                                                  # 检查 '/etc/passwd'的文件格式和语法修正以及存在的用户 
- grpck                                                                 # 检查 '/etc/passwd' 的文件格式和语法修正以及存在的群组 
- newgrp group_name                                                     # 登陆进一个新的群组以改变新创建文件的预设群组 
- su:                                                                   # 切换到root账户
- su test:                                                              # 切换到test账户
-  w                                                                    # 查看活动用户 
-  id <usename>                                                         # 查看指定用户信息 
-  last                                                                 # 查看用户登录日志 
-  cut -d: -f1 /etc/passwd                                              # 查看系统所有用户 
-  cut -d: -f1 /etc/group                                               # 查看系统所有组 
-  crontab -l                                                           # 查看当前用户的计划任务

### 7.Linux权限命令
- ls -lh                                    # 显示权限 
- ls /tmp | pr -T5 -W$COLUMNS               # 将终端划分成5栏显示 
- chmod ugo+rwx directory1                  # 设置目录的所有人(u)、群组(g)以及其他人(o)以读（r ）、写(w)和执行(x)的权限 
- chmod go-rwx directory1                   # 删除群组(g)与其他人(o)对目录的读写执行权限 
- chown user1 file1                         # 改变一个文件的所有人属性 
- chown -R user1 directory1                 # 改变一个目录的所有人属性并同时改变改目录下所有文件的属性 
- chgrp group1 file1                        # 改变文件的群组 
- chown user1:group1 file1                  # 改变一个文件的所有人和群组属性 
- find / -perm -u+s                         # 罗列一个系统中所有使用了SUID控制的文件 
- chmod u+s /bin/file1                      # 设置一个二进制文件的 SUID 位 - 运行该文件的用户也被赋予和所有者同样的权限 
- chmod u-s /bin/file1                      # 禁用一个二进制文件的 SUID位 
- chmod g+s /home/public                    # 设置一个目录的SGID 位 - 类似SUID ，不过这是针对目录的 
- chmod g-s /home/public                    # 禁用一个目录的 SGID 位 
- chmod o+t /home/public                    # 设置一个文件的 STIKY 位 - 只允许合法所有人删除文件 
- chmod o-t /home/public                    # 禁用一个目录的 STIKY 位 

### 8.Linux打包和压缩命令
- bunzip2 file1.bz2                         # 解压一个叫做 'file1.bz2'的文件 
- bzip2 file1                               # 压缩一个叫做 'file1' 的文件 
- gunzip file1.gz                           # 解压一个叫做 'file1.gz'的文件 
- gzip file1                                # 压缩一个叫做 'file1'的文件 
- gzip -9 file1                             # 最大程度压缩 
- rar a file1.rar test_file                 # 创建一个叫做 'file1.rar' 的包 
- rar a file1.rar file1 file2 dir1          # 同时压缩 'file1'， 'file2' 以及目录 'dir1' 
- rar x file1.rar                           # 解压rar包 
- unrar x file1.rar                         # 解压rar包 
- tar -cvf archive.tar file1                # 创建一个非压缩的 tarball 
- tar -cvf archive.tar file1 file2 dir1     # 创建一个包含了 'file1'， 'file2' 以及 'dir1'的档案文件 
- tar -tf archive.tar                       # 显示一个包中的内容 
- tar -xvf archive.tar                      # 释放一个包 
- tar -xvf archive.tar -C /tmp              # 将压缩包释放到 /tmp目录下 
- tar -cvfj archive.tar.bz2 dir1            # 创建一个bzip2格式的压缩包 
- tar -xvfj archive.tar.bz2                 # 解压一个bzip2格式的压缩包 
- tar -cvfz archive.tar.gz dir1             # 创建一个gzip格式的压缩包 
- tar -xvfz archive.tar.gz                  # 解压一个gzip格式的压缩包 
- zip file1.zip file1                       # 创建一个zip格式的压缩包 
- zip -r file1.zip file1 file2 dir1         # 将几个文件和目录同时压缩成一个zip格式的压缩包 
- unzip file1.zip                           # 解压一个zip格式压缩包 

### 9.Linux防火墙命令
- systemctl start firewalld                                         # 启动 firewalld
- systemctl status firewalld / firewall-cmd --state                 # 查看状态：这个命令也可以，只是信息会简单点
- systemctl disable firewalld                                       # 停止firewalld
- systemctl stop firewalld                                          # 禁用 firewalld
- firewall-cmd --zone=public --add-port=80/tcp --permanent          # 开启一个端口（--permanent永久生效，没有此参数重启后失效）
- firewall-cmd --add-port=80/tcp                                    # 添加端口外部访问权限（这样外部才能访问）
- firewall-cmd --reload                                             # 重新载入，添加端口后重新载入才能起作用.这些之后，端口是开启成功的，如果没有成功，重启系统试试。
- firewall-cmd --state                                              # 查看防火墙状态
- systemctl stop firewalld.service                                  # 关闭防火墙
- systemctl start firewalld.service                                 # 启动防火墙
- systemctl enable firewalld.service                                # 设置开机自动启动
- systemctl disable firewalld.service                               # 关闭开机启动
- firewall-cmd --zone=public --list-ports                           # 查看防火墙所有开放的端口
- firewall-cmd --zone=public --add-port=8080-8081/tcp --permanent   # 永久开启某个(某段)端口
- firewall-cmd --zone=public --add-port=8080-8081/tcp               # 临时开启某个(某段)端口
- firewall-cmd --zone=public --add-port=5672/tcp --permanent        # 永久开放5672端口
- firewall-cmd --zone=public --remove-port=5672/tcp --permanent     # 永久关闭5672端口
- firewall-cmd --reload                                             # 在不改变状态的条件下重新加载防火墙--配置立即生效
- netstat -tunlp | grep 8081                                        # 查看具体某个端口【模糊查询】
- lsof -i:8081                                                      # 查看具体某个端口【精确查询】
- firewall-cmd --list-ports                                         # 查看开放的所有端口
- firewall-cmd --get-service                                        # 获取所有支持的服务
- firewall-cmd --zone=public --add-service=https                    # 临时 启动某个服务 
- firewall-cmd --permanent --zone=public --add-service=https        # 永久启动某个服务 
- iptables -L -n | grep 21                                          # 检查设定是否生效 

# 三.Linux用户，用户组和密码
### 1.Linux用户
Linux系统是一个多用户多任务的分时操作系统，也就是说Linux 系统支持多个用户在同一时间内登陆，不同用户可以执行不同的任务，并且互不影响。任何一个要使用系统资源的用户，都必须首先向系统管理员申请一个账号，每个用户都有唯一的用户名和密码。在登录系统时，只有正确输入用户名和密码，才能进入系统和自己的主目录。用户的账号一方面可以帮助系统管理员对使用系统的用户进行跟踪，并控制他们对系统资源的访问；另一方面也可以帮助用户组织文件，并为用户提供安全性保护。

|超级用户root	|系统用户	|普通用户|
|-|-|-|
|权限	|具有一切权限	|为了满足相应的系统进程对文件属主的要求而建立的系统用户不能用来登录|	由管理员赋予的一般权限|
|功能	|管理系统的各项功能，如添加/删除用户、启动/关闭服务进程、开启/禁用硬件设备|Linux系统正常工作所必需的内建的用户，例如：bin、daemon、adm、lp等|	由管理员创建的用于日常工作的用户|
|UID	|0	|1～999	|从1000开始|

### 2.Linux用户组
用户组是具有相同特征用户的逻辑集合。简单的理解，有时我们需要让多个用户具有相同的权限，比如查看、修改某一个文件的权限，一种方法是分别对多个用户进行文件访问授权，如果用户过多需要分别进行授权这种方法不太合理。通过建立一个组，让这个组具有查看、修改此文件的权限，然后将所有需要访问此文件的用户放入这个组中。那么，所有用户就具有了和组一样的权限，这就是用户组。

### 3.Linux用户相关文件
Linux不像Windows 那样有专门的数据库用来存放用户的信息，Linux系统采用纯文本文件来保存账号的各种信息，其中最重要的文件有/etc/passwd、/etc/shadow、/etc/group等。账号的管理实际上就是对这几个文件的内容进行添加、修改和删除记录行的操作。Linux中所有用户(包括系统管理员)的账号和密码都可以在/etc/passwd和/etc/shadow这两个文件中找到，/etc/passwd只有系统管理员才可以修改的，该文件对所有用户可读。/etc/shadow文件是passwd文件的一个影子，/etc/shadow文件中的记录行与/etc/passwd中的一一对应，它由pwconv命令根据/etc/passwd中的数据自动产生。但是/etc/shadow其他用户看不了，/etc/shadow文件只有系统管理员才能够进行修改和查看。
|文件目录|功能|
|-|-|
|/etc/passwd	|用户帐号信息保存在passwd文件中|
|/etc/shadow	|用户的加密口令保存在shadow文件中|
|/home/teacher	|用户的宿主目录是home目录中与用户名称相同的目录|
|/etc/skel	    |用户的初始配置文件来在skel目录（配置模版）|
|/etc/group	    |存放关于组的信息|
>Linux系统为了自己的安全，缺省情况下只允许超级用户更改它们。

##### (1.)Linux查看用户信息
Linux 系统中的 /etc/passwd 文件，是系统用户配置文件，存储了系统中所有用户的基本信息，并且所有用户都可以对此文件执行读操作。
```
cat /etc/passwd
```

该文件中，每一行的存储格式为：
```
账号名称 : 密码 : UID : GID : 用户信息说明列 : 主文件夹 : shell

root : x : 0 : 0 : root : /root : /bin/bash
```
其中，密码项显示 “x” 是出于安全考虑，Linux 将密码信息移到 /etc/shadow 进行存储；每一个用户都有一个UID、GID，对应的含义就是UserID、GroupID，UID 会映射到 /etc/shadow 以获得密码信息，GID 会映射到 /etc/group 以获取用户的用户组信息。
##### (2.)Linux查看用户密码
```
cat /etc/shadow
```
该文件中，每一行的存储格式为：
```
账号名称 : 密码 : 最近改动密码的日期 : 密码不可被改变的天数 : 密码需要重新更改的天数 : 更改提醒天数 : 密码过期后账号的宽限时间 : 账号失效日期 : 保留

root : (字符串，此处打码) : 200 : 0 : 99999 : 7 : : :
```
其中第二列表示密码加密后的字符串。

##### (3.)Linux查看用户组
```
cat /etc/group
```
该文件中，每一行的存储格式为：
```
用户组名称 : 用户组密码 : GID : 此用户组包含的账号名称

root : x : 0 : root
```
其中，用户组密码通常是为了设置用户组管理员存在的，其信息也移动到 /etc/gshadow 中；/etc/passwd 通过 GID，在该文件中找到对应的用户组，并提取用户组相关信息； 由于一个用户可以在多个用户组中，因此就有一个初始用户组的有效用户组的概念。所谓的初始用户组，就是用户所记录的 GID，是在创建用户时生成或指定的用户组；所谓的有效用户组，就是利用命令 groups 查看并输出的首个用户组，即有效用户组；用户在登录的时候，以初始用户组身份工作，用户可以用 newgrp 命令实现有效用户组的切换。
##### (4.)Linux查看用户组密码
```
cat /etc/gshadow
```
该文件中，每一行的存储格式为：
```
用户组名 : 密码 : 用户组管理员账号 : 该用户组包含的账号名称

root : : : root
```
一般用户组不使用用户组管理员，相应地也就不需要设置密码。

### 4.Linux用户切换
切换用户的命令是su，su是(switch user)切换用户的缩写。通过su命令，可以从普通用户切换到root用户，也可以从root用户切换到普通用户。
从普通用户切换到root用户或者从普通用户切换到普通用户都需要密码(该密码是普通用户的密码)，从root用户切换到普通用户不需要密码，直接可切换成功。
su 命令的基本格式如下：
```
[root@localhost ~]# su [选项] 用户名
```
选项：
-：当前用户不仅切换为指定用户的身份，同时所用的工作环境也切换为此用户的环境（包括 PATH 变量、MAIL 变量等），使用 - 选项可省略用户名，默认会切换为 root 用户。
-l：同 - 的使用类似，也就是在切换用户身份的同时，完整切换工作环境，但后面需要添加欲切换的使用者账号。
-p：表示切换为指定用户的身份，但不改变当前的工作环境（不使用切换用户的配置文件）。
-m：和 -p 一样；
-c 命令：仅切换用户执行一次命令，执行后自动切换回来，该选项后通常会带有要执行的命令。


>注意，使用 su 命令时，有 - 和没有 - 是完全不同的，- 选项表示在切换用户身份的同时，连当前使用的环境变量也切换成指定用户的。我们知道，环境变量是用来定义操作系统环境的，因此如果系统环境没有随用户身份切换，很多命令无法正确执行。

### 5.sudo执行
sudo 是一种权限管理机制，管理员可以授权于一些普通用户去执行一些 root 执行的操作，而不需要知道 root 的密码。普通用户可以通过 sudo 命令，使用 root 用户权限来执行命令。
当然，不是所有的用户都能执行 sudo 命令的，而是在 /etc/sudoers 文件内的用户才能执行这个命令。sudo 的执行流程大致为：
1. 系统到 /etc/sudoers 下检查用户是否有执行 sudo 的权限
2. 若有 sudo 权限，则需要输入本用户的密码（root 用户执行 sudo 不需要密码）
3. 验证成功后执行命令
因此，关键在于执行 sudo 的用户是否存在于 /etc/sudoers 文件内。
要想使一个用户具有使用sudo的能力，需要让root用户将其名字、可以执行的特定命令、按照哪种用户或用户组的身份执行等信息注册到/etc/sudoers文件中，即完成对该用户的授权（此时该用户称为“sudoer”）才可以。
当一般用户执行特殊权限时，在命令前加上 sudo，此时系统会让你输入密码以确认终端机前操作的是你本人，确认后系统会将该命令的进程以超级用户的权限运行。

# 四.Linux的目录结构和访问权限
### 1.Linux的目录结构

|目录名|作用|
|-|-|
|/：              | 根目录，一般根目录下只存放目录，在Linux下有且只有一个根目录。所有的东西都是从这里开始。当你在终端里输入“/home”，你其实是在告诉电脑，先从/（根目录）开始，再进入到home目录。|
|/bin、/usr/bin:  | 可执行二进制文件的目录，如常用的命令ls、tar、mv、cat等。|
|/boot：          | 放置linux系统启动时用到的一些文件，如Linux的内核文件：/boot/vmlinuz，系统引导管理器：/boot/grub。|
|/dev：           | 存放linux系统下的设备文件，访问该目录下某个文件，相当于访问某个设备，常用的是挂载光驱 mount /dev/cdrom /mnt。|
|/etc：           | 系统配置文件存放的目录，不建议在此目录下存放可执行文件，重要的配置文件有 /etc/inittab、/etc/fstab、/etc/init.d、/etc/X11、/etc/sysconfig、/etc/xinetd.d。|
|/home：          | 系统默认的用户家目录，新增用户账号时，用户的家目录都存放在此目录下，~表示当前用户的家目录，~edu 表示用户 edu 的家目录。|
|/lib、/usr/lib、/usr/local/lib： | 系统使用的函数库的目录，程序在执行过程中，需要调用一些额外的参数时需要函数库的协助。|
|/lost+fount：    | 系统异常产生错误时，会将一些遗失的片段放置于此目录下。|
|/mnt: /media：   | 光盘默认挂载点，通常光盘挂载于 /mnt/cdrom 下，也不一定，可以选择任意位置进行挂载。|
|/opt：           | 给主机额外安装软件所摆放的目录。|
|/proc：          | 此目录的数据都在内存中，如系统核心，外部设备，网络状态，由于数据都存放于内存中，所以不占用磁盘空间，比较重要的目录有 /proc/cpuinfo、/proc/interrupts、/proc/dma、/proc/ioports、/proc/net/* 等。|
|/root：          | 系统管理员root的家目录。|
|/sbin、/usr/sbin、/usr/local/sbin：| 放置系统管理员使用的可执行命令，如fdisk、shutdown、mount 等。与 /bin 不同的是，这几个目录是给系统管理员 root使用的命令，一般用户只能"查看"而不能设置和使用。|
|/tmp：                             | 一般用户或正在执行的程序临时存放文件的目录，任何人都可以访问，重要数据不可放置在此目录下。|
|/srv：                             | 服务启动之后需要访问的数据目录，如 www 服务需要访问的网页数据存放在 /srv/www 内。|
|/usr：                             | 应用程序存放目录，/usr/bin 存放应用程序，/usr/share 存放共享数据，/usr/lib 存放不能直接运行的，却是许多程序运行所必需的一些函数库文件。/usr/local: 存放软件升级包。/usr/share/doc: 系统说明文件存放目录。/usr/share/man: 程序说明文件存放目录。|
|/var：                             | 放置系统执行过程中经常变化的文件，如随时更改的日志文件 /var/log，/var/log/message：所有的登录文件存放目录，/var/spool/mail：邮件存放的目录，/var/run:程序或服务启动后，其PID存放在该目录下。|

### 2.Linux访问用户与访问权限
1.访问用户：所有者，用户组，其他用户
2.访问权限：
![image.png](/images/0cad7d04bcd60b6b2e8a6184b6c24498.webp)
- 读权限（r）： 对文件而言，具有读取文件内容的权限；对目录来说，具有浏览目录的权限。
- 写权限（w）： 对文件而言，具有新增、修改文件内容的权限；对目录来说，具有删除、移动目录内文件的权限。
- 可执行权限（x）： 对文件而言，具有执行文件的权限；对目录了来说该用户具有进入目录的权限。

- 第1个字母代表文件的类型：“d” 代表文件夹、“-” 代表普通文件、“c” 代表硬件字符设备、“b” 代表硬件块设备、“s”表示管道文件、“l” 代表软链接文件。 后 9 个字母分别代表三组权限：文件所有者、用户者、其他用户拥有的权限。
- 每一个用户都有它自身的读、写和执行权限。
- 第一组权限控制访问自己的文件权限，即所有者权限。
- 第二组权限控制用户组访问其中一个用户的文件的权限。
- 第三组权限控制其他所有用户访问一个用户的文件的权限。

# 五.linux软件和包管理
一个“ 包(package)”(或“软件包”)通常指的是一个应用程序，它可以是一个 GUI 应用程序、 行工具或(其他软件程序需要的)软件库。包本质上是一个存档文件，包含二进制可执行文件、配置文件，有时还包含依赖关系的信息。linux软件包的安装一般是有三种形式:
1. 源码安装
2. 二进制包(RPM包、deb包)
3. 云端包管理器安装(yum安装 （RedHat、CentOS），apt-get安装 （debian，ubuntu）)
|操作系统	|格式	|工具|
|-|-|-|
|Debian	|.deb	|apt， apt-cache， apt-get， dpkg|
|Ubuntu	|.deb	|apt， apt-cache， apt-get， dpkg|
|CentOS	|.rpm	|yum|
### 1.Linux源码安装软件
在之前的linux系统中，很多新版本的软件包的更新都会优先提供tar包版本的，然后各linux厂商拿到这个tar包之后再给自己的操作系统提供官方的rpm或者dpkg类型的软件包，
而这种tar工具打包的软件包我们一般称之为源码包，在这些源码包中一般包含有，程序源代码文件，配置文件（configure）或 Makefile，安装使用说明（INSTALL，HOWTO，README）
你必须自己编译该软件或自己处理所有的依赖关系(有些软件需要安装其他软件)。这种tar包源码包简单的安装流程就是:
1. 获取软件包
2. 解压文件
3. 检查当前系统是否满足软件包安装需求
4. 使用gcc进行编译，生成主要的二进制文件
5. 将二进制文件安装到主机
这些步骤看起来很简单，但是在使用过程中有很多问题需要解决，比如说需要解决系统环境，权限问题等等，不同类型的软件在安装方法上会有差异，但是整体步骤就是我们上面所提到的。
源码安装的流程一般是三部曲：
```
./configure
make
make install  
```
1. ./configure是为了检测目标安装平台的特征，并且检查依赖的软件包是否可用或者是否缺少依赖软件包，configure事实上是个脚本，最终的目的是生成Makefile。
2. 如果第一条指令没有报错，会生成一个Makefile，make指令就是编译这个源码包
3. 正常编译完之后如果没有报错，就生成了可执行文件，make install指令就是将可执行文件放到指定目录并配置环境变量，允许我们在任何目录下使用这个软件。
优点：
- 开源，源代码可改
- 自由选择功能，灵活
- 和自身系统耦合度低，稳定，效率高
- 卸载方便

缺点：
- 安装麻烦，容易出错
- 编译时间长
- 要求高，编译出错，新手很难解决

### 2.linux源码二进制包软件
前面我们提到过源码包安装需要解决系统环境、权限等等，这些对于初学者而言都是噩梦一般的存在，所以linux厂商推出了一种类似windows系统中的安装方式，
有开发者直接在已知的系统中编译好，使用者可以直接下载并进行安装，升级，卸载等操作。Debian 及其衍生版，如 Ubuntu、Linux Mint 和 Raspbian，它们的包格式是 .deb。
CentOS、Fedora 和其它 Red Hat 家族成员使用 RPM 文件。
优点：
- 安装维护方便，只通过几个命令就可以实现包的安装、升级、查询和卸载
- 安装速度快
缺点：
- 编译后，不再看到源代码
- 功能可选择性差，不灵活
- 依赖性高
##### (1.)dpkg包管理工具
dpkg直接将二进制的文档复制进计算机的/usr目录中，省去你大量编译的时间(毕竟现在电脑不是i686就是x86_64)，这也拯救了那些没有自带编译器的系统。
然而，你要知道就算你想装的软件包只有一个，你还是得装大量的软件包，这就是Linux界软件包的依赖关系。一个软件包会调用其他软件包的可执行文件(如python脚本)，
以及库文件(那些以lib开头的文件)，这就很蛋疼了。
- dpkg -i package   #安装包
- dpkg -R /usr/local/src   #安装一个目录下面所有的软件包
- dpkg --unpack package    #解开一个包，如果和-R一起使用，参数可以是一个目录
- dpkg --configure package    #重新配置和释放软件包
- dpkg -r package  #删除包
- dpkg --merge-avail      #合并包
- dpkg -P  #删除包，包括配置文件
- dpkg -A package   #从软件包里面读取软件的信息
- dpkg --update-avail    #替代软件包的信息
- dpkg --forget-old-unavail    #删除Uninstall的软件包信息
- dpkg --clear-avail   #删除软件包的Avaliable信息
- dpkg -C   #查找只有部分安装的软件包信息
- dpkg --compare-versions ver1 op ver2  #比较同一个包的不同版本之间的差别
- dpkg -b directory [filename]    #建立一个deb文件
- dpkg -c filename  #显示一个Deb文件的目录
- dpkg -p package   #显示包的具体信息
- dpkg -S filename-search-pattern    #搜索指定包里面的文件（模糊查询）
- dpkg -L package    #显示一个包安装到系统里面的文件目录信息
- dpkg -s package    #报告指定包的状态信息
- dpkg -l    #显示所有已经安装的Deb包，同时显示版本号以及简短说明
##### (2.)rpm包管理工具
商业大佬Redhat因为对Debian的dpkg羡慕嫉妒恨，也开发了一个叫rpm的软件包管理器，其本质也是和dpkg相似，
都是将二进制可执行文件/字节码/脚本复制到计算机硬盘中。 
rpm最早是由redhat开发出来，由于很好用，所以很多发行版也利用rpm来进行软件包的管理。RPM全名RedHat Package Manager，
最大的特点就是把需要安装的软件提前编译，打包，然后在rpm包里面存放了用以记录软件依赖关系的相关数据，
当用户安装时，优先查看这些数据，如果系统满足数据要求就安装软件包，否则不能安装，安装完成后，将软件包相关信息记录到rpm自己的数据库中，便于查询和卸载等。
所以说rpm的优点是方便安装，卸载，查询，缺点就是只能在指定的操作系统上使用，所以不同厂商的rpm包，甚至同一厂商不同版本操作系统的rpm包都不通用。

rpm包的相关文件一般都会放在对应的目录中，比如rpm包安装后，配置文件会放在/etc下，执行文件会放在/usr/bin下，链接库文件会放在/usr/lib下，
帮助与说明文档会放在/usr/share/man和/usr/share/doc目录下.

RPM常用选项：
-i：表示安装。
-v， -vv， -vvv：表示详细信息。
-h：以"#"号显示安装进度。
-q：查询指定包名。
-e：卸载指定包名。
-U：升级软件，若未软件尚未安装，则安装软件。
-F：升级软件。
-V：对RPM包进行验证。
--nodeps：忽略依赖关系。
--query：查询指定包名。同-q选项。
--hash：同-h。
--install：表示安装，同-i选项。
--test：仅作测试，不真正执行，可用于测试安装，测试卸载。
--replacepkgs：重新安装。替换原有的安装。
--force：忽略软件包及文件的冲突。
--initdb：新建RPM的数据库。
--rebuilddb：重建RPM的数据库。
--percent：以百分比的形式输出安装的进度。

RPM包的查询：
rpm -q：查询某一个RPM包是否已安装
rpm -qi：查询某一个RPM包的详细信息
rpm -ql：列出某RPM包中所包含的文件。
rpm -qf：查询某文件是哪个RPM包生成的。
rpm -qa：列出当前系统所有已安装的包

>通常，用tar打包的，都是源程序;而用rpm、dpkg打包的则常是可执行程序。一般来说，自己动手编译源程序能够更具灵活性，但也容易遇到各种问题和困难。
而相对来说，下载那些可执行程序包，反而是更容易完成软件的安装，当然那样灵活性就差多了。所以一般一个软件总会提供多种打包格式的安装程 序的。你可以根据自己的情况来选择。

### 3.apt/yum/dnf通过云端管理包
为了解决依赖关系这个蛋疼的事情，Debian系和Redhat系分别开发出了自己的工具。
apt是Debian开发的软件包管理器，apt可以通过从网络站点下载软件包，并自动解决Debian系统的软件包依赖关系，
这就是为什么你装一个GNOME3可能你要装一大堆没有用的软件包，当然如果你是精简派人物你也可以用--no-install-recommends参数解决。
而Redhat用了yum这个软件包管理器，和apt不同，yum用python进行编写，这样就表明了它具有比apt更好的拓展性，可以用一些python脚本添加一些功能。
however，这是有代价的，由于使用的是脚本语言，速度会慢于apt。由于python2式微，现在Redhat在使用新的软件包管理器dnf，它用python3编写，还支持多线程下载，apt到现在还是没有这个功能。
#### (1.)apt/apt-get包管理工具
使用apt-get的主流Linux系统包括Debian和Ubuntu变异版本。

###### apt-get相关的目录
形如 apt-get install apps 这样的命令，一般会将下载文件放在 /var/cache/apt/archives目录下，然后安装。
如果不及时清理，这个目录所占空间会越来越大，幸运的是apt提供了相应的管理工具apt-get clean删除/var/cache/apt/archives/ 和 /var/cache/apt/archives/partial/目录下所有包(锁定的除外)。
apt-get autoclean仅删除不再能被下载的包。 
一般安装软件都是使用apt-get install。那么安装完后，软件的安装目录为:
- 下载的软件的存放位置：/var/cache/apt/archives
- 安装后软件的默认位置：/usr/share
- 可执行文件位置：/usr/bin
- 配置文件位置：/etc
- lib文件位置：/usr/lib
```
#文件的内容是软件包的描述信息， 该软件包括当前系统所使用的 ubunt 安装源中的所有软件包，其中包括当前系统中已安装的和未安装的软件包.
/var/lib/dpkg/available

#目录是在用 apt-get install 安装软件时，软件包的临时存放路径
/var/cache/apt/archives

#存放的是软件源站点
/etc/apt/sources.list

#使用apt-get update命令会从/etc/apt/sources.list中下载软件列表，并保存到该目录
/var/lib/apt/lists
```
##### 常用的APT命令参数
- apt-cache search package 搜索包
- apt-cache show package 获取包的相关信息，如说明、大小、版本等
- sudo apt-get install package 安装一个新软件包
- sudo apt-get install package - - reinstall 重新安装一个新软件包
- sudo apt-get -f install 修复安装"-f = ――fix-missing"
- sudo apt-get remove package 删除包
- sudo apt-get remove package - - purge 删除包，包括删除配置文件等
- sudo apt-get update 更新源
- sudo apt-get upgrade 更新已安装的包
- sudo apt-get dist-upgrade 升级系统
- sudo apt-get dselect-upgrade 使用 dselect 升级
- apt-cache depends package 了解使用依赖
- apt-cache rdepends package 是查看该包被哪些包依赖
- sudo apt-get build-dep package 安装相关的编译环境
- apt-get source package 下载该包的源代码
- sudo apt-get clean && sudo apt-get autoclean 清理无用的包
- sudo apt-get check 检查是否有损坏的依赖
- apt-cache search packagename 搜索包
- apt-cache show packagename 获取包的相关信息，如说明、大小、版本等
- apt-get remove packagename 删除包
- apt-get remove packagename - - purge 删除包，包括删除配置文件等
- apt-get remove --purge packagename #卸载一个已安装的软件包（删除配置文档）
- apt-get autoremove packagename #删除包及其依赖的软件包
- apt-get autoremove --purge packagname #删除包及其依赖的软件包+配置文件，比上面的要删除的彻底一点
- dpkg --force-all --purge packagename #有些软件很难卸载，而且还阻止了别的软件的应用，就能够用这个，但是有点冒险。
##### APT换源
1、备份当前的源文件。
```
cp /etc/apt/source.list /etc/apt/source.list.bak
```
2、编辑新的源文件。
```
vim /etc/apt/source.list
```
3、将原来的列表删除，添加如下内容（阿里镜像源）
```
deb http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multivers
deb http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse
```
4、更新系统apt的源，让新的源配置生效；
```
sudo apt-get update 
```
#### (2.)yum包管理工具
yum（ Yellow dog Updater， Modified）是一个在 Fedora 和 RedHat 以及 SUSE 中的 Shell 前端软件包管理器。
基于 RPM 包管理，能够从指定的服务器自动下载 RPM 包并且安装，可以自动处理依赖性关系，并且一次安装所有依赖的软件包，无须繁琐地一次次下载、安装。

YUM被称为 Yellow dog Updater， Modified，是一个在Fedora和RedHat以及SUSE中的Shell前端软件包管理器。YUM使用Python语言写成。YUM客户端基于RPM包进行管理，
可以通过HTTP服务器下载、FTP服务器下载、本地软件池的等方式获得软件包，可以从指定的服务器自动下载RPM包并且安装，可以自动处理依赖性关系。YUM在安装RPM时，会从服务器下载相应包，且缓存在本地。

rpm软件包形式的管理虽然方便，但是需要手工解决软件包的依赖关系。很多时候安装一个软件安装一个软件需要安装1个或者多个其他软件，手动解决时，很复杂，yum解决这些问题。
Yum是rpm的前端程序，主要目的是设计用来自动解决rpm的依赖关系，其特点：
1. 自动解决依赖关系
2. 可以对rpm进行分组，基于组进行安装操作
3. 引入仓库概念，支持多个仓库
4. 配置简单
5. yum仓库用来存放所有的现有的.rpm包，当使用yum安装一个rpm包时，需要依赖关系，会自动在仓库中查找依赖软件并安装。仓库可以是本地的，也可以是HTTP、FTP、nfs形式使用的集中地、统一的网络仓库。
6. 仓库的配置文件/etc/yum.repos.d目录下

使用YUM进行RPM包的管理，非常简单方便。

##### yum 语法
yum [options] [command] [package ...]
options：可选，选项包括-h（帮助），-y（当安装过程提示选择全部为 "yes"），-q（不显示安装的过程）等等。
command：要进行的操作。
package：安装的包名。
##### yum常用命令
1. 安装
- yum install 全部安装
- yum install package1 安装指定的安装包package1
- yum groupinsall group1 安装程序组group1
2. 更新和升级
- yum update 全部更新
- yum update package1 更新指定程序包package1
- yum check-update 检查可更新的程序
- yum upgrade package1 升级指定程序包package1
- yum groupupdate group1 升级程序组group1
3. 查找和显示
- yum info package1 显示安装包信息package1
- yum list 显示所有已经安装和可以安装的程序包
- yum list package1 显示指定程序包安装情况package1
- yum groupinfo group1 显示程序组group1信息yum search string 根据关键字string查找安装包
4. 删除程序
- yum remove &#124; erase package1 删除程序包package1
- yum groupremove group1 删除程序组group1
- yum deplist package1 查看程序package1依赖情况
5. 清除缓存
- yum clean packages 清除缓存目录下的软件包
- yum clean headers 清除缓存目录下的 headers
- yum clean oldheaders 清除缓存目录下旧的 headers
- yum clean， yum clean all (= yum clean packages; yum clean oldheaders) 清除缓存目录下的软件包及旧的headers
##### yum换源
使用yum的官方源进行yum install xxxx 的时候，速度非常慢，只有几kB/s，有时候还不到1kB/s。这就会造成安装包的速度的速度要么特变慢，要么就根本安装不了。
修改yum源为阿里源
1. 查看yum源信息:
```
yum repolist
```
2. 定位到base reop源位置
```
cd /etc/yum.repos.d
```
3. 接着备份旧的配置文件
```
sudo mv CentOS-Base.repo CentOS-Base.repo.bak
```
4. 下载阿里源的文件CentOS-Base.repo 到 /etc/yum.repos.d/
CentOS6:
```
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-6.repo
```
CentOS7:
```
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
```
5.清理缓存
```
yum clean all
```
6.重新生成缓存
```
yum makecache
```
7. 再次查看yum源信息
```
yum repolist
```

# 六.Linux服务管理
### 1.Linux服务
服务(service) 本质就是进程，但是是运行在后台的，通常都会监听某个端口，等待其它程序的请求，比如(mysql ， sshd 防火墙等)，因此我们又称为守护进程。
|指令|作用|
|-|-|
|systemctl start                            |服务名	开启服务 |
|systemctl stop                             |服务名	关闭服务 |
|systemctl status                           |服务名	显示状态 |
|systemctl restart                          |服务名	重启服务 |
|systemctl enable                           |服务名	开机启动服务 |
|systemctl disable                          |服务名	禁止开机启动 |
|systemctl list-units	                    |查看系统中所有正在运行的服务 |
|systemctl list-unit-files	                |查看系统中所有服务的开机启动状态 |
|systemctl list-dependencies                |服务名	查看系统中服务的依赖关系 |
|systemctl mask                             |服务名	冻结服务 |
|systemctl unmask                           |服务名	解冻服务 |
|systemctl set-default multi-user.target	|开机时不启动图形界面 |
|systemctl set-default graphical.target	    |开机时启动图形界面 |

systemctl和service、chkconfig命令的关系:
- systemctl命令：是一个systemd工具，主要负责控制systemd系统和服务管理器。
- service命令：可以启动、停止、重新启动和关闭系统服务，还可以显示所有系统服务的当前状态。
- chkconfig命令：是管理系统服务(service)的命令行工具。所谓系统服务(service)，就是随系统启动而启动，随系统关闭而关闭的程序。

systemctl命令是系统服务管理器指令，它实际上将 service 和 chkconfig 这两个命令组合到一起，所以systemctl命令是service命令和chkconfig命令的集合和代替。可以使用它永久性或只在当前会话中启用/禁用服务。

>注意：在CentOS7.0后，不再使用service，而是systemctl 。centos7.0是向下兼容的，也是可以用service.

### 2. Linux查看系统进程
在linux中，统进程的命令为ps，常用格式为如下两个：
- ps aux        # unix格式查看系统进
- ps -le        # linux格式查看系统进程
一般地，ps aux更常用，下面主要讲解ps aux命令:
```
ps -aux
```
输出格式：
[](https://upload-images.jianshu.io/upload_images/3067896-b8227d91503aaae4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
输出内容字段：
- USER: 进程拥有者
- PID: pid
- %CPU: 占用的 CPU 使用率
- %MEM: 占用的记忆体使用率
- VSZ: 占用的虚拟记忆体大小（virtual）
- RSS: 占用的记忆体大小（true）
- TTY: 终端的次要装置号码 (minor device number of tty)
- STAT: 该行程的状态:
  1. D: 无法中断的休眠状态 (通常 IO 的进程)
  2. R: 正在执行中
  3. S: 静止状态
  4. T: 暂停执行
  5. Z: 不存在但暂时无法消除（僵尸状态）
  6. W: 没有足够的记忆体分页可分配
  7. <: 高优先序的行程
  8. N: 低优先序的行程
  9. L: 有记忆体分页分配并锁在记忆体内 (实时系统或捱A I/O)
- START: 行程开始时间
- TIME: 执行的时间
- COMMAND:所执行的指令

### 3.Linux查看系统运行状态
在linux中，用top命令来查看系统运行性能及状态。
- top                    # 实时显示进程状态
- top:top命令可以看到总体的系统运行状态和cpu的使用率 。
  1. PID：当前运行进程的ID
  2. USER：进程属主
  3. PR：每个进程的优先级别
  4. NInice：反应一个进程“优先级”状态的值，其取值范围是-20至19，一共40个级别。这个值越小，表示进程”优先级”越高，而值越大“优先级”越低。一般会把nice值叫做静态优先级
  5. VIRT：进程占用的虚拟内存
  6. RES：进程占用的物理内存
  7. SHR：进程使用的共享内存
  8. S：进程的状态。S表示休眠，R表示正在运行，Z表示僵死状态，N表示该进程优先值为负数
  9. %CPU：进程占用CPU的使用率
  10. %MEM：进程使用的物理内存和总内存的百分比
  11. TIME+：该进程启动后占用的总的CPU时间，即占用CPU使用时间的累加值。
  12. COMMAND：进程启动命令名称

**top命令常用快捷键**
- ctr+z 停止
- ctr+c 强制退出
- q 退出
- m 按内存排序查找
- p 按PID排序

### 4.Linux查看进程树
linux中查看进程树命令是pstree，要使用它，首先在linux上安装
```
yum install psmisc -y
```
1.查看默认进程树
```
pstree
```
2.带有PID的进程树
```
pstree -p
```
3.通过进程名查找
```
pstree -p | grep java
```

# 七.Linux的环境变量
|用户|环境变量配置文件|
|-|-|
|所有用户|/ect/profile /etc/bashrc /etc/environment|
|root|~/.bashrc ~/.bash-profile|
|非root用户|	/home/非root用户名/.bashrc|
### 1.Linux配置环境变量
按变量的生存周期来划分，Linux变量可分为两类： 
1 永久的：需要修改配置文件，变量永久生效。 
2 临时的：使用export命令声明即可，变量在关闭shell时失效。

**常见的设置变量的三种方法:**
1. 在/etc/profile文件中添加变量【对所有用户生效(永久的)】 
用VI在文件/etc/profile文件中增加变量，该变量将会对Linux下所有用户有效，并且是“永久的”。 
例如：编辑/etc/profile文件，添加CLASSPATH变量 
```
# vi /etc/profile 
export CLASSPATH=./JAVA_HOME/lib;$JAVA_HOME/jre/lib
```
注：修改文件后要想马上生效还要运行``# source /etc/profile``不然只能在下次重进此用户时生效。

2. 在用户目录下的.bash_profile文件中增加变量【对单一用户生效(永久的)】 
用VI在用户目录下的.bash_profile文件中增加变量，改变量仅会对当前用户有效，并且是“永久的”。 
```
例如：编辑guok用户目录(/home/guok)下的.bash_profile 
vi/home/guok/.bash.profile添加如下内容：exportCLASSPATH=./JAVAHOME/lib;JAVA_HOME/jre/lib 
```
注：修改文件后要想马上生效还要运行$ source /home/guok/.bash_profile不然只能在下次重进此用户时生效。

3. 直接运行export命令定义变量【只对当前shell(BASH)有效(临时的)】 
在shell的命令行下直接使用[export 变量名=变量值] 定义变量，

该变量只在当前的shell(BASH)或其子shell(BASH)下是有效的，
shell关闭了，变量也就失效了，再打开新shell时就没有这个变量，需要使用的话还需要重新定义。

**设置环境变量的所有方法:**
方式1：
```
export PATH=/usr/local/src/python3/bin:$PATH
# 或者把PATH放在前面
export PATH=$PATH:/usr/local/src/python3/bin

生效时间：立即生效
生效期限：当前打开的终端有效，窗口关闭后无效
生效范围：当前登录用户
需要加上$PATH，否则会覆盖原有路径
```
方式2:
```
vim ~/.bashrc
# 在最后一行添加环境变量
export PATH=$PATH:/usr/local/src/python3/bin

生效时间：使用相同的用户打开新的终端时生效，或者手动 source ~/.bashrc 生效
生效期限：永久有效
生效范围：当前登录用户
可能会被后续的环境变量文件覆盖了PATH的值
```
方式3：
```
vim ~/.bash_profile
#最后添加环境变量
export PATH=$PATH:/usr/local/src/python3/bin
生效时间：使用相同的用户打开新的终端时生效，或者手动 source ~/.bash_profile 生效
生效期限：永久有效
生效范围：当前登录用户
如果没有 ~/.bash_profile 文件，则可以编辑 ~/.profile 文件或者新建一个
```
方式4:
```
#如果/etc/bashrc文件不可编辑，需要修改为可编辑
chmod -v u+w /etc/bashrc
vim /etc/bashrc
#在最后一行加上
export PATH=$PATH:/usr/local/src/python3/bin

生效时间：使用相同的用户打开新的终端时生效，或者手动 source /etc/bashrc 生效
生效期限：永久有效
生效范围：所有用户
```
方式5:
```
# 如果/etc/profile文件不可编辑，需要修改为可编辑
chmod -v u+w /etc/profile
vim /etc/profile
# 在最后一行加上
export PATH=$PATH:/usr/local/src/python3/bin

生效时间：使用相同的用户打开新的终端时生效，或者手动 source /etc/profile 生效
生效期限：永久有效
生效范围：所有用户
```
方式6:
```
# 如果/etc/bashrc文件不可编辑，需要修改为可编辑
chmod -v u+w /etc/environment

vim /etc/profile

# 在最后一行加上
export PATH=$PATH:/usr/local/src/python3/bin
生效时间：使用相同的用户打开新的终端时生效，或者手动 source /etc/environment 生效
生效期限：永久有效
生效范围：所有用户
```

### 2.Linux环境变量加载顺序
- /etc/environment
- /etc/profile
- /etc/bashrc
- ~/.profile
- ~/.bashrc

### 3.Linux查看环境变量
1. 使用echo命令查看单个环境变量。例如： 
```
echo $PATH 
```
2. 使用env查看所有环境变量。例如： 
```
env 
```

### 4.Linux更新环境变量
```
source /etc/profile
or
. /etc/profile
```

### 5.使用unset删除指定的环境变量
set可以设置某个环境变量的值。清除环境变量的值用unset命令。如果未指定值，则该变量值将被设为NULL。示例如下： 
export TEST="Test..." #增加一个环境变量TEST env|grep TEST #此命令有输入，证明环境变量TEST已经存在了 
TEST=Test... 
unset  TEST #删除环境变量TEST 
$ env|grep TEST #此命令没有输出，证明环境变量TEST已经删除

# 八.vi/vim编辑器
### 1.vi/vim是什么
1. vi是Visual Interface的缩写，即 可视化接口。
2. vim是vi iMprove的缩写，即 vi的增强版（具有语法着色功能）。

### 2.vi/vim的三种模式
##### (1.)命令模式：
用户刚刚启动 vi/vim，便进入了命令模式。
命令模式是启动vi后进入的工作模式，并可转换为文本编辑模式和最后行模式。在命令模式下，从键盘上输入的任何字符都被当作编辑命令来解释，而不会在屏幕上显示。
如果输入的字符是合法的vi命令，则vi就会完成相应的动作;否则vi会响铃警告。
此状态下敲击键盘动作会被Vim识别为命令，而非输入字符。比如我们此时按下i，并不会输入一个字符，i被当作了一个命令。
以下是常用的几个命令：
- i 切换到输入模式，以输入字符。
- x 删除当前光标所在处的字符。
- : 切换到底线命令模式，以在最底一行输入命令。
若想要编辑文本：启动Vim，进入了命令模式，按下i，切换到输入模式。

命令模式只有一些最基本的命令，因此仍要依靠底线命令模式输入更多命令。
##### (2.)文本编辑模式
在命令模式下按下i就进入了输入模式。
文本编辑模式用于字符编辑。在命令模式下输入i（插入命令）、a（附加命令）等命令后进入文本编辑模式，此时输入的任何字符都被vi当作文件内容显示在屏幕上。按Esc键可从文本编辑模式返回到命令模式。
在输入模式中，可以使用以下按键：
- 字符按键以及Shift组合，输入字符
- ENTER，回车键，换行
- BACK SPACE，退格键，删除光标前一个字符
- DEL，删除键，删除光标后一个字符
- 方向键，在文本中移动光标
- HOME/END，移动光标到行首/行尾
- Page Up/Page Down，上/下翻页
- Insert，切换光标为输入/替换模式，光标将变成竖线/下划线
- ESC，退出输入模式，切换到命令模式
##### (3.)底线命令模式
在命令模式下按下:（英文冒号）就进入了底线命令模式。
在命令模式下，按“：”键进入最后行模式，此时vi会在屏幕的底部显示“：”符号年作为最后行模式的提示符，等待用户输入相关命令。命令执行完毕后，vi自动回到命令模式。
底线命令模式可以输入单个或多个字符的命令，可用的命令非常多。
在底线命令模式中，基本的命令有（已经省略了冒号）：
　末行模式下：
　　　w：保存
　　　q：退出
　　　wq 或 x：保存退出，wq 和 x 都是保存退出
　　　q！：强制退出
　　　w！：强制保存，管理员才有权限
　　命令模式下：
　　　ZZ：保存并退出

### 3.vi/vim三种模式的转换
命令模式→输入模式：
　　i：在当前光标所在字符的前面，转为输入模式
　　I：在当前光标所在行的行首转换为输入模式
　　a：在当前光标所在字符的后面，转为输入模式
　　A：在光标所在行的行尾，转换为输入模式
　　o：在当前光标所在行的下方，新建一行，并转为输入模式
　　O：在当前光标所在行的上方，新建一行，并转为输入模式
　　s：删除光标所在字符
　　r：替换光标处字符
输入模式→命令模式
　　ESC键
命令模式→末行模式
　　输入：即可 转为末行模式
[](https://upload-images.jianshu.io/upload_images/3067896-d0e247756e460410.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# 九.Linux远程连接服务SSH
### 1. 什么是ssh
SSH是专门为远程登录会话与其他网络服务提供的一种安全性协议。SSH是标准的网络协议，可用于大多数UNIX操作系统，能够实现字符界面的远程登录管理，它默认使用22号端口，采用密文的形式在网络中传输数据，相对于通过明文传输的Telnet，具有更高的安全性。SSH提供了口令和密钥两种用户验证方式，这两者都是通过密文传输数据的。

### 2.ssh服务认证类型
##### (1.)基于口令认证
基于口令的安全验证的方式就是大家现在一直在用的，只要知道服务器的SSH连接帐号和口令(当然也要知道对应服务器的 IP及开放的 SSH端口，默认为22 )，就可以通过 ssh客户端登录到这台远程主机。此时，联机过程中所有传输的数据都是加密的。
##### (2.)基于密钥认证
注意事项：不要使用 root 用户生成密钥对，这样只有 root 用户才可以使用。使用普通用户创建密钥对。如何在本地系统上创建一个 SSH 密钥对?只需要在客户端系统上运行下面的命令。
```
$ ssh-keygen
```

### 3.增强ssh服务的安全性
- 修改默认端口
- 禁止root登录
- 限制ssh监听的IP
- 禁止使用密码登录

### 4.SSh无法连接linux主机问题
1. 查询是否开启了ssh服务
```
peng@ubuntu:~$ ps -e |grep ssh
```
没有安装或者没有开启服务的话则查不出结果，如果开启则显示有sshd，如下：
```
peng@ubuntu:~$ ps -e |grep ssh
  6178 ?        00:00:00 sshd
  6332 ?        00:00:00 sshd
  6409 ?        00:00:00 sshd
```

2.安装ssh服务，输入命令：
```
peng@ubuntu:~$ sudo apt-get install openssh-server
```

3. 如果没有开启，执行/etc/init.d/ssh start 来启动ssh服务

4. 检查Ubuntu的防火墙状态
(1.)如果状态为active则防火墙为开启状态，inactive为关闭，如果防火墙开启则xshell也是不能连接上的
```
peng@ubuntu:~$ sudo ufw status
Status: active
```
(2.)若为开启状态，则关闭防火墙(开启防火墙为 sudo ufw enable)
```
peng@ubuntu:~$ sudo ufw disable
```

### 5.linux命令行清屏
```
clear
```
这个命令将会刷新屏幕，本质上只是让终端显示页向后翻了一页，如果向上滚动屏幕还可以看到之前的操作信息。一般都会用这个命令。
```
reset
```
这个命令将完全刷新终端屏幕，之前的终端输入操作信息将都会被清空，这样虽然比较清爽，但整个命令过程速度有点慢，使用较少。


参考资料:
[Linux内核版本和发行版本](https://blog.csdn.net/wonderful_life_mrchi/article/details/78352227)
[Linux分支图](https://upload-images.jianshu.io/upload_images/3067896-939781abc76132c5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
[【Linux】Linux版本介绍（内核版本和发行版本](https://blog.csdn.net/love_Aym/article/details/80726722)
[什么是挂载，Linux挂载详解](http://c.biancheng.net/view/2859.html)
[Linux学习教程，Linux入门教程（超详细）](http://c.biancheng.net/linux_tutorial/)
[比起 Windows，怎样解读 Linux 的文件系统与目录结构？](https://www.infoq.cn/article/how-to-read-linux-file-system-and-directory-structure)
[Linux系统的用户和用户组管理](https://www.cnblogs.com/zhongguiyao/p/9165917.html)
[Linux之shell编程](https://blog.csdn.net/happiness_llz/article/details/82809789)
[apt-get简介](https://www.cnblogs.com/downey-blog/p/10473893.html)
[ssh服务详解 ](https://blog.51cto.com/u_13438667/2117175))