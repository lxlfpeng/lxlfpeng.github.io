---
title: CI-CD工具之GitLab-Runner
---

# 一.GitLab-CI和GitLab-Runner简介
### 1.GitLab-CI是什么?
GitLab-CI就是一套配合GitLab使用的持续集成系统（当然，还有其它的持续集成系统，同样可以配合GitLab使用，比如Jenkins）。GitLab8.0以后的版本默认集成了GitLab-CI并且默认启用的。

### 2.GitLab-Runner是什么?
Gitlab只是个代码仓库，想要实现CI/CD还需安装gitlab-runner，gitlab-runner相当于是Gitlab-CI中的任务的执行器，Gitlab会在需要执行任务时调用它。
GitLab-CI的作用是管理各个项目的构建状态，运行构建任务这种浪费资源的事情就交给 GitLab Runner 来做。因为 GitLab Runner 可以安装到不同的机器上，所以在构建任务运行期间并不会影响到 GitLab 的性能 ，Runner可以分布在不同的主机上，同一个主机上也可以有多个Runner。
一般GitLab里面的每一个工程都会定义一个属于这个工程的软件集成脚本(.gitlab-ci.yml)，用来描述如何自动化地完成一些软件集成工作。当这个工程的仓库代码发生变动时，比如有人push了代码，GitLab就会将这个变动通知GitLab-CI。这时GitLab-CI会找出与这个工程相关联的GitLab-Runner，并通知这些Runner把代码更新到本地并执行预定义好的执行脚本。
所以，GitLab-Runner就是一个用来执行软件集成脚本的东西。你可以想象一下：Runner就像一个个的工人，而GitLab-CI就是这些工人的一个管理中心，所有工人都要在GitLab-CI里面登记注册，管理中心(GitLab-CI)会将任务分配给工人进行执行。

>gitlab-runner可以在不同的主机上部署，也可以在同一个主机上设置多个gitlab-runner ，还可以根据不同的环境设置不同的环境，比如我们需要区分研发环境，测试环境以及正式环境等。

### 3.GitLab-CI执行步骤
.gitlab-ci.yml文件会告诉GitLab Runner 去做哪些任务。默认情况下，.gitlab-ci.yml会定义一个pipeline，pipeline分为三个阶段：build，test，deploy。没有使用的的阶段会被忽略执行。
因此，简而言之，CI所需要的步骤可以归结为：
1. 配置一个Runner。
2. 添加`.gitlab-ci.yml`到项目的根目录。
配置好以后，在每一次push到Git仓库的过程中，Runner会自动开启pipline，pipline将显示在项目的Pipline页面中。

GitLab-CI完整流程:
1. 本地代码改动。
2. 变动代码推送到GitLab上。
3. GitLab 将这个变动通知GitLab-CI。
4. GitLab-CI找出这个工程相关联的gitlab-runner。
5. gitlab-runner把代码更新到本地。
6. 根据预设置的条件配置好环境。
7. 根据预定义的脚本(一般是.gitlab-ci.yml)执行。
8. 把执行结果通知给GitLab。
9. GitLab显示最终执行的结果。

### 4.GitLab-Runner执行器
Runner需要一个环境来运行jobs. 这个环境称之为执行环境（executor）。GitLab Runner 支持多种执行环境，包括 SSH，Docker，VirtualBox 等。
- Shell
- Docker
- Docker Machine and Docker Machine SSH (auto-scaling)
- Parallels
- VirtualBox
- SSH
- Kubernetes

推荐使用shell方式，对应的jdk，maven工具可以自行安装与配置，这种配置比较简单。如果选择docker，那么要指定一个镜像，这个镜像必须在docker images中或者hub docker中可以找到，并且需要的编译工具都需要在docker中安装好。

# 二.GitLab-Runner安装及注册
### 1.GitLab-Runner安装
GitLab-Runner安装分为两种:
- 本地安装
- Docker安装
##### (1.)本地安装GitLab-Runner
1. 下载二进制文件
```
$ sudo wget -O /usr/local/bin/gitlab-runner https://gitlab-runner-downloads.s3.amazonaws.com/latest/binaries/gitlab-runner-linux-amd64
```
2. 接着授予可执行权限
```
$ sudo chmod +x /usr/local/bin/gitlab-runner
```
3. 创建一个gitlab-ci用户
```
$ sudo useradd --comment 'GitLab Runner' --create-home gitlab-runner --shell /bin/bash  
```
4. 安装，并作为服务启动
```
$ sudo gitlab-runner install --user=gitlab-runner --working-directory=/home/gitlab-runner  --user root
```
5. GitLab-Runner常用命令
```
$ sudo gitlab-runner list //查看各个 Runner 的状态
$ sudo gitlab-runner stop //停止服务
$ sudo gitlab-runner start //启动服务
$ sudo gitlab-runner restart //重启服务
```
或者直接用脚本安装:
```
sudo wget -O /usr/local/bin/gitlab-runner https://gitlab-runner-downloads.s3.amazonaws.com/latest/binaries/gitlab-runner-linux-amd64

curl -L https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh | sudo bash

sudo apt-get install gitlab-runner
```
##### (2.)Docker安装GitLab-Runner(推荐)
1. 首先下载gitlab-runner的Docker镜像
```
docker pull docker.io/gitlab/gitlab-runner
```
2. 使用如下命令运行gitlab-runner；
```
docker run -d --name gitlab-runner --privileged=true -v /var/run/docker.sock:/var/run/docker.sock -v /srv/gitlab-runner/config:/etc/gitlab-runner gitlab/gitlab-runner:latest
```
此时我们如果查看gitlab-runner的容器日志的话，会发现如下错误，config.toml文件找不到，
```
ERROR: Failed to load config stat /etc/gitlab-runner/config.toml: no such file or directory  builds=0
```
这个问题不必担心，当我们将gitlab-runner注册到Gitlab时，会自动生成该文件；
3. 进入docker容器
```
docker exec -it --user root containerid /bin/bash
```

### 2.GitLab-Runner的分类
GitLab-Runner服务启动以后如何才能和GitLab-CI关联起来?这里就需要对GitLab-Runner进行注册。GitLab-CI会生成一个唯一的Token，在对GitLab-Runner进行注册的时候绑定GitLab-CI的主机地址和token就能将GitLab-Runner和GitLab-CI关联起来。
gitlab-runner分为三种：Shared Runner、Group Runner、Specific Runner。
##### (1.)Shared Runners
shared Runners 是gitlab 管理员统一配置的runner，作用于整个gitlab的所有项目，所以要gitlab的admin权限来进行创建，只要你的项目是在当前的gitlab下，就可以使用shared runner。
即是共享runner，gitlab上所有的project都可以通过指定tag去使用，可以在Settings > CICD > runner中查看，如果某个project不想使用share runner，可以Project>Settings > CICD > runner下设置disable，默认一般是enable.
##### (2.)Group Runner
Group Runner是配置则是在用户组里面配置的，相当于给一个分组设置runner，因此，分组中所有的项目都可以使用。需要Group的管理这及以上的权限。
Group runner需要满足两个条件
- 用户在用户组里面
- 项目在用户组里面
##### (3.)Specific Runner
Specific Runner：这种Runner只能为指定的工程服务。拥有该工程访问权限的人都能够为该工程创建Shared Runner，在gitlab上打开project下的settings-> CICD-> runners。
##### (4.)三种GitLab-Runner总结
|种类|创建权限|使用权限|token位置|备注|
|-|-|-|-|-|
|Specific Runner|只有系统管理员能够创建|全局的runner，所有的项目都可以使用|管理员->admin area(小扳手图标)->OverView->Runners|-|
|Group Runner|Group的管理员及以上的权限|分组中所有的项目都可以使用|对应Group项目->setttings->CICD->runners|-|
|Specific Runner|项目的开发者|项目特有的runner，只有该项目才能使用|对应Project项目->setttings->CICD->runners|-|

>个人建议使用Group Runner，可以根据不同种类的项目，创建不同的分组，比如：Android、IOS、服务端等，然后针对每个分组创建对应的Group Runner，这样相互之间不会有影响，同时又不需要为每个工程单独创建runner。

>在gitlab admin area中可以管理你gitlab所有注册的runners。share runner可以转为group runner或者specific runner，但是不可以逆转。

### 3.注册gitlab-runner到GitLab-CI
执行命令:
```
sudo gitlab-runner register
```
配置Runner:
```
Runtime platform      arch=amd64 os=linux pid=11348
revision=943fc252 version=13.6.0
Running in system-mode.
Enter the GitLab instance URL (for example, https://gitlab.com/):#输入gitlab的url 

Enter the registration token: #输入注册令牌

Enter a description for the runner: #输入runner的描述 [gitlab-cicd]:
test
Enter tags for the runner (comma-separated): #输入标签
test
Registering runner... succeeded runner=K-_PmTnN
Enter an executor: virtualbox, custom, shell, ssh, docker+machine, docker-ssh+machine, kubernetes, docker, docker-ssh, parallels: #输入以何种方式提供runner
shell  #这里选择最简单的shell方式
```
注册的步骤在不同平台下大同小异：运行``gitlab-runner register``命令，会输出一个交互界面，在里面依次输入 GitLab 实例地址、CI Token、Runner 描述、
标签列表（用于区分不同类型的 Runner，使不同阶段的 job 在不同的 Runner 中运行）、执行环境类型，如果选择基于 Docker 的执行环境，则需要再输入一个默认的的image(镜像).
注册之后，Runner 会将配置写入``/etc/gitlab-runner/config.toml`` 文件中，如果文件内容不丢失，gitlab-runner 程序会自动读取配置内容并运行，无需重复注册。
当然，如果你需要一些更高级的配置，则可以直接修改 ``/etc/gitlab-runner/config.toml`` 。具体的配置可以见官方文档。在配置文件更改后，runner daemon 会自动重新加载配置，无需重启。

> gitlab-runner register config.toml 中的部分配置也可以通过环境变量注入，且所有配置都可以通过注册命令的参数传入。

**gitlab-runner配置文件位置**
Runner的信息是存放在一个配置文件里面的，配置文件的格式一般是.toml。这个配置文件的存放位置有以下几种情况：
- 如果是以root用户身份运行``gitlab-ci-multi-runner register``，那么配置文件默认是``/etc/gitlab-runner/config.toml``
- 如果是以非root用户身份运行``gitlab-ci-multi-runner register``，那么配置文件默认是``~/.gitlab-runner/config.toml``

**查看注册成功的gitlab-runner**
在gitlab上打开project下的settings > CICD > runners，可以看到我们配置好的runner.
![](https://upload-images.jianshu.io/upload_images/3067896-38c004c8ed782fb1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 4.gitlab-runner取消注册
```
#使用令牌注销
gitlab-runner unregister --url http://gitlab.example.com/ --token t0k3n

#使用名称注销（同名删除第一个）
gitlab-runner unregister --name test-runner

#注销所有
gitlab-runner unregister --all-runners
```

# 三.GitLab-Runner的executor(执行器)
### 1.executor(执行器)的分类
在Gitlab-Runner注册中我们需要选择executor(执行器)，gitlab-runner又有很多种类型的执行器（就是所谓的executor）。
- SSH
- Shell
- Parallels
- VirtualBox
- Docker
- Docker Machine (auto-scaling)
- Kubernetes
- Custom
![](https://upload-images.jianshu.io/upload_images/3067896-d521efcbcd1e7129.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
其中比较常用的是shell executor和docker executor。

### 2.SSH executor
通过ssh连接到远程主机，然后在远程主机上启动一个进程来执行GitLab CI构建过程。连接时需指定url、port、user、password/identity_file等参数；若想要上传artificate，需要将Runner安装在ssh 连接到的远程主机上。

### 3.VirtualBox/Parallel executor
通过ssh远程连接到虚拟机，在虚拟机中执行GitLab CI构建过程，可能会创建虚拟机快照以加速下一次构建。类似地，需指定user、password/identity_file；同SSH方式类似，若想要上传artificate，需要将Runner安装在VirtualBox的虚拟机中；正式开启CI流程前，需提前在VirtualBox中创建或导入一个Base Virtual Machine，并在其中安装 OpenSSH Server以及依赖等。

### 4.Kuberentes executor
- 让Runner连接到连Kubernetes API Server，为每一个Job动态创建一个Pod来执行GitLab CI构建过程。
- 且此Pod除了包含固有的Infra Container外，还一定会包含Build Container和Help Container，另外，可能包含Service Container。简单而言，Build Container用于执行.gitlab-ci.yml文件中在stage标签中定义的脚本。Help Container则用于辅助Build Container的执行构建工作，具体是负责git和certificate store相关的操作。
- 最后Service Container的用途则对应着.gitlab-ci.yml文件中定义的service标签，即一个辅助容器，为Build Container提供服务，其基本实现原理是Docker Link。最后，每一个Job都会包含四个阶段（Job构建过程的生命周期）：Prepare、Pre-Build、Build和Post-Build。这几个阶段的具体作用，我在这里就不阐述了，比较简单，可以阅读这里，也可以在源码中找到。

### 5.shell executor
这种方式使用安装Runner的同一台主机启动一个进程来执行GitLab CI构建过程，在host中执行shell，比较简单，但对运维不友好，因为构建用到的所有程序，
都需要安装到host主机中，比如maven项目就需要安装java和mvn的软件包和配置环境。并且在这种方式中如果需要使用Docker镜像的话，由于runner在host主机中会以gitlab-runner用户执行脚本，
所以需要把gitlab-runner加入docker组才行，但是这样gitlab-runner会拥有root用户的权限，因此对host不安全，如果想要构建docker镜像，采用这种方式，需要慎重。这种方式的好处是凡是支持安装Runner的机器类型，都可以用使用shell的方式。这意味着Windows PowerShell、Bash、Sh和CMD都是可以的。

### 6.docker executor
这种方式是在docker容器中执行shell，docker服务需要选择定制化的镜像，该镜像必须拥有shell运行时需要的一切命令。在在.gitlab-ci.yml文件中可以定义的镜像.
对于docker executor，每次都是启动一个新的container构建，新的container是一个非常clear的环境，因此上次构建使用到的base image和构建的缓存都无法使用.

以下几个场景可能需要应用内部去调用docker命令，实现docker镜像/容器的操作。 列举以下场景：

1. 如果你使用流水线工具，需要docker命令去构建和管理镜像，但流水线工具是以docker容器的方式运行。
2. 如果你是在kubernetes环境部署，应用需要同docker进行交互。

在Docker中实现运行Docker的两种方法
- docker-in-docker 方法
- 通过挂载docker.sock（DooD方法）运行docker


##### (1.)docker-in-docker
在docker容器种使用docekr.这种方式需要以特权方式执行docker，带来不安全的因素。同时，构建也是非常慢的。因此也需要使用缓存去加速构建。
原理是：docker先从registry拉取上次构建的镜像。然后构建的时候指定--cache-from=<last-image>，也就是说以上次的镜像作为缓存构建。
构建完毕后，上次镜像，作为下次的构建缓存使用。但是需要注意的是，仍需要花费一部分时间在download image上。如果registry在内网，其实下载和上传都是蛮快的，可以接受。
[文档](https://docs.gitlab.com/ee/ci/docker/using_docker_build.html#use-docker-in-docker-executor)
这种方式是使用需要运行在特权模式privileged下的特殊的 Docker 镜像——docker-in-docker（dind）和所安装的 docker 工具来执行脚本，GitLab Runner 注册选择 docker 和privileged模式。
```
sudo gitlab-runner register -n \
   --url https://gitlab.com/ \
   --registration-token REGISTRATION_TOKEN \
   --executor docker \
   --description "My Docker Runner" \
   --docker-image "docker:stable" \
   --docker-privileged
```
以上命令将注册一个使用docker:stable镜像的 Runner，它使用privileged模式启动构建和服务容器。这也是使用docker-in-docker模式必须使用的设置
>注意：通过--docker-privileged启用特权模式，禁用容器的所有安全机制，并将主机暴露在权限提升中，这可能导致容器中断。更多信息查看 Docker 官方文档运行时特权和 linux 功能
上面的命令得到对应配置文件如下
```
 [[runners]]
   url = "https://gitlab.com/"
   token = TOKEN
   executor = "docker"
   [runners.docker]
     tls_verify = false
     image = "docker:stable"
     privileged = true
     disable_cache = false
     volumes = ["/cache"]
   [runners.cache]
     Insecure = false
```
.gitlab-ci.yml例子如下，[参考](https://gitlab.com/gitlab-examples/docker)
```
image: docker:latest

services:
  - docker:dind

build:
  stage: build
  script:
    - docker build -t test .
```
缺点和不足如下：
- 使用 docker-in-docker 时，每个作业都处于干净的环境中，没有过去的历史记录。并发任务执行正常，因为每个构建都有自己的 Docker 引擎实例，因此它们不会相互冲突。但这也意味着工作可能会变慢，因为没有层缓存
- 默认情况下，docker:dind 使用的--storage-driver vfs 是最慢的形式。要使用其他驱动程序，请参阅 使用 overlayfs 驱动程序
- 由于 docker:dind 容器和运行器容器不共享其根文件系统，因此任务的工作目录可用作子容器的安装点。例如，如果您要与子容器共享文件，则可以在/builds/$CI_PROJECT_PATH 其下创建子目录并将其用作挂载点（有关更详细的说明，请查看问题＃41227）使用 Docker 套接字绑定

##### (2.)docker socket binding(挂载宿主机Docker)
镜像中安装docker-ce。运行镜像时把host的docker.socks映射到容器内，这样容器内就可以直接使用host的docker服务。容器内看到的镜像和容器都是host上的。

>注意：如果在使用 GitLab Runner 11.11 或更高版本时绑定 Docker 套接字，则无法再将其 docker:dind 用作服务，因为也会对服务进行卷绑定，从而使这些服务不兼容

docker本身具有挂载相应的目录，文件到容器之中的能力，我们直接将docker命令以及docker daemon的socket文件挂载进运行容器之中即可运行docker命令。 但是注意，在容器内部实际上使用的是宿主机的docker进程，因此我们对镜像以及容器的处理其实都是在宿主机这个视角下。
同时同宿主机的docker环境交互，不便于镜像的管理，会在宿主机上留下过多的镜像残留垃圾。

Runner 注册命令如下
```
sudo gitlab-runner register -n \
   --url https://gitlab.com/ \
   --registration-token REGISTRATION_TOKEN \
   --executor docker \
   --description "My Docker Runner" \
   --docker-image "docker:stable" \
   --docker-volumes /var/run/docker.sock:/var/run/docker.sock
```
以上命令将注册一个使用docker:stable镜像的 Runner。注意：他是用的是 Runner 本身的 Docekr 守护程序，而 docker 命令生成的任何容器都是 Runner 的兄弟，而不是 Runner 的子节点。
上面的命令得到对应配置文件如下
```
 [[runners]]
   url = "https://gitlab.com/"
   token = REGISTRATION_TOKEN
   executor = "docker"
   [runners.docker]
     tls_verify = false
     image = "docker:stable"
     privileged = false
     disable_cache = false
     volumes = ["/var/run/docker.sock:/var/run/docker.sock", "/cache"]
   [runners.cache]
     Insecure = false
```
对应的.gitlab-ci.yml例子如下
```
image: docker:stable

before_script:
  - docker info

build:
  stage: build
  script:
    - docker build -t my-docker-image .
    - docker run my-docker-image /script/to/run/tests
```
可以看到，这个模式不需要使用服务，直接通过套接字通信。此模式也是有一些需要注意的地方：
- 由于是共享 docker 守护程序，项目的操作会真实产生影响。比如项目如果运行docker rm -f $(docker ps -a -q)，那么将会删除所有容器
- 并发可能会有冲突，比如创建相同的名称的容器
- 由于创建的容器是 Runnner 的兄弟，所以文件与目录的共享是在主机上下文完成，而不是构建容器上下文

由于此方式最终实际上是使用的host的docker daemon，因此，镜像和构建的缓存都是直接使用host中的缓存。当然，有利就有弊，此种方式的缺点有：

- 由于共享了主机的docker socket，所以docker命令都是向主机发出的命令，比如docker rm -f $(docker ps -a -q)会把主机上的所有docker容器删除了，包括gitlab-runner容器。
- 并发工作可能无法正常执行；创建具有特定名称的容器，则它们可能会相互冲突。
- 将源仓库中的文件和目录共享到容器中可能无法正常工作，因为卷安装是在主机而不是构建容器的上下文中完成的。
- 你必须时刻注意，你的docker命令是在主机执行的，而不是容器内部。
- 需要修改gitlab-runner的配置，挂载主机的docker socket，但是不同的host system的sock文件路径不同，这目前只能在host上配置。
- 在k8s中，docker binding脱离了k8s的控制，是非常危险的行为。有的k8s集群通过名称空间做环境隔离，想想一下，开发环境的docker命令删除了线上环境的容器。

如何绑定docker.sock?
修改gitlab-runner服务的配置文件 /srv/gitlab-runner/config/config.toml
```
volumes = ["/cache","/var/run/docker.sock:/var/run/docker.sock"]
```

##### (3.)Docker中实现运行Docker总结
选择两种方式都各有好坏，可根据实际情况进行选择。这里还是推荐用第二种，因为第一种真的很干净，所以很慢，但是需要做好权限管理和控制，避免危险的脚本
还有一点是，指定镜像版本的时候，最好指定具体的版本。比如使用第一种模式，引入服务docker:dind，最好使用docker:18.09.8-dind。避免镜像拉取策略，每次拉取最新的镜像，导致实际是docker:19.0-dind，与安装的 docker 版本不符，发生一些意想不到的错误。
两种方法的优缺点
|优点|缺点|
|-|-|
|挂载宿主机docker	|简单，易上手	|隔离性不好，依赖宿主机|
|使用docker in docker的官方镜像	|安全，隔离性好	|无法集成到已经构建好的镜像环境|

>挂载宿主机docker，多用在以容器运行的环境，而且对安全要求不高的平台。

### 7.executor(执行器)总结
docker executor是最好的选择。尤其是构建软件的版本（或docker image），一般都可以通过cicd文件配置。运维只需要安装gitlab-runner程序就可以了，绝大多数时候无需对gitlab-runner程序进行配置。
这就是说，所有的运维工作都可以使用cicd文件管理，如果你想新增一个gitlab-runner服务，只需要安装即可。不过现在国内的docker executor文档比较少且不详细，经常需要查阅官网资料，这对英语水平有一定要求。

# 四.GitLab编写ci、cd流程文件
### 1.Pipeline & Stages & Jobs#
.gitlab-ci.yml文件会告诉GitLab Runner 做什么。
如果将.gitlab-ci.yml文件添加到存储库的根目录，并将GitLab项目配置为使用Runner，则每次提交或推送都会触发CI 管道。也就是说在对存储库进行任何推送时，
在GitLab都会寻找.gitlab-ci.yml文件，并对此次commit开始并根据该文件的内容在Runners上启动作业，jobs的内容来源于.gitlab-ci.yml文件。
定义pipeline的全部阶段（stage），阶段内所有任务并行执行，全部执行成功开始下一阶段任务，任何阶段内任意job执行失败都会导致pipeline失败，所有stage，job执行成功后pipeline会显示pass。如果未定义stages，则默认有build、test、deploy三个阶段，如果未定义stage，则默认test阶段

一个 Pipeline 大概相对于一个构建任务，里面可以包含多个流程，如安装依赖、运行测试、编译、部署测试服务器、部署生产服务器等流程，
Git 提交时会触发 Pipeline。而一个 Pipeline 中又可以包含一至多个 Stage，即用来定义安装依赖、运行测试之类的流程的。然后，一个 Stage 中又包含了一至多个 Job，
Jobs 表示一个 Stage 中具体的构建工作，即某个 Stage 里面执行的工作。我们可以在 Stages 里面定义这些 Job，它们之间的关系如下图所示：

注意：
Stages 会按 .gitlab-ci.yml 中配置的顺序执行，当前面的 Stage 执行完毕后才会继续执行后面的 Stage，如果一个 Stage 失败，那么后面的 Stage 不会执行，该构建任务失败。
Stage 中的 Jobs 会并行执行，当这个 Stage 中所有的 Job 都执行完毕，该 Stage 才算执行成功。换而言之，只要有一个 Job 执行失败，整个 Pipeline 也就失败了。

### 2.创建一个简单的.gitlab-ci.yml
注意：.gitlab-ci.yml是一个YAML文件，所以必须要格外注意锁紧。使用空格，而不是tabs。
在项目的根目录创建一个名为.gitlab-ci.yml的文件。

```
stages:
- build
- test
- deploy

build_project:
  stage: build
  script:
  - echo "配置构建环境....."
  - echo "开始构建....."
  - echo "构建完成"

test_project:
  stage: test
  script:
  - echo "配置测试环境....."
  - echo "执行测试脚本....."
  - echo "测试完毕"

deploy_project:
  stage: deploy
  script:
  - echo "配置部署项目...."
  - echo "部署项目...."
  - echo "部署完成"
```

在每个jobs之前，before_script定义的命令都将会被执行。
.gitlab-ci.yml定义了三个build_maven，test_springboot和deploy_springboot（名字可以随便取）jobs，他们执行不同的命令。
其中包含如何运行和何时运行的限制。jobs必须定义一个stages元素，而且总是必须包含script关键字。

如果你想检验.gitlab-ci.yml文件的语法是否正确，在GitLab实例页面中有一个命令行工具/ci/lint。也可以从项目中的CI/CD->ci/lint 找到命令行工具进行验证。 关于更多.gitlab-ci.yml的信息和语法，请阅读.gitlab-ci.yml参考文档。

将.gitlab-ci.yml文件push到远程仓库.
现在到Pipelines页面查看，将会看到该Pipline处于等待状态。
![](https://upload-images.jianshu.io/upload_images/3067896-d19bfec0c7d5ea68.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
因为我们只定义了任务并没有定义由哪个runner去执行这个脚本.
接着我们打开Project的setting->CI/CD->Runners/Expand->对应Runners edit按钮->勾选Indicates whether this runner can pick jobs without tags(指示此运行程序是否可以拾取没有标记的作业)->save change
![](https://upload-images.jianshu.io/upload_images/3067896-948be32f731268e4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
再次到Pipelines页面查看，将会看到该该任务执行完毕.

当有新内容push到仓库，或者有代码合并后，GitLab会查找是否有.gitlab-ci.yml文件，如果文件存在，Runners将会根据该文件的内容开始build本次commit。


### 3.Job关键字
##### (1.)不可以被用于 Job名 的保留字
|关键字|是否必须|描述|
|-|-|-|
|image|no|使用的docker镜像。|
|services|no|使用的docker服务。|
|stages|no|定义构建场景|
|types|no|stages的别名(不赞成使用)|
|before_script	|no	|定义每个任务的脚本启动前所需执行的命令|
|after_script	|no	|定义每个任务的脚本执行结束后所需执行的命令|
|variables	|no	|定义构建变量|
|cache	|no	|定义哪些文件需要缓存，让后续执行可用|

##### (2.)Job 的保留字
|关键字	|是否必须|描述|
|-|-|-|
|script|	yes	|Runner执行的命令或脚本。可以包含多条命令|
|image	|no	|使用的docker镜像。详见|
|services	|no	|使用的docker服务。详见|
|stage	|no	|定义job stage（默认：test）|
|type	|no	|stage的别名（已弃用）|
|variables	|no	|定义job级别的变量|
|only	|no	|定义一列git分支，并为其创建job|
|except	|no	|定义一列git分支，不创建job|
|tags	|no	|定义一列tags，用来指定选择哪个Runner（同时Runner也要设置tags）|
|allow_failure	|no	|允许job失败。失败的job不影响commit状态|
|when	|no	|定义何时开始job。可以是on_success，on_failure，always或者manual|
|dependencies	|no	|定义job依赖关系，这样他们就可以互相传递artifacts|
|cache	|no	|定义应在后续运行之间缓存的文件列表|
|before_script	|no	|重写一组在作业前执行的命令|
|after_script	|no	|重写一组在作业后执行的命令|
|environment	|no	|定义此作业完成部署的环境名称|
|coverage	|no	|定义给定作业的代码覆盖率设置|

##### (3.)only and except 保留字
|关键字|	描述|
|-|-|
|branches|	当一个分支被push上来|
|tags|	当一个打了tag的分支被push上来|
|api|	当一个pipline被piplines api所触发调起，详见piplines api|
|external|	当使用了GitLab以外的CI服务|
|pipelines|	针对多项目触发器而言，当使用CI_JOB_TOKEN并使用gitlab所提供的api创建多个pipelines的时候|
|pushes	|当pipeline被用户的git push操作所触发的时候|
|schedules|	针对预定好的pipline而言（每日构建一类）|
|triggers|	用token创建piplines的时候|
|web|	在GitLab页面上Pipelines标签页下，你按了run pipline的时候|

#### (4.)gitlab-runner标签关键字（Tags）
注册runner的时候，可以给它添加一个Tag(标签)。添加标签以后，就可以在CI/CD配置文件里，通过标签来调用特定的Runner.
例如我们有三个runner:build_runner.test_runner.deploy_runner，经过如下配置，build_project会在build_runner上执行，test_project会在test_runner上执行，
deploy_project会在deploy_runner上执行
```
stages:
- build
- test
- deploy

build_project:
  stage: build
  script:
  - echo "配置构建环境....."
  - echo "开始构建....."
  - echo "构建完成"
  tags:
  - build_runner

test_project:
  stage: test
  script:
  - echo "配置测试环境....."
  - echo "执行测试脚本....."
  - echo "测试完毕"
  tags:
  - test_runner
  
deploy_project:
  stage: deploy
  script:
  - echo "配置部署项目...."
  - echo "部署项目...."
  - echo "部署完成"
  tags:
  - deploy_runner
```

- variables	no	定义job层次的变量
- only	no	定义哪些分支或tag的修改触发该流程
- except	no	定义哪些分支或tag的修改不触发该流程
- tags	no	定义哪个标签的runner来执行，该标签指runner配置时的名称，不是Git的tag分支
- dependencies	no	定义该job依赖于哪项job的结果，用于把之前job的附件传进来
- artifacts	no	定义job产生的附件，可用于下载和保存以及传递，没有该项设置产生的过程文件都会被删除
- cache	no	定义缓存的文件或文件夹，如果是在job外定义则为全局变量
- before_script	no	定义job执行前的操作
- after_script	no	定义job执行后的操作
- retry	no	定义任务失败后的重复执行次数或时间
- parallel	no	定义并行的任务数量，限于2~50

### 4.Job重要的关键字解析
##### (1.)after_script

before_script 和 script 在一个上下文中是串行执行的，after_script 是独立执行的。所以根据执行器(在runner注册的时候，可以选择执行器，docker，shell 等)的不同，工作树之外的变化可能不可见，例如，在before_script中执行软件的安装。

你可以在任务中定义 before_script，after_script，也可以将其定义为顶级元素，定义为顶级元素将为每一个任务都执行相应阶段的脚本或命令。

##### (2.)variables

GitLab CI允许你为.gitlab-ci.yml增加变量，该变量将会被设置入任务环境。这些变量是你存储在git仓库里，并且非敏感的项目配置，例如:
```
variables:
    DATABASE_URL: "postgres://postgres@postgres/my_database"
```
>注意:整数和字符串一样，对于设置变量名和变量值来说都是合法的。但浮点数是非法的。


script
script是一段由Runner执行的shell脚本，例如：
```
job:
    script: "bundle exec rspec"
```
这个参数也可以使用数组包涵好几条命令：
```
job:
    script:
        - uname -a
        - bundle exec rspec
```
注意：有些时候，script命令需要被单引号或者双引号所包裹。例如：当命令中包涵冒号的时候，该命令需要被引号所包裹。这样YAML解析器才知道该命令语句不是“key: value”语法的一部分。当命令中包涵以下字符时需要注意打引号:`: { } [ ] , & * # ? | - < > = ! % @ ``

##### (3.)Stages
Stages 表示构建阶段，说白了就是上面提到的流程。默认有3个stages：build， test， deploy。也可以自行添加多个.我们可以在一次 Pipeline 中定义多个 Stages，这些 Stages 会有以下特点：
- 所有 Stages 会按照顺序运行，即当一个 Stage 完成后，下一个 Stage 才会开始
- 只有当所有 Stages 完成后，该构建任务 (Pipeline) 才会成功
- 如果任何一个 Stage 失败，那么后面的 Stages 不会执行，该构建任务 (Pipeline) 失败

stage翻译为阶段的意思，在构建的过程中，必须要有一个先后顺序。最上面的stages配置意思是，先构建阶段为build的job，然后再构建阶段为test的job，下面build_job和test_job都是job，
如果不配置stages，默认为：
```
stages:
- build
- test
- deploy
```
stages的允许定义多个，灵活的场景阶段的pipline。定义的元素的顺序决定了任务执行的顺序。例如：
```
    stages:
      - build
      - test
      - deploy
```
build场景的任务将被并行执行。test、deploy 同理
build 任务成功后，test 执行。test 成功后，deploy 执行
所有的都成功了，提交将会标记为成功
任何一步任务失败了，提交标记为失败并之后的场景，任务都不回执行。

##### (4.)Jobs
Jobs 表示构建工作，表示某个 Stage 里面执行的工作。我们可以在 Stages 里面定义多个 Jobs，这些 Jobs 会有以下特点：
1. 相同 Stage 中的 Jobs 会并行执行
2. 相同 Stage 中的 Jobs 都执行成功时，该 Stage 才会成功
3. 如果任何一个 Job 失败，那么该 Stage 失败，即该构建任务 (Pipeline) 失败

##### (5.)only and except

only和except两个参数说明了job什么时候将会被创建:

only定义了job需要执行的所在分支或者标签
except定义了job不会执行的所在分支或者标签
以下是这两个参数的几条用法规则：

only和except如果都存在在一个job声明中，则所需引用将会被only和except所定义的分支过滤.
only和except允许使用正则
only和except允许使用指定仓库地址，但是不forks仓库
例子解析：

job将会只在issue-开头的refs下执行，反之则其他所有分支被跳过：
```
job:
    # use regexp
    only:
        - /^issue-.*$/
    # use special keyword
    except:
        - branches
```
job只会在打了tag的分支，或者被api所触发，或者每日构建任务上运行，
```
job:
    # use special keywords
    only:
        - tags      # tag 分支 commit 之后触发
        - triggers  # API 触发
        - schedules # 每日构建触发
```
job将会在父仓库gitlab-org/gitlab-ce的非master分支有提交时运行。
```
job:
    only:
        - branches@gitlab-org/gitlab-ce
    except:
        - master@gitlab-org/gitlab-ce
```
在计划被触发时或者master分支被push时触发，并且先决条件是kubernetes服务是活跃的（你启用了kubernetes服务作为执行器，相关请看gitlab ci runner的文档，ce用户一般用求不到）
```
job:
    only:
        refs:
            - master
            - schedules
        kubernetes: active
```

##### (6.)artifacts

artifacts 被用于在 job 作业成功后将制定列表里的文件或文件夹附加到 job 上，传递给下一个 job ，如果要在两个 job 之间传递 artifacts，你必须设置dependencies，下面有几个例子

传递所有binaries和.config：
```
artifacts:
    paths:
        - binaries/
        - .config
```
传递所有git没有追踪的文件
```
artifacts:
    untracked: true
```
传递binaries文件夹里所有内容和git没有追踪的文件
```
artifacts:
    untracked: true
    paths:
        - binaries/
```
禁止传递来的artifact:
```
job:
    stage: build
    script: make build
    dependencies: []
```
只为打tags的行为创建artifacts。artifacts将会在job执行完毕后送到GitLab ui前台来，你可以直接下载它(tag、details、pipeline 的下载按钮上都会出现)。
```
default-job:
    script:
        - mvn test -U
    except:
        - tags

release-job:
    script:
        - mvn package -U
    artifacts:
        paths:
            - target/*.war
        only:
            - tags
artifacts:name
```
name指令允许你对artifacts压缩包重命名，你可以为每个artifect压缩包都指定一个特别的名字，这样对你在gitlab上下载artifect的压缩包有用
```
job:
    artifacts:
        name: "$CI_JOB_NAME"
artifacts:when
```
用于job失败或者未失败时使用。artifacts:when能设置以下值：

on_success 这个值是默认的，当job成功时上传artifacts
on_failure 当job执行失败时，上传artifacts
always 不管失败与否，都上传
```
job:
    artifacts:
        when: on_failure    #当失败时上传artifacts
artifacts:expire_in
artifacts:expire_in 用于设置 artifacts 上传包的失效时间. 如果不设置，artifacts 的打包是永远存在于 gitlab上 的。当指定 artifacts 过期时间的时候， 在该期间内，artifacts 包将储存在 gitLab 上。并且你可以在 job 页面找到一个 keep 按钮，按了以后可以覆盖过期时间，让 artifacts 永远存在。过期之后，用户将无法访问到 artifacts 包。时间的例子如下:
```
'3 mins 4 sec'
'2 hrs 20 min'
'2h20min'
'6 mos 1 day'
'47 yrs 6 mos and 4d'
'3 weeks and 2 days'
```
job:
    artifacts:
        expire_in: 1 week # 一周后过期
```

##### (7.)Triggers

Triggers被用于重建特定分支，tag或者commit，他是api触发的。

##### (8.)image
使用的docker 镜像，这里docker镜像的地址，也可用：image:name和image:entrypoint。
##### (9.)services
使用docker服务映像。也可用：services:name，services:alias，services:entrypoint，和services:command。
### 5.Job综合示例
```
# 定义 stages（阶段）。任务将按此顺序执行。
stages:
  - build
  - test
  - deploy

# 定义 job（任务）
job1:
  stage: test
  tags:
    - XX #只有标签为XX的runner才会执行这个任务
  only:        
    - dev    #只有dev分支提交代码才会执行这个任务。也可以是分支名称或触发器名称
    - /^future-.*$/ #正则表达式，只有future-开头的分支才会执行
  script:
    - echo "I am job1"
    - echo "I am in test stage"

# 定义 job
job2:
  stage: test    #如果此处没有定义stage，其默认也是test
  only:
    - master    #只有master分支提交代码才会执行这个任务
  script:
    - echo "I am job2"
    - echo "I am in test stage"
  allow_failure: true #允许失败，即不影响下步构建    

# 定义 job
job3:
  stage: build
  except:    
    - dev #除了dev分支，其它分支提交代码都会执行这个任务
  script:
    - echo "I am job3"
    - echo "I am in build stage"    
  when: always #不管前面几步成功与否，永远会执行这一步。它有几个值：on_success （默认值）\on_failure\always\manual（手动执行）
    
# 定义 job
.job4:    #对于临时不想执行的job，可以选择在前面加个"."，这样就会跳过此步任务，否则你除了要注释掉这个jobj外，还需要注释上面为deploy的stage
  stage: deploy
  script:
    - echo "I am job4"    

# 模板，相当于公用函数，有重复任务时很有用
.job_template: &job_definition  # 创建一个锚，'job_definition'
  image: ruby:2.1
  services:
    - postgres
    - redis

test1:
  <<: *job_definition           # 利用锚'job_definition'来合并
  script:
    - test1 project

test2:
  <<: *job_definition           # 利用锚'job_definition'来合并
  script:
    - test2 project    

 

before_script:
  - echo "每个job之前都会执行"    
  
after_script:
  - echo "每个job之后都会执行"    

#下面几个都相当于全局变量，都可以添加到具体job中，这时会被子job的覆盖     
variables:    #变量
  DATABASE_URL: "postgres://postgres@postgres/my_database"  #在job中可以用${DATABASE_URL}来使用这个变量。常用的预定义变量有CI_COMMIT_REF_NAME（项目所在的分支或标签名称），CI_JOB_NAME（任务名称），CI_JOB_STAGE（任务阶段）
  GIT_STRATEGY: "none" #GIT策略，定义拉取代码的方式，有3种：clone/fetch/none，默认为clone，速度最慢，每步job都会重新clone一次代码。我们一般将它设置为none，在具体任务里设置为fetch就可以满足需求，毕竟不是每步都需要新代码，那也不符合我们测试的流程

cache:    #缓存
  #因为缓存为不同管道和任务间共享，可能会覆盖，所以有时需要设置key
  key: ${CI_COMMIT_REF_NAME}  # 启用每分支缓存。
  #key: "$CI_JOB_NAME/$CI_COMMIT_REF_NAME" # 启用每个任务和每个分支缓存。需要注意的是，如果是在windows中运行这个脚本，需要把$换成%
  untracked: true    #缓存所有Git未跟踪的文件
  paths:    #以下2个文件夹会被缓存起来，下次构建会解压出来
    - node_modules/
    - dist/  

```
### 6.使用docker关键字
image该关键字指定一个任务（job）所使用的docker镜像，例如image: python:latest使用Python的最新镜像。
镜像下载的策略：
- never： 当使用这个策略，会禁止Gitlab Runner从Docker hub或者其他地方下拉镜像，只能使用自己手动下拉的镜像
- if-not-present： 当使用这个策略，Runner会先检测本地是否有镜像，有的话使用该镜像，如果没有再去下拉。这个策略如果再配合定期删除镜像，就能达到比较好的效果。
- always： 这个是gitlab-ci默认使用的策略，即每一次都是重新下拉镜像，导致的结果就是比较耗时间

services
该关键字指向其他Docker镜像，这些镜像会与image关键字指定的镜像绑定（link）。比如可以绑定一个mysql服务，存储单元测试所需要的假数据。
```
default_job:
image: python:3.6

services:
- mysql:5.7

before_script:
- apt-get install mysql-client
  复制代码before_script和after_script
  before_script关键字定义了一组在每个任务开始之前需要执行的命令，after_script则相反。例如可以在before_script做好ssh连接的准备，见下文。
  注：before_script可以针对全部任务，也可以针对单个任务。
```

# 五.gitlab ci/cd触发
### 1.gitlab ci/cd Triggers
创建一个用于流水线触发的认证token：
![](https://img-blog.csdnimg.cn/img_convert/4529f375ab95ecb250578808c5912dfc.png)
##### (1.)使用API触发

使用curl命令进行测试
```
curl -X POST \
     -F token=b2ba95b229f5fd0eb834454bc9aad8 \
     -F ref=main \
     http://192.168.1.200/api/v4/projects/31/trigger/pipeline
```
使用postman测试

![](https://img-blog.csdnimg.cn/img_convert/ff003c0f02a2c77d3d95cc06f17c838f.png)

##### (2.)gitlabci作业中触发
```
script:
  - "curl -X POST -F token=TOKEN -F ref=REF_NAME http://192.168.1.200/api/v4/projects/31/trigger/pipeline"
```
优化：将token以变量的方式存储到项目中。
```
stages:         
  - build
 
build-job: 
  tags:
    - build     
  stage: build
  script:
    - "curl -X POST -F token=${CITOKEN} -F ref=main  http://192.168.1.200/api/v4/projects/29/trigger/pipeline"
    - echo "Compile complete."
    - sleep 1
 ```

##### (3.)触发并传递参数
```
curl -X POST \
     -F token=TOKEN \
     -F "ref=main" \
     -F "variables[BUILD_TOOL]=mavenandmaven" \
     http://192.168.1.200/api/v4/projects/31/trigger/pipeline
```
.gitlab-ci.yml:
```
ciTriggerTest:
  tags:
    - build
  stage: build
  script:
    - echo ${BUILD_TOOL}
```

# 六.Android 项目配置 gitlab-ci 持续集成
```
image: openjdk:8-jdk

variables:
  ANDROID_COMPILE_SDK: "28"
  ANDROID_BUILD_TOOLS: "28.0.2"
  ANDROID_SDK_TOOLS:   "4333796"

before_script:
  - apt-get --quiet update --yes
  - apt-get --quiet install --yes wget tar unzip lib32stdc++6 lib32z1
  - wget --quiet --output-document=android-sdk.zip https://dl.google.com/android/repository/sdk-tools-linux-${ANDROID_SDK_TOOLS}.zip
  - unzip -d android-sdk-linux android-sdk.zip
  - echo y | android-sdk-linux/tools/bin/sdkmanager "platforms;android-${ANDROID_COMPILE_SDK}" >/dev/null
  - echo y | android-sdk-linux/tools/bin/sdkmanager "platform-tools" >/dev/null
  - echo y | android-sdk-linux/tools/bin/sdkmanager "build-tools;${ANDROID_BUILD_TOOLS}" >/dev/null
  - export ANDROID_HOME=$PWD/android-sdk-linux
  - export PATH=$PATH:$PWD/android-sdk-linux/platform-tools/
  - chmod +x ./gradlew
  # temporarily disable checking for EPIPE error and use yes to accept all licenses
  - set +o pipefail
  - yes | android-sdk-linux/tools/bin/sdkmanager --licenses
  - set -o pipefail

stages:
  - build
  - test

lintDebug:
  stage: build
  script:
    - ./gradlew -Pci --console=plain :app:lintDebug -PbuildDir=lint

assembleDebug:
  stage: build
  script:
    - ./gradlew assembleDebug
  artifacts:
    paths:
    - app/build/outputs/

debugTests:
  stage: test
  script:
    - ./gradlew -Pci --console=plain :app:testDebug
```

推荐一个 Docker Android 镜像：[docker-android-sdk](https://hub.docker.com/r/runmymind/docker-android-sdk)
对 CI  .gitlab-ci.yml  文件内容修改，更换镜像，避免每次都下载 Android SDK ：
```
image: runmymind/docker-android-sdk:latest

before_script:
  - chmod +x ./gradlew

stages:
  - build

assembleDebug:
  stage: build
  script:
    - ./gradlew clean
    - ./gradlew assembleDebug
  artifacts:
    paths:
    - app/build/outputs/
  only:
    - master

assembleRelease:
  stage: build
  script:
    - ./gradlew clean
    - ./gradlew assembleRelease
  artifacts:
    paths:
    - app/build/outputs/
  only:
    - master
```

.gitlab-ci.yml脚本文件语法介绍
```
# 就是上文说的stages
stages:
  - build_debug # 这里就是一个stage，可以定义多个stage，这个stage就是下面的build_debug

# 构建之前会执行的脚本，这里导入本地的环境变量
before_script:
  - export ANDROID_HOME=/Users/work/Android/SDK
  - export PATH=$PATH:${ANDROID_HOME}/tools
  - export PATH=$PATH:${ANDROID_HOME}/platform-tools
  - chmod +x ./gradlew

# 声明一个名叫build_debug的构建任务
build_debug:
  stage: build_debug
  # 构建中，执行一些脚本
  script:
    - ./gradlew --stacktrace assembleDevelopDebug
  # 指定监听哪一个分支或什么时候触发Pipeline
  only: 
    - tags #这里tags的作用是当修改gitlab项目tag的时候会触发
    - test # 监听GitLab的这个分支
  #    - master
  # 指定由哪一个runner运行
  tags:
    - dev # 这个dev是上文注册Runner时的tag，和注册时候tag一样的话就会用对应的Runner来执行任务
  # 指定成功后应附加到任务的文件和目录的列表
  artifacts:
    paths:
      - app/build/outputs/

# 构建完成之后执行的脚本
#after_script:
#  - 这里如果是要配合monkey的话，一般在这个地方执行monkey的脚本
```

配置Android工程
runner配置好后，接下来的工作就是配置Android项目，只需要在工程目录下创建.gitlab-ci.yml配置文件，然后往里面填充你想要实现的步骤即可，有点类似Jenkins中的pipeline脚本。不过，感觉gitlab ci的配置更加简单一些。
```
image: gitlab-ci-android:V2 # 用来编译 android 项目的镜像
variables:
  GRADLE_OPTS: "-Dorg.gradle.daemon=false" # 禁用 gradle 守护进程
before_script:
  #  配置 gradle 的缓存目录
  - export GRADLE_USER_HOME=/cache/.gradle
  #  获取权限
  - chmod +x ./gradlew
  - chmod +x ./update-version-code.sh
stages:
  - build
# 提交代码自动编译
build:
  stage: build
  only:
    - master
  script:
    - ./gradlew assembleDebug
  tags:
    - android
# 构建测试包
qa:
  stage: build
  only:
    - qa
  script:
    - ./gradlew assembleDebug
    - sh -x /cache/deploy-android.sh
  artifacts:
    paths:
      - app/build/outputs/apk/debug/
  tags:
    - android
```
上面配置的大致意思是：当开发往qa分支提交代码时，会触发构建测试包，打包完成后，会将包上传到一个文件服务器上，方便下载安装。

```
image: seanghay/android-ci
before_script:
  - chmod +x ./gradlew
stages:
  - build
cache:
  paths:
    - .gradle/wrapper
    - .gradle/caches
assembleDebug:
  stage: build
  script:
    - ./gradlew assembleDebug
    - cp app/build/outputs/apk/debug/app-debug.apk app-debug.apk
  artifacts:
    paths:
      - app-debug.apk
```


配置 runner 缓存路径
在服务器上找一个文件夹挂载到 docker 容器里边，给 .gradle 做一个缓存，这样每次编译的时候，就不用一直下载 gradle 了，这里我挂载的是 /home/android-cache 文件夹：
```
vi /etc/gitlab-runner/config.toml
```
![](https://img-blog.csdnimg.cn/410e2f809177436ebf8eb5add59fcd9d.png?x-oss-process=image/watermark,type_ZHJvaWRzYW5zZmFsbGJhY2s,shadow_50,text_Q1NETiBAd2RlbzM2MDE=,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center)
```
pull_policy = "if-not-present" 避免docker 镜像每次都pull
```
>注意，如果你的 gitlab 服务器迁移了之后，如果不想再重新注册 runner，可以改这个配置文件的 url 和 token 为迁移后的值

参考资料:
[GitLab CI/CD 介绍和使用](http://blinkfox.com/2018/11/22/ruan-jian-gong-ju/devops/gitlab-ci-jie-shao-he-shi-yong/#toc-heading-8)
[超简单配置Android持续集成自动化打包流程 - GitHub+GitLab-CI+蒲公英+钉钉](https://www.jianshu.com/p/e0553d3ac743/)
[Android 项目配置 gitlab-ci 持续集成](https://www.cnblogs.com/aimqqroad-13/p/10115799.html)
[Android 持续集成实践（二）——配置 Docker + gitlab-runner 实现线上自动编译](https://blog.csdn.net/Captive_Rainbow_/article/details/90407356)
[Android 持续集成实践（三）——编写 .gitlab-ci.yml 实现自动化](https://blog.csdn.net/Captive_Rainbow_/article/details/90480269)
[Android 持续集成实践（四）——配置 WebHook 通知编译结果](https://blog.csdn.net/Captive_Rainbow_/article/details/90634669)
