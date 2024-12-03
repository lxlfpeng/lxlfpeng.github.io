---
title: Flutter与Android混编
date: 2020-11-13
categories: 
  - Fluter开发
---

# 一.Flutter工程模式
flutter有四种工程模式:``application、plugin、package、module``
### 1.Flutter Application： Flutter应用
##### (1.)创建命令
```
flutter create xxapp
```
##### (2.)目录结构
```
│  pubspec.lock
│  pubspec.yaml
│  README.md
├─android
│
├─ios
│
├─lib
│      main.dart
│
├─test
│      widget_test.dart
│
└─web
```
- android：Android原生代码目录。
- ios：iOS原生代码目录。
- lib：这个是Flutter项目的核心目录，写的Flutter代码放在这个目录，也可以在这个目录创建子目录。
- test：测试代码目录。
- pubspec.yaml：这个是Flutter项目的依赖配置文件，类似于Android build.gradle文件，这里面包含了Flutter SDK 版本、依赖等。

##### (3.)说明
Flutter Application是一个标准的Flutter App项目工程，包含标准的Dart层与Native平台层代码，项目主体是Flutter， 其内部包含 Android 和 iOS、 Web 项目。

### 2.Flutter Plugin：Flutter插件
##### (1.)创建命令
```
flutter create --template=plugin xxapp_plugin
```
##### (2.)目录结构
```
│  pubspec.lock
│  pubspec.yaml
│  README.md
│
├─example
│  │
│  ├─lib
│  │      main.dart
│  │
│  └─test
│          widget_test.dart
│
├─lib
│      flutter_application_1.dart
│
└─test
        flutter_application_1_test.dart
```
##### (3.)说明
FlutterPlugin是Flutter 插件，包含Dart层与Native平台层的实现。Flutter Plugin提供Android或者iOS的底层封装，在Flutter层提供组件功能， 使Flutter可以方便的调取Native的模块。如果要开发一个 Plugin 且此 Plugin 涉及到原生支持，比如蓝牙功能、网络功能等，这些功能纯 Flutter 是无法实现得。 很多平台相关性或者对于Flutter实现起来比较复杂的部分，也都可以封装成Plugin。

### 3.Flutter Package：纯Dart组件
##### (1.)创建命令
```
flutter create --template=package xxapp_package
```
##### (2.)目录结构


```
│  pubspec.lock
│  pubspec.yaml
│  README.md
├─lib
│      flutter_application_1.dart
│
└─test
        flutter_application_1_test.dart
```
##### (3.)说明
Flutter Package是纯 Flutter 模块，不需要原生开发，没有Android 和 iOS 项目，仅包含Dart层的实现，往往定义一些公共Widget。

### 4.Flutter Module :Flutter模块
##### (1.)创建命令
```
flutter create --template module my_flutter
```
##### (2.)目录结构
```
│  pubspec.lock
│  pubspec.yaml
│  README.md
│
├─.android
│
├─.ios
│
├─lib
│      main.dart
│
└─test
        widget_test.dart
```
.android 文件夹包含一个 Android 项目，该项目不仅可以帮助你通过 flutter run 运行这个 Flutter 模块的独立应用，而且还可以作为封装程序来帮助引导 Flutter 模块作为可嵌入的 Android 库。
通过查看app的build.gradle文件可以知道是将Flutter变成moudle的形式依赖到Android项目中的:
```
...
buildDir = new File(rootProject.projectDir, "../build/host")
dependencies {
    implementation project(':flutter')
    implementation fileTree(dir: 'libs', include: ['*.jar'])
...
}

```


>这种集成方式虽然比较方便， 但是在多人协作的app中， 尤其是对非flutter开发的同学来说， 是强依赖本地安装flutter环境的， 所以也是有缺点的。

# 二.Flutter和Native工程混编方案
### 1.混编方案
一般来说混编方案有以下两种：
##### (1.)统一管理方案(不推荐)
![image.png](/images/e6b2d91cb53653c31113edf4be75aff1.webp)
也就是Flutter Application创建工程的方案，目的是将iOS工程和Android工程作为Flutter工程的子工程，由Flutter统一管理。
**优点:**
- 代码集中，可以很方便的进行项目开发，每个开发都可以进行iOS、Android和Flutter的工程开发。

**缺点:**
- 对原有项目的侵入性太大，项目对外部环境的依赖程度增加。
- 每个开发人员本地都要装有自己端的开发环境（iOS/Android）和Flutter的开发环境，并且Flutter SDK版本要保持一致。
- 耦合度会越来越高。当项目越来越复杂后，整个项目的代码耦合度会越来越高，相关工具链耗时也会越来越长，导致开发效率降低。
##### (2.)各端分离方案(推荐)
![image.png](/images/6befc8db1857031a7ca81469b24e89a9.webp)
各端分离方案是iOS、Android和Flutter分别作为三个独立项目存在，将Flutter工程的编译产物作为iOS工程和Android工程的依赖模块，原有工程的管理模式不变，对原生工程没有侵入性，无需额外配置工作。 这种方案需要单独创建Flutter项目，然后通过iOS（CocoaPods）和安卓的依赖管理工具将Flutter项目build出来的framework、资源包等放入Native工程以供使用。 这种方式可以将iOS、Android和Flutter项目放在一个目录下面作为一个项目来管理，也可以不在同一目录下，关键是设置Flutter模块依赖时相对路径一定要设置正确。

>通过Flutter Module创建工程的方案就可以完成这种混编。

### 2.混编方案总结
**官方也比较推荐各端分离方案这种混合开发解决方案，并且推出了Flutter Module工程方便，可将flutter作为module让原生native工程直接依赖。**

# 三.Android项目引入Flutter模块
在上文中得出Flutter和Native工程混编采用各端分离方案比较合理，下面来研究一下如果将Flutter作用一个单独的模块如何引入Android项目工程。
Flutter 可以作为 Gradle 子项目源码或者 AAR 嵌入到现有的 Android 应用程序中。因此Android 原生项目中接入Flutter项目一般有两种方式:
- 将 Flutter 打包成 AAR 包，然后在现有项目引入。
- 将 Flutter 源码视为 Gradle Module 引入现有项目。
>目前现有的 Android 项目可能支持 mips 或 x86 之类的架构，然而，Flutter 当前仅支持 为 x86_64，armeabi-v7a 和 arm64-v8a 构建预编（AOT）的库。 可以考虑使用 abiFilters 这个 Android Gradle 插件 API 来指定 APK 中支持的架构，从而避免 libflutter.so 无法生成而导致应用运行时崩溃

# 四.通过AAR的方式引入Flutter
### 1.创建Flutter module工程
这种方式需要配置好Flutter的开发环境. 有两种方式:
- 通过命令行生成Flutter module
- 可以通过Android Studio或者Vscode安装对应的插件创建工程。
##### (1.)命令行生成Flutter module集成项目
在Android工程中集成flutter，要保证 将要使用的Flutter Module工程与原生Android工程 在同一根目录下 ， Terminal进入到项目根目录， 执行以下命令:
```
flutter create -t module --org {package_name} {module_name}
// 此处 module_name 的命令遵循 Android 子 module 的命名即可。不能有中划线。比如，:
flutter create -t module --org com.emple.demo.flutter flutter_module
```
执行完成后会在Android的同一级目录下生成一个新的 flutter_module文件夹。这里在项目根目录创建子 module 只是为了把代码放在一个仓库，方便维护，理论上可以放在硬盘的任何位置。
##### (2.)通过Android studio创建Flutter module
1. 通过Android studio创建module
2. new->new module择flutter module
3. 根据提示指定创建路径后，指定目录就可以看见刚刚创建的module

Flutter module模块项目，其中包含一些 Dart 代码来帮助你入门以及一个隐藏的子文件夹 .android/。 .android 文件夹包含一个 Android 项目，该项目不仅可以帮助你通过 flutter run 运行这个 Flutter 模块的独立应用，而且还可以作为封装程序来帮助引导 Flutter 模块作为可嵌入的 Android 库。 注意:
- 将自己的 Android 代码添加到现有应用程序的项目或插件中，而不是添加到 .android/ 中的模块。在模块的 .android/ 目录中所做的任何更改并不会显示在使用该模块的现有 Android 项目中。
- 由于 .android/ 目录是自动生成的，因此不需要对它的代码进行版本控制，在新机器上构建模块之前，可以先在 my_flutter 目录中运行 flutter pub get 来重新生成 .android/ 目录，然后再使用 Flutter 模块构建 Android 项目。

### 2.编译打包AAR
可以将Flutter模块打成Android AAR 作为依赖媒介引入到Android应用程序中，这样Android应用开发不用安装Flutter SDK也可以.缺点是如果Flutter需要经常修改就需要每次都需要重新编译一次打包AAR进行引入。这种方式会将 Flutter 库打包成由 AAR 和 POM artifacts 组成的本地 Maven 存储库。这种方案可以使你的团队不需要安装 Flutter SDK 即可编译宿主应用。之后，也可以从本地或远程存储库中分发更新AAR。
假设你在 some/path/my_flutter 下构建 Flutter 模块，执行如下命令：
```
content_copy
cd some/path/my_flutter
flutter build aar
```
执行打包命令`` flutter build aar ``，这个打包AAR方式会包含多种abi，如果想要指定abi可以使用 ``flutter build aar --target-platform xxx``平台。
执行成功以后会输出以下信息。也就是说build以后会生成本地的maven仓库，仓库位于build->host->outputs->repo内，将这个仓库配置到需要混编的Android项目的gradle就可以完成混编。
```
1. Open <host>\app\build.gradle
2. Ensure you have the repositories configured, otherwise add them:

    String storageUrl = System.env.FLUTTER_STORAGE_BASE_URL ?: "https://storage.googleapis.com"
    repositories {
      maven {
          url 'C:\Users\WIN10\Desktop\fluttermodel\flutter_module2\build\host\outputs\repo'
      }
      maven {
          url "$storageUrl/download.flutter.io"
      }
    }
3. Make the host app depend on the Flutter module:

  dependencies {
    debugImplementation 'cn.tqxd.flutter_module2:flutter_debug:1.0'
    profileImplementation 'cn.tqxd.flutter_module2:flutter_profile:1.0'
    releaseImplementation 'cn.tqxd.flutter_module2:flutter_release:1.0'
  }
4. Add the `profile` build type:

  android {
    buildTypes {
      profile {
        initWith debug
      }
    }
  }
```
`` flutter build aar ``该命令主要用于创建（默认情况下创建 debug/profile/release 所有模式）本地存储库，主要包含以下文件:
build/host/outputs/repo
└── com
└── example
└── my_flutter
├── flutter_release
│   ├── 1.0
│   │   ├── flutter_release-1.0.aar
│   │   ├── flutter_release-1.0.aar.md5
│   │   ├── flutter_release-1.0.aar.sha1
│   │   ├── flutter_release-1.0.pom
│   │   ├── flutter_release-1.0.pom.md5
│   │   └── flutter_release-1.0.pom.sha1
│   ├── maven-metadata.xml
│   ├── maven-metadata.xml.md5
│   └── maven-metadata.xml.sha1
├── flutter_profile
│   ├── ...
└── flutter_debug
└── ...

### 3.Android工程引入AAR
可以发现，使用上面的命令编译的AAR包主要分为debug、profile和release三个版本，使用哪个版本的AAR需要根据原生的环境进行选择。找到AAR包，然后再Android宿主应用程序中修改 app/build.gradle 文件， 使其包含本地存储库和上述依赖项。
```
android {
  // ...
}

repositories {
  maven {
    url 'some/path/my_flutter/build/host/outputs/repo'
    // This is relative to the location of the build.gradle file
    // if using a relative path.
  }
  maven {
    url 'https://storage.googleapis.com/download.flutter.io'
  }
}

dependencies {
  // ...
  debugImplementation 'com.example.flutter_module:flutter_debug:1.0'
  profileImplementation 'com.example.flutter_module:flutter_profile:1.0'
  releaseImplementation 'com.example.flutter_module:flutter_release:1.0'
}
```



>注意，不要将编译好的aar直接copy到项目中去，必须要通过maven坐标依赖才能将完整的Flutter模块引入。

如果需要打不同版本的AAR在构建命令后面加上`` --build-number [版本号]``；
例如:
```
flutter build aar --build-number 1.1
```

### 4.AAR上传Maven仓库
如果团队开发时，这种本地Maven仓库引用aar的方式就不方便了，毕竟本地仓库路径都不一样。可以先分析通过flutter build aar是如何生成本地的maven仓库的:
//执行-v命令，查看命令输出信息
```
flutter build aar -v
```
可以发现，整个flutter build aar命令中，其实就执行了这三个Gradle任务``assembleAarDebug、assembleAarProfile、assembleAarRelease``而这三个任务都执行了``flutter\packages\flutter_tools\gradle\aar_init_script.gradle``这个gradle脚本。
查看aar_init_script.gradle文件:
```
// This script is used to initialize the build in a module or plugin project.
// During this phase, the script applies the Maven plugin and configures the
// destination of the local repository.
// The local repository will contain the AAR and POM files.
// 此脚本用于在模块或插件项目中初始化构建。
// 在此阶段，脚本应用 Maven 插件并配置
// 本地存储库的目的地。
// 本地存储库将包含 AAR 和 POM 文件。

//配置了本地maven仓库的地址
 project.uploadArchives {
        repositories {
            mavenDeployer {
              repository(url:"file://${outputDir}/outputs/repo")
            }
        }
    }

```
它在指定的目录下，``生成了一个maven本地仓库，并将aar上传到了这里``。 因此如果需要将aar上传到自己的私有maven仓库中，只需要把repository中的地址改成自己的maven私服地址即可。
例如
```
...

repository(url: "http://172.17.0.172:8081/repository/maven-releases/") {
    authentication(userName: "xxx", password: "xxx")
}
```

>也可以通过shell脚本来实现动态的修改:

### 5.AAR的方式的优缺点
**优点：**
- 不开发flutter的同学无需安装环境与工程，方便分离开发。
- 更有利于组件化开展。

**缺点：**
- 调试包与正式包都需要单独编译，测试较为麻烦。
- 上线前需要主动更新版本号。

# 五.依赖模块的源码引入Flutter
### 1.创建Flutter module工程
和上文中一致，参考上文。

### 2.settings.gradle配置
在settings.gradle里面配置如下代码:
// 加入下面配置
```
setBinding(new Binding([gradle: this]))
evaluate(new File(
        settingsDir.parentFile,
        rootProject.name + '/flutter_module/.android/include_flutter.groovy'
))
include ':flutter_module'
```
如果主module名称不是app，而是改成了其他的名称:，则还需要在project级别的gradle.properties中添加如下代码:
```
flutter.hostAppProjectName = app_module_name 
```

### 3.依赖flutter模块
在app主模块的build.gradle的dependencies中加入依赖库
```
implementation project(':flutter')
```
现在的原生项目就包含 Flutter SDK 的所有依赖了。 Flutter UI 相关的内容，还是用 dart 在 main.dart 中写， 然后可以把这个 dart 渲染出来的内容按照 Activity 、Fragment 或 View 的形式添加到已有的项目中了。

### 4.Flutter Module方式的优缺点
**优点**
方便快捷，所见即所得，不用频繁发布。

**缺点**
- 需要Android开发者配置flutter环境，且会增加构建时间。
- Android Studio 项目结构上会出现很多flutter依赖的模块，使项目视图变得杂乱。 
- 需要团队每个人都要安装flutter 环境，下载sdk等，否则无法编译项目。

# 六.Android启动Flutter页面
### 1.Android启动Flutter页面
有两种方式:
- 直接启动一个FlutterActivity
- 启动复写后的FlutterActivity（推荐）
##### (1.)直接启动一个FlutterActivity
//在清单配置文件中注册activity
```
<activity
   android:name="io.flutter.embedding.android.FlutterActivity"
   android:configChanges="orientation|keyboardHidden|keyboard|screenSize|locale|layoutDirection|fontScale|screenLayout|density|uiMode"
   android:hardwareAccelerated="true"
   android:windowSoftInputMode="adjustResize"
   />
```
//跳转到flutter页面
```
startActivity(
    FlutterActivity
        .withNewEngine() 
        //.initialRoute("/my_route")
        .build(MainActivity.this)
);
 
```
##### (2.)启动复写后的FlutterActivity（推荐）
自己创建一个FlutterAppActivity继承自FlutterActivity.
```
public class MainActivity extends FlutterActivity {

}
```

##### (3.)两种启动方式的区别
如果单纯只是想打开一个Flutter页面，两种方式实际上基本没有太大区别，第一种方式也许还会更简单一点。 但是，在Flutter开发中，往往还需要开发一些Native插件供Flutter调用，如果使用复写FlutterActivity的方式更有利于在FlutterActivity中注册的Native插件， 所以实际开发中一般推荐使用第二种方式.

### 2.Android跳转到Flutter指定页面
上文中的跳转是假定 Dart 代码入口是调用 main()，并且Flutter 初始路由是 ‘/’。 Dart 代码入口不能通过 Intent 改变，但是初始路由可以通过 Intent 来修改。Android跳转到Flutter指定页面是通过路由来跳转的,需要先声明路由;
在Flutter项目工程的MeterialApp下声明路由;并创建ImagePage()和TextPage()页面:
```
MaterialApp(
      theme: ThemeData(
      ),
      home: MyHomePage(),
      routes: <String,WidgetBuilder>{
        "one_page" : (context) => OnePage(),
        "two_page" : (context) => TwoPage(),
      },
    );
```
Android部分通过指定路由跳转:
```
/**
 * 进入Flutter页面 通过路由来指定页面
 */
startActivity(FlutterActivity.
        withNewEngine().
        initialRoute("two_page").//跳转到two_page页面
        build(MainActivity.this));

```

### 3.缓存FlutterEngine（可选）
默认情况下，每一个FlutterActivity都会创建自己的FlutterEngine对象，每一个FlutterEngine都需要加载耗时，也就是说打开每一个标准的FlutterActivity时都会有一个延迟。 为了减少这个延迟，可以在打开FlutterActivity前预加载FlutterEngine，需要使用的时候直接使用预加载好的FlutterEngine。
需要找一个合适的地方来预加载FlutterEngine，下面的示例在Application代码中进行预加载：
```
public class MyApplication extends Application {
  @Override
  public void onCreate() {
    super.onCreate();
    // Instantiate a FlutterEngine.
    flutterEngine = new FlutterEngine(this);

    // Start executing Dart code to pre-warm the FlutterEngine.
    flutterEngine.getDartExecutor().executeDartEntrypoint(
      DartEntrypoint.createDefault()
    );

    // Cache the FlutterEngine to be used by FlutterActivity.
    FlutterEngineCache
      .getInstance()
      .put("my_engine_id", flutterEngine);
  }
}
```
传递给FlutterEngineCache的id可以是任意值，只要确保和在FlutterActivity和FlutterFragment中取出FlutterEngine时使用的一致即可。要使用预热且缓存的 FlutterEngine 时，让你的 FlutterActivity 从缓存中获取 FlutterEngine，而不是创建一个新的。可以使用 FlutterActivity 的 withCachedEngine() 方法来实现：
```
myButton.addOnClickListener(new OnClickListener() {
  @Override
  public void onClick(View v) {
    startActivity(
      FlutterActivity
        .withCachedEngine("my_engine_id")
        .build(currentActivity)
      );
  }
});
```
当使用withCachedEngine方法时，注意id要和预加载FlutterEngine时保持一致。现在再打开FlutterActivity时，延迟问题就好很多了。

>当使用一个缓存的 FlutterEngine 时， FlutterEngine 会比展示它的 FlutterActivity 或 FlutterFragment 存活得更久。切记，Dart 代码会在你预热 FlutterEngine 时就开始执行，并且在你的 FlutterActivity 或 FlutterFragment 销毁后继续运行。要停止代码运行和清理相关资源，可以从 FlutterEngineCache 中获取你的 FlutterEngine，然后使用 FlutterEngine.destroy() 来销毁 FlutterEngine。

# 七.通过FlutterFragment添加Flutter界面
### 1.FlutterFragment启动Flutter页面
```
class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        //val flutterFragment =fragmentManager.findFragmentByTag(TAG_FLUTTER_FRAGMENT) as FlutterFragment;
        val flutterFragment = FlutterFragment.createDefault()
        supportFragmentManager
            .beginTransaction()
            .add(R.id.fragment_container, flutterFragment)
            .commit()
    }
}
```

### 2.FlutterFragment生命周期
FlutterFragment它不支持生命周期管理，需要借助Activity:
```
public class MyActivity extends FragmentActivity {
    @Override
    public void onPostResume() {
        super.onPostResume();
        flutterFragment.onPostResume();
    }

    @Override
    protected void onNewIntent(@NonNull Intent intent) {
        flutterFragment.onNewIntent(intent);
    }

    @Override
    public void onBackPressed() {
        flutterFragment.onBackPressed();
    }

    @Override
    public void onRequestPermissionsResult(
        int requestCode,
        @NonNull String[] permissions,
        @NonNull int[] grantResults
    ) {
        flutterFragment.onRequestPermissionsResult(
            requestCode,
            permissions,
            grantResults
        );
    }

    @Override
    public void onUserLeaveHint() {
        flutterFragment.onUserLeaveHint();
    }

    @Override
    public void onTrimMemory(int level) {
        super.onTrimMemory(level);
        flutterFragment.onTrimMemory(level);
    }
}
```

### 3.FlutterFragment使用预热的 FlutterEngine
默认情况下，FlutterFragment 会创建它自己的 FlutterEngine 实例，同时也需要不少的启动时间。这就意味着您的用户会看到短暂的白屏。通过使用已存在的、预热的 FlutterEngine 就可以大幅度减少启动的耗时。 要在 FlutterFragment 中使用预热 FlutterEngine，可以使用工厂方法 withCachedEngine() 实例化 FlutterFragment。
```
// Somewhere in your app, before your FlutterFragment is needed,
// like in the Application class ...
// Instantiate a FlutterEngine.
FlutterEngine flutterEngine = new FlutterEngine(context);

// Start executing Dart code in the FlutterEngine.
flutterEngine.getDartExecutor().executeDartEntrypoint(
    DartEntrypoint.createDefault()
);

// Cache the pre-warmed FlutterEngine to be used later by FlutterFragment.
FlutterEngineCache
  .getInstance()
  .put("my_engine_id", flutterEngine);
```

```
FlutterFragment.withCachedEngine("my_engine_id").build();
```

FlutterFragment 内部可访问 FlutterEngineCache，并且可以根据传递给 withCachedEngine() 的 ID 获取预热的 FlutterEngine。 如上所示，通过提供预热的 FlutterEngine，您的应用将以最快速度渲染出第一帧。

### 4.FlutterFragment缓存引擎中的初始路由
当配置一个使用新 FlutterEngine 的 FlutterActivity 或者 FlutterFragment 时，会使用到初始路由的概念。但是，使用缓存中的 Flutter 引擎时， FlutterActivity 或者 FlutterFragment 则没有涉及初始路由的概念。这是因为被缓存的引擎理论上已经执行了 Dart 代码，在这时配置初始路由已经太迟了。
开发者如果想要让缓存中的引擎从自定义的初始路由开始运行，那么可以执行 Dart 入口前，为缓存的 FlutterEngine 配置自定义的初始路由。如下面这个例子：
```
public class MyApplication extends Application {
  @Override
  public void onCreate() {
    super.onCreate();
    // Instantiate a FlutterEngine.
    flutterEngine = new FlutterEngine(this);
    // Configure an initial route.
    flutterEngine.getNavigationChannel().setInitialRoute("your/route/here");
    // Start executing Dart code to pre-warm the FlutterEngine.
    flutterEngine.getDartExecutor().executeDartEntrypoint(
      DartEntrypoint.createDefault()
    );
    // Cache the FlutterEngine to be used by FlutterActivity or FlutterFragment.
    FlutterEngineCache
      .getInstance()
      .put("my_engine_id", flutterEngine);
  }
}
```
通过设置导航通道中的初始路由，会让关联的 FlutterEngine 在 runApp() 方法首次执行后，展示已配置的路由页面。在 runApp() 的首次执行之后，修改导航通道中的初始路由属性是不会生效的。想要在不同的 Activity 和 Fragment 之间使用同一个 FlutterEngine，并且在其展示时切换不同的路由，开发者需要设置一个方法通道，来显式地通知他们的 Dart 代码切换 Navigator 路由。

# 八.Flutter与Android原生交互
### 1.在Flutter中调用原生方法，并获取返回值
##### (1.)Flutter端代码
首先创建一个MethodChannel对象，它接受一个String作为参数，String可以为任意字符串，这个String的作用是用来和原生中注册的MethodChannel进行匹配，只有双方的值一致时，这个通道才起作用。
```
static const platform = const MethodChannel('samples.flutter.dev/battery');
```
然后通过MethodChannel的invokeMethod()方法调用原生，这个方法接受两个参数，第一个参数为标识，也就是原生内边的方法名字，第二个参数就是需要向原生传递的参数，可以是一个map或者jsonString，我这没有需要向原生传递的参数，所以就没填。
```
Future<void> _getBatteryLevel() async {
    String batteryLevel;
    try {
      final int result = await platform.invokeMethod('getBatteryLevel');
      batteryLevel = '您的手机电量还有 $result % .';
    } on PlatformException catch (e) {
      batteryLevel = "手机电量获取失败: '${e.message}'.";
    }
 
    setState(() {
      _batteryLevel = batteryLevel;
    });
  }
```
##### (2.)Android端代码
Fluttrt的代码写完后，接着实现原生端的代码，首先需要在原生注册MethodChannel，如果你用的Activity，那么就继承FlutterActivity，如果用的Fragment，那么就继承FlutterFragment， 然后需要在Activity或者Fragment中实例化一下这个通道。常用的做法是在 configureFlutterEngine 这个方法中实例化通道就行了，有多少个通道，就在这里实例化多少个通道。
>值得注意：不管执行结果如何都要执行result.success或者result.error，否则Flutter端可能会一直等待响应
```
override fun configureFlutterEngine(@NonNull flutterEngine: FlutterEngine) {
        GeneratedPluginRegistrant.registerWith(flutterEngine)
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, "samples.flutter.dev/battery")
                .setMethodCallHandler { call, result ->
                    when (call.method) {
                                  "getBatteryLevel" -> {
                                      val batteryLevel = getBatteryLevel()
                                      if (batteryLevel != -1) {
                                          result.success(batteryLevel)
                                      } else {
                                          result.error("UNAVAILABLE", "Battery level not available.", null)
                                      }
                                  }
                              }
                }
    }
```
>注意，第二个参数的值要和Flutter中MethodChannel的值一致。

在Android实例化了一个MethodChannel对象，并调用了setMethodCallHandler方法进行注册。这个setMethodCallHandler方法需要实现一个接口参数，这个接口为MethodChannel.MethodCallHandler，看一下这个接口。
```
public interface MethodCallHandler {        
    @UiThread
    void onMethodCall(@NonNull MethodCall call, @NonNull Result result);
}
```    
这个接口只有一个onMethodCall方法，并且有两个参数，MethodCall和Result，其实最终就是通过这两个参数来与Flutter进行通信。Result，为一个接口，当Android处理完Flutter调用的方法逻辑后需要向Flutter回传一些数据时，就通过Result来实现。

### 2.在Android中调用Flutter方法
Android调用Flutter，更简单，只是需要注意线程问题，UI相关就放主线程执行，耗时操作放子线程然后event更新即可.
例如
- Android端调用location方法并传参给Flutter，当然不传参数不加参数，也不取参数就行了，这里就写个带参数的

##### (1.)Flutter端代码
例如用的StatefulWidget，在initState方法中给它加个接收消息
```
  @override
  void initState() {
    _initChannel();
  }
  void _initChannel() {
      var channel = MethodChannel("your_channel_name");
      channel.setMethodCallHandler((call) {
          // 同样也是根据方法名分发不同的函数
          switch(call.method) {
            case "your_method_name": {
              String msg = call.arguments["msg"];
              print("Native 调用 Flutter 成功，参数是：$msg");
              return "成功";
            }
          }
          return null;
      });
  }
```
##### (2.)Android端代码
```
class MainActivity: FlutterActivity() {

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)

        val messenger = flutterEngine.dartExecutor.binaryMessenger

        // 新建一个 Channel 对象
        val channel = MethodChannel(messenger, "your_channel_name")

        // 调用 Flutter 中的方法
        val params = mapOf(
            "msg" to "这是来自 Android 端的参数"
        )
        channel.invokeMethod("your_method_name", params)
    }

}
```

# 九.Flutter混合栈管理
Flutter 整个项目都是绘制在一个 Surface 画布上，而fluttet_boost 将栈统一到了原生层，通过一个单例的 flutter engine 进行绘制。每个 FlutterFragment 和 FlutterActivity 都是一个 Surface承载容器， 切换页面时就是切换 Surface 渲染显示，而对于不渲染的页面通过 Surface 截图缓存画面显示。 这样整个 Flutter 的路由就被映射到原生栈中，统一由原生页面栈管理，Flutter 内每 push 一个页面就是打开一个 Activity 。 一般情况下都会避免混合栈的相互调用 ，但是面对不得不如此为之的情况下，还是会出现问题。
### 1.Google官方（多引擎方案）
即每次使用一个新的FlutterEngine来渲染Widget树。虽然Flutter 2.0之后的创建FlutterEngine的开销大大降低，但是依然没有解决每个FlutterEngine是一个单独isolate。

### 2.flutter_boost（单引擎方案）
[flutter_boost](https://github.com/alibaba/flutter_boost)阿里巴巴闲鱼团队出品的一款解决Flutter栈管理的框架


参考资料:
[Flutter 开发文档](https://flutter.cn/docs)
[Flutter 开发文档(英文版)](https://docs.flutter.dev/)



[恋猫小郭Flutter合集](https://juejin.cn/user/817692379985752/posts)
[android调用flutter aar_在原生项目中集成Flutter](https://blog.csdn.net/weixin_39567870/article/details/112136412)
[Flutter文章中文版](https://flutter.cn/docs/get-started)
[Android 项目集成 Flutter](https://juejin.cn/post/6969086158122942501)
[在 Flutter 中使用原生控件](https://www.jianshu.com/p/607176087138)
[详解Flutter工程创建的几种模式](https://juejin.cn/post/6844904096734904328)
[Flutter混合开发组件化与工程化架构](http://zhengxiaoyong.com/2018/12/16/Flutter%E6%B7%B7%E5%90%88%E5%BC%80%E5%8F%91%E7%BB%84%E4%BB%B6%E5%8C%96%E4%B8%8E%E5%B7%A5%E7%A8%8B%E5%8C%96%E6%9E%B6%E6%9E%84/)
[Flutter: 以 aar 形式嵌入 android 中的方案和原理](https://juejin.cn/post/6844904164972036103)
[Flutter打包AAR插件之fat-aar使用教程](https://juejin.cn/post/6850037282884452360)
[优雅地将Flutter项目打包aar上传maven](https://blog.csdn.net/qq_37299249/article/details/115012889)
[flutter打包aar并上传Maven私服，flutter模块与原生工程解耦](https://blog.csdn.net/Ever69/article/details/120494115)
[flutter工程化踩坑实录](https://juejin.cn/post/7004856160872300557#heading-4)
[Android Native 工程集成 Flutter 的两种方式](https://juejin.cn/post/6844903970490548231)
[Flutter 工程化搭建（Android端）](https://juejin.cn/post/6934886225559945247)
[给现有 App 引入 Flutter Module](https://juejin.cn/post/6844903991923441672)
[开门见山——Flutter 自动打包aars 并上传Maven仓库](https://juejin.cn/post/6917079172913299470)
[Flutter 2.0 下混合开发浅析](https://juejin.cn/post/6940937798593544222)