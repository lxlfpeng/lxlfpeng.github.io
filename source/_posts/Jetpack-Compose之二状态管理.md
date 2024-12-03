---
title: Jetpack-Compose之二状态管理
---

# 一.Compose状态管理绪论
状态是什么?状态指的是Ui的形态，例如按钮控件的文字、颜色的状态等等，在软件编程中我们会用一个状态值去保存该状态。传统的Android视图层次结构中，界面是通过一个个的View， 例如:ImageView、TextView等搭建而成，然后通过findViewById找到对应的View的引用后，设置它的内部状态值，例如设置TextView的文本，当UI的状态值改变时，基于XML的UI框架会自动刷新UI来显示正确的状态。Compose 是声明式的 UI，在组合函数中这些状态值描述了这个UI组件的状态，所以想更改一个UI的状态，只能用``新的状态值去重新调用该组件的可组合函数``，状态值的更新就对应着重组(重绘)的发生(刷新该UI)。 也就是说Compose 主要是根据状态的改变进行重组的，实际上Compose的UI变化本质是："状态(State) 驱动"，即控件UI的变化原因是控件UI的状态发生了变化，需要加入状态并对相关的状态进行管理。

**对状态变化做出反应是 Compose 的核心。Compose 应用程序通过调用 Composable 函数将数据转换为 UI。如果您的数据发生变化，您可以使用新数据调用这些函数，从而创建更新的 UI。Compose 提供了用于观察应用程序数据变化的工具，这些工具会自动调用您的函数——这称为重构。Compose 还会查看单个可组合组件需要哪些数据，以便它只需要重新组合数据已更改的组件，并且可以跳过组合未受影响的组件。 在底层，Compose 使用自定义 Kotlin 编译器插件，因此当底层数据发生变化时，可以重新调用可组合函数以更新 UI 层次结构。 例如，当你调用Greeting("Android")的MyScreenContent可组合的功能，你是硬编码的输入("Android")，所以Greeting将添加到UI树一次，永远不会改变，即使身体MyScreenContent被重构。 要将内部状态添加到可组合，请使用该mutableStateOf函数，它提供可组合的可变内存。为了不让每次重组都有不同的状态，请记住使用remember. 而且，如果在屏幕上的不同位置有多个可组合实例，每个副本将获得自己的状态版本。您可以将内部状态视为类中的私有变量。 可组合函数将自动订阅它。如果状态发生变化，读取这些字段的可组合项将被重新组合。**
[节选自](https://blog.csdn.net/Mr_Tony/article/details/118858756)

# 二.Compose重组(Recomposition)
### 1.什么是Compose重组(Recomposition)
在命令式界面模型中，如需更改某个控件的状态，可以在该控件上调用 setter()等方法通过改变其属性来更改其内部状态。 在 Compose 中，可以使用新数据再次调用可组合函数，这样就会导致可组合函数进行重组(重绘)，系统会根据新数据重新调用绘制函数绘制出新的UI。简单来说重组实际上就是当状态值改变后，再次调用可组合函数进行的绘制过程，是否重组的判断条件是与 @Composable 元素绑定的数据是否发生了变化。

### 2.Compose智能重组
上文说到当状态变化时需要再次调用可组合函数触发UI重组，但是如果是一个很庞大的 Composable 层级结构，当只针对于层级中的某一部分发生改变时，不可能对该层级中所有的UI都进行重组，这样会带来很多多余的性能损耗。因此仅仅只需要针对依赖该状态的UI元素进行重组生成新的UI即可，与状态修改无关的UI元素，让其保持之前生成的实例。Compose 为了保证重组性能引入了"局部重组，也叫智能重组":Compose 编译器会在 @Composable 元素初始化的时候，对每一个元素做标记，当关联状态变化时，然后根据状态是否修改来智能的选择需要被重组的元素。

重组需要注意的地方:
- 重组意味着系统会重新调用 @Composable 元素方法的执行，而重组可能会随时且非常频繁的发生，所有的 @Composable 组合函数的执行都是乱序和并行的。
- 应避免修改可组合 lambda 中的变量的代码，因为此类代码并非线程安全代码，而且可能被多次调用应该禁止此类变量的写入操作。
- 可能在重组过程中，Local 变量可能会失效，动态计算方法会调用很多次。

### 3.Compose重组的最小范围
在Compose中重组的范围主要受两种因素影响:
- 只有会受到 state 变化影响的代码块才会参与到重组，不依赖 state 的代码不参与重组。
- 只有非inline函数才有资格成为重组的最小范围， 这是因为Compose 在编译期分析出会受到某 state 变化影响的代码块，并记录其引用，当此 state 变化时，会根据引用找到这些代码块并标记为 Invalid。在下一渲染帧到来之前 Compose 会触发 recomposition，并在重组过程中执行 invalid 代码块。

### 4.Compose重组是乐观的操作
只要Compose认为可组合项中的数据或状态发生了改变，就会开始重组。重组是个乐观的操作，所以Compose会预计在下一次改变发生前完成重组。但是如果在重组完成前再次发生变化时，Compose会取消当前的重组，并使用新数据重新开始重组。 并且取消重组后，Compose 会从重组中舍弃界面树。如有任何附带效应依赖于显示的界面，那么即使取消了组成操作，也会应用该附带效应。这可能会导致应用状态不一致。需要确保所有可组合函数和 lambda 都幂等且没有附带效应，以处理乐观的重组。

# 三.在Compose重组中保存状态值(remember)
上文说到Compose声明式UI不像以前可以通过setText会自动更新UI，它需要向可组合函数传入新的状态值来触发重组，从而生成新的UI。Compose提供了remember，remember的作用是将该状态存储在 Composition 中，当重组发生的时候会自动丢弃原先的对象转而使用改变状态后的值。remember 既可用于存储可变对象，又可用于存储不可变对象。remember 会将对象存储在组合中，当调用 remember 的可组合项从组合中移除后，它会忘记该对象。
>虽然 remember 可帮助您在重组后保持状态，但不会帮助您在配置例如旋转屏幕等情况更改后保持状态。在这种情况下，必须使用 rememberSaveable。rememberSaveable 会自动保存可保存在 Bundle 中的任何值。对于其他值，您可以将其传入自定义 Saver 对象。

# 四.在Compose中创建可观察的状态(MutableState)
在Compose实际编程中，当数据发生变更后，怎么去通知刷新界面?Compose通过可观察的状态，来触发可组合函数的重组。Compose将状态的显示与状态的存储和更改解耦，通过观察者模式来驱动界面变化。
mutableStateOf 会创建可观察的 MutableState<T>:
```
interface MutableState<T> : State<T> {
    override var value: T
}
```
value如有任何更改，系统会通知所有订阅了该可观察对象的可组合函数，并触发它们的重组。简单来说就是只要对 MutableState 的 value 进行改变就会引起用到该状态的 composable 方法重组。
例如:
```
var data = remember { mutableStateOf("")}
```
上述代码中data就是一个MutableState对象，每当data.value值发生改变的时候，系统就会重组ui。

在可组合项中声明 MutableState 对象的方法有三种：
- ``val mutableState = remember { mutableStateOf(default) }``
- ``var value by remember { mutableStateOf(default) }``
- ``val (value, setValue) = remember { mutableStateOf(default) }``

这三种写法是等效的，以语法糖的形式针对状态的不同用法提供。

>Compose 的核心内容就是响应 state 状态的改变，Compose 通过调用 Composable 函数可以将 state 展示在 UI 上，Compose 本身也提供了MutableState等工具去观察 state 的变化，从而可以自动地回调重组UI。

MutableState需要结合remember进行使用，remember 将该状态存储在 Composition 中，当重组发生的时候会自动丢弃原先的对象转而使用改变状态后的值。只要对 MutableState 的 value 进行改变就会引起用到该状态的 composable 方法重组。
例如:
```
@Composable
fun Greeting() {
    var info by remember { mutableStateOf("") }
    Column(modifier = Modifier.padding(16.dp)) {
        if (info.isNotEmpty()) {
            Text(text = info)
        }
        OutlinedTextField(
            value = info,
            onValueChange = {
                info = it
            },
            label = { Text("标题") }
        )
    }
}

```
这里的功能很简单，就是在 OutlinedTextField 中用键盘输入的内容如果不为空就能够实时显示在上方，主要是通过 ``var info by remember { mutableStateOf("") }`` 来进行通知改变的，当 变量的值发生了改变的时候，Compose 就会刷新使用到这个变量的组件，对应的组件状态也会发生改变，所以在使用 Compose 的时候只需要更新数据就可以了。

>但是 remember 只能在重组的时候保存状态，一旦其他情况如屏幕旋转等 Configuration 发生改变的时候 remember 就无能为力了，这时候就需要使用 rememberSaveable。只要是 Bundle 类型的数据，rememberSaveable 就能够自动保存。

# 五.使用rememberSaveable保存状态及恢复态
remember可以帮助我们在界面重组的时候保存状态，而rememberSaveable可以帮助我们存储配置更改(重新创建activity或进程)时的状态。使用rememberSaveable来存储UI的状态变量， 可以在activity或进程重新创建、可组合函数的重绘过程中保存状态。
### 1.Parcelize
所有能被添加到Bundle中的数据都会自动保存。如果你想保存一些无法被添加到Bundle中的数据，可以用下列方法：对该对象的类加上注解 @Parcelize。
例如下面的代码定义了一个Persion数据类型实现了Parcelable接口，就可以使用rememberSaveable保存状态:
```
@Parcelize
data class Persion(val name: String, val country: String) : Parcelable

@Composable
fun PersionScreen() {
    var selectedCity = rememberSaveable { mutableStateOf(Persion("zhangsan", "china"))}
}
```

### 2.MapSaver
如果不方便使用@Parcelize，可以用mapSaver自定义转换规则，把一个对象转变成一系列键值对，这些键值对可以存入Bundle
```
data class Persion(val name: String, val country: String)

val PersionSaver = run {
    val nameKey = "Name"
    val countryKey = "Country"
    mapSaver(
        save = { mapOf(nameKey to it.name, countryKey to it.country) },
        restore = { Persion(it[nameKey] as String, it[countryKey] as String) }
    )
}

@Composable
fun PersionScreen() {
    var selectedPersion = rememberSaveable(stateSaver = PersionSaver) {
        mutableStateOf(Persion("zhangsan", "china"))
    }
}
```

### 3.ListSaver
如果不想定义键值，可以用listSaver替代，它默认用索引作为键值
```
data class Persion(val name: String, val country: String)

val PersionSaver = listSaver<City, Any>(
    save = { listOf(it.name, it.country) },
    restore = { Persion(it[0] as String, it[1] as String) }
)

@Composable
fun PersionScreen() {
    var selectedPersion = rememberSaveable(stateSaver = PersionSaver) {
        mutableStateOf(Persion("zhangsan", "china"))
    }
}
```

# 六.Compose支持的其他状态工具(Livedata、Flow、RxJava 转换为状态)
Jetpack Compose并不强制开发者使用``MutableState<T>``来管理状态，它还支持其他类型的可观察对象。 但是在使用这些其他类型的对象时，必须转型为State<T>类型，好让Jetpack Compose能在它们变化时自动给重绘相关组件，例如使用 LiveData 就要在 Composable 方法使用它之前转换成 tate 类型，可以使用``LiveData<T>.observeAsState()``。
常见的可观察对象如:
- [LiveData](https://developer.android.com/reference/kotlin/androidx/compose/runtime/package-summary#(kotlinx.coroutines.flow.StateFlow).collectAsState(kotlin.coroutines.CoroutineContext))
- [Flow](https://developer.android.com/reference/kotlin/androidx/compose/runtime/package-summary)
- [RxJava2](https://developer.android.com/reference/kotlin/androidx/compose/runtime/rxjava2/package-summary)
  这三个框架是安卓常用的三个响应式开发框架，都支持转化为State对象，以 LiveData 举例，如下代码可以转化为一个 State：
```
import androidx.compose.material.Text
import androidx.compose.runtime.livedata.observeAsState

val value: String? by liveData.observeAsState()
Text("Value is $value")
```

>另外，如果你使用的是自定义的可观察类型，可以通过为Jetpack Compose新增一个扩展方法的形式来使用它们。

注意:
- State 类型的变量作为可组合函数的入参后，该变量的改变会自动触发该组件的重绘。
- 如果用其他类型的可观察变量作为入参，比如LiveData，必须先转型为State<T>。你可以用扩展函数来实现这一点，比如LiveData<T>.observeAsState()
- 可变对象不能作为Compose中的状态变量，比如 ArrayList<T> 或 mutableListOf()，在 Compose 中将可变对象(如 ArrayList<T> 或 mutableListOf())用作状态会导致用户在您的应用中看到不正确或陈旧的数据。
- 可变对象并不是可观察的对象，不可观察的可变对象(如 ArrayList<T> 或可变数据类)不能由 Compose 观察，因而 Compose 不能在它们发生变化时触发重组。你可以用State<List<T>>替代，或者干脆用不可变的对象如listOf()。

>建议使用可观察的数据存储器(如 State<List<T>>)和不可变的 listOf()，而不是使用不可观察的可变对象。

# 七.有状态和无状态组合函数
Compose使用 remember 存储内部状态，使可组合函数变成有状态的。 使用 remember、rememberSaveState 方法保存状态的组合项是有状态组合，反之则是无状态组合。也就是说一个UI组合中包含了状态就是有状态组合，如果不包含状态就是无状态组合。
无状态组合:
```
@Composable
fun HelloScreen(){
    Text("Hello Compose!")
}
```
有状态组合:
```
@Composable
fun CounterScreen() {
    var count by remember { mutableStateOf(0) }
    Button(onClick = { count++ }) {
        Text("I've been clicked $count times")
    }
}

```
Compose使用 remember 存储内部状态，使可组合函数变成有状态的。 无状态的可组合函数不持有任何状态变量，例如上面例子中的HelloScreen。上面的例子中，CounterScreen 就是个有状态的可组合函数，其内部持有并自动修改count属性的值。 这在调用者不需要控制组件的状态的情况下非常有用。但是这样的可组合函数不容易复用和测试。解决方法是可以通过状态提升来解决这样的问题。

# 八.状态提升
### 1.可组合函数状态提升
Compose中的状态提升是一种编程范式，指把可组合函数的状态变量提升到它的调用者里，来使该可组合函数本身是无状态的。Compose通用的状态提升方法是将一个状态变量用两个参数替代：
- value: T: 当前要展示的状态变量值。
- onValueChange: (T) -> Unit: 该状态变量发生改变的事件，T是建议的新值。
>当然，Compose并不限制你一定用onValueChange，可以用lambda表达式自定义你需要的事件形式。

状态提升有一些重要的特征
- 单一数据源: 通过提升状态而不是复制状态，可以确保状态来源是唯一的，有助于减少bug
- 封装性: 只有有状态的可组合函数才能修改状态。
- 可共享的: 被提升的状态变量可以同时用于多个可组合函数。比如上例中，我们希望在多个可组合函数中使用name变量。
- 可拦截的: 可组合函数的调用者接收到状态变量的改变这一事件后，可以选择忽略本次事件，或者修改该事件。
- 解耦的: 被提升的状态变量可以存储在任意位置，比如ViewModel中。

如下代码是官方关于状态提升的代码：
```
@Composable
fun HelloScreen() {
    //1.状态  等待事件向上流动修改状态。
    var name by rememberSaveable { mutableStateOf("") }

    HelloContent(name = name, onNameChange = { name = it })
}

@Composable
fun HelloContent(name: String, onNameChange: (String) -> Unit) {
    Column(modifier = Modifier.padding(16.dp)) {
        Text(
            text = "Hello, $name",
            modifier = Modifier.padding(bottom = 8.dp),
            style = MaterialTheme.typography.h5
        )
        OutlinedTextField(
            value = name,
            //2.事件,触发之后向上流动去修改1中的状态
            onValueChange = onNameChange,
            label = { Text("Name") }
        )
    }
}
```
本例代码中 HelloContent 是无状态的，它的状态被提升到了 HelloScreen 中，HelloContent 有name和onNameChange两个参数，name 是状态，通过 HelloScreen 组合项传给 HelloContent而 HelloContent 中发生的更改它也不能自己进行处理，必须将更改传给HelloScreen进行处理并重组界面。 通过状态提升，HelloContent更容易复用和测试，同时和它的状态变量是如何保存的解耦开来。这种解耦意味着当我们修改或者替换HelloScreen时，不用修改HelloContent的实现。

![](https://img-blog.csdnimg.cn/img_convert/9b1891409655e936bf938639e45e661c.png)

以上的逻辑也叫做：状态下降，事件上升。上例中，状态量从HelloScreen流向HelloContent，而事件则反向传递。 遵循这种编程模式，你可以将展示UI的可组合函数与存储状态变量解耦开来。

提升状态的三条原则:
- 状态变量至少被提升到所有使用了该状态变量的可组合函数的最近的调用者处。
- 状态变量应该被提升到它有可能被改变的最高层次。
- 如果两个状态变量会被同一个事件所更改，它们应该被一起提升。

>你可以把状态提升得更高，但最低也不能低于这三条准则，否则就很难维护单向数据流的概念。

### 2.单向数据流
1. `状态(state)`: 任何可以随时间变化的值。
2. `事件(event)`: 通知程序发生了什么事情。
3. `单向数据流模式(unidirectional data flow)`: 指的是向下传递状态，向上传递事件的设计模式。

上文这种状态向下传递，事件向上传递的方式被叫作单向数据流，在 Compose 应用中使用的常见可观察类型包括 State、LiveData、StateFlow、Flow 和 Observable。通过状态订阅``val name  = mutableStateOf("Hello World!")``name.value可以被订阅，值的更新可引起组件重绘。在 Jetpack Compose 中，状态和事件是分开的。状态表示可更改的值，而事件表示有情况发生的通知。通过将状态与事件分开，可以将状态的显示与状态的存储和更改方式解耦。动态的 @Composable 元素由上层传递的数据所控制，交互事件通过 Block 的方式再传回上层，通过在上层更新数据，从而实现 UI 的动态更新。数据传递是自上而下的，交互事件的传递是自下而上的。

按照这种逻辑，如果我们需要用到ViewModel来管理状态，则需要在 ViewModel 中定义可变的数据，同时定义好修改数据的方法，把数据自上而下传递到实际的 UI 中，然后将 UI 的交互事件向上传递，通过执行最上层 ViewModel 中修改数据的方法，更新数据。

参考资料:
[compose资料](https://docs.compose.net.cn/)
[Compose UI官方文档](https://developer.android.com/jetpack/compose/documentation?hl=zh-cn)
[Android全新UI编程 - Jetpack Compose 超详细教程](https://juejin.cn/user/4125023359205742/posts)
[JetPack Compose 之 state](https://www.jianshu.com/p/93d8a384a8a0)
[Jetpack-Compose 学习笔记](https://blog.csdn.net/lbs458499563)
[Jetpack-Compose](https://blog.csdn.net/m0_37667770/article/details/114542808)
[Compose的State(九)](https://blog.csdn.net/Mr_Tony/article/details/118858756)
[Compose系列 三 状态管理](https://blog.csdn.net/ljjliujunjie123/article/details/120935611)
[Android Compose 的使用](https://segmentfault.com/a/1190000041149397)
[JetPack Compose从初探到实战](https://zhuanlan.zhihu.com/p/428047484)
[原创|Android Jetpack Compose 最全上手指南](https://juejin.cn/post/6844903999347359751)
[Android Jetpack Compose 超快速上手指南](https://juejin.cn/post/6877056735018745863)