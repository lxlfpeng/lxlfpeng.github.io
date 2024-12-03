---
title: Kotlin总结之二数组和集合容器
date: 2019-07-09
categories: 
  - Kotlin
---

# 一 Kotlin中的数组
### 1.数组的类型
|kotlin | java|
|-|-|
|IntArray  |	int[]|
|ShortArray|	short[]|
|LongArray|	long[]|
|FloatArray|	float[]|
|DoubleArray|	double[]|
|CharArray|	char[]|

### 2.数组的创建
java创建数组的两种方式：
```
int[] intArray = new int[6]                //表达式：数据类型[]   标识  =   new  数据类型[长度];
String[] strArray = {"value0","value1"}    //表达式： 数据类型[]  标识  = {value0,value1,...}
```
在kotlin中有两种创建数组的方式:
- 使用arrayOf()、arrayOfNulls()、emptyArray()等工具函数；
- 使用Array(size:Int,init:(Int)->T)构造器；
```
//创建包含指定元素的数组（相当于Java数组的静态初始化）
var stringArr = arrayOf("kotlin", "php", "python", "c")
var intArr = arrayOf(1, 24, 20, -3)

//创建指定长度、元素为null的数组（相当于Java数组的动态初始化）
var arr2 = arrayOfNulls<Double>(9)
var intArr2 = arrayOfNulls<Int>(3)

//创建长度为0的空数组
var arr3 = emptyArray<String>()
var intArr3 = emptyArray<Int>()

//创建指定长度、使用Lambda表达式初始化数组元素的数组
var strArr4=Array(6,{"kotlin"})
```

### 3.访问数组的元素
[] 可以用于访问数组的元素，实际上 [] 被进行了操作符的重载，调用的是 Array 类的 setter 和 getter 方法:
```
val arr = arrayOf(1, 2, 3)
arr[1]           //结果:1
arr.get(1)       //结果:1
// arr[10]       //报错ArrayIndexOutOfBoundsException
```
>[] 虽然调用的是 setter 和 getter 方法，但是编译成字节码时会被进行优化，变成直接访问数组的内存地址，所以不会造成性能损失。

### 4.修改数组元素
```
val intArr = intArrayOf(1,2,3)
intArr[1] = 0           //与java一样，可以这样修改数据
intArr.set(2,1)         //kotlin可以通过set函数进行修改数据
```

### 5.遍历数组元素
```
val intArr = intArrayOf(1,2,3)
for(item in intArr){
    println(item)                   //遍历intArr里面的元素，item就是元素本身
}
for (index in intArr.indices){
    println(intArr[index])          //遍历initArr索引的元素，从0开始
    println(intArr.get(index))      //可以通过get(索引)来获取元素
}
```
# 二.集合
### 1.只读集合和可变集合
Kotlin将集合分为``只读集合``和``可变集合``。
![](/images/2ab9b95b7bfb5df651b3ead4a7785dec.webp)
-  **只读集合:**源自最基础的集合接口：kotlin.collections.Collection。该接口可以对集合进行一些基本操作，但无任何添加和移除元素的方法。
-  **可变集合:**实现 kotlin.collections.MutableCollection 接口才可以修改集合的数据。MutableCollection 接口继承自 Collection，并提供添加、移除和清空集合元素的方法。
>可变集合一般都带有 “Mutable” 前缀修饰，意味着能对集合中的元素进行修改。

Kotlin 标准库提供了基本集合类型的实现：`` set、list 以及 map``。

### 2.集合的创建
|集合类型|只读集合|可变集合|
|-|-|-|
|List |listOf|mutableList、arrayListOf|
|Set|setOf	| mutableSetOf、hashSetOf、linkedSetOf、sortedSetOf|
|Map	|mapOf	| mutableMapOf、hashMapOf、linkeMapOf、sortedMapOf|

>集合类存放的都是对象的引用，而非对象本身，通常说的集合中的对象指的是集合中对象的引用。

##### (1.)只读集合的创建
```
val emptyList = listOf<Int>()       //创建空的list集合
val emptySet = setOf<Int>()         //创建空的set集合 
val emptyMap = mapOf<Int,Int>()     //创建空的map集合

val list1 = listOf("kotlin","java") //该函数返回不可变的List集合。该函数可接受0个或多个参数，这些参数将作为集合的元素。
val set2 = setOf("kotlin","java")   //该函数返回不可变的Set集合。该函数可以接受0个或多个参数，这些参数将作为集合的元素。
val map2 = mapOf("key" to "value")  //该函数返回不可变的Map集合。该函数可接受0个或多个key-value对，这些key-value对将作为Map的元素。
    
```
##### (2.)可变集合的创建
```
val emptyMutableList = mutableListOf<Int>()     //创建空的list集合
val emptyMutableSet = mutableSetOf<Int>()       //创建空的set集合
val emptyMutableMap = mutableMapOf<Int,Int>()   //创建空的map集合

val initMutableList = mutableListOf(1)          //该函数返回可变的MutableList集合。该函数可接受0个或多个参数，这些参数将作为集合的元素。
val initMutableSet = mutableSetOf(2)            //该函数返回可变的MutableSet集合。该函数可接受0个或多个参数，这些参数将作为集合的元素。
val initMutableMap = mutableMapOf(1 to 1)       //该函数返回可变的MutableMap集合。该函数可接受0个或多个key-value对，这些key-value对将作为Map的元素。
```
### 3.Set集合
##### (1.)Set集合的创建
- setOf()：该函数返回不可变的Set集合。该函数可以接受0个或多个参数，这些参数将作为集合的元素。
- mutableSetOf()：该函数返回可变的MutableSet集合。该函数可接受0个或多个参数，这些参数将作为集合的元素。
- hashSetOf()：该函数返回可变的HashSet集合。该函数可接受0个或多个参数，这些参数将作为集合的元素。
- linkedSetOf()：该函数返回可变的LinkedHashSet集合。该函数可接受0个或多个参数，这些参数将作为集合的元素。
- sortedSetOf()：该函数返回可变的TreeSet集合。该函数可接受0个或多个参数，这些参数将作为集合的元素。

##### (2.)Set集合的操作
```
//创建不可变集合，返回值是Set
var set = setOf("Java", "Kotlin", "Go")
//判断是否所有元素的长度都大于4
println(set.all { it.length > 4 })
//判断是否任一元素的长豆都大于4
println(set.any { it.length > 4 })
//以Lambda表达式的值为key，集合元素为value，组成Map集合
val map = set.associateBy { "学习" + it + "语言" }
println(map)

println("Java" in set)
println("Go" !in set)

//返回删除Set集合前面两个元素后的集合
val dropedList = set.drop(2)
println(dropedList)

//对Set集合元素进行过滤：要求集合元素包含li
val fliteredList = set.filter { "li" in it }
println(fliteredList)

//查找Set集合中包含li的元素，如果找到就返回该元素，否则就返回null
val foundStr1 = set.find { "li" in it }
println(foundStr1)

//查找Set集合中的所有字符串拼接在一起
val foldedList = set.fold("", { acc, e -> acc + e })
println(foldedList)

//查找某个元素的出现位置
println(set.indexOf("Go"))

//将每个集合元素映射成新值，返回所有新值组成的Set集合
val mappedList = set.map { "学习" + it + "编程" }
println(mappedList)

//获取最大值
println(set.max())

//获取最小值
println(set.min())

//反转集合顺序
val reversedList = set.reversed()
println(reversedList)

val bSet = setOf("Lua", "Erlang", "Kotlin")
//计算两个集合的交集
println(set intersect bSet)
//计算两个集合的并集
println(set union bSet)
//集合相加，相当于并集
println(set + bSet)
//集合相减，减去公共的元素
println(set - bSet)
```
输出结果：
```
false
true
{学习Java语言=Java, 学习Kotlin语言=Kotlin, 学习Go语言=Go}
true
false
[Go]
[Kotlin]
Kotlin
JavaKotlinGo
2
[学习Java编程, 学习Kotlin编程, 学习Go编程]
Kotlin
Go
[Go, Kotlin, Java]
[Kotlin]
[Java, Kotlin, Go, Lua, Erlang]
[Java, Kotlin, Go, Lua, Erlang]
[Java, Go]
Kotlin规定以infix修饰的方法，能以运算符的方式进行调用。
```

##### (3.)遍历Set集合
Kotlin也支持使用for-in循环遍历Set，与遍历数组的方式基本相同:
```
    var languages = setOf("Java", "Kotlin", "Python")
    for (language in languages) {
        println(language)
    }
```
输出结果：
```
Java
Kotlin
Python
```
Set集合可使用接口中定义的forEach()方法来遍历集合:
```
    var languages = setOf("Java", "Kotlin", "Python")
    languages.forEach { println(it) }
```
输出结果：
```
Java
Kotlin
Python
```
由于setOf()方法返回的Set集合是有序的，所以可以通过索引来遍历Set集合，Set集合提供了indices方法返回其索引的区间:
```
    var languages = setOf("Java", "Kotlin", "Python")
    for (i in languages.indices) {
        println(languages.elementAt(i))
    }
```
输出结果：
```
Java
Kotlin
Python
```

##### (4.)可变Set集合
setOf()函数返回的额集合是不可变集合；使用mutableSetof()、hashSetOf()、linkedSetOf()、sortedSetOf()函数返回的集合都是可变的。可变Set集合除了set集合常见的操作还支持其他的操作；
**集合添加元素**
Set提供了add(element:E)方法来添加元素，每调用该方法一次，就会向Set中添加一个元素，Set的长度也会自动加1。也提供了addAll(elements:Collection<E>)方法来批量添加多个元素。
```
//定义一个可变的Set
var languages = mutableSetOf("Java")
//添加一个元素
languages.add("Go")
languages.add("Lua")
println(languages)
println(languages.count())
languages.addAll(setOf("Swift", "Kotlin"))
println(languages)
```
输出结果：
```
[Java, Go, Lua]
3
[Java, Go, Lua, Swift, Kotlin]
```
**集合删除元素**
Set提供了如下方法来删除元素：
- remove(element:E)：删除指定元素，删除成功则返回true。
- removeAll(elements:Collection<E>)：批量删除Set集合中的多个元素。
- retainAll(elements:Collection<E>)：只保留Set集合中与elements集合共有的元素。
- clear()：清空集合。
```
var languages = mutableSetOf("Java", "OC", "PHP", "Perl", "Ruby", "Go") //定义一个可变的Set
languages.remove("PHP")                                                 //删除"PHP"
languages.remove("Perl")                                                //再次删除"Perl"
println(languages)
languages.removeAll(setOf("Ruby", "Go"))                                //批量删除多个元素
println(languages)
languages.clear()                                                       //清空Set集合
println(languages.count())
```
输出结果：
```
[Java, OC, Ruby, Go]
[Java, OC]
0
```
>Kotlin的MutableIterator才相当于Java的Iterator。
### 5.List集合
##### (1.)List集合的创建
- listOf()：该函数返回不可变的List集合。该函数可接受0个或多个参数，这些参数将作为集合的元素。
- listOfNotNull()：该函数返回不可变的List集合。该函数与前一个函数的唯一区别是,该函数会自动去掉传入的一系列参数中的null值。
- mutableListOf()：该函数返回可变的MutableList集合。该函数可接受0个或多个参数，这些参数将作为集合的元素。
- arrayListOf()：该函数返回可变的ArrayList集合。该函数可接受0个或多个参数，这些参数将作为集合的元素。

##### (2.)List集合的方法
List除了支持Set所支持的操作外，还增加了通过索引操作集合元素的方法。
- get：带operator修饰的方法，因此可用"[]"运算符访问集合元素。
- indexOf：返回集合元素在List中的索引。
- lastIndexOf：返回集合元素在List中最后一次的出现位置。
- subList：返回List集合的子集合。
```
var list1 = listOf("Java", "Kotlin", null, "Go")  //创建不可变集合，返回值是List
for (i in list1.indices) {
    println(list1[i])
}
println(list1.indexOf("Kotlin"))                 //获取指定元素的出现位置
println(list1.subList(1, 3))                     //获取List的子集合
```
输出结果：
```
Java
Kotlin
null
Go
1
[Kotlin, null]
```

##### (3.)可变List集合的方法
可变的List除了支持可变的Set所支持的方法外，还增加了根据索引执行插入、删除、替换的方法。
```
var list1 = mutableListOf("Java", "Kotlin", null, "Go") //创建不可变集合，返回值是List
list1.add(2, "Java")                                    //在索引2处插入一个新元素
println(list1)
list1.removeAt(1)                                       //删除索引1处的元素
println(list1)
list1[1] = "Python"                                     //将索引1处的元素替换为"Python"
println(list1)
list1.clear()                                           //清空List集合的所有元素
println(list1.count())
```
输出结果：
```
[Java, Kotlin, Java, null, Go]
[Java, Java, null, Go]
[Java, Python, null, Go]
0
```
### 6.Map集合
##### (1.)Map集合的创建
- mapOf()：该函数返回不可变的Map集合。该函数可接受0个或多个key-value对，这些key-value对将作为Map的元素。
- mutableMapOf()：该函数返回可变的MutableMap集合。该函数可接受0个或多个key-value对，这些key-value对将作为Map的元素。
- hashMapOf()：该函数返回可变的HashMap集合。该函数可接受0个或多个key-value对，这些key-value对将作为Map的元素。
- linkedMapOf()：该函数返回可变的LinkedHashMap集合。该函数可接受0个或多个key-value对，这些key-value对将作为Map的元素。
- sortedMapOf()：该函数返回可变的TreeMap集合。该函数可接受0个或多个key-value对，这些key-value对将作为Map的元素。

##### (2.)Map集合的操作
```
var map = mapOf("Java" to 86, "Kotlin" to 92, "Go" to 78)//创建不可变集合，返回值是Map
println(map.all { it.key.length > 4 && it.value > 80 })//判断是否所有key-value对的key的长度都大于4，value都大于80
println(map.any { it.key.length > 4 && it.value > 80 })//判断是否任一key-value对的key的长豆都大于4、value都大于80
println("Java" in map)
println("Go" !in map)
val filteredMap = map.filter { "li" in it.key }//对Map集合元素进行过滤：要求key包含li
println(filteredMap)
val mappedList = map.map { "${it.key}有${it.value}节课" }//将每个key-value对映射成新值，返回所有新值组成的Map集合
println(mappedList)
println(map.maxBy { it.key })//根据key获取最大值
println(map.minBy { it.value })//根据value获取最小值
var bMap= mapOf("Lua" to 67,"Erlang" to 73,"Kotlin" to 92)
println(map+bMap)//求并集
println(map-bMap)//集合相减
```
输出结果：
```
false
true
true
false
{Kotlin=92}
[Java有86节课, Kotlin有92节课, Go有78节课]
Kotlin=92
Go=78
{Java=86, Kotlin=92, Go=78, Lua=67, Erlang=73}
{Java=86, Kotlin=92, Go=78}
```

##### (3.)Map集合的遍历
Map集合由多个key-value对组成，因此遍历Map集合时既可以通过对key-value对进行遍历，也可先遍历key，再通过key来获取对应的value进行遍历。
下面是对Map集合遍历的几种方式：
```
var map = mapOf("Java" to 86, "Kotlin" to 92, "Go" to 76)//创建不可变集合，返回值是Map
//遍历Map的key-value对，entris元素返回key-value对组成的Set
for (en in map.entries) {
    println("${en.key}->${en.value}")
}
//先遍历Map的key，再通过key获取value
for (key in map.keys) {
    println("${key}->${map[key]}")
}
//直接用for-in循环遍历Map
for ((key, value) in map) {
    println("${key}->${value}")
}
map.forEach({ println("${it.key}->${it.value}") })//用Lambda表达式遍历Map
```
输出结果：
```
Java->86
Kotlin->92
Go->76

Java->86
Kotlin->92
Go->76

Java->86
Kotlin->92
Go->76

Java->86
Kotlin->92
Go->76
```

##### (4.)可变的Map集合操作
可变的Map为操作key-value对提供了如下方法：
- clear()：清空所有的key-value对。
- put(key:K,value:V)：放入key-value对。如果原来已有key，value将被覆盖。
- putAll(form:Map<out K,V>)：批量放入多个key-value对。
- remove(key:K)：删除key-value对。
```
var mutableMap = mutableMapOf("OC" to 96, "PHP" to 3400, "Perl" to 4300, "Ruby" to 5600, "Go" to 5600)
mutableMap["Swift"] = 9000//以方括号语法放入key-value对
println(mutableMap)
mutableMap.put("OC", 8600)//以put方法放入key-value对
println(mutableMap)
mutableMap.remove("PHP")//删除key为"PHP"的key-value对
println(mutableMap)
println(mutableMap.size)
mutableMap.clear()//删除所有元素
println(mutableMap)
println(mutableMap.size)
```
输出结果：
```
{OC=96, PHP=3400, Perl=4300, Ruby=5600, Go=5600, Swift=9000}
{OC=8600, PHP=3400, Perl=4300, Ruby=5600, Go=5600, Swift=9000}
{OC=8600, Perl=4300, Ruby=5600, Go=5600, Swift=9000}
5
{}
0
```

参考自：
[kotlin官方文档](https://www.kotlincn.net/docs/reference/constructing-collections.html)

