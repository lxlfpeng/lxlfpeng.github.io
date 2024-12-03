---
title: Flutter使用Provider进行状态管理
date: 2020-11-08
categories: 
  - Fluter开发
---

### provider状态管理
几种常见情况，点击一个按钮,改变另外一个控件的值
思路: 首先给要改变值得控件绑定一个监听,${context.watch<Counter>().count}，如果点击按钮改变了数据,监听文字自动发生改变。

点击一个按钮,获取另外一个控件的值
思路:首先这个控件上显示的数据肯定不是死数据, 否则也没有获取的意义了,如果你说默认是死数据但是有可能会发生改变, 那么发生改变的时候应该用一个变量来控制。也就是先用${context.watch<Counter>().count}监听, 死数据也通过改变数据的方式来改变控件文字。这样获取的时候就用${context.read<Counter>().count}即可。

初始化数据后, 通过数据改变更改控件数据
思路:和第二种情况类似, 通过model来驱动视图。

看下 ChangeNotifierProvider 用法，一个单一的观察者模式
```
//继承ChangeNotifier后，可以通知所有订阅者
class Counter with ChangeNotifier {
  int _count = 0; //要保存的数据
  int get count => _count; //提供全局get方法获取计数总值
  void increment() {//提供全局方法，让全局计数+1
    _count++;
    notifyListeners(); //当数值改变后，通知所有订阅者刷新ui
  } 
}
 
runApp(
    /// Providers are above [MyApp] instead of inside it, so that tests
    /// can use [MyApp] while mocking the providers
//    MultiProvider(
//      providers: [
//        ChangeNotifierProvider(create: (_) => Counter()),
//      ],
//      child: MyApp(),
//    ),
    ChangeNotifierProvider(  //页面只需要一个provider情况
      create: (_) => Counter(),
      child: MyApp(),
    ),
  );
```
需要监听修改的Text
```
${context.watch<Counter>().count}
```
读取最新值
```
${context.read<Counter>().count}
 ```
点击触发count
```
context.read<Counter>().increment(),
```

provider入门实战
本人使用的 provider: ^4.3.2+3，最新为5.0.0，大家可以按需配置依赖

下边开始用provider实现计数器

首先创建model类
```
import 'package:flutter/cupertino.dart';
import 'package:flutter/foundation.dart';

//继承ChangeNotifier后，可以通知所有订阅者
class CounterModel with ChangeNotifier {
  int _count;//要保存的数据，我这里实现计数器，所以只有一个int变量
  CounterModel(this._count);

  void add() {//提供全局方法，让全局计数+1
    _count++;
    notifyListeners(); //当数值改变后，通知所有订阅者刷新ui
  }

  get count => _count; //提供全局get方法获取计数总值
}
```
修改官方的计数器代码
修改Flutter初始项目main.dart
```
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:provider_demo/provider/Counter.dart';
import 'package:provider_demo/widgets/menu.dart';

void main() {
  runApp(
    ChangeNotifierProvider(//全局状态设置
      create: (context) => CounterModel(0),//创建一个countermodel全局状态类，管理count值
      child: MyApp(),
    ),
  );
}

//不多做介绍
class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: MyHomePage(title: 'Provider'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);
  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
        actions: [
          IconButton(
            icon: Icon(Icons.golf_course),
            onPressed: () {//创建一个跳转界面，跳转到新的路由，本跳转不传任何值
              Navigator.push(context, MaterialPageRoute(builder: (context) {
                return MenuView();
              }));
            },
          ),
        ],
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Text(
              //以下代码Provider.of<model类名>(context).属性值
              //请注意，属性值在model类中必须有get方法
              "${Provider.of<CounterModel>(context).count}",
              style: Theme.of(context).textTheme.headline4,//字体样式
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(//创建一个悬浮按钮
        onPressed: _incrementCounter,
        tooltip: 'Increment',
        child: Icon(Icons.add),
      ),
    );
  }

  void _incrementCounter() {//悬浮按钮点击事件
    //context.read<model类名>().model中的方法;
    context.read<CounterModel>().add();
  }
}

```
一个简单的全局共享就完成了

>注：不建议在程序入口初始化Provider，这里只是为了演示方便这么做，实际项目中要是都在程序入口初始化可能会导致内存急剧增加，除非是共享一些全局的状态，例如app日夜间模式切换，中英文切换等

这时候我们发现，我们没有传值更没有返回值，就能轻松两个界面管理一个数据，是不是效率高了很多

但是我们发现，只能全局管理一个状态，那么怎么管理多个状态呢？

很简单，在main.dart

将
```
void main() {
  runApp(
    ChangeNotifierProvider(//全局状态设置
      create: (context) => CounterModel(0),//创建一个countermodel全局状态类，管理count值
      child: MyApp(),
    ),
  );
}
```
改为
```
void main() {
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (context) => CounterModel(0)),
	//可以继续添加，语法如上，这样可以全局管理多个状态
      ],
      child: MyApp(),
    ),
  );
}
```
总结
通过简单demo我们使用了provider演示计数器，那么在实际开发中，不会只管理这么简单的数据，如果管理数据过多，provider就给我们节省了大量工作量

一个model类可以有多个属性，一个app可以有多个model类
全局管理类，不见得用model结尾，但是我个人喜欢用model来存储数据
model类必须要继承ChangeNotifier类，否则无法刷新数据
model管理的状态，只有get方法，修改他的值是通过单独的方法进行修改的，在修改后要调用notifyListeners方法


- 触发者（Provider.of）：如果只是需要获取到数据model，不需要监听变化（例如点击按钮），推荐使用Provider.of(context, listen: false)来获取数据model。
- 监听者（推荐使用Consumer）：推荐使用Consumer。

- 简化了监听回调，实际是内部自动注册监听了；
- 注意局部使用 Provider；并不是所有数据都要放在 main 里面，放到使用到数据的顶层就行了；


我们在代码中是采用Provider.of来获取CounterProvider，这中获取方式确实会引起整个页面的重绘，至于原因不在本章讨论范围，以后有时间再说。 那么Provider到底能不能实现“局部刷新”呢? 当然是可以的，不然这个框架真的没啥用了。下面我们再来认识一位重量级嘉宾：

##### Consumer
这一节我们沿用计数器的代码，对其进行改造。之前我们提到了在程序入口初始化Provider是很不规范的，所以我们改成在页面级别初始化，并结合Consumer来使用。


# provider状态管理
使用Provider.of获取值的时候不要在initStates里面去取,需要在build函数或者 didChangeDependencies函数中去取.

不要在只会调用一次的组件生命周期中调用Provider,比如如下的使用方法是错误的
```
initState() {
  super.initState();
  print(Provider.of<Foo>(context).value);
}
```
要解决这个问题，要么使用其他生命周期方法（didChangeDependencies/build）
```
didChangeDependencies() {
  super.didChangeDependencies();
  final value = Provider.of<Foo>(context).value;
  if (value != this.value) {
    this.value = value;
    print(value);
  }
}
```
或者指明你不在意这个值的更新，比如

```
initState() {
  super.initState();
  print(Provider.of<Foo>(context, listen: false).value);
}
```

以上已经完成单个页面状态的管理，如果你想实现跨组件，跨路由状态共享。你只要把ChangeNotifierProvider放在整个应用的Widget树的根上即可。

[Flutter状态管理：Provider4 入门教程（一）](https://juejin.cn/post/6844904179014582286)
[【Flutter 技能篇】你不得不会的状态管理 Provider](https://juejin.cn/post/6919633080097439757)
[[- Flutter-技能篇 -] 使用Provider前你应了解Consumer](https://cloud.tencent.com/developer/article/1622727)
[Flutter Provider状态管理-Consumer](https://blog.csdn.net/u013894711/article/details/102782366)
[Flutter | 状态管理指南篇——Provider](https://www.jianshu.com/p/c89eca674670)