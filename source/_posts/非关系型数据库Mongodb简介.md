---
title: 非关系型数据库Mongodb简介
date: 2021-05-25
categories: 
  - 数据库
tags: 
  - 数据库
  - MongoDB
  - NoSQL
  - 数据存储
---

# 一.MongoDB简介
### 什么是NoSQL
NoSQL：Not Only SQL ，本质也是一种数据库的技术，相对于传统数据库技术，它不会遵循一些约束，比如：sql标准、ACID属性，表结构等。
**优点:**
- 满足对数据库的高并发读写；
- 对海量数据的高效存储和访问；
- 对数据库高扩展性和高可用性；
- 灵活的数据结构，满足数据结构不固定的场景；

**缺点:**

- 一般不支持事务；
- 运维人员数据维护相对复杂；

### 什么是MongoDB
[MongoDB](http://www.mongodb.org/) 是一个基于分布式文件存储的数据库。由C++语言编写，旨在为WEB应用提供可扩展的高性能数据存储解决方案。MongoDB 将数据存储为一个文档，数据结构由键值(key=>value)对组成，MongoDB文档类似于json对象，字段值可以包含其他文档，数组及文档数组。 MongoDB是一个介于关系数据库和非关系数据库之间的产品，是非关系数据库当中功能最丰富，最像关系数据库的。

### MongoDB的特点
MongoDB 最大的特点是他支持的查询语言非常强大，其语法有点类似于面向对象的查询语言，几乎可以实现类似关系数据库单表查询的绝大部分功能，而且还支持对数据建立索引。它是一个面向集合的，模式自由的文档型数据库。

- 面向集合存储，易于存储对象类型的数据；
- 模式自由；
- 支持动态查询；
- 支持完全索引，包含内部对象；
- 支持复制和故障恢复；
- 使用高效的二进制数据存储，包括大型对象（如视频等）；
- 自动处理碎片，以支持云计算层次的扩展性；
- 支持Python，PHP，Ruby，Java，C，C#，Javascript，Perl 及 C++语言的驱动程序，社区中也提供了对Erlang 及.NET 等平台的驱动程序；
- 文件存储格式为 BSON（ JSON 的扩展）；

### MongoDB的结构
MongoDB 的逻辑结构是一种层次结构。主要由：数据(database)、集合(collection) 、文档(document)这三部分组成的:

- 数据库（database）:
  数据库是一个仓库，在仓库中可以存放集合。

- 集合（collection）:
  集合类似于数组，在集合中可以存放文档。

- 文档（document）:
  文档是数据库中的最小单位，存储和操作的内容都是文档。

**MongoDB与MySQL数据库逻辑结构概念的对比:**

| MongoDb           | 关系型数据库Mysql |
| - | - |
| 数据库(databases) | 数据库(databases) |
| 集合(collections) | 表(table)         |
| 文档(document)    | 行(row)           |
| 域(field) |数据字段(column)|

### MongoDB支持的数据类型

| 类型       | 示例|
| - | - |
| null       | 用于表示空值或者不存在的字段，`{"x":null}`                                                                                                                               |
| 布尔型     | 布尔类型有两个值true和false，`{"x":true}`                                                                                                                                |
| 数值       | shell默认使用64为浮点型数值{“x”：3.14}或{“x”：3}，对于整型值可以使用NumberInt(4字节符号整数)或NumberLong(8字节符号整数)，`{"x”:NumberInt(“3")}{"x":NumberLong("3")}` |
| 字符串     | UTF-8字符串都可以表示为字符串类型的数据，`{"x":"呵呵"}`                                                                                                                  |
| 日期       | 日期被存储为自新纪元依赖经过的毫秒数，不存储时区，`{"x":new Date()}`                                                                                                     |
| 正则表达式 | 查询时，使用正则表达式作为限定条件，语法与JavaScript的正则表达式相同，`{"x":/[abc]/}`                                                                                    |
| 数组       | 数据列表或数据集可以表示为数组，`{"x"： ["a"，"b"，"c"]}`                                                                                                                 |
| 内嵌文档   | 文档可以嵌套其他文档，被嵌套的文档作为值来处理，`{"x":{"y":3 }}`                                                                                                         |
| 对象Id     | 对象id是一个12字节的字符串，是文档的唯一标识，相当于UUID`{"x":objectId()}`                                                                                               |
| 二进制数据 | 二进制数据是一个任意字节的字符串。它不能直接在shell中使用。如果要将非utf-字符保存到数据库中，二进制数据是唯一的方式                                                          |
| 代码       | 查询和文档中可以包括任何JavaScript代码，`{"x":function(){/…/}}`                                                                                                          |

# 二.Docker安装MongoDB

1. 搜索镜像

```
docker search mongo
```

2. 下载镜像

```
docker pull mongo
```

3. 创建一个文件夹，用作mongodb的数据目录挂载

```
sudo mkdir -p /usr/mongodb/datadb
#mongodb下面所有子目录给予777权限
sudo chmod 777 -R /usr/mongodb/
```

4. 启动MongoDB容器

```
docker run -d --name mongodb -p 27018:27017 -v /usr/mongodb/datadb:/data/db --privileged=true --restart always mongo
```
参数介绍:
* -d 后台运行容器
* –name mongodb 运行容器名
* -p 27018:27017 将容器的27017端口映射到主机的27018端口
* -v /usr/mongodb/datadb:/data/db 文件挂载： 本机:容器
* –privileged=true 使得容器内的root拥有真正的root权限
* –restart always 跟随docker一起启动，即docker启动时会自动运行容器
* mongo 运行的镜像名字

5. 查看MongoDB容器是否启动成功

```
docker ps -a
```

6. 进入MongoDB容器

```
docker exec -it mongodb /bin/bash
```

7. 查看MongoDB信息

```
mongo
```

会输出Mongo相关信息并进入命令工具:

```
MongoDB shell version v5.0.9
connecting to: mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb
...
```

# 三.MongoDB相关配置
### MongoDB账户权限配置
默认情况下，MongoDB实例启动运行时是没有启用用户访问权限控制的，也就是说，默认是"非授权模式"(也就是不需要任何权限验证、不需要验证账户，直接在命令窗口中输入 mongo 回车，就可以进行相关操作)，这是非常不安全的(尤其是在生产环境中)为了能保障mongodb的安全可以做以下几个步骤：
- 配置数据库的用户访问权限
- 使用新的端口，默认的27017端口如果一旦知道了ip就能连接上，不太安全。
- 设置mongodb的网络环境，最好将mongodb部署到公司服务器内网，这样外网是访问不到的。公司内部访问使用vpn等。
- 开启安全认证。认证要同时设置服务器之间的内部认证方式，同时要设置客户端连接到集群的账号密码认证方式。

##### 创建数据库管理员账户
要添加用户，MongoDB提供了``db.createUser()``方法。添加用户时，可以为用户分配角色，授予权限。在数据库中创建的第一个用户应该具有管理其他用户的权限。


1. 进入mongo语法环境
```
mongo
```
2. 创建admin数据库
```
use admin
```
4. 添加管理员用户
```
db.createUser({
        user: "root",
        pwd: "123",
        customData: {description:"superuser"},
        roles:[{role: "userAdminAnyDatabase" , db:"admin"}]
})
```
- user字段，为新用户的名字；
- pwd字段，用户的密码；
- cusomData字段，为任意内容，例如可以为用户全名介绍；
- roles字段，指定用户的角色，可以用一个空数组给新用户设定空角色。在roles字段,可以指定内置角色和用户定义的角色。超级用户的role有两种，userAdmin或者userAdminAnyDatabase(比前一种多加了对所有数据库的访问,仅仅是访问而已)。
- db是指定数据库的名字，admin是管理数据库。 不能用admin数据库中的用户登录其他数据库。

一旦经过认证的用户管理员，可以使用db.createUser()去创建额外的用户。
>注：用户管理员只能查看当前数据库中的用户，只能查看admin数据库中创建的用户。用户管理员应只有创建用户账户的权限，而不能管理数据库或执行其他管理任务。


##### 创建一个业务数据库管理员用户
业务数据库管理员用户只负责某一个或几个数据库的増查改删
```
db.createUser({
    user:"user1",
    pwd:"123456",
    customData:{
        name:'zhangsan',
        email:'zhangsan@qq.com',
        age:18,
    },
    roles:[
        {role:"readWrite",db:"db001"},
        {role:"readWrite",db:"db002"},
        'read'// 对其他数据库有只读权限，对db001、db002是读写权限
    ]
})
```

- 数据库用户角色：read、readWrite；
  - Read：允许用户读取指定数据库
  - readWrite：允许用户读写指定数据库
- 数据库管理角色：dbAdmin、dbOwner、userAdmin;
  - dbAdmin：允许用户在指定数据库中执行管理函数，如索引创建、删除，查看统计或访问system.profile
  - userAdmin：允许用户向system.users集合写入，可以在指定数据库里创建、删除和管理用户
  - clusterAdmin：只在admin数据库中可用，赋予用户所有分片和复制集相关函数的管理权限。
- 备份恢复角色：backup、restore；
- 所有数据库角色：readAnyDatabase、readWriteAnyDatabase、userAdminAnyDatabase、dbAdminAnyDatabase
  - readAnyDatabase：只在admin数据库中可用，赋予用户所有数据库的读权限
  - readWriteAnyDatabase：只在admin数据库中可用，赋予用户所有数据库的读写权限
  - userAdminAnyDatabase：只在admin数据库中可用，赋予用户所有数据库的userAdmin权限
  - dbAdminAnyDatabase：只在admin数据库中可用，赋予用户所有数据库的dbAdmin权限。
- 超级用户角色：root
  - root：只在admin数据库中可用。超级账号，超级权限

##### 账户配置常用命令

- 查看当前数据库中的用户
    ```
    show users
    或：
    db.getUsers()
    ```
- 登录认证
    ```
    db.auth("admin", "123456")
    ```
- 创建用户
    ```
    db.createUser({
        user："admin",    // 用户名
        pwd："123456",    // 密码
        roles：["root"]   // 角色
    }) 
    ```
- 修改用户密码
    ```
    db.updateUser( "admin", {
        pwd: "abc666"
    })
    ```
- 删除用户
    ```
    db.dropUser("admin")  // admin 是要删除的用户名
    ```

# 四.MongoDB操作
### 数据库操作
##### 查看数据库
使用show dbs来查看所有的数据库:

```
show dbs
```

##### 创建/切换数据库
使用use命令来切换/创建数据库，会发现创建的数据库并不在数据库的列表中， 要显示它，需要向数据库插入一些数据:

```
use db_name
```

> 注：1.use命令具有打开、 切换、 创建数据库的功能: 如果打开的这个数据库存在就是打开这个数据库。如果打开的是一个不存在的数据库(没有这个数据库名字)，那么就会创建一个同名的数据库。
> 2.在MongoDB中创建一个新的数据库时，需要向数据库中创建一个集合(collections【就像关系数据库中的表】)，并且插入一条数据，这个数据库才能创建成功。

##### 显示当前选中的数据库
使用db命令来显示当前数据库

```
db
```

> 注:使用MongoDB客户端进行操作，MongoDB 中默认的数据库为 test，如果没有创建新的数据库，集合将存放在 test 数据库中。

##### 删除数据库
1. 先切换到要删除的数据中

  ```
  > use db_name
  ```

2. 删除数据库（需要先切换到要删除的数据库）

  ```
  > db.dropDatabase()
  ```

> 注：这个命令一定要慎用，一旦该命令一执行一下当前所在数据库中的所有数据都会被清空。

##### 查看当前数据库相关信息
```
> db.stats()
```
>名称、文档个数、视图、索引、大小等

##### 查看集合(表)

```
> show tables
```

##### 删除集合（表）

```
> db.user.drop()
```

> 注：如果成功删除选定集合，则 drop() 方法返回 true，否则返回 false。

### 集合(数据表)操作

##### 插入数据

往集合中插入一条数据。可以不用先创建集合，直接往里添加数据即可。

```
> db.user.insert({"name": "zhangsan"})
```

> user就是集合(表)名，当命令执行后，数据库系统发现user是一个数据集合不存的，就自动创建一个名为user的集合，并随着数据的插入，数据库和集合也就真正的创建成功了。

##### 修改数据

更新数据(更新不存在的数据，会新增字段))

```
db.user.update({id:1},{$set:{age:22}},true)
```

参考说明：

```
db.collection.update(
   <query>,
   <update>,
   [
	 upsert: <boolean>,
	 multi: <boolean>,
	 writeConcern: <document>
   ]
)
```

- query : update的查询条件，类似sql update查询内where后面的。
- update : update的对象和一些更新的操作符（如$，$inc...）等，也可以理解为sql update查询内set后面的
- upsert : 可选，这个参数的意思是，如果不存在update的记录，是否插入objNew，true为插入，默认是false，不插入。
- multi : 可选，mongodb 默认是false，只更新找到的第一条记录，如果这个参数为true，就把按条件查出来多条记录全部更新。
- writeConcern :可选，抛出异常的级别。

##### 查询数据

```
db.user.find()  #查询全部数据
db.user.find({},{id:1,username:1})  #只查询id与username字段
db.user.find().count()  #查询数据条数
db.user.find({id:1}) #查询id为1的数据
db.user.find({age:{$lte:21}}) #查询小于等于21的数据
db.user.find({age:{$lte:21}, id:{$gte:2}}) #and查询，age小于等于21并且id大于等于2
db.user.find({$or:[{id:1},{id:2}]}) #查询id=1 or id=2

#分页查询：Skip()跳过几条，limit()查询条数
db.user.find().limit(2).skip(1)  #跳过1条数据，查询2条数据

db.user.find().sort({id:-1}) #按照age倒序排序，-1为倒序，1为正序
```

参考说明:

```
db.user.find([query],[fields])
```

- query ：可选，使用查询操作符指定查询条件
- fields ：可选，使用投影操作符指定返回的键。查询时返回文档中所有键值，只需省略该参数即可（默认省略）。

##### 删除数据

```
db.user.remove({age:25})		#删除所有符合条件的数据
db.user.remove({age:22},true)	#删除1条数据
db.user.remove					#删除所有数据

#为了简化操作，官方推荐使用deleteOne()与deleteMany()进行删除数据操作。
db.user.deleteOne({id:1})
db.user.deleteMany({})  #删除所有数据

```

参考说明：

```
db.collection.remove(
   <query>,
   {
	 justOne: <boolean>,
	 writeConcern: <document>
   }
)
```

- query :（可选）删除的文档的条件。
- justOne : （可选）如果设为 true 或 1，则只删除一个文档，如果不设置该参数，或使用默认值 false，则删除所有匹配条件的文档。
- writeConcern :（可选）抛出异常的级别。

# 五.MongoDB可视化工具
在使用MongoDB过程中，如果单单依靠命令行操作MongoDB数据库，效率不高而且查看不方便。因此我们可以借助可视化管理工具来创建数据库、管理集合和文档、运行临时查询、评估和优化查询、性能图表、构建地理查询等操作，提升工作效率。

### COMPASS（免费）

MongoDB 官方自己推出的 GUI 可视化管理工具，功能有限。免费简洁，不支持 SQL 查询，支持性能监控。适用于 Windows，macOS 和 Linux 系统。

[官网下载地址](https://www.mongodb.com/zh-cn/products/compass)

### Robo3T（免费）

Robo 3T 前身是 Robomongo，后被 3T 公司收购，是一款免费开源的 GUI 管理工具。支持 MongoDB 4.0+，轻量级 GUI，支持语法填充等等。适用于 Windows，macOS 和 Linux 系统。
[官网下载地址](https://robomongo.org/)

### Studio3T

超过 100，000 的开发人员和数据库管理员使用 Studio 3T 作为 MongoDB GUI 的首选。Studio 3T 属于收费工具，30 天的免费试用期，Studio 3T 具有更多更强大的功能并提供企业支持服务，支持副本集、独立主机和分片集群连接，支持导入导出，SQL
查询，语法填充，支持 MongoDB 4.0+ 等等。适用于 Windows，macOS 和 Linux。
[官网下载地址](https://studio3t.com/download/)

### Navicat for MongoDB

数据库管理工具，支持多种数据库的集成，已集成 MongoDB 类型，属于付费型管理工具。好处是用会了一个 DB 版的 Navicat，所有 DB 版都会很顺手，维持一套操作习惯。
[官网下载地址](http://www.navicat.com.cn/download/navicat-for-mongodb)

