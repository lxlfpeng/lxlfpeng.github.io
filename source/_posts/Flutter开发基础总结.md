---
title: Flutter开发基础总结
---

# 一.命令式UI和声明式UI
### 1. 命令式编程和声明式编程的区别
命令式编程：命令“机器”如何去做事情(how)，这样不管你想要的是什么(what)，它都会按照你的命令实现。
声明式编程：告诉“机器”你想要的是什么(what)，让机器想出如何去做(how)。

### 2. Flutter中命令式编程的应用
在Flutter中每个组件，会有个build函数，这里会返回一个能够完整描述UI的对象结构。每当数据改变时，就重新调用build函数，返回新的结构。
如何高效渲染，就是框架去做的事情了。通过这种方式，不管是UI的初始布局结构，还是后面的修改，都是build函数返回的对象结构去声明的，完整的声明式UI由此而来。
所以Flutter是构建新的widget实例，而不是改变旧的实例。

# 二.Flutter中的Widget
Flutter 中Widget 是一切的基础,一切的显示都是 Widget,利用响应式模式进行渲染。在 Flutter 中自定义组件就是一个类，这个类需要继承 ``StatelessWidget\StatefulWidget``。
Widget 分为 ``有状态(StatefulWidget)`` 和 ``无状态(StatelessWidget)`` 两种，在 Flutter 中每个页面都是一帧，无状态就是保持在那一帧，而有状态的 Widget 当数据更新时，其实是创建了新的 Widget，
只是 State 实现了跨帧的数据同步保存。

## 1. 无状态StatelessWidget
### (1.)定义
如果一个控件的UI页是静态的，也就是一旦这些UI页被成功渲染之后就不需要也不可能去改变他的状态，例如纯展示页面。就使用StatelessWidget。在需要实现一个StatelessWidget组件的时候，
声明一个class类extends继承StatelessWidget，必须要重写 build 方法，这个 build 方法会携带一个 BuildContext 参数。另外 build 方法返回一个 Widget 值，也就是我们自定义的无状态的布局。
这样就可以创建一个无状态的Widget。StatelessWidget 的 构造方法 和 build 方法之会创建一次，不会随着子节点StatefulWidget 控件的状态改变而重构布局。所以它适合放在布局嵌入比较深的布局节点，
又因为StatelessWidget是静态的，所以性能比较好，建议多使用。

>注意： 如果无状态Widget里面有子Widget，并且子Widget是有状态的，则子Widget的内容是可以通过setState来更改的。无状态Widget影响的仅仅是自己是无状态的，不会影响他的父Widget和子Widget。

### (2.)使用
flutter系统中提供了许多的已经定义好的StatelessWidget，例如StatelessWidget：StatelessWidget、 Icon、 IconButton、Text等。
```
class CircleAvatar extends StatelessWidget {}
class Icon extends StatelessWidget {}
class Text extends StatelessWidget {}
class IconButton extends StatelessWidget {}
```
Widget 和 Widget 之间通过 child: 进行嵌套。其中有的 Widget 只能有一个 child；有的 Widget 可以多个 child ，也就是children，比如` Column 布局。

StatelessWidget 是不能调用setState函数的。
例如：
```
class HomePage extends StatelessWidget {
  int countNum = 1; 
  @override
  Widget build(BuildContext context) {
    return Column(
      children: <Widget>[
        SizedBox(height: 200),
        Text("${ this.countNum }"),
        SizedBox(height: 20),
        RaisedButton(
          child: Text("按钮"),
          onPressed: (){
            setState()   // 错误写法 没法改变页面里面的数据
          this.countNum++;
              print(this.countNum);
          }
        )
      ]
    );
  }
}
```

## 2.有状态StatefulWidget
### (1.)定义
StatefulWidget是可变状态的widget。StatefulWidget依赖的数据在Widget生命周期中可能会频繁的发生变化。当使用StatefulWidget依赖的数据发生变化时调用setState函数时，
会通知Flutter框架某个状态发生了变化，Flutter会重新运行build方法，应用程序变可以显示最新的状态，Widget只是视图的“配置信息”，是数据的映射。
### (2.)使用
flutter系统中提供了许多的已经定义好的StatefulWidget，例如Checkbox, Radio, Slider, InkWell, Form, 和 TextField 都是有状态的widget，也是StatefulWidget的子类。
```
class Checkbox extends StatefulWidget {}
class Radio<T> extends StatefulWidget {}
class Slider extends StatefulWidget {}
```

自定义 StatefullWidget :
```
class HomePage extends StatefulWidget {
  HomePage({Key key}) : super(key: key);
  _HomePageState createState() => _HomePageState();
}
class _HomePageState extends State<HomePage> {
  int countNum = 0;
  @override
  Widget build(BuildContext context) {
    return Column(
      children: <Widget>[
        SizedBox(height: 200),
        Chip(
          label:Text('${this.countNum}') ,
        ),
        SizedBox(height: 20),
        RaisedButton(
          child: Text('按钮'),
          onPressed: (){
             setState(() {   // 只有有状态组件里面才有
                  this.countNum++;
             });
          }
        )
      ]
    );
  }
}
```

### (3.)State概念
每一个 StatefulWidget 类都会对应一个 State 类，State 表示与其对应的 StatefulWidget 要维护的状态，保存的状态信息可以在 build 时被获取，
同时，在 widget 生命周期中可以被改变，改变发生时，可以调用其 setState() 方法通知 framework 发生改变，framework 会重新调用 build 方法重构 widget 树，最终完成更新 UI 的目的。 
state 中包含两个常用属性：``widget`` 和 ``context``。widget 属性表示当前正在关联的 widget 实例，但关联关系可能会在 widget 重构时发生变化（framework 会动态设置 widget 属性为最新的widget 对象）。context 属性是 buildContext 类的实例，表示构建 widget 的上下文，每个 widget 都有一个自己的 context 对象，
它包含了查找、遍历当前 widget 树的方法。

### (3.)State的生命周期
如下代码:
```
class TestStateWidget extends StatefulWidget {
  @override
  _TestStateWidgetState createState() => _TestStateWidgetState(text);
}
class _TestStateWidgetState extends State<TestStateWidget> {
  _TestStateWidgetState(this.text);
  @override
  void initState() {
    ///初始化，这个函数在生命周期中只调用一次
    super.initState();
  }
  @override
  void dispose() {
    ///销毁
    super.dispose();
  }
  @override
  void didChangeDependencies() {
    ///在initState之后调 Called when a dependency of this [State] object changes.
    super.didChangeDependencies();
  }
  @override
  Widget build(BuildContext context) {
    return Container(
    ...
    );
  }
}
```
State 中主要的声明周期有 ：
- initState：初始化，理论上只有初始化一次。
- didChangeDependencies：在 initState 之后调用，此时可以获取其他 State 。
- dispose：销毁，只会调用一次。

### 3.Flutter自定义Widget
上文也讲到了在Flutter开发中，可以继承自StatelessWidget或者StatefulWidget来创建自己的Widget类；
- StatelessWidget： 没有状态改变的Widget，通常这种Widget仅仅是做一些展示工作而已；
- StatefulWidget： 需要保存状态，并且可能出现状态改变的Widget；

build方法什么情况下被执行呢：
1. 当我们的StatelessWidget第一次被插入到Widget树中时（也就是第一次被创建时）；
2. 当我们的父Widget（parent widget）发生改变时，子Widget会被重新构建；
3. 如果我们的Widget依赖InheritedWidget的一些数据，InheritedWidget数据发生改变时；

# 三. StatefulWidget的状态管理
### 1.widget的状态
我们知道在Flutter 内一切皆 Widge。runApp函数接受给定的Widget并使其成为widget树的根。
Widget描述了他们的视图在给定其当前配置和状态时应该看起来像什么。widget 的主要工作是通过实现 build 函数 来构建自身。
当widget调用build 函数时就会绘制出一帧静止的画面.当需要widget进行改变的时候就要不断地调用widget的build 函数进行绘制.
我们将widget对应的每一帧画面称作为一个状态.当widget的状态发生变化时，widget会重新构建UI，Flutter会对比前后变化的不同以确定底层渲染树从一个状态转换到下一个状态所需的最小更改.

>注意:通常我们所说的StatefulWidget是有状态的组件，意思不是说StatefulWidget类本身是可变的，实际上StatefulWidget类本身也是不变的，StatefulWidget持有的state状态
是在该对应widget整个生命周期内一直存在的，
也是因为有了这个state状态，我们就可以通知Flutter框架某一个状态发生了变化，Flutter会重新运行build方法来重新绘制界面。这里的有状态指的是创建时需要指定一个 State ，
在需要更新 UI时调用 setState(VoidCallbackfn)，并在 VoidCallback 中改变一些些变量数值等，组件会重新 build 以达到数显状态/UI的效果。

### 2.widget的状态改变的实现
来看一下Widget的源码：

```
@immutable
abstract class Widget extends DiagnosticableTree {
    // ...
}
```
@immutable实际上是一个注解 被@immutable注解标明的类或者子类都必须是不可变的也就是说定义到Widget中的数据一定是不可变的，需要使用final来修饰.
StatelessWidget是没有状态得因此它里面的数据通常是直接定义完后就不修改的。StatefulWidget需要有状态（可以理解成变量）的改变,既然我们在上面源码里面分析了Widget是不可变，
那么StatefulWidget如何来存储可变的状态呢？Flutter是靠将StatefulWidget设计成了两个类来实现状态的变化的:
- 一个类继承自StatefulWidget，作为Widget树的一部分；
- 一个类继承自State，用于记录StatefulWidget会变化的状态，并且根据状态的变化，构建出新的Widget；
这样设计的原因是因为在Flutter中，只要数据改变了Widget就需要重新构建（rebuild）


### 3.widget的状态管理的方式
状态管理就是一些能够引发界面状态改变的变量进行管理.这些变量需要在多个组件或者是路由界面中使用，所以就有了状态管理。
目前状态管理的方式有三种:
- Widget管理自己的状态。
- 父Widget管理子Widget状态。
- 混合管理（父Widget和子Widget都管理状态）。
如果某些状态只需要在自己的Widget中使用即可,Widget树中的其它部分并不需要访问这个状态.那么我们可以通过widget 管理自己的 state.比如选择框的选中状态.
但是如果某些状态需要在多个部分进行共享,那我们只有通过父 widget 管理子 widget 状态或者混合管理来实现了.比如用户的登录状态信息.

>一般的原则是：如果状态是组件私有的，则应该由组件自己管理；如果状态要跨组件共享，则该状态应该由各个组件共同的父元素来管理.

### 4. 跨widget跨页面状态管理
上面说到跨组件状态管理我们一般是通过父Widget管理子Widget状态来实现.例如A组件嵌套B,C两个兄弟组件,B组件有一个B1组件,C组件有一个C1组件.如果B1和C1组件需要共享一个状态,
那实现起来就非常麻烦,我们需要这个状态放到A组件中再通过B组件和C组件将整个状态传递到B1组件和C1组件组件中去.
通过这种方式我们可以发现B,C两个组件本身并不需要这个共享的状态,但是他们作为中转组件也必须要持有这个状态,如果随着层架的增加这种情况还会更加严重.我们如果在不同的Widget之间将状态传递来、传递去，
那么是无穷尽的，并且代码的耦合度会变得非常高，牵一发而动全身，无论是代码编写质量、后期维护、可扩展性都非常差。并且有的状态是需要跨页面共享的,例如登录状态.传递起来就更麻烦了.
这时，正确的做法是通过一个全局状态管理器来处理这种相距较远的组件之间的通信。目前主要有两种办法：

- 实现一个全局的事件总线EventBus，需要这个状态的组件可以通过订阅这个状态的通知,在收到通知后调用setState(...)方法重新build一下自身即可。
- 使用一些专门用于状态管理的包，如Provider、GetX、Redux等专门管理状态的工具包进行管理.(后续我会讲解这些包的使用)

# 三.常见的Widget
### 1.容器
Flutter 中拥有需要将近30种内置的 容器Widget，其中常用有 Container、Padding、Center、Flex、Stack、Row、Column、ListView 等.
例如:
- Row，是水平方向的线性布局（linearlayout）
- Column，是垂直方向的线性布局（linearlayout）
- Stack，可以理解成为相对布局。
```
class MyApp extends StatelessWidget{
  @override
  Widget build(BuildContext context) {
    return new MaterialApp(
      title: 'Welcome to Flutter',
      home: new Scaffold(
        appBar: new AppBar(
          title: new Text('Welcome to Flutter'),
        ),
        body: new Center(
          child: new Column(
            children: <Widget>[
              new Text('Text 1'),
              new Text('Text 2'),
              new Text('Text 3')
            ],),),),);}
}
```
### 2.页面
Flutter 中除了布局的 Widget，还有交互显示的 Widget 和完整页面呈现的Widget，其中常见的有Scaffold等.

# 四. widget事件
这里分两种情况,一种是widget 本身支持事件监测,另外一种是widget不支持事件检测.
### 1.widget 本身支持事件,
如果 widget 本身支持事件监测，直接传递给它一个函数，并在这个函数里实现响应方法。例如，RaisedButton、IconButton、OutlineButton、Checkbox、SnackBar、Switch等。
```

class SampleApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
    body:Center(
      child: MaterialButton(
        child: Text('click me'),
         onPressed: (){
            print('on click')
         );
      }),
     ),
    );
  }
}

``` 
### 2. widget 本身不支持事件,
如果 widget 本身不支持事件监测，则在外面包裹一个 GestureDetector(或者支持事件的widget例如: InkWell)，并给它的属性传递一个onTap函数：
```
class SampleApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: GestureDetector(
          child: Text('click me'),
          onTap: () {
           print('on click')
          },
        ),
      ),
    );
  }
}
```
###  3. widget 手势事件
|  函数   | 说明  |
|  ----  | ----  |
onTapDwon	| 当按下屏幕时触发
onTap	|当与屏幕短暂地触碰时触发，最常用
onTapUp	|当用户停止触碰屏幕时触发
onTapCancel	|当用户触摸屏幕，但没有完成Tap事件时触发
onDoubleTap	|快速双击屏幕时触发
onLongPress	|当长按屏幕时触发（与屏幕接触事件必须超过500ms）
onPanUpdate	|当在屏幕上移动时触发
onVerticalDragDown	|当手指触碰屏幕且准备往屏幕垂直方向移动时触发
onVerticalDragStart	|当手指触碰屏幕且开始往屏幕垂直方向移动时触发
onVerticalDragUpdate	|当手指触碰屏幕且开始往屏幕垂直方向移动并发生位移时触发
onVerticalDragEnd	|当用户完成垂直方向触摸屏幕时触发
onVerticalDragCancel	|当用户中断了onVerticalDragDown时触发
onHorizontalDragDown	|当手指触摸屏幕且准备往屏幕水平方向移动时触发
onHorizontalDragStart	|当手指触摸屏幕且开始往屏幕水平方向移动时触发
onHorizontalDragUpdate	|当手指触摸屏幕且开始往屏幕水平方向移动并发生位移时触发
onHorizontalDragEnd	|当用户完成水平方向触摸屏幕时触发
onHorizontalDragCancel	 |当用户中断了onHorizontalDragDown时触发
onPanDown	|当用户触摸屏幕时触发
onPanStart	|当用户触摸屏幕并开始移动时触发
onPanUpdate	|当用户触摸屏幕并产生移动时触发
onPanEnd	|当用户完成触摸屏幕时触发
onScaleStart	|当用户触摸屏幕并开始缩放时触发
onScaleUpdate	|当用户触摸屏幕并产生缩放时触发
onScaleEnd	|当用户完成缩放时触发

# 五.路由和导航
Flutter 中万物皆 Widget，页面自然也是一个 Widget。只不过是一个全屏的 Widget。在flutter中两种页面跳转方式:
- 无名路由跳转(一种动态构建路由的方式)。
- 命名路由跳转(一种提前命名路由的方式)。
### 1.无名路由跳转
直接使用使用 Navigator 跳转页面，在 Flutter 中，使用 Navigator 来进行页面跳转。一个简单的跳转页面的例子：
```
Navigator.push(
  context,
  MaterialPageRoute(
  // 目标页面，一个 Widget
    builder: (context) => PageA(),
  ),
);
```
或者
```
Navigator.of(context).push(
  MaterialPageRoute(
    builder: (context) => PageA(),
  ),
);
```
在A页面中关闭A页面返回到上一个页面:
```
Navigator.pop(context);
```
或者:
```
 Navigator.of(context).pop();
```
### 2.命名路由跳转
命名路由跳转需要先注册路由表,放在MaterialApp的 initialRoute 和 routes 中.命名路由路由存在的意义在于可以让我们更方便的导航到想要到达的页面，便于管理和维护。
要想使用命名路由，我们必须先提供并注册一个路由表（routing table），这样应用程序才知道哪个名字与哪个路由组件相对应。路由表的注册方式很简单，找到MaterialApp，添加routes属性，
```
void main() => runApp(MyApp());//单行函数调用写法
class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: "AppTitle",
      theme: ThemeData(primaryColor: Colors.green),
      initialRoute: "first_page",//初始路由页面,作用是定义APP启动时第一个显示的页面
      routes: {
        //路由注册表
        "first_page": (BuildContext context) => FirstPage(),  //当navigating到‘first_page’ route时，FirstPage widget
        "second_page": (BuildContext context) => SecondPage(), //当navigating到‘second_page’ route时，SecondPage widget
      },
    );
  }
}
```
要通过路由名称来打开新路由，可以使用Navigator 的pushNamed方法：
Future pushNamed(BuildContext context, String routeName,{Object arguments})
Navigator 除了pushNamed方法，还有pushReplacementNamed等其他管理命名路由的方法，读者可以自行查看API文档。通过刚刚注册的页面名称来跳转一个页面：
```
Navigator.pushNamed(context, 'first_page');// one_page表示页面别名
```
### 3.界面之间传递参数
传递的方式有两种:
- 通过构造方法中传递数据。
- 在Route中传递数据给下一个页面。
##### (1. )通过构造方法中传递数据
需要在接收数据的页面事先定义好构造方法，构造方法中定义要接收的参数。例如：我们在SecondPage中定义一个构造方法，构造方法中可以定义我们要接收的数据:
```
class SecondPage extends StatelessWidget {
  String data;
  PageB({this.data});
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Second页面"),
      ),
      body: Center(
        child: Text(data),
      ),
    );
  }
}
```
Frist页面跳转SecondPage页面时给传递数据：
```
Navigator.push(
  context,
  MaterialPageRoute(
    builder: (context) => SecondPage(
          data: "数据",
        ),
  ),
);
```
##### (2.)将参数传递给指定路由
构造方法参数参数的缺点不是太灵活。Flutter提供了把传递的参数放到Navigator中，然后传递给指定的路由，在接收的页面提取出需要的参数即可，这种方式更加灵活一些。
1. 首先要先定义好要传递的数据
例如：
我们先定义一个实体类：
```
class People {
  String name;
  int age;
  People(this.name, this.age);
}
```
2. 传递参数
将参数数据传递给SecondPage，可以有如下四种传参方式，效果都一样
第一种:
```
Navigator.pushNamed(
  context,
  second_page,
  arguments: People("张三", 30),//要传递的数据
);
```
第二种:
```
Navigator.of(context).pushNamed(second_page, arguments: People("张三", 30));
```
第三种:
```
Navigator.push(context,
   MaterialPageRoute(
     builder: (context) => SecondPage(),
     settings: RouteSettings(
       arguments: People("张三", 30),
     ),
   ),
 );
```
第四种
```
Navigator.of(context).push(
  MaterialPageRoute(
      builder: (context) => SecondPage(),
      settings: RouteSettings(
          arguments: People("张三", 30),
      )
  ),
);
```
3. 接收参数
在SecondPage接收数据时，数据要通过 ModalRoute.of 方法。此方法返回带有参数的当前路由。
```
class SecondPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    /*获取传递过来的参数*/
    People _people = ModalRoute.of(context).settings.arguments;

    return Scaffold(
      appBar: AppBar(
        title: Text("SecondPage"),
      ),
      body: Center(
        child: Text("name：${_people.name},age：${_people.age}"),
      ),
    );
  }
}
```
### 4.返回参数
路由打开页面后可以通过await 关键字等待路由返回参数.
```
class FirstPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Center(
      child: RaisedButton(
        onPressed: () async {
          // 打开`SecondPage`，并等待返回结果
          var result = await Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) {
                return SecondPage(
                  // 路由参数
                  text: "xxxx",
                );
              },
            ),
          );
          //输出路由返回结果
          print("路由返回值: $result");
        },
        child: Text("open SecondPage"),
      ),
    );
  }
}
```
通过Navigator.pop返回数据
```
class SecondPage extends StatelessWidget {
  TipRoute({
    Key key,
    @required this.text,  // 接收一个text参数
  }) : super(key: key);
  final String text;
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: EdgeInsets.all(18),
        child: Center(
          child: Column(
            children: <Widget>[
              Text(text),
              RaisedButton(
                onPressed: () => Navigator.pop(context, "我是返回值"),
                child: Text("返回"),
              )
            ],
          ),
        ),
      ),
    );
  }
}
```
### 5. 路由拦截
我们开发App的时候,有的界面无需要登录就可以查看例如新闻,视频等功能,但是有的界面如我的,收藏列表等页面需要登录才能查看.为了实现上诉功能通常的做法是
在打开每一个路由页前判断用户登录状态,但是每次打开路由前我们都需要去判断一下将会非常麻烦，可以用Flutter提供路由拦截来解决这种问题.MaterialApp有一个onGenerateRoute属性，
当调用Navigator.pushNamed(...)打开命名路由时，如果指定的路由名在路由表中已注册，则会调用路由表中生成路由组件；
如果路由表中没有注册，才会调用onGenerateRoute来生成路由。要实现制页面权限的功能就非常容易：在onGenerateRoute中进行统一的权限控制判断，如：
```
MaterialApp(
  ... 
   onGenerateRoute: (RouteSettings settings) {
        //isLogin 为登录逻辑的判断
        String routeName = isLogin ? settings.name! : "/login";
        return MaterialPageRoute(builder: (context) {
          switch (routeName) {
            case "/index":
              return MyHomePage();
            case "/login":
              return LoginScreen();
            default:
              return Scaffold(
                body: Center(
                  child: Text("页面不存在"),
                ),
              );
          }
        });
   }
  }
);
```

>onGenerateRoute只会对命名路由生效。

### 5.路由使用总结
建议最好统一使用命名路由的管理方式好处有：
- 语义化更明确。
- 代码更好维护；如果使用匿名路由，则必须在调用Navigator.push的地方创建新路由页，这样不仅需要import新路由页的dart文件，而且这样的代码将会非常分散。
- 可以通过onGenerateRoute做一些全局的路由跳转前置处理逻辑。

# 六. 资源管理
Flutter APP安装包中会包含代码和 assets（资源）两部分。Assets是会打包到程序安装包中的，可在运行时进行访问。常见类型的assets包括:
- 图标和图片（JPEG，WebP，GIF，动画WebP / GIF，PNG，BMP和WBMP） 
- 字体
- Json文件
- 静态数据(视频,声音)
 
### 1.加载图片
类似于Android原生开发，Flutter也可以为当前设备加载适合其分辨率的图像。

|dpi范围|密度|
|-|-|
0dpi ~ 120dpi|ldpi
120dpi ~ 160dpi|mdpi
160dpi ~ 240dpi|hdpi
240dpi ~ 320dpi|xhdpi
320dpi ~ 480dpi|xxhdpi
480dpi ~ 640dpi|xxxhdpi

##### (1.)声明分辨率相关的图片 assets
pubspec.yaml中asset添加不同设备像素比例的图片。

```
…/my_icon.png
…/2.0x/my_icon.png
…/3.0x/my_icon.png
```
在设备像素比率为1.8的设备上，.../2.0x/my_icon.png 将被选择。对于2.7的设备像素比率，.../3.0x/my_icon.png将被选择。

如果没有在Image widget上指定渲染图像的宽度和高度，那么Image widget将占用与主资源相同的屏幕空间大小。 
也就是说，如果是.../my_icon.png是72px乘72px，如果是.../3.0x/my_icon.png应该是216px乘216px;
pubspec.yaml中asset部分中的每一项都应与实际文件相对应，但主资源项除外。当主资源缺少某个资源时，会按分辨率从低到高的顺序去选择，也就是说1x中没有的话会在2x中找，2x中还没有的话就在3x中找。

### 2. 特定平台 assets
上面的资源都是flutter应用中的，这些资源只有在Flutter框架运行之后才能使用，如果要给我们的应用设置APP图标或者添加启动图，那我们必须使用特定平台的assets。

##### (1.)设置APP启动图标
**Android**
在Flutter项目的根目录中，导航到.../android/app/src/main/res目录，里面包含了各种资源文件夹（如mipmap-hdpi已包含占位符图像“ic_launcher.png”）。
 只需按照Android开发人员指南 (opens new window)中的说明， 将其替换为所需的资源，并遵守每种屏幕密度（dpi）的建议图标大小标准。

>注意: 如果您重命名.png文件，则还必须在您AndroidManifest.xml的<application>标签的android:icon属性中更新名称。

**iOS**
在Flutter项目的根目录中，导航到.../ios/Runner。该目录中Assets.xcassets/AppIcon.appiconset已经包含占位符图片， 只需将它们替换为适当大小的图片，保留原始文件名称。

##### (2.)启动页
**Android**
要将启动屏幕（splash screen）添加到您的Flutter应用程序， 请导航至.../android/app/src/main。在res/drawable/launch_background.xml，通过自定义drawable来实现自定义启动界面
（你也可以直接换一张图片）。

**iOS**
要将图片添加到启动屏幕（splash screen）的中心，请导航至.../ios/Runner。在Assets.xcassets/LaunchImage.imageset， 拖入图片，
并命名为LaunchImage.png、LaunchImage@2x.png、LaunchImage@3x.png。 如果你使用不同的文件名，那您还必须更新同一目录中的Contents.json文件，图片的具体尺寸可以查看苹果官方的标准。
您也可以通过打开Xcode完全自定义storyboard。在Project Navigator中导航到Runner/Runner然后通过打开Assets.xcassets拖入图片，或者通过在LaunchScreen.storyboard中使用Interface Builder进行自定义。

# 七.包管理与第三方库引入
### 1. YAML包管理
Flutter使用配置文件pubspec.yaml（位于项目根目录）来管理第三方依赖包。
pubspec.yaml:
```
name: flutter_in_action
description: First Flutter application.

version: 1.0.0+1

dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^0.1.2

dev_dependencies:
  flutter_test:
    sdk: flutter
    
flutter:
  uses-material-design: true
```  
下面，我们逐一解释一下各个字段的意义：

- name：应用或包名称。
- description: 应用或包的描述、简介。
- version：应用或包的版本号。
- dependencies：应用或包依赖的其它包或插件。
- dev_dependencies：开发环境依赖的工具包（而不是flutter应用本身依赖的包）。
- flutter：flutter相关的配置选项。
如果我们的Flutter应用本身依赖某个包，我们需要将所依赖的包添加到dependencies 下.
>需要注意dependencies和dev_dependencies的区别，前者的依赖包将作为APP的源码的一部分参与编译，生成最终的安装包。
>而后者的依赖包只是作为开发阶段的一些工具包，主要是用于帮助我们提高开发、测试效率，比如flutter的自动化测试包等。

### 2.依赖方式
有三种依赖方式:
##### 1. 依赖Pub仓库
[Pub](https://pub.dev/)是Google官方的Dart Packages仓库，类似于node中的npm仓库，android中的jcenter。我们可以在Pub上面查找我们需要的包和插件，也可以向Pub发布我们的包和插件。
我们也可以在控制台，定位到当前工程目录，然后手动运行flutter packages get 命令来下载依赖包。
##### 3. 依赖本地包
如果我们正在本地开发一个包，包名为pkgOne，我们可以通过下面方式依赖：
```
dependencies:
	pkg1:
        path: ../../code/pkgOne
```
路径可以是相对的，也可以是绝对的。
##### 3依赖git仓库
依赖Git：你也可以依赖存储在Git仓库中的包。如果软件包位于仓库的根目录中，请使用以下语法
```
dependencies:
  pkg1:
    git:
      url: git://github.com/xxx/pkg1.git
```
上面假定包位于Git存储库的根目录中。如果不是这种情况，可以使用path参数指定相对位置，例如：
```
dependencies:
  package1:
    git:
      url: git://github.com/flutter/packages.git
      path: packages/package1        
```

# 八.Json解析
由于Flutter禁用运行时反射，所以在Flutter中是没有GSON，Jackson这类解析JSON的库。
- 方案一:手写实体类
- 方案二:json_ serializable库生成实体类
- 方案三:json-to-dart插件自动生成实体类
### 1. 手动序列化JSON
手动解析通常应用在一些基本简单的场合，即数据结构不是很复杂的场景，手动解析JSON是指使用Flutter提供的dart:convert中内置的JSON解码器。
它能够将原始JSON字符串传递给json.decode() 方法，该方法可以根据JSON字符串具体内容将其转为List或Map,然后在返回的Map<String, dynamic>或者List中查找所需的值。
它不需要依赖任何第三方库，对于小项目来说很方便。
例如:
```
Map<String, dynamic> person = JSON.decode(jsonStr);
print('${person['name']}');
print('${person['age']');
```
>JSON.decode()返回一个Map<String, dynamic>，这意味着我们直到运行时才知道值的类型。失去了静态类型语言特性，代码非常容易出错。非常不推荐。

可以通过引入Model在模型类中序列化JSON来解决上述问题.
```
class Person {
  final String name;
  final String age;

  User(this.name, this.age);

  User.fromJson(Map<String, dynamic> json)
      : name = json['name'],
        age = json['age'];

  Map<String, dynamic> toJson() =>
    {
      'name': name,
      'age': age,
    };
}
```
使用时
```
Map personMap = JSON.decode(jsonStr);
var person = Person.fromJson(personMap);
print('${person.name}');
print('${person.age}');
```
通过Model调用代码可以具有类型安全、自动补全字段以及编译时异常等静态类型语言特性。如果拼写或者类型错误就不会通过编译，而不是在运行时崩溃。
不过在实际项目中JSON对象很少会这么简单，各种List和Map嵌套的JSON也是很常见的。如果每一个属性都通过手写来实现无疑是非常麻烦的。因此我们一般是不会手写的.

### 2.通过使用 json_serializable生成JsonModel
json_serializable是Google提供的一个自动化的源代码生成器，可以为我们生成JSON序列化模板。这种方案易维护，由于序列化数据代码不再需要手动编写或者维护，可以将序列化 JSON 数据在运行时的异常风险降到最低；
##### (1.)引入依赖
需要用到以下三个依赖包，通过代码自动生成的方式，生成模型。
- [json_annotation ](https://pub.dev/packages/json_annotation)
- [json_serializable ](https://pub.dev/packages/json_serializable)
- [build_runner](https://pub.dev/packages/build_runner)
在pubspec.yaml中添加依赖并执行flutter pub get：
```
dependencies:
  json_annotation: ^x.x.x

dev_dependencies:
  build_runner: ^1.0.0
  json_serializable: x.x.x
```
##### (2.)生成模型类
例如Json有如下Json文件
```
{
    "name": "张三",
    "age": "20",
    "tele": "13888888888"
}
```
编写生成模型类:
```
import 'package:json_annotation/json_annotation.dart'; 
part 'person.g.dart';// result.g.dart 将在我们运行生成命令后自动生成
@JsonSerializable()
  class Person extends Object {

  //定义字段
  @JsonKey(name: 'name')
  String name;

  @JsonKey(name: 'age')
  String age;

  @JsonKey(name: 'tele')
  String tele;

  Person(this.name,this.age,this.tele,); //定义构造方法

  factory Person.fromJson(Map<String, dynamic> srcJson) => _$PersonFromJson(srcJson); //固定格式，不同的类使用不同的mixin即可

  Map<String, dynamic> toJson() => _$PersonToJson(this); //固定格式

}
```
- 初次创建 Person.dart 的时候，需要加入 part 'Person.g.dart';
- 在需要转换的实体 dart 类 前加入 @JsonSerializable(nullable: false) 注解，标识需要 json序列化处理
- fromJson()、toJson() 方法的写法是固定模式，按模板修改即可
- Person.g.dart 和 文件名 需要保持一致，否则执行以下命令无效

因为实体类的生成代码还不存在,所以上代码会提示一-些错误是正常现象

当然如果我们不想手动编写这个生成类,也可以通过一些工具进行.[json2dart](https://caijinglong.github.io/json2dart/index_ch.html) 就是这样的一个工具.
工具使用很简单直接粘贴生成对应的类名称,此时我们将生成的代码copy出来创建一个文件在自己的工程中,或者直接下载文件放入工程中即可.

##### (3.)执行命令根据模型类,生成模型类代码.
一次性生成:
```
flutter packages pub run build_runner build
```
持续生成:
```
flutter packages pub run build_runner watch。
```
##### (4.)使用
```
Map person = JSON.decode(json);
var list = getPersonModel(person);
```
### 2.通过在线或者开发工具json-to-dart插件生成
Json2Dart在线插件:
[JSON to Dart](https://javiercbk.github.io/json_to_dart/)
[JSON To Model](https://czero1995.github.io/json-to-model/)
[quicktype](https://app.quicktype.io/)
或者在Android Studio里面装一个Dart2Json插件.

方案| 特点| 适合场景 
|-|-|-|
手写实体类| 耗时 |小型项目且json不复杂 
json_serializable| 需要定义字段、易维护 | 中大型项目
json-to-dart插件| 快速、易操作 | 任何类型的项目 

# 九.网络请求
flutter网络请求三种方式: 
- flutter自带的HttpClient
- 第三方库http 
- 第三方库Dio 
### 1. 原生方式(不建议使用)
1.1 get 请求
```
  void getNetData() async {
    var client = new HttpClient();
    var request = await client.getUrl(Uri.parse(url));
    var response = await request.close();
    if (response.statusCode == HttpStatus.ok) {
      _content = await response.transform(Utf8Decoder()).join();
    }
  }
```
### 2.库http(不建议使用)
##### (1.)get 请求
代码如下：
```
  void getNet() async {
    var client = http.Client();
    http.Response response = await client.get(url);
    _content = response.body;
  }
```
代码量比原生的简洁很多，然而还可以更简洁
```
  void getNet() {
    http.Client()
        .get(url)
        .then((http.Response response) {
              _content = response.body;
    });
  }
```
##### (2.)post 请求
```
  void postNet() async {
    var params = Map<String, String>();
    params["username"] = "xxxx";
    params["password"] = "xxxx";
 
    var client = http.Client();
    var response = await client.post(url_post, body: params);
    _content = response.body;
```

### 3. 库 dio(推荐使用)
官方提供的HttpClient和http都可以正常的发送网络请求，但是对于现代的应用程序开发来说，通常要求的东西会更多：比如拦截器、取消请求、文件上传/下载、超时设置等等；可以使用一个在Flutter中非常流行的三方库：[dio](https://github.com/flutterchina/dio/blob/master/README-ZH.md)；
>dio是一个强大的Dart Http请求库，支持Restful API、FormData、拦截器、请求取消、Cookie管理、文件上传/下载、超时、自定义适配器等…
pubspec.yaml 添加依赖：
```
dependencies:
  ...  
  dio: ^1.0.9
```
##### (1.)get 请求
```
  void getNet() async {
    Dio dio = new Dio();
    var response = await dio.get(url);
    _content = response.data.toString();
  }
```

##### (2.)post 请求
```
  void postNet() async {
    FormData formData = new FormData.from({
      "username": "xxxx",
      "password": xxxx,
    });
    var dio = new Dio();
    var response = await dio.post(url_post, data: formData);
    _content = response.data.toString();
  }
```
# 十.弹窗Dialog
Flutter中的操作提示主要有 ``SnackBar、BottomSheet、Dialog``
Flutter中也提供了很多Dialog 弹窗，如：``AboutDialog、AlertDialog、SimpleDialog、CupertinoAlertDialog、CupertinoFullscreenDialogTransition、BottomSheet``。
对话框本质上是属于一个路由的页面Route，由Navigator进行管理，所以控制对话框的显示和隐藏，也是调用Navigator.of(context)的push和pop方法。
在Flutter中，对话框会有两种风格，调用showDialog()方法展示的是material风格的对话框，调用showCupertinoDialog()方法展示的是ios风格的对话框。 
而这两个方法其实都会去调用showGeneralDialog()方法，可以从源码中看到最后是利用Navigator.of(context, rootNavigator: true).push()一个页面。
基本要传的参数:context上下文,builder用于创建显示的widget,barrierDismissible可以控制点击对话框以外的区域是否隐藏对话框。
showDialog()方法返回的是一个Future对象,可以通过这个future对象来获取对话框所传递的数据。 比如我们想知道想知道用户是点击了对话框的确认按钮还是取消按钮,那就在退出对话框的时候，
利用``Navigator.of(context).pop("一些数据")``;

在 MaterialDesign下，
Dialog主要有 3 种：
- SimpleDialog
- AlertDialog
- BottomSheet
### 1. SimpleDialog
```
void showMySimpleDialog(BuildContext context) {
    showDialog(
        context: context,
        builder: (context) {
          return new SimpleDialog(
            title: new Text("SimpleDialog"),
            children: <Widget>[
              new SimpleDialogOption(
                child: new Text("SimpleDialogOption One"),
                onPressed: () {
                  Navigator.of(context).pop("SimpleDialogOption One");
                },
              ),
              new SimpleDialogOption(
                child: new Text("SimpleDialogOption Two"),
                onPressed: () {
                  Navigator.of(context).pop("SimpleDialogOption Two");
                },
              ),
              new SimpleDialogOption(
                child: new Text("SimpleDialogOption Three"),
                onPressed: () {
                  Navigator.of(context).pop("SimpleDialogOption Three");
                },
              ),
            ],
          );
        });
  }
```
### 2. AlertDialog
```
void showMyMaterialDialog(BuildContext context) {
    showDialog(
        context: context,
        builder: (context) {
          return new AlertDialog(
            title: new Text("title"),
            content: new Text("内容内容内容内容内容内容内容内容内容内容内容"),
            actions: <Widget>[
              new FlatButton(
                onPressed: () {
                  Navigator.of(context).pop();
                },
                child: new Text("确认"),
              ),
              new FlatButton(
                onPressed: () {
                  Navigator.of(context).pop();
                },
                child: new Text("取消"),
              ),
            ],
          );
        });
  }
```
### 3. BottomSheet
```
showModalBottomSheet(
     context: context,
     backgroundColor: Colors.green,
     shape: RoundedRectangleBorder(
         borderRadius: BorderRadius.circular(10)),
     enableDrag: false,
     //设置不能拖拽关闭
     isDismissible: false,
     //设置不能点击消失
     builder: (BuildContext context) {
       return new Container(
           height: 300.0,
           child: Column(
             children: <Widget>[
               RaisedButton(
                 onPressed: () {
                   Navigator.of(context).pop();
                 },
                 child: Text("点击关闭"),
               ),
             ],
           ));
     },
   ).then((val) {
     print(val);
   });
```

### 4. 自定义弹窗
定义组件类来继承Dialog,添加build方法，return 自定义内容
```
class MyCustomLoadingDialog extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    Duration insetAnimationDuration = const Duration(milliseconds: 100);
    Curve insetAnimationCurve = Curves.decelerate;

    RoundedRectangleBorder _defaultDialogShape = RoundedRectangleBorder(
        borderRadius: BorderRadius.all(Radius.circular(2.0)));

    return AnimatedPadding(
      padding: MediaQuery.of(context).viewInsets +
          const EdgeInsets.symmetric(horizontal: 40.0, vertical: 24.0),
      duration: insetAnimationDuration,
      curve: insetAnimationCurve,
      child: MediaQuery.removeViewInsets(
        removeLeft: true,
        removeTop: true,
        removeRight: true,
        removeBottom: true,
        context: context,
        child: Center(
          child: SizedBox(
            width: 120,
            height: 120,
            child: Material(
              elevation: 24.0,
              color: Theme.of(context).dialogBackgroundColor,
              type: MaterialType.card,
              //在这里修改成我们想要显示的widget就行了，外部的属性跟其他Dialog保持一致
              child: new Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.center,
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  new CircularProgressIndicator(),
                  // Padding(
                  //   padding: const EdgeInsets.only(top: 20),
                  //   child: new Text("加载中"),
                  // ),
                ],
              ),
              shape: _defaultDialogShape,
            ),
          ),
        ),
      ),
    );
  }
}
```


Flutter相关教程:
[Flutter布局方式总](https://www.jianshu.com/p/88c66747eec1)
[Flutter 初尝试：入门教程](https://www.jianshu.com/p/e889c5d407a9) 
[GSY Flutter 系列专栏](https://guoshuyu.cn/home/wx/)
[flutter中文网](https://book.flutterchina.club/)
[Flutter入门进阶之旅](https://www.jianshu.com/u/794cff487721)
[Flutter基础--状态管理](https://www.cnblogs.com/qianxiaox/p/14025615.html)
[带你全面了解 Flutter，它好在哪里？它的坑在哪里？ 应该怎么学？](https://juejin.cn/post/6932033252320346126)
[Flutter教程](https://segmentfault.com/u/coderwhy)
[Flutter State Management状态管理全面分析](https://segmentfault.com/a/1190000022748118)
[Flutter 状态管理](https://blog.csdn.net/sinat_17775997/article/details/106658143)
[Flutter如何状态管理](https://juejin.cn/post/6998054516637745183)
[Flutter 网络请求框架封装](https://www.jianshu.com/p/3080e0b81cf4)

Flutter综合教程:
[Flutter教程](https://guoshuyu.cn/home/wx/Flutter-1.html)
[《Flutter实战》电子书](https://book.flutterchina.club/)
[w3c school](https://www.w3cschool.cn/flutter_in_action/flutter_in_action-i7rc3ez6.html)
[Flutter核心技术与实战](https://www.kancloud.cn/alex_wsc/flutter_demo/1559549)
[给 Android 开发者的 Flutter 指南](https://flutter.cn/docs/get-started/flutter-for/android-devs)
[Flutter页面跳转和传值传参，接收页面返回数据、以及解决返回（pop）页面时黑屏的问题](https://blog.csdn.net/yuzhiqiang_1993/article/details/89090742)





