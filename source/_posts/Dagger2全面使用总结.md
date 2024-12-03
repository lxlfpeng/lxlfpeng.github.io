---
title: Dagger2全面使用总结
date: 2017-02-17
categories: 
  - Android开发
---

# 一 依赖注入
依赖注入（DI）是控制反转（Inversion of Control,IoC）的一种重要方式，IoC是将依赖对象的创建和绑定通过被依赖对象类的外部来实现。依赖注入提供一种机制，将需要依赖对象的引用传递给被依赖对象。
它是面向对象的一种设计模式，其目的是为了降低耦合。举个栗子：
```
public class Person {
    Decorate decorate;
    public Person(){
        decorate = new Decorate(jacket,shoe);
    }
```
这里的Person对象的初始化为实例化Decorate，如果Decorate类实例化参数增加，则必须对Person对象初始化进行修改。如果还有其他类的也是按照这种方式创建Decorate类，那么就需要修改多处，这违背了单一职责原则和开闭原则。
因此需要引入依赖注入来解决这个问题。依赖注入，就是将依赖注入到宿主类（或者叫目标类）中，从而解决上面所述的问题。

# 二 依赖注入实现的三种方式
下面将会介绍三种简单的依赖注入方式，一般依赖注入的框架的基本原理基本一样，避免在被依赖对象中直接实例化依赖对象，而是通过其他方式引入。根据依赖注入的定义，下面例子中依赖对象为Decorate，被依赖对象为Person。

### 1. 构造注入
通过构造函数直接注入
```
public class Person {
    private Decorate decorate;
    public Person(Decorate decorate){
        this.decorate = decorate;
    }
}
```

### 2. 属性注入
通过属性来传递依赖即通过set方法
```
public class Person {
    private Decorate decorate;
    public void setPerson(Decorate decorate){
        this.decorate = decorate;
    }
}
```


### 3. 通过Java注解
```
public class Person {
    //此时并不会完成注入，还需要依赖注入框架的支持，如RoboGuice,Dagger2
    @inject Decorate decorate;

    

```
在Dagger2中用的就是最后一种注入方式，通过注解的方式，将依赖注入到宿主类中。


# 三 Dagger2注解使用
Dagger2是Dagger的升级版，是一个依赖注入框架，现在由Google接手维护。在github上Dagger2是这样定义的，Dagger2是一个Android和java快速依赖注入框架。
Dragger2是在编译时注解的方式实现依赖注入，是Dagger的升级版，取消了反射的使用。通过@Component的接口替代ObjectGraph/Injector，从而使代码更精简。
早期的一些注入框架是通过反射机制在运行时完成注入的工作，而反射对性能影响很大，所以现在基本上是采用编译时通过工具生成相应的类文件实现的。

### 1.Dagger2的依赖引入
完成Dagger2的依赖方式有两种，分别为annotationProcessor和android-apt。android-apt是开发者自己开发的apt框架，随着谷歌Android Gradle2.2插件的发布，插件提供了annotationProcessor来替换android-apt，
自此基本上都使用annotationProcessor。
项目中通过annotationProcessor的方式进行依赖，在app的build.gradle添加：
```
implementation 'com.google.dagger:dagger:2.10'
annotationProcessor "com.google.dagger:dagger-compiler:2.10"
implementation "org.glassfish:javax.annotation:10.0-b28"
```

### 2.Inject方式注入（Inject+Component）
1. 定义一个Person类，在构造函数前加上@Inject，表明支持依赖注入。
```
public class Person {
    @Inject
    public Person(){
    }
    public String getName(){
        return "xiaoming";
    }
}
```
2. 定义接口MainActivityComponent，在接口前添加@Component，定义相应的抽象方法，方法的参数为需要注入对象的真实所在的类，方法名一般为Inject。
Component可以理解为Person（依赖对象）和MainActivity（被依赖对象）之间的桥梁。
```
@Component
public interface MainActivityComponent {
    void inject(MainActivity activity);
}
```
3. 对项目进行Rebuild，Dagger2框架会根据MainActivityComponent自动生成DaggerMainActivityComponent(命名规则Dagger+Component名称)。
在MainActivity声明Person对象，并用@Inject的注解，然后通过DaggerMainActivityComponent注入Person对象。
```
public class DaggerSimpleActivity extends AppCompatActivity {

    private static final String TAG = "MainActivity";
    @Inject
    Person person;
    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        DaggerMainActivityComponent.builder().build().inject(this);
        Log.d(TAG,person.getName());
    }
}
```
执行结果:
```
MainActivity: xiaoming
```
可以看出MainActivity成功注入了Person类，下面分析是如何注入Person类的：
打开DaggerMainActivityComponent，可以看出其对应的路径\app\build\generated\source\apt\debug，在其目录下同时也有其他两个类Person_Factory，MainActivity_MembersInjector。
DaggerMainActivityComponent.java:
```
public final class DaggerMainActivityComponent implements MainActivityComponent {
    private DaggerMainActivityComponent() {

    }

    public static Builder builder() {
        return new Builder();
    }

    //1.调用create实际上是调用Builder().build()方法
    public static MainActivityComponent create() {
        return new Builder().build();
    }

    //3.重写MainActivityComponent的inject方法
    @Override
    public void inject(MainActivity activity) {
        injectMainActivity(activity);
    }

    //4. 调用  MainActivity_MembersInjector的injectMPerson方法将MainActivity的引用和new 创建的Person对象传入
    private MainActivity injectMainActivity(MainActivity instance) {
        MainActivity_MembersInjector.injectMPerson(instance, new Person());
        return instance;
    }

    public static final class Builder {
        private Builder() {
        }

        //2.build()会通过new关键字创建DaggerMainActivityComponent对象
        public MainActivityComponent build() {
            return new DaggerMainActivityComponent();
        }
    }
}
```
在MainActivity中DaggerMainActivityComponent.builder().build()将会通过构建者实例化DaggerMainActivityComponent，
DaggerMainActivityComponent实现了MainActivityComponent接口.重写MainActivityComponent的inject方法.因此我们再MainActivity中调用inject方法时会走
4中的步骤MainActivity_MembersInjector的injectMPerson方法将MainActivity的引用和new 创建的Person对象传入.

MainActivity_MembersInjector.java
```

public final class MainActivity_MembersInjector implements MembersInjector<MainActivity> {
  private final Provider<Person> mPersonProvider;

  public MainActivity_MembersInjector(Provider<Person> mPersonProvider) {
    this.mPersonProvider = mPersonProvider;
  }

  public static MembersInjector<MainActivity> create(Provider<Person> mPersonProvider) {
    return new MainActivity_MembersInjector(mPersonProvider);}

  @Override
  public void injectMembers(MainActivity instance) {
    injectMPerson(instance, mPersonProvider.get());
  }

  //1.在DaggerMainActivityComponent的injectMainActivity方法中将MainActivity对象和Person对象传入
  @InjectedFieldSignature("com.base.example.dagger.simple.MainActivity.mPerson")
  public static void injectMPerson(MainActivity instance, Person mPerson) {
    //2.这里的instance就是MainActivity,这里为MainActivity的mPerson对象赋值了刚传入的Person对象
    instance.mPerson = mPerson;
  }
}
```
MainActivity_MembersInjector类是实例化Person类的关键，也是注入具体的实现方式。aggerMainActivityComponent的injectMainActivity方法中将MainActivity对象和Person对象传入,
然后对MainActivity的mPerson对象赋值了刚传入的Person对象.因此在MainActivity就完成了Person的依赖注入.MainActivity持有了Person对象.

### 3.带Module的Inject方式（Inject+Component+Module）
在上面的Person中是自己定义的类，如果是某个库中的类，我们不能够改它的源码因此是不能够去该类中添加@Inject注解了，那么注入这种类该如何注入呢，这个时候就需要Module。
Module可以理解为对象的实例化，向Component的提供依赖对象。下面以Person类为对象说明：
1 .创建一个MainModule，并用@Module注解，在类中提供Person对象的方法并用@Provider注解（取消之前Person类中的@Inject注解）
```
@Module
public class MainModule {
    @Provides
    public Person providePerson(){
        return new Person();
    }
}
```
2. 修改MainActivityComponent，为其添加Module应用，来说明其可能需要用到MainModule中提供的对象。
```
@Component(modules = MainModule.class)
public interface MainActivityComponent {
    void inject(MainActivity activity);
}
```
3. MainActivity保持不变

执行结果:
```
MainActivity: xiaoming
```

可以看出和上面的例子结果一样，主要不同的是增加了MainModule。我们接下来再来分析一下生成的源码.

DaggerMainActivityComponent.java:
```
public final class DaggerMainActivityComponent implements MainActivityComponent {
  private final MainModule mainModule;

  //3. 对DaggerMainActivityComponent中的mainModule进行赋值
  private DaggerMainActivityComponent(MainModule mainModuleParam) {
    this.mainModule = mainModuleParam;
  }

  public static Builder builder() {
    return new Builder();
  }

  public static MainActivityComponent create() {
    return new Builder().build();
  }

  //4.MainActivity中调用DaggerMainActivityComponent的inject方法将MainActivity的引用传入
  @Override
  public void inject(MainActivity activity) {
    injectMainActivity(activity);}

    //调用了MainActivity_MembersInjector的injectMPerson方法传入MainActivity的引用
  private MainActivity injectMainActivity(MainActivity instance) {
    MainActivity_MembersInjector.injectMPerson(instance, MainModule_ProvidePersonFactory.providePerson(mainModule));
    return instance;
  }

  public static final class Builder {
    private MainModule mainModule;

    private Builder() {
    }

    public Builder mainModule(MainModule mainModule) {
      this.mainModule = Preconditions.checkNotNull(mainModule);
      return this;
    }
    //1.这里通过new关键字创建了MainModule对象.
    public MainActivityComponent build() {
      if (mainModule == null) {
        this.mainModule = new MainModule();
      }
      //2.通过new关键字创建DaggerMainActivityComponent对象将mainModule传入
      return new DaggerMainActivityComponent(mainModule);
    }
  }
}

```
我们看到调用MainActivity_MembersInjector.injectMPerson的时候的Person对象是通过MainModule_ProvidePersonFactory获取到的.
MainModule_ProvidePersonFactory.java:
```
public final class MainModule_ProvidePersonFactory implements Factory<Person> {
  private final MainModule module;

  public MainModule_ProvidePersonFactory(MainModule module) {
    this.module = module;
  }

  @Override
  public Person get() {
    return providePerson(module);
  }

  public static MainModule_ProvidePersonFactory create(MainModule module) {
    return new MainModule_ProvidePersonFactory(module);
  }

  //1.调用MainModule的providePerson()方法返回Person对象
  public static Person providePerson(MainModule instance) {
    return Preconditions.checkNotNull(instance.providePerson(), "Cannot return null from a non-@Nullable @Provides method");
  }
}

```
### 5.Module带参数
一般情况下大多数的类都需要传入参数的，下面看下带参数的类的实例化是如何的。
1. 修改Person类
```
public class Person {

    private int age;

    public Person(int age) {
        this.age = age;
    }

    public String getName() {
        return "mike";
    }

    public int getAge() {
        return age;
    }
}
```
2. 将Person类的age参数传入
```
@Module
public class MainModule {
    int age;
    public MainModule(int age){
        this.age = age;
    }
    @Provides
    public Person providePerson(){
        return new Person(age);
    }
}
```
3 .在MainActivity中设置MainModule对象的参数
```
DaggerMainActivityComponent.builder().mainModule(new MainModule(19)).build().inject(this);
```
执行结果:
```
MainActivity: 19

```
需要注意的是在无参数的时候，DaggerMainActivityComponent会提供create方法，但是有参数时，只有build方法，因为需要传入MainModule对象
。一般建议通过provide方法提供参数，主要是解耦和增加代码的可读性。
```
@Module
public class MainModule {
    int age;
    public MainModule(int age){
        this.age = age;
    }

    @Provides
    public int provideAge(){
        return age;
    }

    @Provides
    public Person providePerson(){
        return new Person(age);
    }
    @Provides
    public Decorate providerDecorate(){
        return new Decorate();
    }
}
```
Module中不能出现参数和返回参数一致的情况，否则会导致死循环。如：
```
@Provides
public int provideAge(int age){
    return age;
}

```

# 四.@Inject 和 @Provides 的优先级
Dagger2 依赖查找的顺序是先查找 Module 内所有的 @Provides 提供的依赖，如果查找不到再去查找 @Inject 提供的依赖。
- 步骤1：查找Module中是否存在创建该类的方法。
- 步骤2：若存在创建类方法，查看该方法是否存在参数
- 步骤2.1：若存在参数，则按从步骤1开始依次初始化每个参数
- 步骤2.2：若不存在参数，则直接初始化该类实例，一次依赖注入到此结束
- 步骤3：若不存在创建类方法，则查找Inject注解的构造函数，看构造函数是否存在参数
- 步骤3.1：若存在参数，则从步骤1开始依次初始化每个参数
- 步骤3.2：若不存在参数，则直接初始化该类实例，一次依赖注入到此结束

# 五.Scope作用域
### 1.Scope作用域
scope 就是作用域的意思，在不使用@Scope的情况下，每次注入的对象都会是一个新的不同的对象，而@Scope能限制被注入的对象.
在MainActivity中注入两个Person对象
```
@Inject
Person person1;
@Inject
Person person2;
@Override
protected void onCreate(@Nullable Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_main);
    DaggerMainActivityComponent.builder().mainModule(new MainModule(19)).build().inject(this);
    Log.d(TAG,"person1 hash:"+person1.toString());
    Log.d(TAG,"person2 hash:"+person2.toString());

}
```
运行程序可以看到可以看到person1和person2的hash值并不相同,因此说明它们是两个不同的对象.在 dagger2 中，@scope 的一个默认实现就是 @Singleton.
### 2.Singleton注解
如果标注了Scope注解，那么注入器可能就会保持这个实例，下次注入需要这个依赖时就可以重用了.@scope 的一个默认实现就是 @Singleton.
@Singleton，这是一个标注了@Scope的注解
```
/**
 * Identifies a type that the injector only instantiates once. Not inherited.
 *
 * @see javax.inject.Scope @Scope
 */
@Scope
@Documented
@Retention(RUNTIME)
public @interface Singleton {}
```
从Scope文档中的示例可以看出，这个Singleton的写法并没有什么特殊的，仅仅是在文档注释写了句标记单例的类型.实际上，Scope就是作为一种类型的标记而已，而这种标记的目的是为了更好地区分作用域.
@Scope所描述的注解用于两个地方：
- Component类
- Module中用于创建实例的provideXXX方法

使用Singleton注解来看看效果.

1. 在PersonModule中加入
```
@Module
public class PersonModule {
    @Provides
    @Singleton  //1.添加@Singleton标明该方法产生只产生一个实例
    public Person providePerson(){
        return new Person();
    }
}
```
2. 在Component中加入

```
@Singleton //2.添加@Singleton标明该Component中有Module使用了@Singleton
@Component(modules = PersonModule.class)
interface ScopeComponent {
    void inject(DaggerScopeActivity daggerActivity);//针对这个参数对象进行依赖注入
}
```
添加完Singleton注解以后.再次运行程序.我们发现在MainActivity中person1和person2的hash值相同.说明他们在MainActivity中保持了单例.

我们通过分析Dagger自动生成的代码来分析如何实现单例的：
```
public final class DaggerMainActivityComponent implements MainActivityComponent {
  private Provider<Person> providePersonProvider;

  private DaggerMainActivityComponent(MainModule mainModuleParam) {
    //2. 这里会调用initialize方法
    initialize(mainModuleParam);
  }

  public static Builder builder() {
    return new Builder();
  }

  public static MainActivityComponent create() {
    return new Builder().build();
  }

  @SuppressWarnings("unchecked")
  private void initialize(final MainModule mainModuleParam) {
    //2.根据MainModule创建providePersonProvider对象
    this.providePersonProvider = DoubleCheck.provider(MainModule_ProvidePersonFactory.create(mainModuleParam));
  }

  @Override
  public void inject(MainActivity activity) {
    injectMainActivity(activity);}

  private MainActivity injectMainActivity(MainActivity instance) {
    //3.providePersonProvider是单例的所以providePersonProvider.get()获取到的对象也是相同的
    MainActivity_MembersInjector.injectMPerson(instance, providePersonProvider.get());
    MainActivity_MembersInjector.injectMPerson2(instance, providePersonProvider.get());
    return instance;
  }

  public static final class Builder {
    private MainModule mainModule;

    private Builder() {
    }

    public Builder mainModule(MainModule mainModule) {
      this.mainModule = Preconditions.checkNotNull(mainModule);
      return this;
    }
    //1.通过build方法会创建一个MainModule对象
    public MainActivityComponent build() {
      if (mainModule == null) {
        this.mainModule = new MainModule();
      }
      return new DaggerMainActivityComponent(mainModule);
    }
  }
}
```
在创建DaggerMainActivityComponent时会调用initialize生成providePersonProvider对象.
MainModule_ProvidePersonFactory.java:
```
public final class MainModule_ProvidePersonFactory implements Factory<Person> {
  private final MainModule module;

  public MainModule_ProvidePersonFactory(MainModule module) {
    this.module = module;
  }

  @Override
  public Person get() {
    return providePerson(module);
  }
  //1.通过new关键字创建MainModule_ProvidePersonFactory对象
  public static MainModule_ProvidePersonFactory create(MainModule module) {
    return new MainModule_ProvidePersonFactory(module);
  }

  public static Person providePerson(MainModule instance) {
    return Preconditions.checkNotNull(instance.providePerson(), "Cannot return null from a non-@Nullable @Provides method");
  }
}
```
在DaggerMainActivityComponent的inject方法中providePersonProvider是单例的所以providePersonProvider.get()获取到的对象也是相同的.就算换个Scope，生成的也是一样的代码.
这个单例只针对同一个Component实例的情况下，毕竟Component本身也是能重复创建的,Dagger通过Singleton创建出来的单例并不保持在静态域上，而是保留在Component实例中。

那在别的Activity中是否也会是使用MainActivity中的单例对象呢?
我们再添加一个界面SecondActivity.
在SecondActivity中注入两个Person对象
```
@Inject
Person person3;
@Inject
Person person4;
@Override
protected void onCreate(@Nullable Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_main);
    DaggerMainActivityComponent.builder().mainModule(new MainModule(19)).build().inject(this);
    Log.d(TAG,person1+"");
    Log.d(TAG,person2+"");

}
```

重新运行程序.我们发现在SecondActivity中的person3和person4对象是相同的,但是并不和MainActivity中person1和person2的hash值相同.
这里也印证了我们上面的结论:用 @Singleton 确定的单例作用域应该也是在 Component 的范围内。这个范围在单个的 Component 中。
MainActivity 和 SecondActivity 运用了不同的 Component 即使他们都添加了@Singleton 注解 MainActivity 和 SecondActivity 中的生成的对象 也不是同一个。
如果在应用的Application中创建Component，在Activity中进行注入,那么被注入的对象在整个应用程序中就是单例的。

**在 Dagger2 中 Scope 机制可以保证在 Scope 标记的 Component 作用域内 ，类会保持单例 **

并不是只有 @Singleton  注解标记的相关类生产的实例是单例的，是所有的 Scope(自定义 Scope) 标记的相关类生产的实例 都是单例 的，只不过这个单例是有条件的 -- 在 Scope 注解标记 Component 的作用域内生产的实例是单例的 。
Scope 机制下的单例其实和 @Singleton 的字面意义 没有一点点关系，可以把 @Singleton  换成任意单词，什么 @Dog、@Cat、@XXx 都可以，你只要保证这个注解标记的 Component 在 App 进程中为单例的，并且得到正确的实现(被正确的标记到 类构造器 或 Module 中的 @Provides 标记的方法)，那么它对应生成的类实例就是 单例 的。
@Singleton 之所以被默认实现，只是因为这可以让人根据它的字面意思，知道被他标记的相关生成的类实例为单例，这符合了 Java 的命名规范。
例如我们要创建整个应用程序中的单例对象:
MyApplication.Java:
```
public class MyApplication extends Application {

    ActivityComponent activityComponent;
    @Override
    public void onCreate() {
        super.onCreate();
        activityComponent = DaggerActivityComponent.builder().build();
    }

    public static MyApplication getApplication(Context context){
        return (MyApplication) context.getApplicationContext();
    }

   public ActivityComponent getActivityComponent(){
        return activityComponent;
    }
}
```

FirstActivity.java:
```
public class FirstActivity extends AppCompatActivity {
    private TextView mContentTextView;

    @Inject
    Person person1;
    @Inject
    Person person2;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_singleton_and_scope);
        mContentTextView = (TextView) findViewById(R.id.contentTextView);
        //通过Application中的Component注入
        MyApplication.getApplication(this).getActivityComponent().inject(this);
        mContentTextView.setText(person1.hashCode() + "\n" + person2.hashCode());
    }

}
```
SecondActivity.java
```
public class SecondActivity extends AppCompatActivity {
    private TextView mContentTextView;

    @Inject
    Person person1;
    @Inject
    Person person2;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_singleton_and_scope);
        mContentTextView = (TextView) findViewById(R.id.contentTextView);
        //通过Application中的Component注入
        MyApplication.getApplication(this).getActivityComponent().inject(this);
        mContentTextView.setText(person1.hashCode() + "\n" + person2.hashCode());
    }

}
```
按照如上修改我们就可以得到全局的单例对象.
### 3.自定义@Scope
对于Android，我们通常会定义一个针对整个APP全生命周期的@PerApp的Scope注解,通过仿照@Singleton
```
@Scope
@Documented
@Retention(RUNTIME)
public @interface PerApp{}
```
你可能会发现，这个自定义的@Scope 和@Singleton代码完全一样，那@PerApp是不是也能具有实现单例模式的功能?答案是肯定的.
那你可能会有疑问，既然功能都是一样的，干嘛还自定义@Scope 结论就是不同的@Scope ，定义单例对象的生命周期，也就是使用范围。
在写代码时，程序员更加清楚什么时候创建Component，什么时候结束。

自定义@Scope总结起来有以下两点好处：

- 更好的管理ApplicationComponent和Module之间的关系，Component和Component之间的依赖和继承关系。如果关系不匹配，在编译期间会报错

- 代码可读性，让程序猿更好的了解Module中创建的类实例的使用范围。


@Singleton"并没有真正为你产生单列"，该注解只是保证只是在同一个Component对象中是单列而已，不同的Component进行注入，就会导致不是单例了，真正要实现全局单列，还是得靠自己控制，保证我们所有的地方都是使用同一个Component注入的对象.


总结的结论：
- 必须使用同一个Component对象来生成，也就是DaggerActivityComponent.builder().build()只能执行一次。
- Component和它的Module要使用相同的Scope。同一个Module中需要使用同样的Scope，否则相应的Component不知道使用什么Scope。
- 有依赖关系或者包含关系的Component不能使用同样的Scope。

>注意，Scope只的单例是在Component的生命周期中相关依赖是单例的，也就是同一个Component对象注入的同类型的依赖是相同的。按上面例子，如果我们又创建了个AppComponent，它注入的InfoRepository对象与之前的肯定不是一个。
这里所谓的「生命周期」是与 Component 相关联的。与 Activity 等任何 Android 组件没有任何关系.


# 六.@Named和@Qualifier注解
如果一个类有多个构造方法，或者有两个相同依赖时，它们都继承同一个父类或者实现同一个接口，那么怎么区分呢？这就要用到@Named或者@Qualifier注解了。

### 1. @Named
```
public class Car {
    private String engine = "默认引擎";
    private String tyre = "默认轮胎";
    private String color = "默认颜色";

    public Car() {
    }

    public Car(String engine) {
        this.engine = engine;
    }

    public Car(String engine, String tyre) {
        this.engine = engine;
        this.tyre = tyre;
    }

    public Car(String engine, String tyre, String color) {
        this.engine = engine;
        this.tyre = tyre;
        this.color = color;
    }

    public String make() {
        return "改装完成车的引擎是:" + engine + " 车的颜色是:" + color + " 车的轮胎是:" + tyre;
    }
}
```

```
@Module
public class QualifierModule {

    //普通车
    @Provides
    @Named("nomal")
    public Car defaultCarProvides() {
        return new Car();
    }

    //赛车
    @Provides
    @Named("racing")
    public Car racingCarProvides() {
        return new Car("赛车引擎");
    }

    //自定义改装车
    @Provides
    @Named("custom")
    public Car customCarProvides() {
        return new Car("赛车引擎", "米其林轮胎", "红色");
    }
}
```
```
public class  DaggerQualifierActivity extends AppCompatActivity() {

    //普通车
    @Inject
    @Named("nomal")
    Car defaultCar;

    //赛车
    @Inject
    @Named("racing")
    Car racingCar;

    //自定义改装车
    @Inject
    @Named("custom")
    Car customCar;

  @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.test_activity_dagger_qualifier);
        DaggerQualifierComponent.builder().qualifierModule(QualifierModule()).build().Inject(this)
    }
}
```
### 2.@Qualifier
以上通过 @Named 实现的标识功能 @Qualifier 同样可以实现，但是需要我们自定义注解来完成，具体一个使用场景如下：

自定义注解
```
@Qualifier
@Retention(RetentionPolicy.RUNTIME)
public @interface UserThirdQualifier {
    String value() default "";
}
```
注意，这里自定义注解需要使用 @Qualifier 进行标注。

Module 类中标记
```
@Module
public class UserThirdModule {

    @UserThirdQualifier("c")
    @Provides
    UserThird provideUserThird(){
        return new UserThird("男",1243);
    }

    @UserThirdQualifier("d")   
    @Provides
    UserThird provideUserThirdWithoutParams() {
        return new UserThird();
    }
}

```
目标类
```
public class ThirdActivity extends AppCompatActivity {
    @UserThirdQualifier("c")
    @Inject
    UserThird mUserTwoC;

    @UserThirdQualifier("d")
    @Inject
    UserThird mUserTwoD;

    private static final String TAG = "SecondActivity";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_second);
        DaggerUserThirdComponent.builder().userThirdModule(new UserThirdModule()).build().injectToThirdActivity(this);
        Log.e(TAG, "onCreate: " + "sex" + mUserTwoC.getSex() + " number：" + mUserTwoC.getCarNum());
        mUserTwoC.setCarNum(46);
        mUserTwoC.setSex("女");
        Log.e(TAG, "onCreate: " + "sex" + mUserTwoC.getSex() + " number：" + mUserTwoC.getCarNum());
        Log.e(TAG, "onCreate: " + "sex" + mUserTwoD.getSex() + " number：" + mUserTwoD.getCarNum());
    }
}
```
同样的，以上代码需要重点关注的是 Module 类 中使用 @UserThirdQualifier 注解方法和在 目标类 中使用 @UserThirdQualifier 注解标记类的实例变量，并且 Module 中的 @UserThirdQualifier("c") 和 目标类中的 @UserThirdQualifier("c")是一 一对应的。

# 七.Dagger2 中的懒加载和重加载
### 1. Dagger2 中的懒加载
智能懒加载，是Dagger2实现高性能的重要举措之一：在需要的时候才对成员变量进行初始化，可以大幅缩短应用初始化的时间。

使用方法：用Lazy<T>修饰变量即可。Lazy 是泛型类，接受任何类型的参数。
```
    @Inject
    Lazy<Object> object;
```    
用Lazy<T>修饰需要被注入的对象即可。
```
public class Car {
    /**
     * @Inject：@Inject有两个作用，一是用来标记需要依赖的变量，以此告诉Dagger2为它提供依赖
     */
    @Inject
    Lazy<Engine> engine;
 
    public Car() {
        DaggerCarComponent.builder().build().inject(this);
    }
 
    public Engine getEngine() {
        return this.engine;
    }
 
    public static void main(String ... args){
        Car car = new Car();
        System.out.println(car.getEngine());
    }
}
```
### 2.Provider 强制重新加载
@Singleton 标注实现的单例可以让我们每次获取的都是同一个对象（暂不细究全局/局部单例），但有时，我们希望每次都创建一个新的实例，这种情况与 @Singleton 完全相反。
Dagger2 通过 Provider 就可以实现。它的使用方法和 Lazy 很类似。

使用方法：用Provider<T>修饰变量即可。Provider是泛型类，接受任何类型的参数。 
```
    @Inject
    Provider<Object> object;
```
用Provider<T>修饰需要被注入的对象即可。 
```
public class Car {
    /**
     * @Inject：@Inject有两个作用，一是用来标记需要依赖的变量，以此告诉Dagger2为它提供依赖
     */
    @Inject
    Provider<Engine> engine;
 
    public Car() {
        DaggerCarComponent.builder().build().inject(this);
    }
 
    public Engine getEngine() {
        return this.engine;
    }
 
    public static void main(String ... args){
        Car car = new Car();
        System.out.println(car.getEngine());
    }
}
```

但是，需要注意的是 Provider 所表达的重新加载是说每次重新执行 Module 相应的 @Provides 方法，如果这个方法本身每次返回同一个对象，那么每次调用 get() 的时候，对象也会是同一个。

# 八.Component间依赖的两种方式
Component 管理着依赖实例，根据依赖实例之间的关系就能确定 Component 的关系。在 Dagger 2 中 Component 的组织关系分为两种：dependence和subcomponent，有些像组合和继承的关系。
- 依赖关系：一个 Component 依赖其他 Compoent ，以获得其中公开的依赖实例，用 Component 中的dependencies声明。
- 继承关系：一个 Component 继承（扩展）其他的 Component， 以获得其他的Component中的依赖，SubComponent 就是继承关系的体现。
### 1.Dependence方式
Component 依赖 是通过 @Component 的注解中 dependencies 选项来标识的，意思是指 该 Component 依赖 dependencies 指定的 Component 。
举个例子，看以下代码：
创建RetrofitUtils网络请求工具
```
public class RetrofitUtils {
    public String doNetWork() {
        return "网络请求到数据了:xxx";
    }
}
```
创建JsonUtils解析工具
```
public class JsonUtils {
    //解析Json数据
    public String parseJson(String json) {
        return "解析过后的Json数据:" + json;
    }
}
```
创建NetWorkModule提供RetrofitUtils和JsonUtils对象
```
@Module
public class NetWorkModule {
    //向外提供JsonUrils对象
    @Provides
    JsonUtils providesGson() {
        return new JsonUtils();
    }

    //向外提供RetrofitUtils对象
    @Provides
    RetrofitUtils providesRetrofit() {
        return new RetrofitUtils();
    }
}
```

以MVP架构为例:在Presenter中我们需要用到RetrofitUtils来请求网络数据,还需要用到JsonUtils来解析数据.
```
public class Presenter {

    private JsonUtils mJsonUtils;

    private RetrofitUtils mNetWorkUtils;


    public Presenter(JsonUtils jsonUtils, RetrofitUtils netWorkUtils) {
        this.mJsonUtils = jsonUtils;
        this.mNetWorkUtils = netWorkUtils;
    }

    public String doNetWork() {
        String respon = mNetWorkUtils.doNetWork();//请求网络数据
        String jsonString = mJsonUtils.parseJson(respon);//解析网路数据
        return jsonString;
    }
}
```
创建提供Presenter的PresenterModule
```
@Module
public class PresenterModule {
    //这里的JsonUtils和RetrofitUtils 是通过PresenterComponent里dependencies = NetWorkComponent,从NetWorkComponent里面获取的.
    @Provides
    public Presenter providesPresenter(JsonUtils jsonUtils, RetrofitUtils retrofitUtils) {
        return new Presenter(jsonUtils, retrofitUtils);
    }
}
```
创建NetWork依赖注入接口NetWorkComponent
```
@Component(modules = NetWorkModule.class)
public interface NetWorkComponent {

    //将NetWorkModule中的Gson对象、WorkUtils暴露出来，以便于其他依赖于NetWorkComponent的Component调用
    JsonUtils getGson();

    RetrofitUtils getNetWorkUtils();

    //自己本身也可以座位Component进行注入
    //void inject(DaggerDependenciesActivity daggerDependenciesActivity);
}
```
创建PresenterComponent依赖注入对象:
```
@Component(modules = PresenterModule.class, dependencies = NetWorkComponent.class)
public interface PresenterComponent {
    void inject(DaggerDependenciesActivity daggerDependenciesActivity);
}
```

DaggerDependenciesActivity.java
```
public class DaggerDependenciesActivity extends AppCompatActivity {
    @Inject
    Presenter mPresenter;
    @Inject
    RetrofitUtils mRetrofitUtils;
    @Inject
    JsonUtils mJsonUtils;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.test_activity_dagger_dependencies);
        DaggerPresenterComponent.builder().netWorkComponent(DaggerNetWorkComponent.create()).presenterModule(new PresenterModule()).build().inject(this);
        findViewById(R.id.btn_test).setOnClickListener(v -> {
            ToastUtils.showShort(mPresenter.doNetWork());
        });
    }
}

```
### 2.SubComponent
@SubComponent  也是管理 Component 间的依赖，不同的是这种方式不需要 在被依赖的 Component 中显式的声明可以获取相应类实例的方法。
通过 @SubComponent 来管理的 Component 之间是一种 继承关系，子 Component 理所当然的可以使用父 Component 的可以提供的类实例

子Component需要使用@Subcomponent注解，同时需要提供一个Builder接口，供父Component来生成Component，Builder接口中需提供一个返回子Component的抽象接口方法
子组件可以使用父组件所有的Module实现进行依赖注入，同时在构建子组件时的代码实现方式也和构建组件依赖时不一样。

首先定义一个使用@Subcomponent注解的依赖注入组件接口：
```
@Subcomponent(modules = {SubModule.class})
public interface MySubComponent {
    void inject(SubActivity activity);
}
```
它依赖的 SubModule 为：
```
@Module
public class SubModule {
    @Provides
    public Flower provideFlower() {
        return new Flower("腊梅", "红色");
    }
}
```
如果我们想让 DetailComponent 做为 MySubComponent 的父组件，则需要在 DetailComponent 中定义一个返回 MySubComponent 的方法，方法参数为其依赖的 Module 类型：
```
@DetailActivityScope
@Component(modules = {DetailModule.class})
public interface DetailComponent {
    void inject(DetailActivity activity);

    // 定义返回子组件的方法，参数为子组件需要的module
    MySubComponent getSubComponent(SubModule module);
}
```
到这里我们的子组件就实现完成了，如何使用呢？子依赖注入注入组件是不能单独直接使用的，因为编译后并不会生成类似DaggerMySubComponent的辅助类，所以需要通过父组件来获取，
这也是我们需要在父组件中定义返回子组件方法的原因。具体的用法如下：
```
public class SubActivity extends AppCompatActivity {
    @Inject
    Book book;

    @Inject
    Flower flower;

    public static void start(Context context) {
        context.startActivity(new Intent(context, SubActivity.class));
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_sub);
        // 创建父组件对象
        DetailComponent detailComponent = DaggerDetailComponent.builder().detailModule(new DetailModule()).build();
        // 得到子组件，并完成依赖注入
        detailComponent.getSubComponent(new SubModule()).inject(this);

        Log.e("SubActivity-book", book.toString());
        Log.e("flower", flower.toString());
    }
}
```
我们并没有在 SubModule 中定义提供 Flowerd 对象的方法，但是同过这种“继承”，MySubComponent 就可以提供 Flower 对象了.

### 5.依赖关系 vs 继承关系
相同点：
- 两者都能复用其他 Component 的依赖
- 有依赖关系和继承关系的 Component 不能有相同的 Scope

区别：
- 依赖关系中被依赖的 Component 必须显式地提供公开依赖实例的接口，而 SubComponent 默认继承 parent Component 的依赖。
- 依赖关系会生成两个独立的 DaggerXXComponent 类，而 SubComponent 不会生成 独立的 DaggerXXComponent 类。
- 在 Android 开发中，Activity 是 App 运行中组件，Fragment 又是 Activity 一部分，这种组件化思想适合继承关系，所以在 Android 中一般使用 SubComponent。

### 4.SubComponent 的其他问题
抽象工厂方法定义继承关系
除了使用 Module 的subcomponents属性定义继承关系，还可以在 parent Component 中声明返回 SubComponent 的抽象工厂方法来定义：
```
@ManScope
@Component(modules = CarModule.class)
public interface ManComponent {
    void injectMan(Man man);
    SonComponent sonComponent();    // 这个抽象工厂方法表明 SonComponent 继承 ManComponent
}
```
这种定义方式不能很明显地表明继承关系，一般推荐使用 Module 的subcomponents属性定义。

>Component 之间共用相同依赖，可以有两种组织关系：依赖关系与继承关系。在 Android 开发中，一般使用继承关系，以 AppComponent 作为 root Component，
AppComponent 一般还会使用 @Singleton 作用域，而 ActivityComponent 为 SubComponent。

参考资料:
[史上最适合新手的Dagger2教程（一）基本注入](https://blog.csdn.net/u014653815/article/details/81201865)
[Android |《看完不忘系列》之dagger](https://juejin.cn/post/6865659377957732359#heading-8)
[深入浅出依赖注入框架Dagger2](https://blog.csdn.net/cao861544325/article/details/81070582)
[Android -- 带你从源码角度领悟Dagger2入门到放弃（一）](https://www.cnblogs.com/wjtaigwh/p/6739614.html)
[Android -- 带你从源码角度领悟Dagger2入门到放弃（二）](https://www.cnblogs.com/wjtaigwh/p/6740643.html)
[Android -- 带你从源码角度领悟Dagger2入门到放弃（三）](https://www.cnblogs.com/wjtaigwh/p/6744939.html)
[Android基础知识：Dagger2入门](https://juejin.cn/post/6844903840450347016#heading-7)
[Dagger2从入门到放弃再到恍然大悟](https://juejin.cn/post/6847902225679958023)
[Dagger 2 系列（一） -- 前奏篇：依赖注入的基本介绍](https://juejin.cn/post/6844903682908094471)
[Android 神兵利器Dagger2使用详解（一）基础使用](https://blog.csdn.net/mq2553299/article/details/73065745)
[Dagger 2 使用及原理](https://www.jianshu.com/p/9f737e477d60)
[听说你还不会用Dagger2？Dagger2 For Android最佳实践教程](https://juejin.cn/post/6844903696417947662)
[轻松学，听说你还没有搞懂 Dagger2](https://blog.csdn.net/briblue/article/details/75578459)
[Dagger2的组件依赖及使用详解](https://blog.csdn.net/lylodyf/article/details/53009042)
[Dagger2 in Android（二）进阶](http://www.chenhe.cc/p/186#i-4)
[Dagger 2 完全解析（三），Component 的组织关系与 SubComponent](https://johnnyshieh.me/posts/dagger-subcomponent/)
[Dagger2 Android应用：@Scope和@Subcomponent](https://cloud.tencent.com/developer/article/1179695)
[Dagger2利器系列二：懒/重加载+Component 的组织关系](https://blog.csdn.net/lucasxu01/article/details/105645626)
[Android | 从 Dagger2 到 Hilt 玩转依赖注入（一）](https://www.jianshu.com/p/32a17846c2b0)
[Dagger2学习笔记4(@Singleton 与@ Scope 实现全局单例与作用域单例)](https://www.jianshu.com/p/c822faa2c083)
[详解 Dagger2 的 @Scope 和 @Subcomponent](https://juejin.cn/post/6844903459909533710)
[Dagger2 in Android（三）Scope与生命周期](https://juejin.cn/post/6844904201223405575)
[Dagger 2 系列（六） -- 进阶篇：Component 依赖、@SubComponent 与多 Component 下的 Scope 使用限制](https://juejin.cn/post/6844903683843424264)