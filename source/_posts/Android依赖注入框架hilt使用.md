---
title: Android依赖注入框架hilt使用
---

# 一.什么是Hilt
Hilt 是Google 最新的依赖注入框架，其基于Dagger研发。Hilt可以说是专门为Android 打造，提供了一种将Dagger依赖项注入到Android应用程序的标准方法，而且创建了一些标准的组件和作用域，这些组件会自动集成到Android应用程序的各个生命周期中，以简化开发者的上手难度。
# 二. 引入Hilt
### 1.AndroidStudio版本
需要AndroidStudio4.0版本及以上以上
### 2.项目根目录build.gradle添加依赖
```
buildscript {
    ...
    dependencies {
        ...
        classpath 'com.google.dagger:hilt-android-gradle-plugin:2.28-alpha'
    }
}
```
### 3.在module下的build.gradle添加以下依赖项：
```
...
apply plugin: 'kotlin-kapt'
apply plugin: 'dagger.hilt.android.plugin'

android {
  ...
  //Hilt 使用 Java 8 功能。如需在项目中启用 Java 8  
  compileOptions {
    sourceCompatibility JavaVersion.VERSION_1_8
    targetCompatibility JavaVersion.VERSION_1_8
  }
}

dependencies {
    implementation "com.google.dagger:hilt-android:2.28-alpha"
    kapt "com.google.dagger:hilt-android-compiler:2.28-alpha"
}
```
# 三.初步使用Hilt
### 1.初始化Hilt
所有使用 Hilt 的应用都必须包含一个带有 @HiltAndroidApp 注释的 Application 类。在Application的上面必须使用这个注解才可以开启hilt依赖注入。
```
@HiltAndroidApp
class ExampleApplication : Application() { ... }
```

### 2.Hilt注入对象
Inject注解和Dagger2中一样有两个作用:
- 注解在构造函数中， 表示该类可以进行注入。
- 注解在成员变量上， 表示该成员变量使用进行注入。

提供依赖项:
```
//@Inject注解在类上，去标记Hilt如何去提供实例。
class AnalyticsAdapter @Inject constructor() { ... }
```

获取依赖项:
```
@AndroidEntryPoint
class ExampleActivity : AppCompatActivity() {
  // 标记Hilt要给该类提供实例  
  @Inject 
  lateinit var analytics: AnalyticsAdapter

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_hilt_test)
        Log.d("TAG",analytics.hashCode().toString())
    }

  ...
}
```

运行项目可以看到，并没有手动实例化AnalyticsAdapter对象，而是通过依赖注入框架进行的实例化。

>注:由 Hilt 注入的字段不能用私有修饰符进行修饰。使用 Hilt 注入私有字段会导致编译错误。

### 2.Hitl默认组件种类
上文说到在 Application 类中设置了 Hilt 件后，Hilt 可以为带有 @AndroidEntryPoint 的组件注入其依赖项。
```
@AndroidEntryPoint
class ExampleActivity : AppCompatActivity() { ... }
```
如果对Dagger2有所了解的朋友，肯定会对Compenent不陌生。Compenent的作用就是将依赖提供项注入到需要使用的地方。前文说过Hitl实际是对Dagger2的封装。在上文例子中并没有用Compenent进行注入就可以进行依赖项实例化。其中的原因就是Hitl默认实现了部分组件的Compenent，可以直接让使用，节省代码。也就说Hilt大幅简化了Dagger2的用法，使得不用通过@Component注解去编写桥接层的逻辑，但是也因此限定了注入功能只能从几个Android固定的入口点开始。 只需要在类上增加 @AndroidEntryPoint 即可支持以下类的注入
|Hilt Compenent|	注入器面向的对象|
|-|-|
|ApplicationComponent|	Application |
|ActivityRetainedComponent|	ViewModel（请参阅JetPack-ViewModel扩展） |
|ActivityComponent |	Activity |
|FragmentComponent |	Fragment |
|ViewComponent |	View |
|ViewWithFragmentComponent |	View 与 @WithFragmentBindings |
|ServiceComponent |	Service |

>注:如果Fragment使用，那么包含Fragment的Activity必须也要用该注解，如果View使用， 对应的Fragment和Activity也必须使用。

### 3.Hitl组件(Compenent)的生命周期
在之前Dagger-Android中，必须创建诸如ActivityScope，FragmentScope之类的范围注释，以管理对象的生命周期， 而Hitl只要使用@InstallIn的注解，就可以委托Hilt帮管理生命周期，Hilt 会按照相应 Android 类的生命周期自动创建和销毁生成的组件类的实例。
|生成的组件 Component        |		创建时机 |	销毁时机 |
|-|-|-|-|
|ApplicationComponent	   | Application#onCreate()	|Application#onDestroy()|
|ActivityRetainedComponent | Activity#onCreate()	|Activity#onDestroy()   |
|ActivityComponent	       | Activity#onCreate()    |Activity#onDestroy()   |
|FragmentComponent	       | Fragment#onAttach()    |Fragment#onDestroy()   |
|ViewComponent	           | View#super()           |视图销毁时              |
|ViewWithFragmentComponent | View#super()	        |视图销毁时              |
|ServiceComponent	       | Service#onCreate()  	|Service#onDestroy()    |

>注:ActivityRetainedComponent是用于ViewModle的，了解ViewModle的应该知道 ViewModel在页面配置更改后(例如屏幕旋转)仍然存在，因此它在第一次调用 Activity#onCreate() 时创建，在最后一次调用 Activity#onDestroy() 时销毁。

### 5.Hitl组件作用域
默认情况下，Hilt 中的所有绑定都未限定作用域，这意味着，每当应用注入时，Hilt 都会创建所需类型的一个新实例。
```
@AndroidEntryPoint
class ExampleActivity : AppCompatActivity() {

  @Inject lateinit var analytics: AnalyticsAdapter
  @Inject lateinit var analytics2: AnalyticsAdapter

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_hilt_test)
        Log.d("TAG",analytics.hashCode().toString())
        Log.d("TAG",analytics2.hashCode().toString())
    }

  ...
}
```
运行代码会发现analytics和analytics2是两个不同的对象，但是如果想要analytics和analytics2在ExampleActivity指向同一个对象。那么就要对组件的作用域进行限定， Hilt 也允许将绑定的作用域限定为特定组件。Hilt 只为绑定作用域限定到的组件的每个实例创建一次限定作用域的绑定，对该绑定的所有请求共享同一实例。

|Android 类	|生成的组件	|作用域|
|-|-|-|
|Application|ApplicationComponent	|@Singleton|
|View Model	|ActivityRetainedComponent	|@ActivityRetainedScope|
|Activity	|ActivityComponent	        |@ActivityScoped|
|Fragment	|FragmentComponent      	|@FragmentScoped|
|View	    |ViewComponent	            |@ViewScoped|
|带有 @WithFragmentBindings  注释的 View|	ViewWithFragmentComponent	|@ViewScoped|
|Service	|ServiceComponent	|@ServiceScoped|

例如上面例子中将组件作用域限定为@ActivityScoped:
```
@ActivityScoped
class AnalyticsAdapter @Inject constructor() { ... }
```

```
@AndroidEntryPoint
class ExampleActivity : AppCompatActivity() {

  @Inject lateinit var analytics: AnalyticsAdapter
  @Inject lateinit var analytics2: AnalyticsAdapter

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_hilt_test)
        Log.d("TAG",analytics.hashCode().toString())
        Log.d("TAG",analytics2.hashCode().toString())
    }

  ...
}
```
运行代码会发现analytics和analytics2是两个相同的对象，它们会在该Activity中保持单例。相应的，如果要使用全局的单例对象，将 AnalyticsService 的作用域限定为 ApplicationComponent即可。 Dagger 允许绑定作用域到特定组件，如上表所示，在指定组件范围内，实例都只会创建一次，并且对该绑定的所有请求都将共享同一实例。
# 四.Hilt注入无法修改构造函数的对象
有时，类不能通过构造函数注入，比如接口， 第三方库， Builder模式构造的对象等。在hilt中可以通过module模块向 Hilt 提供绑定信息， Hilt 模块是一个带有 @Module 注释的类。与 Dagger 模块一样，它会告知 Hilt 如何提供某些类型的实例。与 Dagger 模块不同的是， 必须使用 @InstallIn 为 Hilt 模块添加注解，以告知 Hilt 每个module模块将用在或安装在哪个 Android 类中。在模块中需要了解 如下三个注解:
- @Module:   标记这是一个module.可以通过module模块向 Hilt 提供绑定信息。
- @Provides: 标记方法， 提供依赖返回值。
- @Binds:    标记抽象方法或者接口， 返回接口类型。

>在 Hilt 模块中提供的依赖项可以在生成的所有与 Hilt 模块安装到的 Android 类关联的组件中使用。

### 1.@Module和@Provides为第三方类提供注入
如果某个类来自外部库，如 Retrofit、OkHttpClient 或 Room 数据库等类，或者必须使用构建器模式创建实例，也无法通过构造函数@Inject注入。则可以为Hilt创建一个模块，在 Hilt 模块内创建一个函数，并使用 @Provides 为该函数添加注解提供对象。
1. 假如无法在AnalyticsAdapter的构造函数上面通过@Inject注入:
```
class AnalyticsAdapter  constructor()
```
2. 创建module提供依赖:
```
@Module
@InstallIn(ActivityComponent::class)
class AnalyticsAdapterModule {
    @Provides
    fun provideAnalyticsAnalyticsAdapter(): AnalyticsAdapter {
        return AnalyticsAdapter()
    }
}
```
3. 进行依赖注入，并使用
```
@AndroidEntryPoint
class ExampleActivity : AppCompatActivity() {

  @Inject 
  lateinit var analytics: AnalyticsAdapter

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_hilt_test)
        Log.d("TAG",analytics.hashCode().toString())
    }

  ...
}
```
带有 @Provides注解的函数会向 Hilt 提供以下信息：
- 函数返回类型会告知 Hilt 函数提供哪个类型的实例。
- 函数参数会告知 Hilt 相应类型的依赖项。
- 函数主体会告知 Hilt 如何提供相应类型的实例。每当需要提供该类型的实例时，Hilt 都会执行函数主体。

### 1.@Module和@Binds为接口或抽象类提供注入
@Binds 注释会告知 Hilt 在需要提供接口的实例时要使用哪种实现。带有@Binds注解的函数会向 Hilt 提供以下信息：
- 函数返回类型会告知 Hilt 函数提供哪个接口的实例。
- 函数参数会告知 Hilt 要提供哪种实现。

例如上面例子中AnalyticsService 类是一个接口，则您无法通过构造函数注入它，而应向 Hilt 提供绑定信息，方法是在 Hilt 模块内创建一个带有 @Binds 注释的抽象函数。
1. 接口类:
```
interface IAnalyticsService {
    fun analyticsMethods()
}

```
2. 接口的实现类:
```
class AnalyticsServiceImpl @Inject constructor(): IAnalyticsService {
    //实现接口方法
    override fun analyticsMethods() {

    }
}
```
3. module提供依赖的类:
```
@Module
@InstallIn(ActivityComponent::class)
abstract class AnalyticsModule {

  @Binds
  abstract fun bindAnalyticsService(
    analyticsServiceImpl: AnalyticsServiceImpl
  ): AnalyticsService
}
```

4. 在Activity依赖注入对象
```
@AndroidEntryPoint
class HiltModuleActivity : AppCompatActivity() {
    @Inject
    lateinit var iAnalyticsService: IAnalyticsService
    private val textView: TextView by lazy { findViewById<TextView>(R.id.textView_info) }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.test_activity_hilt_module)
        textView.text = iAnalyticsService.hashCode().toString()
    }
}
```
# 五.Hilt限定构造方法
如果一个类有多个构造方法，那么依赖注入的时候要用到哪个初始化函数进行初始化呢?这时就要用到@Qualifiers限定注解了,Dagger2中@Named也可以实现该功能。

例如:有一个Car类在构造的时候传入name生成对应品牌的车辆,要造BYD和BMW的车,在注入Car的时候就可以用@Qualifiers注解进行区分:
1. 创建car类:
```
class Car constructor(var brand: String) {
    fun getCarBrand(): String = brand
}
```
2. 创建BYD和BMW限定注解:
```
@Qualifier
@Retention(AnnotationRetention.BINARY)
annotation class BMWCarQualifier
```

```
@Qualifier
@Retention(AnnotationRetention.BINARY)
annotation class BYDCarQualifier
```
3. 创建module
```
@Module
@InstallIn(ActivityComponent::class)
class CarModule {
    @BMWCarQualifier
    @Provides
    fun provideBYDCar(): Car {
        return Car("比亚迪")
    }

    @BYDCarQualifier
    @Provides
    fun provideBMWCar(): Car {
        return Car("宝马")
    }
}
```
4. 注入注解进行使用:
```
 @AndroidEntryPoint
 class HiltModuleActivity : AppCompatActivity() {

     @BMWCarQualifier
     @Inject
     lateinit var bmWcar: Car
 
     @BYDCarQualifier
     @Inject
     lateinit var bydcar: Car
 
     private val textView: TextView by lazy { findViewById<TextView>(R.id.textView_info) }
     override fun onCreate(savedInstanceState: Bundle?) {
         super.onCreate(savedInstanceState)
         setContentView(R.layout.test_activity_hilt_module)
         val sb = StringBuilder()
         sb.append("car:" + bydcar.getCarBrand() + " hashCode:" + bydcar.hashCode().toString() + "\n")
         sb.append("car:" + bmWcar.getCarBrand() + " hashCode:" + bmWcar.hashCode().toString() + "\n")
         textView.text = sb.toString()
     }
 }
```

运行代码发现通过@Qualifiers注解成功的对依赖注入对象进行了分类。

# 六.Hilt结合JetPack其他组件使用
作为Google推荐的依赖注入组件，目前Hilt 可以与ViewModel配合使用:

1. 导入依赖
```
    implementation 'androidx.hilt:hilt-lifecycle-viewmodel:1.0.0-alpha02'
    kapt 'androidx.hilt:hilt-compiler:1.0.0-alpha02'
    //viewModel的数据恢复，可以不导入，这里只是为了演示
    implementation "androidx.lifecycle:lifecycle-viewmodel-savedstate:2.2.0"
	//便于 使用ViewModel-ktx扩展
    implementation 'androidx.activity:activity:1.1.0'
    implementation 'androidx.fragment:fragment-ktx:1.2.5'
```
2. ViewModel
```
public class TestViewModel extends ViewModel {
    @ViewModelInject
    public TestViewModel() {

    }
    public void test(){
        Log.e("petterp","我是测试方法");
    }
}
```
2. ViewModel创建按构造方法
```
class TestViewModel @ViewModelInject constructor(
    private val repository: TestRepository,
    @Assisted val savedState: SavedStateHandle
) : ViewModel() {
    fun test() {
        repository.test()
    }
}
```
3. TestRepository
```
@ActivityScoped
class TestRepository @Inject constructor() {
    fun test() {
        Log.e("petterp", "一个测试方法")
    }
}
```

2. 创建一个MainActivty
```
@AndroidEntryPoint
class MainActivity : AppCompatActivity() {

    private val viewModel by viewModels<TestViewModel>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        viewModel.test()
    }
```

[在 Android 应用中使用 Hilt](https://developer.android.google.cn/codelabs/android-hilt?hl=zh_cn#0)

[Hilt-依赖注入框架上手指南](https://blog.csdn.net/petterp/article/details/106771203)

[使用 Hilt 实现依赖项注入](https://developer.android.google.cn/training/dependency-injection/hilt-android?hl=zh_cn)

[Android Jetpack架构组件(十二)之Hilt](https://segmentfault.com/a/1190000039039120?utm_source=tag-newest)

[Android Hilt](https://blog.csdn.net/weixin_43662090/article/details/107839517)

[Jetpack新成员，一篇文章带你玩转Hilt和依赖注入](https://blog.csdn.net/guolin_blog/article/details/109787732)

[Dagger Hilt 初探](https://juejin.cn/post/6847902220223152136#heading-9)

[Jetpack Hilt](https://juejin.cn/post/6912014711932321806#heading-4)

[Hilt 的使用以及遇到的问题](https://juejin.cn/post/6953883719954382878#heading-20)

[快速上手Google 提供的依赖注入框架 「Hilt」](https://juejin.cn/post/6953913131026350110#heading-6)

[Android Hilt使用教程（包含实例)](https://www.jianshu.com/p/f32beb3614e5)

[Android Jetpack系列---Hilt](https://blog.csdn.net/qq_45485851/article/details/110128769)

[Android Hilt](https://blog.csdn.net/weixin_43662090/article/details/107839517)

[Dagger Hilt 初探](https://blog.csdn.net/u011215710/article/details/107230043)

[依赖注入库Hilt的使用和理解，一篇就够了](https://www.jianshu.com/p/a301a8d93583)

[Android Hilt](https://blog.csdn.net/weixin_43662090/article/details/107839517)

[上手指南 | Jetpack Hilt 依赖注入框架](https://juejin.cn/post/6845166891325997069#heading-5)