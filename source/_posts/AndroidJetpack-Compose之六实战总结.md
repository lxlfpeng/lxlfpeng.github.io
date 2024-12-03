---
title: AndroidJetpack-Compose之六实战总结
---

官方推荐将 Composable 函数写在顶级函数，方便以后复用。
# Compose配合ViewModel使用
概述
Compose中ViewModel的使用和Jetpack一致，通常我们构建页面的时候，如果一条数据多个布局都需要使用到的话我们只能在方法的形参中层层传递。但是这样明显是不合理的，会降低代码的可读性。
使用ViewModel可以完美的解决这个问题，Compose中使用ViewModel的话需要引入lifecycle-viewmodel-compose库，获取ViewModel的方式需要用到扩展函数：viewModel()
多个@Composable修饰的函数里面使用viewModel()获取ViewModel可以获取到同一个ViewModel对象，这就是我们能解决问题的根本原因

> 以上所说仅限于同一个导航页中。如果是在不同的导航页中，那么获取到的ViewModel是不同的对象，这一点跟我们不同Activity中获取不同ViewModel是一样的

# 数据流Flow
概述
Compose可以在不导入依赖的情况下使用Flow，用法基本与相同。不过Compose中使用StateFlow不需要我们在协程中开启collect收集数据流，使用的时候直接使用Flow.collectAsState即可获取到StateFlow中的值进行展示。


下面代码使用了MutableStateFlow实现了数据监听，当更新MutableStateFlow值的时候函数会被刷新，然后使用collectAsState即可获取到最新值进行展示。

点击下面的按钮改变值，上面的按钮内容被改变展示效果
```
@Composable
fun useStateFlow() {
    var repository = remember {     Repository()    }
    Column {
        listItem(
            itemData = ItemData(
                title = "点击更改StateFlow的值",
                content = repository.stateFlow.collectAsState().value//获取StateFlow中的值展示
            ), onClick = {
            })
        changeUiWithState(repository)
    }

}

@Composable
fun changeUiWithState(repository: Repository) {
    listItem(itemData = ItemData(title = "点击改变数据"), onClick = {
        repository.increase()//点击数值自增1
    })
}

class Repository {
    val stateFlow = MutableStateFlow("初始值0")
    var count = 0
    fun increase(): Int {
        stateFlow.value = count.toString()//更改StateFlow中的值
        return count++
    }
}
```

# Hilt
初学者可以将Hilt的学习延后，Hilt不是学习Compose的充要条件

hilt的使用和传统开发基本一致，可以查看我的另一篇文章：https://juejin.cn/post/6967148539277213733

# Coil
[coil](https://coil-kt.github.io/coil/README-zh/)是一个图片库，可以用来加载Compose中的远程图片
### 添加依赖
```
implementation "io.coil-kt:coil:1.4.0"
implementation "io.coil-kt:coil-compose:1.4.0"
```

### 基础使用
```
@Composable
fun useCoil() {
    val painter =
        rememberImagePainter(data = "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fb-ssl.duitang.com%2Fuploads%2Fitem%2F201501%2F27%2F20150127103509_KvXhU.jpeg&refer=http%3A%2F%2Fb-ssl.duitang.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1631501719&t=9653a6a5bb4e29505b9b582c770b42ef",
            builder = {
                crossfade(true)
            })
    Image(
        modifier = Modifier
            .size(300.dp)
            .clip(shape = RoundedCornerShape(20.dp)),
        painter = painter,
        contentDescription = ""
    )
}
```

### 占位图
```
Image(painter = rememberImagePainter(
        data = "http://pic-bucket.ws.126.net/photo/0003/2021-11-16/GOTKEOOU00AJ0003NOS.jpg",
        builder = {
            //占位图
            placeholder(R.mipmap.ic_launcher)
        }), contentDescription = null)
```

### transformations
##### 圆形图片
```
Image(painter = rememberImagePainter(
              data = "http://pic-bucket.ws.126.net/photo/0003/2021-11-16/GOTKEOOU00AJ0003NOS.jpg",
              builder = {
              	  //圆形图片
                  transformations(CircleCropTransformation())
              },
         ),
          contentDescription = null)
```

##### 圆角
圆角效果当然也可以使用Modifier.clip()来实现
```
Image(painter = rememberImagePainter(
              data = "http://pic-bucket.ws.126.net/photo/0003/2021-11-16/GOTKEOOU00AJ0003NOS.jpg",
              builder = {
                  //可以单独设置4个角的圆角度
                  transformations(RoundedCornersTransformation(50f,50f,30f,30f))
              },
         ), contentDescription = null)
```

##### 高斯模糊
```
val context = LocalContext.current
    Image(painter = rememberImagePainter(
              data = "http://pic-bucket.ws.126.net/photo/0003/2021-11-16/GOTKEOOU00AJ0003NOS.jpg",
              builder = {
              	  //设置高斯模糊
              	  //context 上下文对象
              	  //10f 模糊的半径，越大越模糊 ，默认10f
              	  //1f 图片缩放，默认1f
                  transformations(BlurTransformation(context,10f,1f))
              },
         ), contentDescription = null)
```

### Transitions
##### 淡入淡出
```
Image(painter = rememberImagePainter(
        data = "http://pic-bucket.ws.126.net/photo/0003/2021-11-16/GOTKEOOU00AJ0003NOS.jpg",
        builder = {
           //淡入淡出效果，可以传入true,默认动画持续时间是100毫秒
           //crossfade(true)
           //也可以直接传入动画时间
           crossfade(1000)
        },
    ), contentDescription = null)
```

### 加载状态监听
```
val painter = rememberImagePainter(data = "http://pic-bucket.ws.126.net/photo/0003/2021-11-16/GOTKEOOU00AJ0003NOS.jpg")
    //图片加载状态
    when(painter.state){
        is ImagePainter.State.Success ->{
            Log.i("Coil","图片加载完成")
        }
        is ImagePainter.State.Loading ->{
            Log.i("Coil","图片加载中....")
        }
        is ImagePainter.State.Error ->{
            Log.i("Coil","图片加载错误")
        }
    }
    Image(painter = painter, contentDescription = null)
```

# Compose动态内容
在可组合函数中可以使用 if 语句来确定是否要显示特定的界面元素,也可以可以使用循环创建界面元素。
```
@Composable
fun ListItem(items: List<Int>) {
    Column {
        for (item in items) {
            if(item%2==0){
                Text("标题")
            }else{
                Text("内容")
            }
        }
    }
}
```

# Compose 中使用livedata 、viewmodel、协程、获取context
livedata转换成compose 的state，使用需要添加compose livedata的依赖
```
@Composable
fun StatisticsPage() {
    val dataList by viewModel.dataList.observeAsState(listOf())
}
```

```
//compose livedata相关
implementation "androidx.compose.runtime:runtime:$compose_version"
implementation "androidx.compose.runtime:runtime-livedata:$compose_version"
```
compose组件中获取context
```
@Composable
fun StatisticsPage() {
    val context = LocalContext.current
}
```
compose组件中获取viewmodel
```
@Composable
fun StatisticsPage() {
    val viewModel: StatisticsViewModel = viewModel()
}
```
compose 中使用协程
```
@Composable
fun StatisticsPage() {
    val scope = rememberCoroutineScope()
    observeAsState函数是LiveData的扩展函数，将LiveData对象转化成State对象。
}
```

# Compose重组最小范围
如下：
```
@Composable
fun ParentComponent(list: List<Data>) {
	Log.d("compose", "render parent")
	ChildComponent(list) 
}

@Composable
fun ChildComponent(list :List<Data>) {
	Box{
		Log.d("compose", "render child")
	}
}
```

由于ChildComponent签名中依赖了list，当list变化引起重绘时的日志如下
```
D/compose: render parent
D/compose: render child
```
如果ChildComponent改为无参函数：
```
@Composable
fun ParentComponent(list: List<Data>) {
	Log.d("compose", "render parent")
	ChildComponent() 
}

@Composable
fun ChildComponent() {
	Box{
		Log.d("compose", "render child")
	}
}
```
```
D/compose: render parent
```
由于对list不再依赖，当list变化引起重绘时child不再重绘

内联组件的重绘
当我们把child直接内联到parent中时：
```
@Composable
fun ParentComponent(list: List<Data>) {
	Log.d("compose", "render parent")
	Box{
		Log.d("compose", "render child")
	}
}
```
```
D/compose: render parent
D/compose: render child
```
虽然Box{ ... }内部没有对list的依赖，但是仍然参与了重绘。

Column、Row、Box甚至是Layout 这类容器类Composable都是inline函数，因此它们只能共享调用方的Scope。

如果你希望缩小重绘范围，提高性能怎么办？如上，自定义非inline函数，使之满足Compose重绘范围最小化条件。

# 状态
应用的状态（State）是指可以随时间变化的任何值，其定义十分宽泛，从函数的入参参数到应用的背景色都包括在内

对于 Android 传统的 View 视图结构来说，控件会直接持有着 State。例如，EditText 的内部就包含一个 CharSequence 类型的全局变量 mText，用于存储 EditText 当前显示的文本。当想要改变文本内容时，就需要通过手动调用 EditText.setText 方法来改变 mText，EditText 也随之刷新，mText 即 EditText 持有的 State

而 Compose 通过组合多个可组合函数来描述整个屏幕状态并以此来绘制屏幕，更新视图的唯一途径就是生成新的入参参数并再次调用可组合函数，新的入参参数就代表想要的屏幕状态，每当 State 更新时就会触发可组合函数进行重组，从而实现 UI 刷新。在这整个过程中，可组合函数并不直接持有 State，而是通过读取 State 来确定自身应该如何显示

副作用与 Lifecycle
我们也可以不借助 ViewModel 直接在 Composalbe 中操作数据。 但是数据操作涉及 IO，不应该跟随重组反复进行，应该被当做副作用（SideEffect） 处理。
```
@Composable
fun ConversationScreen() {
    
    var message = remember { mutableStateOf(emptyList()) } 
    val scope = rememberCoroutineScope()
    
    SideEffect {
        scope.launch {
            message = apiService.getMessage()
        }
    }
    
    MessageLit(messages)
}
```
SideEffect {...} 处理副作用，只在 Composable 首次上树显示时执行一次，不会随重组反复执行；
rememberCoroutineScope() 可以获取与当前 Composalbe 关联的 CoroutieScope，当 Composable 从树上移除时，其中的协程会随之取消。
当副作用用到协程时，也可以直接使用LaunchedEffect，更加方便：
```
//LaunchedEffect中提供了CoroutineScope，可以直接启动协程
LaunchedEffect {
    message = apiService.getMessage()
}
```
# Compose 如何集成到现有项目
对于很多现有的项目，从头开始使用Compose是不现实的，我肯可以根据上面提到的手动修改gradle的方式，使项目支持Compose。
### 在XML中使用
我们可以直接把Compopse作为一个普通View使用
```
<androidx.compose.ui.platform.ComposeView
        android:id="@+id/compose_view"
        android:layout_width="match_parent"
        android:layout_height="match_parent"/>
```
```
findViewById<ComposeView>(R.id.compose_view).setContent {
          ComposeTheme {
              Surface(color = MaterialTheme.colors.background) {
                  Greeting("Android")
              }
          }
      }
```
### Activity、Fragment
作为独立的界面使用Compopse直接使用setContent方法即可。

[Jetpack Compose Image加载网络图片](https://blog.csdn.net/u013710752/article/details/121499769)
[关于Jetpack Compose重绘（Recomposition）的一个坑](https://blog.csdn.net/vitaviva/article/details/113806838)
[Jetpack Compose：理解composable的重组范围（Recomposition Scope）](https://blog.csdn.net/vitaviva/article/details/115605867)