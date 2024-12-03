---
title: 上传Aar到maven库
---

# 方式一:
```
plugins {
    id 'com.android.library'
    id 'org.jetbrains.kotlin.android'
    id 'maven-publish'
}

task androidSourceJar(type: Jar) {
    from android.sourceSets.main.java.getSrcDirs()//源码路径 包括Java和Kotlin源码
    archiveClassifier.set("sources")
}

afterEvaluate {
    publishing {
        publications {
            plugin(MavenPublication) {
                artifact androidSourceJar // 增加上传源码的 task
                afterEvaluate { artifact(tasks.getByName("bundleReleaseAar")) }
                groupId = 'com.peng'
                artifactId = 'imageloader'
                version = '1.1.0'
            }
        }
        repositories {
            maven {
                url = 'https://packages.aliyun.com/maven/repository/2327308-release-bYyYbx/'
                credentials {
                    username = '63dcce3babc54e81b83ad6cb'
                    password = 'do0qQ1PvgsF-'
                }
            }
            maven {
                url = 'https://packages.aliyun.com/maven/repository/2327308-snapshot-qzGl2I/'
                credentials {
                    username = '63dcce3babc54e81b83ad6cb'
                    password = 'do0qQ1PvgsF-'
                }
            }
        }
    }
}
```
# 方式二:
```
plugins {
    id 'com.android.library'
    id 'org.jetbrains.kotlin.android'
    id 'maven-publish'
}

afterEvaluate {
    publishing {
        publications {
            plugin(MavenPublication) {
                // 添加以下配置可以自动从编译容器中获取release版本内容（使用debug可以获取debug版本内容），并生成pom文件
                // 注意：发布物声明必须在 afterEvaluate 内部，因为 components 在 afterEvaluate 阶段才生成完成
                from components.release
                groupId = 'com.peng'
                artifactId = 'imageloader'
                version = '1.1.0'
            }
        }
        repositories {
            maven {
                url = 'https://packages.aliyun.com/maven/repository/2327308-release-bYyYbx/'
                credentials {
                    username = '63dcce3babc54e81b83ad6cb'
                    password = 'do0qQ1PvgsF-'
                }
            }
            maven {
                url = 'https://packages.aliyun.com/maven/repository/2327308-snapshot-qzGl2I/'
                credentials {
                    username = '63dcce3babc54e81b83ad6cb'
                    password = 'do0qQ1PvgsF-'
                }
            }
        }
    }
}
```
# 说明文档

伴随着正式的JDK 11环境以及 Gradle 7.0，迎来了一系列的 gradle 编译问题，当然，这里主要讨论 maven 发布相关的变更与适配。

这里直接抛出主要问题：以前的 **maven **plugin 已经被废弃，带来的是 **maven-publish** plugin 。从代码层面讲就是：

```
apply plugin: 'maven'
```

变成了：

```
apply plugin: 'maven-publish'
```

同时，相关脚本也进行了变更，直接贴上最新的脚本代码：

```
afterEvaluate {
    publishing {
        publications {
            release(MavenPublication) {
                 from components.release 
                groupId = MAVEN_GROUP_ID
                artifactId = MAVEN_ARTIFACTID
                version = MAVEN_VERSION
            }
        }

        repositories {
            maven {
                allowInsecureProtocol true
                name = "nexus"
                url = MAVEN_RELEASE_URL
                credentials {
                    username = MAVEN_USERNAME
                    password = MAVEN_PASSWORD
                }
            }
        }
    }
}
```

这里大写的属性均为 gradle.properties 中定义的与 maven 发布相关的变量，通过命名应该很容易知道。

主要说两点:

* 对于非 https 的仓库地址，需要使用 `allowInsecureProtocol` 字段，包括引用该仓库的地方
* 对于需要上传的 maven 仓库，需要显式指定 name，因为在编译后，会生成相关任务，比如这样：

[![](https://img-blog.csdnimg.cn/img_convert/4fac4c22748bc7fb17c3cda116949020.png)](http://i.lckiss.com/wp-content/uploads/2021/08/2021080206190183.png)

另外，对于 release(MavenPublication) 节点中 `from components.<strong>release<span> </span></strong>`字段，是有含义的~ 官网描述如下：

[![](https://img-blog.csdnimg.cn/img_convert/19f4152760ea79193b5bb931c0e7a7aa.png)](http://i.lckiss.com/wp-content/uploads/2021/08/2021080206253739.png)

换成中文说就是：一个 module 的不同变种。

而对于 Android 来说，一般情况下有两种 lib，一种是 比如 gradle 插件的 Jar lib，另一种为 资源库类型的 AAR lib，这里分开说明。

* Jar lib

纯 jar 包，也就是 gradle 配置为：`apply<span> </span><strong>plugin</strong>:<span> </span><strong>'java-library'</strong>` 类型的 module，直接按照官方的例子进行配置：

```
from components.java
```

* AAR lib

对于 Android 特有的lib，即 gradle 配置为：`apply<span> </span><strong>plugin</strong>:<span> </span><strong>'com.android.library'</strong>` 类型的 module，则需要根据 module 中的buildTypes 进行配置，比如：

```
buildTypes {
    release {
        minifyEnabled false
        proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
    }
    debug {
        minifyEnabled false
    }
}
```

那么就有两种选择：

```
from components.release 
或
from components.debug
```

即会上传不同版本的 aar 文件，这里还可以添加 Android 的风味，即：productFlavors，不进行赘述，详见官方文档：

[https://developer.android.com/studio/build/build-variants?hl=zh-cn](https://developer.android.com/studio/build/build-variants?hl=zh-cn)


# 处理依赖传递问题
依赖传递是使用仓库的一个便利之处，就是我们只需要引入某个库的依赖，这个库所依赖的其他依赖项，都会自动依赖到项目中，完成这一个功能主要依靠 pom.xml 文件的配置信息。 pom.xml 文件中声明了关联的所有依赖，其中 <scope> 节点定义了依赖的传递类型，其中包括以下几种：

compile：依赖在编译时起作用，具有传递性；
provided：依赖在编译或者测试时起作用，跟 compile 类似，但是无传递性；
runtime：依赖在运行时或者测试时起作用，编译时不起作用，不具备传递性；
test：依赖在测试时起作用，运行时不起作用；
system：跟 provided 非常类似，主要不同之处是 system 需要我们在系统中直接指定一个特定的jar，需要配合 <systemPath> 使用，这个 scope 已经废弃。
import：Maven 2.0.9 之后新增，仅在依赖类型为 pom 时（由<type>节点指定）有用。表示此项依赖将会被 pom 文件中所有有效的依赖替代。
其实我们常用的是上面的四种，对于手动生成 pom 文件，可以根据需求进行手动指定映射，但是对于自动生成 pom 文件的情况，我们就必须清楚在 AndroidStudio 的依赖声明中，依赖类型默认映射是怎样的，才能准确实现依赖传递。下面是常用的部分

AndroidStudio依赖类型	Maven 依赖类型
implementation	runtime
api	compile
provided	provided
runtimeOnly	runtime
compileOnly	-
testImplementation	-
从前面的介绍我们知道，Maven 中只有 compile 依赖才具有传递性，因此，在AndroidStudio中使用 maven-pulbish 插件发布工件，如果使用自动生成 pom 文件，那么就需要在 build.gradle 文件中声明依赖是，对需要传递的依赖使用 api 来声明。

__注意事项：旧版的maven插件的映射有所不同，其中implementation映射为compile，因此如果你的项目从旧版迁移到新版插件，切记一定要修改依赖声明，否则会出现需要传递的依赖无法传递的问题。<scope>节点未指定时，默认为compile，如果手动生成pom文件，没有指定<scope>将采用默认值，但是建议显式指定<scope>值。 __

#使用生成的aar

在settings.gradle中要先把公司的maven仓库地址设置好，如下：
```
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()

        // 公司仓库
        maven {
            allowInsecureProtocol = true // 仓库默认不允许使用非https协议，所以这里设置为允许
            url 'http://192.168.1.251:8081/content/repositories/android_repositories/'
        }
    }
}
rootProject.name = "ContextHolderLib"
include ':app'
include ':ContextHolder'
```

设置好仓库地址后，就可以在module的build.gradle中依赖我们的aar库了，如下：
```
dependencies {

    implementation 'androidx.core:core-ktx:1.5.0'
    implementation 'androidx.appcompat:appcompat:1.2.0'
    
    // ContextHolder
    implementation 'cn.android666.contextholder:contextholder:1.1.1'
}
```

# 参考文档
[Android：发布aar包到maven仓库以及 maven插件 和 maven-publish 插件的区别](https://juejin.cn/post/7017608469901475847#heading-0)
[Android studio通过Gradle7发布aar到maven私有仓库](https://www.jianshu.com/p/e55401f7e462)
[Android：发布aar包到maven仓库； maven插件 和 maven-publish 插件的区别](https://blog.csdn.net/h_bpdwn/article/details/122479437)