---
title: AndroidJetpack-Compose之五常用组件及主题
date: 2022-06-09
categories: 
  - Android开发
tags:
  - JetpackCompose    
---

# 使用Material design 设计主题Theme
在Android中可以对整个应用的风格(颜色,字体等等)进行管理，这种风格叫做主题。通过主题对整个应用的字体、颜色、大小、形状进行管理可以使整个应用变得容易维护，保证App视觉的一致性。
Compose 的 Theme 摆脱了对 XML 的使用。Theme 一般会作为最顶层的 Composalbe 出现，所有内部 Composalbe 都会应用当前主题的配置。这样使得主题切换也变得非常容易。

Material主题设置是一种系统化的方法，用于自定义Material Design以更好反映产品的品牌，它是由颜色、排版和形状属性组成。如果这些属性被定义，构建应用的组件就会展现出对应属性的效果。
在Jetpack Compose中使用MaterialTheme可组合项来实现这些概念。
### 简单使用
例如根据系统Dark/Light主题，设置不同颜色
1. 定义好深色模式和浅色模式的颜色值,定义自定义的Theme方法,根据将不同的状态传入深色还是浅色值:
```
/*定义深色模式的颜色值*/
private val DarkColorPalette = darkColors(
    primary = Teal200,
    primaryVariant = Purple700,
    secondary = Teal200
)
/*定义浅色模式的颜色值*/
private val LightColorPalette = lightColors(
    primary = Purple200,
    primaryVariant = Purple700,
    secondary = Teal200
)
/*定义一个自定的主题方法调用MaterialTheme*/
@Composable
fun ComposeTheme(darkTheme: Boolean = isSystemInDarkTheme(), content: @Composable() () -> Unit) {
    /*根据传递的参数判断配置深色还是浅色*/
    val colors = if (darkTheme) {
        DarkColorPalette
    } else {
        LightColorPalette
    }
    MaterialTheme(
        colors = colors,
        typography = Typography,
        shapes = Shapes,
        content = content
    )
}
```
2. 将自定义的Theme作为最顶层的 Composalbe,这样我们就可以在在内层的组件中使用定义好的.
```
class ThemeActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            ComposeTheme(darkTheme = false) {
                Box(
                    Modifier
                        .size(200.dp, 200.dp)
                        .background(MaterialTheme.colors.primary)
                ) {
                }
            }
        }
    }
}
```
上述代码ComposeComingTheme 该组合函数在 MaterialTheme 上构建而成，MaterialTheme由colors、typography、shapes属性组成。
然后该组合函数默认根据系统 是否是暗黑主题 将 颜色属性 进行了不同的定义。如果是暗黑主题使用DarkColorPalette，
否则使用LightColorPalette。darkColors和lightColors都继承自Colors，并有相关的默认颜色值。

### 主题自带颜色
```
primary: Color = Color(0xFF6200EE),
primaryVariant: Color = Color(0xFF3700B3),
secondary: Color = Color(0xFF03DAC6),
secondaryVariant: Color = Color(0xFF018786),
background: Color = Color.White,
surface: Color = Color.White,
error: Color = Color(0xFFB00020),
onPrimary: Color = Color.White,
onSecondary: Color = Color.Black,
onBackground: Color = Color.Black,
onSurface: Color = Color.Black,
onError: Color = Color.White
```


# UI组件类型
虽然Jetpack Compose 1.0 才刚面世，但实际上其UI组件库已经十分完备，几乎完全覆盖了Android现有视图系统的所有组件及能力，主要包括：
- 基础UI组件，如Button、TextView等，连Card、Fab、AppBar等Material Designe的控件都会涵盖；
- 列表类组件，如List等，采用items{...} 中创建每条项目的 Composalbe，避免了额外的Adapter适配；
- 布局类组件，提供了多种容器类Composalbe，可以十分高效方便地对子组件进行布局；通过一系列链式调用的Modifier操作符来装饰 Composable 的外观。操作符的使用十分丰富，如size、backgrounds、padding等；
- 动画组件，同样是采用状态（State）驱动进行动画效果的实现。

# Text
- text	文字
- color	文字颜色
- fontSize	字体大小
- fontStyle	字体样式, 可设置为斜体Italic
- fontWeight	字体权重,可设置字体加粗
- overflow	文字溢出效果,与maxLines结合使用可实现文字溢出显示省略号效果
- maxLines	最大行数 ,与overflow结合使用实现文字溢出显示省略号效果

# Button组件
### 源码
```
@Composable
fun Button(
    onClick: () -> Unit,// 按钮的点击事件
    modifier: Modifier = Modifier,
    enabled: Boolean = true, //是否启用
    interactionState: InteractionState = remember { InteractionState() },
    elevation: ButtonElevation? = ButtonDefaults.elevation(),//海拔
    shape: Shape = MaterialTheme.shapes.small,//形状
    border: BorderStroke? = null,//边框
    colors: ButtonColors = ButtonDefaults.buttonColors(),//颜色
    contentPadding: PaddingValues = ButtonDefaults.ContentPadding,//内边距
    content: @Composable RowScope.() -> Unit //内容组件
) { ... }
```
### 示例
Button 组件点击事件 onClick 和内容组件 content 是必填参数外。
```
@Composable
fun TestButton() {
    Button(onClick = {/*TODO点击事件*/ }) {
        Text(text = "button")
    }
}
```

# Image组件
### 源码
```
@Composable
fun Image(
    bitmap: ImageBitmap,
    contentDescription: String?,
    modifier: Modifier = Modifier,
    alignment: Alignment = Alignment.Center,
    contentScale: ContentScale = ContentScale.Fit,
    alpha: Float = DefaultAlpha,
    colorFilter: ColorFilter? = null
) {
  ...
}
```
### 属性
Image 对应于 Android View 的 ImageView，可以用来显示图片，它主要有以下属性：
- bitmap: ImageBitmap：可以直接传入 ImageBitmap 构建,如想显示 drawable 文件夹下的图片，可以通过 ``var imageBitmap = ImageBitmap.imageResource(id = R.drawable.xxx)``
- contentDescription: String?：accessibility services 用于辅助功能时提示给用户的描述信息
- modifier : Modifier：Image 的修饰符
- aligment : Aligment：对齐方式
- contentScale : ContentScale：图片的显示模式(ContentScale.Crop 居中裁剪)
- alpha : Float：设置透明度，默认是 1.0f
- colorFilter : ColorFilter：可以设置颜色滤镜

### 引入 coil 依赖库加载网络图片
```
// build.gradle
implementation "io.coil-kt:coil:1.4.0"
implementation "io.coil-kt:coil-compose:1.4.0"
```
coil 是 Compose 中推荐使用的图片网络加载库，底层采用 Kotlin 协程进行加载。添加了依赖之后，就可以使用 rememberImagePainter 直接将图片链接传给 data 即可。如下代码：
```
Image(
    painter = rememberImagePainter(
        data = "https://www.baidu.com/img/flexible/logo/pc/result.png"
    ),
    contentDescription = "baidu",
    modifier = Modifier.size(50.dp),
    contentScale = ContentScale.Crop  // 居中裁剪
)
```

# Spacer组件
### 源码
```
fun Spacer(modifier: Modifier) {
    ...
}
```
### 示例
传统布局中，可以添加Margin属性，设置间距，在Jetpack Compose 中，可以使用Spacer() 来设置垂直和水平间距
```
Row {
   Spacer(Modifier.width(20.dp))//设置水平间距20dp
   Spacer(Modifier.height(20.dp)) //设置垂直间距20dp
    }
```

# Divider
### 源码

```
@Composable
fun Divider(
    modifier: Modifier = Modifier,
    color: Color = MaterialTheme.colors.onSurface.copy(alpha = DividerAlpha),
    thickness: Dp = 1.dp,
    startIndent: Dp = 0.dp
) {
  ...
}
```
### 属性
- color //颜色
- thickness //线的高度
- startIndent //距离开始的间距

# Surface
### 源码
```
@Composable
fun Surface(
    modifier: Modifier = Modifier,
    shape: Shape = RectangleShape,
    color: Color = MaterialTheme.colors.surface,
    contentColor: Color = contentColorFor(color),
    border: BorderStroke? = null,
    elevation: Dp = 0.dp,
    content: @Composable () -> Unit
) {
    ...
}
```
### 属性
当想要为我们自定义的一个组件添加背景颜色时，我们就需要用到 Surface，它主要有以下属性：
- modifier: Modifier：可以为 Surface 设置修饰符
- shape: Shape：设置形状，默认是 RectangleShape
- color: Color：设置背景色
- contentColor: Color：为 Surface 中的 Text 文字设置颜色，当 Text 没有指定颜色时，就是使用该颜色
- border: Border?：设置外边框
- elevation: Dp：为 Surface 设置在 Z 轴方向上的高度
- content: @Composable () -> Unit：为 Surface 设置内容布局，需要传入 @Compose 方法
### 示例
```
Surface(modifier = Modifier.padding(4.dp), color = Color.Gray) {
    Column {
        Text(modifier = Modifier.align(Alignment.CenterHorizontally), text = "custom")
        Image(
            modifier = Modifier.size(150.dp),
            painter = ColorPainter(color = Color.Green),
            contentDescription = "image color"
        )
    }
}
```

# Canvas
Canvas 是在屏幕上指定区域执行绘制的组件。注意在使用时需要添加修饰符来指定尺寸，可以通过 Modifier.size
设置固定的大小，也可以使用 Modifier.fillMaxSize，ColumnScope.weight 设置相对父组件大小。如果父组件没有设置大小，那么 Canvas
必须要设置固定的大小。
Canvas 就是类似于原来的自定义 View，但是更加的简便，通过 DrawScope 定义的绘制方法进行绘制出自己想要的效果，可以通过 drawArc ，drawCircle
，drawLine，drawPoints 等方法来绘制图形（详情可参考 DrawScope 下的方法）：
```
Canvas(modifier = Modifier.fillMaxSize()) {
    val canvasWidth = size.width
    val canvasHeight = size.height
    // 绘制一条从左下角到右上角的蓝色的线
    drawLine(
        start = Offset(x = canvasWidth, y = 0f),
        end = Offset(x = 0f, y = canvasHeight),
        color = Color.Blue
    )

    // 在以 200，1200 位置 120 为半径绘制一个圆
    drawCircle(color = Color.Green, center = Offset(200f, 1200f), radius = 120f)
}
```

# 滚动布局
只需要用 Column 中的 Modifier.verticalScroll 属性就可以了。
```
@Composable
fun SimpleList() {
    //使用 rememberScrollState 保存滚动的位置信息
    val scrollState = rememberScrollState()
    //Modifier.verticalScroll 可添加竖直方向上的滚动属性,使用 Column 的 Modifier.verticalScroll 方法确实可以创建一个可滑动的List，但是这种方法在开始时就会将所有 item 全部加载，类似于 ScrollView
    Column(Modifier.verticalScroll(scrollState)) {
        repeat(100) {
            Text(text = "Item $it")
            Divider(color = Color.Blue, thickness = 1.5.dp, startIndent = 10.dp)
        }
    }
}

@Composable
fun BodyContent(modifier: Modifier) {
    Column(modifier = modifier) {
        Text(text = "Hi there!")
        Text(text = "Thanks for watching this")
        SimpleList()    // 将 List 放在之前的布局中展示出来
    }
}
```
这种实现方法最简单，但是会在页面开始展示时，将列表中所有的 item 加载到内存中，虽然很多 item 都没有显示在屏幕上，这种方法当列表内容很多时，会出现内存占用大的问题。

# 列表
可以滾動的佈局
```
//我們可以使用 verticalScroll() 修飾符使 Column 可滾動
Column (
        modifier = Modifier.verticalScroll(rememberScrollState())){
        messages.forEach { message ->
            MessageRow(message)
        }
    }
```
但以上佈局並無法實現重用，可能導致性能問題，下面介紹我們重點佈局，列表``LazyColumn/LazyRow==RecylerView/listView``列表佈局，解決了滾動時的性能問題，LazyColumn 和 LazyRow 之間的區別就在於它們的列表項佈局和滾動方向不同
內邊距:
```
LazyColumn(
    contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
) {
    // ...
}

```
item間距:
```
LazyColumn(
    verticalArrangement = Arrangement.spacedBy(4.dp),
) {
    // ...
}
```
浮動列表的浮動標題，使用 LazyColumn 實現粘性標題，可以使用實驗性 stickyHeader()函數
```
@OptIn(ExperimentalFoundationApi::class)
@Composable
fun ListWithHeader(items: List<Item>) {
    LazyColumn {
        stickyHeader {
            Header()
        }

        items(items) { item ->
            ItemRow(item)
        }
    }
}
```
網格佈局LazyVerticalGrid
```
@OptIn(ExperimentalFoundationApi::class)
@Composable
fun PhotoGrid(photos: List<Photo>) {
    LazyVerticalGrid(
        cells = GridCells.Adaptive(minSize = 128.dp)
    ) {
        items(photos) { photo ->
            PhotoItem(photo)
        }
    }
}
```


```
@Composable
fun CreateDrawerLayout() {
    val list = mutableListOf<Student>()
    for (i in 0..33) {
        list.add(Student("学生${i}", i))
    }
    LazyColumn(modifier = Modifier.fillMaxWidth()) {
        items(list.size) {
            Text(
                text = "items:姓名：${list[it].name},年龄${list[it].age}岁",
                fontSize = 18.sp
            )
            Spacer(modifier = Modifier.height(10.dp))
        }

        itemsIndexed(items = list) { index: Int, item: Student ->
            Text(
                text = "itemsIndexed:姓名：${item.name},年龄${item.age}岁",
                fontSize = 18.sp, modifier = Modifier.clickable {

                })
            Spacer(modifier = Modifier.height(10.dp))
        }

        list.forEachIndexed { index, student ->
            item {
                Text(
                    text = "forEachIndexed:姓名：${student.name},年龄${student.age}岁",
                    fontSize = 18.sp
                )
                Spacer(modifier = Modifier.height(10.dp))
            }
        }

    }
}

data class Student(
    val name: String,
    val age: Int
)
```

```
@Composable
fun ImageListItem(index: Int) {    
    //列表 item 布局
    //Row 可设置竖直方向上的对齐方式
    Row(verticalAlignment = Alignment.CenterVertically) {
        Image(
            painter = rememberImagePainter(
                data = "https://pic.ntimg.cn/20140810/3822951_180850680000_2.jpg"
            ), 
            contentDescription = "Test Img", 
            modifier = Modifier.size(50.dp)
        )
        Spacer(modifier = Modifier.width(10.dp)) // Spacer 也可设置边距
        Text(text = "Item #$index", style = MaterialTheme.typography.subtitle1)
    }
}

@Composable
fun ScrollingList() {
    val listSize = 100
    // 使用 rememberLazyListState 保存滚动的位置
    val scrollState = rememberLazyListState()

    LazyColumn(state = scrollState) {
        items(listSize) {
            ImageListItem(index = it)
            Divider(color = Color.Blue, thickness = 1.5.dp, startIndent = 10.dp)
        }
    }
}
```

# Scaffold
```
Scaffold(
    modifier: Modifier = Modifier,
    scaffoldState: ScaffoldState = rememberScaffoldState(),
    topBar: @Composable () -> Unit = {},
    bottomBar: @Composable () -> Unit = {},
    snackbarHost: @Composable (SnackbarHostState) -> Unit = { SnackbarHost(it) },
    floatingActionButton: @Composable () -> Unit = {},
    floatingActionButtonPosition: FabPosition = FabPosition.End,
    isFloatingActionButtonDocked: Boolean = false,
    drawerContent: @Composable (ColumnScope.() -> Unit)? = null,
    drawerGesturesEnabled: Boolean = true,
    drawerShape: Shape = MaterialTheme.shapes.large,
    drawerElevation: Dp = DrawerDefaults.Elevation,
    drawerBackgroundColor: Color = MaterialTheme.colors.surface,
    drawerContentColor: Color = contentColorFor(drawerBackgroundColor),
    drawerScrimColor: Color = DrawerDefaults.scrimColor,
    backgroundColor: Color = MaterialTheme.colors.background,
    contentColor: Color = contentColorFor(backgroundColor),
    content: @Composable (PaddingValues) -> Unit
)
```

属性说明
- topBar 顶部的布局
- bottomBar 底部的布局
- floatingActionButton 悬浮按钮布局
- floatingActionButtonPosition 悬浮按钮位置,有FabPosition.End(默认)和FabPosition.Center可选
- isFloatingActionButtonDocked 与BottomAppBar配合使用,可以实现底部导航条的裁剪效果,效果可以看下图
- drawerGesturesEnabled 是否开启侧边抽屉手势(开启后可侧滑弹出抽屉)
- drawerShape 抽屉的形状
- drawerContent 侧边抽屉内容,是个Column布局,自己可以顺便排列
- drawerElevation 侧边抽屉的阴影
- drawerBackgroundColor 侧边抽屉的背景色
- drawerContentColor 侧边抽屉内容颜色(似乎是覆盖字体颜色而已)
- drawerScrimColor 侧边抽屉遮盖最底层的颜色

Material 支持的最高级别的可组合项是 Scaffold。Scaffold 可让您实现具有基本 Material Design 布局结构的界面。Scaffold 可以为最常见的顶级 Material 组件（如 TopAppBar、BottomAppBar、FloatingActionButton 和 Drawer）提供插槽。通过使用 Scaffold，很容易确保这些组件得到适当放置且正确地协同工作。

# BottomNavigation
```
@Composable
fun Tab(viewModel: ViewMod){
    // tab标题
    val listItem = listOf("组织","发现","我的")
    // tab未选图标
    val icons = listOf(R.drawable.home,R.drawable.find,R.drawable.profile)
    // tab选中图标
    val selectIcons = listOf(R.drawable.homeselect,R.drawable.findselect,R.drawable.profileselect)
    // 记住选中tab位置
    val selectIndex = remember {
        mutableStateOf(0)
    }
    // 脚手架
    val navControllers = rememberNavController()
    Scaffold(
        modifier = Modifier.fillMaxSize(),
        bottomBar = {
            // BottomNavigation的显示和隐藏先借助本地数据存储，再说
            BottomNavigation(
                backgroundColor = Color.White,
                elevation = 3.dp
            ) {
                val navBackStackEntry by navControllers.currentBackStackEntryAsState()
                val currentRoute = navBackStackEntry?.arguments?.getString(KEY_ROUTE)

                items.forEachIndexed { index, s ->
                    BottomNavigationItem(
                        selected = currentRoute == s.route,
                        onClick = {
                            selectIndex.value = index
                            navControllers.navigate(s.route) {
                                // Pop up to the start destination of the graph to
                                // avoid building up a large stack of destinations
                                // on the back stack as users select items
                                popUpTo = navControllers.graph.startDestination
                                // Avoid multiple copies of the same destination when
                                // reselecting the same item
                                launchSingleTop = true
                            }
                                  },
                        icon = {
                            when(index){
                                selectIndex.value -> {
                                    Image(painter = painterResource(id = selectIcons[index]), contentDescription = null)
                                }
                                else -> {
                                    Image(painter = painterResource(id = icons[index]), contentDescription = null)
                                }
                            }
                        },
                        label = {
                           Text(
                               text = listItem[index],
                               textAlign = TextAlign.Center,
                               color = if (index == selectIndex.value) Color(0xFF0077E6) else Color(0xFFD8D8D8)
                           )
                        }
                    )
                }
            }
        },
        content = {
            NavHost(navControllers, startDestination = Screen.Home.route) {
                // 首页
                composable(Screen.Home.route) { Home(viewModel,navControllers) }
                // 发现
                composable(Screen.Find.route) { Find(navControllers) }
                // 我的
                composable(Screen.Profile.route) { Profile(navControllers,viewModel) }
            }
        }
    )
}

sealed class Screen(val route: String, @StringRes val resourceId: Int) {
    object Home : Screen("home", R.string.home)
    object Find : Screen("find", R.string.find)
    object Profile : Screen("profile", R.string.profile)

}

val items = listOf(
    Screen.Home,
    Screen.Find,
    Screen.Profile
)
```

# OutlinedTextField 属性解析
在实现以上效果前，先要了解OutlinedTextField的属性，才能加以运用 ；先看一下属性列表。

```
@Composable
fun OutlinedTextField(
    value: String,
    onValueChange: (String) -> Unit,
    modifier: Modifier = Modifier,
    enabled: Boolean = true,
    readOnly: Boolean = false,
    textStyle: TextStyle = LocalTextStyle.current,
    label: @Composable (() -> Unit)? = null,
    placeholder: @Composable (() -> Unit)? = null,
    leadingIcon: @Composable (() -> Unit)? = null,
    trailingIcon: @Composable (() -> Unit)? = null,
    isError: Boolean = false,
    visualTransformation: VisualTransformation = VisualTransformation.None,
    keyboardOptions: KeyboardOptions = KeyboardOptions.Default,
    keyboardActions: KeyboardActions = KeyboardActions.Default,
    singleLine: Boolean = false,
    maxLines: Int = Int.MAX_VALUE,
    interactionSource: MutableInteractionSource = remember { MutableInteractionSource() },
    shape: Shape = MaterialTheme.shapes.small,
    colors: TextFieldColors = TextFieldDefaults.outlinedTextFieldColors()
) 
```

- value: String 输入框显示的文本
- onValueChange: (String) -> Unit 值发生改变之后触发的回调
- modifier: Modifier = Modifier 修饰
- enabled: Boolean = true 可用
- readOnly: Boolean = false 是否只读
- textStyle: TextStyle = LocalTextStyle.current
- label: @Composable (() -> Unit)? = null 输入框获取焦点时左上角提示的内容
- placeholder: @Composable (() -> Unit)? = null 输入框提示的内容
- leadingIcon: @Composable (() -> Unit)? = null 输入框左侧的图标
- trailingIcon: @Composable (() -> Unit)? = null 输入框右侧的图标
- isError: Boolean = false 是否处于错误状态
- visualTransformation: VisualTransformation = VisualTransformation.None, 转换输入值的视觉表示
- keyboardOptions: KeyboardOptions = KeyboardOptions.Default 输入框输入类型
- singleLine: Boolean = false, 是否单行显示
- maxLines: Int = Int.MAX_VALUE 最大行数
- colors: TextFieldColors = TextFieldDefaults.outlinedTextFieldColors() 颜色集合，设置获取焦点，失去焦点以及光标等颜色

# AlertDialog 
1、属性一览
【目前基于alpha09版本】请看该对话框支持的两个函数，首先看第一个函数，该函数会根据可用空间水平放置其按钮：
```
@Composable fun AlertDialog(
    onDismissRequest: () -> Unit, 
    confirmButton: () -> Unit, 
    modifier: Modifier = Modifier, 
    dismissButton: () -> Unit = null, 
    title: () -> Unit = null, 
    text: () -> Unit = null, 
    shape: Shape = MaterialTheme.shapes.medium, 
    backgroundColor: Color = MaterialTheme.colors.surface, 
    contentColor: Color = contentColorFor(backgroundColor), 
    properties: DialogProperties? = null
): Unit
```
- modifier: Modifier = Modifier	应用于布局的修饰符
- onDismissRequest: () -> Unit	当用户点击对话框外部或者按下返回按钮的时候会执行。注意：点击对话框的关闭按钮时并不会执行
- confirmButton: () -> Unit	一个由用户确认操作的按钮，默认没有回调，需要调用者自行设置回调事件。
- dismissButton: () -> Unit = null	一个用于关闭对话框的按钮，默认没有回调，需要调用者自行设置回调事件。
- title: () -> Unit = null	对话框的标题，默认无
- text: () -> Unit = null	对话框的内容，默认无
- shape: Shape = MaterialTheme.shapes.medium	对话框的形状
- backgroundColor: Color = MaterialTheme.colors.surface	对话框的背景色
- contentColor: Color = contentColorFor(backgroundColor)	提供给其子级的首选内容颜色
- properties: DialogProperties? = null	用于进一步配置特定属性的对话框

# Tab及ScrollableTabRow
关于tab有两个函数，如下：
```
@Composable fun Tab(
    selected: Boolean, 
    onClick: () -> Unit, 
    modifier: Modifier = Modifier, 
    text: () -> Unit = emptyContent(), 
    icon: () -> Unit = emptyContent(), 
    interactionState: InteractionState = remember { InteractionState() }, 
    selectedContentColor: Color = AmbientContentColor.current, 
    unselectedContentColor: Color = selectedContentColor.copy(alpha = ContentAlpha.medium)
): Unit
```
- selected: Boolean	该Tab是否被选中
- onClick: () -> Unit	点击该Tab时候的回调事件
- modifier: Modifier = Modifier	应用于该Tab的修饰符
- text: () -> Unit = emptyContent()	显示在该Tab中的文本
- icon: () -> Unit = emptyContent()	显示在该Tab中的图标
- interactionState: InteractionState = remember { InteractionState() }	该Tab的交互状态
- selectedContentColor: Color = AmbientContentColor.current	选中该Tab时内容的颜色，以及水波纹的颜色
- unselectedContentColor: Color = selectedContentColor.copy(alpha = ContentAlpha.medium)	未选中该Tab时内容的颜色




参考资料:
[Jetpack Compose初体验](https://blog.csdn.net/mingyunxiaohai/article/details/116271290)
[compose资料](https://docs.compose.net.cn/)
[Compose UI官方文档](https://developer.android.com/jetpack/compose/documentation?hl=zh-cn)
[Android全新UI编程 - Jetpack Compose 超详细教程](https://juejin.cn/user/4125023359205742/posts)
[JetPack Compose 之 state](https://www.jianshu.com/p/93d8a384a8a0)
[Jetpack-Compose 学习笔记](https://blog.csdn.net/lbs458499563)
[Jetpack-Compose](https://blog.csdn.net/m0_37667770/article/details/114542808)
[Compose的State(九)](https://blog.csdn.net/Mr_Tony/article/details/118858756)
[Compose系列 三 状态管理](https://blog.csdn.net/ljjliujunjie123/article/details/120935611)
[原创|Android Jetpack Compose 最全上手指南](https://juejin.cn/post/6844903999347359751)
[Android Jetpack Compose 超快速上手指南](https://juejin.cn/post/6877056735018745863)
[compose text组件](https://www.cnblogs.com/baiyuas/p/14988887.html)
[Jetpack Compose初体验--（布局、动画等）](https://juejin.cn/post/6956487779807133727)
[Jetpack Compose初体验--（导航、生命周期等）](https://juejin.cn/post/6983968223209193480)
[compose text组件](https://www.cnblogs.com/baiyuas/p/14988887.html)
[Jetpack Compose初体验--(布局、动画等)](https://juejin.cn/post/6956487779807133727)
[Jetpack Compose初体验--(导航、生命周期等)](https://juejin.cn/post/6983968223209193480)

[告别XML，使用Compose Theme为你的app轻松换皮](https://blog.csdn.net/vitaviva/article/details/114764215)











