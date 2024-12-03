---
title: Flutter之常见控件
date: 2021-05-13
categories: 
  - Fluter开发
---

# Flutter列表控件
在 Flutter 中，ListView 可以沿一个方向（垂直或水平方向）来排列其所有子 Widget，常被用于需要展示一组连续视图元素的场景。
ListView 构造方法:
- ListView：仅适用于列表中含有少量元素的场景
- ListView.build：适用于子 Widget 比较多的场景
- ListView.separated：适用于需要设置分割线的场景
构造方法名 | 特点 |	使用场景
|-|-|-|
|ListView|一次性创建好所有子 Widget|适用于展示少量连续子 Widget 的场景。|
|ListView.build|提供了子 Widget 创建方法，仅在需要展示时才创建|适用于子 Widget 较多，且视觉效果呈现某种规律性的场景。|
|ListView.separated|提供了子 Widget 创建方法，仅在需要展示时才创建，且提供了自定义分割线的功能|适用于子 Widget 较多，且视觉效果呈现某种规律性、每个子 Widget 之间需要分割线的场景。|
 
### 1.ListView
可以通过设置 children 参数，将所有子 Widget 包含到 listView 中，但这种创建方法要求提前将所有子 Widget 一次性创建好，而不是等到真正需要在屏幕上显示时才创建，即这种方法是导致性能下降 。因此，这种方式只适合列表中含有少量元素的场景:
```
class ListPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: ListView(
        children: <Widget>[
          ListTile(
            leading: Icon(
              Icons.home,
              color: Colors.cyan, // 图标颜色
            ),
            title: Text("首页"),
            selected: true, // 设置状态为选中状态
          ),
          ListTile(
            leading: Icon(
              Icons.add_shopping_cart,
              color: Colors.black54,
            ),
            title: Text("购物车"),
          ),
          ListTile(
            leading: Icon(
              Icons.account_circle,
              color: Colors.black54,
            ),
            title: Text("我的"),
          )
        ],
      ),
    );
  }
}
```
### 2.ListView.builder
- itemBuilder：列表项的创建方法。当列表滚动到相应位置时，ListView 会调用该方法创建对应的子 Widget
- itemCount：列表项的数目。如果不设置或设置为空，则表示 ListView 为无限列表
- itemExtent：列表项高度。可选参数，但对于定高的列表项元素，建议设置该参数的值（不设置时，ListView 会动态的根据子 Widget 创建完成后的结果，决定自身的视图高度，以及子 Widget 在 ListView 中的相对位置）
```
class ListBuild extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: ListView.builder(
        itemBuilder: (context, index) => ListTile(
          leading: Icon(Icons.adb),
          title: Text("下标" + index.toString()),
        ),
        itemExtent: 46, // 列表项高度
        itemCount: 50, //列表项总数，不设置为无限加载
      ),
    );
  }
}
 ```

### 3.ListView.separatorBuilder
设置列表项之间的分隔线，可以根据下标设置不同的分隔线
```
class ListSeparated extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Android小白营"),
      ),
      body: ListView.separated(
        itemBuilder: (context, index) => GestureDetector(
          child: ListTile(
            leading: Icon(Icons.adb),
            title: Text("下标" + index.toString()),
          ),
          onTap: () => Fluttertoast.showToast(msg: index.toString()), // 列表项点击事件
        ),
        separatorBuilder: (BuildContext context, index) {
          divider divider;
          if (index % 2 == 0) {
            divider = Divider(
              thickness: 1, // 分隔线宽度
              height: 0,
              color: Colors.black12, // 分隔线颜色
            );
          } else {
            divider = Divider(
              thickness: 2,
              height: 0,
              color: Colors.deepOrangeAccent,
            );
          }
          return divider;
        },
        itemCount: 100,
      ),
    );
  }
}
```

# Flutter设置margin和padding
### 方式一使用Container包裹
用Container包裹起来然后在Container上面设置:
```
  padding: EdgeInsets.fromLTRB(10, 10, 15, 20),//内边距，里边的蓝块，需要给宽高
  margin: EdgeInsets.fromLTRB(100, 10, 15, 15),//外边距，父容器本身相对外部容器的移动
```
### 方式二使用Padding和SizedBox 组件
Flutter开发，万物皆Widget，对于内边距，我们一般是在目标控件包裹一层父级控件Padding，并通过Padding控件的padding属性指定内边距数值，例如:
统一指定上下左右的内边距
```
Padding(
  padding: const EdgeInsets.all(20.0),
  child: Text(text),
),
```
指定左侧内边距
```
Padding(
  padding: EdgeInsets.only(left: 20.0),
  child: Text(text),
),
```
指定上下左右内边距
```
Padding(
  padding: const EdgeInsets.fromLTRB(15.0, 10.0, 15.0, 10.0),//此处也可以使用EdgeInsets.only
  child: Text(text),
),
```
对于外边距，Flutter没有类似Padding的控件，但是很多时候我们又想要实现控件间的间距效果，这个时候SizedBox控件就派上用场了，它是一种类似于Android平台的space占位view，只占空间不显示，使用方法也很简单：

设置上下外边距
```
SizedBox(
  height: 20.0,
)
```
设置左右外边距
```
SizedBox(
  width: 20.0,
)
```
2.使用Spacer填充尽可能大的空间
```
Row(
  children: <Widget>[
      Text("1"),
      Spacer(), // use Spacer
      Text("2"),
  ],
)
```

# FlutterFlex弹性布局
### 弹性系数
如果为 0 或 null，则 child 是没有弹性的，即不会被扩伸占用的空间。
如果大于 0，所有的Expanded按照其flex的比例来分割主轴的全部空闲空间。

### Expanded占据剩余的空间
Expanded使用与类似与Column，Row，Flex等展示多个组件集合的组件，Expanded包含的组件可以占据剩余的空间。
Expanded组件可以使Row、Column、Flex等子组件在其主轴方向上展开并填充可用空间(例如，Row在水平方向，Column在垂直方向)。如果多个子组件展开，可用空间会被其flex factor(表示扩展的速度、比例)分割。
Expanded组件必须用在Row、Column、Flex内，并且从Expanded到封装它的Row、Column、Flex的路径必须只包括StatelessWidgets或StatefulWidgets组件(不能是其他类型的组件，像RenderObjectWidget，它是渲染对象，不再改变尺寸了，因此Expanded不能放进RenderObjectWidget)。
>注意一点：在Row中使用Expanded的时候，无法指定Expanded中的子组件的宽度width，但可以指定其高度height。同理，在Column中使用Expanded的时候，无法指定Expanded中的子组件的高度height，可以指定宽度width。

# Flutter给组件设置点击事件
- 在flutter 开发中用InkWell或者GestureDetector将某个组件包起来，可添加点击事件。
- GestureDetector 使用点击无水波纹出现，InkWell可以实现水波纹效果。
### 1. InkWell有点击效果
```
InkWell(
      onTap: (){},
      child: Container())
```
### 2. GestureDetector 设置点击
```
GestureDetector(
            child: Text("GestureDetector 点击"),
            onTap: () {})
```

# Flutter快捷键生成控件
- 输入stless就可以创建一个StatelessWidget。
- 输入stful就可以创建一个StatefulWidget。

# Flutter圆角控件
### 1.通过Card的shape属性
```
Card(
            shape: RoundedRectangleBorder(
                borderRadius: BorderRadiusDirectional.circular(20)),
            clipBehavior: Clip.antiAlias,
            child: Image.asset(
              "images/landscape0.jpeg",
              width: double.maxFinite,
            ),
          )
```
唯一值的注意的地方就是borderRadius看准了，不要用错了，要不然没效果。
### 2.通过Container的decoration
```
Container(
          decoration: ShapeDecoration(
              image: DecorationImage(
                  image: AssetImage("images/landscape1.jpeg"),
                  fit: BoxFit.fitWidth),
              shape: RoundedRectangleBorder(
                  borderRadius: BorderRadiusDirectional.circular(20))),
          width: double.maxFinite,
          height: 300,
          child: Align(
            child: Padding(
              padding: const EdgeInsets.all(8.0),
              child: Text(
                "Container decoration实现圆角(radius = 20)",
                style: TextStyle(color: Colors.white),
              ),
            ),
            alignment: Alignment.bottomCenter,
          ),
        )
```
使用的DecorationImage，相当于把图片当做一个背景，这里需要注意的就是Container的child的尺寸问题，就算不放内容，也需要设置一个带尺寸的child Widget。
### 3.直接使用ClipRRect
```
ClipRRect(
              borderRadius: BorderRadius.circular(20),
              child: Image.asset("images/landscape2.jpeg"),
            ),
```
这种方式是最简单的，直接使用即可。

# 装饰容器DecoratedBox
DecoratedBox可以在其子组件绘制前(或后)绘制一些装饰（Decoration），如背景、边框、渐变等。DecoratedBox定义如下：
```
/**
 * 在子控件绘制之前或之后绘制一个装饰
    const DecoratedBox({
    Key key,
    @required this.decoration,//要绘制的装饰器
    this.position = DecorationPosition.background,//绘制在子组件上面(DecorationPosition.background)还是下面(DecorationPosition.foreground)
    Widget child
    })
 */
```
- decoration：代表将要绘制的装饰，它的类型为Decoration。Decoration是一个抽象类，它定义了一个接口 createBoxPainter()，子类的主要职责是需要通过实现它来创建一个画笔，该画笔用于绘制装饰。
- position：此属性决定在哪里绘制Decoration，它接收DecorationPosition的枚举类型，该枚举类有两个值：
- background：在子组件之后绘制，即背景装饰。
- foreground：在子组件之上绘制，即前景。
BoxDecoration
我们通常会直接使用BoxDecoration类，它是一个Decoration的子类，实现了常用的装饰元素的绘制。
定义：
```
/** 装饰器，可以用来修饰其他的组件，和Android里面的shape很相似
    const BoxDecoration({
    this.color,//背景色
    this.image,//图片
    this.border,//描边
    this.borderRadius,//圆角大小
    this.boxShadow,//阴影
    this.gradient,//过度效果
    this.backgroundBlendMode,//背景混合模式
    this.shape = BoxShape.rectangle,//形状,BoxShape.circle和borderRadius不能同时使用
    })
 */
```

# Flutter Container组件宽度撑满屏幕
在flutter开发中，如果不给Container组件设置宽度的话，它的宽度是取决于子组件的宽度，如何给Container设置撑满屏幕的宽度呢？
以下两种方式都可：
```
Container(
  color: Colors.red,
  width: MediaQuery.of(context).size.width,
  child: Text("宽度有多宽"),
)
```
```
Container(
  color: Colors.red,
  width: double.infinity,
  child: Text("宽度有多宽"),
)
```

# Flutter中的颜色
### 1.常规使用
Flutter中颜色的设置有很多方法，但是一般我使用的有4种.
```
Color c1 = Color(0xFF3CAAFA);
Color c2 = Color.fromRGBO(60, 170, 250, 1);
Color c3 = Color.fromARGB(255, 60, 170, 250);
Color c5 = Colors.blue;
```
1. Color(int value)
Color(0xFF3CAAFA),value接收的是一个十六进制（0x开头),FF表示的是十六进制透明度(00-FF),3CAAFA是十六进制色值。

2. Color.fromRGBO(int r, int g, int b, double opacity)
Color.fromRGBO(60, 170, 250, 1)，r、g、b分别表示red、green、blue，常规的红绿蓝三色，取值范围为0-255，opacity表示透明度，取值0.0-1.0。

3. Color.fromARGB(int a, int r, int g, int b)
Color.fromARGB(255, 60, 170, 250),a表示透明度，取值0-255，rgb同上一样。

4. Colors._()
Colors类定义了很多颜色，可以直接使用，例如 Colors.blue,其实就是第一种Color(int value)的封装。

### 2.在Flutter中使用16进制颜色
##### (1.)方法一: 使用原生方法
Flutter中, Color类仅接收整数作为参数. 你也可以使用fromARGB或者fromRGBO.

比如拿到了一个16进制颜色#b74093. 因为Color还需要传入透明度, 255就是最大值(也就是不透明), 转为16进制就是0xFF, 所以我们只需这样表示:
```
const color = Color(0xffb74093);
```
正规一点的写法(可选, 因为大小写不敏感):
```
const color = Color(0xFFB74093);
```
##### (2.)方法二: 接收字符串格式, 转为Color
创建一个HexColor类:
```
class HexColor extends Color {
  static int _getColorFromHex(String hexColor) {
    hexColor = hexColor.toUpperCase().replaceAll("#", "");
    if (hexColor.length == 6) {
      hexColor = "FF" + hexColor;
    }
    return int.parse(hexColor, radix: 16);
  }

  HexColor(final String hexColor) : super(_getColorFromHex(hexColor));
}
```
然后进行调用:
```
Color color1 = HexColor("b74093");
Color color2 = HexColor("#b74093");
Color color3 = HexColor("#88b74093");
```

### 3.封装Color使用
```
class Colours {
  static const Color app_main = Color(0xFFFE9A4E);
  static const Color dark_app_main = Color(0xFFFE9A4E);

}

```
调用：
```
theme: ThemeData(
		...
        primaryColor: Colours.colorPrimary,
        primaryColorDark: Colours.colorPrimaryDark,
        accentColor: Colours.colorAccent,
        dividerColor: Colours.dividerColor,
      ),
```

# Flutter根据状态显示隐藏widget
### 1.占位方案
```
buildTestWidget() {
    if (xxx) {
        // 真正需要展示的空间
        return Widget();    
    } else {
        // 空白的占位符，不能返回null
        return Container(
            width: 0,
            height: 0
        );
    }

```

### 2.Visibility控件
```
Visibility(
  child: Text("不可见"),
  maintainSize: true, 
  maintainAnimation: true,
  maintainState: true,
  visible: false, ), //false 为不可见
```

### 3.Offstage控件
offstage为true时表示不渲染，也不占位，相当于gone。
```
Offstage(
  offstage: true, //这里控制 true  false 布尔值
  child: '子控件',
),
```

### 4.可以通过if条件控制控件的显示或隐藏
用 Row 或者 Column 控件，控件里面有一个包含Widget的list，所以可以根据条件把需要展示的 Widget 放入 list 中，然后再使用 Row 或 Column 控件来展示 list，达到控制显示还是不显示的目的。
```  
   Column(
     children: <Widget>[
       if (show) Text("根据show值显示或隐藏"),
       Text("始终显示"),
     ],)
```

### 5.使用Opacity控件
opacity 其实是根据visible 控制透明度而已，其实还是占位的，相当于invisible，而且也是会渲染绘制的。
```
     Opacity(
                 opacity: visible ? 1.0 : 0.0,
                 child: Padding(
                   padding: EdgeInsets.all(30),
                   child: Text('Now you see me, now you don\'t!'),
                 ),
               ),

```

# Flutter中的输入框
TextField输入框
### 1.获取输入内容
获取输入内容有两种方式：
- 定义两个变量，用于保存用户名和密码，然后在onChange触发时，各自保存一下输入内容。
- 通过controller直接获取。

### 2.监听文本变化
监听文本变化也有两种方式：
- 设置onChange回调
```
  TextField(
       autofocus: true,
       onChanged: (v) {
         print("onChange: $v");
       }
   )
```
- 通过controller监听
```
 @override
   void initState() {
     //监听输入改变  
     _unameController.addListener((){
       print(_unameController.text);
     });
   }
```
>onChanged是专门用于监听文本变化，而controller的功能却多一些，除了能监听文本变化外，它还可以设置默认值、选择文本

# Flutter中的常见错误
### 1. Navigator operation requested with a context that does not include a Navigator.
```
class  MyApp  extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        body: Center(
          child: FlatButton(
              onPressed: () {
                Navigator.of(context).push(
                    MaterialPageRoute(builder: (context) => SecondPage()));
              },
              child: Text('跳转')),
        ),
      ),
    );
  }
}
```
当我们在 build 函数中使用Navigator.of(context)的时候，这个context实际上是通过 MyApp 这个widget创建出来的Element对象，而of方法向上寻找祖先节点的时候（MyApp的祖先节点）并不存在MaterialApp，也就没有它所提供的Navigator。
所以当我们把Scaffold部分拆成另外一个widget的时候，我们在FirstPage的build函数中，获得了FirstPage的BuildContext，然后向上寻找发现了MaterialApp，并找到它提供的Navigator，于是就可以愉快进行页面跳转了。

# Flutter的TabBar组件（顶部Tab切换组件）
### 1.TabBar组件的常用属性
|属性|描述|
|-|-|
|tabs	|显示的标签内容，一般使用 Tab 对象,也可以是其他的Widget |
|controller|TabController 对象|
|isScrollable|是否可滚动|
|indicatorColor|指示器颜色|
|indicatorWeight|指示器高度|
|indicatorPadding|底部指示器的 Padding|
|indicator|指示器 decoration，例如边框等|
|indicatorSize|指示器大小计算方式，TabBarIndicatorSize.label 跟文字等宽,TabBarIndicatorSize.tab 跟每个 tab 等宽|
|labelColor|选中 label 颜色|
|labelStyle|选中 label 的 Style|
|labelPadding|每个 label 的 padding 值|
|unselectedLabelColor|未选中 label 颜色|
|unselectedLabelStyle|未选中 label 的 Style|

### 2.TabBar的实现方式1（不常用）
```
import 'package:flutter/material.dart';

void main() {
  runApp(
    MaterialApp(
      home: DefaultTabController(
        length: 6,
        child: Scaffold(
          appBar: AppBar(
              title: Text("TabBarDemo"),
              bottom: TabBar(
                tabs: <Widget>[
                  Tab(text: "热门"),
                  Tab(text: "推荐"),
                  Tab(text: "关注"),
                  Tab(text: "收藏"),
                  Tab(text: "新增"),
                  Tab(text: "点赞"),
                ],
              ),
          ),
          body: TabBarView(
            children: <Widget>[
              Center(
                child: Text("这是热门的内容")
              ),
              Center(
                  child: Text("这是推荐的内容")
              ),
              Center(
                  child: Text("这是关注的内容")
              ),
              Center(
                  child: Text("这是收藏的内容")
              ),
              Center(
                  child: Text("这是新增的内容")
              ),
              Center(
                  child: Text("这是点赞的内容")
              )
            ],
          ),
        ),
      ),
    )
  );
}
```

### 3.TabBar的实现方式2（常用）
```
import 'package:flutter/material.dart';

void main() {
  runApp(MaterialApp(
    title: "TabBarWidget",
    home: MyApp(),
  ));
}


class MyApp extends StatefulWidget {
  @override
  _MyAppState createState() => _MyAppState();
}


class _MyAppState extends State<MyApp> with SingleTickerProviderStateMixin{
  TabController _tabController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(vsync: this,length: 6);
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("顶部Tab切换"),
        bottom: TabBar(
          tabs: <Widget>[
            Tab(text: "热门"),
            Tab(text: "推荐"),
            Tab(text: "关注"),
            Tab(text: "收藏"),
            Tab(text: "新增"),
            Tab(text: "点赞"),
          ],
          controller: _tabController,  // 记得要带上tabController
        ),
      ),
      body: TabBarView(
        controller: _tabController,
        children: <Widget>[
          Center(
              child: Text("这是热门的内容")
          ),
          Center(
              child: Text("这是推荐的内容")
          ),
          Center(
              child: Text("这是关注的内容")
          ),
          Center(
              child: Text("这是收藏的内容")
          ),
          Center(
              child: Text("这是新增的内容")
          ),
          Center(
              child: Text("这是点赞的内容")
          )
        ],
      ),
    );
  }
}
```
flutter TabBarView 没有跟Scaffold 一起使用的时候，容易报 Horizontal viewport was given unbounded height 错误，例如将其作为Column的子元素，就会出现该错误。错误提示意思是水平视图高是无限的，这里由于是用在Column中， 所以水平应该理解为垂直方向。解决该问题就是需要在其父级添加高度限制。
例如在其外层包裹Expanded，并设置flex。如下：
```
Widget build(BuildContext context) {
    return Column(
      children: <Widget>[
        header(),// 自定义组件
        Expanded(// 设置高度。直接将TabBarView作为Column子元素，而不设置高度，会报错
          flex: 1,
          child: TabBarView(....),// 省略无关代码
        ),
      ],
    );
  }
```
**写动态tabbar将 singleTickerProviderStateMixin 改成 TickerProviderStateMixin 才能调用setState重绘**
```
class _TravelPageState extends State<TravelPage> with TickerProviderStateMixin{
  TabController _tabController;
  TravelTabModel travelTabModel;
  List<TravelTab> tabs = [];
  @override
  void initState() {
    _tabController = TabController(length: 0, vsync: this);
    TravelTabDao.fetch().then((TravelTabModel model){
      print(model);
      _tabController = TabController(length: model.tabs.length, vsync: this);
      setState(() {
       tabs = model.tabs;
       travelTabModel = model;
      });
    }).catchError((e){
      print(e);
    });
    super.initState();
  }
```

# Flutter中的状态栏 
通过SafeArea包裹内容来防止布局的内容填充到状态栏里面。

# Flutter的嵌套层级深
解决方法
解决Flutter Widget地狱的方法有很多种，根据我的开发经验，着重介绍以下几种方法。

- 将组件转化为方法，这一种方式非常常用。
- 将组件转化为 StatelessWidget 或者 StatefulWidget ，我们习惯只把重复用到的组件做封装，实际上这样写更好，这个我会在后面提到。
- 第三种灵感来自于掘金的一篇文章《Flutter嵌套深？扩展函数了解一下》，有兴趣的朋友可以看一下。

# Flutter 自定义 Widget 的方式
当我们在实际开发中，可能 Flutter 的基础 Widget 组件并不能满足我们的需求，这时我们就需要自定义 Widget 来实现我们的需求。
Flutter 有多种实现自定义 Widget 的方式：
- 通过继承 Widget 来修改和扩展它的功能；
- 通过组合 Widget 来扩展功能；
使用 CustomPaint 绘制自定义 Widget。这几种方式都有各自的优势和特点，相对来说 CustomPaint 绘制实现自定义是这里面比较复杂的一种自定义 Widget 方式。
Flutter 中的很多基础 Widget 也是通过继承 Widget 进行扩展形成新的 Widget 或者是自己绘制 Widget。其实在大部分的平台都存在 Canvas 这个对象，它可以实现绘制布局、组件等功能，
当然 Flutter 也可以通过 Canvas 来实现 Widget 的绘制。自定义Widget 在开发中也非常常见，例如：我们可以自定义封装实现一个加载中的对话框、实现一个通用的 ToolBar 等等。


[『Flutter』组件通信传值学习](https://www.jianshu.com/p/879ee03cab23)
[Flutter | 深入理解BuildContext](https://juejin.cn/post/6844903777565147150)
[Dio官方文档](https://github.com/flutterchina/dio/blob/master/README-ZH.md)
[Flutter基础（十一）网络请求（Dio）与JSON数据解析](https://juejin.cn/post/6844903902182113288)
[Flutter如何高效的JSON转Model](https://juejin.cn/post/6844904039340048391)
[Flutter动态加载TabBar](https://blog.csdn.net/xudailong_blog/article/details/98967330)
[善用 Provider 榨干 Flutter 最后一点性能](https://juejin.cn/post/6844904057321046029)
[实操flutter避免嵌套地狱的5种方法](https://zhuanlan.zhihu.com/p/182985171)
