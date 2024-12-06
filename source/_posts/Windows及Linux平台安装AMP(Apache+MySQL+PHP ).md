---
title: Windows及Linux平台安装AMP(Apache+MySQL+PHP )
date: 2016-12-31
categories: 
  - Windows系统
tags:
  - PHP
---

# 一. linux平台安装AMP
### 安装apache
#### 1. 查看是否安装了apache服务器(apache服务的软件包名称叫做httpd)。
```
1、可以通过 apachectl -v 或者httpd -v 查看apache是否安装，如果安装了的话会显示版本号；

2、如果通过rpm包安装的话可以用  rpm -q  httpd 查看，如果安装的的话会显示包的名称；
```
![image.png](/images/e35a00e423d1df755b743b645250b157.webp)
#### 2. 通过yum安装Apache服务程序。
```
yum install httpd -y
```
#### 3. 安装完成后，启用并启动Apache服务。
```
sudo systemctl enable httpd
sudo systemctl start httpd
```
#### 4. 检查Apache服务的状态和版本。
```
sudo systemctl status httpd
```
![image.png](/images/aabe2089e8923e139f84faf9e84492f9.webp)

#### 5. 查看Apache监听的端口。
```
netstat -an|grep :80
```
![image.png](/images/d8c85a0655bc6f8cce133d1e0ba6cdbe.webp)
可以看到，80端口处于监听状态，说明服务已经启动，为使客户端能访问Apache服务器的80端口，要打开防火墙的TCP80端口。
```
iptables -I INPUT -p tcp --dport 80 -j ACCEPT
```
#### 6. 查看服务器是否启动成功。
在地址栏里面输入地址如果看到是如下的就说明启动成功了.
![image.png](/images/aaf9587527038bde08f2777a3ef1085c.webp)
##### 将网站放到指定的文件夹(默认的是/var/www/html/)然后通过浏览器访问

#### 7. 到/etc/httpd/conf/httpd.conf修改下面两行参数

```
DocumentRoot "/var/www/html" //改为自己想要放的地方

<Directory "/var/www/html"> 同上

```

若在该目录下放一个html文件，在浏览器中输入

> [http://ip](https://link.jianshu.com?t=http://ip)地址(或者域名):80/文件名

### 安装PHP
#### 1. 安装php
```
yum -y install php
```
#### 2. 最后测试一下PHP是否成功安装.
在 /var/www/html 目录下创建文件 info.php ,编辑其内容为
```
<?php
    phpinfo();
?>
```
重启Apache服务器
```
 systemctl restart httpd
```
浏览器访问刚刚创建的页面，如下图则为正常安装成功
![image.png](/images/df55503914b6e3232395572b8d70ebed.webp)

### 安装mysql
#### 1. 安装mysql.
查看是否安装mysql
```
whereis mysql：如果安装了mysql就会显示mysql安装的地址
 mysql -V         :查看安装的mysql的版本
```
安装mysql
```
 wget http://dev.mysql.com/get/mysql-community-release-el7-5.noarch.rpm
 rpm -ivh mysql-community-release-el7-5.noarch.rpm
 yum install mysql-community-server
```
安装成功后重启mysql服务。
```
service mysqld restart
```
#### 2. 进入mysql.

##### 2.1 密码明文
语法：mysql -u用户名 -p用户密码
举例：
```
mysql -uroot -p123456
```
#####  2.2 密码密文
语法：mysql -u用户名 -p+回车，然后输入密码
举例：
```
mysql -uroot -p
```
![image](/images/5ec8822431fe3b4113fcb69f67871887.webp)
#### 3. 退出mysql.
![image.png](/images/5f7c5826eb4ddc6a4c8532338df681a6.webp)
#### 4. 使用命令show global variables like 'port';查看端口号 
![image.png](/images/ef92206b3484645b714b19090fdf6cfb.webp)
#### 5. 修改密码
　　语法：mysql> set password for 用户名@localhost = password('新密码');

　　举例：mysql>set password for root@localhost = password('123456');
#### 6. 常用操作（需登录）
- 显示数据库列表

　　show databases;
- 创建、删除数据库

　　create database 数据库名;

　　drop database 数据库名;

- 显示库中的数据表

　　use mysql;

　　show tables;

- 显示数据表结构

　　describe 数据表名;

#### 7. 远程连接数据库.
把在所有数据库的所有表的所有权限赋值给位于所有IP地址的root用户。
```
mysql> grant all privileges on *.* to root@'%'identified by 'password';
```
如果是新用户而不是root，则要先新建用户
```
mysql>create user 'username'@'%' identified by 'password';  
```
如果还是不行则:
**1.FirewallD防火墙开放3306端口**
```
firewall-cmd --zone=public --add-port=3306/tcp --permanent
```
命令含义：
```
--zone#作用域

--add-port=3306/tcp#添加端口，格式为：端口/通讯协议

--permanent#永久生效，没有此参数重启后失效
```
重启防火墙
```
systemctl restart firewalld.service
```

# 二. window平台安装AMP

### apache服务器.
#### 1. 下载安装文件.
https://www.apachelounge.com/download/
https://home.apache.org/~steffenal/VC15/binaries/httpd-2.4.37-win64-VC15.zip
![image.png](/images/ad7cb5139febca456551d0fbbda60be3.webp)
将下载下来的压缩包解压到要安装的位置，解压即安装；
![image.png](/images/b5a9fb971244597777ba7e83ac0e7bd2.webp)
#### 2. 配置 Apache HTTP Server
打开 Apache24\conf 目录下的 httpd.conf，修改配置信息:
将文件目录地址修改为你的安装位置:
```
ServerRoot "C:/Apache24"
```
**目录斜杠的符号应该是/**

修改端口号:
默认的是80端口，但是多数情况下，80端口被占用，所以需要修改80端口。如果确定80端口未被占用则可以不修改，建议还是修改一下:
![image.png](/images/4634c813815bcbca956cc50175e2a66b.webp)

#### 3. 启动Apache HTTP Server：
- 打开dos窗口的第一种方法：快捷键 win + R 或者 在开始菜单输入 cmd 
- 打开dos窗口的第二种方法：在文件夹所在的地址栏输入 cmd 回车；
- 打开dos窗口的第二种方法：在指定的文件下的下，按住shift按键不放单击鼠标的右键，选择 “在此处打开命令窗口”。

#### 4. 检测是否启动服务器.
然后打开浏览器在地址栏输入 [http://localhost:8081/](http://localhost:8081/) 就可以访问页面，页面如下：
![image.png](/images/a2d836c3f0de2cf3925270fdb283bcd6.webp)

### php的安装.
#### 1. 下载安装文件:
https://windows.php.net/download
![image.png](/images/c3011f923d6f7105ee5ac1df46f1bff2.webp)
下载完成之后将其解压到之前指定好的文件夹中.
#### 2. 配置php:
然后，将目录下的php.ini-development文件重命名为php.ini.
![image.png](/images/b8f3f955969e44880b5844f51d498b36.webp)
打开php.ini 进行如下修改:
```
;extension_dir="ext"
```
将其修改为：
```
#去掉前面的分号，并且将地址更改为自己的安装位置
extension_dir="E:/php-7.2.12-Win32-VC15-x64/ext"
```
```
;extension=php_mysqli.dll  
#将前面的;去掉，这样PHP便可以支持mysqli扩展
```
保存退出.

#### 3. 配置apache支持php
Apache安装好之后，先向httpd.conf文件中写入PHP支持模块。
打开httpd.conf文件.
```
DirectoryIndex index.html
```
将其修改为
```
修改首页面文件类型支持
DirectoryIndex index.html index.htm index.php
```
然后，在文件尾部添加下面的内容：
```
#让Apache支持PHP
LoadModule php7_module "D:/phpenvir/php7.1.1/php7apache2_4.dll" 
#告诉Apache php.ini的位置
PHPIniDir  "D:/phpenvir/php7.1.1"   
AddType application/x-httpd-php .php .html .htm
```
写好之后保存文件。
### mysql的安装.
#### 1.下载[官网地址](https://dev.mysql.com/downloads/mysql/)
![image.png](/images/9f25eed7aac10afd4c1747226300cd1c.webp)
#### 2.下载完成，将文件解压到你想要安装的盘里。
#### 3.配置
-     在mysql的文件夹下创建一个名为data的空文件夹。
-     创建一个my.ini的文件，放在bin目录里面。
```
[mysql]
# 设置mysql客户端默认字符集
default-character-set=utf8 
[mysqld]
#设置3306端口
port = 3306 
# 设置mysql的安装目录
basedir=E:/mysq
# 设置mysql数据库的数据的存放目录
datadir=E:/mysq/data
# 允许最大连接数
max_connections=200
# 服务端使用的字符集默认为8比特编码的latin1字符集
character-set-server=utf8
# 创建新表时将使用的默认存储引擎
default-storage-engine=INNODB
```
#### 4.启动mysql.
以管理员身份运行DOS窗口。进入到mysql的bin文件夹下：
接下来在dos窗口里面输入：
```
mysqld --initialize-insecure
```
再输入：
```
mysqld -install        （如果说已经存在，可以使用sc delete mysql  或者 mysql -remove 将其删除）

```
会显示Service successfully installed.
 最后输入：
```
net start mysql     #启动mysql服务
```
![image.png](/images/50b6fad237654af5007476911e724f18.webp)
默认没有密码，直接进入
```
mysql -uroot -p
```
设置过密码则输入密码进入：
```
mysqladmin -u root -p password
```
展示所有的数据:
```
show databases;
```
修改数据库密码:
```
ALTER USER "root"@"localhost" IDENTIFIED  BY "password";
```

\c 可以退出当前行命令，
\q或者exit退出mysql命令行
