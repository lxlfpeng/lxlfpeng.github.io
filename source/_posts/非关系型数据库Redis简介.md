---
title: 非关系型数据库Redis简介
date: 2021-06-10
categories: 
  - 数据库
tags: 
  - 数据库
  - 后端开发
  - 数据存储
---

# 一.Redis简介
### Redis简介
Redis 全称 Remote Dictionary Server（即远程字典服务），它是一个基于内存实现的键值型非关系（NoSQL）数据库， 使用 ANSI C 语言编写、遵守 BSD 协议、支持网络、可基于内存、分布式、可选持久性的键值对(Key-Value)存储数据库。

### Redis的特点
* Redis支持数据的持久化，可以将内存中的数据保存在**磁盘**中，重启的时候可以再次加载进行使用。
* Redis不仅仅支持简单的key-value类型的数据，同时还提供list，set，zset，hash等数据结构的存储。
* Redis支持数据的备份，即master-slave模式的数据备份。

### Redis应用场景
数据库的存储方式大体可分为两大类，基于磁盘存储和基于内存存储。磁盘存储的数据库，因为磁头机械运动以及系统调用等因素导致读写效率较低。Redis 基于内存来实现数据存取，相对于磁盘来说，其读写速度要高出好几个数量级。因此Redis一般用来缓存一些经常被访问的热点数据、或者需要耗费大量资源的内容，通过把这些内容放到 Redis 中，可以让应用程序快速地读取它们。例如，网站的首页需要经常被访问，并且在创建首页的过程中会消耗的较多的资源，此时就可以使用 Redis 将整个首页缓存起来，从而降低网站的压力，减少页面访问的延迟时间。又比如再商城类的业务中，秒杀类的场景大家都是比较熟悉的，往往电商官方推出一款产品，然后在某一个特定的时间点向广大的消费者开发订购功能，那么在那个特定的时间点，可能系统平台一下子就达到10W+的QPS访问量，10w+的QPS，如果直接指向数据库，数据库很容易崩溃，导致整个系统崩溃。对于以上的业务场景，Redis就派上大用场了，一个很简单的思路，我们可以将商品的相关的信息初始化到redis中，当用户访问的时候，可以直接从Redis中获取数据返回给用户，这样的话，mysql的访问量就一下子降低了很多，同时用户的访问速度也会得到很大的提升。当然，Redis的实际应用场景是很多的，但是总的来说大部分的应用场景的眼里都是将数据保存在redis中，然后利用Redis的高性能来实现业务场景的高可用、高并发等业务问题。由此可见，将复杂的高并发和高可用业务模型简单化，Redis堪称一代神器了。


>注意:Redis 基于内存来实现数据的存储，因此其速度非常快。但是我们知道，计算机的内存是非常珍贵的资源，所以 Redis 不适合存储较大的文件或者二进制数据，否则会出现错误，Redis 适合存储较小的文本信息。理论上 Redis 的每个 key、value 的大小不超过 512 MB。

### Redis的优势
- 性能极高：Redis 基于内存实现数据存储，它的读取速度是 110000次/s，写速度是 81000次/s；
- 多用途工具： Redis 有很多的用途，比如可以用作缓存、消息队列、搭建 Redis 集群等；
- 命令提示功能：Redis 客户端拥有强大的命令提示功能，使用起来非常的方便，降低了学习门槛；
- 可移植性：Redis 使用用标准 C语言编写的，能够在大多数操作系统上运行，比如 Linux，Mac，Solaris 等；

# 二.Docker安装Redis教程

### 1.搜索镜像

```
docker search redis
```

### 2.拉取镜像

```
docker pull redis
```

在不指定版本的情况下，默认是拉取最新版本。

### 3.准备容器数据目录

```
mkdir -p /usr/redis/conf
mkdir -p /usr/share/redis
```

### 4.编辑Redis的配置文件
启动前需要先创建Redis外部挂载的配置文件 （ /home/redis/conf/redis.conf ）之所以要先创建 ， 是因为Redis本身容器只存在 /etc/redis 目录 ， 本身就不创建 redis.conf 文件当服务器和容器都不存在 redis.conf 文件时， 执行启动命令的时候 docker 会将 redis.conf 作为目录创建 ， 这并不是我们想要的结果 。因为 redis 默认配置你会发现只能够本地连接，不能进行远程访问，使用 Redis Desktop Manager连接都会报错，因此需要手动挂载 redis 配置文件。

```
cd /usr/redis/conf
wget http://download.redis.io/redis-stable/redis.conf
```

> 配置文件内容特别说明

- bind 127.0.0.1 #注释掉这部分，这是限制redis只能本地访问；
- protected-mode no #默认yes，开启保护模式，限制为本地访问；
- daemonize no #默认no，改为yes意为以守护进程方式启动，可后台运行，除非kill进程（可选），改为yes会使配置文件方式启动redis失败；
- dir ./ #输入本地redis数据库存放文件夹（可选）；
- appendonly yes #redis持久化（可选）；

### 5.安装运行redis

```
docker run -p 6379:6379 --name redis -v /usr/redis/conf/redis.conf:/etc/redis/redis.conf  -v /usr/share/redis:/data -d redis redis-server /etc/redis/redis.conf --appendonly yes
```

参数说明

* --appendonly yes 开启持久化；
* redis-server /etc/redis/redis.conf 以redis.conf作为配置文件启动；
* -v 配置数据卷；
* --name redis: 容器别名；
* -d ：后台启动；
* -p 6379:6379：映射容器服务的 6379 端口到宿主机的 6379 端口。外部可以直接通过宿主机ip:6379 访问到 Redis 的服务。（前者为宿主机端口，后者为容器端口）；
* redis：为镜像名称；

### 6.进入容器

```
docker exec -it redis /bin/bash
```

这里可以通过容器别名或者容器ID都是可以进入的。

# 三.Redis支持的数据类型
- String: 字符串
- Hash: 散列
- List: 列表
- Set: 集合
- Sorted Set: 有序集合

## 1.String（字符串）
string是redis最基本的类型，一个key对应一个value，string类型是二进制安全的。意思是redis的string可以包含任何数据。比如jpg图片或者序列化的对象 。string一个键最大能存储512MB。
```
> SET name "zhangsan"
OK
> GET name
"zhangsan"
```
在以上实例中我们使用了 Redis 的 SET 和 GET 命令。键为 name，对应的值为 `zhangsan`。

## 2.Hash（哈希）

Redis hash 是一个 string 类型的 field 和 value 的映射表，hash 特别适合用于存储对象。

```
> HMSET student name "zhangsan" age "35"
"OK"
> HGET student name
"zhangsan"
> HGET student age
"35"
```

实例中我们使用了 Redis HMSET， HGET 命令，HMSET 设置了两个 field=>value 对， HGET 获取对应 field 对应的 value。

## 3.List（列表）

Redis 列表是简单的字符串列表，按照插入顺序排序。你可以添加一个元素到列表的头部（左边）或者尾部（右边）。

```
> lpush students zhangsan
(integer) 1
> lpush students lisi
(integer) 2
> lpush students wangwu
(integer) 3
> lrange students 0 10
1) "zhangsan"
2) "lisi"
3) "wangwu"
```

>列表最多可存储 232 - 1 元素 (4294967295， 每个列表可存储40多亿)。

## 4.Set（集合）
Redis的Set是string类型的无序集合。 集合是通过哈希表实现的，所以添加，删除，查找的复杂度都是O(1)。
```
> sadd users zhangsan
(integer) 1
> sadd users lisi
(integer) 1
> sadd users wangwu
(integer) 1
> sadd users wangwu
(integer) 0
> smembers users
1) "lisi"
2) "wangwu"
3) "zhangsan"
```

>注意：以上实例中 wangwu 添加了两次，但根据集合内元素的唯一性，第二次插入的元素将被忽略。 集合中最大的成员数为 232 - 1(4294967295， 每个集合可存储40多亿个成员)。

## 5.zset(sorted set：有序集合)
Redis zset 和 set 一样也是string类型元素的集合，且不允许重复的成员。 不同的是每个元素都会关联一个double类型的分数。redis正是通过分数来为集合中的成员进行从小到大的排序。 zset的成员是唯一的，但分数(score)却可以重复。

```
> zadd staffs 0 zhangsan
(integer) 1
> zadd staffs 0 lisi
(integer) 1
> zadd staffs 0 wangwu
(integer) 1
> zadd staffs 0 wangwu
(integer) 0
> ZRANGEBYSCORE staffs 0 10
1) "lisi"
2) "wangwu"
3) "zhangsan"
```

# 四.Redis基础命令操作
Redis客户端的基本语法如下：
```
$redis-cli
```
要启动redis客户端，打开终端，输入命令Redis命令行：``redis-cli``。这将连接到本地服务器，现在就可以运行各种命令了。

### 1.连接操作相关的命令

* quit：关闭连接（connection）
* auth：简单密码认证

### 2.对value操作的命令

* exists(key)：确认一个key是否存在
* del(key)：删除一个key
* type(key)：返回值的类型
* keys(pattern)：返回满足给定pattern的所有key
* randomkey：随机返回key空间的一个key
* rename(oldname, newname)：将key由oldname重命名为newname，若newname存在则删除newname表示的key
* dbsize：返回当前数据库中key的数目
* expire：设定一个key的活动时间（s）
* ttl：获得一个key的活动时间
* select(index)：按索引查询
* move(key, dbindex)：将当前数据库中的key转移到有dbindex索引的数据库
* flushdb：删除当前选择数据库中的所有key
* flushall：删除所有数据库中的所有key

### 3.对String操作的命令

* set(key, value)：给数据库中名称为key的string赋予值value
* get(key)：返回数据库中名称为key的string的value
* getset(key， value)：给名称为key的string赋予上一次的value
* mget(key1, key2,…, key N)：返回库中多个string（它们的名称为key1，key2…）的value
* setnx(key, value)：如果不存在名称为key的string，则向库中添加string，名称为key，值为value
* setex(key, time, value)：向库中添加string（名称为key，值为value）同时，设定过期时间time
* mset(key1, value1, key2, value2,…key N, value N)：同时给多个string赋值，名称为key i的string赋值value i
* msetnx(key1, value1, key2, value2,…key N, value N)：如果所有名称为key i的string都不存在，则向库中添加string，名称key i赋值为value i
* incr(key)：名称为key的string增1操作
* incrby(key, integer)：名称为key的string增加integer
* decr(key)：名称为key的string减1操作
* decrby(key, integer)：名称为key的string减少integer
* append(key, value)：名称为key的string的值附加value
* substr(key, start, end)：返回名称为key的string的value的子串

### 4.对List操作的命令

* rpush(key, value)：在名称为key的list尾添加一个值为value的元素
* lpush(key, value)：在名称为key的list头添加一个值为value的 元素
* llen(key)：返回名称为key的list的长度
* lrange(key, start, end)：返回名称为key的list中start至end之间的元素（下标从0开始，下同）
* ltrim(key, start, end)：截取名称为key的list，保留start至end之间的元素
* lindex(key, index)：返回名称为key的list中index位置的元素
* lset(key, index, value)：给名称为key的list中index位置的元素赋值为value
* lrem(key, count, value)：删除count个名称为key的list中值为value的元素。count为0，删除所有值为value的元素，count>0从头至尾删除count个值为value的元素，count<0从尾到头删除|count|个值为value的元素。 lpop(key)：返回并删除名称为key的list中的首元素 rpop(key)：返回并删除名称为key的list中的尾元素 blpop(key1, key2,… key N, timeout)：lpop命令的block版本。即当timeout为0时，若遇到名称为key i的list不存在或该list为空，则命令结束。如果timeout>0，则遇到上述情况时，等待timeout秒，如果问题没有解决，则对keyi+1开始的list执行pop操作。
* brpop(key1, key2,… key N, timeout)：rpop的block版本。参考上一命令。
* rpoplpush(srckey, dstkey)：返回并删除名称为srckey的list的尾元素，并将该元素添加到名称为dstkey的list的头部

### 5.对Set操作的命令

* sadd(key, member)：向名称为key的set中添加元素member
* srem(key, member) ：删除名称为key的set中的元素member
* spop(key) ：随机返回并删除名称为key的set中一个元素
* smove(srckey, dstkey, member) ：将member元素从名称为srckey的集合移到名称为dstkey的集合
* scard(key) ：返回名称为key的set的基数
* sismember(key, member) ：测试member是否是名称为key的set的元素
* sinter(key1, key2,…key N) ：求交集
* sinterstore(dstkey, key1, key2,…key N) ：求交集并将交集保存到dstkey的集合
* sunion(key1, key2,…key N) ：求并集
* sunionstore(dstkey, key1, key2,…key N) ：求并集并将并集保存到dstkey的集合
* sdiff(key1, key2,…key N) ：求差集
* sdiffstore(dstkey, key1, key2,…key N) ：求差集并将差集保存到dstkey的集合
* smembers(key) ：返回名称为key的set的所有元素
* srandmember(key) ：随机返回名称为key的set的一个元素

### 6.对zset（sorted set）操作的命令

* zadd(key, score, member)：向名称为key的zset中添加元素member，score用于排序。如果该元素已经存在，则根据score更新该元素的顺序。
* zrem(key, member) ：删除名称为key的zset中的元素member
* zincrby(key, increment, member) ：如果在名称为key的zset中已经存在元素member，则该元素的score增加increment；否则向集合中添加该元素，其score的值为increment
* zrank(key, member) ：返回名称为key的zset（元素已按score从小到大排序）中member元素的rank（即index，从0开始），若没有member元素，返回“nil”
* zrevrank(key, member) ：返回名称为key的zset（元素已按score从大到小排序）中member元素的rank（即index，从0开始），若没有member元素，返回“nil”
* zrange(key, start, end)：返回名称为key的zset（元素已按score从小到大排序）中的index从start到end的所有元素
* zrevrange(key, start, end)：返回名称为key的zset（元素已按score从大到小排序）中的index从start到end的所有元素
* zrangebyscore(key, min, max)：返回名称为key的zset中score >= min且score <= max的所有元素 zcard(key)：返回名称为key的zset的基数 zscore(key, element)：返回名称为key的zset中元素element的score zremrangebyrank(key, min, max)：删除名称为key的zset中rank >= min且rank <= max的所有元素 zremrangebyscore(key, min, max) ：删除名称为key的zset中score >= min且score <= max的所有元素
* zunionstore / zinterstore(dstkeyN, key1,…,keyN, WEIGHTS w1,…wN, AGGREGATE SUM|MIN|MAX)：对N个zset求并集和交集，并将最后的集合保存在dstkeyN中。对于集合中每一个元素的score，在进行AGGREGATE运算前，都要乘以对于的WEIGHT参数。如果没有提供WEIGHT，默认为1。默认的AGGREGATE是SUM，即结果集合中元素的score是所有集合对应元素进行SUM运算的值，而MIN和MAX是指，结果集合中元素的score是所有集合对应元素中最小值和最大值。

### 7.对Hash操作的命令

* hset(key, field, value)：向名称为key的hash中添加元素field<—>value
* hget(key, field)：返回名称为key的hash中field对应的value
* hmget(key, field1, …,field N)：返回名称为key的hash中field i对应的value
* hmset(key, field1, value1,…,field N, value N)：向名称为key的hash中添加元素field i<—>value i
* hincrby(key, field, integer)：将名称为key的hash中field的value增加integer
* hexists(key, field)：名称为key的hash中是否存在键为field的域
* hdel(key, field)：删除名称为key的hash中键为field的域
* hlen(key)：返回名称为key的hash中元素个数
* hkeys(key)：返回名称为key的hash中所有键
* hvals(key)：返回名称为key的hash中所有键对应的value
* hgetall(key)：返回名称为key的hash中所有的键（field）及其对应的value

### 8.持久化

* save：将数据同步保存到磁盘
* bgsave：将数据异步保存到磁盘
* lastsave：返回上次成功将数据保存到磁盘的Unix时戳
* shundown：将数据同步保存到磁盘，然后关闭服务

### 9.远程服务控制

* info：提供服务器的信息和统计
* monitor：实时转储收到的请求
* slaveof：改变复制策略设置
* config：在运行时配置Redis服务器

# 五.Redis可视化工具
### RedisDesktopManager(收费)
[RedisDesktopManager](https://github.com/uglide/RedisDesktopManager) 实用比较广泛的可视化工具，旧版免费使用，最新版需要收费。一般开发上十万级别数据就会卡顿延迟。界面比较简洁，功能很全。

### AnotherRedisDesktopManager(免费)
[AnotherRedisDesktopManager](https://github.com/qishibo/AnotherRedisDesktopManager) 一款比较稳定简洁的redis UI工具， **百万级数据加载不卡顿，无延迟。** 

