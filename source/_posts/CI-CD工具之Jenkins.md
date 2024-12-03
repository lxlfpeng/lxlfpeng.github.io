---
title: CI-CD工具之Jenkins
date: 2019-07-10
categories: 
  - CI/CD
---

# 一.CI/CD(持续集成/持续部署)
软件开发周期中需要一些可以帮助开发者提升速度的自动化工具。其中工具最重要的目的是促进软件项目的持续集成与交付。通过CI/CD工具，开发团队可以保持软件更新并将其迅速的投入实践中。CI/CD也被认为是敏捷开发的最重要实践之一。
具体而言，CI/CD 可让持续自动化和持续监控贯穿于应用的整个生命周期（从集成和测试阶段，到交付和部署）。这些关联的事务通常被统称为"CI/CD 管道"，由开发和运维团队以敏捷方式协同支持。
### 1.持续集成
Continuous Integration：持续集成，简称CI，是软件开发周期的一种实践，把代码仓库（Gitlab或者Github）、构建工具（如Jenkins）和测试工具（SonarQube）集成在一起，频繁的将代码合并到主干然后自动进行构建和测试。
### 2.持续交付
Continuous Delivery：持续交付，简称CD，是在CI的基础进行了扩展，在CI环节完成了软件构建和测试工作并形成了新的版本，那么接下来就要进行交付，而这里的交付并不是交付到生产环境，而是类生产环境（STAGING），我们可以理解为灰度环境或者预发环境，进而接受部分真实流量的测试。如果没有问题的话则通过手动的方式部署到生产环境。

# 二.安装配置Jenkins
[Jenkins](https://github.com/jenkinsci/jenkins) 是一个可扩展的持续集成引擎。主要用于持续、自动的构建/测试软件项目、监控外部任务的运行。Jenkins用Java语言编写，可在Tomcat等流行的servlet容器中运行，也可独立运行。通常与版本管理工具(SCM)、构建工具结合使用。常用的版本控制工具有SVN、GIT，构建工具有Maven、Ant、Gradle。
### 1.手动安装Jenkins
##### (1.)安装依赖
- Jenkins使用java开发，首先必然需要安装jdk。
##### (2.)Jenkins安装
下载地址：https://jenkins.io/download/
可直接使用以下命令启动Jenkins：
```
java -jar jenkins.war
```
如果使用tomcat，那么在jenkins下载完后将war包直接复制到tomcat的webapps目录下，然后启动tomcat（windows点startup.bat）
**启动完成后直接访问链接：http://localhost:8080/jenkins/**
##### (3.)jenkins初始化配置
1. 初次访问http://localhost:8080/jenkins，会需要输入密码，根据指引可以在对于目录找到密码输入。
2. 进入后下一界面是要安装插件，如下图所示。如果不熟悉推荐直接点“Install suggested plugins”即可，真要增删插件以后也可以通过“Manage Jenkins > Manage Plugins”修改。
![](/images/45618340235895cf36275a2b787621d4.webp)
3. 进入如下界面，等待其自动完成即可
![](/images/e7596fd14f03d018d30f9fa1bb6be443.webp)
4. 下一步是创建管理员账号用于以后登录和管理，按自己想要的建即可
![](/images/373ced32c76508ca7984edc2fa92ef17.webp)

[image.png](https://upload-images.jianshu.io/upload_images/3067896-1f5911c48b29f2ab.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
2.全局工具配置->配置JDK，Git，Gradle
[image](https://img-blog.csdn.net/20180726150053443?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JpbmJpbnFxODY=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
### 2.Docker安装Jenkins
1. 启动docker，下载Jenkins镜像文件
```
docker pull jenkins/jenkins
```
2. 创建Jenkins挂载目录并授权权限
```
mkdir -p /var/jenkins_mount
chmod 777 /var/jenkins_mount
```

3. 创建并启动Jenkins容器
```
docker run -d -p 10240:8080 -p 10241:50000 -v /var/jenkins_mount:/var/jenkins_home -v /etc/localtime:/etc/localtime --name myjenkins jenkins/jenkins
```
-d 后台运行镜像
-p 10240:8080 将镜像的8080端口映射到服务器的10240端口。
-p 10241:50000 将镜像的50000端口映射到服务器的10241端口
-v /var/jenkins_mount:/var/jenkins_mount /var/jenkins_home目录为容器jenkins工作目录，我们将硬盘上的一个目录挂载到这个位置，方便后续更新镜像后继续使用原来的工作目录。这里我们设置的就是上面我们创建的 /var/jenkins_mount目录
-v /etc/localtime:/etc/localtime让容器使用和服务器同样的时间设置。
--name myjenkins 给容器起一个别名

# 三.Jenkins构建Freestyle project(自由构建项目)
### 1.Jenkins创建自由构建项目
Jenkins的使用，核心就是创建一个个的构建任务:
![](images/59aeb3f8e14bfaac8e8dc62b06879d38.webp)
名称随便填:
![](images/4ee7bbe9abaec606eb637279f8dee5b9.webp)
Freestyle project（自由风格的软件项目）：自由风格的软件项目，在这种Job里面可以结合任何SCM和任何构建系统来构建项目，甚至可以构建软件以外的系统。
这种类型的Job有“常规配置”，“源码管理”，“构建触发器”，“构建环境”，“构建”，“构建后操作”等配置项，可以根据多种脚本语言构建，如：Ant， Gradle， Windows batch， shell等。
这种类型的好处是可以自由设计构建方式，比较方便扩展。缺点是如果你只需要一个大众化/典型的持续集成、交付流程，想使用很多Jenkins内置方法、插件，这种方式就不太方便。

### 2.General常规配置
![](/images/b1bba02efb172d1086d1930728b0a34b.webp)
- 项目名称: 是刚才创建构建任务步骤设置的，当然在这里也可以更改。
- 描述: 对构建任务的描述。  
- 丢弃旧的构建： 服务器资源是有限的，有时候保存了太多的历史构建，会导致Jenkins速度变慢，并且服务器硬盘资源也会被占满。当然下方的"保持构建天数" 和 保持构建的最大个数是可以自定义的，需要根据实际情况确定一个合理的值。

### 3.源码管理
源码管理就是配置你代码的存放位置。支持主流的github 和gitlab代码仓库。
![](/images/8c6f3b86cba1e10bab178e8ee388eb38.webp)
- Repository URL：仓库地址
- Credentials：凭证。可以使用HTTP方式的用户名密码，也可以是RSA文件。 但要通过后面的"ADD"按钮添加凭证。
- Branches to build：构建的分支。*/master表示master分支，也可以设置为其他分支。

### 4.构建触发器
![](/images/dca846d54d6d2c003cd9903719e2d5fd.webp)
- 触发远程构建(例如，使用脚本): 该选项会提供一个接口，可以用来在代码层面触发构建。
- Build after other projects are built： 该选项意思是"在其他projects构建后构建"。这里不作介绍，后期可能会用到该选项。
- Build periodically： 周期性的构建。很好理解，就是每隔一段时间进行构建。日程表类似linux crontab书写格式。如下图的设置，表示每隔30分钟进行一次构建。
- Build when a change is pushed to GitLab：当有更改push到gitlab代码仓库，即触发构建。后面会有一个触发构建的地址，一般被称为webhooks。需要将这个地址配置到gitlab中，webhooks如何配置后面介绍。这个是常用的构建触发器。
- Poll SCM：该选项是配合上面这个选项使用的。当代码仓库发生改动，jenkins并不知道。需要配置这个选项，周期性的去检查代码仓库是否发生改动。

### 5.构建环境
![image.png](/images/e5826f379e9c5593710331da9fdd28f4.webp)

### 6.开始构建
选中invoke gradle通过调用gradle脚本进行构建，选择在系统管理中配置的gradle的版本
![](/images/437a9e1445cdbad38f71452da5146445.webp)
Eexcute shell： 执行shell命令，该工具是针对linux环境的，windows环境也有对应的工具"Execute Windows batch command"。 在构建之前，可能我们需要执行一些命令，比如压缩包的解压之类的。

### 7.构建后操作
- Publish Clover PHP Coverage Report：发布代码覆盖率xml格式的文件报告。路径会在"build.xml"文件中定义
- Publish HTML reports：发布代码覆盖率的HTML报告。  
- Report Crap: 发布crap报告。
- E-mail Notification:  邮件通知，构建完成后发邮件到指定的邮箱。
也可以通过安装插件实现:
- 项目构建成功后，要先发布到蒲公英， jenkins 有个插件叫 Upload to pgyer ，在打包完成后，帮我们把 apk 上传到蒲公英。
- 构建结果发布到 fir 平台。
- 构建结果通过钉钉机器人发布消息。

### 8.自由构建打Android包
1. Jenkins执行的服务器安装JDK，AndroidSdk，Gradle环境
2. 新建Item 输入任务名选择对应项目Freestyle project点击下边确定
3. 输入描述
4. 选择源码管理git->输入对应的url，点击添加设置git账号。
5. 构建选择之前设置的gradle 
6. 在下方Tasks设置对应操作命令
```
app:clean
app:assembleRelease
```
注：以上是最简单的Jenkins 打包Android项目，打包成功之后可以到工作空间：app / build / outputs / apk / HomePocketSeller / release 这个目录下找到打包文件，

# 四.Jenkins构建Pipeline(流水线)
Pipeline（流水线）适合大众化项目，构建简单方便，可以很方便的利用Jenkins的checkout功能从代码仓库拉取代码，然后用配置好的构建工具进行构建，Pipeline script可以直接写在job配置里面，也可以放在远程代码仓库里面，建议放在远程代码仓库，这样迁移/维护起来比较容易。Jenkins pipeline要用groovy语言编写，Jenkins提供了一些Pipeline语法示例，简单易用。
### 1.创建pipeline项目
1. 选择新建构建->pipeline
2. 配置pipeline项目，直接配置pipeline即可
3. Pipeline流水线可以通过web页面编写，也可以直接从github拉取出来的文件中读取脚本(Pipeline流水线脚本书写具体配置形式有两种声明式、脚本式)

### 2.pipeline脚本的类型
Pipeline支持两种语法：Declarative Pipeline（在Pipeline 2.5中引入，结构化方式）和Scripted Pipeline，两者都支持建立连续输送的Pipeline。
共同点：
``两者都是pipeline代码的持久实现，都能够使用pipeline内置的插件或者插件提供的steps，两者都可以利用共享库扩展。``
区别：
``两者不同之处在于语法和灵活性。Declarative pipeline对用户来说，语法更严格，有固定的组织结构，更容易生成代码段，使其成为用户更理想的选择。但是Scripted pipeline更加灵活，因为Groovy本身只能对结构和语法进行限制，对于更复杂的pipeline来说，用户可以根据自己的业务进行灵活的实现和扩展。``

##### (1.)声明式(Declarative Pipeline)
```
pipeline {
    agent any  //在可用的节点运行
    stages{
　　　　stage ('Prepare'){
            steps{          //清空发布目录
                bat '''if exist D:\\publish\\LoginServiceCore (rd/s/q D:\\publish\\LoginServiceCore)
                       if exist C:\\Users\\Administrator\\.nuget (rd/s/q C:\\Users\\Administrator\\.nuget) exit''' } } 

       //拉取git代码仓库
       stage ('Checkout'){
            steps{
                checkout([$class: 'GitSCM', branches: [[name: '*/master']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], 
                    userRemoteConfigs: [[credentialsId: 'c6d98bbd-5cfb-4e26-aa56-f70b054b350d', 
                    url: 'http://xxx/xxx/xxx']]])
            　　　　　　}
        　　　　}

       //构建
       stage ('Build'){
        　　steps{
        　　　　　bat '''cd "D:\\Program Files (x86)\\Jenkins\\workspace\\LoginServiceCore\\LoginApi.Hosting.Web"
            　　　　　　dotnet restore
            　　　　　　dotnet build
            　　　　　　dotnet publish --configuration Release --output D:\\publish\\LoginServiceCore'''
            　　　　　　}
        　　　　}
    
       //部署
    　　stage ('Deploy'){
        　　steps{
           　　　 bat '''cd D:\\PipelineScript\\LoginServiceCore
            　　　　　　python LoginServiceCore.py'''
           　　　　　　 }
        　　　　　}
        
   　　 //自动化测试（python代码实现）
    　　stage ('Test'){
        　　steps{
            　　　bat'''cd D:\\PipelineScript\\LoginServiceCore
            　　python LoginServiceCoreApitest.py'''   
            　　　　　　}
        　　　　 }
    }
 }
```

##### (2.)脚本式(Scripted Pipeline)
```
node('master') {     //master节点运行，以下stage也可指定节点
    stage 'Prepare'  //清空发布目录
        bat '''if exist D:\\publish\\LoginServiceCore (rd/s/q D:\\publish\\LoginServiceCore)
               if exist C:\\Users\\Administrator\\.nuget (rd/s/q C:\\Users\\Administrator\\.nuget)
               exit'''

    //拉取git代码仓库
    stage 'Checkout'
        checkout([$class: 'GitSCM', branches: [[name: '*/master']], doGenerateSubmoduleConfigurations: false, extensions: [], 
　　　　　　　submoduleCfg: [], userRemoteConfigs: [[credentialsId: 'c6d98bbd-5cfb-4e26-aa56-f70b054b350d', 
            url: 'http://xxx/xxx/xxx']]])
   
    //构建
    stage 'Build'
        bat '''cd "D:\\Program Files (x86)\\Jenkins\\workspace\\LoginServiceCore\\LoginApi.Hosting.Web"
            dotnet restore
            dotnet build
            dotnet publish --configuration Release --output D:\\publish\\LoginServiceCore'''
    
    //部署
    stage 'Deploy'
        bat '''
        cd D:\\PipelineScript\\LoginServiceCore
        python LoginServiceCore.py
        '''

    //自动化测试（python代码实现）    
    stage 'Test'
        bat'''
        cd D:\\PipelineScript\\LoginServiceCore
        python LoginServiceCoreApitest.py
        '''   
}
```
### 3.pipeline脚本位置
保存Pipeline script有2种方法：一种是pipeline script from SCM：需要配置SCM代码存储Git地址或SVN地址，指定script文件Jenkinsfile所在路径，每次构建job会自动去指定的目录执行script文件；一种是pipeline script，直接在Web UI的script输入框输入pipeline script语句；
##### (1.)本地脚本 (Pipeline Script)
直接在web页面编写即可。
##### (2.)远程脚本 (Pipeline Script from SCM)
将Pipeline script放到git，执行的时候从git拉下来执行，通过Jenkinsfile文件，控制Jenkins版本发布，首先拉取指定的远程仓库文件到jenkins节点服务器上， 然后获取仓库文件下的Jenkinsfile文件内容选择 Pipeline script from SCM 选项。此选项指示Jenkins从源代码管理（SCM）仓库获取你的流水线， 这里的仓库就是你clone到本地的Git仓库。

### 4.Jenkinsfile文件
复杂的 Pipeline 难以在 Pipeline 配置页面的文本区域内进行写入和维护。为了解决这一问题，jenkins Pipeline 支持在文本编辑器中编写脚本文件 jenkinsFile，Jenkins 可以通过从 SCM 选项的控件中加载 Pipeline 脚本。
选择 SCM 选项中的 Pipeline 脚本后，不要在 Jenkins UI 中输入任何 Groovy 代码; 只需指定要检索的 Pipeline 脚本的路径。更新指定的存储库时，只要 Pipeline 配置了 SCM 轮询触发器，就会触发一个新构建。
### 5.pipeline脚本语句生成器
Jenkins也提供了脚本生成器，内置的 “Snippet Generator” 程序有助于为单个步骤生成代码段。Snippet Generator 动态填充 Jenkins 实例可用的步骤列表。可用的步骤数量取决于安装的插件，它明确地暴露了在 Pipeline 中使用的步骤。

# 五.Multibranch Pipeline(多分支流水线)
每一个分支对应一个构建脚本.其实只要添加个 Branch Sources就可以了.当创建好后这个项目后后自动进行一次Scan了.目的是为了找到这个项目内有哪些分支可以进行构建的(依据的是项目内分支里的jenkinsfile文件)


参考资料:
[Jenkins实现android自动打包上传蒲公英及fir.im](https://juejin.cn/post/6844903615979585543)
[在 Docker 中用 Jenkins 搭建 Android 自动化打包](https://devbins.github.io/post/jenkins/)
[Jenkins实现Android自动化打包](https://blog.csdn.net/zhaoyanjun6/article/details/77102359)
[Android使用Jenkins持续集成](https://blog.csdn.net/binbinqq86/article/details/81033707)

