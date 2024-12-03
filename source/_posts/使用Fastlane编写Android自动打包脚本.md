---
title: 使用Fastlane编写Android自动打包脚本
---

# 一.什么是Fastlane?
Fastlane 是一款为 iOS 和 Android 开发者提供的自动化构建工具，它可以帮助开发者将 App 打包、签名、测试、发布、信息整理、提交 App Store 等工作完整的连接起来， 实现完全自动化的工作流。Fastlane本身没有一套特殊语法，使用的Ruby语言。Fastlane的插件工具叫做action，每一个action都对应一个具体的功能。

# 二.安装Fastlane
Fastlane是基于Ruby编写得因此需要先安装Ruby开发环境，如果使用Docker可以拉取Ruby镜像进行操作。
gem是ruby的包管理工具，首先确认下你的gem版本，最好是2.6+，
```
gem -v
2.6.6
```
正式开始安装fastlane之前，建议再换一下源：
```
gem sources --add https://gems.ruby-china.org/ --remove https://ruby     gems.org/
```
换完后确认一下：
```
gem sources -l
*** CURRENT SOURCES ***
https://gems.ruby-china.org/
```
好了，可以安装了：
```
sudo gem install fastlane --verbose
```
安装完成后，可以通过版本验证下：
```
fastlane -v
fastlane 1.103.0
```

# 三.初始化Fastlane项目
终端CD到项目根目录执行初始化命令:
```
fastlane init
```
系统会要求您确认您已准备好开始，然后再提供一些信息。快速入门：
在询问时提供您的应用程序的软件包名称（例如com.xx.xx） 这个步骤不小心按快了也没关系，可以在Appfile中重新定义， 当询问您的json机密文件的路径时，按Enter键，当系统询问您是否打算通过快速通道将信息上传到Google Play时，请回答“ n”（可以稍后进行设置） 执行完毕以后，fastlane将根据提供的信息自动为您生成配置。

您可以看到新创建的./fastlane目录，其中包含以下文件：
- Appfile 它定义了应用程序全局的配置信息。
- Fastfile它定义了驱动器的行为的“通道” FASTLANE。


如果没有配置过 ANDROID_HOME 环境变量，请先配置好AndroidSDK环境（~/.bashrc，~/.bash_profile，~/.profile 或者 ~/.zshrc）
```
export ANDROID_HOME=/Users/***/Library/Android/sdk
export PATH=$ANDROID_HOME:$PATH
```


# 四.编写 Fastlane脚本
初始化执行完成后，fastlane 会在当前项目根目录创建 ./fastlane 目录，里面最重要的就是 fastlane/Fastfile 文件，它主要用于定义 fastlane 需要如何执行任务。Fastlane 可以定义一些 lanes，类似任务。
示例：
```
lane :beta do
  # 执行 gradle 命令
  gradle(task: "clean assembleRelease")
  # 使用 slack 通知
  slack(
    slack_url: "https://hooks.slack.com/services/***/***",
    message: "message."
  )
end
```
上述片段定义了一个 beta lane，用于执行 gradle 命令并使用 slack 通知。

然后执行：
```
fastlane beta
```
fastlane 便会根据 Fastlane 里配置的 lane 执行。


>注意beta不是固定的命令，因为上面Fastlane里面do前面起的名字是beta，所以写beta


# 五.编写Fastlane Android打包脚本
使用Fastlane简化Android打包，并上传到蒲公英平台:
```
default_platform(:android)

platform :android do

     lane:beta do
     #从蒲公英平台拿到的api_key和user_key
     #api_key = "xxx"
     #user_key = "xxx"
     puts "开始打包xxxdebug版本"
     # 开始打包
    gradle(task:'clean')
    gradle(
        task: 'assemble',
        build_type: 'Debug',
      )
    puts "xxx打包成功"
    #puts "开始上传到蒲公英"
    #开始上传ipa到蒲公英，这里用的是蒲公英提供的插件
    #update_description代表更新信息，password代表安装密码
    #pgyer(update_description: "#{desc}", api_key: "#{api_key}", user_key: "#{user_key}", password: "123456", install_type: "2")
    #puts "上传到蒲公英成功"
    #在上传完apk后，打开apk的存放文件夹，起到提示上传完成的作用
    #system "open /User/wangchang/Desktop/defaultFlavor/debug"
    end


     lane:release do
     #从蒲公英平台拿到的api_key和user_key
     #api_key = "xxx"
     #user_key = "xxx"



    #输入蒲公英上传apk包后输入的版本描述信息
    #puts "请输入版本描述："
    #desc = STDIN.gets

    puts "开始打包xxxrelease版本"
    # 开始打包
    gradle(task:'clean')
    gradle(
        task: 'assemble',
        build_type: 'Release',
      )
    puts "xxx打包成功"
    #puts "开始上传到蒲公英"
    #开始上传ipa到蒲公英，这里用的是蒲公英提供的插件
    #update_description代表更新信息，password代表安装密码
    #pgyer(update_description: "#{desc}", api_key: "#{api_key}", user_key: "#{user_key}", password: "123456", install_type: "2")
    #puts "上传到蒲公英成功"
    #在上传完apk后，打开apk的存放文件夹，起到提示上传完成的作用
    #system "open /User/wangchang/Desktop/defaultFlavor/debug"
    end
end
```
> sdk位置，如果是本地打包，local.properies不需要改，如果是运维打包，它需要下载sdk到运维机器以及配置jks，这个时候地址都需要改为运维机器上的地址。

# 六.使用Fastlane打Android渠道包
首先，我们自定义一个 Action：add_channels_to_apk，这个 Action 的作用就是： 拷贝最终打包生成的 apk 文件，并修改文件名为渠道名，如 gengmei_qq_630.apk 然后将一个渠道名写入到 apk 文件的 META-INFO 目录中 其次，新建一个 txt 文件，里面写入所有需要打包的渠道名，如：QQ，360，Baidu…等等，渠道名之间用逗号隔开。
最后，在 Fastfile 中定义一个 Lane 来进行最终的集成处理：
```
desc "Package a new app version with different channels"
lane :do_package_apk do |options|
    project = "#{options[:project]}"
    target_version = options[:version]
 
    hipchat(message: "Start package #{project} at version #{target_version}")
 
    git_pull
    gradle(task: "clean")
    gradle(task: "assembleRelease")
    add_channels_to_apk(channels: './channels.txt')
 
    hipchat(message: "Deliver app #{project} successfully!")
end
```
接下来的事就简单多了，每次需要打包的时候，只要执行如下的命令即可：
```
fastlane do_package_apk project:Gengmei version:6.3.0 
```
无论是 5 个渠道，还是 50 个渠道，1 分钟内全部搞定，非常的方便。

# 七.Fastlane常用命令
- fastlane actions: 展示所有有效action列表
- fastlane action [action_name]: 展示一个action的详细说明，使用方法等
- fastlane lanes: 展示fastfile中的所有lane
- fastlane list: 展示fastfile中的所有的有效的lane
- fastlane new_action: 创建一个新的action
- fastlane env: 打印fastlane、ruby环境，一般提bug到issue的时候会要求提供

单独使用 Fastlane，或者单独使用 Jenkins，其实都可以完成打包操作。单独使用 Fastlane，开发人员需要自行打包，测试人员无法打包；单独使用 Jenkins，打包配置过于繁琐，证书失效等情况会导致配置文件失效，导致打包失败。 Fastlane 和 Jenkins 相结合的打包方式，通过 Jenkins 执行 Fastlane 的打包脚本，无需复杂的配置，不同的项目只需要简单的修改脚本，支持测试人员自行打包。

|执行顺序|方法名|说明|
|-|-|-|
|1	|before_all	    |在执行 lane 之前只执行一次|
|2	|before_each	|每次执行 lane 之前都会执行一次|
|3	|lane	        |自定义的任务|
|4	|after_each 	|每次执行 lane 之后都会执行一次|
|5	|after_all	    |在执行 lane 成功结束之后执行一次|
|6	|error	        |在执行上述情况任意环境报错都会中止并执行一次|


参考资料:
[使用Jenkins+Fastlane+Fir/Pgyer实现自动化打包](https://www.jianshu.com/p/f8abc79416ea#comments)
[Android GitLab CI + fastlane 工程实践](https://juejin.cn/post/6844903668278378503)
[Jenkins+Fastlane+自动化打包发布+蒲公英二维码展示](https://juejin.cn/post/6844903936650919943)
[Fastlane 实战教程](https://www.infoq.cn/profile/6B041998E073BA/publish)
[Android使用Fastlane打渠道包-签名-加固](https://wangzhumo.com/fastlane-apk-sign-jiagu/)
[使用 Fastlane 实现 iOS 跟 Android 自动打包脚本](https://juejin.cn/post/6844903727183183880)
[官方文档](https://docs.fastlane.tools/getting-started/android/beta-deployment/)
[Fastlane 实战教程](https://juejin.cn/user/2788017220881975)
[App自动化打包平台的搭建与维护](https://www.jianshu.com/p/1bf8e315847b)
[Fastlane使用说明](https://blog.csdn.net/u013599468/article/details/116664422)