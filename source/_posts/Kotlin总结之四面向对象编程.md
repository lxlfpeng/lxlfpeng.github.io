---
title: Kotlin总结之四面向对象编程
---

# 一.Kotlin类的创建
###  1.类的声明
Kotlin 类可以包含：构造函数和初始化代码块、函数、属性、内部类、对象声明。
Kotlin 中使用关键字 class 声明类，后面紧跟类名：
```
// 类名为 Apple
class Apple{  
 // 大括号内是类体构成
}
```
当类没有结构体的时候，大括号可以省略。如:
```
class Apple
```
|  类的修饰符   | 描述  |
|  -  | -  |
|    abstract    | 抽象类|
|    final       | 类不可继承，默认属性|
|    enum        | 枚举类|
|    open        | 类可继承，类默认是final的|
|    annotation  | 注解类|

|  访问权限修饰符   | 描述  |
|  -  | -  |
|    private    |  仅在同一个文件中可见|
|     protected |  同一个文件中或子类可见|
|     public    |  所有调用的地方都可见|
|     internal  |  同一个模块中可见|

### 2. 类的构造函数
在kotlin中有两种类型的构造函数：
- 主构造函数(主构造器)。
- 次级构造函数(次级构造器)。
>在Kotlin类中只有一个主构造函数(主构造器)，而辅助构造函数（次级构造器）可以是一个或者多个。
##### (1.)主构造函数
主构造函数是类头的一部分：它跟在类名（和可选的类型参数）后。
```
class 类名 construction(参数1，参数2….){  }
```
如果主构造函数没有任何注解或者可见性修饰符，可以省略这个 constructor 关键字，否则不能省略。
不能省略:
```
class Person private constructor(name:String){
 val mName: String = name
 ...
}
```
可以省略:
```
class Person(name: String) {
 val mName: String = name
  ...
}
```
如果不需要将构造函数中参数同时作为类属性,也可以写成如下形式(constructor表示构造函数,里面执行初始化的处理):
```
class Person{
    constructor(name:String){
    ....
    }
}
```
由于主构造函数没有函数体。如果需要在主构造函数中编写代码该怎么做？初始化的代码可以放 到以 init 关键字作为前缀的初始化块（initializer blocks）中,可以在这里编写要在主构造函数中完成的业务，init{...}中能使用构造函数中的参数：
```
class Person(username: String, age: Int){
	private val username: String
	private var age: Int
	init{
		this.username = username
		this.age = age
	}
}
```
注意，主构造的参数可以在初始化块中使用。它们也可以在 类体内声明的属性初始化器中使用：
```
class Person(name: String) {
    val name= name+"..."
    ...
}
```
事实上，声明属性以及从主构造函数初始化属性，Kotlin 有简洁的语法：
```
class Person(var name: String, var age: Int) {
    ...
}
```
与普通属性一样，主构造函数中声明的属性可以是 可变的（var）或只读的（val）。
##### (2.)次构造函数
类也可以声明前缀有 constructor的次构造函数，可以声明多个次构造函数：
```
class Person {
    constructor() {
        ...        
    }
   constructor(name: String) {
        ...        
    }
  constructor(name: String,age:Int) {
        ...      
    }
}
```
1. kotlin声明了主构造器
如果类有一个主构造函数，每个次构造函数需要委托给主构造函数， 可以直接委托或者通过别的次构造函数间接委托。委托到同一个类的另一个构造函数 用 this 关键字即可：
```
class Person (name : String?,age : Int) {
    var name : String?
    var age : Int
    init {
        println("执行初始化块")
        this.name = name
        this.age = age
    }
    constructor() : this(null,0) {//直接委托调用主构造器

    }
    constructor(name : String) : this() {//间接委托调用主构造器
        
    }
}
```
2. kotlin没声明主构造器
kotlin没声明主构造器，重载构造器不需要调用当前类的其他构造器，调用构造器时也会执行初始化块。
```
class Person {
    var name : String?
    var age : Int
    init {
        println("执行初始化块")
    }
    //在各自的构造器中对属性进行赋值
    constructor() {
        this.name = null
        this.age = 0
    }

    constructor(name : String) {
        this.name = name
        this.age = 0
    }

    constructor(name : String, age : Int) {
        this.name = name
        this.age = age
    }
}
````
如果一个非抽象类没有声明任何（主或次）构造函数，它会有一个生成的 不带参数的主构造函数。构造函数的可见性是 public。如果你不希望你的类 有一个公有构造函数，你需要声明一个带有非默认可见性的空的主构造函数(此时这个类不能够实例化)：
```
class Person private constructor () {

}
```

- 当只写了主构造函数，没有次构造函数，就会覆盖了默认的空造函数，此时创建对象只能通过你写的主构造函数来调用。
- 当只写了次构造函数，不写主构造函数，创建对象必须通过次构造函数调用，若不写空的参数构造函数，则调用空的构造函数会报错。
- 当写了既写了主构造，又写了次构造函数，可以直接调用主构造函数或者调用次构造函数创建对象。次构造函数最终都是调用主构造函数来创建对象的。

>注意：在 JVM 上，如果主构造函数的所有的参数都有默认值，编译器会生成 一个额外的无参构造函数，它将使用默认值。

# 二.Kotlin类的继承
在 Kotlin 中所有类都有一个共同的超类``Any``，没有申明超类的类是默认继承超类Any：
```
class Person // 从 Any 隐式继承
```
> Any不是 java.lang.Object；尤其是，它除了 equals()、hashCode()和toString()外没有其他属性或者方法。

在Kotlin中，所有类在默认情况下都是无法被继承的，简而言之，就是说Kotlin中，所有类在默认情况下都是final的，但如何才能被继承，Kotlin给我们提供了一个``关键字open``，只有被open修饰的类才可以被继承（关键字open的作用与final相反），否则编译器会报错。
```
open class Parent(p: Int)//申明该类是open修饰的,该类可以继承
class Child(p: Int) : Parent(p)//继承open类
```
方法重写:
```
//父类
open class Parent{
    open fun method(){}
    fun unOpen(){  //没有open显示指定，这个函数不能被重写覆盖
        println("unOpen")
    }
}

//子类
class Child: Parent() {
    ///重写覆盖的方法这里必须使用override关键字来修饰
    override fun method() {
        super.method()
    }
   override fun unOpen(){  //Child的子类不可再被重写覆盖
      super.open()
   }
}
```
>覆盖属性和覆盖方法类似。

# 三.Kotlin抽象类
和Java一样，在kotlin中，抽象类用关键字abstract修饰，抽象类的成员可以在本类中提供实现，也可以不实现而交给子类去实现，不实现的成员必须用关键字abstract声明：
```
abstract class AbsBase{
    abstract fun  method()
}
```
>在kotlin中，被继承的类需要用关键字open声明，表明该类可以被继承，但是抽象类或者抽象函数是不用 open 标注的。但是如果子类要实现抽象类的非抽象函数，需要在抽象类中将其声明为open。

抽象类有如下的特点:
- 抽象类就是为继承设计的，因此即使不用open关键字修饰，抽象类也是可以被继承的。
- 使用abstract关键字修饰的抽象函数也可以不加open。
- 抽象类中的非抽象方法如果不用open修饰的话，不能被子类覆盖。
```
abstract class AbsBase{
    abstract fun  method()   // 如果子类要实现需声明为抽象 
    open fun method1(){//非抽象方法如果要类子类实现，需要声明为open
        println("输出")
    }
}

class Child : AbsBase() {
    override fun method() {
      //抽象类的实现    
    }
    override fun method1() {
        super.method1()
        println("子类实现")
    }
}
```

# 四.Kotlin接口
### 1.接口的定义
Kotlin接口用interface作为关键字，基本上和Java的接口类似，但是kotlin的接口不仅可以有抽象方法，也可以有已实现的方法。
```
interface Animal {
    val kind: String
    val color: String

    fun doing()

    fun eat() {
        println("吃骨头")
    }
}

class Dog : Animal {
    
    override val kind = "小黑狗"
    override val color = "黑色的"

    override fun doing() {
        println("正在玩")
    }
}
```

### 2.接口和抽象类区别
-  抽象类可以为属性设置值和getter、setter，而接口不可以。
-  抽象类和接口中都可以有默认的实现方法，但接口中的方法不能有状态，即涉及到属性的值需要到实现类中设置。
-  子类只能继承一个父类，但可以实现多个接口。

### 3.解决实现多个接口导致的覆盖冲突
Kotlin中可以实现多个接口,可能会出现继承了同一个方法的多个实现。``调用应该使用super<类名>.同名方法的形式调用``，举个例子：
```
interface A {
    fun foo() {
        println("A")
    }
    fun bar()
}

interface B {
    fun foo() {
        println("B")
    }
    fun bar() {
        println("bar")
    }
}

class C : A {
    override fun bar() {
        println("C.bar")
    }
}

class D : A, B {
    override fun foo() {
        super<A>.foo()
        super<B>.foo()
        println("D.foo")
    }

    override fun bar() {
        super<B>.bar()
    }
}

fun main(args: Array<String>) {
    var d = D()
    d.foo()
    d.bar()
}
```

# 五.Kotlin的嵌套类
只要将一个类放在另一个类中定义，这个类就变成了嵌套类，相当于Java中static修饰的静态内部类。
```
class Outer {                  // 外部类
    private val value: Int = 1

    class Nested {             // 嵌套类
        var inValue = 2
        fun nestedMethod() {
            // println(value)       //嵌套类无法直接访问外部类属性
            println(Outer().value) //但可以通过外部类的对象访问，因为有private修饰符，普通类通过对象也无法访问
        }
    }

    fun outerMethod() {
        // println(inValue)         //外部类无法直接访问嵌套类的属性
        // method()                 //外部类无法直接访问嵌套类的方法
        println(Nested().inValue) //外部类无法通过嵌套类的对象访问private属性，但是可以访问public
    }
}

fun main() {
    val demo = Outer.Nested().inValue // 调用格式：外部类.嵌套类.嵌套类方法/属性
    println(demo)    // == 2
}
```

# 六.Kotlin的内部类
内部类是一种特殊的嵌套类，被嵌套到里面的类使用inner关键字修饰，内部类可以拥有对外部类的引用。但是外部类没有内部类的引用。所以内部类可以访问外部类成员属性和成员函数。
内部类的特点:
- 内部类成员可以直接访问外部类的私有数据，因为内部类相当于外部类的成员之一。
- 外部类不能访问内部类的成员，如需访问，需要通过创建内部类对象，通过对象访问内部类成员。
```
class Outer {
    private val value1: Int = 1
    var value2 = "成员属性"

    //嵌套内部类
    inner class Inner {
        fun innerFun() = value1  // 访问外部类成员
        fun innerTest() {
            val outer = this@Outer //获取外部类的成员变量
            println("内部类可以引用外部类的成员，bar：${innerFun()}")
            println("内部类可以引用外部类的成员，例如：${outer.value2}")
        }
    }
}

fun main(args: Array<String>) {
    val demo = Outer().Inner().innerFun()
    println(demo) //   1
    Outer().Inner().innerTest()
}
```
为了消除歧义，要访问来自外部作用域的 this，我们使用this@label，其中 @label是一个 代指 this 来源的标签。

# 七.Kotlin的匿名内部类
名内部类主要是针对那些获取抽象类或者接口对象而来的。最常见的匿名内部类点击事件：
```
interface OnClickListener {
    fun onClick()
}

class View {
    fun setClickListener(clickListener: OnClickListener) {

    }
}

fun main(args: Array<String>) {
    val view = View()
    view.setClickListener(object : OnClickListener {
        override fun onClick() {

        }
    })
}
```

# 八.Kotlin的伴生对象 Companion Objects
与Java不同的是，在kotlin中，类是没有显式的定义static方法和static成员变量的。大多数情况下，推荐顶层函数。但是顶层函数不能访问类的private成员，因此需要通过伴生对象的形式间接提供的。
Kotlin语言中使用"companion object"修饰静态方法，可以使用类名.方法名的形式调用，如下：
```
class Util {
    companion object {
        fun getCurrentVersion(): String {
            return BuildConfig.VERSION_NAME
        }
    }
}
```
调用：
```
var version_name2 = Util .getCurrentVersion()
```
伴生对象的特点:
- 每个类最多定义一个伴生对象；
- 伴生对象相当于外部类的对象，可以直接通过外部类名访问伴生对象的成员；
- 由于kotlin取消了static关键字，伴生对象是为了弥补kotlin没有static关键字修饰的静态成员的不足；
- 虽然伴生对象是为其所在对象模拟静态成员，但是伴生对象成员依然属于伴生对象本身的成员，而不属于其外部类的成员。


# 九.Kotlin的数据类
在类的声明前添加data关键字，即可将一个类定义成数据类。
```
data class <类名> <(主构造函数参数列表)> [:继承类和实现接口] [(/*类体*/)]
```
主构造函数的参数列表必须使用val或var声明为类属性，而且要求 **至少有一个**，否则无法通过编译。
```
data class User(val id:Int, val name:String)
```
数据类的特点:
- 自动声明与构造函数入参同名的属性字段。
- 自动实现每个属性字段的存取器方法set/get。
- 自动提供equals方法用于比较两个数据对象是否相等。
- 自动提供copy方法允许完整复制某个数据对象。
- 自动提供toString方法。

# 十.Kotlin的密封类
### 1.密封类的定义
就像用enum类型一样，经常需要在代码中声明一些有限集合，如: 网络请求可能为成功或失败需要先定义一个enum类型 网络请求状态NetStatus，再定义Loading、Success、Error这些网络请求状态。
枚举就是为了控制住你所有要的情况是正确的，而不是用硬编码方式写成字符串“Loading”，“Success”，“Error”。 同样的，密封类（sealed）的目的与enum类似，一个类之所以设计成sealed，就是为了限制类的继承结构，将一个值限制在有限集中的类型中，而不能有任何其他的类型。
密封类用来表示受限的类继承结构（规定了有限个类型，不可以存在其他类型）。是一种同时拥有枚举类 enum 和 普通类 class 特性的类。可以保证我们写出更安全的代码。
密封类与枚举类的区别:
**相同点 ( 类型限制 ) **: 从类型种类角度对比 , 类与枚举类类似 , 枚举类的值的集合是受限制的 , 不能随意扩展 ;
**不同点 ( 对象个数限制 ) **: 从每个类型对象个数对比 , 枚举类的每个类型只能存在一个实例 (每一个枚举值代表一个类的实例), 而密封类的每个类型可以创建无数个实例 ;

所以可以将密封类看做是枚举的拓展，基于枚举，高于枚举。枚举类型的每个值只允许有一个实例，同时枚举也无法为每个类型添加额外信息，例如，您无法为枚举中的 "Error" 添加相关的 Exception 类型数据。
而且不能控制对象的构建时机，当枚举类构建时 NetStatus 中的各种子类也必须构建好。 虽然也可以使用一个抽象类然后让一些类继承它，这样就可以随意扩展，但这会失去枚举所带来的有限集合的优势。
也可以说成，密封类是包含了一组受限的类集合，因为里面的类都是继承自这个密封类的。但是其和其他继承类（open）的区别在，密封类可以不被此文件外被继承，有效保护代码。
所以说密封类 则同时包含了前面两者的优势 —— 抽象类表示的灵活性和枚举里集合的受限性。
### 2.密封类的使用场景
- 禁止外部继承，对于一些只划分固定类型的数据，保证安全（作用类似于枚举）。
- when遍历密封类的子类时，不用加else语句。(主要解决了when结构需要添加一个默认的else分支的问题)
例如：新建一个 Result.kt
```
interface NetworkStatus
class Loading : NetworkStatus()
class Successed : NetworkStatus()

fun getResultMsg(result: NetworkStatus) = when(result) {
    is Loading -> {}
    is Successed -> {}
    else -> throw IllegalArgumentException()
}
```
这里定义了一个 NetworkStatus 接口，然后定义了两个类去实现 NetworkStatus 接口。然后再写一个 getResultMsg() 方法。实际上 Result 的执行结果只能是 Loading 或 Successed，所以里边的 else 永远无法走到，但我们不得不写上，只是为了满足 Kotlin 编译器的语法检查而已。

密封类就可以帮我们解决这个问题：
```
sealed class NetworkStatus
class Loading : NetworkStatus()
class Successed : NetworkStatus()

fun getResultMsg(result: NetworkStatus) = when(result) {
    is Loading -> {}
    is Successed -> {}
}
```
如果添加了一个新的分支，编译器就会发现有的地方发生了改变，编译器就会提醒处理。
例如:
```
sealed class NetworkStatus
class Loading : NetworkStatus()
class Successed : NetworkStatus()
class Error(val code: Int, val message: String) : NetworkStatus()

fun getResultMsg(result: NetworkStatus) = when(result) {
    is Loading -> {}
    is Successed -> {}
    is Error->{} //强制要求你将每一个子类所对应的条件全部处理,如果不进行处理编译器就会进行报错提醒
}
```


参考自：
[kotlin官方文档](https://www.kotlincn.net/docs/reference/constructing-collections.html)










