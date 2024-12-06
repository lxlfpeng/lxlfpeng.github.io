---
title: 使用Aop技术提升Android开发效率
date: 2017-01-25
categories: 
  - Android开发
tags: 
  - AOP
  - 切面编程
---

# 一.AOP概念
**AOP** 和 **OOP**的区别:
面向对象的特点是``继承``、``多态``和``封装``。为了符合单一职责的原则，OOP将功能分散到不同的``对象``中去。让不同的类设计不同的方法，这样代码就分散到一个个的类中。可以降低代码的复杂程度，提高类的复用性。
但是OOP在分散代码的同时，也增加了代码的``重复性``。例如，我们在两个类中，可能都需要在每个方法中做日志。按照OOP的设计方法，我们就必须在两个类的方法中都加入记录日志的内容。也许他们是完全相同的，但是因为OOP的设计让类与类之间无法联系，而不能将这些重复的代码统一起来。然而AOP就是为了解决这类问题而产生的，它是在运行时动态地将代码切入到类的指定方法、指定位置上的编程思想。
AOP只是一种``思想``的统称，实现这种思想的方法有挺多。AOP通过``预编译方式``和``运行期动态代理``来实现程序功能的统一维护的一种技术。利用AOP可以对业务逻辑的各个部分进行隔离，从而使得业务逻辑各部分之间的耦合度降低，提高程序的可重用性，提高开发效率。
**总结**性的来说:AOP是一种：可以在不改变原来代码的基础上，通过“动态注入”代码，来改变原来执行结果的技术。

# 二.AOP主要使用场景
有这样一段代码:
```
 private void doSomeWork() {
        long startTime = System.currentTimeMillis();
        //执行要做的事
        long endTime = System.currentTimeMillis();
        //记录该方法运行的时间
        long duration = endTime - startTime;
    }
    private void doSomeWorkTwo() {
        long startTime = System.currentTimeMillis();
        //执行要做的事
        long endTime = System.currentTimeMillis();
        //记录该方法运行的时间
        long duration = endTime - startTime;
    }
```
doSomeWork()和doSomeWorkTwo()里面都要记录方法执行时间的代码，如果在两个方法中都写上记录时长的代码，不仅违背了单一职责的规则，而且使得代码非常的冗余。所以我们就可以使用AOP在这两个方法中动态的加入时间统计的代码。
AOP主要使用场景包括:
- 数据统计
- 日志记录
- 用户行为统计
- 应用性能统计
- 数据校验
- 行为拦截
- 无侵入的在宿主中插入一些代码，
- 做日志埋点
- 性能监控
- 动态权限控制
- 代码调试
>AOP是一种编程范式，与语言无关，是一种程序设计思想。

# 三.Java中实现AOP的方法
AOP仅仅只是个概念，就像是oop一样，是一种编程的思想。在Java中实现Aop主要有如下几种方式。
|方法|作用时机|操作对象|优点|缺点|
|-|-|-|-|-|
|APT|编译期：还未编译为 class 时|.java 文件|1. 可以织入所有类；2. 编译期代理，减少运行时消耗|1. 需要使用 apt 编译器编译；2. 需要手动拼接代理的代码（可以使用 Javapoet 弥补）；3. 生成大量代理类|
|Javassist |编译期：class 还未编译为 dex 时或运行时|class 字节码|1. 减少了生成子类的开销；2. 直接操作修改编译后的字节码，直接绕过了java编译器，所以可以做很多突破限制的事情，例如，跨 dex 引用，解决热修复中 CLASS_ISPREVERIFIED 问题。|运行时加入切面逻辑，产生性能开销。|
|AspectJ|编译期、加载时|.java 文件|1.功能强大，除了 hook 之外，还可以为目标类添加变量，接口。也有抽象，继承等各种更高级的玩法。2.和Java语言无缝衔接的面向切面的编程的扩展工具（可用于Android）。|1. 不够轻量级；2. 定义的切点依赖编程语言，无法兼容Lambda语法；3. 无法织入第三方库；4. 会有一些兼容性问题，如：D8、Gradle 4.x等|
|动态代理|运行时|-|在运行期，目标类加载后，为接口动态生成代理类，将切面织入到代理类中|-|

**Java代码注入主要利用了Java的反射和注解机制，根据注解时机的不同，主要分为 编译时织入、 加载时织入、运行时织入。**
### 1. 编译时织入。
编译时织入是指在java编译期，采用特殊的编译器，将切面织入到java类当中去。
### 2. 类加载时织入(也属于编译时织入的一种)。
类加载时织入指的是通过特殊的类加载器，在字节码加载到JVM时，织入切面。
### 3. 运行时织入。
运行时织入指的是使用动态代理等方式在运行的时候进行织入（这可以说并不是真正的代码注入）。

# 四.APT(annotation processing tool)技术
APT是一种处理编译器注解的工具，确切的说它是javac的一个工具，APT在代码编译期解析注解，并且生成新的 Java 文件，减少手动的代码输入。
原理：利用apt，可以找到源代中的注解，并根据注解做相应的处理，生成额外的class文件或其他文件。使用APT不会影响性能，只是影响项目构建的速度
这里我们说一下Android中使用apt的步骤，Android中开发自定义的apt学会两个库及一个类基本就足够了。
- [JavaPoet API](https://link.juejin.im?target=https%3A%2F%2Fgithub.com%2Fsquare%2Fjavapoet) 这个库的主要作用就是帮助我们通过类调用的形式来生成代码，简单理解就是利用这个库可以生成额外的Java代码。具体的API可以去github上看下。
- [AutoService](https://github.com/google/auto) 这个库是Google开发的，主要的作用是注解 processor 类，并对其生成 META-INF 的配置信息。可以理解使用这个库之后编译的时候IDE会编译我们的Annotation处理器，只需要在自定义的Processor类上添加注释 `@AutoService(Processor.class)`。

Processor类，我们自定义的Annotation处理器都需要实现该接口，Java为我们提供了一个抽象类实现了该接口的部分功能，我们自定义Annotation处理器的时候大部分只需要继承AbstractProcessor这个抽象类就行了。
### 1.JavaPoet技术实现AOP
``作用:``JavaPoet项目可以动态的生成Java文件，使用注解的时候假如需要生成新的Java文件就可以通过这个开源项目实现。
[JavaPoet](https://github.com/square/javapoet)
1. 导入依赖:
```
implementation 'com.squareup:javapoet:1.8.0'
```
也可以在开源项目处找到jar文件，下载下来，引入到项目中。
``JavaPoet常用的类:``
- MethodSpec 代表一个构造函数或方法声明。
- TypeSpec 代表一个类、借口或者枚举声明。
- FieldSpec 代表一个成员变量，一个字段声明。
- JavaFile 包含一个顶级类的Java文件。
2. 生成一个简单的类:
```
public static void main(String[] args) {
        ClassName activity = ClassName.get("android.app", "Activity");

        TypeSpec.Builder mainActivityBuilder = TypeSpec.classBuilder("SecondActivity")
                .addModifiers(Modifier.PUBLIC)
                .superclass(activity);

        ClassName override = ClassName.get("java.lang", "Override");

        ClassName bundle = ClassName.get("android.os", "Bundle");

        ClassName nullable = ClassName.get("android.support.annotation", "Nullable");

        ParameterSpec savedInstanceState = ParameterSpec.builder(bundle, "savedInstanceState")
                .addAnnotation(nullable)
                .build();

        MethodSpec onCreate = MethodSpec.methodBuilder("onCreate")
                .addAnnotation(override)
                .addModifiers(Modifier.PROTECTED)
                .addParameter(savedInstanceState)
                .addStatement("super.onCreate(savedInstanceState)")
                .addStatement("setContentView(R.layout.activity_main)")
                .build();

        TypeSpec mainActivity = mainActivityBuilder.addMethod(onCreate)
                .build();

        JavaFile javaFile = JavaFile.builder("com.test", mainActivity).build();
        File outputFile = new File("src/"); //输出文件

        try {
            javaFile.writeTo(outputFile);
            javaFile.writeTo(System.out);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
```

# 五.Javassit技术
[Javassit](https://github.com/jboss-javassist/javassist)
Java 字节码以二进制的形式存储在 .class 文件中，每一个 .class 文件包含一个 Java 类或接口。Javaassist 就是一个用来 处理 Java 字节码的类库。它可以在一个已经编译好的类中添加新的方法，或者是修改已有的方法，并且不需要对字节码方面有深入的了解。
Javassist 可以绕过编译，直接操作字节码，从而实现代码注入。所以使用 Javassist 的时机就是在构建工具 Gradle 将源 文件编译成 .class 文件之后，在将 .class 打包成 .dex 文件之前。

# 六.AspectJ技术
``AspectJ``实际上是对AOP编程思想的一个实践，AOP虽然是一种思想，但就好像OOP中的Java一样，一些先行者也开发了一套语言来支持AOP。目前用得比较火的就是AspectJ了，它是一种几乎和Java完全一样的语言，而且完全兼容Java。当然，除了使用AspectJ特殊的语言外，AspectJ还支持原生的Java，只要加上对应的AspectJ注解就好。所以，使用AspectJ有两种方法： 
- 完全使用AspectJ的语言。这语言一点也不难，和Java几乎一样，也能在AspectJ中调用Java的任何类库。AspectJ只是多了一些关键词罢了。 
- 或者使用纯Java语言开发，然后使用AspectJ注解，简称@AspectJ。

### 1.Android项目引入AspectJ
如果要在Android Studio中使用AspectJ，需要在项目的build里面进行一大堆配置，为了方便快捷，推荐使用沪江的[gradle_plugin_android_aspectjx](https://link.jianshu.com/?t=https%3A%2F%2Fgithub.com%2FHujiangTechnology%2Fgradle_plugin_android_aspectjx)。
##### (1.)步骤一:
在project级别的build.gradle中添加:
```
buildscript {
  ...
    dependencies {
     ...
        classpath 'com.hujiang.aspectjx:gradle-android-plugin-aspectjx:2.0.4'
    }
}
```
##### (2.)步骤二:
在module级别的build.gradle中添加:
```
apply plugin: 'android-aspectjx'
//或者这样也可以
apply plugin: 'com.hujiang.android-aspectjx'
```

### 2.AspectJ代码编写
##### (1.)步骤一:
创建一个FirstActivity ，只有基本的生命周期方法。
```
public class FirstActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_first);
    }

    @Override
    protected void onStart() {
        super.onStart();
    }

    @Override
    protected void onResume() {
        super.onResume();
    }
}
```
##### (2.)步骤二:
编写一个AspectJ类。这个类要做的事情是告诉ACJ编译器，要在MainActivity中的每个方法前面打印一行log，输出当前执行的是哪个方法，
```
@Aspect// 告诉ACJ编译器这是个AspectJ类
public class TraceAspect {
    private static final String TAG = "TraceAspect";

    @Pointcut("execution(* com.yousheng.aspectjdemo.FirstActivity.**(..))")// 注意*号后面必须有空格
    public void executeAspectJ() {

    }

    @Before("executeAspectJ()")
    public void beforeAspectJ(JoinPoint joinPoint) throws Throwable {
        Log.d(TAG, "injected -> " + joinPoint.toShortString());
    }
}

```
##### (3.)步骤三:
查看这段代码执行的结果
```
injected -> execution(FirstActivity.onCreate(..))
injected -> execution(FirstActivity.onStart())
injected -> execution(FirstActivity.onResume())
```
**分析:** 通过上面例子我们可以看到，我们在FirstActivity 的onCreate()，onStart()，onResume()中并未写任何代码，但是在执行这些方法的时候却输出了Log信息。这说明我们的切面成功的进行了切入。
而且在上面引出了``@Aspect``，``Join Points``，``@Pointcut``， ``@Around``这样的概念， 下面我们分别对这些进行解释。
1. **@Aspect** 修饰一个类，作用是把当前类标识为一个切面供容器读取，切面是切入点和通知的集合。
2. **Join Points** 程序运行执行点，比如上面的execution就是其中的一种类型，还有Call类型等 ，Join Points可以看做是程序运行时的一个``执行点``，比如：一个函数的调用可以看做是个Join Points，相当于代码切入点。但在AspectJ中，只有下面几种执行点是认为是Join Points
|Join Points|说明|实例|
|-|-|-|
|method call	| 函数调用 |	比如调用Log.e()，这是一个个Join Point|
|method execution |	函数执行 |	比如Log.e()的执行内部，是一处Join Points。注意这里是函数内部|
|constructor call |	构造函数调用 |	和method call 类似|
|constructor execution |	构造函数执行 |	和method execution 类似|
|field get |	获取某个变量 |	比如读取DemoActivity.debug成员|
|field set |	设置某个变量 |	比如设置DemoActivity.debug成员|
|pre-initialization |	Object在构造函数中做的一些工作。|	-|
|initialization |	Object在构造函数中做的工作。|	-|
|static initialization | 类初始化 |	比如类的static{}|
|handler  |	异常处理 |	比如try catch 中，对应catch内的执行|
|advice execution |	这个是AspectJ 的内容 |	-|

3. **Pointcut** 选出我们需要的Join Points，是指那些通过使用一些特定的表达式过滤出来的想要切入Advice的连接点。如
```
@Pointcut("execution(@com.yousheng.aspectjdemo.SingleClick * *(..))")// 切点表达式
private void dataAccessOperation() {} // 切点前面的这个方法必须无返回值.
```
``execution``指的是类型，也就是以方法执行时为切点，触发Aspect类。而execution里面的字符串是触发条件，也是具体的切点。``com.yousheng.aspectjdemo.annotation.SingleClick`` 指的是包名+对应的类名，第一个* 指的是返回值为任意类型，第二个*指的是方法名为任意类型或者是构造器的话使用new代替，(..)指的是任意类型的参数，参数用的是正则匹配语法。

**Join Points和Pointcut的区别**
Join point就是菜单上的选项，Pointcut就是你选的菜。Join point 你只是你切面中可以切的那些方法，一旦你选择了要切哪些方法，那就是Pointcut。
也就是说，所有在你程序中可以被调用的方法都是Join point. 使用Pointcut 表达式，那些匹配的方法，才叫Pointcut。所以你根本不用关心Join point。比如你有10个方法，你只想切2个方法，那么那10个方法就是Join point， 2个方法就是Pointcut。
所有的方法都可以认为是 joinpoint， 但是我们并不希望在所有的方法上都添加 Advice， 而 pointcut 的作用就是提供一组规则(使用 AspectJ pointcut expression language 来描述) 来匹配joinpoint， 给满足规则的 joinpoint 添加 Advice.
- **Advice** 就是我们插入的代码可以以何种方式插入，常见的有Before 还有 After、Around。

|名称 |描述|
|-|-|
|Before |在方法执行之前执行要插入的代码|
|After |在方法执行之后执行要插入的代码|
|Around |在方法前后各插入代码，他包含了 Before和 After 的全部功能|

- **Weaving** 编织：主要是在编译期使用AJC将切面的代码注入到目标中， 并生成出代码混合过的.class的过程.

execution()是最常用的切点函数，其语法如下所示:
例如下面这段语法：
```
@Around(“execution(* *..MainActivity+.on*(..))")
```
整个表达式可以分为五个部分：
- execution()是表达式主体
- 第一个*号代表返回类型，*号代表所有的类型。
- 包名 表示需要拦截的包名，这里使用*.代表匹配所有的包名。
- 第二个*号表示类名，后面跟.MainActivity是指具体的类名叫MainActivity。
- *(..) 最后这个星号表示方法名，+.代表具体的函数名，*号通配符，包括括弧号里面表示方法的参数，两个dot代表任意参数。


结合注解的例子:
**第一步:**
```
@Retention(RetentionPolicy.CLASS)
@Target(ElementType.METHOD)
public @interface Transaction {
}
```
**第二步:**
```
@Aspect
public class TransactionAspect {
    private static final String TAG = "TransactionAspect";
    private static final String TRANSACTION_METHOD =
            "execution(@com.goach.myaspectj.annotation.Transaction * *(..))";
    @Pointcut(TRANSACTION_METHOD)
    public void transactionMethod(){}

    @Around("transactionMethod()")
    public void addTransaction(ProceedingJoinPoint joinPoint){
        Log.d(TAG,"开始事务....");
        try {
            joinPoint.proceed();//执行原方法
        } catch (Throwable throwable) {
            throwable.printStackTrace();
        }
        Log.d(TAG,"结束事务....");
    }
}
```
**第三步:**
```
@Transaction//加上注解
public void hello(View view){
        Log.d(TAG,"hello aspectJ");
}
```
**执行结果 :**
![](/images/93cc8d85afdde4cf18bce704e340fcb6.webp)
```
   @Around("transactionMethod()")
    public void addTransaction(ProceedingJoinPoint joinPoint){
         MethodSignature methodSignature = (MethodSignature) point.getSignature();
// 拿到注解        
BehaviorTrace behaviorTrace = methodSignature.getMethod().getAnnotation(BehaviorTrace.class); 
// 类名
        String className = methodSignature.getDeclaringType().getSimpleName();
        // 方法名
        String methodName = methodSignature.getName();
    }
```

参考资料:
[AOP之AspectJ在Android中的应用](https://blog.csdn.net/xinzhou201/article/details/81566653)
[AndroidStudio 配置 AspectJ 环境实现AOP](https://blog.csdn.net/qby_nianjun/article/details/79182346)
[Spring 之AOP AspectJ切入点语法详解（最全面、最详细。）](https://blog.csdn.net/zhengchao1991/article/details/53391244)
[AOP AspectJ 字节码 示例 Hugo MD](https://www.cnblogs.com/baiqiantao/p/373ed2c28b94e268b82a0c18516f9348.html)
[AOP之@AspectJ技术原理详解](https://blog.csdn.net/woshimalingyi/article/details/73252013)
[关于AspectJ，你需要知道的一切](http://linbinghe.com/2017/65db25bc.html)
[java动态代理实现与原理详细分析](https://www.cnblogs.com/gonjan-blog/p/6685611.html)
[AOP技术的几种实现方式](http://android9527.com/2018/10/20/2018-10-20-AOP%E6%8A%80%E6%9C%AF%E7%9A%84%E5%87%A0%E7%A7%8D%E5%AE%9E%E7%8E%B0%E6%96%B9%E5%BC%8F/)
[一文读懂 AOP](https://www.jianshu.com/p/0799aa19ada1)

[android的APT技术](https://www.cnblogs.com/tangZH/p/12343786.html)
[Android APT快速教程](https://www.jianshu.com/p/7af58e8e3e18)
[【Android】APT](https://juejin.cn/post/6844903696900292621#heading-14)
[ARouter原理剖析及手动实现](https://www.bbsmax.com/A/A7zgNxWod4/)
[ARouter原理剖析及手动实现](https://www.jianshu.com/p/857aea5b54a8)
[Android APT工作原理（annotationProcessor）](https://www.jianshu.com/p/89ac9a2513c4)
