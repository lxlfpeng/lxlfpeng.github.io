---
title: GitHubAction详解
---

# 一.GitHubAction简介
### 🧅什么是Github Action ?
GitHubActions是一个持续集成和持续交付的平台，它可以帮助你通过自动化的构建（包括编译、发布、自动化测试）来验证你的代码，从而尽快地发现集成错误。github于2019年11月后对该功能全面开放，现在所有的github用户可以直接使用该功能。GitHub 提供 Linux、Windows 和 macOS 虚拟机来运行您的工作流程，或者您可以在自己的数据中心或云基础架构中托管自己的自托管运行器。在使用Github Action之前首先需要了解以下前置知识:
- 持续集成/持续交付的概念。
- Git相关知识。
- Linux或Windows或macOS脚本相关知识。
- Yaml基础语法。

### 🍤什么是Yaml ?
编写GithubAction的流程时，需要创建一个workflow工作流，workflow必须存储在你的项目库根路径下的``.github/workflows``目录中，每一个 workflow对应一个具体的.yml 文件（或者 .yaml）。
yml是YAML（YAML Ain’t Markup Language）语言的文件，以数据为中心，比properties、xml等更适合做配置文件，主要有以下几个特点:
- 大小写敏感。
- 使用缩进表示层级关系。
- 缩进只能使用空格，不能用 TAB 字符。
- 缩进的空格数量不重要，只要层级相同的元素左对齐即可。
- ‘#’ 表示注释。

### 🍝Github Action基本概念
- workflow: 一个 workflow 就是一个完整的工作流过程，每个workflow 包含一组 jobs任务。
- job : jobs任务包含一个或多个job ，每个 job包含一系列的 steps 步骤。
- step : 每个 step 步骤可以执行指令或者使用一个 action 动作。
- action : 每个 action 动作就是一个通用的基本单元。

### 🍓Github Action 的使用限制
在使用免费版本的Github Action是有如下限制的:
* **作业执行时间** - 工作流中的每个作业最多可以运行 6 小时的执行时间。如果作业达到此限制，该作业将终止且无法完成。
* **工作流运行时间** - 每个工作流运行限制为 35 天。如果工作流运行达到此限制，则工作流运行将被取消。此时间段包括执行持续时间以及等待和批准所花费的时间。
* **API 请求** - 您可以在一小时内跨存储库中的所有操作执行多达 1000 个 API 请求。如果超出此限制，其他 API 调用将失败，这可能会导致作业失败。
* **并发作业** - 可以在帐户中运行的并发作业数取决于 GitHub 计划，如下表所示。如果超出，则任何其他作业都将排队。

  | GitHub 计划 | 并发作业总数 | 最大并发 macOS 作业数 |
  | - | - | - |
  | 自由 | 20 | 5 |
  | 专业版 | 40 | 5 |
  | 团队 | 60 | 5 |
  | 企业 | 180 | 50 |

* **作业矩阵** - 作业矩阵每次工作流运行最多可以生成 256 个作业。此限制适用于 GitHub 托管和自托管的运行程序。
* **工作流运行队列** - 每个存储库的排队时间间隔不超过 500 个工作流运行，间隔为 10 秒。如果工作流运行达到此限制，则工作流运行将终止且无法完成。

具体以最新版官方文档为主:[usage-limits-billing-and-administration](https://docs.github.com/en/actions/learn-github-actions/usage-limits-billing-and-administration)

# 二.GitHubAction的使用
## 😀workflow
在项目库根路径下的``.github/workflows``目录中创建一个.yml 文件（或者 .yaml）:
```
name: hello-github-actions
# 触发 workflow 的事件
on:
  push:
    # 分支随意
    branches:
      - master
# 一个workflow由执行的一项或多项job
jobs:
  # 一个job任务，任务名为build
  build:
    #运行在最新版ubuntu系统中
    runs-on: ubuntu-latest
    #步骤合集
    steps:
      #新建一个名为checkout_actions的步骤
      - name: checkout_actions
        #使用checkout@v2这个action获取源码
        uses: actions/checkout@v2 
      #使用建一个名为setup-node的步骤
      - name: setup-node
        #使用setup-node@v1这个action
        uses: actions/setup-node@v1
        #指定某个action 可能需要输入的参数
        with:
          node-version: '14'
      - name: npm install and build
        #执行执行某个shell命令或脚本
        run: |
          npm install
          npm run build
      - name: commit push
        #执行执行某个shell命令或脚本
        run: |
          git config --global user.email xxx@163.com
          git config --global user.name xxxx
          git add .
          git commit -m "update" -a
          git push
         # 环境变量
        env:
          email: xxx@163.com   
```

## 😂name
Workflow的名字，随便可以设置，就是工作流的名字。如果省略该字段，默认为当前 workflow 的文件名。
```
name: hello-github-actions
```

## 🤣on
触发的事件，可以是一个事件数组。
在代码仓库Push时触发:
```
#push时触发
on: push
```
可以用数组指定多个条件触发:
```
#push和merge时触发
on: [push, merge]
```
还可以对条件进行限制触发:
```
#当master分支push时触发，可以限定分支或标签。
on:
  push:
    branches:
      - master
```
完整的事件列表，请查看[官方文档](https://help.github.com/en/articles/events-that-trigger-workflows)。除了代码库事件，GitHub Actions 也支持外部事件触发，或者定时运行。

## 😉jobs
#### 1.job
jobs表示要执行的一项或多项任务。jobs可以包含一个或多个job，一个job就是一个任务，这个任务可以包含多个步骤(steps):
```
jobs:
  job1:
    ...
  job2:
    ...     
```
需要注意的是每一个Job都是并发执行的并不是按照申明的先后顺序执行的， 如果多个job 之间存在依赖关系，那么你可能需要使用 needs :
```
jobs:
  job1:
  
  job2:
    needs: job1
  
  job3:
    needs: [job1, job2]
```

这里的needs声明了job2 必须等待 job1 成功完成，job3必须等待 job1 和 job2依次成功完成。因此，这个 workflow 的运行顺序依次为：job1、job2、job3。needs字段指定当前任务的依赖关系，即运行顺序。

#### 2.job->runs-on
runs-on字段指定运行所需要的[虚拟机环境](https://docs.github.com/cn/actions/using-github-hosted-runners/about-github-hosted-runners)。它是必填字段，目前可用的虚拟机如下:
- ubuntu-latest，ubuntu-18.04或ubuntu-16.04。
- windows-latest，windows-2019或windows-2016。
- macOS-latest或macOS-10.14。
  指定job的运行环境:
```
jobs:
  job1:
    runs-on: ubuntu-18.04
  job2:
    runs-on: macos-10.15
  job3:
    runs-on: windows-2019    
```
github 会提供一个配置很不错的服务器做为 runner，Windows 和 Linux 虚拟机的硬件规格：
- 2 核处理器。
- 7 GB 内存。
- 14 GB 固态硬盘空间。

macOS 虚拟机的硬件规格：
- 3 核处理器。
- 14 GB 内存。
- 14 GB 固态硬盘空间。

>如果你有网络时延的需求，（比如推送及拉取镜像时产生的网络时延），你也可以[自建runner](https://docs.github.com/cn/actions/using-github-hosted-runners/customizing-github-hosted-runners) 。

#### 3.job->env
使用env可以给该任务或者是步骤配置环境变量:
```
 env:
   name: "zhangsan"
 run: |
   echo $name
```
环境变量可以配置在以下地方:
- jobs->job->env
- jobs->job->steps.env

#### 4.job->steps
steps字段指定每个 Job 的运行步骤，每个job由多个step构成，它会从上至下依次执行。steps可以包含一个或多个步骤，每个 step 步骤可以有:
- name：步骤名称，步骤的名称。
- env：该步骤所需的环境变量。
- id : 每个步骤的唯一标识符
- uses : 使用哪个action，这个表示使用别人预先设置好的Actions，比如因为我代码中要用到python，所以就用了actions/setup-python@v1来设置python环境，不用我自己设置了。
- with: 指定某个action 可能需要输入的参数。
- run: 执行哪些指令，具体运行什么命令行代码。
- continue-on-error : 设置为 true 允许此步骤失败job 仍然通过。
- timeout-minutes : step 的超时时间。
  例如:
```
...
name: Sync To Gitee
on: [ push ]
jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
    #创建一个打印环境变量的步骤
    - name: PrintName
      env:
        name: "zhangsan"
      run: |
        echo $name
    #创建一个安装Python环境的步骤    
    - name: SetUpPython
      uses: actions/setup-python@v1
      with:
        python-version: 3.7
    #创建一个安装Python包的步骤 
    - name: Install dependencies
      run: |
          python -m pip install --upgrade pip
          pip install requests
          pip install bs4
          pip install lxml     
```
>使用uses指的是这一步骤需要先调用哪个 Action。 Action 是组成工作流最核心最基础的元素。 每个 Action 可以看作封装的独立脚本，有自己的操作逻辑，我们只需要 uses 并通过 with 传入参数即可。 比如 actions/checkout@v2 就是官方社区贡献的用来拉取仓库分支的 Action， 你不需要考虑安装 git 命令工具，只需要把分支参数传入即可。

#### 5.Action
Github Actions 是GitHub的持续集成服务。持续集成由很多操作组成，比如登录远程服务器，发布内容到第三方服务等等，这些相同的操作完全可以提取出来制作成脚本供所有人使用。GitHub允许开发者把每个操作写成独立的脚本文件，存放到代码仓库，使得其他开发者可以引用该脚本，这个脚本就是一个Action。如果你需要某种功能的Action可以从GitHub社区共享的[action官方市场](https://github.com/marketplace?type=actions)查找，也可以自己编程Action开源出来供大家使用。既然 actions 是代码仓库，当然就有版本的概念，用户可以引用某个具体版本的 action。 下面都是合法的 action 引用:
```
actions/setup-node@74bc508 # 指向一个 commit
actions/setup-node@v1.0    # 指向一个标签
actions/setup-node@master  # 指向一个分支
```

## 😊GitHub Actions 中使用密文
在持续集成的过程中，我们可能会使用到自己的敏感数据，这些数据不应该被开源并泄露。那么如何才能安全的使用这些敏感数据呢?GithubActions提供了Secrets变量来实现这一效果。我们可以在 github repo 上依次点击  Settings  ->  Secrets-> Actions->New repository secret创建一个敏感数据例如:OSS_KEY_ID，OSS_KEY_SECRET， 然后我们就可以在GithubAction脚本中使用这一变量了:
```
-  name:  setup  aliyun  oss
    uses:  manyuanrong/setup-ossutil@master
    with:
        endpoint:  oss-cn-beijing.aliyuncs.com
        access-key-id:  ${{  secrets.OSS_KEY_ID  }}
        access-key-secret:  ${{  secrets.OSS_KEY_SECRET  }}
```

这里的secret就是一种context，描述 CI/CD 一个workflow 中的上下文信息，使用${{ expression }}语法表示。[更多context信息可以参考官方文档](https://docs.github.com/cn/actions/learn-github-actions/expressions)

## 😎GitHubAction执行结果
对于GitHubAction的执行流程我们可以通过repo 上依次点击Actions就可以看到Action的状态和执行结果等信息:
![image.png](/images/dbbd32eb93239b1fe5e7a0843074a56b.webp)

# 三.示例
使用GitHubAction实现Push代码发送邮件通知功能。 主要通过 GitHub Action 监听代码 push 事件，并发送邮件（前提是邮箱需要开通 SMTP 服务）。
在项目中 ./github/workflows/ 路径下添加 .yml 或者 .yaml文件，名字可以随便取。在这里我取名为 github-action-email.yml:
```
name: github-action-email
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    # 检出代码
    - name: CheckoutRepo
      uses: actions/checkout@v2
    # 获取master分支上最新一条提交的git log  
    - name: GetLastLog
      id: git_log
      uses: Edisonboy/latest-git-log-action@main
      with:
        tag: origin/master
    # 发送邮件    
    - name: Send email
      uses: dawidd6/action-send-mail@v3
      with:
        server_address: smtp.qq.com
        server_port: 465
        username: ${{secrets.MAIL_USERNAME}}
        password: ${{secrets.MAIL_PASSWORD}}
        subject: Github Actions job result
        to: ${{secrets.MAIL_TOUSERNAME}}
        from: ${{secrets.MAIL_USERNAME}}
        body: ${{github.repository}} push log : ${{steps.git_log.outputs.log}}
```
- secrets.XXX ： GitHub 允许仓库所有者创建和管理需要保密性的参数。例如邮件的账号和密码都是属于敏感参数。 可以通过项目``Settings -> Secrets -> Actions``配置密码，在这里我们添加 ``MAIL_USERNAME、MAIL_PASSWORD、MAIL_TOUSERNAME ``三个配置参数（注意：这里的密码是指 SMTP 服务的授权密码）。
- 上下文：可以访问工作流程运行、运行器环境、作业及步骤相关信息的方式`` ${{github.repository}} ``：当前仓库的的所有者和仓库名称。``${{steps.git_log_outputs.log}}`` ：获取step id 为 git_log 的输出集。

>因为我们定义 push 为触发条件，所以当我们只有push 代码后，我们定义的 GitHub Action 才会被执行。然后在 GitHub 上的 Action 能够实时看到当前的执行状态。


