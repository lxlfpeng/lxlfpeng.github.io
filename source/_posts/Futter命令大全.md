---
title: Futter命令大全
date: 2021-03-15
categories: 
  - Fluter开发
---

# Flutter常用命令
- **flutter**：列出所有命令
- **flutter help/-h/–help**：获取帮助信息,-h/--help可以作为别的命令的后缀使用 打印详细的命令使用指南 如 flutter run -h
- **flutter doctor**：检查flutter环境状态，了解环境配置的状态
- **flutter doctor -v**：检查flutter环境状态，查看详细信息
- **flutter channel**：查看flutter SDK所有分支
- **flutter channel stable**：切换分支（例如切换到stable分支）
- **flutter upgrade**：更新flutterSdk（此命令会同时更新 Flutter SDK 和你的 Flutter 项目依赖包）
- **flutter logs**：查看日志

- **flutter create flutter_app**：用默认配置创建项目，包名为com.example.flutter_app
- **flutter create --org com.demo utter_app**：创建项目，包名为com.demo.flutter_app
- **flutter create -i swift -a kotlin flutter_app**：指定语言**：默认Android使用Java，iOS使用Objective-C
- **flutter create -t module flutter_module**：创建混编项目
- **flutter create --platforms=windows,macos,linux .**：旧项目新增windows,macos,linux等平台支持，如果编译报错使用``flutter create .``或者``flutter create --org package_name .``

- **flutter packages get**：拉取项目所有的依赖包，取flutter项目中以来的包（不包括flutterSdk）
- **flutter packages upgrade**：升级项目所有依赖包到最新版本（不包括flutterSdk）
- **flutter pub add xmpp_plugin**：给项目添加第三方依赖（例如添加xmpp_plugin）
- **flutter clean**：清空缓存，删除`build/`和`.dart_tool/`目录,清除缓存信息,避免之前不同版本代码的影响

- **flutter analyze**：使用分析器检查代码是否存在问题
- **flutter build ios**：构建iOS
- **flutter build apk**：安卓打包
- **flutter build ios --release**：iOS打包，运行命令后在xcode中打包
- **flutter build web**：打包web，文件在build目录下

- **flutter devices**：列出所有连接的设备，获取所有真机设备列表包括iOS模拟器
- **flutter run**：运行项目
- **flutter run --verbose-system-logs**：显示系统日志运行
- **flutter run -d 'iPhone Xʀ'**：指定设备运行项目
- **flutter run -d all**：运行在所有可用设备上

- **flutter emulators**：查看可用模拟器，获取模拟器列表（iOS、Android模拟器）
- **flutter emulators --launch apple_ios_simulator**：启动iOS模拟器
- **flutter emulators --launch Nexus_5X_API_27**：启动Android 模拟器-只有启动模拟器才可以运行


- **flutter config --enable-web true**：开启平台(web)
- **flutter config --no-enable-web**：关闭平台（关闭后可以删除项目中对应的平台目录文件夹）
- **flutter screenshot**：截图， 默认是在home目录下 -o 指定目录


# 管理版本
flutter使用git来管理，所以可以直接使用git相关的命令来升级、回退flutter版本。
找到对应的commit，使用git进行切换即可

比如


```
git reset --hard 4de0ae470dfa1ebff380378a9d704f5aed406e6a
```
然后，可以再执行下面的指令来检查下环境配置是否正确
```
flutter doctor -v
```
当然，也可以在Flutter官网找到对应的Flutter SDK版本，替换本地的Flutter版本
也可以使用flutter upgrade直接更新到flutter最新版本

# build参数
- **flutter build aar**：
- **flutter build aar --no-debug --no-profile --target-platform=android-arm64 --build-number=2.0**：
https://www.cnblogs.com/baiqiantao/p/16342570.html
## flutter build aar

[How to set Flutter build android aar version](https://stackoverflow.com/questions/60597182/how-to-set-flutter-build-android-aar-version)

shell

<pre class="highlighter-hljs code-theme-dark language-shell hljs code-pre-line" highlighted="true" boxid="code-Z6ZCps"><code-line class="line-numbers-rows"></code-line>flutter build aar --no-debug --no-profile --target-platform=android-arm64 --build-number=2.0
<code-line class="line-numbers-rows"></code-line>flutter build aar -h  # 显示详细帮助信息
<code-line class="line-numbers-rows"></code-line>flutter build aar -v  # 显示详细日志，包括所有 shell commands executed</pre>

> Note: this command builds applications assuming that the entrypoint is `lib/main.dart`. This cannot currently be configured.

* `--[no-]debug`：默认开，Build a debug version of the current project
* `--[no-]release`：默认开，Build a release version of the current project
* `--[no-]profile`：默认开，Build specialized for performance profiling 性能分析
* `--build-number`：版本号，An identifier used as an internal version number
* `--target-platform`：需要支持的目标平台
  * 默认支持 `android-arm`，即 [armeabi-v7a](https://developer.android.google.cn/ndk/guides/abis#v7a) (ARM 32 位)
  * 默认支持 `android-arm64`，即 [arm64-v8a](https://developer.android.google.cn/ndk/guides/abis#arm64-v8a) (ARM 64 位)
  * 默认支持 `android-x64`，即 [x86-64](https://developer.android.google.cn/ndk/guides/abis#86-64) (x86 64 位)
  * 当前不支持 `android-x86`
* `--output-dir`：存放生成的 repository 的绝对路径，默认为 `<current-directory>android/build`
* `--flavor`：Supports the use of `product flavors` in Android Gradle scripts
* `--[no-]pub`：默认开，Whether to run `flutter pub get` before executing this command
* `--split-debug-info=<v1.2.3/>`：可减少包体积，不能和 `--analyze-size` 同时使用
* `--[no-]obfuscate`：可用来混淆源代码，必须和 `--split-debug-info` 同时使用
* `--dart-define=<foo=bar>`：传递附加的键值对常量
* `--android-project-arg`：键值对直接传给 gradle 项目，可在 `build.gradle` 中通过 `project.property` 访问
* `--[no-]track-widget-creation`：默认开，仅在 JIT 模式下有效
* `--[no-]null-assertions`：执行空断言

## flutter build apk

shell

<pre class="highlighter-hljs code-theme-dark language-shell hljs code-pre-line" highlighted="true" boxid="code-er7en2"><code-line class="line-numbers-rows"></code-line>flutter build apk --release --target-platform=android-arm64 --build-number=88 --build-name=8.8
<code-line class="line-numbers-rows"></code-line>flutter build apk -h  # 显示详细帮助信息
<code-line class="line-numbers-rows"></code-line>flutter build apk -v  # 显示详细日志，包括所有 shell commands executed</pre>

> 在 module 项目中，使用 `--build-number` `--build-name` 参数是无效的，只有 application 项目中才有效

和 `flutter build aar` 相同/类似 的参数：

* `--debug`
* `--release`：默认模式
* `--profile`
* `--build-number`：必须是一个整数，对应 `versionCode`
* `--build-name=<x.y.z>`：对应 `versionName`
* `--target-platform`
* `--flavor`
* `--[no-]pub`
* `--split-debug-info=<v1.2.3/>`
* `--[no-]obfuscate`
* `--dart-define=<foo=bar>`
* `--android-project-arg`
* `--[no-]track-widget-creation`
* `--[no-]null-assertions`

新增的参数：

* `--target=<path>`：The main entry-point file，默认为 `lib\main.dart`
* `--[no-]analyze-size`：是否输出构件大小的分析信息，不能和 `--split-debug-info` 同时使用
* `--code-size-directory`：code size analysis 文件的存放位置，默认在 build 目录下
* `--[no-]multidex`：默认开
* `--ignore-deprecation`：忽略使用废弃 API 时的警告
* `--split-per-abi`：按 ABI 拆成独立的包，会根据支持的 ABI 打成多个 APK
