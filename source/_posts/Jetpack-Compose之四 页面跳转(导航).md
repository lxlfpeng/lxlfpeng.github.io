---
title: Jetpack-Compose之四 页面跳转(导航)
---

# 一.Compose页面跳转的方式
### 1.通过Activity进行导航(不推荐)
使用startActivity进行页面跳转，使用intent进行数据传递。每一个Activity承载一个Compose页面，这是Android原生自带的界面跳转方式。

### 2.通过if判断显示界面
声明式compose ui在简单页面可以通过隐藏，显示来实现页面切换。
例如:
```
@Composable
fun App() {
    val context = LocalContext.current
    var isLogin by remember { mutableStateOf(checkLogin(context)) }
    if (isLogin) {
        Home()
    } else {
        Login()
    }
}
```

### 3.Navigation导航库(推荐)
使用单Activity来承载Compose效果非常好，切换页面时可以做到基于view级别。

# 二.使用Navigation-Compose导航库
导航实际上就是页面跳转，因为Compose中每一个@Composable注解标注的方法就可以成为一个视图，所以导航就是用来处理这些视图之间的跳转操作。 Navigation在设计上高度抽象，只负责导航逻辑不关心页面的具体实现，无论是Activity、Fragment甚至是一个已定义View都可以基于Navigation实现导航。当然，Composable也是可以的。
### 1.添加navigation-compose依赖
如果需要使用Navigation组件，必须在应用模块的build.gradle文件中添加一下依赖：
```
dependencies {
  implementation "androidx.navigation:navigation-compose:2.4.0-beta02"
}
```

### 2.NavController导航控制
NavController 是 Navigation 组件的中心 API。此 API 是有状态的，可以跟踪组成应用屏幕的可组合项的返回堆栈以及每个屏幕的状态。在组合项中，它是通过rememberController()方法来创建的。如下：
```
val navController = rememberNavController()
```
为了使所有的组合项都可以访问NavController，需要在组合项层次结构中的适当位置创建它(遵循状态提升的原则)。
NavBackStackEntry存储了导航中回退栈的信息。可以通过以下方式获取:
```
val backstackEntry = navController.currentBackStackEntryAsState()
//获取当前的路由状态
val route = backstackEntry.value?.destination?.route 
```

### 3.创建并关联NavHost
每个NavController都必须与一个NavHost可组合项相关联，NavHost 将 NavController 与导航图相关联导航图用于指定您应能够在其间进行导航的可组合项目的地。在可组合项之间进行导航期间，NavHost的内容会自动进行重组。导航图中的每个可组合项目的地都与一个路线相关联，路线用字符串进行表示,用于定义指向可组合项的路径。
您可以将其视为指向特定目的地的隐式深层链接。每个目的地都应该有一条唯一的路线。如果一条路线用于多个可组合项，则会导航到最后一个设定的可组合项。创建并关联NavHost需要用到rememberNavController创建的NavController和导航图的起始目的地的路线，如下：
```
val navController = rememberNavController()
NavHost(navController = navController, startDestination = "onePage") {
  composable("onePage") { OnePage(/*...*/) }
  composable("twoPage") { TwoPage(/*...*/) }
  composable("thirdPage") { ThirdPage(/*...*/) }
  /*...*/
}
```

### 4.导航（跳转）到可组合项
##### (1.)简单导航
如需导航到导航图中的可组合项目的地，您必须使用 navigate() 方法。navigate() 接受代表目的地路线的单个 String 参数。
```
NavController.navigate("onePage")
```
可以创建FirstPage，SecondPage，ThirdPage组合，然后给它们指定路径进行跳转:
```
@Composable
fun HelloCompose() {
    // 创建NavController
    val navController = rememberNavController()
    // 用NavHost将NavController和导航图相关联，startDestination指定起始的可组合项
    NavHost(navController = navController, startDestination = "first_page") {
        // 给FirstPage可组合项指定路径
        composable("first_page") { FirstPage(navController) }
        // 给SecondPage可组合项指定路径
        composable("second_page") { SecondPage(navController) }
        // 给ThirdPage可组合项指定路径
        //composable("third_page") { ThirdPage(navController) }
    }
}

/**
 *FirstPage可组合项
 */
@Composable
fun FirstPage(navController: NavController) {
    Column {
        Text(text = "FirstPage页面")
        Button(onClick = {
            // 导航到SecondPage可组合项
            navController.navigate("second_page")
        }) {
            Text(text = "去SecondPage")
        }
    }
}

/**
 * SecondPage可组合项
 */
@Composable
fun SecondPage(navController: NavController) {
    Text(text = "SecondPage页面")
}
```  

在上面的代码中，使用NavHost制作屏幕，而我们的第一个屏幕是“ first_screen”，因为我们将startDestination设置为“ first_screen”。在此，“ first_screen ”，“ second_screen ”和“ third_screen ”是每个屏幕的路线。每个目的地都应具有唯一的路线，因为借助这些路线，一个屏幕会与其他屏幕区分开。

##### (2.)导航后清除起始页和目的页之间的页面
导航之前，清除指定可组合项到目的可组合项之间的可组合项:
```
NavController.navigate("目的地路径"){ popUpTo("返回路径") }
```
如下例子
```
@Composable
fun HelloCompose() {
    // 创建NavController
    val navController = rememberNavController()
    // 用NavHost将NavController和导航图相关联，startDestination指定起始的可组合项
    NavHost(navController = navController, startDestination = "first_page") {
        // 给FirstPage可组合项指定路径
        composable("first_page") { FirstPage(navController) }
        // 给SecondPage可组合项指定路径
        composable("second_page") { SecondPage(navController) }
        // 给ThirdPage可组合项指定路径
        composable("third_page") { ThirdPage(navController) }
    }
}

/**
 *FirstPage
 */
@Composable
fun FirstPage(navController: NavController) {
    Column {
        Text(text = "FirstPage页面", color = Color.Red)
        Button(onClick = {
            // 导航到SecondPage可组合项
            navController.navigate("second_page")
        }) {
            Text(text = "去SecondPage")
        }
    }
}   

/**
 * SecondPage
 */
@Composable
fun SecondPage(navController: NavController) {
    Column {
        Text(text = "SecondPage页面", color = Color.Red)
        Button(onClick = {
            // 导航到ThirdPage可组合项
            navController.navigate("third_page") { popUpTo("first_page") }
        }) {
            Text(text = "去ThirdPage")
        }
    }
}

/**
 *ThirdPage
 */
@Composable
fun ThirdPage(navController: NavHostController) {
    Text(text = "ThirdPage页面", color = Color.Red)
}
```
上面例子中点击FirstPage --> SecondPage --> ThirdPage，在ThirdPage，此时点击返回的话，会回到点击FirstPage可组合项，而不是SecondPage。

##### (3.)清除导航后目的页之前的所有页面
清除导航后目的页之前的所有页面，直接加个属性``inclusive=true``就可以了。类似于Activity的``android:launchMode="singleTask"``。
```
@Composable
fun HelloCompose() {
    // 创建NavController
    val navController = rememberNavController()
    // 用NavHost将NavController和导航图相关联,startDestination指定起始的可组合项
    NavHost(navController = navController, startDestination = "first_page") {
        // 给FirstPage可组合项指定路径
        composable("first_page") { FirstPage(navController) }
        // 给SecondPage可组合项指定路径
        composable("second_page") { SecondPage(navController) }
        // 给ThirdPage可组合项指定路径
        composable("third_page") { ThirdPage(navController) }
    }
}

/**
 *FirstPage
 */
@Composable
fun FirstPage(navController: NavController) {
    Column {
        Text(text = "FirstPage页面", color = Color.Red)
        Button(onClick = {
            // 导航到SecondPage可组合项
            navController.navigate("second_page")
        }) {
            Text(text = "去SecondPage")
        }
    }
}

/**
 * SecondPage
 */
@Composable
fun SecondPage(navController: NavController) {
    Column {
        Text(text = "SecondPage页面", color = Color.Red)
        Button(onClick = {
            // 导航到ThirdPage可组合项
            navController.navigate("third_page") { popUpTo("first_page") }
        }) {
            Text(text = "去ThirdPage")
        }
    }
}

/**
 *ThirdPage
 */
@Composable
fun ThirdPage(navController: NavHostController) {
    Text(text = "ThirdPage页面", color = Color.Red)
}
```
上面例子中点击FirstPage --> SecondPage --> ThirdPage，在ThirdPage，此时点击返回的话，会回到桌面。

##### (4.)页面未在页面栈内才进行导航
如果该页面在栈顶的话，不会重新入栈，而是会复用该栈 。类似于Activity的``android:launchMode="singleTop"``。
```
navController.navigate("search") {
    launchSingleTop = true
}
```

### 5.导航传递参数
在页面跳转过程中需要传递参数，可以通过在路径中添加参数占位符的方式来实现。默认情况下，所有参数都会被解析成字符串，不过我们可以通过arguments参数来设置参数类型。
##### (1.)传递参数
设置arguments参数：
```
composable(
    "second_page/{person_name}",
    //设置参数
    arguments = listOf(navArgument("person_name") { type = NavType.StringType })
) { backStackEntry ->
    ...
}
```
默认情况下，所有参数都会被解析为字符串。您可以使用 arguments 参数来设置 type，以指定其他类型： 设置完arguments参数之后， 在导航时，把占位符设置为具体值即可。

##### (2.)接收参数
有传递就有接收，在Compose中是通过composalbe()函数的lambda中提供的NavBackStackEntry中提取NavArguments：
```
composable(
    "second_page/{person_name}",
    arguments = listOf(navArgument("person_name") {
        //表示传递的参数是String类型
        type = NavType.StringType
    })
) { backStackEntry ->
    //backStackEntry里面封装了参数
    SecondPage(navController, backStackEntry)
}
```

```
@Composable
fun SecondPage(navController: NavController, backStackEntry: NavBackStackEntry) {
    val personName = backStackEntry.arguments?.getString("person_name")
    Text(text = "SecondPage页面$personName", color = Color.Red)
}
```

##### (3.)导航传递默认参数
可以在构建导航路由的时候使用defaultValue添加默认参数，代码如下：
```
composable(
    "second_page/{person_name}",
    arguments = listOf(navArgument("person_name") {//路由中三部分的person_name名称必须一致
        type = NavType.StringType//表示传递的参数是String类型
        defaultValue = "默认名字"
    })
) {
    SecondPage(it.arguments?.getString("goodsId"))//获取名称传递给SecondPage视图
}
```

参考资料:
[Compose_15--导航1（页面跳转）](https://blog.csdn.net/weixin_42404361/article/details/121941709)
[Jetpack Compose初体验--（导航、生命周期等）](https://juejin.cn/post/6983968223209193480)
[compose导航简单使用讲解](https://juejin.cn/post/6985782640917872670)











