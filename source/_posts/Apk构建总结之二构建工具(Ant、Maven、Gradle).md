---
title: Apk构建总结之二构建工具(Ant、Maven、Gradle)
---

# 一. 构建工具
### 1.什么是构建工具？
在进行编程操作的时候，我们经常会遇到很多与编程无关的项目管理工作。如下载依赖、编译源码、单元测试、项目部署等操作。
一般的，小型项目我们可以手动实现这些操作，然而大型项目这些工作则相对复杂。所以我们需要用到构建工具。
构建工具是帮助我们实现一系列项目管理、测试和部署操作的工具。构建工具可以把源代码生成可执行应用程序的过程自动化的程序（例如Android app生成apk）。
构建工具包括编译、连接跟把代码打包成可用的或可执行的形式。

总的来说构建的自动化是编写或使一大部分任务自动执行的一个动作，而这些任务则是软件开发者的日常，像是：
- 下载依赖。
- 将源代码编译成二进制代码。
- 打包生成的二进制代码。
- 进行单元测试。
- 部署到生产系统。
### 2.为什么要使用构建工具？
比如我们要写一个Java程序，一般的步骤也就是编译，测试，打包。这个构建的过程，如果文件比较少，我们可以手动使用java, javac, jar命令去做这些事情。
但当工程越来越大，文件越来越多，这个事情就不是那么地令人开心了。因为这些命令往往都是很机械的操作。但是我们可以把机械的东西交给机器去做。

>Java世界中主要有三大构建工具：Ant、Maven和Gradle。
# 二. Java构建工具
### 1.java平台常用的构建工具之Ant.
Ant 是由 Java 编写的构建工具，它的核心代码是由Java编写的，因此具有平台无关性，构建脚本是XML格式的（默认为bulid.xml）。
例如:下面列出一个ant工具所使用的build.xml:
```xml
<?xml version="1.0" encoding="UTF-8" ?>  
<project name="HelloWorld" default="run" basedir=".">  
<property name="src" value="src"/>  
<property name="dest" value="classes"/>  
<property name="jarfile" value="hello.jar"/>  
<target name="init">  
   <mkdir dir="${dest}"/>  
</target>  
<target name="compile" depends="init">  
   <javac srcdir="${src}" destdir="${dest}"/>  
</target>  
<target name="build" depends="compile">  
   <jar jarfile="${jarfile}" basedir="${dest}"/>  
</target>  
<target name="test" depends="build">  
   <java classname="test.ant.HelloWorld" classpath="${hello_jar}"/>  
</target>  
<target name="clean">  
   <delete dir="${dest}" />  
   <delete file="${hello_jar}" />  
</target>  
</project> 
```
ant的构建脚本还是比较清楚的。ant定义了五个任务，init, compile, build, test, clean。每个任务做什么都定义清楚了。
打包之前要先编译，所以通过depends来指定依赖的路径。如果在命令行里执行ant build，那就会先执行compile，而compile又依赖于init，所以就会先执行init。有了这个东西以后，我们只要一条命令：
```
ant test
```
就可以执行编程，打包，测试了。为开发者带来了很大的便利。
但是ant有一个很致命的缺陷，那就是没办法管理依赖。我们一个工程，要使用很多第三方工具，不同的工具，不同的版本。
每次打包都要自己手动去把正确的版本拷到lib下面去，这个工作既枯燥还特别容易出错。为了解决这个问题，maven登场了。
### 2.java平台常用的构建工具之maven.
Maven作为后来者，继承了Ant的项目构建功能，同样采用了XML作为构建脚本的格式。Maven具有依赖管理和项目管理的功能，提供了中央仓库，能帮助我们自动下载库文件。
maven最核心的改进就在于提出仓库这个概念。我可以把所有依赖的包，都放到仓库里去，在我的工程管理文件里，标明我需要什么什么包，什么什么版本。
在构建的时候，maven就自动帮我把这些包打到我的包里来了。我们再也不用操心着自己去管理几十上百个jar文件了。这了达到这个目标，maven提出，要给每个包都标上坐标，这样，便于在仓库里进行查找。
所以，使用maven构建和发布的包都会按照这个约定定义自己的坐标，例如：
```
<?xml version="1.0" encoding="utf-8"?>
<project ...xmlns...>
    <groupId>cn.hinus.recruit</groupId>
    <artifactId>Example</artifactId>
    <version>0.1.0-SNAPSHOT</version>
		 
    <dependencies>
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.10</version>
        </dependency>
    </dependencies>
</project>
```
这样，就定义了包的坐标是cn.hinus.recruit:Example:0.1.0-SNAPSHOT，而我的工程要依赖junit:junit:4.10。那么maven就会自动去帮我把junit打包进来
。如果我本地没有junit，maven还会帮我去网上下载。下载的地方就是远程仓库，我们可以通过repository标签来指定远程仓库。
maven里抛弃了ant中通过target定义任务的做法，而是引入了生命周期的概念。
##### maven的缺点有:
- maven是使用xml进行配置的，语法不简洁。
- maven在约定优于配置这条路上走太远了。就是说，maven不鼓励你自己定义任务，它要求用户在maven的生命周期中使用插件的方式去工作。这有点像设计模式中的模板方法模式。
说通俗一点，就是我使用maven的话，想灵活地定义自己的任务是不行的

### 3.java平台常用的构建工具之Gradle.
gradle充分地使用了maven的现有资源。继承了maven中仓库，坐标，依赖这些核心概念。文件的布局也和maven相同。但同时，它又继承了ant中target的概念，我们又可以重新定义自己的任务了。
Gradle不用XML，它使用基于Groovy的专门的DSL或者或Kotlin DSL，从而使Gradle构建脚本变得比用Ant和Maven写的要简洁清晰。
Gradle样板文件的代码很少，这是因为它的DSL被设计用于解决特定的问题：贯穿软件的生命周期，从编译，到静态检查，到测试，直到打包和部署。Google采用Gradle作为Android OS的默认构建工具。

```groovy
// Apply the java plugin to add support for Java
apply plugin: 'java'

// In this section you declare where to find the dependencies of your project
repositories {
    // Use 'jcenter' for resolving your dependencies.
    // You can declare any Maven/Ivy/file repository here.
    jcenter()
}

// In this section you declare the dependencies for your production and test code
dependencies {
    // The production code uses the SLF4J logging API at compile time
    compile 'org.slf4j:slf4j-api:1.7.21'

    // Declare the dependency for your favourite test framework you want to use in your tests.
    // TestNG is also supported by the Gradle Test task. Just change the 
    // testCompile dependency to testCompile 'org.testng:testng:6.8.1' and add 
    // 'test.useTestNG()' to your build script.
    testCompile 'junit:junit:4.12'
}
```

# 三. Gradle,Gradle Wrapper和Android Plugin for Gradle。
### 1. [Gradle](https://docs.gradle.org/current/userguide/userguide_single.html)
Gradle是个构建系统，能够简化你的编译、打包、测试过程。
[gradle下载地址](http://services.gradle.org/distributions/)
### 2. [Gradle Wrapper](https://docs.gradle.org/current/userguide/gradle_wrapper.html)
Gradle Wrapper称为Gradle包装器，是对Gradle的一层包装。使用Gradle Wrapper可以在没有安装Gradle的情况下使用。
为什么需要Gradle Wrapper呢？比如在一个开发团队中，如果每进来一个成员，都需要在计算机中安装Gradle，这个时候运行Gradle的环境和版本就会对构建结果带来不确定性。
针对这个问题，Gradle提供了一个解决方案，那就是Gradle Wrapper，它是一个脚本，可以在计算机没有安装Gradle的情况下运行Gradle构建，并且能够指定Gradle的版本，
开发人员可以快速启动并运行Gradle项目，而不必手动安装，这样就标准化了项目，从而提高了开发效率。
``Gradle Wrapper生成的文件如下：``
```
|____gradle
| |____wrapper
| | |____gradle-wrapper.jar  //具体业务逻辑
| | |____gradle-wrapper.properties  //配置文件
|____gradlew  //Linux 下可执行脚本
|____gradlew.bat  //Windows 下可执行脚本
```
打开gradle/wrapper/gradle-wrapper.properties 文件就可以修改配置了。根据此配置Gradle Wrapper会自动下载合适的Gradle版本。默认情况下，下载位置是在$USER_HOME/.gradle/wrapper/dists。
```
#规定了解压后的gradle包放在哪里(一般是在~/.gradle/wrapper/dists目录)
distributionBase=GRADLE_USER_HOME 
distributionPath=wrapper/dists
#规定了gradle的zip包放在哪里
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
#规定了使用哪个版本的gradle编译项目，这个地址可以配置成服务器地址或者本地地址
distributionUrl=https\://services.gradle.org/distributions/gradle-3.3-all.zip
```
### 3. [Android Plugin for Gradle](https://developer.android.com/studio/releases/gradle-plugin)
Android Studio构建系统基于Gradle，Android Plugin for Gradle添加了一些特定于构建Android应用程序的功能。虽然Android插件通常与Android Studio保持同步更新，
但插件（以及Gradle系统的其余部分）可独立于Android Studio运行并单独更新。
在android studio中，项目的根目录下的build.gradle中会配置如下代码：
```
buildscript {
    
    repositories {
        google()
        jcenter()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:3.2.0'
        // NOTE: Do not place your application dependencies here; they belong
        // in the individual module build.gradle files
    }
}
```
这个dependencies中的gradle:3.2.0代表的就是使用gradle 插件版本 3.2.0.在编译过程中，如果gradle插件版本与gradle版本不匹配，编译就会失败.
目前在使用的gradle与gradle插件版本的对应。
![](https://upload-images.jianshu.io/upload_images/3067896-5c32446bcf99e9a4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

[gradle插件对应gradle版本](https://developer.android.google.cn/studio/releases/gradle-plugin?hl=zh_cn)
# 四. Android项目中配置gradle
### 1.顶级Gradle文件。
顶级 build.gradle 文件位于项目根目录，用于定义适用于项目中所有模块的构建配置。 默认情况下，此顶级构建文件使用 buildscript 代码块来定义项目中所有模块共用的 Gradle 存储区和依赖项。
```
/**
 * 构建块是您配置存储库和的位置
 * Gradle本身的依赖关系 - 意思是，你不应该包含依赖关系
 * 在这里你的模块。 例如，此块包含Android插件
 * Gradle作为依赖项，因为它提供了Gradle的附加指令
 * 需要构建Android应用程序模块。
 */
buildscript {
    /**
     * 存储库块配置Gradle使用的存储库
     * 搜索或下载依赖项。 Gradle预先配置对远程的支持
     * 依赖仓库，如JCenter，Maven Central和Ivy。 您也可以使用本地
     * 存储库或定义您自己的远程存储库。 下面的代码定义
     * JCenter作为存储库Gradle应该用来查找它的依赖项。
     *
     * 使用Android Studio 3.0及更高版本创建的新项目也包括
     * 谷歌的Maven存储库。
     */
    repositories {
        google()
        jcenter()
    }
    /**
     * dependencies块配置Gradle需要使用的依赖项
     * 建立你的项目。 以下行添加了Gradle的Android插件
     * 版本3.2.0作为类路径依赖项。
     */
    dependencies {
        classpath 'com.android.tools.build:gradle:3.2.0'
        // NOTE: Do not place your application dependencies here; they belong
        // in the individual module build.gradle files
    }
}
/**
 * allprojects块是您配置存储库和的地方
 * 项目中所有模块使用的依赖项，例如第三方插件
 * 或lib。 但是，您应该在其中配置特定于模块的依赖项
 * 每个模块级的build.gradle文件。 对于新项目，Android Studio
 * 默认情况下包括JCenter和Google的Maven存储库，但事实并非如此
 * 配置任何依赖项（除非您选择需要某些依赖项的模板）。
 */

allprojects {
    repositories {
        google()
        jcenter()
    }
}
```
- buildScript块的repositories主要是为了表示只有编译工具才会用这个仓库，获取脚本依赖插件。
- allprojects块的repositories用于多项目构建，为所有项目提供共同所需依赖包。而子项目可以配置自己的repositories以获取自己独需的依赖包。

### 2.模块级Gradle文件。
```
apply plugin: 'com.android.application'

android {
    //compilesdkversion指定Android API级别的Gradle应用于
    //编译你的应用程序。这意味着您的应用程序可以使用
    //此级别及更低级别的API。
    compileSdkVersion 28
    //buildToolsVersion指定Gradle用于构建应用程序的SDK构建工具，命令行工具和编译器的版本。 您需要使用SDK Manager下载构建工具。
    //此属性是可选的，因为默认情况下插件使用推荐版本的构建工具。
    buildToolsVersion "28.0.3"
    //defaultConfig块封装了所有构建变体的默认设置和条目，
    // 并且可以从构建系统动态覆盖main / AndroidManifest.xml中的某些属性。
    // 您可以配置产品flavor以覆盖应用程序的不同版本的这些值。
    defaultConfig {
        //applicationId唯一标识要发布的包。
        //但是，您的源代码仍应引用包名称
        //由main / AndroidManifest.xml文件中的package属性定义。
        applicationId "com.yousheng.myapplication"
        //定义运行应用程序所需的最低API级别。
        minSdkVersion 15
        //指定用于测试应用程序的API级别。
        targetSdkVersion 28
        versionCode 1
        versionName "1.0"
        testInstrumentationRunner "android.support.test.runner.AndroidJUnitRunner"
    }
    //您可以在buildTypes块中配置多个构建类型。
    // 默认情况下，构建系统定义了两种构建类型：debug和release。该
    //调试构建类型未在默认构建配置中显式显示，
    // 但它包含调试工具，并使用调试密钥进行签名。 发布
    // 构建类型应用Proguard设置，默认情况下不签名。
    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
        }
    }
}
//依赖项在模块级构建配置文件中阻止
//指定仅构建模块本身所需的依赖项。
dependencies {
    implementation fileTree(include: ['*.jar'], dir: 'libs')
    implementation 'com.android.support:appcompat-v7:28.0.0'
    implementation 'com.android.support.constraint:constraint-layout:1.1.3'
    testImplementation 'junit:junit:4.12'
    androidTestImplementation 'com.android.support.test:runner:1.0.2'
    androidTestImplementation 'com.android.support.test.espresso:espresso-core:3.0.2'
}
}

```
- **apply plugin** 表示应用了一个插件，该插件一般有两种值可选：
一种为'com.android.application'，表示该模块为应用程序模块，可以直接运行；另一种为'com.android.library'，表示该模块为库模块，只能作为代码库依附于别的应用程序模块来运行。
- **android{}**，在这个闭包中我们可以配置项目构建的各种属性。
- **buildToolsVersion** 构建工具的版本，其中包括了打包工具aapt、dx等等。可以用高版本的build-tool去构建一个低版本的sdk工程。
- **compileSdkVersion** 用于指定项目的编译版本，这里指定成28表示使用Android 8.0系统的SDK编译。只影响编译时的行为，不影响运行时的行为。代码中可用的api也要与该声明版本对应，高于声明版本的api则无法找到、使用。Support库的大版本号要与compileSdkVersion的大版本号相同 
![](https://upload-images.jianshu.io/upload_images/3067896-80cc96d553a093e0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- **minSdkVersion** 指明应用程序运行所需的最小API level。如果Android设备的系统API level低于android:minSdkVersion设定的值，那么android系统会阻止用户安装这个应用。如果指明了这个属性，并且在项目中使用了高于这个API level的API， 那么会在编译时报错。
- **targetSdkVersion** 表示你在该目标版本上已经做过了充分的兼容性处理和测试性处理，系统将会为你的应用程序启用一些最新的功能和特性。应用运行时使用的sdk版本
例如:
android6.0(api 23)系统的动态权限检查功能；targetSdkVersion<23时：该应用安装在android6.0的手机上后，不会执行android6.0系统以上特有的动态权限检查逻辑，而是仍继续执行以前的权限检查逻辑。
当targetSdkVersion变为23后：android6.0系统的动态权限检查特性将生效。
>一般minSdkVersion <targetSdkVersion<= compileSdkVersion；最好别随意更改targetSdkVersion，更改targetSdkVersion必须做好兼容。
- **buildTypes** 封装此项目的所有构建类型配置。

# 五 .Gradle添加构建依赖项
要为您的项目添加依赖项，请在您的 build.gradle 文件的 dependencies 程序块中指定依赖项配置。
例如:以下这个应用模块的 build.gradle 文件包括三种不同类型的依赖项：
```
apply plugin: 'com.android.application'

android { ... }

dependencies {
    // 依赖于本地库模块
    implementation project(":mylibrary")

    // 对本地文件的依赖性(jar,arr等)
    implementation fileTree(dir: 'libs', include: ['*.jar'])

    //依赖于远程文件
    implementation 'com.example.android:app-magic:12.3'
}

```
### 1. 本地library模块依赖。
```
implementation project(":mylibrary")
```
这段代码声明名为“mylibrary”的 Android 库模块的依赖项（该名称必须匹配使用 `settings.gradle`文件中的 `include:` 定义的库名称）。
在构建您的应用时，构建系统会编译库模块，并将生成的编译内容打包到 APK中。

### 2. 本地二进制文件依赖项。
```
implementation fileTree(dir: 'libs', include: ['*.jar'])
```
Gradle 声明项目 module_name/libs/ 目录中 JAR 文件的依赖项（因为 Gradle 会读取 build.gradle 文件的相对路径）。
或者，您也可以像下面这样指定单独的文件：
```
implementation files('libs/foo.jar', 'libs/bar.jar')
```
Gradle 声明项目 module_name/libs/ 目录中 aar 文件的依赖项:
```
android {
    ...
    repositories {
        flatDir {
            dirs 'libs'
        }
    }
}
```
```
dependencies {
    implementation(name: 'mylibrary-release', ext: 'aar')
}
```
### 3. 远程二进制文件依赖项。

缩写形式：
```
implementation 'com.example.android:app-magic:12.3'
```
全写形式：
```
implementation group: 'com.example.android', name: 'app-magic', version: '12.3'
```
这段代码声明“com.example.android”命名空间组内“app-magic”库 12.3 版本的依赖项。

**注意：**
``1.``与此类似的远程依赖项要求您声明相应的 
[远程代码库](https://developer.android.com/studio/build/dependencies#remote-repositories)，Gradle 应在其中寻找该库。 如果本地尚不存在该库，Gradle 会在构建需要它时（例如，当您点击 **Sync Project with Gradle Files** 或当您运行构建时）从远程站点获取该库。
``2.``指定依赖项时，不应使用动态版本号，比如 `'com.android.tools.build:gradle:3.+'`。 使用此功能，可能会导致意外版本更新和难以解析版本差异。

[mvnrepository仓库](http://mvnrepository.com/)

# 六. Gradle依赖仓库
### 1. 为何要使用远程依赖？
手动管理依赖将会带来很大麻烦。首先必须定位到该依赖文件位置，然后下载jar文件，复制该文件到项目，然后引用它们。
通常这些jar文件还没有具体的版本号，所以还必须去记忆它们的版本号，这样当需要更新的时候，才会知道需要替换成哪个版本。
同时必须将该依赖包放在svn或者git上，这样其他同事才可以不用手动去下载这些依赖jar。为了解决这些问题，就引入了远程依赖。

### 2. 远程依赖仓库分类
试想一下如果我们要把依赖放在远程，首先就要有一个存放依赖的仓库吧，所以**maven仓库**就是干这件事的。
在 Maven 的术语中，仓库是一个位置（place），例如目录，可以存储所有的工程 jar 文件、library jar 文件、插件或任何其他的工程指定的文件。

Maven 仓库有三种类型：
- 本地仓库（local）
- 远程仓库（remote）
- 中央仓库（central），(远程仓库的一种)在android开发中最常用

##### 本地仓库
Maven本地仓库是在计算机上的一个文件夹，用来存放所有的 jar等文件，本地仓库是远程仓库的一个缓冲和子集，当你构建Maven项目的时候，首先会从本地仓库查找资源，如果没有，那么Maven会从远程仓库下载到你本地仓库。这样在你下次使用的时候就不需要从远程下载了。如果你所需要的jar包版本在本地仓库没有，而且也不存在于远程仓库，Maven在构建的时候会报错，这种情况可能发生在有些jar包的新版本没有在Maven仓库中及时更新。需要由自己维护。Maven 本地仓库默认被创建在 %USER_HOME% 目录下。

##### 远程仓库
如果我们是library的作者，我们不想把library放到中央仓库的服务器上面，也可以放在自己定义的特有的maven仓库服务器上，这个时候如果别人想使用我们的library就需要先引入我们的仓库地址才能使用。

##### 中央仓库
也是属于远程仓库的一种这个仓库是由Maven社区管理，由Sonatype公司提供服务，其中包含了大量常用的库。且很容易被Apache Ant、Gradle和其他的构建工具使用，需要通过网络访问，通过：[http://search.maven.org/#browse](http://search.maven.org/#browse) 开发者就可以在里面找到自己所需要的代码库。

远程仓库和中央仓库的区别：
``远程仓库一般是由公司或团队创建的一个仓库，由公司或团队维护；中央仓库也是属于远程仓库的一种不过它是互联网上的仓库，由Maven团队维护；``

### 3. 依赖搜索顺序
![Maven 依赖搜索顺序](https://upload-images.jianshu.io/upload_images/3067896-1fad023bac20ada6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

当我们执行 Maven 构建命令时，Maven 开始按照以下顺序查找依赖的库：

- 步骤 1 ： 在本地仓库中搜索，如果找不到，执行步骤 2，如果找到了则执行其他操作。
- 步骤 2 ： 在中央仓库中搜索，如果找不到，并且有一个或多个远程仓库已经设置，则执行步骤 4，如果找到了则下载到本地仓库中已被将来引用。
- 步骤 3 ： 如果远程仓库没有被设置，Maven 将简单的停滞处理并抛出错误（无法找到依赖的文件）。
- 步骤 4 ： 在一个或多个远程仓库中搜索依赖的文件，如果找到则下载到本地仓库来被引用，否则 Maven 将停止处理并抛出错误（无法找到依赖的文件）。

### 2. Maven常见的远程仓库
![常见的仓库](https://upload-images.jianshu.io/upload_images/3067896-42c71b20c1c5f363.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###### MavenCentral仓库
Maven Central 则是由[sonatype.org](https://sonatype.org/)维护的Maven仓库。你可以在[这里](https://repo1.maven.org/maven2/)看到整个仓库。
在Android项目的build.gradle 文件中如下定义仓库，就能使用Maven Central了：

```
buildscript {
    repositories {
        mavenCentral()
    }
}
allprojects {
    repositories {
        mavenCentral()
    }
}

```
下载的本地仓库文件地址:
```
windows: C:\Users\用户名\.gradle\caches\modules-2\files-2.1
OSX: /Users/用户名/.gradle/caches/modules-2/files-2.1
```
>Android Studio早期版本使用的是mavenCentral，后来切换到jcenter了。

###### jcenter仓库
[jcenter](https://bintray.com/)是一个由 bintray.com维护的Maven仓库
在Android项目的的build.gradle 文件中如下定义仓库，就能使用jcenter了：
```
buildscript {
    repositories {
        jcenter()
    }
}
allprojects {
    repositories {
        jcenter()
    }
}
```
下载的本地仓库文件地址:
```
windows: C:\Users\用户名\.gradle\caches\modules-2\files-2.1
OSX: /Users/用户名/.gradle/caches/modules-2/files-2.1
```
>注意，虽然jcenter和Maven Central 都是标准的 android library仓库，但是它们维护在完全不同的服务器上，由不同的人提供内容，两者之间毫无关系。在jcenter上有的可能 Maven Central 上没有，反之亦然。

**Android为何有两个标准的仓库？**
事实上两个仓库都具有相同的使命：提供Java或者Android library仓库储存服务。上传到哪个（或者都上传）取决于开发者。起初，Android Studio 选择Maven Central作为默认仓库。
如果你使用老版本的Android Studio创建一个新项目，mavenCentral()会自动的定义在build.gradle中。但是Maven Central的最大问题是对开发者不够友好。上传library异常困难。
同时还因为诸如安全方面的其他原因，Android Studio团队决定把默认的仓库替换成jcenter。如今一旦使用最新版本的Android Studio创建一个项目，jcenter()自动被定义，而不是mavenCentral()。
至于为何google替换成jcenter的理由，下面是几个主要的原因：
- jcenter是全世界最大的Java仓库，因此在Maven Central 上有的，在jcenter上也极有可能有。换句话说jcenter是Maven Central的超集。
- 上传library到仓库很简单，不需要像在 Maven Central上做很多复杂的事情。
- jcenter通过CDN发送library，使用的是https协议，安全性更高，而Android Studio 0.8版本mavenCentral使用的是http协议
- jcenter性能方面比mavenCentral更优
- mavenCentral会自动下载很多与IDE相关的index，而这些用到的少，且不是必需

>注：不管是jcenter还是Maven Central ，两者都是Maven仓库。

###### 自建远程仓库
除了两个标准的中央仓库之外，如果我们使用的library的作者是**把该library放在自己的服务器上，我们还可以自己定义特有的Maven仓库服务器**。
[Twitter的Fabric.io](http://xn--twitterfabric-9j95a.io/) 就是这种情况，它们在[https://maven.fabric.io/public](https://maven.fabric.io/public)上维护了一个自己的Maven仓库。
如果你想使用Fabric.io的library，你必须自己如下定义仓库的url。

```
repositories {
    maven { url 'https://maven.fabric.io/public' }
}

```

然后在里面使用相同的方法获取一个library。

```
dependencies {
    compile 'com.crashlytics.sdk.android:crashlytics:2.2.4@aar'
	//新版as用 implementation 代替 compile
}

```
>library上传到标准的服务器与自建服务器仓库，哪种方法更好呢？这个需要看自身的需求。如果将自己的library公开，使得其他的开发者也能使用，则自建服务器仓库。

######  google仓库
在gradle4.1以后，添加了新的语法google()，用于引用google自有的仓库，很方便。由于google的仓库是不支持浏览的，只支持下载，所以不便于研究被依赖的aar源文件。
可以通过以下的网址查看支持支持下载的包: [google](https://dl.google.com/dl/android/maven2/index.html)
在Android项目的的build.gradle 文件中如下定义仓库，就能使用google了：
```
buildscript {
    repositories {
        google()
    }
}	
allprojects {
    repositories {
        google()
    }
}

```

下载的本地仓库文件地址:
```
windows: C:\Users\用户名\.gradle\caches\modules-2\files-2.1
OSX: /Users/用户名/.gradle/caches/modules-2/files-2.1
```

当然Android Studio自带了一些库，支持库在sdk中，gradle插件一般在Android Studio安装目录。

######  jitpack仓库
JitPack提供的仓库。在Android项目的build.gradle 文件中如下定义仓库，就能使用JitPack了：
```
buildscript {
    repositories {
          maven { url "https://jitpack.io" }
    }
}	
allprojects {
    repositories {
         maven { url "https://jitpack.io" }
    }
}
```

### 4. 远程仓库镜像（阿里云的国内镜像）
在国内使用jcenter、mavenCentral及google三个远程仓库，GradleSync会很慢，goole仓库甚至需要科学上网才能访问。为了加快Gradle Sync速度，可以优先使用阿里云镜像 仓库作为下载源。
如果下载相关依赖失败，可以尝试用镜像仓库地址。
```
buildscript {
    repositories {
        maven{ url 'https://maven.aliyun.com/repository/public'}
        maven { url 'https://maven.aliyun.com/repositories/jcenter' }
        maven { url 'https://maven.aliyun.com/repositories/google' }
        maven { url 'https://maven.aliyun.com/repository/central' }
        //jcenter()
        //mavenCentral()
        //google()
    }
}
     
allprojects {
    repositories {
        maven{ url 'https://maven.aliyun.com/repository/public'}
        maven { url 'https://maven.aliyun.com/repositories/jcenter' }
        maven { url 'https://maven.aliyun.com/repositories/google' }
        maven { url 'https://maven.aliyun.com/repository/central' }
        maven { url "https://jitpack.io" }
        //jcenter()
        //mavenCentral()
        //google()
    }
}
```
[阿里云仓库地址](https://maven.aliyun.com/mvn/view)

# 七. Gradle引入依赖方式
如果你想在Android项目中引入一个第三方library到你的项目，你只需添加如下的一行代码到模块的build.gradle文件中。
```
dependencies {
	compile 'com.squareup.okhttp:okhttp:2.4.0 
    //新版本as为implementation，代替compile
}
```
就是如此简单的一行代码，你就可以使用这个library了。引用一个library的代码需要3个部分，即：
**GROUP_ID、ARTIFACT_ID、VERSION**
在这句代码里面的 
- GROUP_ID 是com.squareup.okhttp， 有可能在同样的上下文中存在多个不同功能的library。如果library具有相同的group，那么它们将共享一个GROUP_ID。通常我们以开发者包名紧跟着library的group名称来命名，比如com.squareup.okhttp。
- ARTIFACT_ID 是okhttp， 就是library的真实名称。
- VERSION 是2.4.0 就是版本号而已，虽然可以是任意文字，建议设置为x.y.z的形式，如果喜欢还可以加上beta这样的后缀。

上面以Square library的一个例子。你可以看到每个都可以很容易的分辨出library和开发者的名称。

添加了上面的依赖之后，Gradle会询问Maven仓库服务器这个library是否存在，如果存在，gradle会获得请求library的路径，一般这个路径都是这样的形式：GROUP_ID/ARTIFACT_ID/VERSION_ID。
比如可以在[http://jcenter.bintray.com/com/squareup/otto/1.3.7](http://jcenter.bintray.com/com/squareup/otto/1.3.7) 和 
[https://oss.sonatype.org/content/repositories/releases/com/squareup/otto/1.3.7/](https://oss.sonatype.org/content/repositories/releases/com/squareup/otto/1.3.7/)
下获得com.squareup: okhttp:2.4.0的library文件。然后Android Studio 将下载这些文件到我们的电脑上，与我们的项目一起编译。整个过程就是这么简单。

>**从仓库上下载的library只是存储在仓库服务器上的jar 或者aar文件而已**。有点类似于自己去下载这些文件，拷贝然后和项目一起编译。但是使用gradle依赖管理的最大好处是你除了添加几行文字之外啥也不做。
添加完依赖就会下载库然后和项目一起编译。


在 dependencies {}内，您可以使用几种不同依赖项配置中的一种（例如上文所示的 implementation）声明库依赖项。 每项依赖项配置都为 Gradle 提供有关如何使用依赖项的不同说明。 
下表介绍您可以在 Android 项目中对依赖项使用的每种配置。 此表还将这些配置与自 ``Android Gradle Plugin 3.0.0`` 起弃用的配置进行比较。

| 新配置 | 已弃用配置 | 行为 |
| --- | --- | --- |
| `implementation` | `compile` | Gradle 会将依赖项添加到编译类路径，并将依赖项打包到构建输出。但是，当您的模块配置 `implementation` 依赖项时，会告知 Gradle 您不想模块在编译时将依赖项泄露给其他模块。使用此依赖项配置而不是 `api` 或 `compile`（已弃用），可以**显著缩短构建时间**，因为它可以减少构建系统需要重新编译的模块数量。例如，如果 `implementation` 依赖项更改了其 API，Gradle 只会重新编译该依赖项和直接依赖它的模块。大多数应用和测试模块都应使用此配置。
| `api` | `compile` | Gradle 会将依赖项添加到编译类路径，并构建输出。当模块包括 `api` 依赖项时，会告知 Gradle 模块想将该依赖项间接导出至其他模块，以使这些模块在运行时和编译时均可使用该依赖项。此配置的行为类似于 `compile` （现已弃用），但您应仅对需要间接导出至其他上游消费者的依赖项慎重使用它。 这是因为，如果 `api` 依赖项更改了其外部 API，Gradle 会重新编译可以在编译时访问该依赖项的所有模块。 因此，拥有大量 `api` 依赖项会显著增加构建时间。 如果不想向不同的模块公开依赖项的 API，库模块应改用 `implementation` 依赖项。
| `compileOnly` | `provided` | Gradle 只会将依赖项添加到编译类路径（即不会将其添加到构建输出）。如果是创建 Android 模块且在编译期间需要使用该依赖项，在运行时可选择呈现该依赖项，则此配置会很有用。如果使用此配置，则您的库模块必须包含运行时条件，以便检查是否提供该依赖项，然后妥善更改其行为，以便模块在未提供依赖项的情况下仍可正常工作。这样做不会添加不重要的瞬时依赖项，有助于缩减最终 APK 的大小。 此配置的行为类似于 `provided` （现已弃用）。
| `runtimeOnly` | `apk` | Gradle 只会将依赖项添加到构建输出，供运行时使用。也就是说，不会将其添加到编译类路径。 此配置的行为类似于 `apk`（现已弃用）。 |
| `annotationProcessor` | `compile` | 要在库中添加注解处理器依赖项，则必须使用 `annotationProcessor` 配置将其添加到注解处理器类路径。这是因为使用此配置可分离编译类路径与注解处理器类路径，从而提升构建性能。如果 Gradle 在编译类路径上找到注解处理器，则会停用[ 避免编译](https://docs.gradle.org/current/userguide/java_plugin.html#sec:java_compile_avoidance)功能，这样会增加构建时间（Gradle 5.0 和更高版本会忽略编译类路径上的注解处理器）。如果 JAR 文件包含以下文件，则 Android Gradle Plugin 会假定依赖项是注解处理器：`META-INF/services/javax.annotation.processing.Processor`。 如果插件检测到编译类路径上包含注解处理器，则会生成构建错误。 |

要为您的本地测试和设备化测试添加 implementation 依赖项，需要使用下面这样的代码：
```
dependencies {
    // Adds a remote binary dependency only for local tests.
    testImplementation 'junit:junit:4.12'

    // Adds a remote binary dependency only for the instrumented test APK.
    androidTestImplementation 'com.android.support.test.espresso:espresso-core:3.0.2'
}
```


- **implementation:** 会添加依赖到编译路径，并且会将依赖打包到输出（aar或apk），但是在编译时不会将依赖的实现暴露给其他module，也就是只有在运行时其他module才能访问这个依赖中的实现。只能在内部使用此模块，比如我在一个libiary中使用implementation依赖了gson库，然后我的主项目依赖了libiary，那么，我的主项目就无法访问gson库中的方法。
- **api:** 会添加依赖到编译路径，并且会将依赖打包到输出（aar或apk），与implementation不同，这个依赖可以传递，其他module无论在编译时和运行时都可以访问这个依赖的实现

**implementation 和api的区别:**
![](https://upload-images.jianshu.io/upload_images/3067896-4c6ecc4a018a8fcb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
``App Module``依赖于``LibraryA`` ,而``LibraryA ``依赖了`` LibraryB ``。如果``LibraryA ``对``LibraryB  ``的依赖用的是 ``implementation ``关键字。那么``LibraryB ``中的接口，仅仅只能给 ``LibraryA`` 使用,``App Module`` 是无法访问到 ``LibraryB`` 提供的接口的。如果``LibraryA ``对``LibraryB `` 的依赖用的是 ``api ``关键字,则``LibraryB ``中的接口，不仅可以给 ``LibraryA`` 使用,而且还可以给``App Module``使用。

- **compileOnly** Gradle把依赖加到编译路径，编译时使用，不会打包到输出（aar或apk）。这可以减少输出的体积，在只在编译时需要，在运行时可选的情况。
![](https://upload-images.jianshu.io/upload_images/3067896-3644485ad2e712f4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
如果``App Module``依赖于``A Lib、B Lib、C Lib``。``A Lib``和``B Lib``也依赖于``C Lib``。此时我们就可以让``A Lib``和``B Lib``通过``compileOnly ``去依赖于``C Lib``。减少依赖冲突的可能性。

- **runtimeOnly** 与compileOnly对应，gradle添加依赖只打包到APK，运行时使用，但不会添加到编译路径,会导致编译无法通过,一般是不会用到。

- **annotationProcessor** 用于注解处理器的依赖配置。

>注：Android Plugin for Gradle 3.0.0+ 不再支持 [`android-apt` 插件。](https://bitbucket.org/hvisser/android-apt)

# 八. 依赖管理
### 1. Gradle命令查看依赖层级树.
打开terminal控制台命令.
```
gradlew :app(模块名):dependencies  //列出所有的依赖
gradlew :app(模块名):dependencies >log.txt //查看依赖关系保存到log.txt文件夹下面
gradlew -q dependencies app:dependencies --configuration releaseRuntimeClasspath                
//列出某一环境下的依赖(实例为releaseRuntimeClasspath)
```
关于其他配置类型参数可以通过如下命令获得：
```
gradlew dependencies --info
```
![](https://upload-images.jianshu.io/upload_images/3067896-bddacbaf6a57ad55.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

>同一个库存在 多个版本时, gradle 会自动 使用最高版本的库 应用到 所有地方,如果后面带有 “(*)” 的库就表示 这个库 有被覆盖过。
### 2. 使用Gradle View插件查看依赖层级树。
1. 在plugins中找到Gradle View插件安装,重启As。
2. 在View->Tool windows->找到Gradle View点击。
![](https://upload-images.jianshu.io/upload_images/3067896-81f7d67e3098bbce.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 3. 传递依赖。
　在Maven仓库中，构件通过POM（一种XML文件）来描述相关信息以及传递性依赖。Gradle 可以通过分析该文件,获取所有的依赖以及依赖的依赖和依赖的依赖的依赖。
例如:
![](https://upload-images.jianshu.io/upload_images/3067896-d62668dcad48238d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
可以看到，我们的项目依赖了hibernate,然而hibernate却依赖了一众别的依赖.借助Gradle的传递性依赖特性，你无需再你的脚本中把这些依赖都声明一遍，你只需要简单的一行，Gradle便会帮你将传递性依赖一起下载下来。
```
  implementation 'org.hibernate:hibernate-core:3.6.3.Final'
```
传递依赖特性可以轻松地通过transitive参数进行开启或关闭,传递性依赖可以采用指定 transitive = false 的方式来关闭依赖传递特性，也可以采用添加@jar(@aar)的方式忽略该依赖的所有传递性依赖。
```
implementation ('org.hibernate:hibernate-core:3.6.3.Final'){
        transitive = false
    }
```
或者:
```
 implementation 'org.hibernate:hibernate-core:3.6.3.Final@jar'
```
查看依赖关系为:
![](https://upload-images.jianshu.io/upload_images/3067896-17d8b402ca84144c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

全局性的关闭依赖传递特性:
```
dependencies {
configurations.all {
   transitive = false
}
...
}
```
### 4. 排除依赖。
有些时候你可能需要排除一些传递性依赖中的某个模块，此时便不能靠单纯的关闭依赖传递特性来解决了。这时exclude就该登场了。exclude可以解决部分依赖传递问题。
- 依赖冲突时，如果有两个依赖引用了相同jar包的不同版本时，默认情况下gradle会采用最新版本的jar包，此时可以通过排除选项来排除。
- 运行期无需此模块的。
- 无法正常获取到此传递依赖，远程仓库都不存在的。
- 版权原因需要排除的。
比如说我需要对依赖模块mylibrary的support appcompat-v7和support support-annotations进行排除则可以使用:
```
   implementation('cn.qqtheme.framework:WheelPicker:1.5.1') {
        exclude group:'com.android.support' ,module: 'support-v4'
        exclude group:'com.android.support' ,module: 'support-annotations'
    }
```
排除前:
![](https://upload-images.jianshu.io/upload_images/3067896-73cab134d842ba71.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
排除后:
![](https://upload-images.jianshu.io/upload_images/3067896-84753a5de1eb6945.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# 九. AAR包.
### 1.aar对比jar的优势。
- jar文件：只包含class文件和清单文件，不包含资源文件，比如图片等所有的 res下的资源文件。
- aar文件:包含class文件以及res下的所有的资源文件。
### 2.创建aar包。
![](https://upload-images.jianshu.io/upload_images/3067896-70ddcdac48e8f932.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![](https://upload-images.jianshu.io/upload_images/3067896-df95fcc184838636.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 4.aar包容易出现的问题。
##### aar不得包含 assets 原始资源

工具不支持在库模块中使用原始资源文件（保存在 assets/ 目录中）。应用使用的任何原始资源都必须存储在应用模块自身的 assets/ 目录中。
##### minSdkVersion问题
AAR 作为相关应用模块的一部分编译，因此，库模块中使用的 API 必须与应用模块支持的平台版本兼容，所以 AAR 中的 minSdkVersion 要尽量的设置低一点。
##### AAR 内部三方库依赖的问题
```
使用 Android Studio 打包出来的 AAR ，不会将其依赖的三方库打包进去。
```
例如，library Test 依赖了 okhttp，打包成了 Test.aar ,app 使用本地方式引用了 Test.aar，但是无法使用 okhttp，为了不报错，app还需要添加 okhttp 依赖。
为什么 Android Studio 不能将Lib的多个依赖打包进AAR文件的原因是：将不同的library打包在一起，涉及到资源和配置文件智能合并，所以是个比较复杂的问题，同时也容易造成相同的依赖冲突。
这个问题可以通过使用 Maven 依赖解决。因为 library Module 上传 Maven 后，会生成 一个 .pom 文件，记录 library Module 的依赖。
当 Gradle 依赖 Maven 上的这个库时，会通过 pom 文件下载对应依赖。如果不想要对应依赖的话，可以通过下面的方法关闭 Gradle 的依赖传递。
```
//正常依赖
implementation 'com.chemao.android:chemao-sdk:1.2.3'

//关闭全部依赖传递-方法1
implementation 'com.chemao.android:chemao-sdk:1.2.3@aar'

//关闭全部依赖传递-方法2
implementation('com.chemao.android:chemao-sdk:1.2.3') {
        transitive = false
}
```
所以不建议使用本地aar的两个原因:
1. aar中的第三个库无法使用远程依赖
2. 如果使用本地maven,需要每个参与开发的人员都配置一个本地的maven仓库,不现实
##### 多级aar引用导致的问题
**问题描述**
ModuleLib B引用了一个aar,ModuleApp A引用了ModuleLib B,此时就会报找不到Lib的问题。
![](https://upload-images.jianshu.io/upload_images/3067896-05ec136e27cb3dfa.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
**问题分析**
对于 ModuleApp A来说，他们依赖了ModuleLib B，不管用不用，他们都会去把ModuleLib B的依赖走一遍，当走到添加的aar本地依赖时，他们去找aar的路径也需要给出，而且给的方式如果是libs这样的路径，它会去找自己包下的libs，里边自然没有。
**解决方式**

在ModuleApp A中给出ModuleLib B的lib目录:
```
android {
    ...
    repositories {
      flatDir {
            dirs  'libs','../ModuleLib B Name/libs'
        }
    }
}
```
##### aar包中的资源文件重复了
资源文件重复了，主工程的资源文件会直接覆盖aar包中的文件，并且不会有任何报错或者提示，最终aar包中也会直接用主工程的资源文件，所以需要注意命名方式。暂时没有更好的解决方法。

# 十. support支持库.
### 1. 添加support支持库的原因
Google为啥要弄这么多支持库，直接放到sdk里面不好么？ 参阅官方文档有下面3个原因：
- **向后兼容**
比如，我们开发的App需要支持的minSdkVersion=9，targetSdkVersion=11，在程序里使用了android 3.0 (API level 11)提供的ActionBar类，使用compileSdkVersion=11成功编译出apk。在android 3.0的设备上完美运行，但是app在android 2.3的设备就会crash，报找不到ActionBar的错误。这很好理解，因为旧版本上没有新版本里新增的类。为了避免使用了最新功能开发的app只能在最新系统的设备上运行的尴尬，官方把新版系统framework中新增加的接口提出来放到了Android Support Library（支持包）中，开发者在遇到上面的情况时，就可以使用支持包中具有同样功能的ActionBar类，这个支持包会打包进App里，这样使用了新版本系统上功能的App也可以向后兼容以前的老系统版本设备了。
使用支持包中的类除了让我们免于判断App运行的系统版本外，还可以使App在各个版本保持同样的用户体验。如在5.0以下系统使用material design。
``App编译时用的android sdk（android.jar）不会打包进我们的App中。因为App编码是使用android.jar中的接口就是android设备里系统框架层（framework）对外提供的接口。``

- **提供不适合打包进framework的功能**
Android官方对App开发提供了推荐设计，希望Android应用都有相对一致的交互设计来减少用户的使用成本，希望三方App类似系统应用从而完美融入到Android生态系统中。但是这都仅仅是推荐，不要求开发者一定要这样，如果有这种需求就可以使用官方支持包提供的这些功能，避免重复造轮子。如支持包中的DrawerLayout、Snackbar等类都是这种情况。
- **为了支持不同形态的设备**
通过使用支持包来在不同形态设备上提供功能，如手机、电视、可穿戴设备等。

### 2. support分类:
##### android-support-v4
```
compile "com.android.support:support-v4
```
2011年4月份，谷歌推出最低兼容到1.6版本系统的包。
eclipse新建工程时，都默认包含了，里面有类似Fragment，NotificationCompat，LoadBroadcastManager，ViewPager，PageTabAtrip，Loader，FileProvider  等等控件。V4包含了V7和V13的基础功能。

##### android-support-v7
```
compile "com.android.support:appcompat-v7:xx.xx"
```
2014年 I/O大会时推出，最低兼容Android2.1系统。最新的v7包增加了很多material design的兼容类和素材，其中涉及的内容有Theme、value、布局、新的控件、新的动画实现方式，包含了support-v4的全部内容。但是v7是要依赖v4这个包的，也就是如果要使用，两个包得同时被引用。
android studio在创建工程的时候默认导入了v7工程，并且将style使用了兼容style。

##### android-support-v13
为平板开发推出的版本兼容包，最低兼容Android3.2的系统。可以说Android 3.x系统都是平板专用系统。但是3.x系统失败了,所以使用v13的包没有任何价值。

### 3. androidX 
从android9.0 (API28)开始, support库将会进行改动, V7: 28.0.0将会是support库的终结版本。未来新的特性和改进都会进入Androidx包。其主要原因是support库的命名已经越来越令人迷惑 ，包越来越臃肿。
依赖包的变化从：
```
api 'com.android.support:appcompat-v7:28.0.0'
```
变成了：
```
api 'androidx.appcompat:appcompat:1.0.0'
```
需要注意的是，build.gradle中的插件版本要在3.2.0以上才可以。
![image.png](https://upload-images.jianshu.io/upload_images/3067896-8e118aacd0cffbcf.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# 十一. AndroidManifest合并冲突.
### 1. 问题描述
Android Studio 项目每个依赖的module中都可以有一个AndroidManifest.xml文件，但最终的APK 文件只能包含一个 AndroidManifest.xml 文件。在构建应用时，Gradle 构建会将所有清单文件合并到一个封装到 APK 的清单文件中。例如在app的manifest中有application节点下有label属性.app所依赖的mylibrary的manifest中application节点下也有label属性,打包的时候则会出现问题:
![](https://upload-images.jianshu.io/upload_images/3067896-53a74f698df12fbc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
打开manifest可以看到合并的信息中有报错:
![](https://upload-images.jianshu.io/upload_images/3067896-4797fc69cbf7b776.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
### 2. 解决问题
清单文件属性冲突时：用tools:replace="属性名"解决。例如上面例子是label属性存在冲突就可以使用:
```
 tools:replace="label"
```
参考资料：
[构建工具的进化：ant, maven, gradle]("https://zhuanlan.zhihu.com/p/24429133")
[Android官方文档之targetSdkVersion等介绍](https://developer.android.com/guide/topics/manifest/uses-sdk-element.html?utm_campaign=adp_series_sdkversion_010616#target)
[Android官方文档之支持库](https://developer.android.com/topic/libraries/support-library/index.html?hl=zh-cn)
[Android studio gradle系列二](https://www.jianshu.com/p/e1572ae877d8)
[构建工具的进化：ant, maven, gradle]("https://zhuanlan.zhihu.com/p/24429133")
[彻底弄明白Gradle相关配置](https://blog.csdn.net/yechaoa/article/details/80484468?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522161579764216780274140649%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=161579764216780274140649&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-5-80484468.first_rank_v2_pc_rank_v29&utm_term=gradle)
[Gradle 基本使用](https://blog.csdn.net/lixiong0713/article/details/110650986?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522161579764216780266224608%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=161579764216780266224608&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_v2~rank_v29-13-110650986.first_rank_v2_pc_rank_v29&utm_term=gradle)
[Gradle入门教程（三）：Gradle构建脚本基础](https://blog.csdn.net/LiMubai_CN/article/details/102761205?spm=1001.2014.3001.5502)
[Gradle插件从入门到进阶](https://juejin.cn/post/6844903838290296846)
[深入理解Android之Gradle](https://blog.csdn.net/Innost/article/details/48228651)