---
title: 万字长文总结MySQL关系型数据库
date: 2020-01-12
categories: 
  - 数据库
  - Mysql
---

# 数据库介绍
### 什么是数据库？
数据库的英文单词：data base，简称DB。数据库本质就是一个文件系统，它可以按照特定的格式把数据存储起来，可以方便对存储的数据进行增删改查操作。

### 数据库的分类
目前数据库总共分为两个大类:
* 关系型数据库：是建立在关系模型基础上的数据库。（MySQL、Oracle、DB2、SQL Server等等）。
* 非关系型数据库（NO SQL）：通常指数据之间无关系的数据库。（monggodb、redis等等）。

### 数据库服务器、数据库和数据表的关系
数据库服务器是一台安装了一个数据库管理系统（比如： MySQL）的主机，通常会开放一个远程连接的端口(例如MySQL的3306端口)来对外提供数据服务，通过数据库管理系统(MySQL)可以创建并管理管理多个数据库，一般开发人员会针对每一个应用创建一个数据库。
在一个数据库中可以创建多张数据表，这些数据表是真正存储数据的载体。表的每一行称为一条记录（Record）。
![](/images/648fd939178dc2ad42adf0f9a476bcd8.webp)

### SQL语言简介
SQL(Structured Query Language)是结构化查询语言的缩写，用来访问和操作数据库系统。SQL语句既可以查询数据库中的数据，也可以添加、更新和删除数据库中的数据，还可以对数据库进行管理和维护操作。
虽然SQL已经被ANSI组织定义为标准，不幸地是，各个不同的数据库对标准的SQL支持不太一致。并且，大部分数据库都在标准的SQL上做了扩展。 也就是说，如果只使用标准SQL，理论上所有数据库都可以支持，但如果使用某个特定数据库的扩展SQL，换一个数据库就不能执行了。
SQL语言定义了这么几种基础操作数据库的能力：
- DDL：Data Definition Language :DDL允许用户定义数据，也就是创建表、删除表、修改表结构这些操作。通常，DDL由数据库管理员执行。
- DML：Data Manipulation Language:DML为用户提供添加、删除、更新数据的能力，这些是应用程序对数据库的日常操作。
- DQL：Data Query Language:DQL允许用户查询数据，这也是通常最频繁的数据库日常操作。

SQL语法有如下的特点:

1. 不区分大小写。
2. 关键字、字段名、表名需要用空格或逗号隔开。
3. 每一个SQL语句是用分号结尾。
4. 语句可以写一行也可以分开写多行。

>注意虽然SQL语言关键字不区分大小写，但是，针对不同的数据库，对于表名和列名，有的数据库区分大小写，有的数据库不区分大小写。同一个数据库，有的在Linux上区分大小写，有的在Windows上不区分大小写。

### 关系型数据库MySQL简介
MySQL是一款轻量级关系型数据库管理系统它免费、开源、适用于中大型网站，MySQL默认端口号：3306。由瑞典MySQL AB公司开发，后来被Sun公司收购，Sun公司后来⼜被Oracle公司收购，⽬前属于Orac旗下。使⽤C和C++编写，并使⽤了多种编译器进⾏测试，保证源代码的可移植性。
MySQL⽀持多种操作系统和为多种编程语⾔提供了API。

# 安装及配置MySQL数据库
### docker安装MySQL8
##### 搜索MySQL镜像
```
docker search mysql
```

##### 拉取MySQL镜像

```
docker pull mysql:8
```

##### 创建并运行MySQL容器
```
docker run -p 3306:3306 --name mysqltest -e MYSQL_ROOT_PASSWORD=root -d mysql:8
```
参数说明：
* - p 3306:3306 : 将容器的 3306 端口映射到主机的 3306 端口
* - e MYSQL_ROOT_PASSWORD=root : 设置 mysql 登录密码
* - d 后台运行容器，并返回容器 id
* mysql:8 运行的镜像名，也可替换成镜像 id

##### 容器文件映射到本地目录（挂载）
在宿主机创建放置MySQL的配置文件的目录和数据目录可以防止容器被销毁导致数据被销毁问题。
1. 宿主机创建数据目录和配置文件:
```
sudo mkdir -p /usr/mysql/conf /usr/mysql/data /var/log/mysql
sudo chmod -R 777 /usr/mysql/ /var/log/mysql
```
2. 将测试容器里 MySQL 的配置文件复制到该路径。日后需改配置，直接在挂载路径的配置文件上修改即可

```
docker cp mysqltest:/etc/mysql/my.cnf /usr/mysql/conf
```

3. 删除测试容器，
```
docker stop mysqltest
docker rm mysqltest
```
4.创建新的 docker 容器并启动
```
sudo docker run -itd --name=mysql -p 3306:3306 --restart=always -e MYSQL_ROOT_PASSWORD=123456 -v /usr/mysql/conf/my.cnf:/etc/mysql/my.cnf -v /usr/mysql/data:/usr/mysql/data -v /var/log/mysql:/var/log/mysql  mysql:8
```

参数解释： 
* -v : 挂载宿主机目录和 docker容器中的目录，前面是宿主机目录，后面是容器内部目录 
* -d : 后台运行容器 
* -p 3306:3306 : 将容器的 3306 端口映射到主机的 3306 端口
* -e MYSQL_ROOT_PASSWORD=root :环境参数，MYSQL_ROOT_PASSWORD设置root用户的密码
* mysql:8 运行的镜像名，也可替换成镜像 id
* --restart=always:容器自动启动

### 查看MySQL版本

##### 方法1：
进入MySQL容器中使用命令：
```
mysql -V
mysql  Ver 8.0.29 for Linux on x86_64 (MySQL Community Server - GPL)
```

##### 方法2：
如果已经登录了MySQL ，则可以登陆MySQL之后使用内置命令

```
mysql> select version();
+-----------+
| version() |
+-----------+
| 8.0.29    |
+-----------+
1 row in set (0.00 sec)
```

##### 方法3：

同样登录MySQL，使用内置命令

```
mysql> status;
--------------
mysql  Ver 8.0.29 for Linux on x86_64 (MySQL Community Server - GPL)
...

```

或者

```
mysql> \s
--------------
mysql  Ver 8.0.29 for Linux on x86_64 (MySQL Community Server - GPL)
...

```

### 解决远程无法连接MySQL问题

##### 配置MySQL8支持远程连接
1. 进入容器内部

```
docker exec -it mysql /bin/bash
```

2. 连接MySQL

```
mysql -uroot -p123456
```

3. 使用MySQL库

```
use mysql;
```

4. 修改访问主机以及密码等，设置为所有主机可访问

```
ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY '123456';
```
>这里的密码为设置远程连接时的登录密码。

5. 刷新

```
flush privileges;
```

使用Navicat等远程数据库连接工具连接数据库时就可以正常连接了。

#### 检查防火墙是否允许访问该端口
如果MySQL设置了允许远程进行访问，但还是无法通过远程进行连接，那么就要检查主机的防火墙是否是将MySQL监听的端口是否关闭了。
1.. 查看防火墙状态:
```
sudo ufw status
```
2. 开放防火墙3306端口:
```
sudo ufw allow 3306
```

## MySql相关配置
### 查看安装文件路径

```
which mysql
```

### 查找配置文件my.cnf的位置

如果MySQL已经启动了，通过查看MySQL的线程，查看是否有明确指定加载my.cnf文件的路径。

```
ps -aux | grep mysql | grep 'my.cnf'
```

如果查询不到，则MySQL启动时会读取安装目录根目录以及默认目录下的my.cnf文件。首先确认服务器是否有my.cnf文件。

```
locate my.cnf
```

确认有my.cnf文件之后，查看MySQL启动时读取配置文件的默认目录。

```
mysql --help|grep 'my.cnf'
```

### my.cnf配置文件详解
```
[mysqld]
# mysql监听端口，默认3306
port = 3306 
# pid文件所在目录
pid-file = 

# 使用该目录作为根目录（安装目录）
basedir = 

# 数据文件存放的目录
datadir = 

# MySQL存放临时文件的目录
tmpdir = 

#*** skip options 相关选项 ***#
skip-name-resolve 
#禁止 MySQL 对外部连接进行 DNS 解析，使用这一选项可以消除 MySQL 进行 DNS 解析的时间。但需要注意，如果开启该选项，则所有远程主机连接授权都要使用 IP 地址方式，否则 MySQL 将无法正常处理连接请求！

skip-symbolic-links 
#不能使用连接文件，多个客户可能会访问同一个数据库，因此这防止外部客户锁定 MySQL 服务器。 该选项默认开启

skip-external-locking 
#不使用系统锁定，要使用 myisamchk,必须关闭服务器 ,避免 MySQL的外部锁定，减少出错几率增强稳定性。

skip-slave-start 
#启动 mysql,不启动复制

skip-networking 
#开启该选项可以彻底关闭 MySQL 的 TCP/IP 连接方式，如果 WEB 服务器是以远程连接的方式访问 MySQL 数据库服务器则不要开启该选项！否则将无法正常连接！ 如果所有的进程都是在同一台服务器连接到本地的 mysqld, 这样设置将是增强安全的方法

sysdate-is-now = 1 
#把SYSDATE 函数编程为 NOW的别名

#*** 系统资源相关选项 ***#
back_log = 50 
#接受队列，对于没建立 tcp 连接的请求队列放入缓存中，队列大小为 back_log，受限制与 OS 参数，试图设定 back_log 高于你的操作系统的限制将是无效的。默认值为 50。对于 Linux 系统推荐设置为小于512的整数。如果系统在一个短时间内有很多连接，则需要增大该参数的值

max_connections = 1000 
#指定MySQL允许的最大连接进程数。如果在访问数据库时经常出现"Too Many Connections"的错误提 示，则需要增大该参数值。

max_connect_errors = 10000 
#如果某个用户发起的连接 error 超过该数值，则该用户的下次连接将被阻塞，直到管理员执行 flush hosts ; 命令或者服务重启， 防止黑客 ， 非法的密码以及其他在链接时的错误会增加此值

open_files_limit = 10240 
#MySQL打开的文件描述符限制，默认最小1024;当open_files_limit没有被配置的时候，比较max_connections*5和ulimit-n的值，哪个大用哪个，当open_file_limit被配置的时候，比较open_files_limit和max_connections*5的值，哪个大用哪个。

connect-timeout = 10 
#连接超时之前的最大秒数,在 Linux 平台上，该超时也用作等待服务器首次回应的时间

wait-timeout = 28800 
#等待关闭连接的时间

interactive-timeout = 28800 
#关闭连接之前，允许 interactive_timeout（取代了wait_timeout）秒的不活动时间。客户端的会话 wait_timeout 变量被设为会话interactive_timeout 变量的值。如果前端程序采用短连接，建议缩短这2个值, 如果前端程序采用长连接，可直接注释掉这两个选项，默认配置(8小时)  

slave-net-timeout = 600 
#从服务器也能够处理网络连接中断。但是，只有从服务器超过slave_net_timeout 秒没有从主服务器收到数据才通知网络中断

net_read_timeout = 30 
#从服务器读取信息的超时

net_write_timeout = 60 
#从服务器写入信息的超时

net_retry_count = 10 
#如果某个通信端口的读操作中断了，在放弃前重试多次

net_buffer_length = 16384 
#包消息缓冲区初始化为 net_buffer_length 字节，但需要时可以增长到 max_allowed_packet 字节

max_allowed_packet = 64M
# 服务所能处理的请求包的最大大小以及服务所能处理的最大的请求大小(当与大的BLOB 字段一起工作时相当必要)， 每个连接独立的大小.大小动态增加。 设置最大包,限制server接受的数据包大小，避免超长SQL的执行有问题 默认值为16M，当MySQL客户端或mysqld
服务器收到大于 max_allowed_packet 字节的信息包时，将发出“信息包过大”错误，并关闭连接。对于某些客户端，如果通信信息包过大，在执行查询期间，可能会遇到“丢失与 MySQL 服务器的连接”错误。默认值 16M。

table_cache = 512 
# 所有线程所打开表的数量. 增加此值就增加了mysqld所需要的文件描述符的数量这样你需要确认在[mysqld_safe]中 “open-files-limit” 变量设置打开文件数量允许至少4096

thread_stack = 192K 
# 线程使用的堆大小. 此容量的内存在每次连接时被预留.MySQL 本身常不会需要超过 64K 的内存如果你使用你自己的需要大量堆的 UDF 函数或者你的操作系统对于某些操作需要更多的堆,你也许需要将其设置的更高一点.默认设置足以满足大多数应用

thread_cache_size = 20 
# 我们在 cache 中保留多少线程用于重用.当一个客户端断开连接后,如果 cache 中的线程还少于 thread_cache_size,则客户端线程被放入 cache 中.这可以在你需要大量新连接的时候极大的减少线程创建的开销(一般来说如果你有好的线程模型的话,
这不会有明显的性能提升.)服务器线程缓存这个值表示可以重新利用保存在缓存中线程的数量,当断开连接时如果缓存中还有空间,那么客户端的线程将被放到缓存中,如果线程重新被请求，那么请求将从缓存中读取,如果缓存中是空的或者是新的请求，那么这个线程将被重新创建,
如果有很多新的线程，增加这个值可以改善系统性能.通过比较 Connections 和 Threads_created 状态的变量，可以看到这个变量的作用
根据物理内存设置规则如下：
1G  —> 8
2G  —> 16
3G  —> 32
大于3G  —> 64

thread_concurrency = 8 
#此允许应用程序给予线程系统一个提示在同一时间给予渴望被运行的线程的数量.该参数取值为服务器逻辑CPU数量×2，在本例中，服务器有 2 颗物理CPU，而每颗物理CPU又支持H.T超线程，所以实际取值为 4 × 2 ＝ 8.设置 thread_concurrency的值的正确与否, 
对 mysql 的性能影响很大, 在多个 cpu(或多核)的情况下，错误设置了 thread_concurrency 的值, 会导致 mysql 不能充分利用多 cpu(或多核),出现同一时刻只能一个 cpu(或核)在工作的情况。 thread_concurrency 应设为 CPU 核数的 2 倍.比如有一个双核的 CPU, 
那么 thread_concurrency 的应该为 4; 2 个双核的 cpu,thread_concurrency 的值应为 8,属重点优化参数

#*** qcache settings 相关选项 ***#
query_cache_limit = 2M 
#不缓存查询大于该值的结果.只有小于此设定值的结果才会被缓冲,  此设置用来保护查询缓冲,防止一个极大的结果集将其他所有的查询结果都覆盖.

query_cache_min_res_unit = 2K 
#查询缓存分配的最小块大小.默认是 4KB，设置值大对大数据查询有好处，但如果你的查询都是小数据查询，就容易造成内存碎片和浪费
查询缓存碎片率 = Qcache_free_blocks / Qcache_total_blocks * 100%
如果查询缓存碎片率超过 20%，可以用 FLUSH QUERY CACHE 整理缓存碎片，或者试试减小query_cache_min_res_unit，如果你的查询都是小数据量的话。
查询缓存利用率 = (query_cache_size – Qcache_free_memory) / query_cache_size *100%
查询缓存利用率在 25%以下的话说明 query_cache_size 设置的过大，可适当减小;查询缓存利用率在 80%以上而且 Qcache_lowmem_prunes > 50 的话说明 query_cache_size 可能有点小，要不就是碎片太多。
查询缓存命中率 = (Qcache_hits – Qcache_inserts) / Qcache_hits * 100%

query_cache_size = 64M  
#指定 MySQL 查询缓冲区的大小。可以通过在 MySQL 控制台执行以下命令观察：
代码:
> SHOW VARIABLES LIKE '%query_cache%';
> SHOW STATUS LIKE 'Qcache%';如果 Qcache_lowmem_prunes 的值非常大，则表明经常出现缓冲不够的情况；
如果 Qcache_hits 的值非常大，则表明查询缓冲使用非常频繁，如果该值较小反而会影响效率，那么可以考虑不用查询缓冲； Qcache_free_blocks，如果该值非常大，则表明缓冲区中碎片很多。
memlock # 如果你的系统支持 memlock() 函数,你也许希望打开此选项用以让运行中的 mysql 在在内存高度
紧张的时候,数据在内存中保持锁定并且防止可能被 swapping out,此选项对于性能有益

#*** default settings 相关选项 ***#
default_table_type = InnoDB 
# 当创建新表时作为默认使用的表类型,如果在创建表示没有特别执行表类型,将会使用此值

default-time-zone = system 
#服务器时区

character-set-server = utf8 
#server 级别字符集

default-storage-engine = InnoDB 
#默认存储引擎


#*** tmp && heap settings 相关选项 ***#
tmp_table_size = 512M 
#临时表的最大大小，如果超过该值，则结果放到磁盘中,此限制是针对单个表的,而不是总和.

max_heap_table_size = 512M 
#独立的内存表所允许的最大容量.此选项为了防止意外创建一个超大的内存表导致永尽所有的内存资源.

#*** log settings 相关选项 ***#
log-bin = mysql-bin 
#打开二进制日志功能.在复制(replication)配置中,作为 MASTER 主服务器必须打开此项.如果你需要从你最后的备份中做基于时间点的恢复,你也同样需要二进制日志.这些路径相对于 datadir

log_slave_updates = 1 
#表示slave将复制事件写进自己的二进制日志

log-bin-index = mysql-bin.index 
#二进制的索引文件名

relay-log = relay-log 
#定义relay_log的位置和名称，如果值为空，则默认位置在数据文件的目录，文件名为host_name-relay-bin.nnnnnn（By default, relay log file names have the form host_name-relay-bin.nnnnnn in the data directory）；

relay_log_index = relay-log.index  
#relay-log的索引文件名

log-warnings = 1 
# 将警告打印输出到错误 log 文件.如果你对于MySQL有任何问题，你应该打开警告 log 并且仔细审查错误日志,查出可能的原因.

log-error =  /usr/local/mysql/log/mysql.err 
#错误日志路径

log_output = FILE 
#参数 log_output 指定了慢查询输出的格式，默认为 FILE，你可以将它设为 TABLE，然后就可以查询 mysql 架构下的 slow_log 表了

log_slow_queries 
#指定是否开启慢查询日志(该参数要被slow_query_log取代，做兼容性保留)

slow_query_log = 1 
# 指定是否开启慢查询日志. 慢查询是指消耗了比 “long_query_time” 定义的更多时间的查询.如果 log_long_format 被打开,那些没有使用索引的查询也会被记录.如果你经常增加新查询到已有的系统内的话. 一般来说这是一个好主意,

long-query-time = 1 
#设定慢查询的阀值，超出次设定值的SQL即被记录到慢查询日志，缺省值为10s.所有的使用了比这个时间(以秒为单位)更多的查询会被认为是慢速查询.不要在这里使用”1″, 否则会导致所有的查询,甚至非常快的查询页被记录下来(由于MySQL 目前时间的精确度只能达到秒的级别).

log_long_format 
# 在慢速日志中记录更多的信息.一般此项最好打开，打开此项会记录使得那些没有使用索引的查询也被作为到慢速查询附加到慢速日志里

slow_query_log_file =  /usr/local/mysql/log/slow.log 
# 指定慢日志文件存放位置，可以为空，系统会给一个缺省的文件host_name-slow.log

log-queries-not-using-indexes 
#如果运行的SQL语句没有使用索引，则mysql数据库同样会将这条SQL语句记录到慢查询日志文件中。

min_examined_row_limit=1000　　　　
#记录那些由于查找了多余1000次而引发的慢查询

long-slow-admin-statements　　　　
#记录那些慢的optimize table，analyze table和alter table语句

log-slow-slave-statements 
#记录由Slave所产生的慢查询

general_log = 1 
#将所有到达MySQL Server的SQL语句记录下来,默认关闭 

general_log_file =  /usr/local/mysql/log/mysql.log 
#general_log路径

max_binlog_size = 1G 
#如果二进制日志写入的内容超出给定值，日志就会发生滚动。你不能将该变量设置为大于1GB或小于4096字节。 默认值是1GB。如果你正使用大的事务，二进制日志还会超过max_binlog_size

max_relay_log_size = 1G 
#标记relaylog允许的最大值，如果该值为0，则默认值为max_binlog_size(1G)；如果不为0，则max_relay_log_size则为最大的relay_log文件大小；

relay-log-purge = 1 
#是否自动清空不再需要中继日志时。默认值为1(启用)

expire_logs_days = 30 
#超过 30 天的 binlog 删除

binlog_cache_size = 1M 
# 在一个事务中 binlog 为了记录 SQL 状态所持有的 cache 大小,如果你经常使用大的,多声明的事务,你可以增加此值来获取更大的性能.所有从事务来的状态都将被缓冲在 binlog 缓冲中然后在提交后一次性写入到 binlog 中,如果事务比此值大, 会使用磁盘上的临时文件来替代.此缓冲在每个连接的事务第一次更新状态时被创建.session 级别

replicate-wild-ignore-table = mysql.% 
#复制时忽略数据库及表
slave_skip_errors=all 
#定义复制过程中从服务器可以自动跳过的错误号，当复制过程中遇到定义的错误号，就可以自动跳过，直接执行后面的SQL语句。
slave_skip_errors选项有四个可用值，分别为：off，all，ErorCode，ddl_exist_errors。
  默认情况下该参数值是off，我们可以列出具体的error code，也可以选择all，mysql5.6及MySQL Cluster NDB 7.3以及后续版本增加了参数ddl_exist_errors，该参数包含一系列error code（1007,1008,1050,1051,1054,1060,1061,1068,1094,1146）
    一些error code代表的错误如下：
    1007：数据库已存在，创建数据库失败
    1008：数据库不存在，删除数据库失败
    1050：数据表已存在，创建数据表失败
    1051：数据表不存在，删除数据表失败
    1054：字段不存在，或程序文件跟数据库有冲突
    1060：字段重复，导致无法插入
    1061：重复键名
    1068：定义了多个主键
    1094：位置线程ID
    1146：数据表缺失，请恢复数据库
    1053：复制过程中主服务器宕机
    1062：主键冲突 Duplicate entry '%s' for key %d


#*** MyISAM 相关选项 ***#
key_buffer_size = 256M 
#指定用于索引的缓冲区大小，增加它可得到更好的索引处理性能。如果是以InnoDB引擎为主的DB，专用于MyISAM引擎的 key_buffer_size 可以设置较小，8MB 已足够  如果是以MyISAM引擎为主，可设置较大，但不能超过4G. 在这里，强烈建议不使用MyISAM引擎，默认都是用InnoDB引擎.注意：该参数值设置的过大反而会是服务器整体效率降低！

sort_buffer_size = 2M 
#查询排序时所能使用的缓冲区大小。排序缓冲被用来处理类似 ORDER BY 以及 GROUP BY 队列所引起的排序.一个用来替代的基于磁盘的合并分类会被使用.查看 “Sort_merge_passes” 状态变量. 在排序发生时由每个线程分配 注意：该参数对应的分配内存是每连接独占！如果有 100 个连接，那么实际分配的总共排序缓冲区大小为 100 × 6 ＝600MB,所以,对于内存在 4GB 左右的服务器推荐设置为 6-8M。 

read_buffer_size = 2M 
#读查询操作所能使用的缓冲区大小。和 sort_buffer_size 一样，该参数对应的分配内存也是每连接独享！用来做 MyISAM 表全表扫描的缓冲大小.当全表扫描需要时,在对应线程中分配.

join_buffer_size = 8M 
#联合查询操作所能使用的缓冲区大小，和 sort_buffer_size 一样，该参数对应的分配内存也是每连接独享!此缓冲被使用来优化全联合(full JOINs 不带索引的联合).类似的联合在极大多数情况下有非常糟糕的性能表现, 但是将此值设大能够减轻性能影响.通过 “Select_full_join”状态变量查看全联合的数量， 当全联合发生时,在每个线程中分配。

read_rnd_buffer_size = 8M 
#MyISAM 以索引扫描(Random Scan)方式扫描数据的 buffer大小 

bulk_insert_buffer_size = 64M 
#MyISAM 使用特殊的类似树的 cache 来使得突发插入(这些插入是,INSERT … SELECT, INSERT … VALUES (…), (…), …, 以及 LOAD DATAINFILE) 更快. 此变量限制每个进程中缓冲树的字节数.设置为 0 会关闭此优化.为了最优化不要将此值设置大于 “key_buffer_size”.当突发插入被检测到时此缓冲将被分配MyISAM 用在块插入优化中的树缓冲区的大小。注释：这是一个 per thread 的限制 （ bulk 大量）.此缓冲当 MySQL 需要在 REPAIR, OPTIMIZE, ALTER 以及 LOAD DATA INFILE到一个空表中引起重建索引时被分配.这在每个线程中被分配.所以在设置大值时需要小心.

myisam_sort_buffer_size = 64M 
#MyISAM 设置恢复表之时使用的缓冲区的尺寸,当在REPAIR TABLE 或用 CREATE INDEX 创建索引或 ALTER TABLE 过程中排序 MyISAM 索引分配的缓冲区

myisam_max_sort_file_size = 10G
#mysql重建索引时允许使用的临时文件最大大小

myisam_repair_threads = 1 
#如果该值大于 1，在 Repair by sorting 过程中并行创建MyISAM 表索引(每个索引在自己的线程内).如果一个表拥有超过一个索引, MyISAM 可以通过并行排序使用超过一个线程去修复他们.这对于拥有多个 CPU 以及大量内存情况的用户,是一个很好的选择.

myisam_recover = 64K
#允许的 GROUP_CONCAT()函数结果的最大长度
transaction_isolation = REPEATABLE-READ # 设定默认的事务隔离级别.可用的级别如下:READ-UNCOMMITTED, READ-COMMITTED, REPEATABLE-READ,SERIALIZABLE
1.READ UNCOMMITTED-读未提交 2.READ COMMITTE-读已提交 3.REPEATABLE READ -可重复读 4.SERIALIZABLE -串行


# *** INNODB 相关选项 ***#
skip-innodb 
# 如果你的 MySQL 服务包含 InnoDB 支持但是并不打算使用的话,使用此选项会节省内存以及磁盘空间,并且加速某些部分

innodb_file_per_table = 1 
# InnoDB为独立表空间模式，每个数据库的每个表都会生成一个数据空间
独立表空间优点：
1．每个表都有自已独立的表空间。
2．每个表的数据和索引都会存在自已的表空间中。
3．可以实现单表在不同的数据库中移动。
4．空间可以回收（除drop table操作处，表空不能自已回收）
缺点：
1.单表增加过大，如超过100G
结论：
共享表空间在Insert操作上少有优势。其它都没独立表空间表现好。当启用独立表空间时，请合理调整：innodb_open_files

innodb_status_file = 1 
#启用InnoDB的status file，便于管理员查看以及监控等

innodb_open_files = 2048 
# 限制Innodb能打开的表的数据，如果库里的表特别多的情况，请增加这个。这个值默认是300

innodb_additional_mem_pool_size = 100M 
#设置InnoDB存储引擎用来存放数据字典信息以及一些内部数据结构的内存空间大小，所以当我们一个MySQL Instance中的数据库对象非常多的时候，是需要适当调整该参数的大小以确保所有数据都能存放在内存中提高访问效率的。 

innodb_buffer_pool_size = 2G 
#包括数据页、索引页、插入缓存、锁信息、自适应哈希所以、数据字典信息.InnoDB 使用一个缓冲池来保存索引和原始数据, 不像 MyISAM.这里你设置越大,你在存取表里面数据时所需要的磁盘 I/O 越少.在一个独立使用的数据库服务器上,你可以设置这个变量到服务器物理内存大小的 80%,不要设置过大,否则,由于物理内存的竞争可能导致操作系统的换页颠簸.注意在 32 位系统上你每个进程可能被限制在 2-3.5G 用户层面内存限制,所以不要设置的太高.

innodb_write_io_threads = 4
innodb_read_io_threads = 4
# innodb使用后台线程处理数据页上的读写 I/O(输入输出)请求,根据你的 CPU 核数来更改,默认是4
# 注:这两个参数不支持动态改变,需要把该参数加入到my.cnf里，修改完后重启MySQL服务,允许值的范围从 1-64

innodb_data_home_dir =  /usr/local/mysql/var/ 
#设置此选项如果你希望 InnoDB 表空间文件被保存在其他分区.默认保存在 MySQL 的 datadir 中.

innodb_data_file_path = ibdata1:500M;ibdata2:2210M:autoextend
#InnoDB将数据保存在一个或者多个数据文件中成为表空间.如果你只有单个逻辑驱动保存你的数据,一个单个的自增文件就足够好了.其他情况下.每个设备一个文件一般都是个好的选择.你也可以配置 InnoDB 来使用裸盘分区 – 请参考手册来获取更多相关内容

innodb_file_io_threads = 4 
#用来同步 IO 操作的 IO 线程的数量. 此值在 Unix 下被硬编码为 4,但是在 Windows 磁盘 I/O 可能在一个大数值下表现的更好.

innodb_thread_concurrency = 16
#在 InnoDb 核心内的允许线程数量,InnoDB 试着在 InnoDB 内保持操作系统线程的数量少于或等于这个参数给出的限制,最优值依赖于应用程序,硬件以及操作系统的调度方式.过高的值可能导致线程的互斥颠簸.默认设置为 0,表示不限制并发数，这里推荐设置为0，更好去发挥CPU多核处理能力，提高并发量

innodb_flush_log_at_trx_commit = 1 
#如果设置为 1 ,InnoDB 会在每次提交后刷新(fsync)事务日志到磁盘上,这提供了完整的 ACID 行为.如果你愿意对事务安全折衷, 并且你正在运行一个小的食物, 你可以设置此值到 0 或者 2 来减少由事务日志引起的磁盘 I/O
0 代表日志只大约每秒写入日志文件并且日志文件刷新到磁盘.
2 代表日志写入日志文件在每次提交后,但是日志文件只有大约每秒才会刷新到磁盘上.

innodb_log_buffer_size = 8M 
#用来缓冲日志数据的缓冲区的大小.当此值快满时, InnoDB 将必须刷新数据到磁盘上.由于基本上每秒都会刷新一次,所以没有必要将此值设置的太大(甚至对于长事务而言)

innodb_log_file_size = 500M 
#事物日志大小.在日志组中每个日志文件的大小，你应该设置日志文件总合大小到你缓冲池大小的5%~100%，来避免在日志文件覆写上不必要的缓冲池刷新行为.不论如何, 请注意一个大的日志文件大小会增加恢复进程所需要的时间.

innodb_log_files_in_group = 2 
#在日志组中的文件总数.通常来说 2~3 是比较好的.

innodb_log_group_home_dir =  /usr/local/mysql/var/
# InnoDB 的日志文件所在位置. 默认是 MySQL 的 datadir.你可以将其指定到一个独立的硬盘上或者一个 RAID1 卷上来提高其性能innodb_max_dirty_pages_pct = 90 #innodb 主线程刷新缓存池中的数据，使脏数据比例小于 90%,这是一个软限制,不被保证绝对执行.

innodb_lock_wait_timeout = 50 
#InnoDB 事务在被回滚之前可以等待一个锁定的超时秒数。InnoDB 在它自己的 锁定表中自动检测事务死锁并且回滚事务。 InnoDB 用 LOCK TABLES 语句注意到锁定设置。默认值是 50 秒

innodb_flush_method = O_DSYNC 
# InnoDB 用来刷新日志的方法.表空间总是使用双重写入刷新方法.默认值是 “fdatasync”, 另一个是 “O_DSYNC”.

innodb_force_recovery=1
# 如果你发现 InnoDB 表空间损坏, 设置此值为一个非零值可能帮助你导出你的表.从1 开始并且增加此值知道你能够成功的导出表.

innodb_fast_shutdown 
# 加速 InnoDB 的关闭. 这会阻止 InnoDB 在关闭时做全清除以及插入缓冲合并.这可能极大增加关机时间, 但是取而代之的是 InnoDB 可能在下次启动时做这些操作.


# *** 其他 相关选项 ***#
[mysqldump]
quick 
#支持较大数据库的转储，在导出非常巨大的表时需要此项。增加该变量的值十分安全，这是因为仅当需要时才会分配额外内存。例如，仅当你发出长查询或mysqld必须返回大的结果行时mysqld才会分配更多内存。该变量之所以取较小默认值是一种预防措施，以捕获客户端和服务器之间的错误信息包，并确保不会因偶然使用大的信息包而导致内存溢出。 如果你正是用大的BLOB值，而且未为mysqld授予为处理查询而访问足够内存的权限，也会遇到与大信息包有关的奇怪问题。如果怀疑出现了该情况，请尝试在mysqld_safe脚本开始增加ulimit -d 256000，并重启mysqld。

[mysql]
auto-rehash 
#允许通过 TAB 键提示

default-character-set = utf8 
#数据库字符集

connect-timeout = 3
[mysqld_safe]

open-files-limit = 8192 
#增加每个进程的可打开文件数量.确认你已经将全系统限制设定的足够高!打开大量表需要将此值设大
```

## MySQL用户及权限管理
### 添加用户
在MySQL中添加用户使用CREATE USER 和 GRANT就可以了。 例如创建一个普通用户-zhangsan. 然后赋予它一下简单的权限:

```
CREATE USER 'zhangsan'@'localhost' IDENTIFIED BY 'your_password';
// 创建一个zhangsan的用户, 并且, 他的密码为,your_password
> GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,DROP 
   -> ON *.*
   -> TO 'zhangsan'@'localhost';

// 赋予zhangsan 一些基本的权限, 让他去访问某些执行的数据库, 上文中的`*.*`(这表示所有的数据库) 就可以写为你允许该用户访问的数据库的name, 比如, 你可以改为`bank`,`tencent`... 等等
```

这样， 你就可以使用MySQL -u xxx -p 进行指定用户的登录了. 如果，你想创建一个管理员账户的话， 代码就更简单了。

```
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'your_ps';
// 创建一个管理员账户

GRANT ALL PRIVILEGES ON *.* TO 'admin'@'localhost' WITH GRANT OPTION;
// ok
```

如果你想检查， 你创建的用户的权限对不对时， 可以使用:

```
SHOW GRANTS FOR 'admin'@'localhost';
```

### 修改用户密码
有很多种方法， 简单介绍两种. 一种是使用SET，一种是使用ALERT(v5.7.6).

SET 修改密码应该算是比较常用的，使用SET直接修改密码即可，格式为:

```
SET PASSWORD FOR 'zhangsan'@'localhost' = PASSWORD('your_ps');
```

上面那种方法，适用于root的用户进行修改， 如果你想修改自己的密码的话，直接使用:

```
SET PASSWORD = PASSWORD('your_ps');
```

使用ALERT的相关语法也可以修改密码:

```
ALERT USER 'zhangsan'@'localhost' IDENTIFIED BY 'your_ps';
```

如果你不想输，'zhangsan'@'localhost 这一串的话， 可以直接使用USER()进行代替:

```
ALERT USER USER() IDENTIFIED BY 'your_ps';
```

另外， 如果你只想在shell 中直接修改的话，可以直接使用:

```
mysqladmin -u user_name -h host_name password "new_password"
```

### 删除用户

在mysql.user中查看用户信息:

```
`SELECT User FROM mysql.user
```

选择你想要删除的用户名，直接drop就行了:

```
DROP USER 'zhangsan'@'localhost';
```

### 用户相关命令
-- 创建用户
    ```
    CREATE USER zhangsan IDENTIFIED BY '123456'
    ```
-- 删除用户
    ```
    DROP USER zhangsan
    ```
-- 修改当前用户密码
    ```
    SET PASSWORD = PASSWORD('666888')
    ```
-- 修改指定用户密码
    ```
    SET PASSWORD FOR zhangsan = PASSWORD('666888')
    ```
-- 重命名用户
    ```
    RENAME USER zhangsan to wangwu
    ```
-- 用户授权(授予全部权限，除了给其他用户授权)
    ```
    GRANT ALL	PRIVILEGES on *.* TO wangwu
    ```
-- 查询权限
    ```
    SHOW GRANTS FOR wangwu
    ```
-- 查看root用户权限
    ```
    SHOW GRANTS FOR root@localhost
    ```
-- 撤销权限
    ```
    REVOKE ALL PRIVILEGES ON *.* FROM wangwu
    ```

# MySQL数据库的基本操作
## 连接数据库
进入MySQL命令提示符:

```
mysql -uroot -pxxx
```
退出 mysql> 命令提示窗口可以使用 exit 命令，如下所示：

```
mysql> exit
Bye
```

## 选择数据库
1. 查看所有的数据库:

```
show databases;
```
2. 切换到某个数据库:

```
use 数据库名;
```

## 创建数据库
```
create database 数据库名 charset=utf8;
```

数据库名字，它的名字必须是唯一的，不能和其它数据库重名。

## 删除数据库

```
drop database 数据库名;
```

# MySQL数据表的基本操作
## 数据类型
常见的数据类型:
- 整数类型：BIT、BOOL、TINY INT、SMALL INT、MEDIUM INT、 INT、 BIG INT
- 浮点数类型：FLOAT、DOUBLE、DECIMAL
- 字符串类型：CHAR、VARCHAR、TINY TEXT、TEXT、MEDIUM TEXT、LONGTEXT、TINY BLOB、BLOB、MEDIUM BLOB、LONG BLOB
- 日期类型：Date、DateTime、TimeStamp、Time、Year
- 其他数据类型：BINARY、VARBINARY、ENUM、SET、Geometry、Point、MultiPoint、LineString、MultiLineString、Polygon、GeometryCollection等

##### 整型

| MySQL数据类型 | 含义（有符号）                       |
| - | - |
| tinyint(m)    | 1个字节 范围(-128~127)               |
| smallint(m)   | 2个字节 范围(-32768~32767)           |
| mediumint(m)  | 3个字节 范围(-8388608~8388607)       |
| int(m)        | 4个字节 范围(-2147483648~2147483647) |
| bigint(m)     | 8个字节 范围(+-9.22*10的18次方)      |

取值范围如果加了unsigned，则最大值翻倍，如tinyint unsigned的取值范围为(0~256)。

##### 浮点型(float和double)

| MySQL数据类型 | 含义 |
| - | - |
| float(m,d)    | 单精度浮点型 8位精度(4字节) m总个数，d小数位  |
| double(m,d)   | 双精度浮点型 16位精度(8字节) m总个数，d小数位 |

##### 定点数

浮点型在数据库中存放的是近似值，而定点类型在数据库中存放的是精确值。

decimal(m,d) 参数m<65 是总个数，d<30且 d<m 是小数位。

##### 字符串(char,varchar,_text)

| MySQL数据类型 | 含义                            |
| - | --------------------------------- |
| char(n)       | 固定长度，最多255个字符         |
| varchar(n)    | 固定长度，最多65535个字符       |
| tinytext      | 可变长度，最多255个字符         |
| text          | 可变长度，最多65535个字符       |
| mediumtext    | 可变长度，最多2的24次方-1个字符 |
| longtext      | 可变长度，最多2的32次方-1个字符 |

**char和varchar：**
1.char(n) 若存入字符数小于n，则以空格补于其后，查询之时再将空格去掉。所以char类型存储的字符串末尾不能有空格，varchar不限于此。

2.char(n) 固定长度，char(4)不管是存入几个字符，都将占用4个字节，varchar是存入的实际字符数+1个字节（n<=255）或2个字节(n>255)，

3.char类型的字符串检索速度要比varchar类型的快。

**varchar和text：**

1.varchar可指定n，text不能指定，内部存储varchar是存入的实际字符数+1个字节（n<=255）或2个字节(n>255)，text是实际字符数+2个字节。

2.text类型不能有默认值。

3.varchar可直接创建索引，text创建索引要指定前多少个字符。varchar查询速度快于text，在都创建索引的情况下，text的索引似乎不起作用。

##### 二进制数据(_Blob)

1._BLOB和_text存储方式不同，_TEXT以文本方式存储，英文存储区分大小写，而_Blob是以二进制方式存储，不分大小写。

2._BLOB存储的数据只能整体读出。

3._TEXT可以指定字符集，_BLO不用指定字符集。

##### 日期时间类型

| MySQL数据类型 | 含义                          |
| - | - |
| date          | 日期 '2021-12-2'              |
| time          | 时间 '12:25:36'               |
| datetime      | 日期时间 '2021-12-2 22:06:44' |
| timestamp     | 自动存储记录修改时间          |

若定义一个字段为timestamp，这个字段里的时间数据会随其他字段修改的时候自动刷新，所以这个数据类型的字段可以存放这条记录最后被修改的时间。

## 创建数据表
##### 常规创建
CREATE TABLE 语句的基本语法如下：

```
CREATE TABLE IF NOT EXISTS `test_table`(
   `id` INT UNSIGNED AUTO_INCREMENT COMMENT '自增主键',
   `title` VARCHAR(100) NOT NULL,
   `author` VARCHAR(40) NOT NULL,
   `category` VARCHAR(40) NOT NULL DEFAULT 'unkown',
   `date` DATE,
   `create_time` timestamp DEFAULT CURRENT_TIMESTAMP()
   PRIMARY KEY ( `id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

CREATE TABLE 是 SQL 命令，告诉数据库你想创建一个新的表，IF NOT EXISTS表示如果要创建的表存在，则直接返回，不在重新创建该表。它后面紧跟的 table_name 是表的名字。然后在括号中定义表的列，以及每一列的类型。
- PRIMARY KEY 关键字用来指明表的主键。
- 某些字段使用了 NOT NULL 约束，表名在插入数据时这些字段不能为 NULL， 在操作数据库时如果输入该字段的数据为NULL ，就会报错。
- AUTO_INCREMENT 约束用来将某个字段的值设置为自动增长的序列。
- DEFAULT 约束用来设置字段的默认值。
- PRIMARY KEY 用来设置表的主键。
- IF NOT EXISTS表示，如果我们当前数据库中已经存在一个同名的表将不会执行改语句，避免了系统报错。
- COMMENT 为该字段添加注释，后面的字符串为注释内容属性添加注释。
- ENGINE=InnoDB DEFAULT CHARACTER=utf8;是数据库默认的可以不用写，这句是指：数据库引擎使用的是InnoDB， 默认的字符编码是utf8。

- 示例:
1. 最简单的：
```
CREATE TABLE t1(id int not null,name char(20));
```
2. 带主键的：
```
CREATE TABLE t1(id int not null primary key,name char(20));
```
3. 复合主键
```
CREATE TABLE t1(id int not null,name char(20),primary key (id,name));
```
4. 带默认值的：
```
CREATE TABLE t1(id int not null default 0 primary key,name char(20) default '1');
```

##### 复制表创建新表
```
create table 目标表 like 源表
```

##### 将tableA的部分数据拿来创建tableB
```
create table <tableB>(id int(10),name varchar(20));
select id, name
from tableA
```

##### 查看表的字段信息
MySQL命令：
```
desc 数据表名;
```

##### 关键字属性

| MySQL关键字        | 含义                     |
| - | - |
| NULL               | 数据列可包含NULL值       |
| NOT NULL           | 数据列不允许包含NULL值   |
| DEFAULT            | 默认值                   |
| PRIMARY KEY        | 主键                     |
| AUTO_INCREMENT     | 自动递增，适用于整数类型 |
| UNSIGNED           | 无符号                   |
| CHARACTER SET name | 指定一个字符集           |

## 修改数据表字段
随着开发进行 之前建好的表很可能不满足未来需求，所以对表的修改是必须的。同样，修改表也有通用语句：
```
ALTER TABLE <表名> [修改选项]
```

- 添加字段：

    ```
    ALTER TABLE <表名> ADD COLUMN <列名> <类型> ...               //-- 在末尾添加字段
    ALTER TABLE <表名> ADD COLUMN <列名> <类型> ... first         //-- 在开头添加字段
    ALTER TABLE <表名> ADD COLUMN <列名> <类型> ... after `name`  //在指定字段之后添加字段
    ALTER TABLE <表名> ADD COLUMN <列名> <类型> ...
    ```

- 修改字段名：

    ```
    ALTER TABLE <表名> CHANGE COLUMN <旧列名> <新列名> <新列类型> ...
    ```

- 优化(修改)字段类型:

    ```
    ALTER TABLE <表名> MODIFY COLUMN <列名> <类型> ...
    ```

- 删除字段:

    ```
    ALTER TABLE <表名> DROP COLUMN <列名> ...
    ```

- 修改表名:

    ```
    ALTER TABLE <表名> RENAME TO <新表名>
    ```

## 删除数据表字段

注意 使用 DROP TABLE 命令时一定要非常小心，因为一旦删除了表，那么该表中所有的信息将永远丢失。 语法 DROP TABLE 语句的基本语法如下：

```
DROP TABLE table_name;
```

table_name 表示要删除的数据表的名字。

>1、当你不再需要该表时， 用 drop; 2、当你仍要保留该表，但要删除所有记录时， 用 truncate; 3、当你要删除部分记录或者有可能会后悔的话， 用 delete。

# MySQL数据的基本操作

## 插入数据到表
INSERT语句的基本语法是：

```
insert into <表名> (字段1, 字段2, ...) values (值1, 值2, ...);
```

注意到我们并没有列出id字段，也没有列出id字段对应的值，这是因为id字段是一个自增主键，它的值可以由数据库自己推算出来。此外，如果一个字段有默认值，那么在INSERT语句中也可以不出现。 要注意，字段顺序不必和数据库表的字段顺序一致，但值的顺序必须和字段顺序一致。 还可以一次性添加多条记录，只需要在VALUES子句中指定多个记录值，每个记录是由(...)包含的一组值：
一次性添加多条新记录:
```
insert into students (class_id, name, gender, score) values
  (1, '张三', 'm', 87),
  (2, '李四', 'm', 81);

select * from students;
```

## 删除表中数据
DELETE语句的基本语法是：
```
delete from <表名> where ...;
```

## 修改表中数据

```
update <表名> set 字段1=值1, 字段2=值2, ... where ...;
```

## MySQL查询表中数据

### 查询所有的数据
```
SELECT * FROM table_name;
```

### 查询指定字段
```
SELECT f_name, f_price FROM table_name;
```

### 按条件查询
```
SELECT * FROM students WHERE score >= 80
```
SELECT语句可以通过WHERE条件来设定查询条件，查询结果是满足查询条件的记录。例如，要指定条件“分数在80分或以上的学生”，写成WHERE条件就是。 其中，WHERE关键字后面的score >= 80就是条件。score是列名，该列存储了学生的成绩，因此，score >= 80就筛选出了指定条件的记录。

##### 满足多个条件 AND
条件表达式可以用<条件1> AND <条件2>表达满足条件1并且满足条件2。例如，符合条件“分数在80分或以上”，并且还符合条件“男生”，把这两个条件写出来：
```
SELECT * FROM students WHERE score >= 80 AND gender = 'M'
```
##### 满足某个条件 OR
<条件1> OR <条件2>，表示满足条件1或者满足条件2。例如，把上述AND查询的两个条件改为OR，查询结果就是“分数在80分或以上”或者“男生”，满足任意之一的条件即选出该记录：
```
SELECT * FROM students WHERE score >= 80 OR gender = 'M'
```

##### 满足范围 IN
```
SELECT * FROM students WHERE score IN(60,100)
```
##### 条件查找优先级
如果不加括号，条件运算按照NOT、AND、OR的优先级进行，即NOT优先级最高，其次是AND，最后是OR。加上括号可以改变优先级。

### 查询结果排序
使用SELECT查询时，查询结果集通常是按照id排序的，也就是根据主键排序。这也是大部分数据库的做法。如果我们要根据其他条件排序怎么办？可以加上ORDER BY子句。 按score从低到高:

```
select id, name, gender, score from students order by score;
```

按score从高到低:

```
select id, name, gender, score from students order by score desc;
```

### 分页查询
分页 使用SELECT查询时，如果结果集数据量很大，比如几万行数据，放在一个页面显示的话数据量太大，不如分页显示，每次显示100条。
要实现分页功能，实际上就是从结果集中显示第1~100条记录作为第1页，显示第101~200条记录作为第2页，以此类推。
因此，分页实际上就是从结果集中“截取”出第M~N条记录。这个查询可以通过LIMIT <N-M> OFFSET <M>子句实现。
分页查询的关键在于，首先要确定每页需要显示的结果数量pageSize（这里是3），然后根据当前页的索引pageIndex（从1开始），确定LIMIT和OFFSET应该设定的值：
- LIMIT总是设定为pageSize；
- OFFSET计算公式为pageSize * (pageIndex - 1)。 这样就能正确查询出第N页的记录集。

### 聚合函数查询
在数据库查询过程中，不仅只返回数据的基础信息，有时还需对这些数据进行统计和汇总。MySQL 提供了聚合函数，用于实现这些高级功能。 聚合函数用于对一组值进行计算并返回一个汇总值，使用聚合函数可以统计记录行数、计算某个字段值的总和以及这些值的最大值、最小值和平均值等。

| **函数名称** | **功能**             |
| - | - |
| sum  | 返回选取的某列值的总和     |
| max  | 返回选取的某列的最大值     |
| min  | 返回选取的某列的最小值     |
| avg  | 返回选取的某列的平均值     |
| count| 返回选取的某列或记录的行数 |

##### COUNT
-- 统计班级共有多少同学
    ```
    SELECT COUNT(*) FROM student;
    ```
-- 统计班级收集的 qq_mail 有多少个，qq_mail 为 NULL 的数据不会计入结果
    ```
    SELECT COUNT(qq_mail) FROM student;
    ```
##### SUM
-- 统计数学成绩总分
    ```
    SELECT SUM(math) FROM exam_result;
    ```
-- 不及格 < 60 的总分，没有结果，返回 NULL
    ```
    SELECT SUM(math) FROM exam_result WHERE math < 60;
    ```
##### AVG
-- 统计平均总分
    ```
    SELECT AVG(chinese + math + english) 平均总分 FROM exam_result;
    ```
##### MAX
-- 返回英语最高分
    ```
    SELECT MAX(english) FROM exam_result;
    ```
##### MIN
-- 返回 > 70 分以上的数学最低分
    ```
    SELECT MIN(math) FROM exam_result WHERE math > 70;
    ```

### 多表查询
多表查询，也称为关联查询，指两个或更多个表一起完成查询操作。 前提条件：这些一起查询的表之间是有关系的（一对一、一对多），它们之间一定是有关联字段，这个关联字段可能建立了外键，也可能没有建立外键。比如：员工表和部门表，这两个表依靠“部门编号”进行关联。

##### 内连接查询
内连接（INNER JOIN) 使用比较运算符进行表间某（些）列数据的比较操作，并列出这些表中与连接条件相匹配的数据行，组合成新记录。简而言之，查找出同时存在在不同表中的关联数据形成结果表。
```
SELECT 字段1,字段2,字段3,…… FROM 表名1 INNER JOIN 表名2 ON 关联条件；
```
等同于:
```
SELECT 字段1,字段2,字段3,…… FROM 表名1,表名2 WHERE 关联条件；
```

例如，查询所有员工信息和对应的部门信息:
```
SELECT * FROM emp INNER JOIN dept ON emp.`dept_id` = dept.`id`;
```
等同于:
```
SELECT * FROM emp,dept WHERE emp.`dept_id` = dept.`id`;
```

INNER JOIN 连接三个数据表的用法：
```
SELECT * FROM (表1 INNER JOIN 表2 ON 表1.字段号=表2.字段号) INNER JOIN 表3 ON 表1.字段号=表3.字段号
```

**注意事项**
- 如果某字段在多表中都有，则以"表名.列名"限定别名；
- 与INNER JOIN组合使用ON子句，而不是WHERE。ON和WHERE后面的指定条件相同， WHERE子句定义条件更简单明了，但某些时候会影响查询性能，而INNER JOIN语法是ANSI SQL的标准规范，能够确保不忘记连接条件。

##### 外连接查询

**左外连接**
左连接从左表(t1)取出所有记录，与右表(t2)匹配。如果没有匹配，以null值代表右边表的列。
基本语法： 
```
SELECT * FROM [左表] LEFT OUTER JOIN [右表] on [左表].[字段]=[右表].[字段];
```
示例:
```
SELECT 	t1.*,t2.`name` FROM emp t1 LEFT JOIN dept t2 ON t1.`dept_id` = t2.`id`;
```

**右外连接**
右连接从右表(t2)取出所有记录，与左表(t1)匹配。如果没有匹配，以null值代表左边表的列。
基本语法：
```
SELECT * FROM [左表] RIGHT JOIN [右表] on [左表].[字段]=[右表].[字段];
```
示例:
```
SELECT 	* FROM dept t2 RIGHT JOIN emp t1 ON t1.`dept_id` = t2.`id`;
```

# SQL注入
### 什么是SQL注入
SQL注入（SQL Injection）是一种常见的Web安全漏洞，主要形成的原因是在数据交互中，进行数据库操作时，没有做严格的判断，导致其传入的“数据”拼接到SQL语句中后，被当作SQL语句的一部分执行。 
从而导致数据库受损（被脱库、被删除、甚至整个服务器权限陷）。

### 导致SQL注入的原因
SQL注入主要原因是程序员在开发用户和数据库的系统时没有对用户输入的字符串进行过滤、转义、限制或处理不严谨，导致攻击者可以通过精心构造的字符串去非法获取到数据库中的数据。

### 如何防止SQL注入
1. 严格限制 Web 应用的数据库的操作权限，给此用户提供仅仅能够满足其工作的最低权限，从而最大限度的减少注入攻击对数据库的危害。
2. 检查输入的数据是否具有所期望的数据格式，严格限制变量的类型，例如使用 regexp 包进行一些匹配处理，或者使用 strconv 包对字符串转化成其他基本类型的数据进行判断。
3. 对进入数据库的特殊字符（'"\ 尖括号 &*; 等）进行转义处理，或编码转换。Go 的 text/template 包里面的 HTMLEscapeString 函数可以对字符串进行转义处理。
4. 在应用发布之前建议使用专业的 SQL 注入检测工具进行检测，以及时修补被发现的 SQL 注入漏洞。网上有很多这方面的开源工具，例如 sqlmap、SQLninja 等。
5. 避免网站打印出 SQL 错误信息，比如类型错误、字段不匹配等，把代码里的 SQL 语句暴露出来，以防止攻击者利用这些错误信息进行 SQL 注入。

# SQL事务
### 什么是事务
事务（transaction）是作为单个逻辑单元执行的一系列操作。多个操作作为一个整体向系统提交，要么都执行，要么都不执行。 MySQL 事务主要用于处理操作量大，复杂度高的数据。
例如，在人员管理系统中，你删除一个人员，你既需要删除人员的基本资料，也要删除和该人员相关的信息，如信箱，文章等等，这样，这些数据库操作语句就构成一个事务！

### 事务的特性
一般来说，事务是必须满足4个条件（ACID）：：原子性（**A**tomicity，或称不可分割性）、一致性（**C**onsistency）、隔离性（**I**solation，又称独立性）、持久性（**D**urability）。

* **原子性：** 一个事务（transaction）中的所有操作，要么全部完成，要么全部不完成，不会结束在中间某个环节。事务在执行过程中发生错误，会被回滚（Rollback）到事务开始前的状态，就像这个事务从来没有执行过一样。
* **一致性：** 在事务开始之前和事务结束以后，数据库的完整性没有被破坏。这表示写入的资料必须完全符合所有的预设规则，这包含资料的精确度、串联性以及后续数据库可以自发性地完成预定的工作。
* **隔离性：** 数据库允许多个并发事务同时对其数据进行读写和修改的能力，隔离性可以防止多个事务并发执行时由于交叉执行而导致数据的不一致。事务隔离分为不同级别，包括读未提交（Read uncommitted）、读提交（read committed）、可重复读（repeatable read）和串行化（Serializable）。
* **持久性：** 事务处理结束后，对数据的修改就是永久的，即便系统故障也不会丢失。
> 在 MySQL 中只有使用了 Innodb 数据库引擎的数据库或表才支持事务。 事务处理可以用来维护数据库的完整性，保证成批的 SQL 语句要么全部执行，要么全部不执行。

### 事务的控制
在 MySQL 命令行的默认设置下，事务都是自动提交的，即执行 SQL 语句后就会马上执行 COMMIT 操作。因此要显式地开启一个事务务须使用命令 BEGIN 或 START TRANSACTION，或者执行命令 SET AUTOCOMMIT=0，用来禁止使用当前会话的自动提交。

##### 用 BEGIN, ROLLBACK, COMMIT来实现
* **BEGIN** 开始一个事务
* **ROLLBACK** 事务回滚
* **COMMIT** 事务确认

##### 直接用 SET 来改变 MySQL 的自动提交模式:

* **SET AUTOCOMMIT=0** 禁止自动提交
* **SET AUTOCOMMIT=1** 开启自动提交


##### 事务的控制命令语句
* BEGIN 或 START TRANSACTION 显式地开启一个事务；
* COMMIT 也可以使用 COMMIT WORK，不过二者是等价的。COMMIT 会提交事务，并使已对数据库进行的所有修改成为永久性的；
* ROLLBACK 也可以使用 ROLLBACK WORK，不过二者是等价的。回滚会结束用户的事务，并撤销正在进行的所有未提交的修改；
* SAVEPOINT identifier，SAVEPOINT 允许在事务中创建一个保存点，一个事务中可以有多个 SAVEPOINT；
* RELEASE SAVEPOINT identifier 删除一个事务的保存点，当没有指定的保存点时，执行该语句会抛出一个异常；
* ROLLBACK TO identifier 把事务回滚到标记点；
* SET TRANSACTION 用来设置事务的隔离级别。InnoDB 存储引擎提供事务的隔离级别有READ UNCOMMITTED、READ COMMITTED、REPEATABLE READ 和 SERIALIZABLE。

# MySQL导入导出数据
### 导出数据
##### 导出整个数据库中的所有数据
```
mysqldump -u 用户名 -p密码 数据库名 > 导出的文件名
```
示例:
```
mysqldump -u userName -ppassword dabaseName > test_db.sql
```
>结尾没有分号。test_db.sql最好加上路径名。

##### 导出数据库中的某个表的数据
```
mysqldump -u 用户名 -p密码 数据库名 表名> 导出的文件名
```
示例:
```
mysqldump -u userName -ppassword dabaseName tableName > fileName.sql
```

##### 导出整个数据库中的所有的表结构
```
mysqldump -u userName -ppassword -d dabaseName > fileName.sql
```

##### 导出整个数据库中某个表的表结构
```
mysqldump -u userName -ppassword -d dabaseName tableName >fileName.sql
```

### 导入数据
使用 MySQL 命令导入语法格式为：
```
mysql -u用户名    -p密码    <  要导入的数据库数据sql文件
```
示例：
```
mysql -uroot -p123456 < student.sql
```
>以上命令将将备份的整个数据库 student.sql 导入。

# 数据库表的设计原则
- id类型如果没有特殊要求，必须使用bigint unsigned，禁止使用int，即使现在的数据量很小。
- 单表行数超过 500 万行或者单表容量超过 2GB，才推荐进行分库分表。 说明:如果预计2年后的数据量根本达不到这个级别，请不要在创建表时就分库分表。
- 表必备三个字段，id，create_time，update_time，其中id为主键类型为 bigint unsigned、单表时自增、步长为 1， create_time，update_time 为datetime 类型，前者现在时表示创建时间，后者过去分词表示更新时间。
- 表名，字段名必须使用小写字母或数字，且开头不能使用数字。
- 表达是与否概念的字段，必须使用 is_xxx 的方式命名，数据类型是 unsigned tinyint ( 1表示是，0表示否)。
- 小数类型为 decimal，禁止使用 float 和 double。 说明：float 和 double 在存储的时候，存在精度损失的问题，很可能在值的比较时，得到不 正确的结果。如果存储的数据范围超过 decimal 的范围，建议将数据拆成整数和小数分开存储。
- varchar 是可变长字符串，不预先分配存储空间，长度不要超过 5000，如果存储长度大于此值，定义字段类型为 text，独立出来一张表，用主键来对应，避免影响其它字段索引效率。
- 不得使用外键与级联，一切外键概念必须在程序业务端解决。外键与级联更新适用于单机低并发，不适合分布式、高并发集群；级联更新是强阻塞，存在数据库更新风暴和死锁的风险；并且外键影响数据库的插入速度。

# 参考资料:
[docker 安装mysql8](https://www.cnblogs.com/hu308830232/p/15211720.html)
[菜鸟教程](https://www.runoob.com/mysql/mysql-connection.html)
[MySQL教程](http://c.biancheng.net/mysql/)
[廖雪峰SQL教程](https://www.liaoxuefeng.com/wiki/1177760294764384)
[一个小时学会MySQL数据库](https://www.cnblogs.com/best/p/6517755.html#_lab2_0_2)
[MySQL详细学习教程](https://blog.csdn.net/qq_45173404/article/details/115712758)
[MySql教程](https://github.com/Vibing/blog)
[MySQL 有这一篇就够](https://blog.csdn.net/weixin_45851945/article/details/114287877)
[MySQL基础教程15——多表查询](https://juejin.cn/post/7078512878214447135)

