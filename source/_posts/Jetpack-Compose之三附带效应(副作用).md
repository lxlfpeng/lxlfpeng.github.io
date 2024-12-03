---
title: Jetpack-Compose之三附带效应(副作用)
---

# 一.Compose组合函数的特点
### 1.Compose组合函数执行顺序不定
可组合函数并不是按顺序执行的，这些函数可以按任何顺序运行(Compose 可以选择识别出某些界面元素的优先级高于其他界面元素，因而首先绘制这些元素)。
```
@Composable
fun Row() {
   StartScreen()
   MiddleScreen()
   EndScreen()
}
```
对 StartScreen、MiddleScreen 和 EndScreen 这三个组合函数的调用不是按顺序进行的。 所以不能在Row中设置一个全局变量，让 StartScreen()修改这个变量的值，并让 MiddleScreen() 利用这个全局变量的值进行更改，每个组合函数都应该保持独立。

### 2.Compose可组合函数可以并行运行
Compose 可以通过并行运行可组合函数来优化重组。这样Compose 就可以利用多个核心，并以较低的优先级运行可组合函数（不在屏幕上）。 这种优化意味着，可组合函数可能会在后台线程池中执行。如果某个可组合函数对 ViewModel 调用一个函数，则 Compose 可能会同时从多个线程调用该函数。

### 3.可组合函数可能会非常频繁地运行
在某些情况，可组合函数可能会进行非常频繁的重组，例如执行动画时，每一帧的动画都会导致可组合函数进行重组， 如果在该组合函数中进行高昂的操作，例如读取设备信息，可能会造成界面卡顿（因为组合函数不断的重组，可能会在一秒内读取设备信息数百次，最终导致应用崩溃）。 该问题的解决方法是把相应的数据作为传入参数传给可组合函数，或者把高昂的操作移交给其他线程，再或者使用`mutableStateOf`或 `LiveData`将值结果作为参数传递给可组合函数。

# 二.纯函数和副作用
### 1.纯函数
纯函数指的是函数与外界交换数据只能通过函数参数和函数返回值来进行；函数从函数外部接受的所有输入信息都通过参数传递到该函数内部；函数输出到函数外部的所有信息都通过返回值传递到该函数外部。纯函数的运行是不会对外界的环境产生任何的影响，给一个纯函数同样的参数，那么这个函数永远返回同样的值，调用一个纯函数，不会导致任何状态的变化，也就不会影响后来的该函数调用。。
例如以下就是一个纯函数:
```
public int add(int a,int b){
    return a+b;
}
```

### 2.副作用(附带效应)
"副作用"（side effect），指的是如果一个操作、函数或表达式在其内部与外界进行了互动（最典型的情况，就是修改了外部环境的变量值），产生运算以外的其他结果，则该操作、函数或表达式具有副作用。相对的纯函数就是没有副作用的函数。
例如以下就是带有副作用的函数:
```
int a;
public int add(int b){
    return a+b;
}
```
>用一句话概括副作用：一个函数的执行过程中，除了返回函数值之外，对调用方还会带来其他附加影响，例如修改全局变量或修改参数等。

### 3.处理副作用(附带效应)
Compose这类的声明式UI框架都是通过函数（组件）的反复执行来渲染UI的，函数执行的时机和次数都不可控，但是函数的执行结果必须可控，因此，要求这些函数组件用纯函数实现。虽然我们不希望函数执行中出现副作用，但现实情况是有一些逻辑只能作为副作用来处理。例如一些IO操作、计时、日志埋点等，这些都是会对外界或收到外界影响的逻辑，不能无限制的反复执行。所以Compose等框架需要能够合理地处理一些副作用：

- 副作用的执行时机是明确的，例如在Recomposition时等。
- 副作用的执行次数是可控的，不应该随着函数反复执行。
- 副作用不会造成泄露，例如对于注册要提供适当的时机取消注册。

>函数式编程强调没有"副作用"，意味着函数要保持独立，所有功能就是返回一个新的值，没有其他行为，尤其是不得修改外部变量的值。

# 三.Compose组合函数中的副作用 (side-effect)
在上面讲过，Compose中不能有任何的附带效应，附带效应容易让应用产生未知的错误。这里的附带效应也就是一些逻辑操作，在Compose中可组合函数内部理应只做视图相关的事情，而不应该做函数返回之外的事情，如访问文件等，如果有，那这就叫做附带效应，也就是在可组合函数范围之外发生的应用状态变化。
例如，以下操作全部都是危险的附带效应：
- 写入共享对象的属性。
- 更新 ViewModel 中的可观察项。
- 更新共享偏好设置。

可组合函数应该是无副作用的，如果你需要在可组合函数中产生附带效应(例如改变APP的状态)，需要使用EffectAPI，以便以可预测的方式执行那些副作用。一个effect，就是一个可组合函数，这个可组合函数不生成UI，而是在组合完成时产生副作用。 其提供的有：LaunchedEffect、rememberCoroutineScope和DisposableEffect、SideEffect等操作的API，这些APIs很容易被滥用，所以使用时确保不会破坏Compose的数据单向流动性

# 四.Compose组合函数的生命周期
可组合项的生命周期比视图比activity 和 fragment 的生命周期更简单，一般是进入组合、执行0次或者多次重组、退出组合。
![](/images/c9debefa923799713145cb0760fb0779.webp)

- Enter：挂载到树上，首次显示。
- Composition：重组刷新UI。
- Leave：从树上移除，不再显示。
  使用@Composable修饰的可组合函数中没有自带的生命周期函数，想要监听其生命周期，需要使用Effect(附带效应) API:
- LaunchedEffect：第一次调用Compose函数的时候调用。
- DisposableEffect：内部有一个 onDispose()函数，当页面退出时调用。
- SideEffect：compose函数每次执行都会调用该方法。
>Composalbe中引入生命周期，便于处理那些非纯函数的逻辑（不能跟随重组反复执行的逻辑），Compose 提供了Effect(附带效应) API 等函数来处理这些逻辑。 Composalbe 越接近纯函数越利于复用，所以SideEffect、LaunchedEffect等副作用函数越少越好，推荐尽量移动到 ViewModel 中处理。

# 五.Compose中常见的Side-effects
### 1.LaunchedEffect
##### LaunchedEffect简介
如果在composable函数中使用耗时函数做耗时的操作，就需要将这个耗时函数放入coroutine(协程)中执行，而coroutine(协程)需要在CoroutineScope中创建，因此谷歌提供了LaunchedEffect用于创建coroutine。当LaunchedEffect进入一个可组合函数时，它会启动一个协程，协程执行的代码块作为它的参数被传入。如果这个LaunchedEffect离开了Composition，它启动的协程会被取消。

##### LaunchedEffect源码
```
@Composable
@ComposableContract(restartable = false)
fun LaunchedEffect(
    subject: Any?,
    block: suspend CoroutineScope.() -> Unit
) {
    val applyContext = currentComposer.applyCoroutineContext
    remember(subject) { LaunchedEffectImpl(applyContext, block) }
}
```
实现非常简单，使用remember保存了subject参数，然后通过LaunchedEffectImpl启动协程
```
internal class LaunchedEffectImpl(
    parentCoroutineContext: CoroutineContext,
    private val task: suspend CoroutineScope.() -> Unit
) : CompositionLifecycleObserver {

    private val scope = CoroutineScope(parentCoroutineContext)
    private var job: Job? = null

    override fun onEnter() {
        job?.cancel("Old job was still running!")
        job = scope.launch(block = task)
    }

    override fun onLeave() {
        job?.cancel()
        job = null
    }
}
```
LaunchedEffectImpl可以提供CoroutineScope，借助CompositionLifecycleObserver提供的生命周期，进入屏幕时launch启动协程，离开屏幕时cancel取消协程。

##### LaunchedEffect特点
- 当LaunchedEffect进入Composition时，会启动一个coroutine，并将LaunchedEffect后括号中的代码放入该coroutine中执行。
- 当Composable从视图树上detach时，该coroutine还未被执行完毕，该coroutine也会被取消执行。
- 当LaunchedEffect在recompose(重组)时其key不变，那LaunchedEffect不会被重新启动执行block。
- 当LaunchedEffect在recompose(重组)时其key发生了变化，则LaunchedEffect会执行cancel后，再重新启动一个新协程执行block。

##### LaunchedEffect使用示例
1. 在首次启动时显示开屏页。参数Unit，因为不会有diff，所以实现onActive的生命周期效果，也就是仅仅在首次composition时执行一次
```
@Composable
fun SplashScreen(
    onTimeOut: () -> Unit
) {
    LaunchedEffect(Unit) { 
        delay(SplashWaitTime)
        onTimeOut()
    }
    ...
}
```
2. 当检索词变化时，发起检索。
```
@Composable
fun SearchScreen() {
    ...
    var searchQuery by remember { mutableStateOf("") }
    LaunchedEffect(searchQuery) {
        // execute search and receive result
         apiService.searchQuery(searchQuery.value)
    }
    ...
}
```

>让Composable支持协程的重要意义是，可以让一些简单的业务逻辑直接Composable的形式封装并实现复用，而无需额外借助ViewModel。


### 2.rememberCoroutineScope
##### rememberCoroutineScope简介
由于 LaunchedEffect 是可组合函数，因此只能在其他可组合函数中使用。想要在可组合项外启动协程，且需要对这个协程存在作用域限制，以便协程在退出组合后自动取消，可以使用 rememberCoroutineScope，此外，如果您需要手动控制一个或多个协程的生命周期，请使用 rememberCoroutineScope，例如在用户事件发生时取消动画。
##### rememberCoroutineScope实现原理
```
@Composable
inline fun rememberCoroutineScope(
    getContext: @DisallowComposableCalls () -> CoroutineContext = { EmptyCoroutineContext }
): CoroutineScope {
    val composer = currentComposer
    val wrapper = remember {
        CompositionScopedCoroutineScopeCanceller(
            createCompositionCoroutineScope(getContext(), composer)
        )
    }
    return wrapper.coroutineScope
}
```

##### rememberCoroutineScope特点如下：
- rememberCoroutineScope可以返回一个coroutineScope，便于开发者手动控制该coroutine的生命周期，例如:用户点击事件时启动该coroutine。
- rememberCoroutineScope返回的coroutineScope会和其调用点的生命周期保持一致，当调用点所在的Composition退出时，该coroutineScope会被取消。
##### rememberCoroutineScope使用示例
以下是使用rememberCoroutineScope的一个示例，当用户点击按钮时，程序会显示Snackbar，当MoviesScreen被重视图树上移除时协程也随之被取消执行:
```
@Composable
fun MoviesScreen(scaffoldState: ScaffoldState = rememberScaffoldState()) {
    // 创建一个绑定到 MoviesScreen 生命周期的 CoroutineScope
    val scope = rememberCoroutineScope()
    
    Scaffold(scaffoldState = scaffoldState) {
        Column {
            /* ... */
            Button(
                onClick = {
                    // 在事件处理程序中创建一个新的协程以显示一个Snackbar
                    scope.launch {
                        scaffoldState.snackbarHostState.showSnackbar("Something happened!")
                    }
                }
            ) {
                Text("Press me")
            }
        }
    }
}
```
rememberCoroutineScope 是一个可组合函数，它能直接返回一个CoroutineScope，该协程作用域的生命周期与rememberCoroutineScope的调用点绑定，当这个调用点退出组合(Composition)时，该协程作用域自动被取消。这个函数能允许开发者在可组合函数中自定义协程作用域，并手动管理它们的生命周期。
>rememberCoroutineScope常用于开发者需要在回调事件中需要控制coroutine的场景。

### 3.rememberUpdatedState
##### rememberUpdatedState简介
如果key值有更新，那么LaunchedEffect在recompose(重组)时就会被重新启动。但是有时候，你需要在LaunchedEffect中使用最新的参数值，但是又不想重新启动LaunchedEffect， 此时就需要用到rememberUpdatedState。rememberUpdatedState的作用是给某个参数创建一个引用，来跟踪这些参数，并保证其值被使用时是最新值，参数被改变时不重启effect。

##### rememberUpdatedState源码
```
@Composable
fun <T> rememberUpdatedState(newValue: T): State<T> = remember {
    mutableStateOf(newValue)
}.apply { value = newValue }
```

##### rememberUpdatedState特点
- rememberUpdatedState保存某个参数或者状态的最新值，当被调用的时候，返回已保存的最新值。

##### rememberUpdatedState示例
例如应用有一个LandingScreen需要在一段时间后自动消失。LandingScreen内部启动了一个LaunchedEffect来记录这个时间， 那么即使LandingScreen发生了重组(recomposition)，这个LaunchedEffect也不应该被重启。
```
@Composable
fun LandingScreen(onTimeout: () -> Unit) {
    val currentOnTimeout by rememberUpdatedState(onTimeout)

    LaunchedEffect(true) {
        delay(SplashWaitTimeMillis)
        currentOnTimeout()
    }

    /* Landing 页面内容 */
}
```
>这个例子中，onTimeout是计时结束时的回调函数，delay是计时函数。假设计时2分钟，初始化时，currentOnTimeout作为一个指向onTimeout的引用，而LaunchedEffect启动了一个协程，协程遇到挂起函数delay，开始一直等待。 假设到第1分钟时，用户做了一个操作，LandingScreen的入参onTimeout被更改了，那么LandingScreen发生recoposition，此时currentOnTimeout也随之被更新为最新的值。但是rememberUpdatedState函数的效果，使得虽然currenOnTimeout改变了，也就是LaunchedEffect的入参变化了，但LaunchedEffect却不会发生recomposition。所以delay函数也不会被取消，计时正常进行。

为创建与调用点的生命周期相匹配的效应，永不发生变化的常量（如 Unit 或 true）将作为参数传递,在以上代码中，使用 LaunchedEffect(true)。 为了确保 onTimeout lambda 始终包含重组 LandingScreen 时使用的最新值，onTimeout 需使用 rememberUpdatedState 函数封装。 Effect中应使用代码中返回的 State、currentOnTimeout。


### 4.DisposableEffect
##### DisposableEffect简介
DisposableEffect也是一个可组合函数，当 DisposableEffect 在其key值变化或者composable函数离开Composition时，会取消之前启动的协程， 并会在取消协程前调用其回收方法进行资源回收相关的操作， 可以对一些资源等进行清理。如果您只想在输入合成时运行一次效果，并在离开时将其释放，则可以传递一个常量作为键：DisposableEffect(true)或者DisposableEffect(Unit)。

##### DisposableEffect源码
```
@Composable
@NonRestartableComposable
fun DisposableEffect(
    key1: Any?,
    effect: DisposableEffectScope.() -> DisposableEffectResult
) {
    remember(key1) { DisposableEffectImpl(effect) }
}
```

##### DisposableEffect特点
- 当DisposableEffect的key值变化时，当前Effect的onDispose会被调用，此时可以在此函数中对资源进行清理；同时DisposableEffect会被重启，此时可以重新申请资源等。
- DisposableEffect中必须包含onDispose语句，否则IDE会出现编译时错误。

##### DisposableEffect示例
例如，您可能需要使用 LifecycleObserver，根据 Lifecycle 事件发送分析事件。如需在 Compose 中监听这些事件，请根据需要使用 DisposableEffect 注册和取消注册观察器。
```
@Composable
fun HomeScreen(
    lifecycleOwner: LifecycleOwner = LocalLifecycleOwner.current,
    onStart: () -> Unit, // Send the 'started' analytics event
    onStop: () -> Unit // Send the 'stopped' analytics event
) {
    // Safely update the current lambdas when a new one is provided
    val currentOnStart by rememberUpdatedState(onStart)
    val currentOnStop by rememberUpdatedState(onStop)

    // If `lifecycleOwner` changes, dispose and reset the effect
    DisposableEffect(lifecycleOwner) {
        // Create an observer that triggers our remembered callbacks
        // for sending analytics events
        val observer = LifecycleEventObserver { _, event ->
            if (event == Lifecycle.Event.ON_START) {
                currentOnStart()
            } else if (event == Lifecycle.Event.ON_STOP) {
                currentOnStop()
            }
        }

        // Add the observer to the lifecycle
        lifecycleOwner.lifecycle.addObserver(observer)

        // When the effect leaves the Composition, remove the observer
        onDispose {
            lifecycleOwner.lifecycle.removeObserver(observer)
        }
    }

    /* Home screen content */
}
```
在上面的代码中，效应将 observer 添加到 lifecycleOwner。如果 lifecycleOwner 发生变化，系统会通过 lifecycleOwner 处理并再次重启效应。

### 5.SideEffect
##### SideEffect简介
SideEffect是简化版的DisposableEffect， SideEffect 并未接收任何 key 值，所以，每次recomposition(重组)，就会执行其 block。当不需要onDispose、不需要参数控制（即每次onCommit都执行）时使用SideEffect。SideEffect主要用来与非 Compose 管理的对象共享 Compose 状态。

##### SideEffect源码
```
@Composable
@NonRestartableComposable
@OptIn(InternalComposeApi::class)
fun SideEffect(
    effect: () -> Unit
) {
    currentComposer.recordSideEffect(effect)
}

```

##### SideEffect特点
- 在Composition操作失败时，能保证SideEffect中的非Compose管理对象的状态和Composition中的状态一致。
- SideEffect在组合函数被创建并载入视图树后才会被调用。

##### SideEffect示例
例如，您的分析库可能允许您通过将自定义元数据（在此示例中为“用户属性”）附加到所有后续分析事件，来细分用户群体。如需将当前用户的用户类型传递给您的分析库，请使用 SideEffect 更新其值。
```
@Composable
fun rememberAnalytics(user: User): FirebaseAnalytics {
    val analytics: FirebaseAnalytics = remember {
        /* ... */
    }

    // On every successful composition, update FirebaseAnalytics with
    // the userType from the current User, ensuring that future analytics
    // events have this metadata attached
    SideEffect {
        analytics.setUserProperty("userType", user.userType)
    }
    return analytics
}
```

### 6.produceState
##### produceState简介
produceState可以将非 Compose （如 Flow、LiveData 或 RxJava）状态转换为 Compose 状态，可以让该数据是在Composition中使用。它接收一个lambda表达式作为函数体，能将这些入参经过一些操作后生成一个State类型变量并返回。比如有些地方需要一些state值来对UI进行重组，但是这些状态的来源却并没有生产状态，可以使用这个进行转换。
>注意:produceState 创建了一个协程，它也可用于观察非挂起的数据源。如需移除对该数据源的订阅，请使用 awaitDispose 函数。

##### produceState源码
```
@Composable
fun <T> produceState(
    initialValue: T,
    key1: Any?,
    key2: Any?,
    @BuilderInference producer: suspend ProduceStateScope<T>.() -> Unit
): State<T> {
    val result = remember { mutableStateOf(initialValue) }
    LaunchedEffect(key1, key2) {
        ProduceStateScopeImpl(result, coroutineContext).producer()
    }
    return result
}
```

##### produceState特点
- 当produceState进入Composition时，获取数据的任务被启动，当其离开Composition时，该任务被取消。
- 尽管produceState创建了一个协程，它也可以用于获取non-suspending数据源。

##### produceState示例
以下示例展示了如何利用produceState从网络加载一张图片。loadNetworkImage这个函数返回了一个State，这个State可以被用于其他composable函数。
```
@Composable
fun loadNetworkImage(
    url: String,
    imageRepository: ImageRepository
): State<Result<Image>> {
    
    //创建带有结果的状态<T>。Loading作为初始值加载
    //如果“url”或“imageRepository”更改，则运行生产者
    //将取消并使用新的输入重新启动。
    return produceState<Result<Image>>(initialValue = Result.Loading, url, imageRepository) {

        //在协程中，可以进行挂起调用
        val image = imageRepository.load(url)

        //使用错误或成功结果更新状态。
        //这将触发读取此状态的重组
        value = if (image == null) {
            Result.Error
        } else {
            Result.Success(image)
        }
    }
}
```

### 7.derivedStateOf
##### derivedStateOf简介
如果某个状态是从其他状态对象计算或派生得出的，请使用 derivedStateOf。使用此函数可确保仅当计算中使用的状态之一发生变化时才会进行计算。当一个状态由另外几个状态计算或者推导得到时，使用derivedStateOf来记录结果状态，此时作为条件的状态我们称为条件状态。当任意一个条件状态更新时，结果状态都会重新计算。

##### derivedStateOf源码
```
fun <T> derivedStateOf(calculation: () -> T): State<T> = DerivedSnapshotState(calculation)
```

##### derivedStateOf示例
以下示例展示了基本的“待办事项”列表，其中具有用户定义的高优先级关键字的任务将首先显示：
```
@Composable
fun TodoList(highPriorityKeywords: List<String> = listOf("Review", "Unblock", "Compose")) {

    val todoTasks = remember { mutableStateListOf<String>() }

    // Calculate high priority tasks only when the todoTasks or highPriorityKeywords(只有当 todoTasks 或 highPriorityKeywords 时才计算高优先级任务)
    // change, not on every recomposition(改变，而不是每次重组)
    val highPriorityTasks by remember {
        derivedStateOf { todoTasks.filter { it.containsWord(highPriorityKeywords) } }
    }

    Box(Modifier.fillMaxSize()) {
        LazyColumn {
            items(highPriorityTasks) { /* ... */ }
            items(todoTasks) { /* ... */ }
        }
        /* Rest of the UI where users can add elements to the list */
    }
}
```
在以上代码中，derivedStateOf 保证每当 todoTasks 或 highPriorityKeywords 发生变化时，系统都会执行 highPriorityTasks 计算，并相应地更新界面。由于执行过滤以计算 highPriorityTasks 的成本很高，因此应仅在任何列表更改时执行，而不是在每次重组时执行。此外，更新 derivedStateOf 生成的状态不会导致可组合项在声明它的位置重组，Compose 仅对其返回状态为已读的可组合项（在本例中，指 LazyColumn 中的可组合项）进行重组。

### 8.snapshotFlow
##### snapshotFlow简介
使用 snapshotFlow 可以将 State<T> 对象转换为冷 Flow。snapshotFlow 会在收集到块时运行该块，并发出从块中读取的 State 对象的结果。 当在 snapshotFlow 块中读取的 State 对象之一发生变化时，如果新值与之前发出的值不相等，Flow 会向其收集器发出新值（此行为类似于 Flow.distinctUntilChanged 的行为）。

##### snapshotFlow源码
```
fun <T> snapshotFlow(
    block: () -> T
): Flow<T> = flow {
    ...
}
```

##### snapshotFlow示例
下列示例显示了一项附带效应，是系统在用户滚动经过要分析的列表的首个项目时记录下来的：
```
val listState = rememberLazyListState()

LazyColumn(state = listState) {
    // ...
}

LaunchedEffect(listState) {
    snapshotFlow { listState.firstVisibleItemIndex }
        .map { index -> index > 0 }
        .distinctUntilChanged()
        .filter { it == true }
        .collect {
            MyAnalyticsService.sendScrolledPastFirstItemEvent()
        }
}
```
在上方代码中，listState.firstVisibleItemIndex 被转换为一个 Flow，从而可以受益于 Flow 运算符的强大功能。

# 六.重启效应
上文中提到Compose 中有一些effect（如 LaunchedEffect、produceState 或 DisposableEffect）会采用可变数量的参数和键来取消运行effect，并使用新的键启动一个新的effect。
这些 API 的简化形式是：
```
EffectName(restartIfThisKeyChanges, orThisKey, orThisKey, ...) { block }
```
由于此行为的细微差别，如果用于重启效应的参数不是适当的参数，可能会出现问题：
- 重启次数少于预期
- 重启次数多余预期
  一般来说， effect代码块中使用的所有可变和不可变变量，都应该作为参数传递到effect可组合项中。如果更改某些变量不需要导致effect重启，则应将该变量封装在 rememberUpdatedState 中。这些参数中，如果某个参数用remember包裹，且没有任何key，说明该变量永远不会改变，则无需将变量作为键传递给effect。

>要点：应将效应中使用的变量添加为效应可组合项的参数，或使用 rememberUpdatedState。

下例 DisposableEffect 代码中，效应将其块中使用的 lifecycleOwner 作为参数，因为对它们的任何更改都会导致效应重启。
```
@Composable
fun HomeScreen(
lifecycleOwner: LifecycleOwner = LocalLifecycleOwner.current,
onStart: () -> Unit, // Send the 'started' analytics event
onStop: () -> Unit // Send the 'stopped' analytics event
) {
// These values never change in Composition
val currentOnStart by rememberUpdatedState(onStart)
val currentOnStop by rememberUpdatedState(onStop)

    DisposableEffect(lifecycleOwner) {
        val observer = LifecycleEventObserver { _, event ->
            /* ... */
        }

        lifecycleOwner.lifecycle.addObserver(observer)
        onDispose {
            lifecycleOwner.lifecycle.removeObserver(observer)
        }
    }
}
```
无需使用 currentOnStart 和 currentOnStop 作为 DisposableEffect 键，因为它的值绝不会因使用了 rememberUpdatedState 而在组合中发生变化。如果未将 lifecycleOwner 作为参数传递，并且该代码发生变化，那么 HomeScreen 将重组，但 DisposableEffect 不会进行处理和重启。这会导致出现问题，因为此后会使用错误的 lifecycleOwner。

### 1.使用常量作为键
您可以使用 true 等常量作为效应键，使其遵循调用点的生命周期。它实际上具有有效的用例，如上面所示的 LaunchedEffect 示例。但在这样做之前，请审慎考虑，并确保您确实需要这么做。

参考资料:
[Google官方文档](https://developer.android.google.cn/jetpack/compose/side-effects?authuser=0)
[学不动也要学，Jetpack Compose 写一个 IM APP](https://juejin.cn/post/6991429231821684773)
[学不动也要学，Jetpack Compose 写一个 IM APP（二）](https://juejin.cn/post/7028397244894330917#heading-4)
[Compose的附加效应(十四)](https://blog.csdn.net/Mr_Tony/article/details/118941147)
[Jetpack Compose Side Effect：如何处理副作用](https://juejin.cn/post/6930785944580653070)
[对Jetpack Compose设计的初步解读与思考](https://www.jianshu.com/p/7bff0964c767)
[Android Compose的重组中的一段话的理解](https://blog.csdn.net/qq_41899289/article/details/120308504)
[Compose系列 五 副作用 side-effect](https://blog.csdn.net/ljjliujunjie123/article/details/121426028)
[Compose 1.0 将于7月正式发布，还不了解一下？](https://blog.csdn.net/vitaviva/article/details/117264223)
[Compose基础--Side-effect（一）](https://blog.csdn.net/zuoluohust/article/details/120652589)
[Compose基础--Side-effect（二）](https://blog.csdn.net/zuoluohust/article/details/122200728)
[Jetpack Compose 核心概念（一）](https://www.jianshu.com/p/0fc597eeaa93)