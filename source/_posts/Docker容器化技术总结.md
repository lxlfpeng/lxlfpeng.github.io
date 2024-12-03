---
title: Docker容器化技术总结
date: 2021-01-05 
categories: 
  - Docker容器
---

# 一.Docker基础
- image：镜像，是一个只读模版，用来创建容器。
- container: 容器，是一个可运行的镜像实例。
- Dockerfile: 镜像构建的模版，描述镜像构建的步骤。
通过镜像来创建容器，程序就跑在容器中。并且一个镜像可以随意创建N个容器，各个容器间相互隔离。
  
# 二.Docker的安装
### 安装Docker
1. 卸载旧版本
```
sudo apt-get remove docker docker-engine docker.io containerd runc
```
/var/lib/docker的内容，包括镜像、容器、卷和网络，可以保留也可以删除。
2. 运行安装 Docker 的命令：
```
sudo apt-get install -y docker.io
```
3. 等待安装完毕，现在我们使用下面的命令启动 Docker：
```
systemctl start docker
或者:
sudo /etc/init.d/docker start
```
4. 设置开机自动启动：
```
systemctl enable docker
```
5. 查看 docker 版本：
```
docker version
```
6. 查看系统(docker)层面信息，包括管理的images, containers数等
```
docker info
```
7. 停止Docker
```
systemctl stop docker
或者
service docker stop
```
8. 重启Docker
```
systemctl restart docker
或者
service docker restart
```
9. 查看Docker状态
```
systemctl status docker
或者
service docker status
```
### Docker无法启动问题
Cannot connect to the Docker daemon at unix:///var/run/docker.sock”错误的解决办法
错误信息
查看本地docker镜像时提示：
```
root@localhost:~# docker images
Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?
```
解决办法
首先确认是否启动了docker
```
root@localhost:~# ps -ef | grep docker
root        39    10  0 14:17 pts/0    00:00:00 grep --color=auto docker
```
如上图所示，就是docker没有启动，使用如下命令启动docker后：
```
root@localhost:~# service docker start
 * Starting Docker: docker                                         [OK]
```
重新检查docker进程是否存在：
```
root@localhost:~# ps -ef | grep docker
root        90     9  0 14:21 ?        00:00:00 /usr/bin/dockerd -p /var/run/docker.pid
root       105    90  0 14:21 ?        00:00:00 containerd --config /var/run/docker/containerd/containerd.toml --log-level info
root       247    10  0 14:22 pts/0    00:00:00 grep --color=auto docker
```
如上信息表示docker已成功启动。

如果docker未能启动成功，查看docker启动日志/var/log/docker.log（Ubuntu）



### Docker的配置
##### Docker仓库配置
[Docker官方的中央仓库:](https://hub.docker.com/) 这个仓库是镜像最全的，但是下载速度较慢。
1. 配置国内的镜像网站：
创建或修改`` /etc/docker/daemon.json ``文件，修改为如下形式
```
{
  "registry-mirrors": [
    "https://registry.docker-cn.com",
    "http://hub-mirror.c.163.com",
    "https://docker.mirrors.ustc.edu.cn"
  ]
}
```
- [Docker中国区官方镜像](https://registry.docker-cn.com)
- [网易](http://hub-mirror.c.163.com)
- [ustc](https://docker.mirrors.ustc.edu.cn)
2. 重启Docker服务:
```
systemctl daemon-reload
systemctl restart docker  
```
3. 查看是否成功
```
docker info
```
##### 提升Docker权限
```
sudo usermod -aG docker 当前用户名
```
>一定要记得重新登录该用户才能生效。

或者用root账户登录,进行操作.

# 三.Docker镜像操作
### 查看镜像列表
```
docker images
```
### 搜索镜像
```
docker search 镜像名称
```
### 拉取镜像
```
docker pull 镜像名称:版本号
```
### 删除镜像
```
docker rmi 镜像名称:版本号
```
### 查看镜像构成
```
vim /var/lib/docker/image/overlay2/repositories.json
```
### 镜像各个层构成历史
```
docker history docker.io/mysql:5.7
```


# 四.Docker容器操作
### 查询容器
1. 查看正在运行的容器
```
docker ps
```
2. 查看所有容器
```
docker ps -a
```
### 新建容器
```
docker create -it ubuntu:latest
```
使用docker create命令新建的容器处于停止状态，可以使用docker start命令来启动它。
### 运行容器
```docker start containerid```
### 停止容器
1. 停止指定的容器
```
docker stop containerid
```
2. 停止全部容器
```
docker stop $(docker ps -aq)
```
### 新建并运行容器
```
docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
```
通过run命令创建一个新的容器（container）
常用选项说明
- -d, --detach=false， 指定容器运行于前台还是后台，默认为false
- -i, --interactive=false， 打开STDIN，用于控制台交互
- -t, --tty=false， 分配tty设备，该可以支持终端登录，默认为false
- -u, --user=""， 指定容器的用户
- -a, --attach=[]， 登录容器（必须是以docker run -d启动的容器）
- -w, --workdir=""， 指定容器的工作目录
- -c, --cpu-shares=0， 设置容器CPU权重，在CPU共享场景使用
- -e, --env=[]， 指定环境变量，容器中可以使用该环境变量
- -m, --memory=""， 指定容器的内存上限
- -P, --publish-all=false， 指定容器暴露的端口
- -p, --publish=[]， 指定容器暴露的端口
- -h, --hostname=""， 指定容器的主机名
- -v, --volume=[]， 给容器挂载存储卷，挂载到容器的某个目录
- --volumes-from=[]， 给容器挂载其他容器上的卷，挂载到容器的某个目录
- --cap-add=[]， 添加权限，权限清单详见：http://linux.die.net/man/7/capabilities
- --cap-drop=[]， 删除权限，权限清单详见：http://linux.die.net/man/7/capabilities
- --cidfile=""， 运行容器后，在指定文件中写入容器PID值，一种典型的监控系统用法
- --cpuset=""， 设置容器可以使用哪些CPU，此参数可以用来容器独占CPU
- --device=[]， 添加主机设备给容器，相当于设备直通
- --dns=[]， 指定容器的dns服务器
- --dns-search=[]， 指定容器的dns搜索域名，写入到容器的/etc/resolv.conf文件
- --entrypoint=""， 覆盖image的入口点
- --env-file=[]， 指定环境变量文件，文件格式为每行一个环境变量
- --expose=[]， 指定容器暴露的端口，即修改镜像的暴露端口
- --link=[]， 指定容器间的关联，使用其他容器的IP、env等信息
- --lxc-conf=[]， 指定容器的配置文件，只有在指定--exec-driver=lxc时使用
- --name=""， 指定容器名字，后续可以通过名字进行容器管理，links特性需要使用名字
- --net="bridge"， 容器网络设置:
- bridge 使用docker daemon指定的网桥
- host //容器使用主机的网络
- container:NAME_or_ID >//使用其他容器的网路，共享IP和PORT等网络资源
- none 容器使用自己的网络（类似--net=bridge），但是不进行配置
- --privileged=false， 指定容器是否为特权容器，特权容器拥有所有的capabilities
- --restart="no"， 指定容器停止后的重启策略:
- no：容器退出时不重启
- on-failure：容器故障退出（返回值非零）时重启
- always：容器退出时总是重启
- --rm=false， 指定容器停止后自动删除容器(不支持以docker run -d启动的容器)
- --sig-proxy=true， 设置由代理接受并处理信号，但是SIGCHLD、SIGSTOP和SIGKILL不能被代理
### 删除容器
删除容器(删除容器前，需要先停止容器)
```
docker stop containerid
```
### 修改容器
1. Docker 命令修改
```
docker update --restart=always containerid #修改容器为自动重启
```
2. 直接改配置文件
- 首先停止容器，不然无法修改配置文件
- 配置文件路径为：/var/lib/docker/containers/容器ID*
- 在该目录下找到一个文件 hostconfig.json 对文件进行修改即可
- 重新启动容器。
### 进入容器
1. 在容器中开启一个交互模式的终端
```
docker exec -it containerid /bin/bash
```
2. 在容器中开启一个交互模式的终端,以root用户进入容器
```
docker exec -it --user root containerid /bin/bash
```
3. 退出容器
```
exit
```
### 容器日志
```
docker logs -f containerid
```
-f: 可以滚动查看日志的最后几行
### 导出容器
```
docker export -o hello1.tar a4d
docker export a4d > hello2.tar
```
导出容器是指导出一个已经创建的容器到一个文件，不管此时这个容器是否处于运行状态，可以使用docker export命令可以通过-o选项来指定导出的tar文件名，也可以直接通过重定向来实现
### 导入容器
可以使用 docker import 从容器快照文件中再导入为镜像，例如
```
docker import - test/ubuntu:v1.0
```
此外，也可以通过指定 URL 或者某个目录来导入，例如
```
docker import http://example.com/exampleimage.tgz example/imagerepo
```
>注：用户既可以使用 docker load 来导入镜像存储文件到本地镜像库，也可以使用 docker import 来导入一个容器快照到本地镜像库。这两者的区别在于容器快照文件将丢弃所有的历史记录和元数据信息（即仅保存容器当时的快照状态），而镜像存储文件将保存完整记录，体积也要大。此外，从容器快照文件导入时可以重新指定标签等元数据信息。

# 五.制作Docker镜像
制作Docker镜像一般有2种方法：
- 使用hub仓库中已有的镜像，自己安装使用的软件环境后完成image创建.
- 通过Dockerfile，完成镜像image的创建.
### 通过docker commit制作镜像
1. 制作镜像
```
docker commit -m "Added java ubantu" -a "peng" containerid peng/java_ubantu:v2
```
-m 来指定提交的说明信息，跟我们使用的版本控制工具一样；-a 可以指定作者信息；之后是用来创建镜像的容器的 ID；最后指定目标镜像的仓库名和 tag 信息。创建成功后会返回这个镜像的 ID 信息。

2. 使用 docker images 来查看新创建的镜像。

```
sudo docker images
```
3. 使用新的镜像来启动容器

```
docker run -t -i edcefad33ef1 /bin/bash
```
4. 保存镜像为tar压缩包
```
docker save -o xxx.tar peng/java_ubantu:v2
```
5. 加载tar压缩包镜像
```
docker load -i xxx.tar
```
### 通过Dockerfile制作镜像
使用`` docker commit ``命令能够创建一个新镜像，但是有点麻烦，并且该镜像只有制作人员知道其中得细节,团队中不能够轻易的共享它的开发过程。
因此使用一个新的命令``docker build`` ， 从零开始来创建一个新的镜像。首先需要创建一个 Dockerfile 文件，其中包含一组指令来告诉 Docker 如何构建我们的镜像。
#### DockerFile的作用
Dockerfile 是一个用来构建镜像的文本文件，文本内容包含了一条条构建镜像所需的指令和说明。
Dockerfile构建镜像是以基础镜像为基础的，内容是用户编写的一些docker指令，每一条指令构建一层，因此每一条指令的内容，就是描述该层应当如何构建。
可以使用在命令行中调用任何命令。Docker通过读取Dockerfile中的指令自动生成映像。也就是说镜像的定制实际上就是定制每一层所添加的配置、文件。
我们可以把每一层修改、安装、构建、操作的命令都写入一个脚本，这个脚本就是Dockerfile
#### Dockerfile简单示例
1. 创建对应的目录
```
$ mkdir centos-vim
$ cd centos-vim
$ touch Dockerfile
$ vim Dockerfile
```
2. 编写Dockerfile文件
```
FROM centos:7
RUN yum install -y vim
```
3. docker build制作镜像
```
docker build -t peng/centos-vim:v2 .
```
- -t 是标识新建的镜像属于peng的
- centos-vim是仓库的名称
- ：v2 是tag
- "." . 指的是当前目录,它得作用是用来指明使用的Dockerfile文件再当前目录的,也可以替换为一个具体的 Dockerfile 的路径。

4. 创建完成后，从镜像创建容器
```
docker run -t -i peng/centos-vim:v2 /bin/bash
```
#### Dockerfile结构分析
Docker以从上到下的顺序运行Dockerfile的指令。为了指定基本映像，第一条指令必须是FROM。一个声明以＃字符开头则被视为注释。可以在Docker文件中使用RUN，CMD，FROM，EXPOSE，ENV等指令。

在这里列出了一些常用的指令。
##### FROM
指定基础镜像，必须为第一个命令
```
格式：
　　FROM <image>
　　FROM <image>:<tag>
　　FROM <image>@<digest>
示例：
　　FROM mysql:5.6
注：
　　tag或digest是可选的，如果不使用这两个值时，会使用latest版本的基础镜像
```

##### MAINTAINER
维护者信息
```
格式：
    MAINTAINER <name>
示例：
    MAINTAINER Jasper Xu
    MAINTAINER sorex@163.com
    MAINTAINER Jasper Xu <sorex@163.com>
```

##### RUN
构建镜像时执行的命令
```
RUN用于在镜像容器中执行命令，其有以下两种命令执行方式：
shell执行
格式：
    RUN <command>
exec执行
格式：
    RUN ["executable", "param1", "param2"]
示例：
    RUN ["executable", "param1", "param2"]
    RUN apk update
    RUN ["/etc/execfile", "arg1", "arg1"]
注：
　　RUN指令创建的中间镜像会被缓存，并会在下次构建中使用。如果不想使用这些缓存镜像，可以在构建时指定--no-cache参数，如：docker build --no-cache
```

#####  ADD
将本地文件添加到容器中，tar类型文件会自动解压(网络压缩资源不会被解压)，可以访问网络资源，类似wget

```
格式：
    ADD <src>... <dest>
    ADD ["<src>",... "<dest>"] 用于支持包含空格的路径
示例：
    ADD hom* /mydir/          # 添加所有以"hom"开头的文件
    ADD hom?.txt /mydir/      # ? 替代一个单字符,例如："home.txt"
    ADD test relativeDir/     # 添加 "test" 到 `WORKDIR`/relativeDir/
    ADD test /absoluteDir/    # 添加 "test" 到 /absoluteDir/
```

##### COPY
功能类似ADD，但是是不会自动解压文件，也不能访问网络资源

##### CMD
构建容器后调用，也就是在容器启动时才进行调用。

```
格式：
    CMD ["executable","param1","param2"] (执行可执行文件，优先)
    CMD ["param1","param2"] (设置了ENTRYPOINT，则直接调用ENTRYPOINT添加参数)
    CMD command param1 param2 (执行shell内部命令)
示例：
    CMD echo "This is a test." | wc -
    CMD ["/usr/bin/wc","--help"]
注：
 　　CMD不同于RUN，CMD用于指定在容器启动时所要执行的命令，而RUN用于指定镜像构建时所要执行的命令。
```

##### ENTRYPOINT
配置容器，使其可执行化。配合CMD可省去"application"，只使用参数。

```
格式：
    ENTRYPOINT ["executable", "param1", "param2"] (可执行文件, 优先)
    ENTRYPOINT command param1 param2 (shell内部命令)
示例：
    FROM ubuntu
    ENTRYPOINT ["top", "-b"]
    CMD ["-c"]
注：
　　　ENTRYPOINT与CMD非常类似，不同的是通过docker run执行的命令不会覆盖ENTRYPOINT，而docker run命令中指定的任何参数，都会被当做参数再次传递给ENTRYPOINT。Dockerfile中只允许有一个ENTRYPOINT命令，多指定时会覆盖前面的设置，而只执行最后的ENTRYPOINT指令。
```
##### LABEL
用于为镜像添加元数据
```
格式：
    LABEL <key>=<value> <key>=<value> <key>=<value> ...
示例：
　　LABEL version="1.0" description="这是一个Web服务器" by="IT笔录"
注：
　　使用LABEL指定元数据时，一条LABEL指定可以指定一或多条元数据，指定多条元数据时不同元数据之间通过空格分隔。推荐将所有的元数据通过一条LABEL指令指定，以免生成过多的中间镜像。
```
##### ENV
设置环境变量
```
格式：
    ENV <key> <value>  #<key>之后的所有内容均会被视为其<value>的组成部分，因此，一次只能设置一个变量
    ENV <key>=<value> ...  #可以设置多个变量，每个变量为一个"<key>=<value>"的键值对，如果<key>中包含空格，可以使用\来进行转义，也可以通过""来进行标示；另外，反斜线也可以用于续行
示例：
    ENV myName John Doe
    ENV myDog Rex The Dog
    ENV myCat=fluffy
```
##### EXPOSE
指定于外界交互的端口

```
格式：
    EXPOSE <port> [<port>...]
示例：
    EXPOSE 80 443
    EXPOSE 8080
    EXPOSE 11211/tcp 11211/udp
注：
　　EXPOSE并不会让容器的端口访问到主机。要使其可访问，需要在docker run运行容器时通过-p来发布这些端口，或通过-P参数来发布EXPOSE导出的所有端口
```
##### VOLUME
用于指定持久化目录
```
格式：
    VOLUME ["/path/to/dir"]
示例：
    VOLUME ["/data"]
    VOLUME ["/var/www", "/var/log/apache2", "/etc/apache2"
注：
　　一个卷可以存在于一个或多个容器的指定目录，该目录可以绕过联合文件系统，并具有以下功能：
1 卷可以容器间共享和重用
2 容器并不一定要和其它容器共享卷
3 修改卷后会立即生效
4 对卷的修改不会对镜像产生影响
5 卷会一直存在，直到没有任何容器在使用它
```
##### WORKDIR
工作目录，类似于cd命令
```
格式：
    WORKDIR /path/to/workdir
示例：
    WORKDIR /a  (这时工作目录为/a)
    WORKDIR b  (这时工作目录为/a/b)
    WORKDIR c  (这时工作目录为/a/b/c)
注：
　　通过WORKDIR设置工作目录后，Dockerfile中其后的命令RUN、CMD、ENTRYPOINT、ADD、COPY等命令都会在该目录下执行。在使用docker run运行容器时，可以通过-w参数覆盖构建时所设置的工作目录。
```
##### USER:
指定运行容器时的用户名或 UID，后续的 RUN 也会使用指定用户。使用USER指定用户时，可以使用用户名、UID或GID，或是两者的组合。当服务不需要管理员权限时，可以通过该命令指定运行用户。并且可以在之前创建所需要的用户

```
 格式:
　　USER user
　　USER user:group
　　USER uid
　　USER uid:gid
　　USER user:gid
　　USER uid:group

 示例：
　　USER www

 注：

　　使用USER指定用户后，Dockerfile中其后的命令RUN、CMD、ENTRYPOINT都将使用该用户。镜像构建完成后，通过docker run运行容器时，可以通过-u参数来覆盖所指定的用户。

```
##### ARG
用于指定传递给构建运行时的变量
```
格式：
    ARG <name>[=<default value>]
示例：
    ARG site
    ARG build_user=www
```
##### ONBUILD
用于设置镜像触发器
```
格式：
　　ONBUILD [INSTRUCTION]
示例：
　　ONBUILD ADD . /app/src
　　ONBUILD RUN /usr/local/bin/python-build --dir /app/src
注：
　　当所构建的镜像被用做其它镜像的基础镜像，该镜像中的触发器将会被钥触发
```
#### Dockerfile综合例子
```
# This my first nginx Dockerfile
# Version 1.0

# images 基础镜像
FROM centos

#MAINTAINER 维护者信息
MAINTAINER tianfeiyu 

#ENV 设置环境变量
ENV PATH /usr/local/nginx/sbin:$PATH

#ADD  文件放在当前目录下，拷过去会自动解压
ADD nginx-1.8.0.tar.gz /usr/local/  
ADD epel-release-latest-7.noarch.rpm /usr/local/  

#RUN 执行以下命令 
RUN rpm -ivh /usr/local/epel-release-latest-7.noarch.rpm
RUN yum install -y wget lftp gcc gcc-c++ make openssl-devel pcre-devel pcre && yum clean all
RUN useradd -s /sbin/nologin -M www

#WORKDIR 相当于cd
WORKDIR /usr/local/nginx-1.8.0 

RUN ./configure --prefix=/usr/local/nginx --user=www --group=www --with-http_ssl_module --with-pcre && make && make install

RUN echo "daemon off;" >> /etc/nginx.conf

#EXPOSE 映射端口
EXPOSE 80

#CMD 运行以下命令
CMD ["nginx"]

```

编写完成 Dockerfile 后可以使用 docker build 来生成镜像。
```
docker build -t peng/centos-vim:v2 .
```
其中 -t 标记来添加 tag，指定新的镜像的用户信息。“.” 是 Dockerfile 所在的路径（当前目录），也可以替换为一个具体的 Dockerfile 的路径。

可以看到 build 进程在执行操作。它要做的第一件事情就是上传这个 Dockerfile 内容，因为所有的操作都要依据 Dockerfile 来进行。
然后，Dockfile 中的指令被一条一条的执行。每一步都创建了一个新的容器，在容器中执行指令并提交修改（就跟之前介绍过的 docker commit 一样）。
当所有的指令都执行完毕之后，返回了最终的镜像 id。所有的中间步骤所产生的容器都被删除和清理了。
### Docker镜像仓库
制作好镜像后，有时需要将镜像复制到另一台主机上使用。 能达到以上目的有两种方式，一种是上传镜像到仓库中（本地或公共仓库），但是另一台服务器很可能只是与当前服务器局域网想通而没有公网的，
可以搭建私有仓库，来实现这一功能。 如果我们仅仅是要复制到另外少数的服务器，搭建私有仓库显然没有这个必要，将镜像保存为文件上传到其他服务器再从文件中载入镜像也是一个不错的选择。
如果是很多机型需要部署, 无论是运维团队还是开发团队还是一个实验室，都有必要有一个自己的Docker仓库，可以存放符合自己需求的环境或系统镜像，可以实现快速部署。

镜像的管理方式非常像git，可以使用docker push命令上传自己本地镜像到仓库，默认上传到DockerHub官方仓库（需要登陆），命令格式：
```
docker push NAME[:TAG]
```
在上传之前一般会先为自己的镜像添加带自己名字（作者信息）的标签：
```
docker tag testimage:lastest zmc/testimage:lastest
docker pushzmc/testimage:lastest
```

# 六.编排容器
### 什么是容器编排问题?
通过上文我们知道如果要运行一个镜像， 通常都是使用 docker run 命令， 在运行的镜像的时候， 需要指定一些参数，
例如：容器名称、 映射的卷、 绑定的端口、 网络以及重启策略等等。为了保存这些参数， 可以将这个 run 命令保存成 shell 文件， 需要时可以重新运行 shell 文件。
对于只有单个镜像的简单应用， 基本上可以满足需要了。不过不是所有的应用都倾向于做成单个镜像， 这样的镜像会非常复杂， 而且不符合 docker 的思想。 因为 docker 更倾向于简单镜像，
即： 一个镜像只有一个进程。 一个典型的 web 应用， 至少需要一个 web 服务器来运行服务端程序， 同时还需要一个数据库服务器来完成数据的存储， 这就需要两个镜像， 一个是 web ，
一个是 db ， 如果还是按照上面的做法， 需要两个 shell 文件， 或者是在一个 shell 文件中有两个 docker run 命令。这就需要编写复杂的 shell 脚本， 需要的镜像越多， 脚本越复杂，
这个问题被称作 docker 容器的编排。
### Docker-compose是什么?
docker 提供了一个命令行工具 docker-compose 帮助完成镜像的编排,可以通过[Docker-Compose](https://github.com/docker/compose)编写这些参数。
Compose 项目是 Docker 官方的开源项目，负责实现对 Docker 容器集群的快速编排，Docker-Compose可以帮助我们批量的管理容器。
只需要通过一个docker-compose.yml文件去维护即可。前面我们使用 Docker 的时候，定义 Dockerfile 文件，然后使用 docker build、docker run 等命令操作容器。
然而微服务架构的应用系统一般包含若干个微服务，每个微服务一般都会部署多个实例，如果每个微服务都要手动启停，那么效率之低，维护量之大可想而知
使用 Docker Compose 可以轻松、高效的管理容器，它是一个用于定义和运行多容器 Docker 的应用程序工具。
### Docker-Compose安装
##### 安装Python环境
docker-compose是基于python写的脚本,因此需要先安装python环境.
##### 安装Docker-Compose
不但可以通过手动和拉取脚本自动下载安装,还可以通过python包管理工具pip安装.
**手动下载安装Docker-Compose**
1. 去Github官网搜索docker-compose，下载1.24.1版本的Docker-Compose
```
https://github.com/docker/compose/releases/download/1.24.1/docker-compose-Linux-x86_64
```
2. 将下载好的文件拖拽到Linux系统中
将文件上传到你所使用的服务器或者虚拟机，然后将文件移动到/usr/local

3. 需要将Docker-Compose文件的名称修改一下，基于Docker-Compose文件一个可执行的权限
```
mv docker-compose-Linux-x86_64 docker-compose
chmod 777 docker-compose
```
4. 方便后期操作，配置一个环境变量
将docker-compose文件移动到了/usr/local/bin，修改了/etc/profile文件，给/usr/local/bin配置到了PATH中
```
mv docker-compose /usr/local/bin
vi /etc/profile
	export PATH=/usr/local/bin:$PATH
source /etc/profile
```
5. 测试一下
在任意目录下输入
```   
docker-compose --version
```
**脚本自动安装Docker-Compose**
1. 下载docker-compose
```   
curl -L "https://github.com/docker/compose/releases/download/1.28.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
2. 修改执行权限
```   
chmod +x /usr/local/bin/docker-compose
```
3. 测试一下
   在任意目录下输入
```   
docker-compose --version
```
**pip安装**
```
sudo pip install docker-compose
```
### docker-compose.yml文件
- yml文件以key:value方式来指定配置信息
- 多个配置信息以换行+缩进的方式来区分
- 在docker-compose.yml文件中，不要使用制表符
```
version: '3.1'               # 表示该 Docker-Compose 文件使用的是 Version 3.1 file
services:
  mysql:                     # 服务的名称
    restart: always          # 代表只要Docker启动，那么这个容器就跟着一起启动
    image: daocloud.io/library/mysql:5.7.4     # 指定镜像路径
    container_name: mysql    # 指定容器名称
    ports:
      - 3306:3306        # 指定端口号的映射
    environment:
      MYSQL_ROOT_PASSWORD: root         # 指定MySQL的ROOT用户登录密码
      TZ: Asia/Shanghai                 # 指定时区
    volumes:
      - /opt/docker_mysql_tomcat/mysql_data:/var/lib/mysql        # 映射数据卷
  tomcat:
    restart: always          # 代表只要Docker启动，那么这个容器就跟着一起启动
    image: daocloud.io/library/tomcat:8.5.15-jre8     # 指定镜像路径
    container_name: tomcat    # 指定容器名称
    ports:
      - 8080:8080        # 指定端口号的映射
    environment:
      MYSQL_ROOT_PASSWORD: root         # 指定MySQL的ROOT用户登录密码
      TZ: Asia/Shanghai                 # 指定时区
    volumes:
      - /opt/docker_mysql_tomcat/tomcat_webapps:/usr/local/tomcat/webapps        # 映射数据卷
      - /opt/docker_mysql_tomcat/tomcat_logs:/usr/local/tomcat/logs        # 映射数据卷
```
docker-compose.yml 属性
- version：指定 docker-compose.yml 文件的写法格式
- services：多个容器集合
- build：配置构建时，Compose 会利用它自动构建镜像，该值可以是一个路径，也可以是一个对象，用于指定 Dockerfile 参数
### 使用Docker-compose命令管理容器
在使用docker-compose的命令时，默认会在当前目录下找docker-compose.yml
##### 启动容器
up 该命令十分强大，它将尝试自动完成包括构建镜像，（重新）创建服务，启动服务，并关联服务相关容器的一系列操作
```
docker-compose up [options] [SERVICE...]   
docker-compose up
docker-compose up -d  // 后台启动并运行容器
docker-compose -f docker-compose.yml up -d
```
选项包括：
- -d 在后台运行服务容器
- –no-color 不使用颜色来区分不同的服务的控制输出
- –no-deps 不启动服务所链接的容器
- –force-recreate 强制重新创建容器，不能与–no-recreate同时使用
- –no-recreate 如果容器已经存在，则不重新创建，不能与–force-recreate同时使用
- –no-build 不自动构建缺失的服务镜像
- –build 在启动容器前构建服务镜像
- –abort-on-container-exit 停止所有容器，如果任何一个容器被停止，不能与-d同时使用
- -t, –timeout TIMEOUT 停止容器时候的超时（默认为10秒）
- –remove-orphans 删除服务中没有在compose文件中定义的容器
- –scale SERVICE=NUM 设置服务运行容器的个数，将覆盖在compose中通过scale指定的参数
- -f 指定使用的Compose模板文件，默认为docker-compose.yml，可以多次指定。

docker-compose up也可以用于更新容器, 当服务的配置发生更改时，可使用 ``docker-compose up ``命令更新配置
此时，Compose 会删除旧容器并创建新容器，新容器会以不同的 IP 地址加入网络，名称保持不变，任何指向旧容起的连接都会被关闭，重新找到新容器并连接上去
##### 创建容器
```
docker-compose create [options] [SERVICE...]
```
选项包括：
- –force-recreate：重新创建容器，即使配置和镜像没有改变，不兼容–no-recreate参数
- –no-recreate：如果容器已经存在，不需要重新创建，不兼容–force-recreate参数
- –no-build：不创建镜像，即使缺失
- –build：创建容器前，生成镜像
##### 关闭并删除容器
//down 停止 up 命令所启动的容器，并移除网络。——这里需要特别注意，up 启动的，不应该使用rm 去删除，因为这样无法删除网络
```
docker-compose down [options]
docker-compose down
```
选项包括：
- –rmi type，删除镜像，类型必须是：all，删除compose文件中定义的所有镜像；local，删除镜像名为空的镜像
- -v, –volumes，删除已经在compose文件中定义的和匿名的附在容器上的数据卷
- –remove-orphans，删除服务中没有在compose中定义的容器
##### 开启 | 关闭 | 重启容器
```
docker-compose restart [options] [SERVICE...]// restart 重启服务

// stop start 停止和开启容器
docker-compose stop xxx
docker-compose start xxx

// kill 强制停止某容器
docker-compose kill -s SIGINT
```
##### 查看容器
```
docker-compose ps
```
##### 查看容器日志
```
docker-compose logs -f
docker-compose logs [options] [SERVICE...]
```
查看服务容器的输出。默认情况下，docker-compose将对不同的服务输出使用不同的颜色来区分。可以通过–no-color来关闭颜色。
##### 重建容器

build 重建某个容器，在 Dockerfile 发生了改变的时候，可以重建image。然后再 up 运行起来所有的容器
```
docker-compose build [options] [--build-arg key=val...] [SERVICE...]
docker-compose build    //重建所有容器
docker-compose build xxx   //重建指定容器
```
选项包括：
- –compress 通过gzip压缩构建上下环境
- –force-rm 删除构建过程中的临时容器
- –no-cache 构建镜像过程中不使用缓存
- –pull 始终尝试通过拉取操作来获取更新版本的镜像
- -m, –memory MEM为构建的容器设置内存大小
- –build-arg key=val为服务设置build-time变量
服务容器一旦构建后，将会带上一个标记名。可以随时在项目目录下运行docker-compose build来重新构建服务
##### 进入容器
```
docker-compose exec -it ct-phpfpm /bin/bash
docker-compose exec
docker-compose exec [options] SERVICE COMMAND [ARGS...]
```
选项包括：
- -d 分离模式，后台运行命令。
- –privileged 获取特权。
- –user USER 指定运行的用户。
- -T 禁用分配TTY，默认docker-compose exec分配TTY。
- –index=index，当一个服务拥有多个容器时，可通过该参数登陆到该服务下的任何服务，例如：docker-compose exec –index=1 web /bin/bash ，web服务中包含多个容器
##### 查看镜像
```
docker-compose images
```
##### 拉取镜像
```
docker-compose pull [options] [SERVICE...]
```
##### 推送镜像
```
docker-compose push
```
##### 打印某容器的映射端口
```
docker-compose port xxx
```
##### config 验证 docker-compose 文件格式是否正确
```
docker-compose config// top 查看所有容器的进程
docker-compose top

docker-compose config [options]
```
验证并查看compose文件配置。

选项包括：
- –resolve-image-digests 将镜像标签标记为摘要
- -q, –quiet 只验证配置，不输出。 当配置正确时，不输出任何内容，当文件配置错误，输出错误信息
- –services 打印服务名，一行一个
- –volumes 打印数据卷名，一行一个
##### 显示正在运行的进程
```
docker-compose top
```
### Docker-Compose简单示例
1. 新建文件夹，在该目录中编写 app.py 文件
```
mkdir project
cd project
touch app.py
vim app.py
```
app.py:
```
from flask import Flask
from redis import Redis 

app = Flask(__name__)
redis = Redis(host='redis', port=6379) 

@app.route('/')
def hello():    
    count = redis.incr('hits')    
    return 'Hello World! 该页面已被访问 {} 次。\n'.format(count)

if __name__ == "__main__":    
    app.run(host="0.0.0.0", debug=True)
```
2. 编写Dockerfile文件
```
touch Dockerfile
vim Dockerfile
```
Dockerfile文件内容:
```
FROM python:3.6-alpine
ADD . /code
WORKDIR /code
RUN pip install redis flask
CMD ["python", "app.py"]
```
3. 编写docker-compose.yml文件
```
touch docker-compose.yml
vim docker-compose.yml
```
docker-compose.yml文件内容:
```
version: '3'
services:      
  web:    
    build: .    
    ports:     
      - "5000:5000"   
  redis:    
    image: "redis:alpine" 
```
4. 运行 compose 项目
```
docker-compose up -d #-d 后台运行
```
5. 查看 compose容器状态
```
docker-compose ps
```
6. 访问页面
访问本地ip地址 5000 端口，每次刷新页面，计数就会加 1

# 七.Docker、dockerfile、docker-compose、k8s的区别
### 说明
假如不用 docker ，搭建 wordpress 需要先找台 server ，假设其 OS 为 Ubuntu ，然后需要按照文档一步步敲命令，写配置.
如果使用docker, 随便找台 server ，不管什么操作系统，只要支持 docker 就行， docker run ubuntu, docker 会从官方源里拉取最新的 Ubuntu 镜像，
可以认为开了个 Ubuntu 虚拟机，然后一步步安装，配置跟上面一样。
但是这样安装有个显著的缺点，一旦 container 被删，你做的工作就都没了。当然可以用 docker commit 来保存成镜像，这样就可以复用了。
但是镜像一般比较大，而且只分享镜像的话，别人也不知道你这镜像到底包含什么，这些问题都不利于分享和复用。
一个直观的解决方案就是，写个脚本把安装过程全部记录下来，这样再次安装的时候，执行脚本就行了。 Dockerfile 就是这样的脚本，它记录了一个镜像的制作过程。
有了 Dockerfile, 只要执行 docker build . 就能制作镜像，而且 Dockerfile 就是文本文件，修改也很方便。
现在有了 wordpress 的镜像，只需要 docker run 就把 wordpress 启动起来了。
如果仅仅是 wordpress, 这也就够了。但是很多时候，需要多个镜像合作才能启动一个服务，比如前端要有 nginx ， 数据库 mysql, 邮件服务等等，当然你可以把所有这些都弄到一个镜像里去，但这样做就无法复用了。
更常见的是, nginx, mysql, smtp 都分别是个镜像，然后这些镜像合作，共同服务一个项目。而如果涉及多个容器的运行（如服务编排）就可以通过 docker-compose 来实现，它可以轻松的将多个容器作为 service 来运行（当然也可仅运行其中的某个），
并且提供了 scale (服务扩容) 的功能。 docker-compose 就是解决这个问题的。你的项目需要哪些镜像，每个镜像怎么配置，要挂载哪些 volume, 等等信息都包含在 docker-compose.yml 里。
要启动服务，只需要 docker-compose up 就行，停止也只需要 docker-compse stop/down 简而言之， Dockerfile 记录单个镜像的构建过程， docker-compse.yml 记录一个项目(project, 一般是多个镜像)的构建过程。
### 定义
docker 的使用过程，它分为镜像构建与容器启动。
- 镜像构建：即创建一个镜像，它包含安装运行所需的环境、程序代码等。这个创建过程就是使用 dockerfile 来完成的。
- 容器启动：容器最终运行起来是通过拉取构建好的镜像，通过一系列运行指令（如端口映射、外部数据挂载、环境变量等）来启动服务的。针对单个容器，这可以通过 docker run 来运行。

** dockerfile: **的作用是从无到有的构建镜像。它包含安装运行所需的环境、程序代码等。这个创建过程就是使用 dockerfile 来完成的。Dockerfile - 为 docker build 命令准备的，用于建立一个独立的 image
，在 docker-compose 里也可以用来实时 build docker-compose.yml - 为 docker-compose 准备的脚本，可以同时管理多个 container ，包括他们之间的关系、用官方 image 还是自己 build 、各种网络端口定义、储存空间定义等

** docker-compose: **是编排容器的。例如，你有一个php镜像，一个mysql镜像，一个nginx镜像。如果没有docker-compose，那么每次启动的时候，
你需要敲各个容器的启动参数，环境变量，容器命名，指定不同容器的链接参数等等一系列的操作，相当繁琐。
而用了docker-composer之后，你就可以把这些命令一次性写在docker-composer.yml文件中，以后每次启动这一整个环境（含3个容器）的时候，你只要敲一个docker-composer up命令就ok了。
### 简单总结
1.dockerfile: 构建镜像；
2.docker run: 启动容器；
3.docker-compose: 启动服务；
### 结论
##### Dcoker
Docker 这个东西所扮演的角色，容易理解，它是一个容器引擎，也就是说实际上我们的容器最终是由Docker创建，运行在Docker中，其他相关的容器技术都是以Docker为基础，它是我们使用其他容器技术的核心。
##### Dockerfile
dockerfile的作用是从无到有的构建镜像。它包含安装运行所需的环境、程序代码等。这个创建过程就是使用 dockerfile 来完成的。
##### Docker-Compose
Docker-Compose 是用来管理你的容器的，有点像一个容器的管家，想象一下当你的Docker中有成百上千的容器需要启动，如果一个一个的启动那得多费时间。有了Docker-Compose你只需要编写一个文件，
在这个文件里面声明好要启动的容器，配置一些参数，执行一下这个文件，Docker就会按照你声明的配置去把所有的容器启动起来，但是Docker-Compose只能管理当前主机上的Docker，也就是说不能去启动其他主机上的Docker容器
##### Docker Swarm
Docker Swarm 是一款用来管理多主机上的Docker容器的工具，可以负责帮你启动容器，监控容器状态，如果容器的状态不正常它会帮你重新帮你启动一个新的容器，
来提供服务，同时也提供服务之间的负载均衡，而这些东西Docker-Compose 是做不到的
##### Kubernetes
Kubernetes它本身的角色定位是和Docker Swarm 是一样的，也就是说他们负责的工作在容器领域来说是相同的部分，当然也有自己一些不一样的特点。这个就像是Eclipse和IDEA一样，也是一个跨主机的容器管理平台。它是谷歌公司根据自身的多年的运维经验研发的一款容器管理平台。而Docker Swarm则是由Docker 公司研发的。

既然Docker Swarm和Kubernetes这两个东西是一样的，那就面临选择的问题，实际上这两年Kubernetes已经成为了很多大公司的默认使用的容器管理技术，而Docker Swarm已经在这场与Kubernetes竞争中已经逐渐失势，
如今容器管理领域已经开始已经逐渐被Kubernetes一统天下了。

# 八.Docker安装Gitlab
### 创建Gitlab配置映射目录
通常会将 GitLab 的配置 (etc) 、 日志 (log) 、数据 (data) 放到容器之外， 便于日后升级，也为了避免容器运行时数据丢失因此请先准备这三个目录。具体对应关系如下表。
| 宿主机位置 | 容器位置 | 作用 |
| - | - | - |
| /home/gitlab/config | /etc/gitlab | 用于存储 GitLab 配置文件 |
| /home/gitlab/logs | /var/log/gitlab | 用于存储日志 |
| /home/gitlab/data | /var/opt/gitlab | 用于存储应用数据 |

linux创建命令:
```
mkdir -p /home/gitlab/config
mkdir -p /home/gitlab/logs
mkdir -p /home/gitlab/data
```
### 下载Gitlab的最新镜像
```
docker pull gitlab/gitlab-ce:latest
```
### 启动Gitlab容器
```
docker run --detach --publish 443:443 --publish 8880:80 --publish 22:22 --name gitlab  --volume /home/gitlab/config:/etc/gitlab --volume /home/gitlab/logs:/var/log/gitlab --volume /home/gitlab/data:/var/opt/gitlab  --privileged=true gitlab/gitlab-ce:latest
```

使用简化命令
```
docker run -d -p 8843:443 -p 8880:80 -p 8822:22 --name gitlab  -v /home/gitlab/config:/etc/gitlab -v /home/gitlab/logs:/var/log/gitlab -v /home/gitlab/data:/var/opt/gitlab  --privileged=true gitlab/gitlab-ce:latest
```
命令解释
- --detach  保持容器在后台持续运行
- --publish 443:443：将http：443映射到外部端口443
- --publish 8880:80：将web：80映射到外部端口8880
- --publish 222:22：将ssh：22映射到外部端口222
- --name gitlab: 运行容器名
- --restart always: 自动重启
- --volume /home/gitlab/config:/etc/gitlab: 挂载目录
- --volume /home/gitlab/logs:/var/log/gitlab: 挂载目录
- --volume /home/gitlab/data:/var/opt/gitlab: 挂载目录
- --privileged=true 使得容器内的root拥有真正的root权限。否则，container内的root只是外部的一个普通用户权限.
- gitlab/gitlab-ce 镜像的名称，这里也可以写镜像ID
### 访问Gitlab主页
在浏览器中输入主机对应的ip地址和端口号即可:
```
http://192.168.xx.xx:xxxx/
```
查看root账户初始密码:``cat /etc/gitlab/initial_root_password``
进入gitlab访问页面，第一步要做的就是给root用户设置密码，设置完后，通过root + 设置的密码登录。

>如果遇到gitlab502错误请稍等片刻,此时gitlab服务还未完全启动.因为容器开启时间并不等于程序开启时间，有时容器已经启动而Gitlab依旧无法访问。此时如果检查配置文件没有问题，那么继续等待即可。
### Github忘记Root修改密码
1. 进入刚才已经运行的Github容器
```
docker exec -it 容器ID /bin/bash
```
2. 输入命令修改密码
```
gitlab-rails console -e production
```
3. 选择管理员用户
id为1的是超级管理员
```
user = User.where(id: 1).first 
```
4. 修改密码为指定密码
```
user.password='xxxxxx'
```
5. 保存,如果没有问题返回为True
```
user.save!
```
### 本地搭建GitLab地址不一致问题

原因及方案：
/opt/gitlab/embedded/service/gitlab-rails/config/gitlab.yml
内host配置不正确，
```
gitlab:
    ## Web server settings (note: host is the FQDN, do not include http://)
    host: 14883a395243
    port: 80
    https: false
```
修改后重启即可解决问题
```
gitlab-ctl restart
```
# 九.Docker安装nexus镜像
### 1. 查找镜像
```
docker search  nexus
```
### 2. 拉取镜像
拉取最新版本，目前最新版本是3.20.1
```
docker pull sonatype/nexus3
```
### 4. 指定虚拟机与容器对应的文件夹
```
mkdir -p /data/nexus/data
```
### 5. 给文件夹设置权限
```
chmod 777 -R /data/nexus/data
```
### 6. 启动容器
```
docker run -d --name nexus3 -p 8081:8081 --privileged=true -v /data/nexus/data:/nexus-data sonatype/nexus3
```
注：--privileged，该参数可以设置是否给docker容器特权，如果该参数为true，使得docker容器内的root权限为宿主机的root权限，而非只是容器内的root权限
### 7. 查看日志
如果启动失败可以查看日志:
```
docker logs -f nexus3
```
### 8. 访问nexus
打开浏览器，访问 http://192.168.xx.xxx:8081/
### 9. 查看管理员admin密码的
```
cat /data/nexus/data/admin.password
```

# 十.Docker安装Jenkins
### 1.启动docker，下载Jenkins镜像文件
```
docker pull jenkins/jenkins
```
### 2.创建挂载目录
创建Jenkins挂载目录并授权权限（我们在服务器上先创建一个jenkins工作目录/data/nexus/data，赋予相应权限，稍后我们将jenkins容器目录挂载到这个目录上，这样我们就可以很方便地对容器内的配置文件进行修改。 
如果我们不这样做，那么如果需要修改容器配置文件，将会有点麻烦，因为虽然我们可以使用docker exec -it --user root 容器id /bin/bash 命令进入容器目录，但是连简单的 vi命令都不能使用）
```
mkdir -p /data/jenkins/data
chmod 777 /data/jenkins/data
```
### 3.创建并启动Jenkins容器
```
docker run -d -p 8888:8080 -p 50000:50000 --privileged=true -v /data/jenkins/data:/var/jenkins_home -u root -v /etc/localtime:/etc/localtime --name jenkins jenkins/jenkins
```
- -d 后台运行镜像
- -p 8888:8080 将镜像的8080端口映射到服务器的8888端口。
- -p 50000:50000 将镜像的50000端口映射到服务器的50000端口
- -v /var/jenkins_mount:/var/jenkins_mount /var/jenkins_home目录为容器jenkins工作目录，我们将硬盘上的一个目录挂载到这个位置，方便后续更新镜像后继续使用原来的工作目录。这里我们设置的就是上面我们创建的 /var/jenkins_mount目录
- -v /etc/localtime:/etc/localtime让容器使用和服务器同样的时间设置。
- --name myjenkins 给容器起一个别名
- u root 以root账户登录
### 4.访问Jenkins页面
打开浏览器，访问 http://192.168.xx.xxx:8888/
### 5.查看初始密码
进入到映射目录/data/jenkins/data,编辑initialAdminPassword文件查看，把密码输入登录中的密码即可，开始使用。
```
vi /data/jenkins/data/secrets/initialAdminPassword
```


# docker启动容器之后马上又自动关闭了
问题现象：
centos 启动一个容器添加了-d 参数，但是docker ps 或者docker ps -a查看却已经退出了
shell>docker run -d centos
a44b2b88559b68a2221c9574490a0e708bff49d88ca21f9e59d3eb245c7c0547
shell>docker ps 


what ? why?

退出原因
1、docker容器运行必须有一个前台进程， 如果没有前台进程执行，容器认为空闲，就会自行退出
2、容器运行的命令如果不是那些一直挂起的命令（ 运行top，tail、循环等），就是会自动退出
3、这个是 docker 的机制问题

解决方案
方案1：
网上有很多介绍，就是起一个死循环进程，让他不停的循环下去，前台永远有进程执行，那么容器就不会退出了,以centos为例
shell>docker run -d centos /bin/sh -c "while true; do echo hello world; sleep 1; done"
缺点： 命令太冗长了，还占用一个终端

方案2：
shell>docker run -dit centos /bin/bash
添加-it 参数交互运行
添加-d 参数后台运行
这样就能启动一个一直停留在后台运行的Centos了。

shell>docker ps 容器运行起来了


进入容器的方法：
使用exec，不要使用attach命令
attach命令就是使用现有终端，如果你要退出容器操作，那么bash结束，容器也就退出了
shell>docker exec -it <container_id> /bin/bash //新建一个bash


参考资料:
[利用docker搭建前端开发环境](https://juejin.cn/post/6932808129189150734)
[Docker — 从入门到实践](https://yeasy.gitbook.io/docker_practice/)
[Docker-compose](https://blog.csdn.net/weixin_44911419/article/details/99858561)