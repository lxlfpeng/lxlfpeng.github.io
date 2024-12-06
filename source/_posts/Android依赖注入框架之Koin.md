---
title: Android依赖注入框架之Koin
date: 2020-10-12
categories: 
  - Android开发
tags:
  - 依赖注入
---

# 一.依赖引入

Koin是一款轻量级的依赖注入框架，根据官方的描述，它无代理，无代码生成，无反射。
```
 def koinVersion = "2.2.2"
    //Koin for android
    implementation "org.koin:koin-android:$koinVersion"
    //Koin for scope feature
    implementation "org.koin:koin-android-scope:$koinVersion"
    //Koin for viewModel feature
    implementation "org.koin:koin-android-viewmodel:$koinVersion"

```

# 二.基础使用
在application中来做startkoin初始化的动作
```
class MyApp : Application() {
    override fun onCreate() {
        super.onCreate()
        startKoin {
            //开始启动koin
            androidContext(this@MyApp)//这边传Application对象,这样你注入的类中,需要app对象的时候,可以直接使用
            modules(appModule)//这里面传各种被注入的模块对象,支持多模块注入
        }
    }
    val appModule = module {//里面添加各种注入对象
    }
}
```
### 注入方式

|方法名	|描述	|使用|
|  -  | -  | - |
|single 	|生成单一对象	                         |  by inject()|
|factory	|每次都会生成新的对象	                     |    by inject()|
|viewModel	|用来创建ViewModel实例，默认生成的都是新对象 |	by viewModel(),通过get<T>()来获取的ViewModel是不同的对象|
|fragment	|用来创建fragment	                     |    by inject()|


##### 普通注入
使用方式--Factory注入
Factory注入方式跟普通new一个对象一样.factory就是获取的时候每次都生成一个新的实例.会创建多个对象
```
class Person {
 
}
```
创建一个Person类,然后在我们的MyApp中的appModule中,将该Person类注入一下
```
class MyApp : Application() {
      ...
        val appModule = module {//里面添加各种注入对象
        factory {//普通的注入方式
            Person()
        }
    }
}

```
在Activity中调用
```
class FactoryActivity : AppCompatActivity() {
    //调用方式有大致下面几种,后面会再说到
    val person: Person by inject()//方法一
    val person2 by inject<Person>()//方法二
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_factory)
        val person3 = get<Person>()//方法三
    }
}

```
##### 单例注入
Single用法
在MyApp中的appModule中,将该Person类使用方式为single注入一下
```
class MyApp : Application() {
      ...
        val appModule = module {//里面添加各种注入对象
        single  {//单例的注入方式
            Person()
        }
    }
}
```
在Activity中调用生成的三个注入对象是同一个
```
class FactoryActivity : AppCompatActivity() {
    //调用方式有大致下面几种,后面会再说到
    val person: Person by inject()//方法一
    val person2 by inject<Person>()//方法二
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_factory)
        val person3 = get<Person>()//方法三
    }
}

```

# 三.带有参数的构造函数使用
### 1.单个构造参数
修改Person类,使其构造函数带有参数.
```
class Person(var name:String) {
 
}
```
添加依赖时需要将构造参数传入
```
class MyApp : Application() {
      ...
        val appModule = module {//里面添加各种注入对象
        factory  {
            Person("张三")//构造对象的时候将构造参数传入
        }
    }
}
```

### 2. 构造函数依赖于其他类
Person类构造时依赖于PersonInfo类
```
class Person(var personInfo:PersonInfo) {
 
}
```
```
class PersonInfo(var name:String) {
 
}
```
构造时可以通过get()来获取之前创建过的参数对象.
>get()会自动去寻找之前创建过的依赖,找到合适的依赖

```
class MyApp : Application() {
      ...
        val appModule = module {//里面添加各种注入对象
        factory  {
            PersonInfo("张三")//构造对象的时候将构造参数传入
        }
        factory  {
            PersonInfo(get())//get()会自动去寻找之前创建过的依赖PersonInfo
        }
    }
}
```

### 3. 多个构造函数
通过限定符标记构造方法--qualifier
如果被依赖的类有多个构造函数,如何知道用哪个构造函数进行初始化.这里就需要用到限定符qualifier,如果不用就会造成依赖迷失引发报错
创建有多个构造函数的类:
```
class MultStructureHotPot constructor(var name: String) {

    //第二个构造方法
    constructor(name: String, vegetables: Vegetables) : this(name)

    //第三个构造方法
    constructor(name: String, vegetables: Vegetables, meat: Meat) : this(name)

    fun cook() {
        LogTest.d("开始制作${name}火锅")
    }

}

```
注入module
```
class MyApp : Application() {
      ...
  val hotPotModule = module {//里面添加各种注入对象
      factory {
          Vegetables("各种蔬菜")
      }
      factory {
          Meat("各种肉类")
      }
  
      factory {
          MultStructureHotPot("空火锅")
      }
      factory(named("vegetables")) {
          MultStructureHotPot("蔬菜火锅", get())
      }
      factory(named("multi")) {
          MultStructureHotPot("荤素搭配火锅", get(), get())
      }
  
  }    
}
```
```
class FactoryActivity : AppCompatActivity() {
       val mHotPot: MultStructureHotPot by inject()
       val mVegetablesHotPot: MultStructureHotPot by inject(named("vegetables"))
       val mMutilHotPot: MultStructureHotPot by inject(named("multi"))
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_factory)
       
        mHotPot.cook()
        mVegetablesHotPot.cook()
        mMutilHotPot.cook()
    }
}
```

### 4. 构造函数从外部传入

```
val hotPotModule = module {//里面添加各种注入对象
    factory {
        Vegetables("各种蔬菜")
    }
    factory {
        Meat("各种肉类")
    }

    factory {
        MultStructureHotPot("空火锅")
    }
    factory(named("vegetables")) {
        MultStructureHotPot("蔬菜火锅", get())
    }
    factory(named("multi")) {
        MultStructureHotPot("荤素搭配火锅", get(), get())
    }
    factory(named("external")) { (meat: Meat) ->
        MultStructureHotPot("荤素搭配火锅", get(), meat)
    }
}
```
通过parametersOf()传递参数
```
class KoinSingleActivity : AppCompatActivity() {
    val mMutilHotPot2: MultStructureHotPot by inject(named("external")) {
        parametersOf(Meat("驴肉"))
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.test_activity_koin_single)
        mMutilHotPot2.cook()
    }
}
```

# 四.scope范围限定
注入对象都是有作用范围的，如果没有指定scope的话就是koin的一个rootScope，如果指定scope，注入时就会从该scope中去查找声明的对象

Scope 用于控制对象在 Koin 内的生命周期。事实上，前面所讲的 single 与 factory 都是 scope。

single 创建的对象在整个容器的生命周期内都是存在的，因此任意地方注入都是同一实例。
factory 每次都创建新的对象，因此它不被保存，也不能共享实例。


,scope下的对象可以跟一个视图绑定起来,并且该被绑定的对象是单例的模式,其他界面通过scopeId可以获取这个对象.当该视图被销毁的时候,被绑定的对象也会被销毁.其他界面也就获取不到这个scope对象了.

>使用scope可以使对象可以跟一个界面绑定起来,并且该被绑定的对象是单例的模式,其他界面通过scopeId可以获取这个被绑定对象.当被绑定的界面被销毁的时候,被绑定的对象也会被销毁.其他界面通过scopeId就不能获取这个被绑定对象了.
>之前我们学习的single只能创建一个单例对象，factroy每次都创建新的对象。Scope的出现能把不同作用域内的对象作为一个对象，比如说我们想在Activity1和Activity2中的person是一个单例，Activity3和activity4中的Person是一个单例。我们就可以使用Scope来实现

定义 Scope 比较简单：

```
val myModule = module{
    scope(named("MY_SCOPE")){
        scoped {
            Stove()
        }
    }
}
```

但是使用起来就比较麻烦了，我们需要创建或关闭 scope，毕竟 Kolin 怎么会知道你究竟想实现怎样的生命周期呢？
```

// 如果存在则直接获取，否则创建 scope
val scope = getKoin().getOrCreateScope("myScope", named("MY_SCOPE"))
val stove1: Stove = scope.get()
val stove2: Stove = scope.get()
scope.close()
```
这里首先得到了一个 scope 实例，然后进行注入，最后关闭 scope。那么在同一个 scope 中注入的实例是相同的。例如 stove1 与 stove2 实际上是同一个实例。当 scope 被关闭时其缓存会被清空，自然下一次重新创建后会注入新的对象。

注意区分一点，定义 Scope 时使用的叫做 Qualifier，通过 named 可以用字符串包装。在创建 scope 时需要通过 Qualifier 关联到定义，并同时给一个字符串类型的 id，id 仅在运行时使用。可以类比成 Android 的布局文件的 View id 与实际变量名的关系。我们需要通过 View id 来获取实例并赋值给变量保存，变量名与 View id 没有必然的关系。

在 Android 中我们经常需要以 Activity 为单位创建 scope，为了简化使用，Koin 提供了 Android 扩展库。在 Activity 与 Fragment 中，可以直接使用 currentScope 变量来表示当前 scope，他会被自动创建，并绑定到 Android 组件的生命周期。

```
class LocalWatchFaceAty : AppCompatActivity() {
    private val stove: Stove by currentScope.inject()
}
```
除了之前使用的 get，还可以像这样使用 inject 实现懒加载。

定义 scope 也变得简单。之前我们使用字符串作为限定符定义了 scope，现在直接使用类作为限定符：

```
val myModule = module{
    scope(named<LocalWatchFaceAty>()){
        scoped {
            Stove()
        }
    }
}
```



# 五.普通类中使用注解，需要实现KoinComponent接口

创建一个类,该类实现了KoinComponent,在该类中,我们就可以通过by inject和get来过去被注入过的对象了.
```
//类实现了KoinComponent,在该类中,我们就可以通过by inject和get来过去被注入过的对象了.
class InjectPerson : KoinComponent {
    val person = get<KoinPerson>()//非懒加载模式
    val person2=inject<KoinPerson> ()//懒加载模式
    fun speak(){
        person.speak()
    }
}
```
可以直接使用注解
```
class KoinSingleActivity : AppCompatActivity() {
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.test_activity_koin_single)
         //在第三方类中使用注解
         InjectPerson().speak()
    }
}
```

# 六.ViewModel
ViewModel 可以说是 Android 架构组件发布后最流行的部分了，幸运的是 Kolin 对其做了非常方便的适配。对于 ViewModel 类直接使用 viewModel 来定义 Service：
```
class KoinViewModel : ViewModel() {
    override fun onCleared() {
        super.onCleared()
        LogTest.d("====>ViewModel=onCleared")
    }
}
```

```
val localModule = module {
    viewModel {
        KoinViewModel()
    }
}
```
在 Activity 或 Fragment 中直接使用 by viewModel() 或 getViewModel() 来注入。

```
class LocalWatchFaceAty : AppCompatActivity() {
    private val vm: KoinViewModel by viewModel()
}
```
这样一来得到的 ViewModel 可以自动与 UI 生命周期关联。而如果使用传统的 get 只能得到实例但没有任何关联，失去了 ViewModel 最重要的作用。退出该界面,发现viewModel中的clear回调被调用了



[使用Koin来完成Kotlin的依赖注入](https://juejin.cn/post/6844903929117933576)
[](https://github.com/harmittaa/KoinExample/blob/master/app/src/main/java/com/github/harmittaa/koinexample/fragment/WeatherFragment.kt)
[](https://github.com/winlee28/Jetpack-WanAndroid/blob/master/ft_home/src/main/java/com/win/ft_home/api/RequestCenter.kt)
[Koin--适用于Kotlin的超好用依赖注入框架](https://blog.csdn.net/Shaojihan/article/details/104349741)
[Android Koin2 基本使用那件事](https://blog.csdn.net/weixin_45365889/article/details/100566332)
[深入理解Koin框架之koin-core](https://www.jianshu.com/p/8d78761f3c6f?utm_campaign=shakespeare)