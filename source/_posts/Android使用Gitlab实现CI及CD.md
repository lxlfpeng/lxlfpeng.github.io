---
title: Android使用Gitlab实现CI及CD
date: 2020-01-09
categories: 
  - CI/CD
---

# Android 项目配置 gitlab-ci 持续集成
这里只通过docker执行器来进行，如果使用shell也是可以的，不过需要自己写shell代码不如docker方便快捷。
docker容器搭建Android打包环境一般有两种方式:一种是通过基于openjdk:8-jdk 写shell配置好打包环境进行打包处理，另外一种则是通过docker hub上面别人配置好的Android打包环境docker容器进行。
### 1.使用OpenJdk镜像自行打包环境做Gitlab-CI/CD
```
#使用 openjdk镜像
image: openjdk:8-jdk 

#定义Android版本变量
variables:
  ANDROID_COMPILE_SDK: "28"
  ANDROID_BUILD_TOOLS: "28.0.2"
  ANDROID_SDK_TOOLS:   "4333796"
# 构建开始执行的脚本
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
    - ./gradlew assembleDebug#执行打包任务
  only: 
    - tags #这里tags的作用是当修改gitlab项目tag的时候会触发
    - test # 监听GitLab的这个分支
 # 指定由哪一个runner运行
  tags:
    - dev # 这个dev是上文注册Runner时的tag，和注册时候tag一样的话就会用对应的Runner来执行任务
  # 指定成功后应附加到任务的文件和目录的列表
  artifacts:
    paths:
    - app/build/outputs/# 保留app/build/outputs/文件夹
debugTests:
  stage: test
  script:
    - ./gradlew -Pci --console=plain :app:testDebug
# 构建完成之后执行的脚本
#after_script:
#  - 这里如果是要配合monkey的话，一般在这个地方执行monkey的脚本
```

### 2.使用DockerAndroid配置好的打包环境做Gitlab-CI/CD 
##### (1.)[runmymind/docker-android-sdk](https://hub.docker.com/r/runmymind/docker-android-sdk)
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

##### (2.)[jangrewe/gitlab-ci-android](https://hub.docker.com/r/jangrewe/gitlab-ci-android)
jangrewe/gitlab-ci-android的tag里面有基于sdk30、29、28、27、26等版本可以选择:

```
image: gitlab-ci-android:30 # 用来编译 android 项目的镜像
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

##### (3.)[androidsdk](https://hub.docker.com/u/androidsdk)
```
image: androidsdk/android-30:latest
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

##### (4.)[android-build-box](https://hub.docker.com/r/mingc/android-build-box)
```
image: mingc/android-build-box:latest

pipelines:
  default:
    - step:
        caches:
          - gradle
          - gradle-wrapper
          - android-emulator
        script:
          - bash ./gradlew assemble
definitions:
  caches:
    gradle-wrapper: ~/.gradle/wrapper
    android-emulator: $ANDROID_HOME/system-images/android-21
```

### 3.配置 runner 的Dokcker缓存路径
在服务器上找一个文件夹挂载到 docker 容器里边，给 .gradle 做一个缓存，这样每次编译的时候，就不用一直下载 gradle 了，这里我挂载的是 /home/android-cache 文件夹：
vi /etc/gitlab-runner/config.toml
[](https://img-blog.csdnimg.cn/410e2f809177436ebf8eb5add59fcd9d.png?x-oss-process=image/watermark,type_ZHJvaWRzYW5zZmFsbGJhY2s,shadow_50,text_Q1NETiBAd2RlbzM2MDE=,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center)
pull_policy = "if-not-present" 避免docker 镜像每次都pull
注意，如果你的 gitlab 服务器迁移了之后，如果不想再重新注册 runner，可以改这个配置文件的 url 和 token 为迁移后的值


参考资料:
[Docker在Android中的应用](https://blog.csdn.net/wgyscsf/article/details/97533811)
[GitLab CI/CD 介绍和使用](https://my.oschina.net/yunwangjun/blog/4934308)
[GitLab CI/CD 介绍和使用](http://blinkfox.com/2018/11/22/ruan-jian-gong-ju/devops/gitlab-ci-jie-shao-he-shi-yong/#toc-heading-8)
[使用gitlab api触发ci](https://segmentfault.com/a/1190000022939875)
[如何使用 gitlab api 触发 CI](http://quickapp.vivo.com.cn/how-to-use-gitlab-api-to-trigger-ci/)
[超简单配置Android持续集成自动化打包流程 - GitHub+GitLab-CI+蒲公英+钉钉](https://www.jianshu.com/p/e0553d3ac743/)
[Android 项目配置 gitlab-ci 持续集成](https://www.cnblogs.com/aimqqroad-13/p/10115799.html)
[Android 持续集成实践（二）——配置 Docker + gitlab-runner 实现线上自动编译](https://blog.csdn.net/Captive_Rainbow_/article/details/90407356)
[Android 持续集成实践（三）——编写 .gitlab-ci.yml 实现自动化](https://blog.csdn.net/Captive_Rainbow_/article/details/90480269)
[Android 持续集成实践（四）——配置 WebHook 通知编译结果](https://blog.csdn.net/Captive_Rainbow_/article/details/90634669)
[Android 持续集成实践（五）—— ABI 分包、特殊渠道编译需求](https://blog.csdn.net/Captive_Rainbow_/article/details/118856664)
