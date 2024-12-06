---
title: Kotlin总结之一变量常量及流程控制
date: 2019-06-20 
categories: 
  - Kotlin语言
---

# 一.Kotlin中的变量
###  1.var 与 val
- var 用此关键字声明的变量，可以多次重复赋值，``可读且可写``，相当于Java中普通变量。 
- val 用此关键字声明的变量表示只读变量，即``可读但不可写``。相当于Java中用final修饰的变量。
```
var str: String = ""    //str是变量名，String表明该变量是String类型变量，后面就是赋值语句。
var str2= ""            //省略了声明变量类型，它可以根据赋的值而自动推断出类型。
str="1234"              //var 声明的变量可以重新赋值。

val str3= " "           //val申明的变量不能够再次赋值
str3= "123456 "         //再次赋值会报错 
```
### 2.可空变量和不可空变量
定义变量时，可在类型后面加一个问号?，表示该变量是可为空的(初始化的时候不需要赋值)，不加表示该变量不可为null(初始化时必须要进行赋值)。
```
var s:String? = null   //通过?表示该变量是可为空
var s2:String = null   //如果该变量被赋值为null，则编译不能通过
s = "yyy"              //可空变量可以直接赋值
var length= s?.length  //如果s为null，则不执行length方法
var length= s!!.length //如果s为null，则会报错，终止程序执行
```
对于可以为null的变量，在使用该变量的时候，必须用变量名+?的形式进行调用，表示如果该变量为null，则不执行该变量调用的方法。如上表示当s为null时，不会执行length方法，从而避免了java中频繁的空指针异常。
**?和!!的区别**
?：表示当前对象是否可以为空，当对象为空时，不会执行后面的代码。
!!：通知编译器不做非空校验。如果运行时发现变量为空，就抛出异常。

### 3.变量后期初始化与延迟初始化
在一个Kotlin类中定义一个变量（属性）的时候是必须初始化的，否则就会编辑器就会报错。可是有的时候，并不想声明一个类型可空的对象，而且也没办法在对象一声明的时候就为它初始化，那么这时就需要用到Kotlin提供的延迟初始化。Kotlin中有两种延迟初始化的方式。一种是``lateinit var``，一种是``by lazy``。
##### (1.) lateinit var后期初始化
```
  private lateinit var txtView: TextView
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        txtView = findViewById(R.id.txt_main)
        setText()
    }
    fun setText() {
        txtView.text = "这是一段测试代码"
    }
```
**注意**
- lateinit var只能用来修饰类属性，不能用来修饰局部变量。
- 必须是可读且可写的变量，即用val声明的变量，不能声明于可空变量。
- 属性不能拥有自定义的setter与getter方法。
- 不能声明于基本数据类型变量(因为基本类型的属性在类加载后的准备阶段都会被初始化为默认值)。例：Int、Float、Double等，注意：String类型是可以的。
- lateinit的作用就是让编译期在检查时不要因为属性变量未被初始化而报错，所以声明后，在使用该变量前必须赋值，不然会抛出UninitializedPropertyAccessException异常。

##### (2.) by lazy变量延迟初始化
所谓延迟初始化即：指当程序在``第一次使用到这个变量（属性）的时候再初始化``。
```
//定义变量延迟初始化
 private val aTextView by lazy {
        findViewById<TextView>(R.id.txt_main)
    }

 override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        setText()
    }
 fun setText() {
        aTextView.text = "这是一段测试代码"
    }
```
- 使用lazy{}高阶函数，不能用于类型推断。且该函数在变量的数据类型后面，用by链接。
- 必须是只读变量，即用val声明的变量。
- by lazy可以使用于类属性或者局部变量。

那么既然是懒加载，就必然涉及到线程安全的问题，我们看看lazy是怎么解决的：
```
public actual fun <T> lazy(initializer: () -> T): Lazy<T> = SynchronizedLazyImpl(initializer)

public actual fun <T> lazy(mode: LazyThreadSafetyMode, initializer: () -> T): Lazy<T> =
    when (mode) {
        LazyThreadSafetyMode.SYNCHRONIZED -> SynchronizedLazyImpl(initializer)
        LazyThreadSafetyMode.PUBLICATION -> SafePublicationLazyImpl(initializer)
        LazyThreadSafetyMode.NONE -> UnsafeLazyImpl(initializer)
    }
    
public actual fun <T> lazy(lock: Any?, initializer: () -> T): Lazy<T> = SynchronizedLazyImpl(initializer, lock)    
```
可以看到这里是根据LazyThreadSafetyMode的字段来分别进行不同的操作。
LazyThreadSafetyMode是一个枚举类:
```
public enum class LazyThreadSafetyMode {

    SYNCHRONIZED,

    PUBLICATION,

    NONE,
}
```
- **SYNCHRONIZED** 通过加锁来确保只有一个线程可以初始化Lazy实例，是线程安全的。
- **PUBLICATION** 表示不加锁，可以并发访问多次调用，但只将第一个返回值用作[Lazy]实例的值。这也是线程安全的。
- **NONE** 不加锁，是线程不安全的， 如果从多个线程访问实例，可能会有多个实例。除非保证[Lazy]实例永远不会从多个线程初始化，否则不应使用此模式。
在使用by lazy进行初始化的时候的时候，如果不加mode参数的话，它会默认选择执行SynchronizedLazyImpl这个方法，也就是默认线程安全的。也可以通过添加mode参数来指定我们想要的懒加载效果。
```
private val aTextView by lazy( LazyThreadSafetyMode.SYNCHRONIZED) {
    findViewById<TextView>(R.id.txt.more)
}
```

延迟加载有几个好处。首先由于加载时机推迟到了变量被访问时，因此它可以提高应用的启动速度。相比于使用 Kotlin 开发服务端应用，这一特性对开发 Android 应用而言特别有用。其次，这样的延迟加载也有更高的内存效率，因为我们只在它被调用时才将资源加载进内存。在 Android 这样的移动平台上，内存的使用是非常重要的，因为手机资源是共享的且有限的。

# 二.Kotlin中的常量
### 1.val定义常量
在Kotlin中，一个var会默认对应生成两个方法，即getter和setter方法，比如:
```
var name: String? = null
```
打开Android studio 点击``Tools->Kotlin->Show Kotlin ByteCode``查看生成的字节码会包含如下的两个方法:
  ```
  @Nullable
   private String name;

   @Nullable
   public final String getName() {
      return this.name;
   }

   public final void setName(@Nullable String var1) {
      this.name = var1;
   }
```
而对于val来说只会生成一个对应的get方法，比如:
```
 val name: Long = "hello"
```
生成的字节码会包含类似这样的方法:
```
 @NotNull
 private static final String name = "hello";

 @NotNull
 public static final String getName() {
    return name;
 }
```
**val定义常量的坑**
在Kotlin中通过val定义的变量，只有get方法，没有set方法，所以只能读不能写。但是其get方法可以复写，从而造成val定义的变量，有可能会发生值变化，例如下面的例子：
```
 val A : Int 
    get()  {
        val rand = Random(System.currentTimeMillis())
        return rand.nextInt()
    }
```
val定义的常量A的get()方法被复写，每次调用常量A都会返回一个随机数，所以不能保证常量A的值不变。
### 2.Kotlin重如何才能生成真正的常量?
Kotlin重定义真正的常量的方法有两种，一种是``const``，另一个使用``@JvmField``注解。
### 3.使用const定义常量
在Kotlin中除了val关键字定义一个常量外，还提供了一个const关键字标识一个常量。const修饰的val变量相当于java中 static final是真正意义上的java常量，不过仅限于在top-level和object中。
```
//top-level中使用
const val THOUSAND = 1000 

//object中使用
object myObject {
    const val constNameObject: String = "constNameObject"
}
class MyClass {
    //object中
    companion object Factory {
        const val constNameCompanionObject: String = "constNameCompanionObject"
    }
}
```
- const 必须修饰val。
- const 只允许在top-level级别和object中声明。
- const val 可见性为public final static，可以直接访问。
### 3.使用@JvmField定义常量
在val常量前面增加一个@JvmField就可以将它变成常量。其内部作用是抑制编译器生成相应的getter方法。使用该注解修饰后则无法重写val的get方法。
```
@JvmField val NAME = "张三"
```
# 三.Kotlin中的数据类型
Kotlin数据类型 | Java基本数据类型 | Java包装类|
|-|-|-|
|Int| int |java.lang.Integer|
|Long| long |java.lang.Long|
|Float |float| java.lang.Float|
|Double |double |java.lang.Double|
|Short |short |java.lang.Short|
|Char |char |java.lang.Character|
|Byte |byte |java.lang.Byte|
|Boolean |boolean |java.lang.Boolean|

### 1.数字类型Number
- Float（32位）
- Double（64）
- Int（32）
- Byte（8）
- Short（16）
- Long(64，类型用大写L，如12L)
```
var b: Byte = 1
var s: Short = 1
var i: Int = 5
var l: Long = 1L
var f: Float = 1.555F
var d: Double = 1.555
```
***kotlin支持二进制、十进制、十六进制；注意: 不支持八进制(而java以0开头表示八进制 07)***

自 Kotlin 1.1 起，可以用下划线使数字更易读：   
```
val oneMillion = 1_000_000
val creditCardNumber = 1234_5678_9012_3456L
val socialSecurityNumber = 999_99_9999L
val hexBytes = 0xFF_EC_DE_5E
val bytes = 0b11010010_01101001_10010100_10010010
```
**装箱问题**
``在kotlin中的基本数据类型的看起来就是java的装箱类型，在这里我们需要注意，kotlin中已经没有装箱类型，区分装箱还是基本类型，kotlin已经交给了编译器去处理。``

**类型转换问题**
``java中可以将声明的int类型赋值给Long类型(java会自动拆箱装箱)即常说的隐式转换，但是kotlin并不可以，必须进行类型转换(显式转换)``
如(隐式转换):
```
val anInt: Int = 5
val aLong: Long = anInt
```
则无法编译通过，需改成(显示转换):
```
val anInt: Int = 5
val aLong: Long = anInt.toLong()
```
每个数字类型支持如下类型转换:
```
toByte(): Byte
toShort(): Short
toInt(): Int
toLong(): Long
toFloat(): Float
toDouble(): Double
toChar(): Char
```
**== 与 ===**
kotlin中并没有单纯的数值，在我们定义每一个数值的时候，kotlin编译器都在默默的为我们将定义的数值封装成一个对象，以最大限度的解决空指针异常的问题。因此kotlin中数值的比较除了我们常见的 == 号之外还多了 === 。

|java | kotlin | 说明 |
|-|-|-| 
|equal|==| [结构相等]比较两个具体的[数值的大小]是否相同|
|==	|=== | [引用相等]比较两个对象[在内存的存储地址]是否相同|
例如:
```
val a : Int = 10    //Kotlin并不会自动装箱
println(a === a)    //此处返回的值为true
val b : Int = a
println(a === b)    //此处返回的值为true
println(a == b)     //此处返回的值为true
```
### 2.布尔类型（Boolean）
** Boolean关键字表示布尔类型，并且其值有true和false**
```
var isNum: Boolean
isNum = false
println("isNum => $isNum")//输出结果为false
```
**逻辑操作符（与Java相同）**
- ' || ' => 逻辑或（或者）
- ' && ' => 逻辑与（并且）
- ' ! ' => 逻辑非（取反）
### 3.字符型（Char）
与java不同，kotlin中Char类型仅仅表示字符，不能再被直接当做数字。 因此，Char类型的变量必须在单引号之间表示：’变量’。
java代码如下：
```
char a = 'c';
System.out.println(a+1);
```
此时打印的结果为[数字]100。 
在kotlin中：
```
val a : Char = 'c'
println(a+1)
```
上述代码的打印结果为[字符]d

>因此我们要明确：Kotlin中 Char类型由于不是直接当数值用，所以最后返回依旧是Char型。
### 4.字符串
与java类似，kotlin中的String同样是由final修饰的，即不可被继承。
**字符串模版**
字符串可以包含字符串模板用来表示前面用的到的一段代码。kotlin中规定，所有的字符串模板必须以美元符号”$”开头。
```
val a = "temp"
val q = "$a.length():"
println(q+a.length)     //输出结果为temp.length():4
```
**用for循环迭代字符串.**
```
for (s in "12345"){println(s)}
```

# 四.Kotlin中的判断结构
### 1.if语句
1. 传统写法（同Java写法一样）
```
 var a: Int = 1
 var b: Int = 2
 var max: Int = 0
//基本用法
 if (a > b) {
   max = a
 } else {
   max = b
 }
 
```
2. 作为表达式使用。也就是说，整个 if 表达式(包括 else 部分)最终 会返回一个值，因此 if 可以代替 Java 中的三目运算符。（``Kotlin中没有java中的三元表达式``）
```
var age = 20
// 将 if 表达式赋值给 str 变量
var str = if (age > 20) "age大于20" 
    else if (age < 20) "age小于20" else "age等于20"
println(str)
```
``注意：Kotlin中没有java的中的2>1?2:1这样的三元表达式。``

# 五.Kotlin中的选择结构
### 1.when表达式
when 类似其他语言的 switch 操作符。 在 when 中，else 如同 switch 的 default。如果其他分支都不满足条件将会走else 分支，``如果很多分支需要用相同的方式处理，则可以把多个分支条件放在一起，用逗号分隔``。
```
 when (a) {
    1 -> print("x == 1")
    2 -> print("x == 2")
    3, 4 -> print("x == 3 or x == 4")
    in 5..9 -> print("x in [5..9]")
    !in 10..20 -> print("x is outside the range")
    else -> {
        print("x is else")
    }
  }
```
when也可以用来取代if-else-if链，如果不提供参数，所有的分支条件都是简单的布尔表达式，而当一个分支的条件为真时则执行该分支：
```
when {
    x.isOdd() -> print("x is odd")
    x.isEven() -> print("x is even")
    else -> print("x is funny")
}
```
# 六.Kotlin中的循环结构
### 1.for循环
```
val stringArrays : Array<String> = arrayOf("hello","kotlin","hello","android") //定义一个数组
for (item in stringArrays){
    println(item)
}
```
### 2.while 与 do...while 循环
while是最基本的循环:
```
while( 布尔表达式 ) {
  //循环内容
}
```
do…while 循环 对于 while 语句而言，如果不满足条件，则不能进入循环。但有时候我们需要即使不满足条件，也至少执行一次。
do…while 循环和 while 循环相似，不同的是，do…while 循环至少会执行一次。
```
do {
//代码语句
}while(布尔表达式);
```
# 七.Kotlin流程控制
- break:终止最直接包围它的循环，和java没啥区别。
- continue:继续下一次最直接包围它的循环，和java没啥区别。
- return:默认从最直接包围它的函数或者匿名函数返回。

### 1.使用break结束循环
需要在某种条件出现时强行中止循环，而不是等到循环条件为false时才退出循环，可以使用break来完成此功能。break用于完全结束一个循环，跳出循环体。
```
for (i in 0..10) {
    println("i的值是：${i}")
    if (i == 2) {
        //结束循环
        break
    }
}
```
输出结果：
```
i的值是：0
i的值是：1
i的值是：2
```
使用break语句不仅可以结束其所在的循环，还可以直接结束其外层循环。需要在break后紧跟一个标签，用于标识一个外层循环。Kotlin中的标签就是一个紧跟着@的标识符。Kotlin中的标签只有放在循环语句或switch语句之前才起作用:
```
//外层循环
outer@ for (i in 0..10) {
    for (j in 0 until 3) {
        println("i的值为：${i},j的值为：${j}")
        if (j == 1) {
            //跳出outer标签所标识的循环
            break@outer
        }
    }
}
```
输出结果：
```
i的值为：0,j的值为：0
i的值为：0,j的值为：1
```
>break后的标签必须是一个有效的标签，即这个标签必须在break语句所在的循环之前定义，或在其所在循环的外层循环之前定义。

### 2.continue关键字
continue和break有点类似，区别是：
- continue只是忽略本次循环的剩下语句，接着开始下一次循环，并不会中止循环；
- break则是完全中止循环本身。
```
for (i in 0 until 3) {
    println("i的值是${i}")
    if (i == 1) {
        //忽略本次循环的剩下语句
        continue
    }
    println("continue后的输出语句")
}
```
输出结果：
```
i的值是0
continue后的输出语句
i的值是1
i的值是2
continue后的输出语句
```
continue也可以紧跟一个标签，用于直接跳过标签所标识循环的档次循环剩下语句，重新开始下一次循环。
```
//外层循环
outer@ for (i in 0 until 5) {
    //内层循环
    for (j in 0 until 3) {
        println("i的值为：${i},j的值为：${j}")
        if (j == 1) {
            //忽略outer标签所指定的循环中档次循环剩下的语句
            continue@outer
        }
    }
}
```
输出结果：
```
i的值为：0,j的值为：0
i的值为：0,j的值为：1
i的值为：1,j的值为：0
i的值为：1,j的值为：1
i的值为：2,j的值为：0
i的值为：2,j的值为：1
i的值为：3,j的值为：0
i的值为：3,j的值为：1
i的值为：4,j的值为：0
i的值为：4,j的值为：1
```
### 3.使用return结束方法
return用于从最直接包围它的方法、函数或者匿名函数返回。 当函数或方法执行到一条return语句时，这个函数或方法将被结束。
```
fun main(args: Array<String>) {
    test()
}

fun test(){
   for (i in 0 until 10) {
       println("i的值是：${i}")
       if (i == 1) {
           return
       }
       println("return后的输出语句")
   }
}
```
输出结果：
```
i的值是：0
return后的输出语句
i的值是：1
```
>return并不是专门用于控制循环结构的关键字，但通过return语句确实可以结束一个循环。 与continue和break不同的是，return直接结束整个函数或方法，而不管return处于多少层循环之内。

参考自：
[kotlin官方文档](https://www.kotlincn.net/docs/reference/constructing-collections.html)