---
title: Web服务器和应用服务器的区别与联系
date: 2022-04-10
categories: 
  - 服务器
---

# Web服务器与应用服务器
### Web服务器简介
##### 什么是Web服务器
WEB即超文本（hypertext）、超媒体（hypermedia）和超文本传输协议（HTTP），获取这些静态资源实际上是在请求服务器上的文件。这些文件都一直保存在服务器的磁盘上一个固定的文件路径，并生成一个对应的地址。HTML页面就是WEB的数据元素，处理这些数据元素的应用软件就叫WEB服务器，WEB服务器常与客户端打交道，它要处理的主要信息有：session、request、response、HTML、JS、CS等。

##### 常用的Web服务器
* Nginx
* Apache
* Jetty （也支持动态页面处理，但主要还是静态页面）
* IIS

### 应用服务器简介
##### 什么是应用服务器
应用服务器是为客户端提供对业务逻辑的访问这种服务器，根据客户端的请求会将数据转化为动态内容，一般还需要数据库的支持，应用服务器的搭建很多时候依赖于应用程序的开发语言，各种编程语言生态下对应不同的软件， 比如使用Java语言开发的项目通常选择 Tomcat或者接jboss来作为程序运行的应用服务器，而使用python语言开发Web应用，一般会选用Django等python框架下的软件，来作为它的应用服务器。

#####常用的应用服务器
* Tomcat
* Jboss
* WebLogic

>有的应用服务器也提供http服务，如Tomcat，所以可以说，Tomcat是Web服务器也是应用服务器。

### Web服务器和应用服务器的区别及联系
WEB服务器一般是通用的，而应用服务器一般是专用的，如Tomcat只处理JAVA应用程序而不能处理ASPX或PHP。而Apache是一个WEB服务器（HTTP服务器），它的数据源可以是配置在Tomcat中的JAVA应用，也可以是ASPX应用。 Web服务器只负责处理HTTP协议，只能发送静态页面的内容。而JSP，ASP，PHP等动态内容需要通过CGI、FastCGI、ISAPI等接口交给其他程序去处理，这个其他程序就是应用服务器。

* Web服务器只处理静态html。走http协议。客户端为浏览器。
* 应用服务器主要是控制客户端和服务端的业务逻辑，通信格式不限制（如json、html或任何文件），也是走http协议。经常用来处理动态内容。客户端可以是浏览器，也可以是其他应用服务器，手机app等。Web服务器可以算是应用服务器的一个子集。

>现在很多Web服务器通过加载插件也支持动态页面的处理，应用服务器本身也支持静态页面的处理。两者有很多重合的地方，现在也有人叫Web应用服务器。随着Web技术的火热，两者很多功能融合了，但是概念上还是有差异。

这里通过分析Nginx(Web服务器)和Tomcat(应用服务器)来展示二者之间的区别:

**Tomcat的功能职责** ：
Tomcat运行在JVM之上，它和HTTP服务器一样，绑定IP地址并监听TCP端口，同时还包含以下指责：
- 管理Servlet程序的生命周期。
- 将URL映射到指定的Servlet进行处理。
- 与Servlet程序合作处理HTTP请求——根据HTTP请求生成HttpServletResponse对象并传递给Servlet进行处理，将Servlet中的HttpServletResponse对象生成的内容返回给浏览器。

**Nginx的功能职责：**
- 动静态资源分离——运用Nginx的反向代理功能分发请求：所有动态资源的请求交给Tomcat，而静态资源的请求（例如图片、视频、CSS、JavaScript文件等）则直接由Nginx返回到浏览器，这样能大大减轻Tomcat的压力。
- 负载均衡，当业务压力增大时，可能一个Tomcat的实例不足以处理，那么这时可以启动多个Tomcat实例进行水平扩展，而Nginx的负载均衡功能可以把请求通过算法分发到各个不同的实例进行处理。

**两者的区别：**
Apache/Nginx叫做Http server ;而Tomcat 则是一个application Server，或者说是一个servlet/jsp应用容器（python无法直接运行在Tomcat上，java可以） 一个 HTTP Server 关心的是 HTTP 协议层面的传输和访问控制，所以在 Apache/Nginx 上你可以看到代理、负载均衡等功能。客户端通过 HTTP Server 访问服务器上存储的资源（HTML 文件、图片文件等等）。
而应用服务器，则是一个应用执行的容器。它首先需要支持开发语言的 Runtime（对于 Tomcat 来说，就是 Java），保证应用能够在应用服务器上正常运行。其次，需要支持应用相关的规范，例如类库、安全方面的特性。对于 Tomcat 来说，就是需要提供 JSP/Sevlet 运行需要的标准类库、Interface 等。为了方便，应用服务器往往也会集成 HTTP Server 的功能，但是不如专业的 HTTP Server 那么强大，所以应用服务器往往是运行在 HTTP Server 的背后，执行应用，将动态的内容转化为静态的内容之后，通过 HTTP Server 分发到客户端。

### Web服务器与应用服务器的选择
- 如果完全服务静态页面选择Web服务器（如一个静态博客网站） 
- 如果有动态页面处理可以选择应用服务器，或者结合使用。大一点的网站推荐两者都使用，前后端分离，静态页面交给Web服务器，业务逻辑使用应用服务器。（如一个网上购物系统）

### Web服务器选择Apache还是Nginx
Apache HTTP Server(简称Apache)是世界使用排名第一的Web服务器软件，音译为阿帕奇，是Apache软件基金会的一个开放源码Web服务器，可以运行几乎所有的计算机平台，其次开放的API接口，任何组织和个人都可以在它上面扩展和增加各种需要功能，
达到为自己量身定制的功能。再次是因为推出的时间比较久，所有相关文档很齐全，甚至在windows平台很多爱好者都为它开发了各种图形界面，因为如此它迅速占领了70%的Web服务器市场。
Nginx，Nginx ("engine x") 是一个高性能的 HTTP 和 反向代理服务器，也是一个 IMAP/POP3/SMTP 代理服务器。
Nginx 是由 Igor Sysoev 为俄罗斯访问量第二的 Rambler.ru 站点开发的。其次它和Apache一样是开源的，BSD-like 协议下发行。它最强劲也最具有竞争性为其高性能和反向代理，这两项在该领域独领风骚。
在互联网初期，网站大小不是很大，访问量都很轻量，一个网站的访问量一天最多就几万IP，这个时候Apache完全可以满足需要，人们更多的是为它开发各种模块，像重写模块，访问控制列表，缓存模块等等。但是随着互联网的飞速发展，网站我访问量以指数增长，大型网站的除了加大硬件投入外，典型的Web服务器Apache这时候也力不从心了，于是Nginx开始崛起，最初的设计是俄罗斯工程师为大型网站解决高并发设计的。所以注定了高并发是它永恒的优点。再次就是反向代理，现在大型网站分工详细，哪些服务器处理数据流，哪些处理静态文件，这些谁指挥，一般都是用Nginx反向代理到内网服务器，这样就起到了负载均衡分流的作用。再次Nginx高度模块化的设计，编写模块相对简单。
而Apache比Nginx又有什么优势呢，很多中小型网站都在用Apache，非常重要的原因是他出现时间较长，稳定，文档丰富，再次在重写方面相对Nginx更强大，模块超多，基本只要你能想到的，就有人开发过。
面对这些优缺点，该如何取舍呢?尽管Nginx正在一步步取代Apache，市场份额也在不断增加，但是做为一个网站管理员，还是需要从如下几个方面作为出发点来选择适合自身的Web服务器。
1. 网站并发。如果是中小型网站，建议选用Apache;如果大型并发，而且需要反向代理，选择Nginx那是正确的选择。
2. 如果需要大量用到重写模块，建议选用Apache。
2. 系统资源有限，但是自身技术很强大，建议用Nginx，因为Nginx对系统资源暂用极小，同资源下比Apache高了差不多10倍之多。

# Docker安装Apache服务器
### 拉取镜像
```
docker pull httpd
```

### 创建容器
```
docker run -di --name httpd -p 9000:80 httpd
```
* -p 9000:80 :将容器的9000端口映射到主机的80端口

### 容器文件映射到宿主机
1. 创建目录，用于映射目录:
```
mkdir -p /root/dcoker/apache/www 
mkdir -p /root/dcoker/apache/logs 
mkdir -p /root/dcoker/apache/conf
```
* www目录将映射为apache容器配置的应用程序目录
* logs目录将映射为apache容器的日志目录
* conf目录里的配置文件将映射为apache容器的配置文件

2. 拷贝容器内Apache 默认配置文件到本地当前目录下的 conf 目录，容器 ID 可以通过 docker ps 查看

```
docker cp 容器ID:/usr/local/apache2/conf/httpd.conf /root/dcoker/apache/conf
```

3. 删除临时容器

```
# 关闭该容器
docker stop httpd
# 删除该容器
docker rm httpd
```

4. 创建容器

```
docker run -p 9000:80 --privileged=true --name zhuzq-apache -v /root/dcoker/apache/www/:/usr/local/apache2/htdocs/ -v /root/dcoker/apache/conf/httpd.conf:/usr/local/apache2/conf/httpd.conf -v /root/dcoker/apache/logs:/usr/local/apache2/logs/ -d httpd
```

**命令说明：**

* -p 9000:80 :将容器的9000端口映射到主机的80端口
* -v /root/dcoker/apache/www/:/usr/local/apache2/htdocs/ :将主机中当前目录下的www目录挂载到容器的/usr/local/apache2/htdocs/
* -v /root/dcoker/apache/conf/httpd.conf:/usr/local/apache2/conf/httpd.conf :将主机中当前目录下的conf/httpd.conf文件挂载到容器的/usr/local/apache2/conf/httpd.conf
* -v /root/dcoker/apache/logs/:/usr/local/apache2/logs/ :将主机中当前目录下的logs目录挂载到容器的/usr/local/apache2/logs/
* --name zhuzq-apache, zhuzq-apache为容器名称

# docker安装nginx
### 搜索nginx镜像
获取nginx镜像列表
```
docker search nginx
```
### 拉取nginx镜像
拉取nginx镜像到本地(注：默认选取官方最新镜像)，其它版本可以去[DockerHub](https://hub.docker.com/)查询
```
docker pull nginx
```
### 运行nginx镜像

```
docker run --name nginx -p 7000:80  -d nginx
```
* –name 指定容器名称，此处我指定的是nginx
* -p 指定主机与容器内部的端口号映射关系，格式 -p [宿主机端口号]：[容器内部端口]，此处我使用了主机7000端口，映射容器80端口
* -d 指定容器以守护进程方式在后台运行
### 挂载配置文件到主机
由于我们是通过Docker将nginx安装在容器中,因此如果要对nginx的配置进行修改,需要进入到docker容器中去进行。另外还可以将docker容器的文件目录挂在到宿主机中,就可以在宿主机中进行修改了。
#### 进入Nginx容器修改配置
1. 执行命令进入到nginx容器内部，
```
docker exec -it nginx容器ID /bin/bash
```          
``nginx -t ``查看nginx配置文件的位置

2. 修改配置文件
- nginx配置文件都在/etc/nginx目录下。
- 默认首页html文件目录为/usr/share/nginx/html。
- 日志文件位于/var/log/nginx。

>每次都进入到nginx容器内部修改。适合改动少，简单使用的情况
#### 将nginx容器内部配置文件挂载到主机
1. 宿主机创建Nginx配置文件夹
```
# 创建挂载目录
mkdir -p /usr/nginx/conf
mkdir -p /var/log/nginx
mkdir -p /usr/share/nginx/html
```
2. 容器中的nginx.conf文件和conf.d文件夹复制到宿主机

```
# 生成容器(上一步生成了则不用再生成容器了)
docker run --name nginx -p 7000:80 -d nginx
# 将容器nginx.conf文件复制到宿主机
docker cp nginx:/etc/nginx/nginx.conf /usr/nginx/conf/nginx.conf
# 将容器conf.d文件夹下内容复制到宿主机
docker cp nginx:/etc/nginx/conf.d /usr/nginx/conf/conf.d
# 将容器中的html文件夹复制到宿主机
docker cp nginx:/usr/share/nginx/html /usr/share/nginx
```
3. 停止并删除旧的容器
```
# 直接执行docker rm nginx或者以容器id方式关闭容器
# 找到nginx对应的容器id
docker ps -a
# 关闭该容器
docker stop nginx
# 删除该容器
docker rm nginx

# 或者删除正在运行的nginx容器
docker rm -f nginx
```
4. 创建新的Nginx容器并运行
```
docker run \
-p 7000:80 \
--name nginx \
-v /usr/nginx/conf/nginx.conf:/etc/nginx/nginx.conf \
-v /usr/nginx/conf/conf.d:/etc/nginx/conf.d \
-v /var/log/nginx:/var/log/nginx \
-v /usr/share/nginx/html:/usr/share/nginx/html \
-d nginx:latest
```
单行模式:
```
docker run -p 7000:80 --name nginx -v /usr/nginx/conf/nginx.conf:/etc/nginx/nginx.conf -v /usr/nginx/conf/conf.d:/etc/nginx/conf.d -v /var/log/nginx:/var/log/nginx -v /usr/share/nginx/html:/usr/share/nginx/html -d nginx:latest
```
参数解释:
* –name nginx                                          :启动容器的名字
* -d                                                   :后台运行
* -p 9002:80                                           :将容器的 9002(后面那个) 端口映射到主机的 80(前面那个) 端口      |
* -v /usr/nginx/conf/nginx.conf:/etc/nginx/nginx.conf :挂载nginx.conf配置文件
* -v /usr/nginx/conf/conf.d:/etc/nginx/conf.d         :挂载nginx配置文件
* -v /var/log/nginx:/var/log/nginx                    :挂载nginx日志文件
* -v /usr/share/nginx/html:/usr/share/nginx/html            :挂载nginx内容
* nginx:latest                                         :本地运行的版本

>将nginx容器内部配置文件挂载到主机，之后就可以在主机对应目录修改即可,适合频繁修改，复杂使用的情况。

# Docker安装Tomcat
### 下载和安装Tomcat容器

1. 拉取Tomcat镜像

```
docker pull tomcat
```

2. 启动Tomcat容器

```
docker run --name tomcat -d -p 8080:8080 tomcat
```

> -d 表示后台运行，并返回后台容器，
> -p 表示端口号，前一个8080是指我们访问tomcat时的端口号，
> 后一个8080是tomcat启动的一个容器在[docker](https://so.csdn.net/so/search?q=docker&spm=1001.2101.3001.7020)中运行的端口号， 指定端口号为了更明确的访问tomcat。

### 解决404问题

当Tomcat版本过高时，根据IP地址和端口号访问可能会出现404，是因为webapps文件夹下内容为空，内容都在webapps.dist 目录下，解决办法如下：

1. 进入Tomcat容器

```
docker exec -it tomcat /bin/bash
```

2. 将webapps.dist下的内容全部移动到webapps中

```
rm -r webapps
mv webapps.dist webapps
exit
```

3. 再次访问页面成功。

### 容器文件映射到本地目录（挂载）

拷贝容器内 Tomcat 配置文件和日志到本地准备映射

```
mkdir tomcat
docker cp tomcat:/usr/local/tomcat/conf /root/tomcat/conf
docker cp tomcat:/usr/local/tomcat/logs /root/tomcat/logs
docker cp tomcat:/usr/local/tomcat/webapps /root/tomcat/webapps
```

停止tomcat，并删除容器

```
docker stop tomcat
docker rm tomcat
```

创建并运行tomcat容器

```
docker run -d -p 8080:8080 --name tomcat -v /root/tomcat/webapps:/usr/local/tomcat/webapps -v /root/tomcat/conf:/usr/local/tomcat/conf -v /root/tomcat/logs:/usr/local/tomcat/logs tomcat
```

参数解释:
* --name tomcat                                        :启动容器的名字
* -d                                                   :后台运行
* -p 8081:8080                                         :将容器的 8080 端口映射到主机的 8081端口
* -v /root/tomcat/webapps:/usr/local/tomcat/webapps    :挂载容器webapps目录到宿主机
* -v /root/tomcat/conf:/usr/local/tomcat/conf          :挂载容器conf目录到宿主机
* -v /root/tomcat/webapps:/usr/local/tomcat/webapps    :挂载容器webapps目录到宿主机
* tomcat                                               :本地运行的版本

# 参考资料
[Nginx和Apache和Tomcat的区别及优缺点](https://blog.csdn.net/weixin_44221613/article/details/88410701)
[tomcat、nginx、apache、tengine都是什么，及其作用](https://www.cnblogs.com/isme-zjh/p/11381456.html)
[一文看懂Tomcat、Nginx和Apache的区别](https://blog.csdn.net/g6U8W7p06dCO99fQ3/article/details/118560517)
[Apache、Nginx、Tomcat的区别](https://blog.csdn.net/focus_lyh/article/details/122463976)
[一文看懂web服务器、应用服务器、web容器、反向代理服务器区别与联系](https://blog.51cto.com/mingongge/5181928)

