---
title: Flutter环境搭建及项目配置
date: 2019-06-21
categories: 
  - Fluter开发
---

# 一. 下载安装Flutter。
### 1.1 下载安装包[Flutter SDK](https://flutter.cn/docs/development/tools/sdk/releases)
![](/images/790e1a6e1da648f24f5196bf5f40a893.webp)
### 1.2 下载完成后进行解压:
![](/images/584c394cafe48aa90501c58928cc1cfd.webp)
### 1.3 配置环境变量。
控制面板->系统和安全->系统->高级系统设置->环境变量->path->编辑->新建
![](/images/6f8918090fcbff15309423e45ae357bb.webp)
### 1.4 安装flutter依赖并检查。
cmd命令:
```
flutter doctor
```
![](/images/3475896c37cedb706b3578e53057ee66.webp)
### 1.5 查看flutter版本。
```
flutter doctor -v
```
# 二. Android Studio安装配置。
### 2.1 Android studio安装dart和flutter插件。
![](/images/a06dd7c88bef5014a91d02e60205b377.webp)

![](/images/51f7d25a2c5829ad444ea3111bdd2d70.webp)
### 2.2 重启Android studio创建flutter工程。
![](/images/4e2735083e6fe524e45a5eccc77d4335.webp)
# 三. VsCode配置。
### 1. vscode添加flutter支持。
![](/images/6a97f539d0e0be528a95c9fd953624c2.webp)
### 2. 创建一个flutter的项目。
![](/images/042df2a9de26db86a72770aa551d733b.webp)
### 3.使用模拟器调试。
![](/images/fbb639a186bc1752e41df3bc493e498d.webp)
![](/images/0bec2b31685de17ebabf29e1818fece6.webp)
# 四. 创建或者运行项目卡住问题
创建项目一直卡在Creating Flutter Project没反应。
运行项目一直卡在:
```
Running Gradle task 'assembleDebug'...   
```
因为创建和运行flutter项目时会卡住是因为Gradle的Maven仓库在国外, 可以替换使用阿里云的镜像地址。方可解决问题。

(1). 修改项目中android/build.gradle文件
```
buildscript {
     repositories {
         //修改的地方
		 //google()
         //jcenter()
         maven { url 'https://maven.aliyun.com/repository/google' }
         maven { url 'https://maven.aliyun.com/repository/jcenter' }
         maven { url 'http://maven.aliyun.com/nexus/content/groups/public' }
     }
  ...
 }

allprojects {
     repositories {
         //修改的地方
         //google()
         //jcenter()
         maven { url 'https://maven.aliyun.com/repository/google' }
         maven { url 'https://maven.aliyun.com/repository/jcenter' }
         maven { url 'http://maven.aliyun.com/nexus/content/groups/public' }
     }
 }

```
(2). 修改Flutter的配置文件, 该文件在Flutter安装目录/packages/flutter_tools/gradle/flutter.gradle
```
buildscript {
    repositories {
       // google()
       // jcenter()
	   maven { url 'https://maven.aliyun.com/repository/google' }
       maven { url 'https://maven.aliyun.com/repository/jcenter' }
       maven { url 'http://maven.aliyun.com/nexus/content/groups/public' }
	}
  ...
}
  ...
class FlutterPlugin implements Plugin<Project> {
   // private static final String MAVEN_REPO      = "https://storage.googleapis.com/download.flutter.io";
    private static final String MAVEN_REPO      = "http://download.flutter.io";
    ...
}
```
(3).替换download.flutter.io。
- flutter/packages/flutter_tools/gradle/resolve_dependencies.gradle

- flutter/packages/flutter_tools/gradle/aar_init_script.gradle

- flutter/packages/flutter_tools/gradle/flutter.gradle


中的：https://storage.googleapis.com/download.flutter.io   替换为：http://download.flutter.io   重新编译。

# 五 . 项目结构分析
![](/images/402bb23d49be831f11d22d832f48fd08.webp)
- .idea：IDE的生成的一些配置，不用管

- android：创建项目生成的Android原生代码

- build：项目编译目录

- ios：创建项目生成的ios原生代码

- lib：(重点)我们写的代码都在这里边，以.dart结尾。

- test:创建项目自动生成的test文件

pubspec.yaml：(重点)flutter包管理，我们依赖的包都在这里管理，类似于maven、gradle;flutter依赖包中国地址：[flutter-io](https://pub.flutter-io.cn/
)。除此之外还可以对Flutter进行设置、添加资源文件等。

# 六. Flutter添加第三方依赖
在flutter中引入第三方库一共有三种方式:
- Pub方式[pub仓库](https://pub.dev/)
- 导入本地工程方式
- Git 远程仓库添加
### 1. Pub引入方式
Flutter 的依赖管理在 pubspec.yaml 中进行。使用pubspec.yaml 管理第三方库，例如要将包’dio’添加到应用中，请执行以下操作：

- （1.） 添加依赖，打开 ``pubspec.yaml`` 文件，然后在 dependencies 下添加 dio:
```
dependencies:
  dio: ^2.1.6
```
格式为：``包名 + ^ + 版本号``
-  （2.） 进行安装在 terminal 中·：运行 ``flutter packages get``或者在 As 中: 点击 pubspec.yaml 文件顶部的`` Packages Get``。

### 2. 导入本地工程方式
```
dependencies:
    // 包名
    dio:
        // 本地包路径
        path: ../../code/dio
```
### 3. Git 远程仓库添加
```
dependencies:
  // 包名
  dio:
    git:
      // 远程仓库 url
      url: git://github.com/flutter/packages.git
      // 远程仓库中的包的相对路径
      path: packages/dio
```
> **dependencies 与dev_dependencies的区别**
dependencies 与dev_dependencies 是用户发布环境与本地环境开发，一般写在dependencies下面即可devDependencies  里面的插件只用于开发环境，不用于生产环境，而 dependencies  是需要发布到生产环境的。
比如我们写一个项目要依赖于XXX，没有这个包的依赖运行就会报错，这时候就把这个依赖写入dependencies ；
而我们使用的一些构建工具比如XXX、XXX这些只是在开发中使用的包，上线以后就和他们没关系了，所以将它写入devDependencies。

### 4. Flutter的flutter packages get失败
```
Running "flutter pub get" in flutter_app...                     
Got socket error trying to find package flutter_easyrefresh at https://pub.dartlang.org.
```
添加站点
```
1. export PUB_HOSTED_URL=https://pub.flutter-io.cn
```
![](/images/718c0c51fa870ec11a0e05955a2b018e.webp)
```
2. export FLUTTER_STORAGE_BASE_URL=https://storage.flutter-io.cn
```
![](/images/721fc8bf64f3643469d44895e517f551.webp)

# 七. 在Flutter中添加资源文件.
一个应用程序少不了一些静态资源，``例如：图片、字体、配置文件``等。这些静态资源会打包到程序安装包中，可以在运行时访问。

Flutter 中添加静态资源需要将静态资源放置在任意目录（通常是根目录下的 `assets` 文件夹中），然后在配置文件中 `pubspec.yaml` 中配置资源的路径。每个 asset 都通过相对于 `pubspec.yaml` 文件所在位置的路径进行标识。资源才能被打包使用。
### 1.加载资源图片图片

(1.) Flutter 中使用 [AssetImage](https://docs.flutter.io/flutter/painting/AssetImage-class.html) 组件展示图片。Flutter 会根据当前设备的分辨率加载对应的图片，我们只需要按照特定的目录结构来放置图片，例如：
```
images
    ├── logo.png
    ├── 2.0x
        ├── logo.png
    ├── 3.0x
        ├── logo.png
```
(2.) 添加本地图片资源
```
flutter:
    assets:
        // 表示引入根目录下的 images 文件夹下的所有资源文件
        - images/
        // 只添加 images/ 下的 logo.png
        - images/logo.png
```
(3. ) 加载本地图片资源
```
Image.asset("images/logo.png")
// 或者
Image(
  image: new AssetImage("assets/images/logo.png"),
),
```
至此图片就会显示在屏幕上面了。

# 八. Android原生项目添加flutter模块
### 1. 切换到native项目的根目录。再执行下面命令来创建一个flutter模块。
```
flutter create -t module flutter_module
```
### 2. 在project中的settings.gradle文件中添加如下代码。
```
setBinding(new Binding([gradle: this]))
evaluate(new File(
        settingsDir.parentFile,
        'FlutterHybridAndroid\\flutter_module\\.android\\include_flutter.groovy'
))

```
### 3. 项目依赖这个flutter的module。
```
implementation project(':flutter')
```
# 九. flutter打android项目打包
1. 创建打包的jks。
2. 在Flutter工程中/android/app/创建key/目录。
3. sign.jks拖到key/目录下。
4. 配置/android/app/build.gradle文件。
```
android {
    signingConfigs {
        release {
            keyAlias 'sign'
            keyPassword 'android'
            storeFile file('key/sign.jks')
            storePassword 'android'
        }
    }

    buildTypes {
        release {
            signingConfig signingConfigs.release
        }
    }
}
```
5. 打包APK。
   在当前项目目录的终端中，或者直接在 Android Studio 的 Terinal 执行命令：
```
flutter build apk
```
生成的目录：当前项目``\build\app\outputs\apk\release\xx.apk``

参考资料:
[Flutter 插件使用必知必会](https://juejin.im/post/5c206b4ff265da61327f52f4)
