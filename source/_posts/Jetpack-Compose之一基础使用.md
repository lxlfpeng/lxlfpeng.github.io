---
title: Jetpack-Compose之一基础使用
---

# 一.命令式UI和申明式UI
如果之前有了解或者使用果Flutter，应该会对命令式UI这种架构不陌生。目前申明式UI确实是很火包含Flutter，SwiftUI，JetpackCompose都使用了该种方式。2021年7月底，Google 正式发布了 Jetpack Compose 的 1.0 稳定版本，这说明Google认为Compose已经可以用于生产环境了。
### 1.命令式UI
回想再传统的Android开发中，首先会在xml布局文件中写好控件，然后在Activity中通过findViewbyid找到该控件，然后通过命令给他设置各种属性，例如设置背景颜色，设置内边距，控件会根据我们所设置的属性 做UI的变化，至始至终我们都是通过改变同一个控件的属性，来获得不同的显示效果.这就是命令式UI.
```
View view=findViewById(R.id.view)
view.setBackgroundColor(Color.Blue)
view.setTop(xxx)
```

### 2.申明式UI
在申明式UI中视图配置是不可变的，意思就是说需要先描述UI界面的样子，状态变化时，界面按照新的描述的重新“渲染”即可得到正确的界面，每次重新渲染就是在控件自身上触发重建， 不会修改旧的实例控件，而是构造不同的新的实例控件进行展示。
```
return ViewB(
  backgroundColor: Color.Blue,
  top: xxx,
)
```

# 二.项目引入Compose
有两种方式，一种是手动引入，另外一种是通过AndroidStudio创建:
### 1.手动引入Compose依赖
##### (1.)项目根gradle中添加
```
buildscript {
    ext {
        compose_version = '1.0.0' // compose版本
    }
    ext.kotlin_version = "1.4.30"
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath "com.android.tools.build:gradle:7.0.0"
        classpath "org.jetbrains.kotlin:kotlin-gradle-plugin:$kotlin_version"
    }
}
```

##### (2.)app目录下的build.gradle设置
将app支持的最低API 版本设置为21或更高，同时开启Jetpack Compose enable开关
```
android {
    defaultConfig {
        ...
        minSdkVersion 21
    }

    buildFeatures {
        // Enables Jetpack Compose for this module
        compose true
    }
    ...

    // Set both the Java and Kotlin compilers to target Java 8.

    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }

    kotlinOptions {
        jvmTarget = "1.8"
    }
}
```

##### (3.)添加Jetpack Compose工具包依赖项
在app目录下的build.gradle添加Jetpack Compose 工具包依赖项，代码如下：
```
dependencies {
    // You also need to include the following Compose toolkit dependencies.
     //compose依赖
       implementation "androidx.compose.ui:ui:$compose_version"
       implementation "androidx.compose.foundation:foundation:$compose_version"
       implementation "androidx.compose.material:material:$compose_version"
       implementation "androidx.compose.runtime:runtime-livedata:$compose_version"
       implementation "androidx.compose.runtime:runtime-rxjava2:$compose_version"
       implementation 'androidx.activity:activity-compose:1.3.0-alpha03'
       implementation "androidx.compose.ui:ui-tooling:$compose_version"
    ...
}
```

### 2.AndroidStudio创建Compose工程
![](https://img-blog.csdnimg.cn/img_convert/58e63d8ea11aab4e1e7ce944888228f3.png)

# 三.Compose示例分析
### 1.Compose简单使用
在MainActivity.kt中添加如下代码：
```
class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            Text("Hello,Compose!")
        }
    }
}
```
运行就可以看到效果了:
![](https://img-blog.csdnimg.cn/img_convert/8ab6bcdb0c18acd6592f666828de711a.png)
这种写法与使用 XML 布局的方式差别很大，setContent 块定义了 Activity 的布局。不需要使用 XML 文件来定义布局内容，而是调用一个 Compose 函数，比如上面的 Text 函数， 然后 Jetpack Compose 使用自定义 Kotlin 编译器插件将这些 Compose 函数转换为应用的界面元素。

### 2.Composable注解
点开Text函数，可以发现它是kotlin的一个``顶层函数``，并且被@Composable注解修饰:
```
@Composable
fun Text(
    ...
) {
    Text(
      ...
    )
}
```
Jetpack Compose的界面是围绕composable函数来构建的。这些composable函数可以通过描述应用程序的形状和数据依赖，以编程方式定义应用程序的UI，而不是着眼于UI的构建过程。因此要创建composable函数，只需要在函数名前面加上一个@composable注解即可。
例如可以通过Composable注解一个方法对Text进行封装:
```
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            helloText("Hello,Compose!")
        }
    }
    @Composable
    fun helloText(text:String){
        Text(text);
    }
}
```

>需要注意，Composable注解的函数只能在其他Composable注解的函数内调用。

# 四.Compose界面预览
### 1.@Preview注解
在 Compose 框架中通过给 Composable 函数添加 @Preview 注解就可以在不运行App的情况下确认布局的情况:
```
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            helloText()
        }
    }

    @Preview()
    @Composable
    fun helloText(){
        Text("Hello,Compose!")
    }
}
```
![](https://img-blog.csdnimg.cn/img_convert/514b51e5287d2550f9f81a0fa5de8a17.png)

**在IDE的右上角有Code，Split，Design三个选项。分别是只显示代码，同时显示代码和布局和只显示布局。**

### 2.@Preview注解常用参数
打开@Preview注解可以看到可以接收如下参数:
```
@Repeatable
annotation class Preview(
    val name: String = "",
    val group: String = "",
    @IntRange(from = 1) val apiLevel: Int = -1,
    // TODO(mount): Make this Dp when they are inline classes
    val widthDp: Int = -1,
    // TODO(mount): Make this Dp when they are inline classes
    val heightDp: Int = -1,
    val locale: String = "",
    @FloatRange(from = 0.01) val fontScale: Float = 1f,
    val showSystemUi: Boolean = false,
    val showBackground: Boolean = false,
    val backgroundColor: Long = 0,
    @UiMode val uiMode: Int = 0,
    @Device val device: String = Devices.DEFAULT
)

```
##### (1.)给Preview命名
- name: String: 为该Preview命名，该名字会在布局预览中显示。
- group: String: 为该Preview设置group名字，可以在UI中以group为单位显示。
  ![](https://img-blog.csdnimg.cn/img_convert/e4d9bd94c050e1992ffaa5652f6e3fc4.png)

##### (2.)给Preview设置背景颜色
- showBackground: Boolean: 是否显示背景，true为显示。
- backgroundColor: Long: 设置背景的颜色(backgroundColor 是 ARGB Long，而不是 Color 值)。
```
@Preview(showBackground = true, backgroundColor = 0xFF00FF00)
@Composable
fun WithGreenBackground() {
    Text("Hello World")
}
```
![](https://img-blog.csdnimg.cn/img_convert/7383439ba543f4aefbfe57cb7c5139e8.png)


>默认情况下，您的可组合项将以透明背景显示。

##### (3.)给Preview设置显示宽高
- widthDp: Int: 在Compose中渲染的最大宽度，单位为dp。
- heightDp: Int: 在Compose中渲染的最大高度，单位为dp。
  默认情况下，系统会自动选择 @Preview 尺寸来封装其内容。如需手动设置尺寸，可以添加 heightDp 和 widthDp 参数。
```
@Preview(widthDp = 50, heightDp = 50)
@Composable
fun SquareComposablePreview() {
    Box(Modifier.background(Color.Yellow)) {
        Text("Hello World")
    }
}
```
![](https://img-blog.csdnimg.cn/img_convert/a6cb587ab558c5a1f64a1efc16cfde75.png)
>请注意，这些值已解释为 Dp，您无需在值末尾添加 .dp

##### (4.)给Preview设置显示系统界面
如需在预览对象中显示状态栏和操作栏，请添加 showSystemUi 参数：
```
@Preview(showSystemUi = true)
@Composable
fun DecoratedComposablePreview() {
    Text("Hello World")
}
```
![](https://img-blog.csdnimg.cn/img_convert/e6ca15e2c4cd2d26b2956f554f06bcf8.png)

##### (5.)给Preview设置显示语言区域
如需测试不同的用户语言区域，您需要添加 locale 参数：
```
@Preview(locale = "fr-rFR")
@Composable
fun DifferentLocaleComposablePreview() {
    Text(text = stringResource(R.string.greetings))
}
```

##### (6.)通过@PreviewParameter给Preview添加传递参数预览
如果被 @Composable修饰的组件函数是一个有参数的函数，要对其进行预览，可以使用 @PreviewParameter 注解添加参数，以将数据传递给某个可组合项预览函数。
```
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            showUser(User("罗贯中"))
        }
    }
    @Composable
    @Preview("name",showBackground = true, backgroundColor = 0xFF00FF00)
    fun showUser(@PreviewParameter(UserPreviewParameterProvider::class) user: User) {
        Text(user.name)
    }
}

```
如需提供示例数据，请创建一个可实现 PreviewParameterProvider 并以序列形式返回示例数据的类。
```
class UserPreviewParameterProvider : PreviewParameterProvider<User> {
    override val values = sequenceOf(User("刘备"), User("曹操"), User("孙权"))
}
```
序列中的每个数据元素都会呈现一个预览：
![](https://img-blog.csdnimg.cn/img_convert/a80a7c53d1ae38226fa19f9855f23227.png)
如果不想每一个数据对应的预览都展示，可通过设置 limit 参数来限制呈现的预览数量:
```
@Composable
@Preview("name",showBackground = true, backgroundColor = 0xFF00FF00)
fun showUser(@PreviewParameter(UserPreviewParameterProvider::class, limit = 2) user: User) {
    Text(user.name)
}
```
![](https://img-blog.csdnimg.cn/img_convert/eeaff8e5019ea9a0041aa27e5e2987fe.png)

特别需要注意的有两点:
**上面的参数都是可选参数，还有像背景设置等的参数并不是对实际的App进行设置，只是对Preview中的背景进行设置，为了更容易看清布局。**
**在实际的开发中，预览函数不要发布到线上，所以最佳做法是单独创建不会被应用调用的预览函数用于查看实际效果，专门的预览函数可以提高性能，并且有利于以后更轻松地设置多个预览。**

# 五.Compose组件配置属性
上文中我们用到了Compose提供的Text组件，既然是文本组件肯定存在文本属性配置， 我们知道在Jetpack Compose 所有的组件都是 可以组合函数，所以Text 也不例外，源码如下:
```
@Composable
fun Text(
    text: String,//文字内容
    modifier: Modifier = Modifier, // 布局的设置
    color: Color = Color.Unspecified,// 文字颜色
    fontSize: TextUnit = TextUnit.Unspecified,//文字大小
    fontStyle: FontStyle? = null, //文字风格
    fontWeight: FontWeight? = null,//文字比重
    fontFamily: FontFamily? = null, //字体风格
    letterSpacing: TextUnit = TextUnit.Unspecified,//字间距
    textDecoration: TextDecoration? = null,//文字装饰器
    textAlign: TextAlign? = null,//文字对齐方式
    lineHeight: TextUnit = TextUnit.Unspecified,//文字行高
    overflow: TextOverflow = TextOverflow.Clip,// 文字显示不完的处理方式
    softWrap: Boolean = true,// 文本是否应在换行符处中断
    maxLines: Int = Int.MAX_VALUE,//最大行数
    onTextLayout: (TextLayoutResult) -> Unit = {},
    style: TextStyle = AmbientTextStyle.current
) {
    ……
}
```
因此我们在使用Text组件时可以对其属性进行配置。
例如配置文字颜色:
```
Text("Hello Compose", color = Color.Blue)
```
例如配置文字字号:
```
Text("Hello Compose", fontSize=20.sp)
```
通过这些属性我们就可以配置出各式各样不同的文本显示效果。

# 六.Compose组件中的Modifier
在上文中我们可以看到Text组件接收一个Modifier的参数， Modifier， 顾名思义就是一个修饰器，用于装饰Compose UI元素或向其添加行为。``每个 Compose 组件都会提供一个Modifier 参数用于修改样式``。
### 1.经常用到的Modifier属性
借助Modifier 参数可以控制 组件的行为和外观 如大小，背景等，还可以添加一些交互，如点击、滑动等。关于Modifier相关的设置实在是太多，在这里只介绍会经常用到的，更多[Modifier学习](https://developer.android.com/jetpack/compose/modifiers-list)
```
Text(
    "Android",
    modifier = Modifier
        .padding(10.dp)//设置padding
        .size(100.dp)//设置大小
        .background(Color.Gray)//设置背景
        .clickable(onClick = {})//添加点击事件
)
```
##### 1.配置尺寸
- Modifier.fillMaxHeight()    // 填充整个父组件的高度。
- Modifier.fillMaxWidth()     // 填充整个父组件的宽度。
- Modifier.fillMaxSize()      // 填充整个父组件的宽和高 类似于mach_parent
- Modifier.width(2.dp)        // 设置宽度
- Modifier.height(3.dp)       // 设置高度
- Modifier.size(4.dp, 5.dp)   // 设置高度和宽度
##### 2.配置重力
- Modifier.gravity(Alignment.CenterHorizontally)  // 横向居中
- Modifier.gravity(Alignment.Start)               // 横向居左
- Modifier.gravity(Alignment.End)                 // 横向居右

##### 3.配置边距Padding
- Modifier.padding(10.dp)                       //设置上下左右边距为同一值
- Modifier.padding(10.dp, 11.dp, 12.dp, 13.dp)  //分别为上下左右边距值
- Modifier.padding(10.dp, 11.dp)                //分别为上下和左右边距值

##### 4.配置偏移量
- Modifier.offset(x=10.dp,y=10.dp)   //要相对于原始位置放置布局，请添加 offset 修饰符，并在 x 轴和 y 轴中设置偏移量。偏移量可以是正数，也可以是非正数。


>这里设置的值必须为`Dp`，`Compose`为我们在Int中扩展了一个方法`dp`，帮我们转换成`Dp`。

### 2.Modifier属性调用顺序
Modifier是利用 kotlin 扩展函数实现的，每个方法的返回值都是Modifier 因此可以实现链式调用。由于每个函数都会对上一个函数返回的 Modifier 进行更改，因此先后顺序会影响最终结果。
例如:
```
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            Column {
                Text(
                    "Hello Compose One",
                    fontSize = 20.sp,
                    modifier = Modifier
                        .padding(10.dp)
                        .clickable(onClick = {})
                        .widthIn(100.dp, 200.dp)

                )
                Text(
                    "Hello Compose Two",
                    fontSize = 20.sp,
                    modifier = Modifier
                        .clickable(onClick = {})
                        .padding(10.dp)
                        .widthIn(100.dp, 200.dp)
                )
            }
        }
    }
}
```
我们给Modifier设置的padding边距和clickable点击事件的先后顺序不同,会导致组件的可点击区域也会不一样:
![](https://img-blog.csdnimg.cn/img_convert/15e8b9984942860c77394c567e87d346.gif)
>modifier 只能设置 padding，没有 margin 属性。先设置了size尺寸再设置padding就是设置控件的内边距，先设置padding再设置size尺寸就是设置组件的外边距。所以，在 Modifier 中设置 padding 的次序很重要。
# 七.Compose常用的布局容器
![](https://img-blog.csdnimg.cn/img_convert/5696a1080ad8aee975d1c1b047ce774b.png)
### 1.Column垂直布局容器
添加Column，使布局垂直排列
```
Column {
  Text("张飞")
  Text("关羽")
}
```
![](https://img-blog.csdnimg.cn/img_convert/84784882202aa502699a51f7478b9df1.png)

Column源码:
```
@Composable
inline fun Column(
    modifier: Modifier = Modifier,
    verticalArrangement: Arrangement.Vertical = Arrangement.Top,
    horizontalAlignment: Alignment.Horizontal = Alignment.Start,
    content: @Composable ColumnScope.() -> Unit
) {
    ...
}
```
>Column 有两个属性 verticalArrangement 和 horizontalAlignment 来控制 child 的对齐摆放方式。

### 2.Row横向布局容器
```
Row {
    Text("张飞")
    Text("关羽")
    }
```
![](https://img-blog.csdnimg.cn/img_convert/f1d13e00a5d83faa5b8c64f2c65f140d.png)
Row源码:
```
@Composable
inline fun Row(
    modifier: Modifier = Modifier,
    horizontalArrangement: Arrangement.Horizontal = Arrangement.Start,
    verticalAlignment: Alignment.Vertical = Alignment.Top,
    content: @Composable RowScope.() -> Unit
) {
  ...
}
```
>Row 有两个属性 horizontalArrangement 和 verticalAlignment 来控制 child 的对齐摆放方式。

### 2.Box堆叠布局容器
类似于Android View 体系中的 FrameLayout
```
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            Box {
                Box(
                    Modifier
                        .size(200.dp, 200.dp)
                        .background(Color.Blue))
                Box(
                    Modifier
                        .size(100.dp, 100.dp)
                        .background(Color.Red))
            }
        }
    }
}
```
![](https://img-blog.csdnimg.cn/img_convert/a2e03b43d409eadedc4a8d14d6d8b840.png)
Box源码:
```
@Composable
inline fun Box(
    modifier: Modifier = Modifier,//修饰符
    contentAlignment: Alignment = Alignment.TopStart,//对齐方法
    propagateMinConstraints: Boolean = false,
    content: @Composable BoxScope.() -> Unit
) {
    ...
}
```
>Box 有个属性contentAlignment 来控制 child 的对齐摆放方式。

参考资料:
[Compose UI官方文档](https://developer.android.com/jetpack/compose/documentation?hl=zh-cn)
[compose资料](https://docs.compose.net.cn/)


[原创|Android Jetpack Compose 最全上手指南](https://juejin.cn/post/6844903999347359751)
[Jetpack-Compose](https://blog.csdn.net/m0_37667770/article/details/114542808)
[Android Jetpack Compose 超快速上手指南](https://juejin.cn/post/6877056735018745863)
[compose text组件](https://www.cnblogs.com/baiyuas/p/14988887.html)







