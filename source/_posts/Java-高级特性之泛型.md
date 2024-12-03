---
title: Java-高级特性之泛型
date: 2016-11-12
categories: 
  - Java开发
---

# 一. Java 中的泛型
Java 5 中添加了泛型，用以**编译时类型检查**，借此消除使用集合类时常见的ClassCastException风险。
```
List list = new ArrayList();
list.add("abc");
list.add(1); 
for(Object obj : list){
    String str=(String) obj; 
}
```
上面的代码可以很好地编译，但是在运行时会引发ClassCastException，因为我们试图将集合中的对象强制转换为String，而其中一个元素是Integer类型。使用泛型之后:
```
List<String> list1 = new ArrayList<String>(); 
list1.add("abc");
//list1.add(1); //编译时期就会发生报错
for(String str : list1){
     //不需要类型转换, 避免了ClassCastException
}
```
在创建集合时，已指定集合中元素的类型为String。因此，如果在列表中添加任何其他类型的对象，则该程序将引发编译时错误。另外，在循环中，我们不需要对集合中元素进行类型转换，因此在运行时避免了ClassCastException。


# 二. 泛型类
##### 语法
泛型类（generic class）就是具有一个或多个类型变量的类。
```
泛型类的语法形式：
class name<T1, T2, ..., Tn> {
   /* ... */ 
 }
```
##### 单泛型类
一个类型变量的泛型类：
```
public class Generic<T> {
    /* key这个成员变量的类型为T,T的类型由外部指定 */
    private T key;
    /* 泛型构造方法形参key的类型也为T,T的类型由外部指定 */
    public Generic(T key) {
        this.key = key;
    }
    /* 泛型方法getKey的返回值类型为T,T的类型由外部指定 */
    public T getKey() {
        return key;
    }
}
```
定义的泛型类，并不以一定非得传入泛型类型实参！
如果在使用泛型的时候传入泛型实参，则会根据传入的泛型实参做出限制。
如果没有传入泛型实参，在泛型类中用泛型的方法或成员变量定义的类型可以为任何类型。
```
Generic generic1 = new Generic(666666);
Generic generic2 = new Generic("666666");
Generic generic3 = new Generic(666666L);
Generic generic4 = new Generic(true);
```
##### 多泛型类
多个类型变量的泛型类：
```
//两个类型变量的泛型
class Test<K, V>{
    private K key;
    private V value;
  
    Test(K key, V value){
        this.key = key;
        this.value = value;
    }
    
    public K getKey(){
        return key;
    }
    public V getValue(){
        return value;
    }
}
public class TestDemo{
     public static void main(String []args){
         Test<String,Integer> pair1 = new Test<String,Integer>("zhangsan",1);
         Test<String,Integer> pair2 = new Test<String,Integer>("lisi",2);
         System.out.println(pair1.getKey() + "=" + pair1.getValue() );//输出zhangsan=1
         System.out.println(pair2.getKey() + "=" + pair2.getValue() ); //输出lisi=2
     }
}
```
##### 泛型类派生子类
父类派生子类的时候不能在包含类型形参，需要传入具体的类型

错误的方式：
 ```
 public class A extends Test<K, V> {}
```
正确的方式：
```
public class A extends Test<Integer, String> {}
```
也可以不指定具体的类型，系统就会把K,V形参当成Object类型处理
```
public class A extends Test{}
```
# 二. 泛型接口
接口也可以声明泛型。
泛型接口语法形式：
```
public interface GenericIntercace<T> {
     T getData();
}
```
泛型接口有两种实现方式：
1. 实现泛型接口方式一：
```
/**
 * 未传入泛型实参时，与泛型类的定义相同，在声明类的时候，需将泛型的声明也一起加到类中。
 * 如果不声明泛型， 编译器会报错。
 */
public class ImplGenericInterface1<T> implements GenericIntercace<T> {
    private T data;

    private void setData(T data) {
        this.data = data;
    }

    @Override
    public T getData() {
        return data;
    }

    public static void main(String[] args) {
        ImplGenericInterface1<String> implGenericInterface1 = new ImplGenericInterface1<>();
        implGenericInterface1.setData("测试1");
        System.out.println(implGenericInterface1.getData());//输出测试1
    }
}
```
2. 实现泛型接口方式二：
```
public class ImplGenericInterface2 implements GenericIntercace<String> {
    @Override
    public String getData() {
        return "test2";
    }

    public static void main(String[] args) {
        ImplGenericInterface2 implGenericInterface2 = new ImplGenericInterface2();
        System.out.println(implGenericInterface2.getData());//输出测试2
    }
}
```
# 三. 泛型方法
泛型方法可以定义在普通类和泛型类中，比如泛型类更为常用，一般能用泛型方法解决的问题优先使用泛型方法而不使用泛型类。
```
public class Generic {
    //先定义泛型方法
    public <T> void show(T t) {
        System.out.println(t);
    }
}
```
测试代码：
用户传递进来的是什么类型，返回值就是什么类型了
```
    public static void main(String[] args) {
        //创建对象
        Generic generic= new Generic();
        //调用方法,传入的参数是什么类型,返回值就是什么类型
        generic.show("hello");
        generic.show(12);
        generic.show(12.5);
    }
```
泛型方法，是在调用方法的时候指明泛型的具体类型 ，泛型方法可以在任何地方和任何场景中使用，包括普通类和泛型类。注意泛型类中定义的普通方法和泛型方法的区别。
![](/images/80a77f7e564ba048902440d594735b60.webp)
区别一下普通的方法和泛型方法
![](/images/022c37159bb44fd95be19b57439407c0.webp)
可以看到普通方法中也使用了泛型，但是它只是一个普通的方法，只是它的返回值和传入的类型是在前面已经声明过得泛型，所以，这里才可以继续使用 T 这个类型变量。``仅仅使用了泛型变量并不算是泛型方法``。
而下面这个泛型方法，首先通过 <E> 标识了它是一个泛型方法，返回值类型和传入的类型一致，通过泛型进行参数化了。

>前面已经介绍了泛型类了，在类上定义的泛型，在方法中也可以使用。现在可能就仅仅在某一个方法上需要使用泛型。外界仅仅是关心该方法，不关心类其他的属性。这样的话，我们在整个类上定义泛型，未免就有些大题小作了。所以，一般能用泛型方法解决的问题优先使用泛型方法而不使用泛型类。

例如我们编写一个单一的排序方法来对int，String数组或任何支持排序的数组的中元素进行排序：
```
public class Point {
    //对数组进行排序
    public <E> E[] printArray(E[] inputArray) {
        //TODO 进行排序操作
        return inputArray;
    }
}

Integer[] intArray = {1, 2, 3, 4, 5};
Double[] doubleArray = {1.1, 2.2, 3.3, 4.4};
Character[] charArray = {'P', 'I', 'Z', 'Z', 'A'};

Point point = new Point();
//获取排序数组的值
point.printArray(intArray);
point.printArray(doubleArray);
point.printArray(charArray);
```
# 四. 泛型变量的类型限定
到目前为止，只看到了无界限的泛型类型参数。无界意味着我们的``泛型类型参数可以是我们想要的任何类型``。但是有的时候我们又可能希望限制允许传递给参数的类型。例如，对数字进行操作的方法可能只希望接受Number类或其子类的实例。有界类型参数用于此目的。要声明一个有界的类型参数，请列出该类型参数的名称，然后是extends关键字，然后是其上限。实质上类型限定就是使用extends关键字对类型变量加以约束。比如限定泛型参数只接受Number类或者子类Integer、Float等，可以这样限定<T extends Number>，这样限定之后，实际参数只能是Number类或者Number的子类。
```
//定义泛型类Box，并限定类型参数为Fruit
public class Box<T extends Fruit> {}

//由于Box限定了类型参数，实际类型参数只能是Fruit或者Fruit的子类
Box<Fruit> integerBox = new Box<Fruit>();//编译通过
Box<Apple> integerBox = new Box<Apple>();//编译通过
Box<Integer> integerBox = new Box<Integer>();//编译器报错
```
通过限定，箱子Box就只能装水果了。
- 不管限定是类还是接口，统一都使用extends关键字
- 可以使用&符号给出多个限定，例如：``<T extends Fruit & MyInterface1 & MyInterface2>``
多个限制只能有一个类名，其他都是接口名，且类名在最前面。

在类型参数中使用 extends 表示这个泛型中的参数必须是 T 或者T 的子类，这样有两个好处：

- 如果传入的类型不是 T 或者 T 的子类，编译不成功。
- 泛型中可以使用 T 的方法，要不然还得强转成 T 才能使用。
```
private <T extends A, E extends B> E test(K arg1, E arg2){
    E result = arg2;
    arg2.compareTo(arg1);
    //.....
    return result;
}
```
类型参数列表中如果有多个类型参数上限，用逗号分开。

# 五. 泛型通配符
##### 类型通配符
在定义泛型类，泛型方法，泛型接口的时候经常会碰见很多不同的通配符，比如 T，E，K，V 等等，这些通配符又都是什么意思呢？
常用的 ``T，E，K，V，？``
本质上这些个都是通配符，没啥区别，只不过是编码时的一种约定俗成的东西。比如上述代码中的 T ，我们可以换成 A-Z 之间的任何一个 字母都可以，并不会影响程序的正常运行，但是如果换成其他的字母代替 T ，在可读性上可能会弱一些。通常情况下，T，E，K，V，？ 是这样约定的：
|  类型   | 说明  |
|  ----  | ----  |
| T (type)  | 表示具体的一个java类型，T代表在调用时的指定类型，会进行类型推断。 |
|K V (key value) |分别代表java键值中的Key Value|
|E (element) |代表Element(在集合中使用，因为集合中存放的是元素)|
|N|N - Number（数值类型）|


##### 协变
数组的协变
```
class Fruit {}
class Apple extends Fruit {}
class RedApple extends Apple {}
class Orange extends Fruit {}

public class Test{
  public static void main(String[] args) {
        Fruit[] fruits = new Apple[3];
        fruits[0] = new Apple();  // OK
        fruits[1] = new RedApple(); // OK
        fruits[2] = new Orange();//error ArrayStoreException
        fruits[3] = new Fruit();//error ArrayStoreException
    }
} 
```
我们首先创建了一个 Apple 数组并把它赋给 Fruit 数组的引用。Apple 是 Fruit 的子类，一个 Apple 对象也是一种 Fruit 对象，所以一个 Apple 数组也是一种 Fruit 的数组。这被称作数组的协变，Java 把数组设计为协变的，对此是有争议的，有人认为这是一种缺陷。

尽管 Apple[] 可以 “向上转型” 为 Fruit[]，但数组元素的实际类型还是 Apple，只能向数组中放入 Apple或者 Apple 的子类。在上面的代码中，向数组中放入了 Fruit 对象和 Orange 对象。对于编译器来说，这是可以通过编译的，但是在运行时期，JVM 能够知道数组的实际类型是 Apple[]，所以当其它对象加入数组的时候就会抛出异常。
当我们使用泛型容器来替代数组时，看看会发生什么。
```
 public static void main(String[] args) {
      List<Fruit> flist = new ArrayList<Apple>(); // 编译错误
  }
```
直接在编译时报错了。与数组不同，泛型没有**内建的协变类型**。这是因为数组在语言中是完全定义的，因此内建了编译期和运行时的检查，但是在使用泛型时，类型信息在编译期被擦除了，运行时也就无从检查。因此，泛型将这种错误检测移入到编译期。泛型是不变的。
再来看一个例子:
```
Fruit f = new Apple(); //OK 多态
Fruit[] farray = new Apple[10];//OK 数组协变
ArrayList<Fruit> flist = new ArrayList<Apple>();//编译不通过
```
第一行的写法是很常见的，父类引用指向子类对象，这是java多态的表现。第二行父类数组的引用指向子类数组对象在java中也是可以的，这称为数组的协变。上面提到过。由此可知，协变的缺陷在于可能的异常发生在运行期，而编译期间无法检查，泛型设计的目的之一就是避免这种问题，所以泛型是不支持协变的，也就是说，上面的第三行代码是编译不通过的。但是，有时候是需要建立这种“向上转型”的关系，Java泛型是不变（不能协变）的。这时就需要使用通配符来解决，通配符<?>，用来表示某种特定的类型，但是不知道这个类型到底是什么。通配符包括以下几种：``上界通配符、下界通配符、无限定通配符``。
##### 无边界通配符 ？
首先我们定义A、B、C、D四个类，他们的关系如下
```
class A {}
class B extends A {}
class C extends B {}
class D extends C {}
```
通配符？意义就是它是一个未知的符号，可以是代表任意的类。
```
//我们发现，这样写编译不通过，原因很简单，泛型不匹配，虽然B继承A
List<A> listA = new ArrayList<B>(); 

//以下5行代码均编译通过
List<?> list;
list = new ArrayList<A>();
list = new ArrayList<B>();
list = new ArrayList<C>();
list = new ArrayList<D>();

Object o = list.get(0); //编译通过
list.add(new A());      //编译不通过
list.add(new B());      //编译不通过
list.add(new C());      //编译不通过
list.add(new D());      //编译不通过
```
?是定义在引用变量上，T是类上或方法上。
通配符可以使用extends和super关键字来限制边界：
- List<? extends Number> 表示不确定参数类型，但必须是Number类型或者Number子类类型，这是上边界限定。
- List<? super Number> 表示不确定参数类型，但必须是Number类型或者Number的父类类型，这是下边界限定。
- List<?> 表示未受限的通配符，相当于 List<? extends Object>。

>注意上面我们提到泛型变量的类型限定， 它看起来有点像是通配符的边界限定，那他们之间有什么区别吗？主要有以下三点：
- 泛型变量的类型限定，是在定义泛型类的时候对声明的泛型参数进行限定（限定的是形式参数）
public class Box<T extends Fruit>{}
- 通配符的边界限定，是在定义化泛型类的引用的时候对实际泛型参数进行限定（限定的是实际参数）
List<? extends Fruit> listInteger =new ArrayList<Apple>();
- 泛型变量的类型限定只能使用extends关键字，通配符的边界限定可以使用extends或super来限定上边界或下边界。


##### 上界通配符 < ? extends E>
上界通配符：用 extends 关键字声明，表示参数化的类型是E或者是E的子类。

上界通配符用于放宽对变量类型的限制。例如，假设我们只知道集合里面的元素是Number，但是不知道具体是整数还是双精度类型。那么我们如何获得该列表中元素的总和？我们可以使用上限通配符来解决此问题。如下:
```
    public void method(List<? extends Number> list) {
        double sum = 0;
        for (Number i : list) {
            sum += i.doubleValue();
        }
        System.out.println(sum);
    }
    public static void main(String[] args) {
        Integer[] intArray = {1, 2, 3, 4, 5};
        Double[] doubleArray = {1.1, 2.2, 3.3, 4.4};

        List<Integer> integersList = Arrays.asList(intArray);
        List<Double> doublesList = Arrays.asList(doubleArray);

        Point point = new Point();
        point.method(integersList);
        point.method(doublesList);
    }
```
上界的list只能get，不能add（确切地说不能add出除null之外的对象，包括Object）。
```
       List<? extends Fruit> flistTop = new ArrayList<Apple>();
       flistTop.add(null);//OK
       flistTop.add(new Object());//报错
       flistTop.add(new Apple());//报错
       flistTop.add(new Fruit());//报错
       Fruit fruit1 = flistTop.get(0);//可以取值
```
上界 <? extend Fruit> ，表示所有继承Fruit的子类，但是具体是哪个子类，无法确定，所以调用add的时候，要add什么类型，谁也不知道。但是get的时候，不管是什么子类，不管追溯多少辈，肯定有个父类是Fruit，所以，我都可以用最大的父类Fruit接着，也就是把所有的子类向上转型为Fruit。

##### 下界通配符 < ? super E>
下界通配符: 用 super 进行声明，表示参数化的类型可能是所指定的类型，或者是此类型的父类型，直至 Object在类型参数中使用 super 表示这个泛型中的参数必须是 E 或者 E 的父类。
```
        List<? super RedApple> flistBottem = new ArrayList<RedApple>(); //  本身
        List<? super RedApple> flistBottem = new ArrayList<Apple>(); //  直接父类
        List<? super RedApple> flistBottem = new ArrayList<Fruit>(); //  间接父类
        flistBottem.add(new RedApple());
        //get Apple对象会报错
        //RedApple apple = flistBottem.get(0);
```


下界 <? super RedApple>，表示RedApple的所有父类，包括Fruit，一直可以追溯到老祖宗Object 。那么当我add的时候，我不能add RedApple的父类，因为不能确定List里面存放的到底是哪个父类。但是我可以add RedApple及其子类。因为不管我的子类是什么类型，它都可以向上转型为RedApple及其所有的父类甚至转型为Object 。但是当我get的时候，RedApple的父类这么多，我用什么接着呢，除了Object，其他的都接不住。


**Java 的泛型本身是不支持协变和逆变的。**

- 可以使用泛型通配符 ? extends 来使泛型支持协变，但是「只能读取不能修改」，这里的修改仅指对泛型集合添加元素，如果是 remove(int index) 以及 clear 当然是可以的。
- 可以使用泛型通配符 ? super 来使泛型支持逆变，但是「只能修改不能读取」，这里说的不能读取是指不能按照泛型类型读取，你如果按照 Object 读出来再强转当然也是可以的。

# 五. 泛型擦除
Java的泛型是伪泛型，这是因为Java在编译期间，所有的泛型信息都会被擦掉。Java的泛型基本上都是在编译器这个层次上实现的，在生成的字节码中是不包含泛型中的类型信息的，使用泛型的时候加上类型参数，在编译器编译的时候会去掉，这个过程成为类型擦除。

如在代码中定义List<Object>和List<String>等类型，在编译后都会变成List，JVM看到的只是List，而由泛型附加的类型信息对JVM是看不到的。Java编译器会在编译时尽可能的发现可能出错的地方，但是仍然无法在运行时刻出现的类型转换异常的情况，类型擦除也是Java的泛型与C++模板机制实现方式之间的重要区别。

特性
泛型只在编译阶段有效。看下面的代码：
```
        List<String> stringArrayList = new ArrayList<>();
        List<Integer> integerArrayList = new ArrayList<>();

        Class classStringArrayList = stringArrayList.getClass();
        Class classIntegerArrayList = integerArrayList.getClass();

        if (classStringArrayList.equals(classIntegerArrayList)) {
            System.out.print("输入结果：类型相同");
        }
```
输入结果：类型相同
通过上面的例子可以证明，在编译之后程序会采取去泛型化的措施。也就是说Java中的泛型，只在编译阶段有效。在编译过程中，正确检验泛型结果后，会将泛型的相关信息擦出，并且在对象进入和离开方法的边界处添加类型检查和类型转换的方法。也就是说，泛型信息不会进入到运行时阶段。

> 总结成一句话：泛型类型在逻辑上看以看成是多个不同的类型，实际上都是相同的基本类型。

通过反射添加其它类型元素
```
    public static void main(String[] args) {
        ArrayList<Integer> intList = new ArrayList<>();
        intList.add(10086);
        //用反射调用add()方法,添加字符串
        try {
            intList.getClass().getMethod("add", Object.class).invoke(intList, "hello");
        } catch (Exception e) {
            e.printStackTrace();
        }
        for (int i = 0; i < intList.size(); i++) {
            System.out.println(intList.get(i));
        }
    }
```
定义了一个ArrayList泛型类型实例化为Integer对象，如果直接调用add()方法，那么只能存储整数数据，不过当我们利用反射调用add()方法的时候，却可以存储字符串，这说明了Integer泛型实例在编译之后被擦除掉了，只保留了原始类型。


[Java泛型（二） 协变与逆变](https://www.jianshu.com/p/2bf15c5265c5)

[Java泛型总结 - 基本用法，类型限定，通配符，类型擦除](https://www.jianshu.com/p/5928ff170458)

[Kotlin 的泛型](https://kaixue.io/kotlin-generics/)

[Java 泛型 <? super T> 中 super 怎么 理解？与 extends 有何不同？](https://www.zhihu.com/question/20400700)
