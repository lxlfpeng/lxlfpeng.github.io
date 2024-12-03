---
title: Android上传aar到Jcenter和Jitpack
---

# 一.上传项目到Jcenter
### 1.注册jcenter账号
进入[注册地址](https://bintray.com/)选择右边sign up here 进行注册,建议直接使用github账号授权登录。(qq，网易等邮箱很多时候收不到验证码，所以要想成功完成注册最好用google邮箱)
![image.png](https://upload-images.jianshu.io/upload_images/3067896-d9485199291874e8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 2.创建Repository（仓库）
注册成功之后创建Repository，作为存放开源库的仓库，最好选择为公共仓库（public），仓库名称和仓库类型为maven，仓库名称在后面上传时需要用到。
![](https://upload-images.jianshu.io/upload_images/3067896-32a91ba63c936f88.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![](https://upload-images.jianshu.io/upload_images/3067896-379c5431d2343d2d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 3.获取 API Key
登录bintray， Edit profile -> API Key 可以获取上传的秘钥key，后面上传项目的时候需要使用。
![](https://upload-images.jianshu.io/upload_images/3067896-e2b20e3151b27d7d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 4.配置引入 bintray-release插件
项目根目录build.gradle配置，加入bintray-release插件
```
buildscript {
       ...
    repositories {
       ...
    }
    dependencies {
       ...
        classpath 'com.novoda:bintray-release:0.9.2'
    }
}
allprojects {
    repositories {
     ...
    }
    //解决lib中中文乱码问题
    tasks.withType(Javadoc) { 
        options.addStringOption('Xdoclint:none', '-quiet')
        options.addStringOption('encoding', 'UTF-8')
    }
}
```
开源库目录build.gradle配置，每个配置描述都已经给出，完成这两个步骤，就可以准备上传开源库到jcenter了
```
apply plugin: 'com.android.library'
apply plugin: 'com.novoda.bintray-release'//添加 bintray-release 配置
android {
    ...
    defaultConfig {
    ...    
    }
    buildTypes {  
    }
    compileOptions {
        sourceCompatibility = 1.8
        targetCompatibility = 1.8
    }
}
dependencies {
    ...
}
//添加
publish {
    userOrg = 'lxlfpeng'//bintray.com用户名
    repoName = 'RecordingButton'   // bintray上仓库的名字
    groupId = 'com.lagua'//jcenter上的路径
    artifactId = 'RecordingButton'//项目名称
    publishVersion = '1.0.0'//版本号
    desc = 'Make flow layouts simpler'// 描述
    website = 'https://github.com/lxlfpeng/RecordingButton.git'//一般填github 项目地址,一定是要有效的地址
}
```

### 5.上传开源库
##### (1.)在项目根目录下执行上传命令
![](https://upload-images.jianshu.io/upload_images/3067896-e47e44c5dd6f83ef.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
```
# window 下执行
gradlew clean build bintrayUpload -PbintrayUser=Xxxx -PbintrayKey=Xxxxxxxxx -PdryRun=false

# linux 下执行
./gradlew clean build bintrayUpload -PbintrayUser=Xxxx -PbintrayKey=xxxxxxxxx -PdryRun=false
```

##### (2.)上传命令解析
```
gradlew clean build bintrayUpload //根命令
-PbintrayUser=Xxxxxxxxx  //jcenter 账号用户名
-PbintrayKey=Xxxxxxxxx  //文章开头获取的API Key
-PdryRun=false //配置参数，true 执行所以细节但是不上传开源库，false上传开源库

```

# 二.添加到Jcenter中央仓库
### 1. Add to JCenter
上传成功之后就可以打开项目详情，选择 Add to JCenter 就可以申请添加到 JCenter 了，如下图所示：经过上面的步骤，我确实已经把开源库上传到Jcenter了，但是我们还不能引用，要想引用上传的开源库还得提交人工审核，人工审核通过会收到站内message，并且开源库中的Add to Jcenter 也会消失。
![](https://upload-images.jianshu.io/upload_images/3067896-f84c5fccc75ae139.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 2. 审核期间引用
在工程(projrct)的build.gradle文件中，添加maven支持
![](https://upload-images.jianshu.io/upload_images/3067896-0fbec7ca06c93974.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

```
allprojects {
    repositories {
       ...
        maven { url 'https://dl.bintray.com/lxlfpeng/xxxxx' }
    }
}
```
在moudle的build.gradle文件中,添加依赖
```
dependencies {
    ...
    implementation 'com.xx:xx:1.0.0'
}
```

# 三.Jcenter托管项目版本更新
### 1.提交版本
开源库有bug，或者我们进行迭代，就会涉及到版本更新，那就只需要修改开源库目录build.gradle配置中的版本号，其他配置保持不变，再次执行上传开源库命令就可以达到版本更新的目的。
```
publish {
    userOrg = 'maoqitian'//bintray.com用户名
    repoName = 'maolibrary'   // bintray上仓库的名字
    groupId = 'com.mao'//jcenter上的路径
    artifactId = 'flexibleflowlayout'//项目名称
    publishVersion = '2.0.0'//版本号
    desc = 'Make flow layouts simpler'// 描述
    website = 'https://github.com/maoqitian/FlowLayout'//一般填github 项目地址,一定是要有效的地址
}
```

### 2.审核通过
审核通过会发送站内message，同时Add to jCenter按钮消失，并且可以通过访问https://jcenter.bintray.com/你的groupId查看。

# 四.Jcenter托管项目问题相关
### 1.上传成功后jcenter项目首页不显示pom
**问题：**
上传成功后jcenter项目首页不显示pom，点击add to jcenter弹出以下错误提示：
```
Please fix the following before submitting a JCenter inclusion request: - Add a POM file to the latest version of your package.
```
原因是:是由于编码问题导致javadoc生成失败导致。

**解决：**
方式一：在Project的build.gradle中配置以下语句：
```
allprojects {
    repositories {
        google()
        jcenter()
    }
    // 新增
    tasks.withType(Javadoc) { 
        options.addStringOption('Xdoclint:none', '-quiet')
        options.addStringOption('encoding', 'UTF-8')
    }
}
```

方式二：拆分上传命令：
1. 在Terminal执行`gradlew clean build`命令。
2. 先右击执行generatePomFileForReleasePublication task，再右击执行publishReleasePublicationToMavenLocal task，具体操作看图：
![](https://upload-images.jianshu.io/upload_images/3067896-e7a8329cec48bf77.JPEG?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
3. 在Terminal中执行`gradlew bintrayUpload -PbintrayUser=username -PbintrayKey=API Key -PdryRun=false`命令。

### 2.Lint检查报错
**问题：**
Lint检查报错，导致Build & Upload失败。

**解决：**
方式一：需要自行根据错误信息修正Error级别的问题。
方式二：为Library项目的build.gradle配置以下Lint选项实现，--该方式摘自网络，未验证：
```
android {
 
    ...
 
    lintOptions {
        abortOnError false // 即使有报错也不会停止打包
        checkReleaseBuilds false // 打包Release版本的时候也不进行Lint检测
    }
    
    ...
    
}
```
### 3.网络问题导致的上传失败
**问题：**
```
* What went wrong:
Execution failed for task ':utils:bintrayUpload'.
> javax.net.ssl.SSLPeerUnverifiedException: peer not authenticated
```
```
* What went wrong:
Execution failed for task ':utils:bintrayUpload'.
> org.apache.http.conn.HttpHostConnectException: Connection to http://127.0.0.1:8888 refused
```
```
* What went wrong:
Execution failed for task ':utils:bintrayUpload'.
> org.apache.http.NoHttpResponseException: The target server failed to respond
```
**解决：**
1. 关闭代理软件，重启网络。
2. 关闭由上传操作自动开启的Java客户端（Mac上会出现，其他设备不清楚）。

# 五.上传项目到Jitpack
### 1.准备好项目以及要发布的开源库
上传到JitPack的开源库默认使用项目的名称，而不是要发布的开源库的名称，所以尽量给项目起一个比较优雅的名字（这里我们使用同名）。
![](https://upload-images.jianshu.io/upload_images/3067896-5a83760fa82a1c65.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 2.配置gradle插件
用到一个的插件**[android-maven-gradle-plugin](https://link.jianshu.com/?t=https://github.com/dcendents/android-maven-gradle-plugin)**
1. 在项目的build.gradle添加``classpath 'com.github.dcendents:android-maven-gradle-plugin:1.5'``。
```
buildscript {
   ...
    repositories {
        google()
        jcenter()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:3.5.2'
        classpath 'com.github.dcendents:android-maven-gradle-plugin:1.5'
    }
}

allprojects {
  ...
}
```
![](https://upload-images.jianshu.io/upload_images/3067896-e3db40a74b70cf4d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

2. 在要上传的library的build.gralde文件添加如下代码：
```
apply plugin: 'com.android.library'
// JitPack Maven
apply plugin: 'com.github.dcendents.android-maven'
// Your Group
group='com.github.username'
android {
  ...
}
```
3. 将项目上传到github。

### 3.在github主页，创建一个Release或Tag
![image.png](https://upload-images.jianshu.io/upload_images/3067896-8b73d72fbc3be873.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![image.png](https://upload-images.jianshu.io/upload_images/3067896-e0cbc93af0ae81a4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![image.png](https://upload-images.jianshu.io/upload_images/3067896-559bb372cce05851.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![image.png](https://upload-images.jianshu.io/upload_images/3067896-eb4410591b3915a9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 4.将项目的仓库提交到[jitpack.io](https://jitpack.io/)
![image.png](https://upload-images.jianshu.io/upload_images/3067896-1b6cdee039735444.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
版本提交完成后，JitPack会自动生成引用该library的配置信息:
![image.png](https://upload-images.jianshu.io/upload_images/3067896-a75ad47745dfa6da.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

参考资料:
[开源库上传 jcenter](https://www.maoqitian.com/2019/09/03/%E5%BC%80%E6%BA%90%E5%BA%93%E4%B8%8A%E4%BC%A0-jcenter/)
[AS上传Library到JCenter 教程+踩坑记录](https://www.jianshu.com/p/b09871d84fc1)
[亲测android Studio发布Lib到jCenter](https://www.jianshu.com/p/6f04943efd3d)
[如何一步一步的将自己的开源项目上传到jcenter](https://blog.csdn.net/csdn576038874/article/details/79308391)
[如何上传Android库项目的到JCenter](https://juejin.im/post/5df10c116fb9a0165936e0b7)










