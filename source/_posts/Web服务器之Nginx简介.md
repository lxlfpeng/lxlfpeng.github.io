---
title: Web服务器之Nginx简介
---

# 一.Nginx简介
Nginx (engine x) 是一个高性能的Web和反向代理服务器，同时也是一个 IMAP/POP3/SMTP 代理服器。Nginx处理高并发能力是十分强大的，能经受高负载的考验。而且支持热部署，几乎可以做到 7 * 24 小时不间断运行，即使运行几个月也不需要重新启动，还能在不间断服务的情况下对软件版本进行热更新 。性能是 Nginx 最重要的考量，其占用内存少、并发能力强、能支持高达 5w 个并发连接数，最重要的是， Nginx 是免费的并可以商业化，配置使用也比较简单。
[详细介绍](https://lnmp.org/nginx.html)
[nginx官网](https://nginx.org/)

# 二.Nginx的功能
## 正向代理
正向代理是客户端与正向代理客户端在同一局域网，客户端发出请求，正向代理 替代客户端向服务器发出请求。服务器不知道谁是真正的客户端，正向代理隐藏了真实的请求客户端。正向代理一般是客户端架设的，比如在自己的机器上安装一个代理软件。
![](/images/d467017682205e0ec6e524b4af6d4051.webp)

正向代理的用途：
1. 可以做缓存，加速访问资源
2. 对客户端访问授权，上网进行认证
3. 代理可以记录用户访问记录（上网行为管理），对外隐藏用户信息

## 反向代理
反向代理服务器与反向代理在同一个局域网，客服端发出请求，反向代理接收请求 ，反向代理服务器会把我们的请求分转发到真实提供服务的各台服务器中去。反向代理一般是服务器架设的，比如在自己的机器集群中部署一个反向代理服务器。反向代理客户端对代理是无感知的，因为客户端不需要任何配置就可以访问，我们只需要将请求发送到反向代理服务器，由反向代理服务器去选择目标服务器获取数据后，在返回给客户端，此时反向代理服务器和目标服务器对外就是一个服务器，暴露的是代理服务器地址，隐藏了真实服务器 IP 地址。
![](/images/eed8a627d466bbeaec08a3508369592b.webp)

## 负载均衡
当一台服务器的访问量越大时，服务器所承受的压力也就越大，超出自身所指定的访问压力就会崩掉，避免发生此类事情的发生，因此也就有了负载均衡来分担服务器的压力。 我们有几十台、几百台甚至更多服务器，将这些服务器组成一个服务器集群，当客户端访问某台设备的数据时，首先发送的请求先到一台中间服务器，并通过中间服务器在服务器集群中平均分摊到其他服务器中，因此，当用户每次所发送的请求都将会保证服务器集群中的设备均与平摊，以此来分担服务器的压力，从而保持服务器集群的整理性能最优，避免出现有崩溃的现象。利用Nginx的反向代理功能可以很好的实现中间服务器的功能。

![](/images/1d3e71ca7361737d041732f0c526b6ac.webp)

## 动静分离
为了加快网站的解析速度，可以把动态页面和静态页面由不同的服务器来解析，加快解析速度。降低原来单个服务器的压力。
![](/images/2adbb994d4917bd0ae470f86f333f634.webp)
例如:将动态请求与静态请求分离开，动态请求经过Nginx访问tomcat服务器，Nginx可以直接做静态请求服务器，静态请求直接由Nginx处理，动态请求由tomcat处理。

## Nginx的功能总结
1. 缓存静态文件(html，css，js) ：实现完全的前后端分离，且它处理静态文件的效率是应用服务器的几倍。
2. 反向代理: 当真实服务器不能被直接访问到时，Nginx可作为反向代理服务，用于中间做转发。
3. web缓存: 可以对不同的文件做不同的缓存处理，配置灵活，并且支持FastCGI*Cache，主要用于对FastCGI的动态程序进行缓存。配合着第三方的ngx*cache_purge，对制定的URL缓存内容可以的进行增删管理。
4. 负载均衡: 更大程度提高服务器的使用效率。
5. 邮件代理服务器: 实现轻松扩展邮件服务器的数量、根据不同的规则选择邮件服务器，例如，根据客户的IP地址选择最近的服务器，实现邮件服务器的负载均衡。

# 三.Docker安装Nginx
### 搜索Nginx镜像
获取Nginx镜像列表
```
docker search nginx
```
### 拉取Nginx镜像
拉取Nginx镜像到本地(注：默认选取官方最新镜像)，其它版本可以去[DockerHub](https://hub.docker.com/)查询
```
docker pull nginx
```
### 运行Nginx镜像

```
docker run --name nginx -p 7000:80  -d nginx
```
* –name 指定容器名称，此处我指定的是Nginx
* -p 指定主机与容器内部的端口号映射关系，格式 -p [宿主机端口号]：[容器内部端口]，此处我使用了主机7000端口，映射容器80端口
* -d 指定容器以守护进程方式在后台运行
### 访问 Nginx
然后浏览器访问服务器ip，上一步映射的主机端口是7000，因此访问该端口即可。
### 挂载配置文件到主机
由于我们是通过Docker将Nginx安装在容器中，因此如果要对Nginx的配置进行修改，需要进入到docker容器中去进行。另外还可以将docker容器的文件目录挂在到宿主机中，就可以在宿主机中进行修改了。
#### 进入Nginx容器修改配置
1. 执行命令进入到Nginx容器内部，
```
docker exec -it nginx容器ID /bin/bash
```
``nginx -t ``查看nginx配置文件的位置

2. 修改配置文件
- nginx配置文件都在/etc/nginx目录下。
- 默认首页html文件目录为/usr/share/nginx/html。
- 日志文件位于/var/log/nginx。

>每次都进入到Nginx容器内部修改。适合改动少，简单使用的情况
#### 将Nginx容器内部配置文件挂载到主机
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

>将nginx容器内部配置文件挂载到主机，之后就可以在主机对应目录修改即可，适合频繁修改，复杂使用的情况。

# 四.Nginx配置文件
Nginx本身作为一个完成度非常高的负载均衡框架，和很多成熟的开源框架一样，大多数功能都可以通过修改配置文件来完成，使用者只需要简单修改一下nginx配置文件，便可以非常轻松的实现比如反向代理，负载均衡这些常用的功能。Nginx配置文件一般位于Nginx安装目录下的conf目录下。整个文件以block形式组合而成，每一个block都使用"{}"大括号来表示。block中可以嵌套其他block层级。Nginx配置文件分为三大块：全局块，events块，http块，Nginx的主配置文件是nginx.conf，这个配置文件一共由三部分组成，分别为全局块、events块和http块。在http块中，又包含http全局块、多个server块。每个server块中，可以包含server全局块和多个location块。在同一配置块中嵌套的配置块，各个之间不存在次序关系。
默认的 nginx 主配置文件 nginx.conf 内容文件结构如下：
```
#全局块
#user  nobody;
worker_processes  1;

#event块
events {
    worker_connections  1024;
}

#http块
http {
    #http全局块
    include             mime.types;
    default_type        application/octet-stream;
    sendfile            on;
    keepalive_timeout   65;
    #server块
    server {
        #server全局块
        listen       8000;
        server_name  localhost;
        #location块
        location / {
            root   html;
            index  index.html index.htm;
        }
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }
    #这边可以有多个server块
    server {
      ...
    }
}
```

### 全局块
全局块是默认配置文件从开始到events块之间的一部分内容，主要设置一些影响Nginx服务器整体运行的配置指令，因此，这些指令的作用域是Nginx服务器全局。 通常包括配置运行Nginx服务器的用（组）、允许生成的worker process数、Nginx进程PID存放路径、日志的存放路径和类型以及配置文件引入等。在全局块中配置的都是影响Nginx整体运行的配置。比如说：worker(工作进程)的数量，错误日志的位置等
```
user  nobody;
worker_processes  1;
#error_log  logs/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;
#pid        logs/nginx.pid;

events {
    use epoll;
    worker_connections  1024;
}
```
- user  :指定nginx的工作进程的用户及用户组，默认是nobody用户。
- worker_processes   :指定工作进程的个数，默认是1个。具体可以根据服务器cpu数量进行设置， 比如cpu有4个，可以设置为4。如果不知道cpu的数量，可以设置为auto。 nginx会自动判断服务器的cpu个数，并设置相应的进程数。
- error_log   :设置nginx的错误日志路径，并设置相应的输出级别。 如果编译时没有指定编译调试模块，那么 info就是最详细的输出模式了。 如果有编译debug模块，那么debug时最为详细的输出模式。这里设置为默认就好了。
- pid     :指定nginx进程pid的文件路径。
- events  :这个指令块用来设置工作进程的工作模式以及每个进程的连接上限。
- use :用来指定nginx的工作模式，默认是epoll，除了epoll，还有select，poll。
- worker_connections      :定义每个工作进程的最大连接数，默认是1024。

### http块
http块是Nginx服务器配置中的重要部分，代理、缓存和日志定义等绝大多数的功能和第三方模块的配置都可以放在这个模块中。 前面已经提到，http块中可以包含自己的全局块，也可以包含server块，server块中又可以进一步包含location块，使用“http全局块”来表示http中自己的全局块，即http块中不包含在server块中的部分。 可以在http全局块中配置的指令包括文件引入、MIME-Type定义、日志自定义、是否使用sendfile传输文件、连接超时时间、单连接请求数上限等。

```
http {
    include       mime.types;
    default_type  application/octet-stream;
    charset utf-8; 
    #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
    #                  '$status $body_bytes_sent "$http_referer" '
    #                  '"$http_user_agent" "$http_x_forwarded_for"';
    #access_log  logs/access.log  main;
    Sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    #keepalive_timeout  0;
    keepalive_timeout  65;
    keepalive_requests 100; 
    #gzip  on;
    server {
        ...
        location {
            root html;
            ...
        }
    }

}
```


- include    mime.types;  :定义数据类型 如果用户请求lutixia.png，服务器上有lutixia.png这个文件，后缀名是png； 根据mime.types，这个文件的数据类型应该是image/png； 将Content-Type的值设置为image/png，然后发送给客户端
- default_type        :设定默认类型为二进制流，也就是当文件类型未定义时使用这种方式， 例如在没有配置PHP环境时，Nginx是不予解析的， 此时，用浏览器访问PHP文件就会变成下载。
- charset utf-8;   	:解决中文字体乱码
- log_format      	:定义日志文件格式，并默认取名为main，可以自定义该名字。 也可以通过添加，删除变量来自定义日志文件的格式。
- access_log      	:定义访问日志的存放路径，并且通过引用log_format所定义的main名称设置其输出格式。
- sendfile   on 		:用于开启高效文件传输模式。直接将数据包封装在内核缓冲区，然后返给客户，将tcp_nopush和tcp_nodelay两个指令设置为on用于防止网络阻塞；
- keepalive_timeout   65    :设置与客户端绘画保持的超时时间。在超过这个时间之后，服务器会关闭该连接，客户端再次发起请求，则需要再次进行三次握手。
- keepalive_requests 100   :设置nginx在会话保持状态下最多能处理的请求数，到达请求数，即使还在会话保持的时间内，也需要重新连接。 提示：在通过浏览器访问站点时，可以在Linux服务器使用该命令：netstat -ntlpa |grep 80  查看链接状态
- gzip  on        						:开启压缩功能，减少文件传输大小，节省带宽。
- gzip_min_length 1k; 					:最小文件压缩，1k起压。
- gzip_types      text/plain text/xml;    :压缩文件类型（不限于这两个，还可以设置压缩js等）
- gzip_comp_level   3;   					:压缩级别，默认是1。

### server块
server块和“虚拟主机”的概念有密切联系。 虚拟主机，又称虚拟服务器、主机空间或是网页空间，它是一种技术。该技术是为了节省互联网服务器硬件成本而出现的。这里的“主机”或“空间”是由实体的服务器延伸而来，硬件系统可以基于服务器群，或者单个服务器等。虚拟主机技术主要应用于HTTP、FTP及EMAIL等多项服务，将一台服务器的某项或者全部服务内容逻辑划分为多个服务单位，对外表现为多个服务器，从而充分利用服务器硬件资源。从用户角度来看，一台虚拟主机和一台独立的硬件主机是完全一样的。在使用Nginx服务器提供Web服务时，利用虚拟主机的技术就可以避免为每一个要运行的网站提供单独的Nginx服务器，也无需为每个网站对应运行一组Nginx进程。虚拟主机技术使得Nginx服务器可以在同一台服务器上只运行一组Nginx进程，就可以运行多个网站。在前面提到过，每一个http块都可以包含多个server块，而每个server块就相当于一台虚拟主机，它内部可有多台主机联合提供服务，一起对外提供在逻辑上关系密切的一组服务（或网站）。和http块相同，server块也可以包含自己的全局块，同时可以包含多个location块。在server全局块中，最常见的两个配置项是本虚拟主机的监听配置和本虚拟主机的名称或IP配置。

```js
server {
        listen       80;
        server_name  localhost;
        #charset koi8-r;
        #access_log  logs/host.access.log  main;
         index  index.html index.htm;
        location /
         {
            root   html;
            ...
        }
        #error_page  404              /404.html;
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
        #location ~ \.php$ {
                ...
        #}
        #location ~ /\.ht {
        #    deny  all;
        #}
    }
```

- server      		:用来定义虚拟主机。
- listen      		:设置监听端口，默认为80端口
- server_name     	:域名，多个域名通过逗号或者空格隔开
- Charset     		:设置网页的默认编码格式
- access_log     		:指定该虚拟主机的独立访问日志，会覆盖前面的全局配置。
- index        		:设置默认的索引文件
- location       		:定义请求匹配规则。
- error_page      	:定义访问错误返回的页面，凡是状态码是500 502 503 504 都会返回这个页面。


** location指令块：**

```
#location ~ \.php$ {
        #    root           html;
        #    fastcgi_pass   127.0.0.1:9000;
        #    fastcgi_index  index.php;
        #    fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
        #    include        fastcgi_params;
        #}

        # deny access to .htaccess files, if Apache's document root
        # concurs with nginx's one
        #
        #location ~ /\.ht {
        #    deny  all;
        #}
```
- location ~ \.php$     	:凡是以php结尾文件，都会匹配到这条规则。
- root        			:php文件存放的目录
- fastcgi_pass        	:指定php-fpm进程管理的ip端口或者unix套接字
- fastcgi_index   		:指定php脚本目录下的索引文件
- fastcgi_param       	:指定传递给FastCGI服务器的参数
- location ~ /\.ht        :凡是请求类似.ht资源，都拒绝。

### 配置文件分析
Nginx 安装完成之后会在 /usr/local/nginx/conf/ 目录下生成一个配置文件 nginx.conf，也就是默认使用的配置文件。内容如下(注意配置文件中"#"用于注释):

```
# user 指定运行 nginx 的用户和组（第一个参数为用户第二个为组，这里只有用户）
#user  nobody;
# 指定工作进程数（一般设置为CPU核数）
worker_processes  1;   

# 指定错误日志为 logs/ 目录下的 error.log 文件
#error_log  logs/error.log;
# 指定错误日志，并指定写入格式为 notice
#error_log  logs/error.log  notice;
# 指定错误日志，并指定写入格式为 info  
#error_log  logs/error.log  info;

# 指定 pid 文件（存放主进程 pid 号）
#pid        logs/nginx.pid;

# nginx 连接配置模块
events {
    # 指定每个工作进程最大连接数为 1024
    worker_connections  1024;
}

# http 配置模块
http {
    # 通过 include 加载 mime.types 文件，里面的 types {} 模块将文件扩展名映射到响应的 MIME 类型
    include       mime.types;
    # 定义响应的默认 MIME 类型
    default_type  application/octet-stream;

    # 写入格式 main 的内容格式如下
    #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
    #                  '$status $body_bytes_sent "$http_referer" '
    #                  '"$http_user_agent" "$http_x_forwarded_for"';

    # 指定访问日志和写入格式为 main
    #access_log  logs/access.log  main;

    # 启用或者禁用 sendfile()
    sendfile        on;
    # 启用或者禁用使用套接字选项（仅在 sendfile 使用时使用）
    #tcp_nopush     on;

    # 0 值禁用保持活动的客户端连接
    #keepalive_timeout  0;
    # 65 s 超时
    keepalive_timeout  65;

    # 启用或者禁用 gzip
    #gzip  on;

    # 虚拟主机配置模块
    server {
        # 监听 80 端口
        listen       80;
        # 监听域名为 localhost
        server_name  localhost;
        # 将指定的 charset 添加到 “Content-Type” 响应头字段。如果此charset与source_charset指令中指定的charset不同，则执行转换。
        #charset koi8-r;

        # 指定该虚拟主机的访问日志
        #access_log  logs/host.access.log  main;

        # 将特定的文件或目录重新定位，如 php 文件，image 目录等
        location / {
            # 设置请求的根目录
            root   html;
            # 定义索引，按顺序匹配
            index  index.html index.htm;
        }

        # 定义显示 404 错误的 uri
        #error_page  404              /404.html;

        # redirect server error pages to the static page /50x.html
        #
        error_page   500 502 503 504  /50x.html;
        # location 精准匹配 '/50x.html'
        location = /50x.html {
            root   html;
        }

        # proxy the PHP scripts to Apache listening on 127.0.0.1:80
        # 正则表达式匹配 php 文件
        #location ~ \.php$ {
            # 设置代理服务器的协议和地址，以及应该映射位置的可选URI。作为协议，可以指定“http”或“https”。该地址可以指定为一个域名或IP地址，以及一个可选端口
        #    proxy_pass   http://127.0.0.1;
        #}

        # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
        #
        #location ~ \.php$ {
        #    root           html;
             # 设置 FastCGI 服务器的地址。地址可以指定为一个域名或 IP 地址，以及一个端口
        #    fastcgi_pass   127.0.0.1:9000;
             # 设置将在以斜杠结尾的URI之后追加的文件名，
        #    fastcgi_index  index.php;
             # 设置一个应该传递给FastCGI服务器的参数。
        #    fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
             # 加载 conf/fastcgi_params 文件
        #    include        fastcgi_params;
        #}

        # deny access to .htaccess files, if Apache's document root
        # concurs with nginx's one
        #
        #location ~ /\.ht {
        #    deny  all;
        #}
    }


    # another virtual host using mix of IP-, name-, and port-based configuration
    #
    #server {
    #    listen       8000;
    #    listen       somename:8080;
    #    server_name  somename  alias  another.alias;

    #    location / {
    #        root   html;
    #        index  index.html index.htm;
    #    }
    #}


    # HTTPS server
    #
    # ssl 配置，要启用 ssl 模块需要在编译 nginx 时加上 --with-http_ssl_module 参数
    #server {
    #    listen       443 ssl;
    #    server_name  localhost;

    #    ssl_certificate      cert.pem;
    #    ssl_certificate_key  cert.key;

    #    ssl_session_cache    shared:SSL:1m;
    #    ssl_session_timeout  5m;

    #    ssl_ciphers  HIGH:!aNULL:!MD5;
    #    ssl_prefer_server_ciphers  on;

    #    location / {
    #        root   html;
    #        index  index.html index.htm;
    #    }
    #}

}
```

# 参考资料
[超详细的Nginx入门教程](https://blog.csdn.net/m0_64830133/article/details/123150157)
[Nginx超详细入门教程，收藏慢慢看](https://juejin.cn/post/6924534276323016711)
[Nginx从入门到实践，看这一篇就够了！](https://juejin.cn/post/6959805590897950727)
[来了，来了，你们要的Nginx教程来了](https://segmentfault.com/a/1190000023328201)
[写给后端的Nginx初级入门教程:实战篇](https://juejin.cn/post/6844903983622914062)
[从原理到实战，彻底搞懂Nginx（高级篇） - 掘金](https://juejin.cn/post/6844904046789132301)
[前端必备知识之Nginx](https://juejin.cn/post/7108394145068089374)
[作为一名前端，该如何理解Nginx？](https://juejin.cn/post/7082655545491980301)