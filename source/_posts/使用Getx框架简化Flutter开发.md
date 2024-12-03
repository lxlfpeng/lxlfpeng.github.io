---
title: 使用Getx框架简化Flutter开发
date: 2021-09-29
categories: 
  - Flutter开发
---

# 一. GetX的作用
GetX 是 Flutter 上的一个轻量且强大的解决方案,包含了以下的功能.
- 页面状态管理(跨页面交互)
- 路由管理
- 国际化、主题的适配
- 全局BuildContext 无Context弹窗
- 依赖注入
# 二. GetX安装
[GetX](https://pub.dev/packages/get)
### 1. 引入GetX依赖
在pubspec.yaml文件中添加Getx依赖:
```
get: ^4.x.x
```
### 2. GetX入口配置
各模块导包，均使用下面包即可
```
import 'package:get/get.dart';
```
只需要将MaterialApp改成GetMaterialApp便可以使用GetX提供的相关功能.
```
void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return GetMaterialApp(
      home: HomePage(),
    );
  }
}
```
GetMaterialApp还可以配置如下设置:
- initialRoute: '/', //根路由
- getPages: Pages.routes, // 配置路由
- defaultTransition:
- Utils.isIOS() ? Transition.native : Transition.rightToLeft, // 转场动画
- themeMode: ThemeMode.system, // 主题
# 三. GetX控制器GetxController
在介绍状态管理之前我们下来认识Get里面的一个重要的功能Controller.
### 1.GetxController的作用
在开发中如果把UI代码、业务逻辑都放在一起处理，这样对项目的架构、代码的可读性、后期的维护都会造成严重的影响，
因此我们需要将逻辑代码写在Controller里面,使得UI代码与业务逻辑分离开来.GetX为我们提供了GetxController,我们只需要继承GetxController
就可以实现我们自定义的控制器.
### 2.GetxController的简单使用
##### (1.)定义控制器继承自GetxController
```
class MyController extends GetxController {
    ...
}
```
##### (2. )Widget中注入实例化控制器并使用
```  
class HomePage extends StatelessWidget {
   
  MyController controller = Get.put<MyController>(MyController()); 

  @override
  Widget build(BuildContext context) {
    //MyController controller = Get.put<MyController>(MyController()); (由于StatelessWidget不会多次调用build方法因此可以在build方法里面注入Controller)
  }  
}

```
Get提供了一个简单而强大的依赖管理器，通过依赖注入就能检索到 Controller 并使用，不需要提供上下文，不像其他的状态管理方案需要在 inheritedWidget 的子节点进行。
Get.put可以使任何一个子路由使用依赖。所以，如果我们需要访问其他类中的同一个实例，我们可以使用Get.find。当有多个控制器时，使用Get.find也可以指定使用某个具体的控制器。
```
class HomePage extends StatelessWidget {
  MyController controller = Get.put<MyController>(MyController());
}
```
```
class SecondPage extends StatelessWidget {
  MyController controller = Get.find<MyController>(); 
}
```

**Get.put()方法详解**
```
  S put<S>(S dependency,
          {String? tag,
          bool permanent = false,
          InstanceBuilderCallback<S>? builder}) =>
      GetInstance().put<S>(dependency, tag: tag, permanent: permanent);
```
- dependency 是必传的参数,表示要注入的类.
- tag 在注入多个相同类型的类时,用tag进行区分,比如有两个商品实例，就需要使用tag区分不同的实例。
- permanent 代表是否不销毁。通常Get.put()的实例的生命周期和 put 所在的 Widget 生命周期绑定，如果在全局 （main 方法里）put，那么这个实例就一直存在。如果在一个
Widget 里 put ，那么这个那么这个 Widget 从内存中删除，这个实例也会被销毁。

**Get.lazyPut方法详解**
懒加载一个依赖，只有在使用时才会被实例化。适用于不确定是否会被使用的依赖或者计算高昂的依赖。类似 Kotlin 的 Lazy 代理。
```
Get.lazyPut<LazyController>(() => LazyController());
```
LazyController 在这时候并不会被创建，而是等到你使用LazyController的时候才会被 initialized，也就是执行下面代码的时候才 initialized：
```
Get.find<LazyController>();
``` 
在使用后，使用时的 Wdiget 的生命周期结束，也就是这个 Widgetdispose，这个实例就会被销毁。

>如果在一个 Widget 里 Get.find，然后退出这个 widget，此时这个实例也会被销毁，再进入另一个路由的 Widget，再次 find，GetX会打印错误信息，提醒没有 put
。即使全局注入，也一样。可以理解为，Get.lazyPut 注入的实例的生命周期是和在Get.find时的上下文所绑定。
### 3.GetxController的生命周期
GetxController也有生命周期的：
```
class SimpleController extends GetxController {
    @override
    void onInit() {
      // TODO: implement onInit
      print("初始化");
      super.onInit();
    }
    
    @override
    void onReady() {
      // TODO: implement onReady
      print("加载完成");
      super.onReady();
    }
    
    @override
    void onClose() {
      // TODO: implement onClose
      print("控制器被释放");
      super.onClose();
    }
}
```
- onInit：组件在内存分配后会被马上调用，可以在这个方法对 controller 做一些初始化工作。
- onReady：上一篇我们介绍过，这里是在 onInit 一帧后被调用，适合做一些导航进入的事件，例如对话框提示、SnackBar 或异步网络请求。
- onClose：在 onDelete 方法前调用、用于销毁 controller 使用的资源，例如关闭事件监听，关闭流对象，或者销毁可能造成内存泄露的对象，例如
  TextEditingController，AniamtionController。也适用于将数据进行离线持久化。
  
### 4.GetxController实现跨页面交互
例如在A界面处理数据，需要再B界面显示的时候，或者C界面，或者D界面。只要注入了控制器。在其他界面就能拿到A界面的数据。 A界面通过Get.put注入Controller;
此刻A界面跳到B Get.to(BPage)； B在跳到C Get.to(CPage)； C在跳到D Get.to(DPage)；D页面需要A界面的数据,可以通过 Get.find找到A界面里注入的Controller进行操作.

> Get.put可以使任何一个子路由使用该依赖。所以，如果需要访问其他类中的同一个实例，可以使用Get.find。

```
class HomePage extends StatelessWidget {
  Controller controller = Get.put(Controller());
}
class SecondPage extends StatelessWidget {
  Controller controller = Get.find(); 
}
```
### 5.GetxController资源释放
##### (1.)GetxController资源释放
在我们使用GetX的时候，并没有写代码来对GetxController进行释放，如果用了getx的那一套路由跳转api（Get.to、Get.toName...）之类.在组件被销毁的时候GetxController
也会被销毁.在页面中使用GetxController,并且在注入Controller之前在这里打印了一句：
```
class SimplePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    print('SimplePage-->build');
    Controller controller = Get.put(Controller());
    return Scaffold(
        ...    
    )

```
再次打开这个页面，控制台输出：

```
flutter: SimplePage-->build
flutter: SimpleController--onInit
[GETX] " SimpleController" has been initialized
flutter: SimpleController--onReady
SimplePage-build->SimpleController-onInit->SimpleController-onReady
```
关闭当前页面返回：
```
[GETX] CLOSE TO ROUTE /SimplePage
flutter: SimpleController--onClose
[GETX] "SimpleController" onClose() called
[GETX] "SimpleController" deleted from memory
[GETX] Instance "SimpleController" already removed.
```

可以看到SimpleController已经被删除。

通过上面我们知道跳转页面的时候，GetX会拿你到页面信息存储起来，加以管理，如果不使用GetX提供的路由跳转,在组件销毁时,
那么这个GetxController会无法释放.也就是说 GetX虽然各个功能均可单独引用使用，但是状态管理和路由是搭配的，如果没有使用 route_manager
组件，那么状态管理的生命周期就会失效。put的Controller在不使用的时候不会再被删除，而变成了应用状态常驻内存里。

##### (2.)GetxController资源未销毁解决
未使用GetX提供的路由跳转：直接使用原生路由api的跳转操作,这样会直接导致GetX无法感知对应页面GetxController的生命周期，会导致其无法释放.

```
Navigator.push(
    context,
    MaterialPageRoute(builder: (context) => XxxxPage()),
);
```

解决方案是使用StatefulWidget，在这种情况，无法感知生命周期，就需要使用StatefulWidget生命周期在dispose回调处，把当前GetxController从整个GetxController管理链中删除即可:
```

class SimplePage extends StatefulWidget {
  @override
  _SimplePageState createState() => _SimplePageState();
}

class _SimplePageState extends State<SimplePage> {
  final SimpleController _controller = Get.put(SimpleController());

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      ....
    );
  }

  @override
  void dispose() {
    Get.delete<SimpleController>();//将GetxController销毁
    super.dispose();
  }
}

class SimpleController extends GetxController {
 
}
```
# 四. GetX状态管理
### 1.GetBuilder实现状态管理
##### (1)GetBuilder的使用
1. 用计数器示例来演示一下GetBuilder的基本使用：
```
class CounterController extends GetxController {
  int _counter = 0;
  int get counter => _counter;

  void increment() {
    _counter++;
    update();
  }
}
```
这是一个控制器，有 UI 需要的数据counter和用户点击一次加1的方法。
2. 在UI 层一个展示的文本和一个按钮：
```
class HomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return GetBuilder<CounterController>(
        init: CounterController(),//如果在加载变量的时候使用Get.put()生成了CounterController对象，GetBuilder会自动查找该对象，就可以不使用init参数初始化Controller
        builder: (controller) {
          return Scaffold(
            appBar: AppBar(title: Text('计数器')),
            body: Center(
              child: Text(controller.counter.toString()),
            ),
            floatingActionButton: FloatingActionButton(
              onPressed: () {
                controller.increment();
              },
              child: Icon(Icons.add),
            ),
          );
        });
  }
}
```
使用了GetBuilder这个 Widget 包裹了页面，在 init初始化CounterController,然后每次点击，都会更新builder对应的 Widget，GetxController通过update()更新GetBuilder。
这看起来和别状态管理框架并无不同，有时只想重新 build 需要变化的部分，遵循最小原则，那么我们改下GetBuilder的位置，只包裹 Text:
3. 局部刷新:
```
class HomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    print('HomePage--build');
    return Scaffold(
      appBar: AppBar(title: Text('计数器')),
      body: Center(
        child: GetBuilder<CounterController>(
            init: CounterController(),
            builder: (controller) {
              return Text(controller.counter.toString());
            }),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
           Get.find<CounterController>().increment();
        },
        child: Icon(Icons.add),
      ),
    );
  }
}
```

GetX强大的一点的就表现出来了，按钮和文本并不在父子组件，并且和GetBuilder不在一个作用域，但是我们依然能正确得到Controller.

##### (2.)GetxBuilder局部更新UniqueID
在开发的过程中会碰到一种情况，就是多个地方引用了同一个属性，但我只想单独更新某一个地方，那么就可以用UniqueID来进行区分。

```
class BuilderController extends GetxController {
  int count = 0;

  addCount() {
    count++;
    update();
  }

  addJimCount() {
    count++;
    update(["jim"]);//只更新jim对应id的builder
  }

  addTomCount() {
    count++;
    update(["tom"]);//只更新tom对应id的builder
  }
}
```

注意update(['counter']里添加了 id 数组，这样就只更新这个 id 对应的GetBuilder:

```
class GetxBuilderTest extends StatelessWidget {
  const GetxBuilderTest({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    var controller = Get.put(BuilderController());
    return Scaffold(
      appBar: AppBar(
        title: Text("展示GetxBuilder的使用"),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            GetBuilder<BuilderController>(builder: (value) {
              return Text("count:" + value.count.toString());
            }),
            GetBuilder<BuilderController>(
                id: "jim",
                builder: (value) {
                  return Text("count:" + value.count.toString());
                }),
            GetBuilder<BuilderController>(
                id: "tom",
                builder: (value) {
                  return Text("count:" + value.count.toString());
                }),
            ElevatedButton(
                onPressed: () {
                  controller.addCount();
                },
                child: Text("增加计数器")),
            ElevatedButton(
                onPressed: () {
                  controller.addJimCount();
                },
                child: Text("增加Jim计数器")),
            ElevatedButton(
                onPressed: () {
                  controller.addTomCount();
                },
                child: Text("增加Tom计数器")),
          ],
        ),
      ),
    );
  }
}
```
### 2.响应式状态管理OBX
##### (1)OBX基本使用
1. 用计数器示例来演示一下OBX的基本使用：
```
class CounterController extends GetxController {
  // 使用 Rx 和 Darts 泛型，Rx < type >
    final count =0.obs;
      
    // 每次点击增加1
    void increment() {
      print("++")
      // 必须使用 .value 修饰具体的值
      this.count.value++;
    }
}
```
这是一个控制器，有 UI 需要的数据counter和用户点击一次加1的方法。
2. 在UI 层进行数据的增加和页面的更新：
```
class HomePage extends StatelessWidget {
  //注入化控制器
  CounterController controller =
      Get.put<CounterController>(CounterController());
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("OBX状态管理"),
        centerTitle: true,
      ),
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          //没有使用Obx(()=>包裹 每当改变计数时，就不会更新Text()。
          Text('${controller.count}次'),
          // 使用Obx(()=>包裹,每当改变计数时，就更新Text()。
          Obx(() => Text('${controller.count.value} 次')),
          MaterialButton(
              onPressed: () {
                // 直接调用函数
                controller.increment();
              },
              child: Text("点击增加"))
        ],
      ),
    );
  }
}
```

##### (1.)对象转Obx对象
Obx是一种响应式的状态管理,和GetBuilder不同,不需要需要手动调用 update() 更新状态的变化，在Obx包裹的对象属性发生变化时视图会自动更新渲染。
将一个对象编程Obx响应式对象有三种方式:
第一种是使用 Rx { Type }。
```
final name = RxString('');
final isLogged = RxBool(false);
final count = RxInt(0);
final balance = RxDouble(0.0);
final items = RxList<String>([]);
final myMap = RxMap<String, int>({});
```
第二种是使用 Rx 和 Darts 泛型，Rx < type >
```
final name = Rx<string>('');
final isLogged = Rx<bool>(false);
final count = Rx<int>(0);
final balance = Rx<double>(0.0);
final number = Rx<num>(0)
final items = Rx<List<string>>([]);
final myMap = Rx<Map<string, int>>({});
final user = Rx<User>();// 自定义类
```
第三种方法更实用、更简单也是首选，就是把.obs 作为你的变量的后缀:
```
final name = ''.obs;
final isLogged = false.obs;
final count = 0.obs;
final balance = 0.0.obs;
final number = 0.obs;
final items = <String>[].obs;
final myMap = <String, int>{}.obs;
final user = User().obs;// 自定义类
```

##### (2.)Obx变量为类时更新状态:
只有当响应式变量的值发生变化时，才会会执行刷新操作，当某个变量初始值为：1，再赋值为：1，并不会执行刷新操作.
将整个类对象设置为响应类型，当你改变了类其中一个变量，然后执行更新操作，只要包裹了该响应类变量的Obx()，都会实行刷新操作.
如果我们需要观察的数据是一个有许多属性的类.如何进行管理呢?
1. 我们将使整个类成为可观察的，而不是每个属性。
```
class User{
    User({this.name = '', this.age = 0});
    String name;
    int age;
}

// controller
final user = User().obs;
```
2. 有两种方式可以更新对象变量. 
方式一:
```
user.update( (user) { // 这个参数是你要更新的类本身。
    user.name = '张三';
    user.age = 18;
});
```
方式二:
```
user(User(name: '李四', age: 35));
```
3. 获取Obx的值的方式也有两种:
方式一:通过value这种方式获取
```
Obx(()=> Text("Name ${user.value.name}: Age: ${user.value.age}"));
```
方式二:
```
Obx(()=> Text("Name ${user().name}: Age: ${user().age}"));
```
当你定义了一个响应式变量，该响应式变量改变时，包裹该响应式变量的Obx()方法才会执行刷新操作，其它的未包裹该响应式变量的Obx()方法并不会执行刷新操作.

##### (3.)Obx使用Workers回调
响应式不只这些好处，还有一个 Workers ，将协助我们在事件发生时触发特定的回调，也就是 RxJava 的一些操作符；
```
class PersonController extends GetxController {
  var person = Person(20, "张三").obs;
  @override
  void onInit() {
    super.onInit();
    /// 每次更改都会回调
    ever<Person>(person, (person) => print("$person has been changed"));

    /// 第一次更改回调
    once<Person>(person, (person) => print("$person was changed once"));

    /// 更改后3秒回调
    debounce<Person>(person, (person) => print("debouce$person"), time: Duration(seconds: 3));

    ///3秒内更新回调一次
    interval<Person>(person, (person) => print("interval $person"), time: Duration(seconds: 3));
  }
}
```

我们可以利用 Workers ，实现比如防抖函数，在搜索的时候使用，节流函数，在点击事件的时候使用。
### 3.GetxBuilder和Obx总结
##### (1)区别
-Obx是响应式变量变化，Obx自动刷新；GetBuilder需要使用update手动调用刷新
- 响应式变量，因为使用的是StreamBuilder，会消耗一定资源
- GetBuilder内部实际上是对StatefulWidget的封装，所以占用资源极小

##### (2.)使用场景:
- 一般来说，对于大多数场景都是可以使用响应式变量的
- 但是，在一个包含了大量对象的List，都使用响应式变量，将生成大量的GetStream，必将对内存造成较大的压力，该情况下，就要考虑使用简单状态管理了

总的来说：推荐GetBuilder和update配合的写法

- GetBuilder内置回收GetxController的功能，能避免一些无法自动回收GetxController的坑爹问题
- 使用GetBuilder的自动回收：GetBuilder需要设置assignId: true；或使用插件一键Wrap Widget：GetBuilder（Auto Dispose）
- 使用Obx，相关变量定义初始化以及实体更新和常规写法不同，会对初次接触该框架的人，造成很大的困扰
- getx插件现已支持一键Wrap Widget生成GetBuilder，可以一定程度上提升你的开发效率

响应式编程虽好，但是对 RAM 的消耗比较大，因为他们的实现都是流，如果创建一个有80个对象的 List ，每个对象都有几个流，打开dart inspect，查看一个 StreamBuilder
的消耗量，我们就会明白这不是一个好的方法。而 GetBuilder 在 RAM 中是非常高效的，几乎没有比他更高效的方法。所以这些使用方式在使用过程中要斟酌。
# 五.GetX依赖注入
### 1.Binding的使用
上文中我们知道在页面中使用Controller需要先进行Get.put操作.但是每一个界面都这样操作,这种手动注入的方式麻烦不说还很难进行统一管理.为了更好的是组件中使用Controller我们可以用到Getx提供的Binding功能可以实现自动注入功能.
Binding 类是一个将依赖注入进行分离，Binding模块在路由跳转时,统一对界面通过懒注入的方式将binding模块的GetXController注入到界面中，简单说，就是把UI 中的 控制器实例化部分抽离出来了，抽离时需要实现 Bindings 类
可以统一管理复杂模块的多个GetXController,可以将路由、状态管理器和依赖管理器完全集成
当一个路由从栈中移除时，所有与它相关的控制器、变量和对象的实例都会从内存中移除。如果使用的是流或定时器，它们会自动关闭，不必单独进行内存管理处理。Bindings 类是一个解耦依赖注入的类，同时 "
Binding " 路由到状态管理器和依赖管理器。 这使得 GetX 可以知道当使用某个控制器时，哪个页面正在显示，并知道在哪里以及如何销毁它。
### 2.如何使用Bindings
##### (1)第一步： 创建一个控制器
```
class CounterController extends GetxController {
  int _counter = 0;
  int get counter => _counter;
  void increment() {
    _counter++;
    update();
  }
}
```
##### (2)第二步： 创建一个类并实现 Binding，如果有多个控制器，就在这实例化多个
// 创建bindings
```
class TestBingding implements Bindings {
  @override
  void dependencies() {
    Get.lazyPut<CounterController>(() => CounterController());
    // 。。。 还可以添加其它控制器
  }
}
```
##### (3)第三步： 绑定到路由中
我们要使用该 Binding 来建立路由管理器、依赖关系和状态之间的连接。 这里有两种方式，如果使用的是命名路由表：

```
 GetMaterialApp(
       ...
       getPages: [
         GetPage(
             name: "/binding",
             page: () => GetXBingdingPage(),
             binding: TestBingding()),
       ],
     )
```
如果是直接跳转：
```
Get.to(GetXBingdingPage(), binding: TestBingding());
```
##### (4)第四步：Widget 中使用
使用 Get.find() ,可以处理一个UI中有多个控制器的情况，如果你只有一个控制器，可以选择使用GeView.
```
class GetXBingdingPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    var controller = Get.find<BindingController>();
    return Scaffold(
      appBar: AppBar(
        title: Text("Bingding使用"),
      ),
      body: Column(
        children: [
          GetBuilder<CounterController>(builder: (value) {
            return Text("count:" + value.count.toString());
          }),
          ElevatedButton(
              onPressed: () {
                controller.addCount();
              },
              child: Text("点击增加数字"))
        ],
      ),
    );
  }
}
```
>请注意使用binding自动注入时,建议使用使用getx的命名路由方式,不建议在Get.to()方法里面进行binding绑定因为如果存在多个页面跳转到存在binding页面，每个Get.to()方法都需要绑定 这样极其容易出bug.
### 3.GetView
上面使用注入依赖解耦了，但是获取还是略显不方便，GetX 也为我们考虑到了。使用GetView代替StatelessWidget,可以直接使用 controller.变量调用,
前提条件就是只能用于有一个controller控制器
```
class SimplePage extends GetView<CounterController> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Obx(() => Text(controller.counter.value)),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          controller.increment();
        },
        child: Icon(Icons.add),
      ),
    );
  }
}
```

首先，你需要将你的class 继承自 GetxView<T>(T 为你的Controller)

GetxView<HomeController> 会自动帮你把 Controller 注入到 view 中，你可以简单理解为它自动帮你执行了以下步骤

```
final controller = Get.find<HomeController>();
```

不必担心 GetxView<T> 的性能，因为它仅仅是继承自 Stateless Widget ，记住，有了 getx 你完全不需要 Stateful Widget

GetView是一个Stateless Widget，仅是为了方便使用controller。如果我们只有一个controller作为依赖，可以使用GetView取代StatelessWidget并且不用再写Get.find。
这里完全没有Get.find，但是可以直接使用controller，因为GetView里封装好了：
```
abstract class GetView<T> extends StatelessWidget {
  const GetView({Key key}) : super(key: key);

  final String tag = null;

  T get controller => GetInstance().find<T>(tag: tag);

  @override
  Widget build(BuildContext context);
}
```

不在需要 StatelessWidget 和 StatefulWidget。这也是开发最常用的模式，推荐大家使用。

当然，也许有时候觉得每次声明一个 Bingings 类也很麻烦，那么可以使用 BindingsBuilder ，这样就可以简单地使用一个函数来实例化任何想要注入的东西。
```
 GetMaterialApp(
       ...
        GetPage(
        name: '/details',
        page: () => DetailsView(),
        binding: BindingsBuilder(() => {
          Get.lazyPut<DetailsController>(() => DetailsController());
        }),
     )
```

就是这么简单，Bingings 都不需要创建。两种方式都可以，大家根据自己的编码习惯选择最适合的风格。

Bindings的工作原理 Bindings 会创建过渡性工厂，在点击进入另一个页面的那一刻，这些工厂就会被创建，一旦路由过渡动画发生，就会被销毁。
工厂占用的内存很少，它们并不持有实例，而是一个具有我们想要的那个类的 "形状"的函数。 这在内存上的成本很低，但由于这个库的目的是用最少的资源获得最大的性能，所以Get连工厂都默认删除。

> Bindings是我们可以在其中声明依赖项，然后将它们“绑定”到路由的类。但是，这意味着我们只能在使用GetX进行路由管理时使用它。
# 六.GetX路由管理
### 1.简单路由

#### (1.)导航到新页面

```
Get.to(()=>LoginPage());
```

#### (2.)进入新页面 配置路由名称 建议这种统一配置

```
Get.toNamed(Routes.XXXX);
```

#### (3.)pop 返回、关闭snackbars, dialogs, bottomsheets

```
Get.back();
```

#### (4.)push到下一页，但禁止从下一页返回过来

```
Get.off(LoginPage());
```

可以用在启动屏、登录页中。

#### (5.)push到下一页，并且从栈内移除以前的所有路由

```
Get.offAll(LoginPage());
```

可以发现，上面的push和pop方式，不需要传递context,省下了很多麻烦，这个GetX在路由管理的最大优势，这样增加了路由管理的书写范围，扩大了你代码灵活性，不用担心context在哪，而特意使用builder。
### 2.路由传值
在不同页面中传递参数 get中有三种方式
##### (1.)argment 传递
argments 参数是 dynamic 类型的 ， 与Navigator中的arguments相同,但是在getx中获取却非常方便
传递参数:
```
// a页面 附带argements参数
Get.toNamed("/b",arguments: true);  
// 等同于 Navigator.pushNamed(Get.context, "/b", arguments: true);
```
获取参数:
```
//b页面  获取argments参数  (在 build 中)
var data = Get.arguments;
//等同于  var data = ModalRoute.of(context).settings.arguments;
```
##### (2.)parameters 传递
parameters接受 Map<String, String>作为参数传递, 方式类似与网页传值
传递参数:
```
//a页面  
Get.toNamed("/b", parameters: {"name":"张三"});
//或者  使用 拼接形式
Get.toNamed("/b?name=张三");
```
获取参数:
```
//b页面
var data = Get.parameters;
data['name']   
```
##### (3.)parameters 还有一种 传值方式传值通过 绑定路由地址

// 修改路由表  新增 /serach/:id
```
GetPage(
        name: Routes.HOME,  // "/home"
        page: () => TabBarPage(),
        children: [
          GetPage(
            name: Routes.SEARCH,  // "/search"
            page: () => SearchPage(),
          ),
          GetPage(   //  ********* 新增 *******  
            name: Routes.SEARCH+"/:id",
            page: () => SearchPage(),
          ),
        ]
    ),
```
/search/:id 是home的子路由 那么访问 他的完整链接应该是 “/home/search/:id”
```
// 跳转 传递参数
Get.toNamed("/home/search/123");

// 在 search 页面中接收
var data = Get.parameters;
//data =  {"id":"123"}
```
上面的方式学过前端框架的应该很熟悉

```
onPressed: () async {
var data = await Get.to(MinePage());
// 上个页面返回后，立即拿到数据,456
print(data);
}
```
```
MaterialButton(
onPressed: () {
// 返回携带参数
Get.back(result: 456);
},
color: Colors.blue,
textColor: Colors.white,
child: Text("返回上个页面"),
),
```
### 3.命名路由导航

要使用别名路由导航，需要定义路由，在main函数内使用GetMaterialApp，并设置相关属性。

```
void main() {
  // 别名路由配置
  runApp(
    GetMaterialApp(
      initialRoute: '/',
      getPages: [
        GetPage(name: '/', page: () => OnePage()),
        GetPage(
            name: '/two', page: () => TwoPage(), transition: Transition.zoom),//添加跳转动画
      ],
    ),
  );
}
```

#### GetMaterialApp下还有一个属性unknownRoute，可以设置未定义路由的导航，如错误页面。

```
unknownRoute: GetPage(name: '/notfound', page: () => UnknownRoutePage()),
```

#### push到下一页

```
Get.toNamed("/two");
```

#### push下一页并移除前一个页面。

```
Get.offNamed("/two");
```

#### push下一页并移除所有之前的页面

```
Get.offAllNamed("/two");
```

#### push时携带数据 主要在后面加上你要传递的数据即可

```
Get.toNamed("/two", arguments: 'www.qson.tech');
```

在你别名为two的页面通过Get.arguments即可获取数据。
### 4.路由中间件(路由拦截)

在跳转前做些事情，比如判断是否登录，可以使用routingCallback来实现：

```
GetMaterialApp(
  routingCallback: (routing) {
    if(routing.current == '/second'){
     // 如果登录。。。
    }
  }
)
```
# 七.GetX服务GetxService
### 1. GetxService的作用
GetxService就像是全局状态的 “GetxController”，它共享程序的相同的生命周期（“onInit()”、“onReady()”、“onClose()”）。
GetxService不会从内存中删除。所以可以在程序任何地方都可以通过Get.find()获取。GetXService 类似服务,所以如果你需要在你的应用程序的生命周期内对一个类实例进行绝对的持久化。
比如ApiService，StorageService，CacheService，还有需要异步初始化的类，放在这里注入非常合适.
实际删除一个GetxService的唯一方法是使用Get.reset()，它就像"热重启 "你的应用程序。
### 2. GetxService的简单使用
通过GetxService获取usertoken的例子:
第一步：创建Service
```
class SpService extends GetxService {
  Future<String> getUserToken() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    String token = prefs.getString("token");
    print("token 的值为: $token");
    return token;
  }
}
```
第二步：初始化Service
```
/// 初始化服务
Future<void> main() async {
  await initServices();
  runApp(MyApp());
}

Future<void> initServices() async {
  print("初始化服务");
  await Get.putAsync(() async => await SpService());
  print("所有服务启动");
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return GetMaterialApp(
      title: "GetX",
      home: GetXServiceExample(),
    );
  }
}
```
第三步：调用Service
```
class GetXServiceExample extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: ElevatedButton(
            onPressed: () async {
              String userToken =
                  await Get.find<SpService>().getUserToken(); //可以获取到全局的服务
              print("token:$userToken");
            },
            child: Text("获取token")),
      ),
    );
  }
}
```
# 八.GetX其他功能
Getx还提供了许许多多的Api供我们开发时使用.
其他高级API:
```
// 给出当前页面的args。
Get.arguments

//给出以前的路由名称
Get.previousRoute

// 给出要访问的原始路由，例如，rawRoute.isFirst()
Get.rawRoute

// 允许从GetObserver访问Rounting API。
Get.routing

// 检查 snackbar 是否打开
Get.isSnackbarOpen

// 检查 dialog 是否打开
Get.isDialogOpen

// 检查 bottomsheet 是否打开
Get.isBottomSheetOpen

// 删除一个路由。
Get.removeRoute()

//反复返回，直到表达式返回真。
Get.until()

// 转到下一条路由，并删除所有之前的路由，直到表达式返回true。
Get.offUntil()

// 转到下一个命名的路由，并删除所有之前的路由，直到表达式返回true。
Get.offNamedUntil()

//检查应用程序在哪个平台上运行。
GetPlatform.isAndroid
GetPlatform.isIOS
GetPlatform.isMacOS
GetPlatform.isWindows
GetPlatform.isLinux
GetPlatform.isFuchsia

//检查设备类型
GetPlatform.isMobile
GetPlatform.isDesktop
//所有平台都是独立支持web的!
//你可以知道你是否在浏览器内运行。
//在Windows、iOS、OSX、Android等系统上。
GetPlatform.isWeb

// 相当于.MediaQuery.of(context).size.height,
//但不可改变。
Get.height
Get.width

// 提供当前上下文。
Get.context

// 在你的代码中的任何地方，在前台提供 snackbar/dialog/bottomsheet 的上下文。
Get.contextOverlay

// 注意：以下方法是对上下文的扩展。
// 因为在你的UI的任何地方都可以访问上下文，你可以在UI代码的任何地方使用它。

// 如果你需要一个可改变的高度/宽度（如桌面或浏览器窗口可以缩放），你将需要使用上下文。
context.width
context.height

// 让您可以定义一半的页面、三分之一的页面等。
// 对响应式应用很有用。
// 参数： dividedBy (double) 可选 - 默认值：1
// 参数： reducedBy (double) 可选 - 默认值：0。
context.heightTransformer()
context.widthTransformer()

/// 类似于 MediaQuery.of(context).size。
context.mediaQuerySize()

/// 类似于 MediaQuery.of(context).padding。
context.mediaQueryPadding()

/// 类似于 MediaQuery.of(context).viewPadding。
context.mediaQueryViewPadding()

/// 类似于 MediaQuery.of(context).viewInsets。
context.mediaQueryViewInsets()

/// 类似于 MediaQuery.of(context).orientation;
context.orientation()

///检查设备是否处于横向模式
context.isLandscape()

///检查设备是否处于纵向模式。
context.isPortrait()

///类似于MediaQuery.of(context).devicePixelRatio。
context.devicePixelRatio()

///类似于MediaQuery.of(context).textScaleFactor。
context.textScaleFactor()

///查询设备最短边。
context.mediaQueryShortestSide()

///如果宽度大于800，则为真。
context.showNavbar()

///如果最短边小于600p，则为真。
context.isPhone()

///如果最短边大于600p，则为真。
context.isSmallTablet()

///如果最短边大于720p，则为真。
context.isLargeTablet()

///如果当前设备是平板电脑，则为真
context.isTablet()

///根据页面大小返回一个值<T>。
///可以给值为：
///watch：如果最短边小于300
///mobile：如果最短边小于600
///tablet：如果最短边（shortestSide）小于1200
///desktop：如果宽度大于1200
context.responsiveValue<T>()
```
# 九.GetX模板代码生成
在开发中使用getx,有许多的模板代码例如创建controller,创建bindings,创建page.这样的代码技术含量不高,且都是一样的.如果手动编写费时费力,因此我们可以借助一些工具
来生成这些模板代码.
### 1. GetX Cli工具
[GetX Cli](https://github.com/jonataslaw/get_cli)是一个命令行脚本（command-line interface)安装好Cli可以通过命令行代码生成一些模板代码.
CLI有如下的功能:
- 创建Getx项目
- 项目工程化
- 生成Model
- 生成page
- 生成view
- 生成controller
- 自定义controller模板
- 生成翻译文件
### 2.开发工具插件
可以通过AndroidStudio或者是Vscode找寻模板插件,提升开发效率。例如getx_template.

相关资料:
[Flutter GetX使用---简洁的魅力！](https://juejin.cn/post/6924104248275763208)
[【源码篇】Flutter GetX深度剖析 | 我们终将走出自己的路（万字图文）](https://juejin.cn/post/6984593635681517582#heading-34)
[Flutter状态管理终极方案GetX第一篇——路由](https://juejin.cn/post/6905367558008078350)
[Flutter状态管理终极方案GetX第二篇——状态管理](https://juejin.cn/post/6907622450151096334#heading-10)
[GetX第三篇-依赖注入](https://juejin.cn/post/6910920929199521800#heading-10)
[GetX项目级实战](https://juejin.cn/post/6913917533997891591)
[getx的controller是怎么销毁的](https://www.jianshu.com/p/a643a1f6074e)
[Getx - 如何使用依赖管理和Bindings](https://blog.csdn.net/qq_36407748/article/details/115213064)
[getx 学习 使用 记录 - 路由](https://blog.csdn.net/qq_33950912/article/details/117793429)
[Getx - 如何使用路由管理页面](https://blog.csdn.net/qq_36407748/article/details/115204260)
[flutter 一文带你了解GetX](https://blog.csdn.net/iOS_And_Swift/article/details/111587941)
[Flutter GetX系列教程---国际化配置、依赖注入、Binding](https://www.jianshu.com/p/71dd44bf61bb)
[flutter + getx 最佳实践](https://juejin.cn/post/6997283367045562375#heading-0)
[Flutter 入门与实战（七十四）：GetxController 的生命周期详解](https://juejin.cn/post/7005342494552489991)
[Flutter GetX系列教程---GetxController](https://juejin.cn/post/7005010372637753352#heading-2)
[Flutter状态管理--GetX的简单使用](https://juejin.cn/post/6978079109804982285)
