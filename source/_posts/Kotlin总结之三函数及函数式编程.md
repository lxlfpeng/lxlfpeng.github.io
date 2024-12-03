---
title: Kotlin总结之三函数及函数式编程
---

# 一.Kotlin中的函数
函数是执行特定任务的一段代码，程序通过将一段代码定义成函数，并为该函数指定一个函数名，就可以在需要的时候多次调用这段代码，代码复用的重要手段就是通过函数实现的。
### 1.函数声明
定义格式为：
```
权限修饰符 fun 函数名(参数名 ：类型,...) : 返回值{
  //函数执行体
}
```
函数从参数角度，可以分为``有参函数以及无参函数``；从返回值角度，可以分为有``返回值的函数以及没有返回值的函数``。那么函数一共就有4种类型，``无参无返回值、无参有返回值、有参无返回值、有参有返回值``。
```
//无参无返回值
fun test() {
    println("test")
}
 
//无参有返回值
fun test(): String {
    return"test"
}
 
//有参无返回值
fun test(content: String) {
   println(content)
}
 
//有参有返回值
fun test(content: String): String {
    retur ncontent
}
当然，没有返回值的函数，也可以明确指定返回值类型为Unit。
//无参无返回值
fun test():Unit{
    println("outerFun")
}
 
//有参无返回值
fun test(content: String) :Unit {
    println(content)
}
```
- 上面的例子中没有可见性修饰符，那是因为Kotlin中``默认为public可见性修饰符``。
- ()圆括号必须存在，即使是没有参数的情况下。
- {}大括号必须存在，即使是没有函数体的时候，不过在Kotlin中有一个特例就是，函数具备返回值的时候，如果只用一个表达式就可以完成这个函数，则可以使用单表达式函数（可以不加{}）。
- 在函数没有返回值时可以省略Unit。

### 2.单表达式函数
函数只是返回单个表达式，可以省略花括号并在等号后指定函数体即可。这种方式被称为单表达式函数。
```
fun main(args: Array<String>) {
    println(area(2.0, 3.0))
}
fun setValue(x: Int, y: Int) = x + y
```

### 3.顶层函数
不同于Java中函数只能定义在每个类里面，kotlin可以在文件任意位置处定义函数，这种函数称为``顶层函数``。
>  Java作为一门面对对象的语言，Java中，所有的代码都是依托于类而存在，函数作为类的方法，属性作为类的属性。但实际上项目中总有一些函数不属于任何一个类，最终产生了一些类不包含任何状态或者实例函数，仅仅是作为一堆静态函数的容器。在JDK中，最明显的例子应该就是Collections了，还有你的项目中是不是有很多以Util作为后缀的类？
在Kotlin中，根本不需要去创建这些无意义的类，你可以把这些函数直接放到代码文件的顶层，不用从属于任何类。因此可以再任何类中调用。

```
// 文件名 join.kt
package strings //包名
fun joinToString() : String {...}

// kotlin调用
import strings.JoinKt;//导入该顶层函数
fun main(args: Array<String>){
    joinToString()
}

// Java调用
import strings.JoinKt;
public class Main {
    public static void main(String[] args) {
        JoinKt.joinToSting()
    }
}
```
编译完成后顶层函数会成为文件类下的``静态函数``，比如在文件名是join.kt下定义的joinToString函数可以通过JoinKt.joinToSting调用，其中JoinKt是编译后的类名。

- 在Kotlin中，顶层函数属于包内成员，包内可以直接使用，包外只需要import该顶层函数，即可使用。
- 在Java中，类还是必须要存在的，所以编译器将JoinKt.kt文件里的代码放在了一个JoinKt的类中，然后把定义的Kotlin的函数作为静态方法放在其中，所以在Java中是先通过mport导入这个类，然后通过``类名.方法名``来调用。

如果觉得Kotlin自动生成的这个类名不好，那你可以通过@file:JvmName注解来自定义类名:
```
@file:JvmName("StrUtil")//自定义生成顶层函数的类名
package strings

fun joinToString() : String {...}
```

### 4.顶层属性
和函数一样，属性也可以放到文件的顶层，不依附于类。从Java的角度来看就是静态属性，而且由于没有了类的存在，这种属性用到的``机会也不多``。
```
//kotlin文件名为ApiConfigKt
package config

var count = 0
val REQUEST_URL = "http://localhost:8080/"
const val BASE_URL = "http://www.xxx.com/"
```
在kotlin中使用:
```
import config.count

fun main(args: Array<String>){
    //使用var变量
    count++
    //使用val常量
    config.REQUEST_URL
    //使用const val常量
    config.BASE_URL
}

```
在Java中使用:
```
import config.ApiConfigKt;
public class Main {
    public static void main(String[] args) {
        //使用var变量
        ApiConfigKt.setCount(12);
        System.out.println(ApiConfigKt.getCount());
        //使用val常量
        System.out.println(ApiConfigKt.getREQUEST_URL());
        //使用const val常量
        System.out.println(ApiConfigKt.BASE_URL);
    }
}
```
需要注意的是顶层函数和其他任意属性一样，默认是通过访问器暴露给Java使用的（也就是通过getter和setter方法）。为了方便使用，如果你想要把一个常量以public static final 的属性暴露给Java，可以用const 来修饰属性：
```
const val TAG = "tag"
这样就等同与Java的：
public static final String TAG = "tag"
```
Kotlin中通过使用顶层函数和顶层属性帮助我们消除了Java中常见的静态工具类，使我们的代码更加整洁。

# 二.Kotlin中的函数参数
### 1.函数的默认参数
对于默认参数，即使指一个函数中的参数具有默认值，这样在使用该函数的时候，可以省略一部分参数，可以减少函数的重载。
```
// 默认参数的函数使用
test()
test(1, 10f)
test(1, 10f, true)
fun test(numA: Int = 1, numB: Float = 2f, numC: Boolean = false) {
      println("numA  =  $numA \t numB = $numB \t numC = $numC")
  }
```

### 2.函数的具名参数
所为具名参数，是在传递参数的时候，指定参数的具体名称。这样做的好处就是可以不必按照参数的顺序去传值 ，调用函数时，在函数参数中给参数赋值。
```
test(numA = 1, numB = 10f, numC = true)
```
>在kotlin中调用java方法是不能使用具名参数语法，因为jva字节码并不总是会保留参数名信息，如果一个默认参数位于其他无默认值的参数前面，那么默认值只能通过在调用函数时使用具名参数的方式来使用。

### 3.函数可变长度的参数
java中使用String...arg来表示长度不确定的参数，kotlin使用vararg关键字修饰变量，表示该类型参数的数量可变。通常因该把它放在参数列表的最后方。
```
add("xixi", "haha", "heihei")

fun add(vararg arag: String) {
  for (x in arag) {
    Log.d("Tag", x);
  }
}
```
# 三.一等公民函数
### 1.什么是一等公民函数
在程序世界里，有且不仅有这么几种权力：``创建，赋值，传递``。在JAVA中这些权力，``object 都具备，function 都不具备``。object 可以通过参数传递到另一个对象里，从而两个对象可以互相通信。函数却不行，``两个函数想要通信，必须以对象为介质``。
以 Java 举个例子：函数a，想要调用函数b。虽然a并不关心函数b是从哪儿来的，只要函数b可以完成这个特定的功能即可。但是在 Java 的世界里函数必须要依附在一个对象上，所以函数a必须依附在对象A上，函数b必须依附在对象B上，函数a必须通过一个对象才能找到函数b，如下：
```
public class A {
	public void a(Object o) {
		System.out.println("a is invoked");
		o.getClass().getMethod("b").invoke(o);
   }
}

public class B {
	public void b() {
		System.out.println("b is invoked");
	}
}

```

函数b可以这样传递给函数a：

```
new A().a(new B());
```
结果如下：
```
a is invoked
b is invoked
```
>通过这个简单的例子，可以看出，非一等公民的函数生存条件有多么的恶劣，通讯的阻力有多大。 在函数是一等公民的世界里，函数a可以不再依附于对象A而单独存在，函数a可以直接与函数b交流，不再需要通过对象才能找到函数b。

函数是``"一等公民"``特点指的就是函数与变量、对象类型一样，处于平等地位。一等公民函数有三个主要的特点。
- 函数可以赋值给一个变量。
- 函数可以作为参数传入另一个函数。
- 函数可以作为别的函数的返回值。

### 2.一等公民函数可以赋值给一个变量
既然函数可以赋值给一个变量，那么这个变量的类型就是函数类型。Kotlin 中每一个函数都有一个类型，称为 “函数类型”，函数类型是一种数据类型，它与 Int、Boolean等数据类型 在使用场景上没有区别。“::” 可以取出函数的地址引用。
例如：
```
// 计算一个矩形面积  (Double, Double) -> Double
fun rectangleArea(width: Double, height: Double): Double {
    return width * height
}

fun main(args: Array<String>) {
   //通过::取出rectangleArea函数的地址 将函数rectangleArea赋值给一个变量areaFunction，此时areaFunction变量的类型为(Double, Double) -> Double
   val areaFunction: (Double, Double) -> Double = ::rectangleArea
   val area = areaFunction(50.0, 40.0) //靠变量来调用函数
   println(area)                       // 2000.0
}
```
一些相对简单的函数类型：
- () -> Unit:无参、无返回值的函数类型(Unit 返回类型不可省略)。
- (T) -> Unit:接收T类型参数、无返回值的函数类型。
- (T,A) -> Unit:接收T类型和A类型参数、无返回值的函数类型(多个参数同理)。
- (T) -> R:接收T类型参数，并且返回R类型值的函数类型。
- (T,A) -> R:接收T类型和A类型参数、并且返回R类型值的函数类型(多个参数同理)。

### 3.一等公民函数可以作为参数传递
函数可以作为参数进行传递，如果函数可以作为参数进行传递，那么就可以将不同函数进行组合，提高代码的复用，代码会更简洁，这部分就可以引出高阶函数，类似f(g(x))的形式。
```
// 计算一个矩形面积  (Double, Double) -> Double
fun rectangleArea(width: Double, height: Double): Double {
    return width * height
}

//计算一个三角形面积
fun triangleArea(bottom: Double, height: Double): Double {
    return (bottom * height) / 2
}

//获取面积
fun getAreaByFun(funName: (Double, Double) -> Double, a: Double, b: Double): Double {
    return funName(a, b)
}

fun main(args: Array<String>) {
    //参数为函数,传入不同的函数类型
    var triangleArea: Double = getAreaByFun(::triangleArea, 10.0, 15.0)
    print(triangleArea)
    var rectangleArea = getAreaByFun(::rectangleArea, 10.0, 15.0)
    print(rectangleArea)
}
```

### 4.一等公民函数可以作为别的函数的返回值
函数可以作为返回值，那么函数内应该可以定义函数，并且函数可以返回函数内定义的函数。
```
//获取面积，返回值是一个函数的类型
fun getArea(type: String): (Double, Double) -> Double {
    val resultFunction: (Double, Double) -> Double
    if (type == "rectangle") {
        resultFunction = ::rectangleArea
    } else {
        resultFunction = ::triangleArea
    }
    return resultFunction
}

fun main(args: Array<String>) {
    //调用函数
    val rectangleAreaFun: (Double, Double) -> Double = getArea("rectangle")
    println("底 10 高 15，计算三角形面积：${rectangleAreaFun(10.0, 15.0)}")
    //调用函数
    val triangleAreaFun: (Double, Double) -> Double = getArea("triangle")
    println("底 10 高 15，计算长方形面积：${triangleAreaFun(10.0, 15.0)}")
}
```

# 四.函数式编程
函数是“一等公民”是函数式编程的核心概念。
- 使用表达式，不用语句：函数式编程关心输入和输出，即参数和返回值。在程序中使用表达式可以有返回值，而语句没有。例如控制结构中的 if 和 when 结构都属于表达式。
- 高阶函数：函数式编程支持高阶函数，所谓的高阶函数就是一个函数可以作为另一个函数的参数或返回值。
- 无副作用：是指函数执行过程会返回同一个结果，不会修改外部变量，这就是“纯函数”，同样的输入参数一定会有同样的输出结果。
>Kotlin 语言支持函数式编程，提供了函数类型、高阶函数 和 Lambda 表达式。

# 五.Kotlin中的匿名函数
匿名函数就是没有名字的函数对象(注意匿名函数不是函数，而是函数类型的对象)，大多数情况下定义的函数都是具名函数(有名字的函数)。匿名函数就是只定义参数列表、返回值类型和函数体，把一个匿名函数赋给一个没有定义函数体的函数对象。
那这种没有匿名函数我们怎么调用呢？答案是无法直接调用。 匿名函数可以赋值给一个变量，或者当作实参直接传递给一个函数类型的形参。
具名函数如下：
```
fun sum(arg1 : Int,arg2 : Int): Int{
  return arg1 + arg2
}
```
这个函数的名字就叫sum。
那匿名函数定义:
```
fun(arg1 : Int, arg2 : Int) : Int{
    return arg1 + arg2
}
```
这样写还不行，因为不知道怎么去调用，所以我们需要付给一个引用，用来保存它，然后在需要使用的时候调用：
```
val sum = fun(arg1 : Int, arg2 : Int) : Int{
    return arg1 + arg2
}
```

# 六.Kotlin中的lambda表达式
### 1.定义
Lambda 表达式的本质其实就是匿名函数。而函数其实就是功能（function），匿名函数，就是匿名的功能代码了。Lambda表达式才是与高阶函数的绝配，平时我们给高阶函数中的函数类型参数传递值时，一般都会选择传入Lambda表达式，因为它足够简洁与强大。
创建一个函数类型的对象（函数字面量）有三种方式：
- 函数引用，::函数名，表示函数引用，会拿到一个 函数的对象 ；注意不是函数本身。
- 匿名函数，没有名字的函数类型的对象。
- lambda是匿名函数的表现形式也就同上。

通常这样写匿名函数：
```
val addFun = fun(x: Int, y: Int): Int {
    return x + y
}
```
使用lambda表达式可以简化：
```
//lambda表达式
val addLambda = { x: Int, y: Int -> x * y }
```

### 2.lambda表达式语法
- 总是被大括号扩着
- 其参数（如果存在）在->之前声明（参数类型可以省略）
- 函数体（如果存在）在->后面
![](/images/c052b33a825ab971d91dc7e21d4f9d7f.webp)

1. 无参数的情况
``val/var 变量名 = { 操作代码 }``
```
val sum = { }
```
2. 有参数的情况
``val/var 变量名：(参数类型，参数类型，...)->返回值类型 = (参数1，参数2，...->操作参数的代码)``
```
val sum:(Int,Int)->Int = {a,b->a+b}
```
可等价于(此种写法：即表达式的返回值类型会根据操作代码自推导出来)
``val/var 变量名 = {参数1：类型，参数2：类型...->操作代码}``
```
val sum={a:Int,b:Int ->a+b}
```
3.lambda表达式作为函数中的参数的时候
```
fun sum(a:Int,参数名：(参数1：类型，参数2：类型...)->表达式返回类型){
...
}
```

### 3.lambda表达式简化语法
1. 当 lambda 表达式只接受一个参数时，该参数可以省略，使用时用 it 来表示该参数:
```
add("xxx", { s -> s + "xxx" })
//等同于
add("xxx", { it + "xxx" })
```
2. 当函数最后一个参数为函数时，该函数可以写在 () 外，并用 {} 包裹
```
add("xxx", { s -> s + "xxx" })
//等同于
add("xxx") { s -> s + "xxx" }
//等同于
foo("xxx") { it + "xxx" }
```
3. 当函数只有一个参数，且该参数为函数时，可以直接省去 ()
```
foo({ s -> s + "xxx" }) 
//等同于
foo { s -> s + "xxx" }
```
4. 当参数在函数体中没有引用时，可以将其设为 _，若此时只有一个参数（且该参数没有被引用），则可以直接省略该参数；若有两个或以上的参数，就算全部都没有被引用，也不可以省略
```
foo({ s -> print("xxx") })
//等同于
foo({ _ -> print("xxx") })
//等同于
foo({ print("xxx") })
//等同于
foo { print("xxx") }
```

### 4.lambda表达式的返回值
lambda表达式返回值总是返回函数体内部最后一行表达式的值。 lambda表达式语法缺少指定函数的返回类型的能力，因此Lambda表达式不能指定返回值类型，当需要显式指定返回类型时，可以使用匿名函数。
```
fun(x: Int, y: Int): Int {
    return x + y
}
```

### 5.在android使用Lambda的例子
Java8 开始支持 Lambda 表达式 Java 在使用 单 抽象方法的接口时，允许使用 lambda 表达式 在 Kotlin 中就不支持这么写了，因为没有必要（可以直接传函数对象）但在 Kotlin 和 Java 做交互的时候可以这么写。 首先来通过一个例子直观感受一下lambda表达式。Android开发中经常会给一个Button设置OnClickListener。
比如我们需要让按钮点击后消失，平时我们可能是这样写的：
```
//传统Java式写法
mButton.setOnClickListener(new View.OnClickListener() {
        @Override
        public void onClick(View view) {
            view.setVisibility(View.GONE);
        }
    });
```
而在Kotlin中，使用函数式语法，我们可以这样写：
```
//Kotlin函数式写法
mButton.setOnClickListener { 
    it.visibility = View.GONE
}
```
直观来讲，似乎跟我们平时的写法差别有点大，比如，函数调用的小括号不见了，匿名内部类直接被一个函数体取代了，View参数不见了，分号也消失了，还有那个it是什么……其实，就像数学公式推导一样，精简的写法也是通过一步一步简化来的。下面就让我们来看一下代码的“推导过程”：

1. 首先，代码段1转换为Kotlin代码，并替换为函数式写法：
```
mButton.setOnClickListener({ view: View ->
    view.visibility = View.GONE
})
```
这段代码非常清晰，花括号包裹的是一段lambda表达式，可以把它作为实参传递给函数，这一步把匿名内部类省略掉了；另外也干掉了分号，因为在Kotlin中行末尾的分号可以省略；最后还省略了set方法，在Kotlin中，会默认把对属性的直接访问转换成get/set方法调用。

2. 然后，根据Kotlin的语法约定，如果lambda表达式是函数调用的最后一个实参，就可以把它挪到小括号外面：
```
mButton.setOnClickListener() { view: View ->
    view.visibility = View.GONE
}
```
3. 当lambda是函数的唯一实参，就可以去掉空的小括号对：
```
mButton.setOnClickListener { view: View ->
    view.visibility = View.GONE
}
```
4. 如果lambda的参数的类型可以被编译器推导出来，就可以省略它：
```
mButton.setOnClickListener { view ->
    view.visibility = View.GONE
}
```
5. 最后，如果这个lambda只有一个参数，并且这个参数的类型可以被推断出来（也就是同时满足3和4），那么这个参数也可以省略掉。代码中引用这个参数的地方可以通过编译器自动生成的名称it来替代：
```
mButton.setOnClickListener {
    it.visibility = View.GONE
}
```
经过上述5个步骤，就得到了最简洁、最清晰的代码段。

# 七.Kotlin中的闭包
### 1.闭包的定义
程序的变量分为全局变量和局部变量，全局变量，顾名思义，其作用域是当前文件甚至文件外的所有地方；而局部变量，我们只能再其有限的作用域里获取。 那么，如何在外部调用局部变量呢？答案就是——闭包，与此给闭包下个定义：
闭包就是能够读取其他函数内部变量的函数。即是函数中包含函数，这里的函数我们可以包含（Lambda表达式，匿名函数，局部函数，对象表达式）。
```
fun test1(){
     fun test2(){
      
     }
}
```

### 2.闭包使用
我们来看一个闭包的例子：
```
fun returnFun(): () -> Int {
    var count = 0
    return { count++ }
}

fun main() {
    val function = returnFun()
    val function2 = returnFun()
    println(function()) // 0
    println(function()) // 1
    println(function()) // 2

    println(function2()) // 0
    println(function2()) // 1
    println(function2()) // 2
}
```
returnFun返回了一个函数，这个函数没有入参，返回值是Int。我们可以用变量接收它，还可以调用它。function和function2分别是创建的两个函数实例。 每调用一次function()，count都会加一，说明count 被function持有了而且可以被修改。而function2和function的count是独立的，不是共享的。
通过 jadx 反编译可以看到：
```
public final class ClosureKt {
    @NotNull
    public static final Function0<Integer> returnFun() {
        IntRef intRef = new IntRef();
        intRef.element = 0;
        return (Function0) new 1<>(intRef);
    }

    public static final void main() {
        Function0 function = returnFun();
        Function0 function2 = returnFun();
        System.out.println(((Number) function.invoke()).intValue());
        System.out.println(((Number) function.invoke()).intValue());
        System.out.println(((Number) function2.invoke()).intValue());
        System.out.println(((Number) function2.invoke()).intValue());
    }
}
```
被闭包引用的 int 局部变量，会被封装成 IntRef 这个类。这个 IntRef 里面保存着 int 变量，原函数和闭包都可以通过 intRef 来读写 int 变量。Kotlin 正是通过这种办法使得局部变量可修改。除了 IntRef，还有 LongRef，FloatRef 等，如果是非基础类型，就统一用 ObjectRef 即可。

### 3.闭包捕获变量
闭包可以访问函数体之外的变量，这个过程称为捕获变量。
```
var value = 0// 全局变量
fun main(args: Array<String>?) {
    // 局部变量
    var localValue = 20

    val result = { a: Int ->
        value++
        localValue++
        val c = a + value + localValue
        println(c)
    }

    result(30)

    println("value = $value")
    println("localValue = $localValue")
}

System.out: 52
System.out: value = 1
System.out: localValue = 21
```
闭包是捕获 value 和 localValue 变量的 Lambda 表达式。

**Java 与 Koltin 中 Lambda 捕获局部变量区别**
在函数不是“一等公民”的 Java 这里，匿名类其实就是代替闭包而存在的。只不过 Java 严格要求所有函数都需要在类里面，所以巧妙的把“声明一个函数”这样的行为变成了“声明一个接口”或“重写一个方法”。
匿名类也可以捕获当前环境的 final 局部变量。但和闭包不一样的是，匿名类无法修改捕获的局部变量（final 不可修改）。而匿名类能引用 final 的局部变量，是因为在编译阶段，会把该局部变量作为匿名类的构造参数传入。
因为匿名类修改的变量不是真正的局部变量，而是自己的构造参数，外部局部变量并没有被修改。所以 Java 编译器不允许匿名类引用非 final 变量。jdk7在 Lambda 体中只能读取局部变量，不能修改局部变量。
而 kotlin 中没有这个限制，可以读取和修改局部变量。如下面代码：
```
// 声明了一个Java代码接口
public interface Clickable {
    void onClick();
}

// Java中的Lambda表达式局部变量捕获
public class Closure {
    private void closure(Clickable clickable) {
        clickable.onClick();
    }
    public void main(ArrayList<String> args) {
        int count = 0;
        closure(() -> {
            count += 1; // 编译错误，count需要使用final修饰
        });
        System.out.println(count);
    }
}
```
这样的Java代码是编译不过的，必须设置为 count 为 final 才能通过编译，但又不能对 count 进行修改，如果非要修改 count 只能把 count 声明为 Closure 的成员变量。
对比 Kotlin 代码实现：
```
class Closure {

    private fun closure(clickable: Clickable) {
        clickable.onClick()
    }

    fun main(args: Array<String>) {
        var count: Int = 0
        closure(Clickable { count += 1 }) // 编译正常
        println(count)  // 2
    }
}
```
再来看一个闭包的例子：
```
fun returnFun(): () -> Int {
    var count = 0
    return { count++ }
}

fun main() {
    val function = returnFun()
    val function2 = returnFun()
    println(function()) // 0
    println(function()) // 1
    println(function()) // 2

    println(function2()) // 0
    println(function2()) // 1
    println(function2()) // 2
}
```
每调用一次function()，count都会加一，说明count 被function持有了而且可以被修改。而function2和function的count是独立的，不是共享的。

# 八.Kotlin中的扩展函数
扩展函数数是指在一个类上增加一种新的行为，甚至我们没有这个类代码的访问权限。在Java中，通常会实现很多带有static方法的工具类，而Kotlin中扩展函数的一个优势是我们不需要在调用方法的时候把整个对象当作参数传入， 它表现得就像是属于这个类的一样，而且我们可以使用this关键字和调用所有public方法。
```
fun 被扩展类名.扩展函数名( 参数 ){
   //实现代码
}
```
Java调用Kotlin扩展函数:
```
扩展类名Kt.扩展函数名(参数);
```
# 九.Kotlin中的内联函数
### 1.inline关键字
如果没有内联修饰符标记函数，在使用lambda会带来性能开销。举个接收函数类型的例子:
```
//callAction 接受一个函数类型(lambda)
private fun callAction(action: () -> Unit) {
    println("call Action before")
    action()
    println("call Action after")
}

fun main(args: Array<String>) {
    callAction {
        println("call action")
    }
}
```
反编译为:
```
public final void main(@NotNull String[] args) {
      callAction((Function0)null.INSTANCE);
}

 private final void callAction(Function0 action) {
      String var2 = "call Action before";
      boolean var3 = false;
      System.out.println(var2);
      action.invoke();
      var2 = "call Action after";
      var3 = false;
      System.out.println(var2);
   }
```
由此可见当调用``callAction(action: () -> Unit)`` 时，传递的lambda会被Function0所代替，而Function0是一个被定义为如下的接口:
```
public interface Function0<out R> : Function<R> {
    public operator fun invoke(): R
}
```
在调用callAction时，编译器会额外生成一个Function0的实例传递给callAction，内部会调用 Function0 的 invoke() 方法。因此使用lambda会带来额外的性能开销。
可以通过内联函数消除lambda带来的运行时开销。被inline标记的函数就是内联函数，其原理就是：在编译时期，把调用这个函数的地方用这个函数的方法体进行替换。 在函数被使用的时候编译器并不会生成函数调用的代码，
而是使用函数实现的真实代码替换每一次的函数调用。还是拿 callAction(action: () -> Unit) 方法举例，当给该函数添加inline修饰符后，编译后的调用代码如下
```
public final void main(@NotNull String[] {
      ...省略无关紧要的代码
      System.out.println("call Action before");
      System.out.println("call action");
      System.out.println("call Action after");
}
```
总结下:
- 被inline修饰的函数叫内联函数。
- 内联函数会在被调用的位置内联。内联函数的代码会被拷贝到使用它的位置，并把lambda替换到其中。

>在kotlin中lambda 表达式会被正常地编译成匿名类。这表示每调用一次lambda 表达式，一个额外的类就会被创建。并且如果lambda 捕捉了某个变量，那么每次调用的时候都会创建一个新的对象。这会带来运行时的额外开销，导致使用lambda 比使用一个直接执行相同代码的函数效率更低。
如果使用 inline 修饰符标记一个函数，在函数被使用的时候编译器并不会生成函数调用的代码，而是使用函数实现的真实代码替换每一次的函数调用。

### 2.noinline关键字
虽然内联非常好用，但是会出现这么一个问题，就是内联函数的参数(ps:参数是函数,比如上面的body函数)如果在内联函数的方法体内被其他非内联函数调用，就会报错。
例如:
```
inline fun <T> mehtod(lock: Lock, body: () -> T): T {
            lock.lock()
            try {
                otherMehtod(body)//会报错
                return body()
            } finally {
                lock.unlock()
            }
    }
    fun <T> otherMehtod(body: ()-> T){

    }
```
原因:因为method是内联函数，所以它的形参也是inline的，所以body就是inline的，但是在编译时期，body已经不是一个函数对象，而是一个具体的值，然而otherMehtod却要接收一个body的函数对象，所以就编译不通过。
解决方法:当然就是加noinline了，它的作用就已经非常明显了。就是让内联函数的形参函数不是内联的，保留原有的函数特征。
具体操作:
```
fun main(args: Array<String>) {
    val lock = ReentrantLock()
    mehtod(lock,{"body方法体"})
}

inline fun <T> mehtod(lock: Lock, noinline body: () -> T): T {
    lock.lock()
    try {
        otherMehtod(body)
        return body()
    } finally {
        lock.unlock()
    }
}

fun <T> otherMehtod(body: ()-> T){

}
```
这样编译时期这个body函数就不会被内联了,反编译看下:
```
   public static final void main(@NotNull String[] args) {
      Intrinsics.checkParameterIsNotNull(args, "args");
      ReentrantLock lock = new ReentrantLock();
      //这里是生成了一个函数对象
      Function0 body$iv = (Function0)null.INSTANCE;
      ((Lock)lock).lock();

      try {
         otherMehtod(body$iv);
         Object var3 = body$iv.invoke();
      } finally {
         ((Lock)lock).unlock();
      }

   }

   public static final Object mehtod(@NotNull Lock lock, @NotNull Function0 body) {
      Intrinsics.checkParameterIsNotNull(lock, "lock");
      Intrinsics.checkParameterIsNotNull(body, "body");
      lock.lock();

      Object var3;
      try {
         otherMehtod(body);
         var3 = body.invoke();
      } finally {
         InlineMarker.finallyStart(1);
         lock.unlock();
         InlineMarker.finallyEnd(1);
      }

      return var3;
   }

   public static final void otherMehtod(@NotNull Function0 body) {
      Intrinsics.checkParameterIsNotNull(body, "body");
   }
```

### 3.crossinline关键字
很少用到crossinline修饰符，crossinline 的作用是内联函数中让被标记为crossinline 的lambda表达式不允许非局部返回。 在kotlin中，return 只可以用在有名字的函数，或者匿名函数中，使得该函数执行完毕。
而针对lambda表达式，你不能直接使用return你可以使用return+label的形式，将这个lambda结束。但是若你的lambda应用在一个内联函数的时候，这时候你可以在lambda中使用return 可以这么理解，内联函数在编译的时候，
将相关的代码贴入你调用的地方。 lambda表达式就是一段代码而已，这时候你在lambda中的return，相当于在你调用的方法内return crossinline就是为了让其不能直接return。

# 十.Kotin的lambda的简化回调函数
在Kotlin中对Java中的一些的接口的回调做了一些优化，可以使用一个lambda函数来代替。可以简化写一些不必要的嵌套回调方法。但是需要注意:**在lambda表达式，只支持单抽象方法模型，也就是说设计的接口里面只有一个
抽象的方法，才符合lambda表达式的规则，多个回调方法不支持。**
1. 用Java代码实现一个接口的回调:
```
mView.setEventListener(new ExamPlanHomeEventListener(){
   public void onSuccess(Data data){
     //todo
   }
});
```
2. 在Kotlin中的实现一个接口的回调，不使用lambda表达式(``这种方式非常适用于kotlin中对于一个接口中含有多个回调方法``):
```
mView.setEventListener(object: ExamPlanHomeEventListener{
  public void onSuccess(Data data){
    //todo
  }
});
```
3.如果在Kotlin中的对于**接口只有一个回调的方法**，可以使用lambda函数简化:
```
mView.setEventListener({
   data: Data ->
   //todo
})

//或者可以直接省略Data，借助kotlin的智能类型推导

mView.setEventListener({
   data ->
   //todo
})
```
4. 如果以上代码中的**data参数没有使用**到的话，可以直接把data去掉:
```
mView.setEventListener({
  //todo

})
```
5. 以上代码还可以做个调整，由于setEventListener函数**最后一个参数是一个函数**的话，可以直接把括号的实现提到圆括号外面:
```
mView.setEventListener(){
   //todo
}
```
6. 由于setEventListener这个函数**只有一个参数**，可以直接省略圆括号:
```
mView.setEventListener{
  //todo
}
```
# 十一.Kotlin中的作用域函数
### 1.let函数
当需要定义一个变量在一个特定的作用域时，可以考虑使用 let 函数。更多的是用于避免 Null 判断。在 let 函数内部，用 it 指代调用 let 函数的对象，并且最后返回最后的计算值。
1. let函数的使用
```
//一般结构
object.let{
    //用 it 指代 object 对象
    //todo() 是 object对象的共有属性或方法
    //it.todo() 的返回值作为 let 函数的返回值返回
    it.todo()
...
}

//另一种用途 判断object为null的操作
object?.let{
  //表示object不为null的条件下，才会去执行let函数体
it.todo()
}
```
2. let函数底层的inline扩展函数+lambda结构
```
@kotlin.internal.InlineOnly
public inline fun <T, R> T.let(block: (T) -> R): R = block(this)
```
从源码let函数的结构来看它是只有一个lambda函数块block作为参数的函数，调用T类型对象的let函数，则该对象为函数的参数。在函数块内可以通过 it 指代该对象。返回值为函数块的最后一行或指定return表达式。

3. let函数适用的场景:
- 最常用的场景就是使用let函数处理需要针对一个可null的对象统一做判空处理。
- 然后就是需要去明确一个变量所处特定的作用域范围内可以使用。
let函数使用前后的对比:
```
//没有使用let函数的代码是这样的，看起来不够优雅
mTextView?.text = "TextView"
mTextView?.setTextColor(ContextCompat.getColor(this, R.color.colorAccent))
mTextView?.textSize = 10f

//使用let函数后的代码是这样的
mTextView?.let {
    it.text = "TextView"
    it.setTextColor(ContextCompat.getColor(this, R.color.colorAccent))
    it.textSize = 10f
}
```

### 2.with函数
with 和 let 类似，with 最后也包含一段函数块，也是将最后的计算的结果返回。但是 with 不是以拓展的形式存在的。其将某个对象作为函数的参数，并且以 this 指代。
1. with函数使用
```
with(object){
     // todo() 是 object 对象的共有属性或方法
    // todo() 的返回值作为 with 函数的返回值返回
   todo()
}
```
2. with函数底层的inline扩展函数+lambda结构
```
@kotlin.internal.InlineOnly
public inline fun <T, R> with(receiver: T, block: T.() -> R): R = receiver.block()
```
with函数不是以扩展的形式存在的。它是将某对象作为函数的参数，在函数块内可以通过 this 指代该对象。返回值为函数块的最后一行或指定return表达式。with函数是接收了两个参数，分别为T类型的对象receiver和一个lambda函数块，所以with函数最原始样子如下:
```
val result = with(user, {
  println("my name is $name, I am $age years old, my phone number is $phoneNum")
  1000
})
```
由于with函数最后一个参数是一个函数，可以把函数提到圆括号的外部，所以最终with函数的调用形式如下:

```
val result = with(user) {
 println("my name is $name, I am $age years old, my phone number is $phoneNum")
 1000 //返回值
}
```
3. with函数的适用的场景
适用于调用同一个类的多个方法时，可以省去类名重复，直接调用类的方法即可，经常用于Android中RecyclerView中onBinderViewHolder中，数据model的属性映射到UI上。
没有使用kotlin中的实现：
```
@Override
public void onBindViewHolder(ViewHolder holder, int position) {

   ArticleSnippet item = getItem(position);
      if (item == null) {
          return;
      }
      holder.tvTitle.setText(item.titleEn);
      holder.tvSummary.setText(item.summary);
      String gradeInfo = "难度：" + item.gradeInfo;
      String wordCount = "单词数：" + item.length;
      String reviewNum = "读后感：" + item.numReviews;
      String extraInfo = gradeInfo + " | " + wordCount + " | " + reviewNum;
      holder.tvExtraInfo.setText(extraInfo);
      ...
}

```
kotlin的实现：
```
override fun onBindViewHolder(holder: ViewHolder, position: Int){
   val item = getItem(position)?: return
   with(item){
       holder.tvNewsTitle.text = StringUtils.trimToEmpty(titleEn)
       holder.tvNewsSummary.text = StringUtils.trimToEmpty(summary)
       holder.tvExtraInf.text = "难度：$gradeInfo | 单词数：$length | 读后感: $numReviews"
       ...   
   }
}
```

### 3.run函数
既有 let 函数那样又优雅的判空，又能有 with 函数省去同一个对象多次设置属性的便捷写法。非 run 函数莫属了。run 函数基本是 let 和 with 的结合体，对象调用 run 函数，接收一个 lambda 函数为参数，传入 this 并以闭包形式返回，返回值是最后的计算结果。
1. run函数使用的一般结构
```
object.run{
    // todo() 是 object 对象的共有属性或方法
    // todo() 的返回值作为 run 函数的返回值返回
     todo() 
}
```
2. run函数的inline+lambda结构
```
@kotlin.internal.InlineOnly
public inline fun <T, R> T.run(block: T.() -> R): R = block()
```
>run函数实际上可以说是let和with两个函数的结合体，run函数只接收一个lambda函数为参数，以闭包形式返回，返回值为最后一行的值或者指定的return的表达式。

3. run函数的适用场景
适用于let，with函数任何场景。因为run函数是let，with两个函数结合体，准确来说它弥补了let函数在函数体内必须使用it参数替代对象，在run函数中可以像with函数一样可以省略，直接访问实例的公有属性和方法，另一方面它弥补了with函数传入对象判空问题，在run函数中可以像let函数一样做判空处理。
没有使用kotlin中的实现：
```
override fun onBindViewHolder(holder: ViewHolder, position: Int){
   val item = getItem(position)?: return
   with(item){
       holder.tvNewsTitle.text = StringUtils.trimToEmpty(titleEn)
       holder.tvNewsSummary.text = StringUtils.trimToEmpty(summary)
       holder.tvExtraInf = "难度：$gradeInfo | 单词数：$length | 读后感: $numReviews"
       ...   
   }
}
```
使用run函数后的优化：
```
override fun onBindViewHolder(holder: ViewHolder, position: Int){
  getItem(position)?.run{
       holder.tvNewsTitle.text = StringUtils.trimToEmpty(titleEn)
       holder.tvNewsSummary.text = StringUtils.trimToEmpty(summary)
       holder.tvExtraInf = "难度：$gradeInfo | 单词数：$length | 读后感: $numReviews"
       ...   
   }
}
```

### 4.apply函数
apply 函数和 run 函数很像，但是 apply 最后返回的是调用对象自身。

1. apply函数使用的一般结构
```
object.apply{
  // todo() 是 object 对象的共有属性或方法
  todo() 
  "test" // 最后返回的是 object 对象，而不是 test
}
```
2. apply函数的inline+lambda结构
```
@kotlin.internal.InlineOnly
public inline fun <T> T.apply(block: T.() -> Unit): T { block(); return this }
```
从结构上来看apply函数和run函数很像，唯一不同点就是它们各自返回的值不一样，run函数是以闭包形式返回最后一行代码的值，而apply函数的返回的是传入对象的本身。
3. apply函数的适用场景
整体作用功能和run函数很像，唯一不同点就是它返回的值是对象本身，而run函数是一个闭包形式返回，返回的是最后一行的值。正是基于这一点差异它的适用场景稍微与run函数有点不一样。apply一般用于一个对象实例初始化的时候，需要对对象中的属性进行赋值。或者动态inflate出一个XML的View的时候需要给View绑定数据也会用到，这种情景非常常见。特别是在我们开发中会有一些数据model向View model转化实例化的过程中需要用到。
apply函数使用前后的对比
没有使用apply函数的代码是这样的，看起来不够优雅
```
mSheetDialogView = View.inflate(activity, R.layout.biz_exam_plan_layout_sheet_inner, null)
        mSheetDialogView.course_comment_tv_label.paint.isFakeBoldText = true
        mSheetDialogView.course_comment_tv_score.paint.isFakeBoldText = true
        mSheetDialogView.course_comment_tv_cancel.paint.isFakeBoldText = true
        mSheetDialogView.course_comment_tv_confirm.paint.isFakeBoldText = true
        mSheetDialogView.course_comment_seek_bar.max = 10
        mSheetDialogView.course_comment_seek_bar.progress = 0
```
使用apply函数后的代码是这样的

```
mSheetDialogView = View.inflate(activity, R.layout.biz_exam_plan_layout_sheet_inner, null).apply{
   course_comment_tv_label.paint.isFakeBoldText = true
   course_comment_tv_score.paint.isFakeBoldText = true
   course_comment_tv_cancel.paint.isFakeBoldText = true
   course_comment_tv_confirm.paint.isFakeBoldText = true
   course_comment_seek_bar.max = 10
   course_comment_seek_bar.progress = 0
}

```
多层级判空问题
```
    if (mSectionMetaData == null || mSectionMetaData.questionnaire == null || mSectionMetaData.section == null) {
            return;
        }
        if (mSectionMetaData.questionnaire.userProject != null) {
            renderAnalysis();
            return;
        }
        if (mSectionMetaData.section != null && !mSectionMetaData.section.sectionArticles.isEmpty()) {
            fetchQuestionData();
            return;
        }
```
kotlin的apply函数优化
```
 mSectionMetaData?.apply{
            //mSectionMetaData不为空的时候操作mSectionMetaData
        }?.questionnaire?.apply{
            //questionnaire不为空的时候操作questionnaire
        }?.section?.apply{
            //section不为空的时候操作section
        }?.sectionArticle?.apply{
            //sectionArticle不为空的时候操作sectionArticle
        }
```

### 5.also函数
also函数和 let 函数类似，唯一的区别就是 also 函数的返回值是调用对象本身。
1. also函数使用的一般结构
```
object.also{
    // 用 it 指代 object 对象
    // todo() 是 object 对象的共有属性或方法
    it.todo() 
    "test" // 将返回 any 对象，而不是 test
}
```
2. also函数的inline+lambda结构
```
@kotlin.internal.InlineOnly
@SinceKotlin("1.1")
public inline fun <T> T.also(block: (T) -> Unit): T { block(this); return this }
```
>also函数的结构实际上和let很像唯一的区别就是返回值的不一样，let是以闭包的形式返回，返回函数体内最后一行的值，如果最后一行为空就返回一个Unit类型的默认值。而also函数返回的则是传入对象的本身。

3. also函数的适用场景
适用于let函数的任何场景，also函数和let很像，只是唯一的不同点就是let函数最后的返回值是最后一行的返回值而also函数的返回值是返回当前的这个对象。一般可用于多个扩展函数链式调用
   
### 6.let，with，run，apply，also函数区别
通过以上几种函数的介绍，可以很方便优化kotlin中代码编写，整体看起来几个函数的作用很相似，但是各自又存在着不同。使用的场景有相同的地方比如run函数就是let和with的结合体。下面一张表格可以清晰对比出他们的不同之处。
| 函数名 | 函数体内使用的对象 | 返回值 | 是否是扩展函数 | 适用的场景 |
| --- |  --- | --- | --- | --- |
| let |  it指代当前对象 | 闭包形式返回 | 是 | 适用于处理不为null的操作场景 |
| with | this指代当前对象或者省略 | 闭包形式返回 | 否 | 适用于调用同一个类的多个方法时，可以省去类名重复，直接调用类的方法即可，经常用于Android中RecyclerView中onBinderViewHolder中，数据model的属性映射到UI上 |
| run | this指代当前对象或者省略 | 闭包形式返回 | 是 | 适用于let，with函数任何场景。 |
| apply | this指代当前对象或者省略 | 返回this | 是 | 1、适用于run函数的任何场景，一般用于初始化一个对象实例的时候，操作对象属性，并最终返回这个对象。

### 7.Kotlin中的作用域函数选择
![](/images/991e7ee32a7e351f8fef03f47ac8fafd.webp)

参考自：
[kotlin官方文档](https://www.kotlincn.net/docs/reference/constructing-collections.html)








