---
title: Android项目Gadle统一依赖管理
---

# 一.Gradle管理依赖版本

在中大型Android项目中，都会有多个Module进行协同配合。这些module中可能会依赖同一个库的不同版本，这将导致一些问题，要么是代码冲突，要么是APK包体积增大，亦或是项目构建的时间变长，拖慢开发效率。 例如:下图就是在不同的module中依赖同一个库的不同版本。
![](https://img-blog.csdnimg.cn/b5ccb025bd254201a4a20504e4a4025c.png)
要解决这个问题我们首先要了解在Android项目中目前有那些方案来引入第三方依赖:

1. 直接编写(默认方式)
2. 使用ext扩展抽取公共版本
3. 使用buildSrc管理依赖
4. 使用composing builds管理依赖
5. 使用catalog管理依赖(gradle7版本以上才能用，因此暂时忽略)

# 二.直接编写(默认方式)

## 简介

直接编写是Android项目工程自带的默认管理方式，在每一个module中都写死了不同依赖及版本号，因此每次升级依赖库时都需要对每一个module做大量的手动更改。

**module_a/build.gradle:**

```
dependencies {
    implementation 'androidx.core:core-ktx:1.7.0'
    implementation 'androidx.appcompat:appcompat:1.4.1'
    implementation 'com.google.android.material:material:1.5.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.3'
    implementation 'com.squareup.okhttp3:okhttp:4.10.0'
}
```

**module_b/build.gradle:**

```
dependencies {
    implementation 'androidx.core:core-ktx:1.7.0'
    implementation 'androidx.appcompat:appcompat:1.4.1'
    implementation 'com.google.android.material:material:1.5.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.3'
    implementation 'com.squareup.okhttp3:okhttp:4.10.0'
}
```

## 优点

如果是单个module的项目非常适合这种比较简单的方式，一目了然。远端依赖如果升级了新的版本会有提供升级的功能。

## 缺点

如果项目中有多个不同的module，你需要在多个module的build.gradle文件中都做对应的配置，还要确保依赖的库的版本号一致，配置项要重复编写多次。

# 三.使用gradle的extra属性(推荐)

## 简介

Google在[Android官方文档](https://developer.android.com/studio/build/gradle-tips#configure-project-wide-properties)中推荐通过使用gradle的extra属性，将依赖及版本号编写到config.gradle配置文件中，每个module都去依赖config.gradle中的版本，从而达到统一管理的目的。

**Root-level config.gradle**

```
ext {
  versions = [
    core_ktx: "1.7.0",
    appcompat: "1.4.1",
    okhttp: "4.10.0"
  ]
  libs = [
    core_ktx :"androidx.core:core-ktx:${versions.core_ktx}",
    appcompat: "androidx.appcompat:appcompat:${versions.appcompat}",
    okhttp: "com.squareup.okhttp3:okhttp:${versions.rxjava}"
  ]
}
```

**Root-level build.gradle**

```
apply from: "config.gradle"

```

**module_a/build.gradle**

```

dependencies {
    implementation libs.core_ktx
    implementation libs.appcompat
    implementation libs.okhttp
}    
```

**module_b/build.gradle**

```
dependencies {
    implementation libs.core_ktx
    implementation libs.appcompat
    implementation libs.okhttp
}   
```

## 优点

将版本统一管理起来了，只需要更改config.gradle中的版本号就可以对所有module的依赖版本进行修改。

## 缺点

- 不支持代码补全提示。
- 不支持单击跳转。
- 多模块开发时，不同模块相同的依赖需要复制粘贴。
- 依赖版本更新不会提示。

# 四.使用buildSrc管理(推荐)

## 简介

[Gradle文档](https://docs.gradle.org/current/userguide/organizing_build_logic.html#sec:build_sources)中说到:当运行 Gradle 时会检查项目中是否存在一个名为 buildSrc 的目录。 然后Gradle 会自动编译并测试这段代码，并将其放入构建脚本的类路径中， 对于多项目构建，只能有一个 buildSrc 目录，该目录必须位于根项目目录中， buildSrc 是 Gradle 项目根目录下的一个目录， 它可以包含我们的构建逻辑，与脚本插件相比，buildSrc应该是首选，因为它更易于维护、重构和测试代码。

## 使用步骤

1.项目根目录下新建一个名为buildSrc的文件夹(注意：名字必须是 buildSrc，因为上文提到了运行 Gradle 时会检查项目中是否存在一个名为 buildSrc 的目录)，然后在 buildSrc 文件夹里创建名为 build.gradle.kts 的文件。

**build.gradle.kts**

```
plugins {
    `kotlin-dsl`
}

repositories {
    mavenCentral()
    google()
    gradlePluginPortal()
}
```

2. buildSrc下新建目录``src\main\kotlin``这里的目录只是建议，输入其他的名称也是可以的。

3. 在``src\main\kotlin``中创建Dependencies.kt等配置文件:
   **Dependencies.kt**

```
object BuildVersion {
    const val compileSdk = 30
    const val buildTools = "30.0.2"
    const val minSdk = 21
    const val targetSdk = 30
    const val versionCode = 1
    const val versionName = "1.0.0"
}

object Versions {
    val core_ktx = "1.7.0"
    val appcompat = "1.4.1"
    val okhttp = "4.10.0"
}

object Libs {
    val core_ktx = "androidx.core:core-ktx:${Versions.core_ktx}"
    val appcompat = "androidx.appcompat:appcompat:${Versions.appcompat}"
    val okhttp = "com.squareup.okhttp3:okhttp:${Versions.okhttp}"
}
```

4.经过上面步骤后，执行一次Gradle Sync任务，就可以在Android Studio中访问Dependencies.kt中任何值了。 看起来结果与“ext”方式非常相似，但是它支持自动补全和单击跳转功能。

**module_a/build.gradle**

```
android {
    compileSdkVersion BuildVersion.compileSdk
    buildToolsVersion BuildVersion.buildTools

    defaultConfig {
        minSdkVersion BuildVersion.minSdk
        targetSdkVersion BuildVersion.targetSdk
        versionCode BuildVersion.versionCode
        versionName BuildVersion.versionName
        ...
    }

    ...
}

dependencies {
    implementation Libs.core_ktx
    implementation Libs.appcompat
    implementation Libs.okhttp
}
```

**module_b/build.gradle**

```
android {
    compileSdkVersion BuildVersion.compileSdk
    buildToolsVersion BuildVersion.buildTools

    defaultConfig {
        minSdkVersion BuildVersion.minSdk
        targetSdkVersion BuildVersion.targetSdk
        versionCode BuildVersion.versionCode
        versionName BuildVersion.versionName
        ...
    }

    ...
}

dependencies {
    implementation Libs.core_ktx
    implementation Libs.appcompat
    implementation Libs.okhttp
}
```

## 优点

- 将版本统一管理起来了，我们只需要更改Dependencies.kt中的版本号就可以对所有module的依赖版本进行修改。
- 支持 AndroidStudio 自动补全。
- 支持依赖库的点击跳转。

## 缺点

- buildSrc 依赖更新将重新构建整个项目，buildSrc 依赖更新将重新构建整个项目，项目越大，重新构建的时间就越长，造成不必要的时间浪费。
- 依赖版本更新不会提示。

# 五.使用Composing builds管理

## 简介

摘自 [Gradle 文档](https://docs.gradle.org/current/userguide/composite_builds.html)：复合构建只是包含其他构建的构建. 在许多方面，复合构建类似于 Gradle 多项目构建，不同之处在于，它包括完整的 builds，而不是包含单个 projects

## 使用步骤

1. 新建Android library工程module名为version_plugin，包名为com.huke.plugin（非固定名可以自取）并删除多余的文件及文件夹。
   ![](https://img-blog.csdnimg.cn/b60e9f16fab64aea92dca72425bbb08e.png)

2. 修改version_plugin工程中的 build.gradle文件。

```
apply plugin: 'kotlin'
apply plugin: 'java-gradle-plugin'

buildscript {
    repositories {
        google()
        maven { url 'https://jitpack.io' }
        maven { url 'https://maven.aliyun.com/nexus/content/groups/public/' }
        maven { url 'https://maven.aliyun.com/nexus/content/repositories/jcenter' }
        gradlePluginPortal()
        mavenCentral()
    }

    dependencies {
        // 因为使用的 Kotlin 需要需要添加 Kotlin 插件，需要和主工程对应，不然就出现两个版本了
        classpath "org.jetbrains.kotlin:kotlin-gradle-plugin:1.7.0"
    }

}

repositories {
    google()
    maven { url 'https://jitpack.io' }
    maven {url 'https://maven.aliyun.com/nexus/content/repositories/releases/'}
    maven { url 'https://maven.aliyun.com/nexus/content/groups/public/' }
    maven { url 'https://maven.aliyun.com/nexus/content/repositories/jcenter' }
    mavenCentral()
}

dependencies {
    //添加Gradle相关的API，否则无法自定义Plugin和Task
    implementation gradleApi()
    implementation "org.jetbrains.kotlin:kotlin-gradle-plugin:1.7.0"
}

compileKotlin {
    kotlinOptions {
        jvmTarget = "1.8"
    }
}

compileTestKotlin {
    kotlinOptions {
        jvmTarget = "1.8"
    }
}

gradlePlugin {
    plugins {
        version {
            // 在 app 模块需要通过 id 引用这个插件
            id = 'com.huke.plugin'
            // 实现这个插件的类的路径
            implementationClass = 'com.huke.version.VersionPlugin'
        }
    }
}
```

> 注意，插件中的build.gradle文件中的 kotlin-gradle-plugin 版本要和主工程对应。

3. 在项目 settings.gradle 文件内添加``includeBuild("version_plugin")``，添加完毕以后可以Rebuild项目。

```
includeBuild('version_plugin')
```

4. 在plugin-version module中创建VersionPlugin类，继承Plugin。这里可以空实现，也可以根据需求添加其他代码。

```
import org.gradle.api.Plugin
import org.gradle.api.Project

class VersionPlugin : Plugin<Project> {
    override fun apply(target: Project) {

    }
}
```

5.在plugin-version module中创建``Deps.kt``文件用来管理依赖包和版本号，可以声明多个kt文件。

```
/**
 * 配置和 build相关的
 */
object BuildVersion {
    const val compileSdk = 30
    const val buildTools = "30.0.2"
    const val minSdk = 21
    const val targetSdk = 30
    const val versionCode = 1
    const val versionName = "1.0.0"
    
}

object Versions {
    val core_ktx = "1.7.0"
    val appcompat = "1.4.1"
    val okhttp = "4.10.0"
}

object Libs {
    val core_ktx = "androidx.core:core-ktx:${Versions.core_ktx}"
    val appcompat = "androidx.appcompat:appcompat:${Versions.appcompat}"
    val okhttp = "com.squareup.okhttp3:okhttp:${Versions.okhttp}"
}
```

6. 在app或module的 build.gradle 中使用plugin-version中的依赖
   **module_a/build.gradle**

```
plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
    id 'com.ileo.plugin.version'
    //引用插件框架
    id 'com.huke.plugin'
}
/导入依赖包下的类
import com.huke.version.*
android {
    compileSdk BuildVersion.compileSdk

    defaultConfig {
        applicationId "com.huke.composingbuildsdemo"
        minSdk BuildVersion.minSdk
        targetSdk BuildVersion.targetSdk
        versionCode BuildVersion.versionCode
        versionName BuildVersion.versionName

        testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }
    kotlinOptions {
        jvmTarget = '1.8'
    }
}

dependencies {
    //引用依赖
    implementation Dependencies.core_ktx
    implementation Dependencies.appcompat
    implementation Dependencies.okhttp
}
```

**module_b/build.gradle**

```
plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
    id 'com.ileo.plugin.version'
    //引用插件框架
    id 'com.huke.plugin'
}
/导入依赖包下的类
import com.huke.version.*
android {
    compileSdk BuildVersion.compileSdk
    defaultConfig {
        applicationId "com.huke.composingbuildsdemo"
        minSdk BuildVersion.minSdk
        targetSdk BuildVersion.targetSdk
        versionCode BuildVersion.versionCode
        versionName BuildVersion.versionName

        testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }
    kotlinOptions {
        jvmTarget = '1.8'
    }
}

dependencies {
    //引用依赖
    implementation Dependencies.core_ktx
    implementation Dependencies.appcompat
    implementation Dependencies.okhttp
}
```

> tip 如果import com.huke.version.*无法导入可以先使用implementation添加依赖再进行import导包或者 使用com.huke.version.Dependencies.okhttp进行导入。

## 优点

- 支持依赖统一管理。
- 支持单向跟踪。
- 代码自动补全。
- 依赖更新时，不会重新构建整个项目。

## 缺点

- 配置较为复杂。
- 依赖版本更新不会提示。

# 六.总结

直接编写(默认方式)这种方式适合单一module项目使用，并且它并不是一无是处，在远端的依赖版本更新时，它会有提示功能，这是其他几种方式目前无法做到的。使用gradle的extra属性这种方式是google之前推荐的一种方式，不过它并不支持点击跳转，如果要查看依赖的详情必须要进行搜索查看找到对应的源头进行查看。 使用buildSrc管理这种方式比较简单，支持跳转，但是要注意版本号变更以后编译时间比较长。使用Composing builds管理也支持跳转，但是配置稍复杂。目前看来这几种方案似乎都没有做到完美，大家可以根据自己的工程灵活选择其中一种方式使用。

# 扩展阅读

[统一依赖管理Composing builds](https://blog.csdn.net/chuyouyinghe/article/details/122500139)
[项目依赖统一管理方案](https://www.jianshu.com/p/8bbd415ac55f)
[Android项目管理依赖方式总结](https://blog.csdn.net/yubo_725/article/details/118895551)
[Android - 依赖统一管理](https://juejin.cn/post/7037371592816459806)
[再见吧 buildSrc, 拥抱 Composing builds 提升 Android 编译速度](https://juejin.cn/post/6844904176250519565#heading-3)
[Composing builds](https://blog.csdn.net/weixin_35691921/article/details/126381834)
[统一依赖管理Composing builds](https://blog.csdn.net/chuyouyinghe/article/details/122500139)
