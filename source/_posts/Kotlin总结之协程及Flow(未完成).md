---
title: Kotlin总结之协程及Flow(未完成)
---

# 一. 什么是协程
协程本质是一套由 Kotlin 官方提供的线程 API，可以理解为一个线程框架。它最大的好处是：可以在同一个代码块中进行多次线程切换，简化异步任务处理的方案。

协程和线程的区别：

- 协程是运行在单线程中的并发程序，避免了多线程并发机制中切换线程时带来的线程上下文切换、线程状态切换、线程初始化上的性能损耗，能大幅度提高并发性能。

- 线程是由系统调度的，线程切换或线程阻塞的开销都比较大。而协程依赖于线程，但是协程挂起时不需要阻塞线程，几乎是无代价的，协程是由开发者控制的。所以协程也像用户态的线程，非常轻量级，一个线程中可以创建任意个协程。

- 协程是跑在线程上的，一个线程可以同时跑多个协程，每一个协程则代表一个耗时任务，需要手动控制多个协程之间的运行、切换，决定谁什么时候挂起，什么时候运行，什么时候唤醒，而不是线程那样交给系统内核来操作去竞争CPU时间片，缺点是本质是个单线程，不能利用到单个CPU的多个核心。

# 二. 工程配置(引入依赖)
首先，要在工程里引入协程。

这里注意，kotlin相关库的版本最好都用1.3.+的版本，并且要符合gradle插件版本在3.0.0版本以上才可以使用。
```
//project.gradle
classpath 'com.android.tools.build:gradle:3.1.2'
classpath "org.jetbrains.kotlin:kotlin-gradle-plugin:1.3.40"

//app.gradle
implementation "org.jetbrains.kotlinx:kotlinx-coroutines-android:1.3.5"
```

# 三. 启动协程
```
// 不会阻塞线程，但在 Android 中不推荐，因为它的生命周期会和 app 一致
GlobalScope.launch { 
  delay(1000L)    
  println("Hello,World!:Thread->" + Thread.currentThread().name)
 }

```
上述代码使用launch方法启动了一个协程，launch后面的花括号就是协程，花括号内的代码就是运行在协程内的代码。
先看一下GlobalScope类的源码:
```
public object GlobalScope : CoroutineScope {
    /**
     * Returns [EmptyCoroutineContext].
     */
    override val coroutineContext: CoroutineContext
        get() = EmptyCoroutineContext
}

```
发现GlobalScope是一个单例,并且实现了CoroutineScope接口.

再了解一下launch方法的声明：
```

public fun CoroutineScope.launch(
    context: CoroutineContext = EmptyCoroutineContext,
    start: CoroutineStart = CoroutineStart.DEFAULT,
    block: suspend CoroutineScope.() -> Unit
): Job {
    ...
}
```
launch方法是CoroutineScope的拓展方法，也就是说我们启动协程要在一个指定的CoroutineScope上来启动。
CoroutineScope翻译过来就是“协程范围”，指的是协程内的代码运行的时间周期范围，如果超出了指定的协程范围，协程会被取消执行，
上面第一段代码中的GlobalScope是全局单例对象因此它有与应用进程相同生命周期，也就是在进程没有结束之前协程内的代码都可以运行。

接着可以看下launch方法的其他参数：

- context：协程上下文，可以指定协程运行的线程。默认与指定的CoroutineScope中的coroutineContext保持一致，比如GlobalScope默认运行在一个后台工作线程内。
也可以通过显示指定参数来更改协程运行的线程，Dispatchers提供了几个值可以指定：Dispatchers.Default、Dispatchers.Main、Dispatchers.IO、Dispatchers.Unconfined。

- start：协程的启动模式。默认的（也是最常用的）CoroutineStart.DEFAULT是指协程立即执行，除此之外还有CoroutineStart.LAZY、CoroutineStart.ATOMIC、CoroutineStart.UNDISPATCHED。

- block：协程主体。也就是要在协程内部运行的代码，可以通过lamda表达式的方式方便的编写协程内运行的代码。

- CoroutineExceptionHandler：除此之外还可以指定CoroutineExceptionHandler来处理协程内部的异常。

返回值Job：对当前创建的协程的引用。可以通过Job的``start()、cancel()、join()``等方法来控制协程的启动和取消。

启动协程不是只有launch一个方法的，还有async等其他方法可以启动协程，不过launch是最常用的一种方法.


# 三. 协程作用域(协程运行环境)

协程是一套管理和运行异步任务的框架，所以需要有运行的环境，也叫协程的作用域，在这个作用域里，才可以使用协程来执行异步任务，协程作用域是协程运行的作用范围，
换句话说，如果这个作用域销毁了，那么里面的协程也随之失效。就好比变量的作用域。

#### 1. CoroutineScope 接口
在上文例子中我们看到GlobalScope实际上是实现了CoroutineScope接口的,查看这个接口的源代码的话就发现这个接口里面只定义了一个属性 CoroutineContext：
```
public interface CoroutineScope {
    // Scope 的 Context
    public val coroutineContext: CoroutineContext
}

```

#### 2. GlobalScope(全局作用域)
GlobalScope 是 CoroutineScope 的一个单例实现，是一个单例对象，是默认的全局作用域。GlobalScope 实现了 CoroutineScope 接口，这个接口持有了协程上下文。
```
public object GlobalScope : CoroutineScope {
    /**
     * Returns [EmptyCoroutineContext].
     */
    override val coroutineContext: CoroutineContext
        get() = EmptyCoroutineContext
}
```
用法:
```
GlobalScope.launch {
    //...
}
```
GlobalScope代表协程的全局作用域，在该作用域启动的协程为顶层协程，没有父任务，且该scope没有Job对象(管理任务)，所以无法对整个scope执行cancel()操作，所以如果没有手动取消每个任务，
会造成这些任务一直运行(覆水难收)，可能会导致内存泄露等问题，所以不适用于业务开发。


#### 3. 自定义作用域
协程作用域的创建方式有很多，常见的有：
- 继承 CoroutineScope 接口自己实现；
- 使用 coroutineScope 方法或者 supervisorScope 方法创建；

######  实现CoroutineScope 接口
在应用中具有生命周期的组件应该实现 CoroutineScope 接口，并负责该组件内 Coroutine 的创建和管理。

```
CoroutineScope(Dispatchers.Main).launch {
    //...
}
```
通常我们会通过创建CoroutineScope，来实现一个自己的协程作用域，并且可以指定派发器，在我们需要取消该scope下所有任务时(比如Activity退出时)，
调用scope.cancel()方法，就可以取消该scope下所有正在进行的任务，这才是我们所期望的。

例如对于 Android 应用来说，可以在 Activity 中实现 CoroutineScope 接口， 例如：
```
class ScopedActivity : Activity(), CoroutineScope {
    lateinit var job: Job
    // CoroutineScope 的实现
    override val coroutineContext: CoroutineContext
        get() = Dispatchers.Main + job

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        job = Job()

    /*
     * 注意 coroutine builder 的 scope， 如果 activity 被销毁了或者该函数内创建的 Coroutine
     * 抛出异常了，则所有子 Coroutines 都会被自动取消。不需要手工去取消。
     */
      launch { // <- 自动继承当前 activity 的 scope context，所以在 UI 线程执行
          val ioData = async(Dispatchers.IO) { // <- launch scope 的扩展函数，指定了 IO dispatcher，所以在 IO 线程运行
            // 在这里执行阻塞的 I/O 耗时操作
          }
        // 和上面的并非 I/O 同时执行的其他操作
          val data = ioData.await() // 等待阻塞 I/O 操作的返回结果
          draw(data) // 在 UI 线程显示执行的结果
      }
    }

    override fun onDestroy() {
        super.onDestroy()
        // 当 Activity 销毁的时候取消该 Scope 管理的 job。
        // 这样在该 Scope 内创建的子 Coroutine 都会被自动的取消。
        job.cancel()
    }


}
```
由于所有的 Coroutine 都需要一个 CoroutineScope，所以为了方便创建 Coroutine，在 CoroutineScope 上有很多扩展函数，比如 launch、async、actor、cancel 等。



 **②  使用 coroutineScope 和 supervisorScope 方法创建协程作用域**
coroutineScope 方法可以用来创建一个子作用域，它只能在另一个已有的协程作用域中调用，例如在另外一个 suspend 方法中调用。
supervisorScope 方法和 coroutineScope 类似，也用于创建一个子作用域，区别是 supervisorScope 出现异常时不影响其他子协程， coroutineScope 出现异常时会把异常抛出。

#### 4. MainScope
在 Android 中会经常需要实现这个 CoroutineScope，所以为了方便开发者使用， 标准库中定义了一个 MainScope() 函数，
该函数定义了一个使用 SupervisorJob 和 Dispatchers.Main 为 Scope context 的实现。

```
class MainActivity: AppCompatActivity(), CoroutineScope by MainScope() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // 在IO线程中，请求网络数据
        launch(Dispatchers.IO) {
            val res = requestService()

            // 在主线程中，更新 UI
            launch {
                updateUi(res)
            }
        }
    }

    override fun onDestroy() {
        super.onDestroy()

        // 在 Activity 销毁时取消
        cancel()
    }
}
```



# 四. 启动协程
现在有了协程运行环境和任务执行环境，接下来要做的就是启动一个协程了！
需要构造器来启动协程。官方目前提供的基础构造器有两个：

- runBlocking
- 通过scope对象，使用launch和async方法创建协程。

这两个构造器都会启动一个协程，区别在于后者不会阻塞当前线程，并且会返回一个协程的引用，而前者会等待协程的代码执行结束，再执行剩下的代码。

### 1. runBlocking
runBlocking是启动新协程的一种方法。
runBlocking启动一个新的协程，并阻塞它的调用线程，直到里面的代码执行完毕。

```
 public fun <T> runBlocking(context: CoroutineContext = EmptyCoroutineContext, block: suspend
  CoroutineScope.() -> T): T {
        ...
    }
```

举例

```
println("aaaaaaaaa ${Thread.currentThread().name}")

runBlocking {
    for (i in 0..10) {
        println("$i ${Thread.currentThread().name}")
        delay(100)
    }
}

println("bbbbbbbbb ${Thread.currentThread().name}")
```

上面代码的输出为：

```
aaaaaaaaa main
0 main
1 main
2 main
3 main
4 main
5 main
6 main
7 main
8 main
9 main
10 main
bbbbbbbbb main
```

所有的代码都在主线程执行，按照顺序来，去掉runBlocking也是一样的。

但是，runBlocking可以指定参数，就可以让runBlocking里面的代码在其他线程执行，但同样可以阻塞外部线程。

```
println("aaaaaaaaa ${Thread.currentThread().name}")
runBlocking(Dispatchers.IO) { // 注意这里
    for (i in 0..10) {
        println("$i ${Thread.currentThread().name}")
        delay(100)
    }
}
println("bbbbbbbbb ${Thread.currentThread().name}")
```

上面的代码，给runBlocking添加了一个参数，Dispatchers.IO，这样里面的代码块就会执行到其他线程了。

来一起看看效果：

```
aaaaaaaaa main
0 DefaultDispatcher-worker-1
1 DefaultDispatcher-worker-1
2 DefaultDispatcher-worker-1
3 DefaultDispatcher-worker-4
4 DefaultDispatcher-worker-4
5 DefaultDispatcher-worker-6
6 DefaultDispatcher-worker-7
7 DefaultDispatcher-worker-7
8 DefaultDispatcher-worker-9
9 DefaultDispatcher-worker-1
10 DefaultDispatcher-worker-5
bbbbbbbbb main
```

### 2. launch方法
launch 是最常见的协程构建器，它会启动一个新的协程(AbstractCoroutine)，并将这个协程对象返回，接着会在协程中执行参数中的 block。不会阻塞调用线程。

AbstractCoroutine 继承了 Job，launch 返回的 Job 对象实际就是协程对象本身。

launch 的原型如下：
```
public fun CoroutineScope.launch(
    /** 上下文 */
    context: CoroutineContext = EmptyCoroutineContext,

    /** 如何启动 */
    start: CoroutineStart = CoroutineStart.DEFAULT,

    /** 启动后要执行的代码 */
    block: suspend CoroutineScope.() -> Unit
): Job
```
launch 方法有两个可选参数：``CoroutineContext 和 CoroutineStart``。
- CoroutineContext：
  是协程的上下文，默认使用 EmptyCoroutineContext，最主要的两个元素是：Job、Dispatcher。
Job控制协程的开始、取消等，Dispatchers作用是决定把协程派发到哪个线程中执行，与指定的CoroutineScope中的coroutineContext保持一致，比如GlobalScope默认运行在一个后台工作线程内。也可以通过显示指定参数来更改协程运行的线程，Dispatchers提供了几个值可以指定：Dispatchers.Default、Dispatchers.Main、Dispatchers.IO、Dispatchers.Unconfined。

- CoroutineStart：
协程的启动模式。默认的（也是最常用的）CoroutineStart.DEFAULT是指协程立即执行，除此之外还有CoroutineStart.LAZY、CoroutineStart.ATOMIC、CoroutineStart.UNDISPATCHED。

- block：
协程主体。也就是要在协程内部运行的代码，block是一个suspend匿名方法，可以通过lamda表达式的方式方便的编写协程内运行的代码。

- 返回值Job：
Job是launch方法的返回值，它就是用来控制协程的运行状态的。Job中有几个关键方法：
   - start。如果是CoroutineStart.LAZY创建出来的协程，调用该方法开启协程。
   - cancel。取消正在执行的协程。如协程处于运算状态，则不能被取消。也就是说，只有协程处于阻塞状态时才能够取消。
    - join。阻塞父协程，直到本协程执行完。
    - cancelAndJoin。等价于cancel + join。

### 3. async方法

async 比较常见，它也会启动新的协程(AbstractCoroutine)，并返回这个协程对象，然后在协程中执行 block。它与launch类似，差别在于返回值。async方法返回一个Deferred<T>类型。
Deferred继承自Job，最主要的是增加了await方法，通过await方法返回T。Deferred.await在等待返回值时会阻塞当前的协程。

参数和 launch 一样，我们看看 async 怎么获取返回值：
```
// 任务1：耗时一秒后返回100
val coroutine1 = GlobalScope.async {
    delay(1000)
    return@async 100
}

// 任务2：耗时1秒后返回200
val coroutine2 = GlobalScope.async {
    delay(1000)
    return@async 200
}

// 上面两个协程会并发执行

// 等待两个任务都执行完毕后，再继续下一步（打印结果）。
GlobalScope.launch {
    val v1 = coroutine1.await()
    val v2 = coroutine2.await()
    log("执行的结果,v1 = $v1, v2=$v2")
}
```

### 4. launch和async方法创建协程区别。
```
CoroutineScope(Dispatchers.IO).launch {  }
CoroutineScope(Dispatchers.IO).async {  }
```
而两者的最大不同是，async会创建一个Deferred的协程，可以用来等待该协程执行完毕再进行后续操作。
runBlocking {  }在当前线程启动一个协程，阻塞当前线程。也是一个协程，不过一般不这样使用
```
CoroutineScope(Dispatchers.IO).launch {
  val job = async {  }
  val data = job.await()
  //do something with data
}
```
上述代码，在launch的协程执行到await()方法时，会将协程挂起(而不是线程挂起，不会阻塞线程)，等待async异步任务执行完成后，会返回结果到data，从而进行后续逻辑。

当然，如果在调用await()方法时，async协程已经执行完毕拥有了结果，那么不会挂起协程，而是直接返回结果到data变量里。

# 五. 协程派发器(任务执行环境)

有了运行环境执行异步任务，还需要有派发器将不同的任务派发到不同的线程执行，在lanch()函数中有一个CoroutineContext 参数，该参数就是制定任务环境的参数。这也是我们经常遇到的，比如网络请求在工作线程，结果回来后的UI展示，需要在主线程进行。协程调度器可以将协程的执行局限在指定的线程中，调度它运行在线程池中或让它不受限的运行。kotlin给我们提供了一些默认的Dispatcher：

- Dispatchers.IO：工作线程池，依赖于Dispatchers.Default，支持最大并行任务数。这个调度器被优化在主线程之外执行磁盘或网络 I/O。例如包括使用 Room 组件、读写文件，以及任何网络操作。

- Dispatchers.Main：主线程，这个在不同平台定义不一样，所以需要引入相关的依赖，比如Android平台，需要使用包含MainLooper的handler来向主线程派发。使用这个调度器在 Android 主线程上运行一个协程。这应该只用于与 UI 交互和一些快速工作。示例包括调用挂起函数、运行 Android UI 框架操作和更新 LiveData 对象。

- Dispatchers.Default：默认线程池，核心线程和最大线程数依赖cpu数量。这个调度器经过优化，可以在主线程之外执行 cpu 密集型的工作。例如对列表进行排序和解析 JSON。

- Dispatchers.Unconfined：无指定派发线程，会根据运行时的上线文环境决定。

通常我们用的就是Dispatchers.IO和 Dispatchers.Main，在创建scope时，可以指定派发器，如``CoroutineScope(Dispatchers.Main)``，就是指定该scope启动的协程，都在主线程执行。调度器实现了CoroutineContext接口。
# 六. 启动模式
在lanch()函数中有一个CoroutineContext 参数，该参数就是制定任务环境的参数。在Kotlin协程当中，启动模式定义在一个枚举类中：
```
public enum class CoroutineStart {
    DEFAULT,
    LAZY,
    @ExperimentalCoroutinesApi
    ATOMIC,
    @ExperimentalCoroutinesApi
    UNDISPATCHED;
}
```
一共定义了4种启动模式，下表是含义介绍：

|启动模式	|作用|
|  ----  | ----  |
DEFAULT	| 默认的模式，立即执行协程体
LAZY	| 只有在需要的情况下运行
ATOMIC	| 立即执行协程体，但在开始运行之前无法取消
UNDISPATCHED	| 立即在当前线程执行协程体，直到第一个 suspend 调用



# 七. 挂起函数
协程体是一个用suspend关键字修饰的一个无参，无返回值的函数类型。被suspend修饰的函数称为挂起函数，与之对应的是关键字resume（恢复），suspend，对协程的挂起并没有实际作用，其实只是一个提醒，函数创建者对函数的调用者的提醒，提醒调用者我是需要耗时操作，需要用挂起的方式，在协程中使用。

注意：挂起函数只能在协程中和其他挂起函数中调用，不能在其他地方使用，因为普通函数没有suspend和resume这两个特性，所以必须要在协程的作用中使用。通过报错来提醒调用者和编译器，这是一个耗时函数，需要放在后台执行。

给函数前加上suspend 关键字
```
suspend fun testSuspendfun(){

  }
```
需要使用挂起函数常见的场景有：

- 耗时操作：使用 withContext 切换到指定的 IO 线程去进行网络或者数据库请求、io耗时操作获取数据库数据、一些等待一会需要的操作：列表排除，json解析等;

- 等待操作：使用delay方法去等待某个事件。


# 八. 取消协程
现在我们已经可以完整的运行一个协程任务了，还有一个问题，就是如何取消协程呢？这个也很重要，比如Android中的网络请求等资源数据的加载，需要在页面关闭时中断，从而减少性能流量的损耗，以及避免一些内存泄露的问题。
```
//1.通过协程cancel()
val scope = CoroutineScope(Dispatchers.IO)
scope.launch {
  launch {
    while (true) {
      log("inner-launch")
    }
  }
  while (true) {
    log("outer-launch")
  }
}
scope.launch {
  delay(1000)
  scope.cancel()
}
//2.通过CorouinteScope.cancel)(
val scope = CoroutineScope(Dispatchers.IO)
val outerJob = scope.launch {
  launch {
    while (true) {
      log("inner-launch")
    }
  }
  while (true) {
    log("outer-launch")
  }
}
scope.launch {
  delay(1000)
  outerJob.cancel()
}
```
kotlin协程的取消规则是这样的：
- 父协程调用cancel()，会取消自己以及所有子(内部)协程。
- 子协程调用cancel()，默认不会取消父协程。

可以通过调用CoroutineScope的cancel()方法，取消掉该scope产生的所有协程。

据此，以上两个demo的行为是这样的：
1. outer和inner的协程全部被取消。
2. outer和inner以及scope开启的所有协程被取消。

但是，运行上面的demo我们会发现，log会一直输出东西，这是为什么呢？因为协程的cancel()原理是改变了协程对象的内部状态，但并没有终止逻辑代码的调用，也就是说协程状态和代码运行是两个部分，具体的原理我们在下面会说。那我们应该怎么办呢？

答案很简单，既然改变了协程的状态，那么我们用协程状态字段来判断协程是否被取消了即可，将判断条件代码改成如下：
```
while (isActive) {
  log("outer-launch")
}
```
isActive是协程的一个状态字段。

# 八. 异常捕获
现在我们成功通过协程执行了一段代码，对于执行代码，必不可少就是对可能的异常进行捕获和处理。
kotlin的协程，也有一套自己的捕获异常机制。


```
//1.根协程为launch
CoroutineScope(Dispatchers.IO).launch {
  async{ launch { throw IllegalStateException("this is an error") } }
}
//2.根协程为async
CoroutineScope(Dispatchers.IO).async {
  async{ launch { throw IllegalStateException("this is an error") } }
}
//3.捕获async{}.await()异常
CoroutineScope(Dispatchers.IO).async {
  try {
    val job = async { throw IllegalStateException("this is an error") }
    val data = job.await()
    //do something with data
  } catch (e: Exception) {
    log(e.message)
  }
}
```
先来简单描述下协程的异常机制：

- 在协程内部通过try-catch捕获的异常，由我们自己处理(和java异常一样)。

- 未捕获的异常，协程本身默认不处理，而是一层一层的交由父协程，直到根协程进行处理。

- 根协程处理异常时，会使用注册的CoroutineExceptionHandler对象进行处理；Android的协程依赖包，会引入并自动注册一个该对象，处理行为与java处理一致(直接交由UncaughtExceptionHandler)。

- 有些协程类型重写了处理异常方法，默认不处理异常，比如async式协程，这类协程作为根协程的话，最终会导致异常丢失，继续执行后续逻辑。

- 内部协程出现异常，会逐层cancel掉父协程。

据此机制，我们看下上面三个demo的异常处理情况：

- 根协程为launch式协程时，会使用Android提供的handler进行异常抛出，最终表现就是应用崩溃。

- 根协程为async式协程时，不会处理异常，最终表现就是没异常的抛出(但继续执行下去其实很危险)。

- async式协程的await()方法，在返回异常时，会进行抛出，所以我们可以通过try-catch这个await()方法，来捕获async式协程产生的异常。

这里需要注意的是，如果根协程为launch式协程，即使我们使用(3)描述的办法，依然没有办法阻止崩溃，因为launch协程会处理异常并抛出。

综上所述，对于我们想捕获的异常，最靠谱的办法还是在协程内部自己捕获异常进行处理，避免因为未捕获而直接崩溃。

supervisorScope
指定协程作用域，在该作用域内当自身执行任务失败的时候，只会向下传播去关闭子协程,

异常传播
异常传播还涉及到协程作用域的概念，例如我们启动协程的时候一直都是用的 GlobalScope，意味着这是一个独立的顶级协程作用域，此外还有 coroutineScope{...} 以及 supervisorScope{...}。

通过 GlobeScope 启动的协程单独启动一个协程作用域，内部的子协程遵从默认的作用域规则。通过 GlobeScope 启动的协程“自成一派”。

coroutineScope 是继承外部 Job 的上下文创建作用域，在其内部的取消操作是双向传播的，子协程未捕获的异常也会向上传递给父协程。它更适合一系列对等的协程并发的完成一项工作，任何一个子协程异常退出，那么整体都将退出，简单来说就是”一损俱损“。这也是协程内部再启动子协程的默认作用域。

supervisorScope 同样继承外部作用域的上下文，但其内部的取消操作是单向传播的，父协程向子协程传播，反过来则不然，这意味着子协程出了异常并不会影响父协程以及其他兄弟协程。它更适合一些独立不相干的任务，任何一个任务出问题，并不会影响其他任务的工作，简单来说就是”自作自受“，例如 UI，我点击一个按钮出了异常，其实并不会影响手机状态栏的刷新。需要注意的是，supervisorScope 内部启动的子协程内部再启动子协程，如无明确指出，则遵守默认作用域规则，也即 supervisorScope 只作用域其直接子协程。

# Kotlin Flow

Flow 库是在 Kotlin Coroutines 1.3.2 发布之后新增的库，也叫做异步流，类似 RxJava 的 Observable 、 Flowable 等等
1. 基础
先上一段代码：
lifecycleScope.launch {
    // 创建一个协程 Flow<T>
    createFlow()
        .collect {num->
            // 具体的消费处理
            // ...
        }
    }
}
复制代码
我在 createFlow 这个方法中，返回了 Flow<Int> 的对象，所以我们可以这样对比。



对比
Flow
RxJava




数据源
Flow<T>
Observable<T>


订阅
collect
subscribe



创建 Flow 对象
我们暂不考虑 RxJava中的背压和非背压，直接先将 Flow 对标 RxJava 中的 Observable。
和 RxJava 一样，在创建 Flow 对象的时候我们也需要调用 emit 方法发射数据：
fun createFlow(): Flow<Int> = flow {
    for (i in 1..10)
        emit(i)
}
复制代码
一直调用 emit 可能不便捷，因为 RxJava 提供了 Observable.just() 这类的操作符，显然，Flow 也为我们提供了快速创建操作：

flowof(vararg elements: T)：帮助可变数组生成 Flow 实例扩展函数 .asFlow()：面向数组、列表等集合
比如可以使用 (1..10).asFlow() 代替上述的 Flow 对象的创建。
消费数据
collect 方法和 RxJava 中的 subscribe 方法一样，都是用来消费数据的。
除了简单的用法外，这里有两个问题得注意一下：

collect 函数是一个 suspend 方法，所以它必须发生在协程或者带有 suspend 的方法里面，这也是我为什么在一开始的时候启动了 lifecycleScope.launch。lifecycleScope 是我使用的 Lifecycle 的协程扩展库当中的，你可以替换成自定义的协程作用域。
2. 线程切换
我们学习 RxJava 的时候，大佬们都会说，RxJava 牛逼，牛逼在哪儿呢？
切换线程，同样的，Flow 的协程切换也很牛逼。Flow 是这么切换协程的：
lifecycleScope.launch {
    // 创建一个协程 Flow<T>
    createFlow()
        // 将数据发射的操作放到 IO 线程中的协程
        .flowOn(Dispatchers.IO)
        .collect { num ->
            // 具体的消费处理
            // ...
        }
    }
}
复制代码
和 RxJava 对比：



操作
Flow
RxJava




改变数据发射的线程
flowOn
subscribeOn


改变消费数据的线程
无
observeOn



改变数据发射的线程
flowOn 使用的参数是协程对应的调度器，它实质改变的是协程对应的线程。
改变消费数据的线程
我在上面的表格中并没有写到在 Flow 中如何改变消费线程，并不意味着 Flow 不可以指定消费线程？
Flow 的消费线程在我们启动协程指定调度器的时候就确认好了，对应着启动协程的调度器。比如在上面的代码中 lifecycleScope 启动的调度器是 Dispatchers.Main，那么 collect 方法就消费在主线程。
3. 异常和完成
异常捕获



对比
Flow
RxJava




异常
catch
onError



Flow 中的 catch 对应着 RxJava 中的 onError，catch 操作：
lifecycleScope.launch {
    flow {
        //...
    }.catch {e->

    }.collect(

    )
}
复制代码
除此以外，你可以使用声明式捕获 try { } catch (e: Throwable) { } 去捕获异常，不过 catch 本质上是一个扩展方法，它是对声明式捕获的封装。
完成



对比
Flow
RxJava




完成
onCompletion
onComplete



Flow 中的 onCompletion 对应这 RxJava 中的 onComplete 回调，onCompletion操作：
lifecycleScope.launch {
    createFlow()
        .onCompletion {
            // 处理完成操作
        }
        .collect {

        }
}
复制代码
除此以外，我们还可以通过捕获式 try {} finally {} 去获取完成情况。
4. Flow的特点
我们在对 Flow 已经有了一些基础的认知了，再来聊一聊 Flow 的特点，Flow 具有以下特点：

冷流有序协作取消
如果你对 Kotlin 中的 Sequence 有一些认识，那么你应该可以轻松的 Get 到前两个点。
冷流
有点类似于懒加载，当我们触发 collect 方法的时候，数据才开始发射。
lifecycleScope.launch {
    val flow = (1..10).asFlow().flowOn(Dispatchers.Main)

    flow.collect { num ->
            // 具体的消费处理
            // ...
        }
    }
}
复制代码
也就是说，在第2行的时候，虽然流创建好了，但是数据一直到第四行发生 collect 才开始发射。
有序
看代码比较容易理解：
lifecycleScope.launch {
    flow {
        for(i in 1..3) {
            Log.e("Flow","$i emit")
            emit(i)
        }
    }.filter {
        Log.e("Flow","$it filter")
        it % 2 != 0
    }.map {
        Log.e("Flow","$it map")
        "${it * it} money"
    }.collect {
        Log.e("Flow","i get $it")
    }
}
复制代码
得到的日志：
E/Flow: 1 emit
E/Flow: 1 filter
E/Flow: 1 map
E/Flow: i get 1 money
E/Flow: 2 emit
E/Flow: 2 filter
E/Flow: 3 emit
E/Flow: 3 filter
E/Flow: 3 map
E/Flow: i get 9 money
复制代码
从日志中，我们很容易得出这样的结论，每个数据都是经过 emit、filter 、map和 collect 这一套完整的处理流程后，下个数据才会开始处理，而不是所有的数据都先统一 emit，完了再统一 filter，接着 map，最后再 collect。
协作取消
Flow 采用和协程一样的协作取消，也就是说，Flow 的 collect 只能在可取消的挂起函数中挂起的时候取消，否则不能取消。
如果我们想取消 Flow 得借助 withTimeoutOrNull 之类的顶层函数，不妨猜一下，下面的代码最终会打印出什么？
lifecycleScope.launch {
    val f = flow {
        for (i in 1..3) {
            delay(500)
            Log.e(TAG, "emit $i")
            emit(i)
        }
    }
    withTimeoutOrNull(1600) {
        f.collect {
            delay(500)
            Log.e(TAG, "consume $it")
        }
    }
    Log.e(TAG, "cancel")
}
复制代码
5. 操作符对比
限于篇幅，我仅介绍一下 Flow 中操作符的作用，就不一一介绍每个操作符具体怎么使用了。
普通操作符：



Flow 操作符
作用




map
转换操作符，将 A 变成 B


take
后面跟 Int 类型的参数，表示接收多少个 emit 出的值


filter
过滤操作符



特殊的操作符
总会有一些特殊的情况，比如我只需要取前几个，我只要最新的数据等，不过在这些情况下，数据的发射就是并发执行的。



Flow 操作符
作用




buffer
数据发射并发，collect 不并发


conflate
发射数据太快，只处理最新发射的


collectLatest
接收处理太慢，只处理最新接收的



组合操作符



Flow 操作符
作用




zip
组合两个流，双方都有新数据才会发射处理


combine
组合两个流，在经过第一次发射以后，任意方有新数据来的时候就可以发射，另一方有可能是已经发射过的数据



展平流操作符
展平流有点类似于 RxJava 中的 flatmap，将你发射出去的数据源转变为另一种数据源。



Flow 操作符
作用




flatMapConcat
串行处理数据


flatMapMerge
并发 collect 数据


flatMapLatest
在每次 emit 新的数据以后，会取消先前的 collect



末端操作符
顾名思义，就是帮你做 collect 处理，collect 是最基础的末端操作符。



末端流操作符
作用




collect
最基础的消费数据


toList
转化为 List 集合


toSet
转化为 Set 集合


first
仅仅取第一个值


single
确保流发射单个值


reduce
规约，如果发射的是 Int，最终会得到一个 Int，可做累加操作


fold
规约，可以说是 reduce 的升级版，可以自定义返回类型



其他还有一些操作符，我这里就不一一介绍了，感兴趣可以查看 API。






[Kotlin 协程之一：基础使用](https://blog.csdn.net/qq_15827013/article/details/97644113)
[破解 Kotlin 协程(1) - 入门篇](https://www.jianshu.com/p/086a0d681f29)
[Kotlin Coroutine(协程) 简介](https://blog.csdn.net/huyongl1989/article/details/89287132)
[kotlin 协程在 Android 中的使用(Jetpack 中的协程、Retofit中使用协程)](https://blog.csdn.net/knight1996/article/details/102492883)
[kotlin协程-Android实战 ](https://juejin.im/post/5d74ad56e51d456201486eab)
[Kotlin Primer·第七章·协程库](https://www.kymjs.com/code/2017/11/24/01/)
[Kotlin协程学习](https://www.dazhuanlan.com/?s=Kotlin%E5%8D%8F%E7%A8%8B%E5%AD%A6%E4%B9%A0)
[Kotlin Coroutines基础和原理初探](http://mouxuejie.com/blog/2019-05-23/kotlin-coroutines-basic/)
[kotlin极简教程](https://www.bookstack.cn/read/EasyKotlin/spilt.1.ch9.md)
[](https://blog.csdn.net/c10wtiybq1ye3/article/details/103640848)
[Kotlin协程用法及解析](https://ljd1996.github.io/2020/10/12/Kotlin%E5%8D%8F%E7%A8%8B%E7%94%A8%E6%B3%95%E5%8F%8A%E8%A7%A3%E6%9E%90/)
[即学即用Kotlin - 协程](https://juejin.cn/post/6854573211418361864#heading-11)
[抽丝剥茧Kotlin - 协程](https://juejin.cn/post/6862548590092140558)
[抽丝剥茧Kotlin - 协程中绕不过的Flow](https://juejin.cn/post/6914802148614242312)
[Kotlin 协程 的实战](https://juejin.cn/post/6844904022407643144)
[Kotlin Flow场景化学习](https://onlyloveyd.blog.csdn.net/article/details/112750914)
[破解 Kotlin 协程(4) - 异常处理篇](https://zhuanlan.zhihu.com/p/64331148)
[枯燥的Kotlin协程三部曲(上)——概念启蒙篇](https://juejin.cn/post/6854573213704912910)
[枯燥的Kotlin协程三部曲(中)——应用实战篇](https://juejin.cn/post/6860464281272451080)


