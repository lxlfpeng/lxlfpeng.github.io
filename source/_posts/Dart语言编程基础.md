---
title: Dart语言编程基础
---

# 一.Dart 简述
在Dart中，一切都是对象，每个对象都是一个类的实例，所有对象都继承自Object。 Dart是强类型的，也有自动推断类型的机制。

# 二.变量。
### 1.变量的声明。
Dart中定义变量有两种方式，一种是静态类型语言常用的方式，显式指定变量类型，另一种则是动态语言的常用方式，不指定类型，由vm自动推断。
> 变量的默认值:未初始化的变量的初始值为null。甚至具有数字类型的变量最初也是null，因为在Dart中没有基础的数据类型，所有的都是对象类型.数字——就像dart中的其他东西一样是对象。
### 2. 显式指定类型来定义变量
```
void main() {
  // 通过显式指定类型来定义变量
  String name = "张三";
  num age = 18;
  name = 1; //报错，显示指定的变量的类型是无法改变的
}
```
### 3. 隐式推导变量.
无需指定变量的数据类型，变量会根据值的类型进行推导.使用关键字var.
```
void main() {
//使用var定义变量，即使未显式指定类型，在初始化时一旦赋值后类型就被固定，因此使用var定义的变量如果在初始化时进行赋值了则不能改变数据类型
  var id = 100;
  var number;
  number = "2019";
  id = "10010"; // 代码错误，无法运行，number变量已确定为int类型
  number = 19;//代码可以运行因为初始化时进行了类型推到所以可以运行
}
```
### 4 动态数据类型.
如想动态改变变量的数据类型，应当使用dynamic或Object来定义变量。
```

dynamic var1 = "hello";//在这里初始化的是一个sting 类型的
var1 = 52;//在这里又改变成了 int 类型
print(var1);    // 最后的结果时Int类型


Object var2 = 20;// Object声明变量是int类型
var2 = "张三"; //修改为String类型
print(var2);    // 张三
```
##### dynamic:
所有dart 对象的基础类型，在大多数情况下，不直接使用它 通过它定义的变量会关闭类型检查，这意味着 dynamix x= 'hal'; x.foo();这段静态类型检查不会报错，
但是运行时会crash，因为x 并没有foo（） 方法，所以建议大家在编程时不要直接使用dynamic；
##### object:
是Dart 对象的基类，当你定义： object o =xxx ;时这个时候系统会认为o 是个对象，你可以调用o的toString()和hashCode()方法，因为Object 提供了这些方法，但是如果你尝试调用o.foo()时，
因为o 并没有foo（） 方法，静态类型检查会运行报错。

>综上不难看出dynamic 与object 的最大的区别是在静态类型检查上。dynamic在编译期不检测，object在编译器则会检测.

**建议在编写代码时，尽可能显式指定变量类型，这样可以提升代码可读性与调试的便利性。**

# 三.常量。
Dart中定义常量也有两种方式，一种使用final关键字，同Java中的用法， 一个 final 变量只能赋值一次；另一种是Dart的方式，使用const关键字定义。
### 1.Final 修饰符定义常量
```
void main() {
  // final 定义常量
  final  age = 18;
}
```
### 2.const修饰符定义常量
```
void main() {
  // const 定义常量
  const name = '张三';
}
```
### 3. final 和 const 的区别
 const声明时必须赋值，不然会报错，final 声明时可以不用先赋值。
```
void main() {
  final name;
  const age; //报错，声明时必须赋值
}

```

>final定义的常量是运行时常量，final声明变量只能赋值一次，并不要求赋的值一定是编译时常量，可以是常量也可以不是。 在程序运行的时候赋值，赋值后值不再改变。
>const常量则是编译时常量 要求在声明时初始化，并且赋值必需为编译时常量。


### 4.变量的命名规则：
- 变量名称必须由数字、字母、下划线和美元符($)组成。
- 注意：标识符开头不能是数字。
- 标识符不能是保留字和关键字。   
- 变量的名字是区分大小写的如: age和Age是不同的变量。在实际的运用中，也建议，不要用一个单词大小写区分两个变量。
- 标识符(变量名称)一定要见名思意 ：变量名称建议用名词，方法名称建议用动词。


# 四.常用数据类型。
|  类型   | 说明 | 备注|
|--|--|--|
Number	| 可以理解为是 数字数据类型|包括两类，int 整形，double 浮点形
String	| 字符串|可以使用三引号来创建包含多行的字符串
Boolean	| 布尔类型|取值只有 true false
List	        | 数组|List 类似java中的数组与集合var list =[1，2，4，5];
Map	        |键值数据类型|Map 类似java中的hashmap

### 1.数值类型
不像Java把类型分的特别细，比如整数类型，就有byte、short、int 、long 。Dart 内置支持两种数值类型，分别是int 和double ，它们的大小都是64位(具体取决于平台)。
数值类型转换:
```
void main() {
  var one = int.parse('1'); // String 转 int
  var onePointOne = double.parse('1.1'); // String 转 double
  String oneAsStr = 1.toString(); // int 转 String
  String piAsStr = 3.14159.toStringAsFixed(2); //double 转 String 保留两位 '3.14'
}

```
### 2.字符串类型
##### Dart可以使用单引号或双引号来创建字符串
```
  var str1 = "hello";
  var str2 = 'world';
```
##### Dart可以使用三引号来创建包含多行的字符串
```
  var multiLine1 = """xxxxxxx
xxxxxxx
""";

  var multiLine2 = '''yyyyyyy
yyyyy
''';

```
##### Dart支持使用"+"操作符拼接字符串
```
 var hw = "hello" + " world";
```
##### Dart提供了插值表达式"${}"，也可以用于拼接字符串
```
  var name = "张三";
  var str = "hello，${name}";
  print(str); // hello，张三
```
##### 与kotlin类似，Dart使用"=="来比较字符串的内容
```
  print("hello" == "world");
```

##### 其他字符串操作功能
```
void main() {
  var str = "hello word";
  //字符串判断
  print(str.length); // 字符串长度
  print(str.isEmpty); // 是否为空
  print(str.isNotEmpty); //是否不为空

  //字符串分割
  print(str.substring(0， 2)); // 字符串分割，含头不含尾
  print(str.substring(3)); // 字符串分割，从指定index至末尾
  String str2 = "a，d，d d，c，，";
  List<String> strs = str2.split("，"); //使用，分割，返回的是一个数组

  //字符串包含
  print(str.startsWith("xx")); //是否以‘xx’开头
  print(str.startsWith("xx"， 3)); //是否以‘xx’开头 从index=3开始判断
  print(str.endsWith("xx")); // 是否以‘xx’结尾
  print(str.contains("xx")); //是否包含‘xx’
}
```
### 4.布尔类型
Dart中的布尔类型用法同Java，仅有false、true两个值，不能使用0、非0或者null、非null来表达false和true。与Java不同的是，布尔类型的默认值为null。

### 5.列表

```
var list = [1， 2， 3];// 创建列表
print(list[0]);//获取下表为0的元素
print(list.length);// 下标从0开始。使用length可以访问list的长度
list.add(5);// 可以使用add添加元素

var constantList = const [1， 2， 3];// 可在list字面量前添加const关键字，定义一个不可改变的 列表（编译时常量）
constantList[1] = 1;     // 报错 无法进行修改
```
### 6.映射
又称为关联数组，相当于Java中的HashMap。
##### 通过字面量创建Map
```
var person = {
  'name' : '张三'，
  'age': '30'，
  'sex' : '男'
};
```
##### 使用Map类的构造函数创建对象
```
var person = new Map();
// 往Map中添加键值对
person['name'] = '张三';
person['age'] = '30';
person['sex'] = '男';
```
##### 获取Map的长度
```
print(person.length);
```
##### 查找Map
```
pirnt(person["name"]);
print(person["height"]);    // 键不存在则返回 null
```

# 四.流程控制。
### 1.if和else
```
if 和 else
if (表达式1) {
    分支1
} else if （表达式2） {
    分支2
} else{
    分支3
}
```
>dart的if else 必须是bool型
### 2.循环 for，while 和 do-while
```
for (初始语句;条件表达式;结束语句){
    循环体语句
}
例如:
for (var i = 0; i < 2; i++) {
  callbacks.add(() => print(i));
}

while (条件) {
   循环体语句
}

do{
   循环体语句
} while(条件) 
```
### 3.switch case
在 Dart 中 switch 语句使用 == 比较整数，字符串，或者编译时常量。 比较的对象必须都是同一个类的实例（并且不可以是子类）， 类必须没有对 == 重写。 枚举类型可以用于 switch 语句。
```
var command = 'OPEN';
switch (command) {
  case 'CLOSED':
    executeClosed();
    break;
  case 'PENDING':
    executePending();
    break;
  case 'APPROVED':
    executeApproved();
    break;
  case 'DENIED':
    executeDenied();
    break;
  case 'OPEN':
    executeOpen();
    break;
  default:
    executeUnknown();
}
```
### 4.break continue
break语句可以结束for等代码块。
```
void breakDemo() {
  break1:
  for (var i = 0; i < 5; i++) {
    // break2:
    for (var j = 0; j < 5; j++) {
      if (i == 2 && j == 2) {
        break break1;
      }
      print("loop:$j+$i");
    }
  }
  print("...");
}
```
continue语句可以结束当前循环，开始下一次的循环迭代过程。
```
void continueDemo() {
  forloop1:
  for (var i = 0; i < 5; i++) {
    // forloop2:
    for (var j = 0; j < 5; j++) {
      if (i == 2 && j == 2) {
        continue forloop1;
      }
      print("loop:$j+$i");
    }
  }
}
```

# 五.函数。
### 1.方法定义
```
返回类型  方法体  (参数1，  参数2， ...){
    方法体...
    return 返回值
}
```

如果一个函数没有显示声明返回值，Dart 会自动推导它的返回值类型。
```
// 声明返回值
int add(int a， int b) {
  return a + b;
}
// 不声明返回值
void add2(int a， int b) {
  return a + b;
}

```
如果一个函数没有显示的 return，那么它默认会返回 null。
```
fun(){}

print(fun() == null) //true    
```
如果一个函数只有一句表达式，可以使用简写：

```
bool isMan(String sex) => sex == '男';

isMan(String sex) => sex == '男';
```
### 2.命名参数
顾名思义 就是给参数定了个名字，和kotlin里面的具名函数一样.
通过 {} 符号，可以用于指定函数参数的名称。
```
void makeHotPot({required String water， required String seasoning， String meat = "羊肉卷"}) {
  print(water+seasoning+meat);
}
```
可以看到，Dart 支持我们给参数设置默认值。
调用：
```
void main() {
  makeHotPot(water: "矿泉水"， seasoning: "麻辣底料");
  makeHotPot(water: "矿泉水"， seasoning: "麻辣底料"，meat:"麻辣牛肉");
}

```
使用 required 修饰的参数，表示必要的参数，在调用的时候你不能遗漏它。

### 3.位置参数
使用中括号[]括起来的参数是函数的位置参数，代表该参数可传可不传，位置参数只能放在函数的参数列表的最后面。
```
// 位置参数可以有多个，比如[String a， int b]
test(String name， int age， [String hobby]) {
  StringBuffer sb = new StringBuffer();
  sb.write("hello， this is $name and I am $age years old");
  if (hobby != null) {
    sb.write("， my hobby is $hobby");
  }
  print(sb.toString());
}
```
### 4.匿名函数
多数函数是有名字的， 比如 main()和 print()。 也可以创建没有名字的函数，这种函数被称为 匿名函数， 有时候也被称为 lambda 或者 closure(闭包函数) 。 匿名函数可以赋值到一个变量中
匿名方法看起来与命名方法类似，在括号之间可以定义参数，参数之间用逗号分割。

后面大括号中的内容则为函数体：
```
([[类型] 参数[， …]]) {
  函数体;
};
```
注意：参数类型是可以选的，可以不带。
无参数的匿名函数:
```
// 传入一个函数对象，并执行该函数
void runFunc(Function func){
  func();
}

main(List<String> args) {
  runFunc((){print("匿名函数");});
}
```
带参数的匿名函数:
```
void runFunc(Function(String name) func){
  func("张三");
}

main() {
  runFunc((name){print(name);});
}
```
### 5.局部函数
在Dart中还有一种可以直接定义在函数体内部的函数，可以把称为局部函数或者内嵌函数。
函数声明可以出现顶层，比如常见的main函数等等。局部函数的好处就是从作用域角度来看，它可以访问外部函数变量，并且还能避免引入一个额外的外部函数，使得整个函数功能职责统一。
```
//定义外部函数getSoda
String getSoda(String water) {
  //定义内部函数makeSoda
  String makeSoda(String water) {
    return water + "糖" + "果汁" + "二氧化碳";
  }

  return makeSoda(water);
}
```
### 6.顶层函数和静态函数
在Dart中有一种特别的函数，在面向对象语言中比如Java，并不能直接定义一个函数的，而是需要定义一个类，然后在类中定义函数。
但是在Dart中可以不用在类中定义函数，而是直接基于dart文件顶层定义函数，这种函数我们一般称为顶层函数。最常见就是main函数了。
而静态函数就和Java中类似，依然使用static关键字来声明，然后必须是定义在类的内部的。
```
//顶层函数，不定义在类的内部
main() {
  print('hello dart');
}
```
### 4.函数作为参数
在 Dart 中，函数本身也是个对象，它对应的类型是Function，这意味着函数可以当做变量的值或者作为一个方法入传参数值。
```
void sayHello(var name){
  print('hello， $name');
}
//参数时一个函数
void callHello(Function func， var name){
  func(name);
}

void main(){
  // 函数变量
  var helloFuc = sayHello;
  // 调用函数
  helloFuc('张三');
  // 函数参数
  callHello(helloFuc，'李四');
}
```
# 六. 异常处理
异常是表示发生了意外的错误，如果没有捕获异常，引发异常的隔离程序将被挂起，并且程序将被终止；Dart可以抛出并捕获异常，但与java相反，Dart的所有异常都是未检查的异常，方法不声明它们可能抛出哪些异常，也不需要捕获任何异常。
```
try {
  breedMoreLlamas();
} on OutOfLlamasException {
  // 一个特定的异常
  buyMoreLlamas();
} on Exception catch (e) {
  // 其他异常
  print('Unknown exception: $e');
} catch (e) {
  // 没有指定类型， 则处理所有
  print('Something really unknown: $e');
}finally{
      print('finally');
 }
```
可以通过on 关键词来指定异常类型，finally一般用于释放资源等一些操作，它表示最后一定会执行的意思，即便try...catch中有return，它里面的代码也会承诺执行。
# 七.类
### 类的定义
Dart 是一门面向对象的编程语言，所有对象都是某个类的实例，所有类继承了Object类。
- 类的定义用class关键字。
- 如果未显式定义构造函数，会默认一个空的构造函数。
- 类首字母必须大写。
- 使用new关键字和构造函数来创建对象。
一个简单的类：
```
class Person {
  var name;
  var age;

  // 构造器
  Person(this.name， this.age);

  // 实例方法
  String getDescribe() {
    return "我叫$name我今年$age岁";
  }
}

main() {

  var person = new Person("张三"， "50");
  var name = person.name;
  var describe = person.getDescribe();
}
```
Dart 通过. 来调用类成员变量和方法的。和Kotlin一样还可以通过.?来避免null对象。

### 类的引入
在要使用的 dart 文件中引入 Person 类：
```
import 'lib/Person.dart';
```
### 构造函数
自定义类的默认构造函数:

```
class Person {
  String name;
  int age;
  // 默认构造函数
  Person(String name， int age) {
    print('这是构造函数里面的内容 这个方法在实例化的时候触发');
    this.name = name;
    this.age = age;
  }

  void getInfo() {
    print('${this.name}-----${this.age}');
  }
}

main() {
  var p1 = new Person('张三'， 30);
}

```

默认构造函数的简写
```
class Person {
  String name;
  int age;
  // 默认构造函数的简写
  Person(this.name， this.age);

  void getInfo() {
    print('${this.name}-----${this.age}');
  }
}

main() {
  var p1 = new Person('张三'， 30);
}
```
###  命名构造函数
自定义命名函数:
```
class Person {
  String name;
  int age;
  // 默认构造函数的简写
  Person(this.name， this.age);
  //命名构造函数
  Person.now() {
    print('我是命名构造函数');
  }
  // 可以定义多个命名函数
  Person.setInfo(String name， int age) {
    print('我是命名构造函数');
    this.name = name;
    this.age = age;
  }
}

main() {
  // var p1 = new Person('张三'， 30);// 默认实例化类是调用的是默认构造函数

   var p2 = new Person.now();//调用命名构造函数

  var p3 = new Person.setInfo('李四'， 30);//调用命名构造函数

}
```
### 初始化列表
- 初始化列表会在构造方法体执行之前执行。
- 使用逗号分隔初始化列表。
- 初始化列表常用于设置final属性的值。
```
void  main() {

    var map = {'name': 'jack'， 'age': 20， 'gender': '男'};
    var p = Person.withMap(map);
      
    
    print(p.name);
    print(p.age);
    print(p.gender);
}

class  Person {

    String name;
    int age;
    final  String gender;
  
    Person(this.name， this.age， this.gender);
  
    Person.withMap(Map map) : this.name = map['name'] ， this.gender = map['gender'] {       //this.gender = map['gender']  会在构造方法执行前进行赋值，此种方式主要用于final属性的赋值      
        this.age = map['age'];    
    }

}
```
### 类中的getter和setter修饰符
```
class Rect {
  num height;
  num width;

  Rect(this.height， this.width);

  // get 方法
  get area {
    return this.height * this.width;
  }

  // set 方法
  set areaHeight(value) {
    this.height = value;
  }
}

void main() {
  Rect r = new Rect(10， 4);
  //调用set方法
  r.areaHeight = 6;
  //直接通过访问属性的方式访问area
  print("面积:${r.area}");
}
```
### 类变量的可见性
在 Dart 中，没有private、protected、public这些关键词，如果要声明一个变量是私有的，则在变量名前添加下划线_，声明了私有的变量，只在本类库中可见。私有属性及私有方法， 只有放在单独的文件 class 中生效.默认类中的所有属性和方法是public的。
```
class Person {
  String _secret; // 私有属性 只有放在单独的文件 class 中生效
  // 私有方法
  void _run() {
    print('private function _run');
  }
  // 对外暴露私有方法
  void executeRun() {
    this._run();
  }
}
```
### 类中的静态成员 静态方法
使用static关键字来实现类级别的变量和函数。
```
class Person {
  static String name = '张三';
  static void show() {
    print(name);
  }
}

main() {
  print(Person.name);
  Person.show();
}
```
静态方法只能访问静态属性，不能访问非静态成员。非静态方法可以访问静态属性。
```
class Person {
  static String name = '张三';
  int age = 29;

  static void show() {
    print(name);
  }

  void printInfo() {
    //非静态方法可以访问静态成员
    print(name); //访问静态属性
    print(this.age); //访问非静态属性
    show(); //调用静态方法
  }

  static void printInfo2() {
    //静态方法不能访问非静态成员
    print(name); //访问静态属性
    show(); //调用静态方法
    // print(this.age); //报错 不能访问非静态属性
  }
}

main() {
  // Person p = new Person();
  // p.printInfo();

  Person.printInfo2();
}
```
##### 静态变量
- 静态变量(类变量)对于类范围的状态和常量非常有用。
- 静态变量在使用之前不会初始化。
##### 静态方法
静态方法(类方法)不能在实例操作，因此它没有访问this的权限。

>为了常用或广泛使用的实用程序和功能，考虑使用顶层函数，而不是静态方法。可以使用静态方法作为编译时常量。例如，可以将静态方法作为参数传递给常量构造函数。
# 八.抽象类和接口
### 抽象类
Dart 的抽象类和Java差不多，除了抽象类是不能被实例化的，可以声明抽象方法之外，和一般类没有区别。抽象类不能实例化，可以当做抽象类来 extends 也可以当做接口来 implements，dart 中没有 interface 这个关键字，接口也是抽象类实现的。
```
abstract class Animal {
  speak(); // 抽象方法  必须实现
  printInfo() {  // 不需要实现
    print('not abstract method');
  }
}

class Dog extends Animal {
  @override
  speak() {
    print('wang!');
  }
}

class Cat extends Animal {
  @override
  speak() {
    print('miao');
  }
  

}
```
### 隐式的接口
每个类都是都是隐式的接口，包括类的方法和属性。如果你想创建一个类A不继承B的实现，可以实现B的接口来创建类A。一个类允许通过implements 关键词可以实现多个接口。
```
// 每个类都是一个隐式的接口，所以Person类也是个接口，包括成员属性和方法.
class Person {
  // 可在接口中实现， 但仅对这个库可见.
  final _name;

  // 构造函数不能够被接口实现
  Person(this._name);

  // 可在接口中实现.
  String greet(String who) => 'Hello， $who. I am $_name.';
}

// 实现Person接口.
class Impostor implements Person {
  get _name => '';

  String greet(String who) => 'Hi $who. Do you know who I am?';
}

String greetBob(Person person) => person.greet('Bob');

void main() {
  print(greetBob(Person('Kathy')));
  print(greetBob(Impostor()));
}
```
实现多个接口
```
class Point implements Comparable， Location {...}
```
### Mixin混入
在通过implements实现某个类时，类中所有的方法都必须被重新实现 (无论这个类原来是否已经实现过该方法)。但是某些情况下，一个类可能希望直接复用之前类的原有实现方案，怎么做呢?
使用继承吗？但是Dart只支持单继承，那么意味着你只能复用一个类的实现。
Dart提供了另外一种方案: Mixin混入的方式:
除了可以通过class定义类之外，也可以通过mixin关键字来定义一个类。只是通过mixin定义的类用于被其他类混入使用，通过with关键字来进行混入。
```
main(List<String> args) {
  var superMan = SuperMain();
  superMan.run();
  superMan.fly();
}

mixin Runner {
  run() {
    print('在奔跑');
  }
}

mixin Flyer {
  fly() {
    print('在飞翔');
  }
}

// implements的方式要求必须对其中的方法进行重新实现
// class SuperMan implements Runner， Flyer {}

class SuperMain with Runner， Flyer {

} 
```
# 八.类的继承
### extends 关键字
子类继承父类使用 extends 关键字，dart 没有多继承.重写方法最好加上 @override 注解，便于协作.子类构造方法中，如果要初始化父类构造方法，使用 super 关键字，比如: 
```
Dog(String name， int age， [String nickName]) : super(name， age);
```
子类中调用父类的方法使用 ``super.fun()``
使用extends创建子类，super引用父类，子类可以重写实例方法、getter和setter，使用@override注释重写，使用@proxy注释来忽略警告。
```
class Television {
    void turnOn() {
        _illuminateDisplay();
        _activateIrSensor();
    }
}

class SmartTelevision extends Television {
    void turnOn();
    _bootNetworkInterface();
    _initializeMemory();
    _upgradeApps();
}
```
### 重写成员
可以使用 @override 关键字，子类可以重写实例的方法，getters和setters。
```
class SmartTelevision extends Television {
  @override
  void turnOn() {...}
  // ···
}
```
### 重写操作符
你可以重写以下表中显示的运算符。例如，如果定义Vecor类，则可以定义+方法来添加两个vectors。
```
class Vector {
  final int x， y;

  Vector(this.x， this.y);

  Vector operator +(Vector v) => Vector(x + v.x， y + v.y);
  Vector operator -(Vector v) => Vector(x - v.x， y - v.y);

  // Operator == and hashCode not shown. For details， see note below.
  // ···
}

void main() {
  final v = Vector(2， 3);
  final w = Vector(2， 2);

  assert(v + w == Vector(4， 5));
  assert(v - w == Vector(0， 1));
}
```
### noSuchMethod()
当用户调用你定义的类中不存在的属性与方法时，可以做出一些响应，通过重写noSuchMethod()。

```
class A {
  @override
  void noSuchMethod(Invocation invocation) {
    print('You tried to use a non-existent member: ' +
        '${invocation.memberName}');
  }
}
```
# 九. 枚举
枚举类型，通常称为枚举，是一种特殊类型的类，用于表示固定数量的常量值。

### 使用枚举
使用enum关键词来声明一个枚举类型。
```
enum Color { red， green， blue }
```
枚举中的每个值都有一个index索引，它返回枚举声明中值的从零开始的位置。例如，第一个值具有索引0，第二个值具有索引1。
```
print(Color.red.index == 0);//true
print(Color.green.index == 1);//true
print(Color.blue.index == 2);//true
```
若要获取枚举中所有值的列表，请使用枚举的values常量。
```
List<Color> colors = Color.values;
assert(colors[2] == Color.blue);
```
你可以在switch语句中使用枚举，如果不处理枚举的所有值，将会收到警告:

```
var aColor = Color.blue;

switch (aColor) {
  case Color.red:
    print('Red as roses!');
    break;
  case Color.green:
    print('Green as grass!');
    break;
  default: // 没有default，将会报错
    print(aColor); // 'Color.blue'
}
```
枚举类型有以下限制:
- 不能子类化、混合或实现枚举。
- 不能显式实例化枚举。

# 十. 泛型
泛型是程序设计语言的一种特性。允许程序员在强类型程序设计语言中编写代码时定义一些可变部分，那些部分在使用前必须作出指明。
从字面的意思理解来看，泛型，泛就是模糊、暂不确定暂定的意思。可以这样理解，使用泛型就是，定义的一个类型，类型暂不确定，给使用给一个占位符给代替，在使用的时候可以给确定其定义的类型。
### 泛型方法
泛型方法可以约束一个方法使用同类型的参数、返回同类型的值，可以约束里面的变量类型。
```
T getData<T> (T val) {
  return val;
}

getData<String>('123');
getData<int>(123);
getData<double>(123);
// getData<bool>(123); //  约束了类型是 bool 但是传入了 int，所以编译器会报错：
```

### 泛型类
声明泛型类，比如声明一个 Array 类，实际上就是 List 的别名，而 List 本身也支持泛型的实现。
```
class Array<T> {
  List _list = new List<T>();
  Array();
  void add<T>(T value) {
    this._list.add(value);
  }
  get value{
    return this._list;
  }
}
```
使用泛型类:
```
  List l1 = new List<String>();
  // l1.add(12); //报错，泛型是String却添加了int类型
  l1.add('asd');

```

### 泛型接口
下面声明了一个 Storage 接口，然后 Cache 实现了接口，能够约束存储的 value 的类型：
```
abstract class Storage<T>{
  Map m = new Map();
  void set(String key， T value);
  void get(String key);
}

class Cache<T> implements Storage<T> {
  @override
  Map m = new Map();

  @override
  void get(String key) {
    print(m[key]);
  }

  @override
  void set(String key， T value) {
    print('set successed!');
    m[key] = value;
  }
}
```
使用泛型接口实现的类：

```
  Cache ch = new Cache<String>();
  ch.set('name'， '123');
  // ch.set('name'， 1232); // 报错，类型不匹配
  ch.get('name');
```
# 十一.使用类库
有生命力的编程语言，它背后都有一个强大的类库，它们可以让我们站在巨人的肩膀上，又免于重新造轮子。

### 导入类库
在Dart里面，通过import关键词来导入类库。
内置的类库使用dart:开头引入：
```
import 'dart:io';
```

第三方类库或者本地的dart文件用package:开头：
比如导入用于网络请求的dio库：
```
import 'package:dio/dio.dart';
```
Dart 应用本身就是一个库，比如我的应用名是blog，导入其他文件夹的类：
```
import 'package:blog/common/net_utils.dart';
import 'package:blog/model/user.dart';
```
Dart 通过pub.dev来管理类库，类似Java世界的Maven 或者Node.js的npm一样，你可以在里面找到非常多实用的库。

###  解决类名冲突
如果导入的类库有类名冲突，可以通过as使用别名来避免这个问题：
```
import 'package:lib1/lib1.dart';
import 'package:lib2/lib2.dart' as lib2;

// 使用来自 lib1 的 Element
Element element1 = Element();

// 使用来自 lib2 的 Element
lib2.Element element2 = lib2.Element();
```
###  导入部分类
在一个dart文件中，可能会存在很多个类，如果你只想引用其中几个，你可以增加show或者hide来处理：
```
//文件：my_lib.dart中
class One {}

class Two{}

class Three{}
使用show导入One和Two类：

//文件：test.dart中
import 'my_lib.dart' show One， Two;

void main() {
  var one = One();
  var two = Two();
  //compile error
  var three = Three();
}
```
也可以使用hide排除Three，和上面是等价的：
```
//文件：test.dart中
import 'my_lib.dart' hide Three;

void main() {
  var one = One();
  var two = Two();
}
```
# 十二.异步
### 开发中的耗时操作：
在开发中，我们经常会遇到一些耗时的操作需要完成，比如网络请求、文件读取等等；如果我们的主线程一直在等待这些耗时的操作完成，那么就会进行阻塞，无法响应其它事件。
处理耗的操作有两种方式:
- 处理方式一： 多线程，比如Java、C++，我们普遍的做法是开启一个新的线程（Thread），在新的线程中完成这些异步的操作，再通过线程间通信的方式，将拿到的数据传递给主线程。
- 处理方式二： 单线程+事件循环，比如JavaScript、Dart都是基于单线程加事件循环来完成耗时操作的处理。
Dart是一个单线程编程语言。在Dart的世界里没有多线程之说，当然也没有了所谓的主线程和子线程之分。如果任何代码阻塞线程执行都会导致程序卡死。
### 阻塞式调用和非阻塞式调用
- 阻塞式调用： 调用结果返回之前，当前线程会被挂起，调用线程只有在得到调用结果之后才会继续执行。
- 非阻塞式调用： 调用执行之后，当前线程不会停止执行，只需要过一段时间来检查一下有没有结果返回即可。

### 单线程模型
在Java中使用多线程来处理并发任务，适量并合适地使用多线程，能够极大地提高资源的利用率和程序运行效率，但是缺点也比较明显，比如过度开启线程会带来额外的资源和性能消耗或多线程共享内存容易出现死锁等。
因此又出现了基于事件的异步模型。简单说就是在某个单线程中存在一个事件循环和一个事件队列，事件循环不断的从事件队列中取出事件来执行，这里的事件就好比是一段代码，每当遇到耗时的事件时，事件循环不会停下来等待结果，
它会跳过耗时事件，继续执行其后的事件。当不耗时的事件都完成了，再来查看耗时事件的结果。因此，耗时事件不会阻塞整个事件循环，这让它后面的事件也会有机会得到执行。

Dart是一种单线程语言，因此Dart程序没有主线程和子线程之分，Dart是通过消息循环(Event Looper)和事件队列(Event queue)来进行异步操作的.Dart在一条执行线上，同时且只能执行一个任务（事件），其他任务都必须在后面排队等待被执行。也就是说，在一条执行线上，为了不阻碍代码的执行
，每遇到的耗时任务都会被挂起放入任务队列，待执行结束后再按放入顺序依次执行队列上的任务，从而达到异步效果。

Dart事件循环机制是由一个 消息循环(Event looper) 和两个消息队列：事件队列(Event queue) 和 微任务队列(MicroTask queue) 构成。

![image.png](/images/3834a09a65d265a0c57fe6ed7c58c258.webp)
从上图可知，Dart事件循环机制由一个消息循环(event looper)和两个消息队列构成，其中，两个消息队列是指事件队列(event queue)和微任务队列(Microtask queue)。该机制运行原理为：

- 首先，Dart程序从main函数开始运行，待main函数执行完毕后，event looper开始工作。
- 然后，event looper优先遍历执行Microtask队列所有事件，直到Microtask队列为空。
- 接着，event looper才遍历执行Event队列中的所有事件，直到Event队列为空。
- 最后，视情况退出循环。

>注意: Dart中使用阻塞式调用也会造成程序卡死.

### Future
Dart 为 Event Queue 的任务建立提供了一层封装，叫作 Future。从名字上也很容易理解，它表示一个在未来时间才会完成的任务。Future 是一个延后计算的对象，即它的返回值当前并不一定可用，
在未来某个时刻它完成计算后便会返回可用的值。比如一个网络请求。通常使用 Future.then 来处理计算完成的场合，用 Future.catchError 来处理发生异常的场合。
Future是用于自定义Event queue事件。通过创建Future类实例来向Event queue添加事件：
```
new Future(() {
  // 事件任务
});
```

##### then
创建完成Future对象后，可以通过then方法接收Future的结果。
```
import "dart:io";
main(List<String> args) {
     print("main() start");
     //使用变量接收getNetworkData返回的future
     var future = getNetworkData();
     //通过then方法接收Future的结果。
     future.then((value) {
       print(value);
     });
     print("main() end");
   }
   
   Future<String> getNetworkData() {
     return Future<String>(() {
       sleep(Duration(seconds: 3));
       return "network data";
     });
   }
```
执行结果:
```
main() start
main() end
network data
```
Future的链式调用，可以在then中继续返回值，会在下一个链式的then调用回调函数中拿到返回的结果。
```
import "dart:io";
main(List<String> args) {
  print("main() start");
  getNetworkData().then((value1) {
    //得到第一次异步操作的回调，并且执行第二次异步操作
    print(value1);
    return "network data2";
  }).then((value2) {
    //得到第二次异步操作的回调，并且执行第三次异步操作
    print(value2);
    return "network data3";
  }).then((value3) {
    //得到第三次异步操作的回调，
    print(value3);
  });
  print("main() end");
}

Future<String> getNetworkData() {
  return Future<String>(() {
    sleep(Duration(seconds: 3));
    return "network data";
  });
}
```
执行结果:
```
main() start
main() end
network data
network data2
network data3
```


##### catchError
如果Future内的函数执行发生异常，可以通过Future.catchError来处理异常：
```
import "dart:io";

main(List<String> args) {
  print("main() start");
  var future = getNetworkData();
  future.then((value) {
    print(value);
  }).catchError((error) { // 捕获出现异常时的情况
    print(error);
  });
  print("main() end");
}
```
### async 和 await 关键字
async 和 await 关键字用于支持 Dart 语言的异步特性。async用来修饰方法，需要写在方法括号的后面， 它的调用者并不会等待它执行完毕。而 await 关键字必须存在于 async 方法内，被标为await的语句一般为耗时操作，
它后面的语句会等待 await 语句执行完毕。当耗时操作完成时，await后面的代码便会得到执行(异步)。这对关键字的存在意义就是以同步的编程风格，实现异步的执行。await表达式可以使用多次。
有了这两个关键字，我们可以更简洁的编写异步代码，而不需要调用Future相关的API。
将 async 关键字作为方法声明的后缀时，具有如下意义:
- 被修饰的方法会将一个 Future 对象作为返回值
- 该方法会同步执行其中的方法的代码直到第一个 await 关键字，然后它暂停该方法其他部分的执行；
- 一旦由 await 关键字引用的 Future 任务执行完成，await的下一行代码将立即执行。

```
// 导入io库，调用sleep函数
import 'dart:io';
void main(){
  print("main() start");
  getData();
  print("main() end");
}

// 定义一个函数用于包装
getData() async {
  var r = await getNetworkData();
  print(r);
}
// 模拟耗时操作，调用sleep函数睡眠2秒
getNetworkData() async{
  await sleep(const Duration(seconds:2));
  return "network data";
}

```
运行结果：
```
main() start
main() end
network data
```
>需要注意，async 不是并行执行，它是遵循Dart 事件循环规则来执行的，它仅仅是一个语法糖，简化Future API的使用。

### 轻量异步任务
 对于一些轻量异步任务，比如一个小的网络请求，本身的计算量不大，只是我们不知道它的确切完成时间。这种情况我们用 async 和 await 来简单创建一个异步任务即可。
这个异步任务并没有创建新线程，只是通过语言机制达到了异步执行而已。一个简单的例子：
```
Future<String>( () async { 
    await Future.delayed(Duration(seconds: 5)); //故意等待5秒(只模拟未知时间，并没有多大计算量)
    return "一个假设的计算结果";
}).then((value) {
    print("${DateTime.now()} 返回 :$value");
});

print("${DateTime.now()} 这里没有等待");
```
输出：
```
这里没有等待
返回 :一个假设的计算结果
```
从输出我们看到一个异步执行机制， 异步方法后面的语句立即得到执行，5秒后，再输出模拟计算的结果。这里的延时5秒实际并没有占用多少CPU资源，所以它属于轻量计算。
在实际测试中，轻量的异步计算并不会导致UI卡顿。到底多少计算量会导致UI卡顿？一般情况下，如果真实的CPU计算耗时超过10毫秒，就有卡顿风险了。那时就需要创建线程了。

### Isolate
大多数计算机中，甚至在移动平台上，都在使用多核CPU。 为了有效利用多核性能，开发者一般使用共享内存数据来保证多线程的正确执行。
然而多线程共享数据通常会导致很多潜在的问题，并导致代码运行出错。
Dart作为一种新语言，为了缓解上述问题，提出了Isolate(隔离区)的概念，即Dart没有线程的概念，只有Isolate，所有的Dart代码都是在Isolate中运行，
它就像是机器上的一个小空间，具有自己的私有内存堆和一个运行着Event Looper的单个线程。
它与线程最大的区别就是不能共享内存，因此也不存在锁竞争问题，两个Isolate完全是两条独立的执行线，且每个Isolate都有自己的事件循环，它们之间使用 Port 和 Message 来发送消息通信，所以它的资源开销低于线程。
Isolate 可执行于不同CPU核心来提高性能。
默认情况下，Dart程序只有一个Isolate(未自己创建的情况下)，而这个Isolate就是Main Isolate。也就是说，一个Dart程序是从Main Isolate的main函数开始的，而在main函数结束后
，Main isolate线程开始一个一个处理事件循环模型队列中的每一事件(Event)。

##### 使用场景
使用场景
在 Dart 中 async 和 Future 无法解决所有耗时的工作。Dart 虽然支持 异步执行，但其实如果是通过 async 的话，只是把工作丟到同一个 event loop 中， 让他暂时不会卡住目前的工作 ， 等到真的轮到它执行的时候 ，
如果它真的很耗时，那 main isolate 还是会 freeze(冻结) 住的 (为什么会冻结？ 主线程负责 UI的渲染 工作 但是 如果 密集型计算 很耗时 假如 这个计算 占用 1s的时间 你的UI就会卡住1s) 。
Dart 主要的 task 都是在 main isolate 中完成的，isolate 像是个 single thread 的 process。如果真的想要让某些工作能夠同时执行，不要卡住 main isolate 的话，就得要自己产生新的 isolate 來执行。

##### 创建Isolate
需要导入 isolate
```
import 'dart:isolate';
```

创建Isolate是比较简单的，可以使用 Isolate.spawn() 或 Flutter的 compute() 函数创建单独的隔离区来进行消耗性能的计算。
新创建的隔离区拥有自己的事件循环和内存，即使原始隔离区是该新隔离区的父级，也不允许其访问。
Isolate.spawn 必须传入一个有且仅有一个参数的函数，不可以不传。
```
import 'dart:isolate';

void main()  {
  Isolate.spawn(isolate， "true");
  Isolate.spawn(isolate， "false");
}

void isolate(String data) {
  print("isolate ${data}");
}

```
当我们调用 Isolate.spawn 的时候，它将会返回一个对 isolate 的引用的 Future。我们可以通过这个 isolate 来控制创建出的 Isolate，例如 pause、resume、kill 等等。

```
import 'dart:io';
import 'dart:isolate';
import 'lib/rf_timetool.dart';

main(List<String> args) {
  print('main start ${DateTime.now()}');

  //开辟另一个Isolate执行耗时操作
  Isolate.spawn(caculate， 100).then((value) {
    print('value = $value');
    print('${getDateStringNow()}');
  });

  print('main end ${DateTime.now()}');
}

caculate(int count) {
  sleep(Duration(seconds: 3));
  // print('${getDateStringNow()}');
  var total = 0;
  for (var i = 0; i <= count; i++) {
    total += i;
  }
  print(total);
  return total;
}
```

##### Isolate通信机制
但是在真实开发中，我们不会只是简单的开启一个新的Isolate，而不关心它的运行结果：

- 我们需要新的Isolate进行计算，并且将计算结果告知Main Isolate（也就是默认开启的Isolate）。
- Isolate 通过发送管道（SendPort）实现消息通信机制。
- 我们可以在启动并发Isolate时将Main Isolate的发送管道作为参数传递给它。
- 并发在执行完毕时，可以利用这个管道给Main Isolate发送消息。


```
import 'dart:io';
import 'dart:isolate';

main(List<String> args) async {
  print('main start ${DateTime.now()}');

  //1. 创建管道
  ReceivePort port = ReceivePort();

  //2.创建Isolata
  Isolate isolate = await Isolate.spawn(foo， port.sendPort);

  //3.监听管道
  port.listen((message) {
    print('$message ， ${DateTime.now()}');
    //关闭监听;
    port.close();
    // 销毁被监听的Isolate
    isolate.kill();
  });

  print('main end ${DateTime.now()}');
}

foo(SendPort senport) {
  sleep(Duration(seconds: 3));
  int total = 0;
  for (var i = 0; i < 100000000; i++) {
    total += i;
  }
  return senport.send('total = ${total}');
}

```
**双向通信:**
- 事实上双向通信的代码会比较麻烦。
- Flutter提供了支持并发计算的compute函数，它内部封装了Isolate的创建和双向通信。
- 利用它我们可以充分利用多核心CPU，并且使用起来也非常简单。

```
main(List<String> args) async {
  int result = await compute(powerNum， 5);
  print(result);
}

int powerNum(int num) {
  return num * num;
}

```
注意：上面的代码不是dart的API，而是Flutter的API，所以只有在Flutter项目中才能运行。
##### Future和isolate选择
Isolate 实际上是比较重的，每当我们创建出来一个新的 Isolate 至少需要 2mb 左右的空间甚至更多，取决于我们具体 isolate 的用途。那么应该在什么时候使用Future，什么时候使用Isolate呢？
其实这个问题，更值得去注意，因为这是和实际的开发直接相关，有时候确实需要知道什么时候应该是 Future ，什么时候应该使用 isolate . 
有的人说使用 isolate 比较重，一般不建议采用，其实不能这样一概而论。 isolate 也是有使用场景的，有些人会疑惑网络请求应该算耗时吧，平时一般使用 Future 就够了，

最简单的判断方法是根据某些任务的平均时间来选择：
- 方法执行在几毫秒或十几毫秒左右的，应使用Future。
- 如果一个任务需要几百毫秒或之上的，则建议创建单独的Isolate。

换句话说，建议尽可能多地使用 Future （直接或间接通过异步方法），因为一旦 EventLoop 有空闲期，这些 Future 的代码就会运行。

- 如果一段代码不会被中断，那么就直接使用Future就行。
- 如果代码段可以独立运行而不会影响应用程序的流畅性，建议使用 Future。
- 如果繁重的处理可能要花一些时间才能完成，而且会影响应用程序的流畅性，建议使用 isolate。

下面列出一些使用 isolate 的具体场景:

- JSON大数据解析: 解码大JSON数据。
- 加解密: 加解密过程比较耗时
- 图片处理: 比如裁剪图片比较耗时
- 从网络中加载大图

参考资料:
[Dart语法篇之函数的使用(四)](https://juejin.cn/post/6844903989843066894#heading-3)
[Flutter Dart 语言基础详解](https://juejin.im/post/5eb27d63f265da7bc35390b6#heading-27)
[【dart学习】-- Dart之异步编程](https://www.cnblogs.com/lxlx1798/p/11126564.html)
[Dart语法](https://juejin.cn/post/6844903950257225735#heading-43)

