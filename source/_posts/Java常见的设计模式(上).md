---
title: Java常见的设计模式(上)
date: 2020-02-10
categories: 
  - 设计模式
---

# 一. 常见的软件设计模式
总体来说23种设计模式分为三大类：
### 创建型模式（5种）
单例模式、建造者模式、工厂方法模式、抽象工厂模式、原型模式。

### 结构型模式（7种）
适配器模式、装饰器模式、代理模式、外观模式、桥接模式、组合模式、享元模式。

### 行为型模式（11种）
策略模式、模板方法模式、观察者模式、迭代子模式、责任链模式、命令模式、备忘录模式、状态模式、访问者模式、中介者模式、解释器模式。

# 二. 单例模式
### 1. 单例模式的特点?
确保一个类最多只有一个实例对象，并向整个系统提供这个实例。
**优点：**由于单例模式只生成了一个实例，所以能够节约系统资源，减少性能开销，提高系统效率，同时也能够严格控制客户对它的访问。
**缺点：**也正是因为系统中只有一个实例，这样就导致了单例类的职责过重，违背了“单一职责原则”，同时也没有抽象类，这样扩展起来有一定的困难。

### 2.单例模式的使用场景
- 整个程序的运行中只允许有一个类的实例。
- 需要频繁实例化然后销毁的对象。
- 创建对象时耗时过多或者耗资源过多，但又经常用到的对象。
- 方便资源相互通信的环境。

### 3. 单例模式实现


常见的单例模式实现方式有五种：``饿汉式、懒汉式、双重检测锁、静态内部类式和枚举单例``。而在这四种方式中饿汉式和懒汉式又最为常见。

##### 饿汉式
线程安全，调用效率高。但是不能延时加载。
    ```
      public class Singleton{
        //饿汉模式
        //将构造函数私有化
        private Singleton(){}
        //将对象实例化
        private static Singleton instance = new Singleton();
        //得到实例的方法
        public static Singleton getInstance() {
            return instance;
        }
  }
    ```
饿汉式是在类加载的时候创建实例，所以**线程是安全的**。由于该模式在加载类的时候对象就已经创建了，所以加载类的速度比较慢，但是获取对象的速度比较快。
**优点：**线程安全。   
**缺点：**如果不调用的话浪费内存。
##### 懒汉式
    ```
    public class Singleton {
        private static Singleton singleton;
        //将构造函数私有化
        private Singleton() {
        }
    
        public static Singleton getInstance() {
            //判断是否有实例化对象,没有则新建
            if (singleton == null) {
                singleton = new Singleton();
            }
            return singleton;
        }
    }
    ```
此类的设计确保只创建一个 Singleton 对象。构造函数被声明为 private，getInstance() 方法只创建一个对象。这个实现适合于单线程程序。然而，当引入多线程时，就必须通过同步来保护 getInstance() 方法。如果不保护 getInstance() 方法，则可能返回Singleton 对象的两个不同的实例。假设两个线程并发调用 getInstance() 方法并且按以下顺序执行调用：
- 线程 1 调用 getInstance() 方法并决定 instance 在 //1 处为 null。 
- 线程 1 进入 if 代码块，但在执行 //2 处的代码行时被线程 2 预占。 
- 线程 2 调用 getInstance() 方法并在 //1 处决定 instance 为 null。 
- 线程 2 进入 if 代码块并创建一个新的 Singleton 对象并在 //2 处将变量 instance 分配给这个新对象。 
- 线程 2 在 //3 处返回 Singleton 对象引用。
- 线程 2 被线程 1 预占。 
- 线程 1 在它停止的地方启动，并执行 //2 代码行，这导致创建另一个 Singleton 对象。 
- 线程 1 在 //3 处返回这个对象。
>结果是 getInstance() 方法创建了两个 Singleton 对象，而它本该只创建一个对象。
如何实现线程安全的懒汉式可以使用双重检查加锁机制。
    ```
    public class Singleton{
        //volatile防止指令重排序
        private static volatile Singleton instance;
        //将构造函数私有化
        private Singleton() {}
        public static Singleton getInstance() {
            if (instance == null) {
                synchronized (Singleton.class) {
                    if (instance == null) {
                        instance = new Singleton();
                    }
                }
            }
            return instance;
        }
    }
    ```
##### 使用静态内部类实现单例模式
    ```
        public class Singleton {
            private static class SingletonHoler {
                /**
                 * 静态初始化器，由JVM来保证线程安全
                 */
                private static Singleton instance = new Singleton();
            }
            //私有构造方法
            private Singleton() {
            }
            //获取单例对象
            public static Singleton getInstance() {
                return SingletonHoler.instance;
            }
        }
    ```
当getInstance方法第一次被调用的时候,它第一次读取SingletonHolder.instance，导致SingletonHolder类得到初始化；而这个类在装载并被初始化的时候，会初始化它的静态域，从而创建Singleton的实例，由于是静态的域，``因此只会在虚拟机装载类的时候初始化一次，并由虚拟机来保证它的线程安全性``。
>静态内部类方式是在需要实例化时，调用getInstance方法，才会加载SingletonHolder类，实例化Singleton由于类的静态属性只会在第一次加载类的时候初始化，所以在这里我们也保证了线程的安全性，所以通过这种静态内部类的方式解决了资源浪费和性能的问题

##### 使用枚举来实现单例
    ```
        public enum Singleton {
            INSTANCE;// 定义一个枚举的元素，它 就代表了Singleton的一个实例
            public void init() {
                System.out.println("资源初始化。。。");
            }
        }
    ```
可以通过Singleton.INSTANCE来访问，虚拟机会保证一个类的<clinit>() 方法在多线程环境中被正确的加锁、同步。所以，枚举实现是在实例化时是线程安全。
枚举类实现单例模式是 effective java 作者极力推荐的单例实现模式，因为枚举类型是线程安全的，并且只会装载一次，设计者充分的利用了枚举的这个特性来实现单例模式，
枚举的写法非常简单，而且枚举类型是所用单例实现中唯一一种不会被破坏的单例实现模式。

>单例被破坏的方式一般有:``反射破坏单例，序列化破坏单例，克隆破坏单例``

# 四. 构建者模式
### 1. 构建者模式的特点?
构建者模式(Builder模式)指的是在创建一个复杂的对象时，将一部负责对象的构建分为许多小对象的构建，最后在整合构建的模式。将一个复杂的构建与其表示相分离，使得同样的构建过程可以创建不同的表示。

**构建者模式的优点:**
- 使用建造者模式可以使客户端不必知道产品内部组成的细节。
- 具体的建造者类之间是相互独立的，这有利于系统的扩展。
- 具体的建造者相互独立，因此可以对建造的过程逐步细化，而不会对其他模块产生任何影响。

**构建者模式的缺点:**
产品必须有共同点，范围有限制，如果内部变化复杂，会有很多的建造类。

### 2. 建造者模式的使用场景
使用Builder模式来替代多参数构造函数是一个比较好的实践法则。
我们有时候会写这样的构造方法：
```
Person();
Person(String name);
Person(String name，int age);
Person(String name，int age，double height);
Person(String name,int age,double height,double weight);
```

在实际开发中，我们有时候需要声明所有的构造方法，这样书写很常见并且也比较有效率，但是也存在很多不足，对于代码后期维护和协同开发会是一件很痛苦的事情。
Builder模式就是使用一个代理完成对象的构建过程。这样的好处是易于扩展和类的使用，但同时也失去了一些效率。

- 如果一个对象有非常复杂的内部结构「这些产品通常有很多属性」，那么使用建造者模式。
- 如果想把复杂对象的创建和使用分离开来，那么使用建造者模式「使用相同的创建步骤可以创建不同的产品」。

### 3. 建造者模式的JAVA实现
```
public class Person {

    private String mName;
    private int mAge;
    private double mHeight;
    private double mWeight;

    private Person(Builder builder) {
        this.mName = builder.mName;
        this.mAge = builder.mAge;
        this.mHeight = builder.mHeight;
        this.mWeight = builder.mWeight;
    }

    public String getName() {
        return mName;
    }

    public int getAge() {
        return mAge;
    }

    public double getHeight() {
        return mHeight;
    }

    public double getWeight() {
        return mWeight;
    }

    public static class Builder {

        private String mName;
        private int mAge;
        private double mHeight;
        private double mWeight;

        public Builder setName(String name) {
            mName = name;
            return this;
        }

        public Builder setAge(int age) {
            mAge = age;
            return this;
        }

        public Builder setHeight(double height) {
            mHeight = height;
            return this;
        }

        public Builder setWeight(double weight) {
            mWeight = weight;
            return this;
        }

        public Person build() {
            return new Person(this);
        }
        
    }
}
```
使用:
```
public class Test {

    public static void main(String[] args) {
     Person person = new Person.Builder()
                .setName("ZhangSan")
                .setAge(11)
                .setHeight(18.0d)
                .setWeight(20.0d)
                .build();

        Log.i(TAG, "name: "+person.getName()+", age: "+person.getAge()+", height: "+person.getHeight()+", weight: "+person.getWeight());
    }
}
```


# 五. 工厂模式
### 1. 模式的特点?
工厂模式提供一个创建对象实例的功能，而无须关心其具体实现。被创建实例的类型可以是接口、抽象类，也可以是具体的类。
工厂模式用于对象的创建，使得客户从具体的产品对象中被解耦。为了解耦合，把对象的创建者与对象的使用者分开。
例如:制造一个汽车，一般情况我们需要制造轮子、引擎、座位等等；可是如果有一个CarFactory的话，调取该Factory就可以直接制造。

**模式的优点:**
- 工厂模式是为了解耦：可以将对象的创建和使用分离，如果不分离，不但违反了设计模式的开闭原则，需要使用另一个子类的话，需要修改源代码，把对象的创建和使用的过程分开。就是Class A 想调用 Class B ，那么A只是调用B的方法，而至于B的实例化，就交给工厂类。

- 工厂模式可以降低代码重复。如果创建对象B的过程都很复杂，需要一定的代码量，而且很多地方都要用到，那么就会有很多的重复代码。我们可以这些创建对象B的代码放到工厂里统一管理。既减少了重复代码，也方便以后对B的创建过程的修改维护。由于创建过程都由工厂统一管理，所以发生业务逻辑变化，不需要找到所有需要创建B的地方去逐个修正，只需要在工厂里修改即可，降低维护成本。同理，想把所有调用B的地方改成B的子类B1，只需要在对应生产B的工厂中或者工厂的方法中修改其生产的对象为B1即可，而不需要找到所有的new B（）改为new B1()。

- 因为工厂管理了对象的创建逻辑，使用者并不需要知道具体的创建过程，只管使用即可，减少了使用者因为创建逻辑导致的错误。 

- 可以通过参数设置，返回不同的构造函数，不需要修改使用类的地方。如果一个类有多个构造方法（构造的重写），我们也可以将它抽出来，放到工厂中，一个构造方法对应一个工厂方法并命名一个友好的名字，这样我们就不再只是根据参数的不同来判断，而是可以根据工厂的方法名来直观判断将要创建的对象的特点。这对于使用者来说，体验比较好。

### 2. 模式的使用场景
- 消费者不关心它所要创建对象的类(产品类)的时候。
- 消费者知道它所要创建对象的类(产品类)，但不关心如何创建的时候。

在Java语言中，我们通常有以下几种创建对象的方式：
- 使用new关键字直接创建对象；
- 通过反射机制创建对象；
- 通过clone()方法创建对象；
- 通过工厂类创建对象。

工厂设计模式分类：`` 简单工厂模式(静态工厂模式)；工厂方法模式； 抽象工厂模式``

### 3. 简单工厂模式(静态工厂模式)
就是建立一个工厂类，对实现了同一接口的一些类进行实例的创建。
1. 首先，创建二者的共同接口：
    ```
    /**
     *
     * 拿铁、卡布奇诺等均为咖啡家族的一种产品
     * 咖啡则作为一种抽象概念
     *
     */
    public abstract class Coffee {
        /**
         * 获取coffee名称
         * @return
         */
        public abstract String getName();
    }
    ```
2. 其次，创建实现类：
    ```
    /**
     * 卡布奇诺
     *
     */
    public class CappuccinoCoffee extends Coffee {
    
        @Override
        public String getName() {
            return "卡布奇诺";
        }
    }
    ```
    ```
    /**
     * 拿铁
     *
     */
    public class LatteCoffee extends Coffee {
    
        @Override
        public String getName() {
            return "拿铁";
        }
    
    }
    ```
3. 最后，建工厂类：
    ```
    public class CoffeeFactory {
    
        /**
         * 通过类型获取Coffee实例对象
         * @param type 咖啡类型
         * @return
         */
        public static Coffee create(String type){
             if("cappuccino".equals(type)){
                return new CappuccinoCoffee();
            }else if("latte".equals(type)){
                return new LatteCoffee();
            }else{
                throw new RuntimeException("type["+type+"]类型不可识别，没有匹配到可实例化的对象！");
            }
        }
    }
    ```
4. 进行测试
    ```
    public class FactoryTest {
    
        public static void main(String[] args) {
            Coffee latte = CoffeeFactory.create("latte");
            System.out.println("创建的咖啡实例为:" + latte.getName());
            Coffee cappuccino = CoffeeFactory.create("cappuccino");
            System.out.println("创建的咖啡实例为:" + cappuccino.getName());
        }
    }
    ```

**特点：**
- 它是一个具体的类，非接口或是抽象类。有一个重要的create()方法，利用if或者 switch创建产品并返回。
-  create()方法通常是静态的，所以也称之为静态工厂。

**优点：**
使用简单，代码少，所以使用较多。

**缺点：**
添加新的产品需要修改工厂里面的方法，不修改代码的话是无法进行扩展的。所以违背了开闭原则（对扩展开放，对修改关闭）。


### 4.工厂方法模式
也就是定义一个抽象工厂，其定义了产品的生产接口，但不负责具体的产品，将生产任务交给不同的派生类工厂。这样不用通过指定类型来创建对象了。工厂方法是针对每一种产品提供一个工厂类。
通过不同的工厂实例来创建不同的产品实例。

1. 修改工厂类
   ```
    public interface CoffeeFactory {
        //创建不同的产品
        Coffee create();
    }
   ```
2. 创建生产不同产品的工厂
    ```
    public class CappuccinoFactory implements CoffeeFactory {
        @Override
        public Coffee create() {
            return new CappuccinoCoffee();
        }
    }
    ```
    ```
    public class LatteFactory implements CoffeeFactory {
        @Override
        public Coffee create() {
            return new LatteCoffee();
        }
    }
    ```


2. 测试
    ```
        public static void main(String[] args) {
            CappuccinoFactory cappuccinoFactory = new CappuccinoFactory();
            Coffee cappuccino = cappuccinoFactory.create();
    
            LatteFactory latteFactory = new LatteFactory();
            Coffee latte = latteFactory.create();
        }
    ```             

>当需要增加一个产品 Mocca(摩卡咖啡) 时，只需要增加 Mocca 具体产品类和 MoccaFactory 具体工厂类即可，不需要修改原有的产品类和工厂类

**特点：**
符合开闭原则，工厂方法模式是简单工厂模式的延伸，它继承了简单工厂模式的优点，同时还弥补了简单工厂模式的不足。              
**优点：**
- 在工厂方法模式中，工厂方法用来创建客户所需要的产品，同时还向客户隐藏了哪种具体产品类将被实例化这一细节，用户只需要关心所需产品对应的工厂，无须关心创建细节，甚至无须知道具体产品类的类名。
- 基于工厂角色和产品角色的多态性设计是工厂方法模式的关键。它能够让工厂可以自主确定创建何种产品对象，而如何创建这个对象的细节则完全封装在具体工厂内部。工厂方法模式之所以又被称为多态工厂模式，就正是因为所有的具体工厂类都具有同一抽象父类。
- 使用工厂方法模式的另一个优点是在系统中加入新产品时，无须修改抽象工厂和抽象产品提供的接口，无须修改客户端，也无须修改其他的具体工厂和具体产品，而只要添加一个具体工厂和具体产品就可以了，这样，系统的可扩展性也就变得非常好，完全符合”开闭原则”。

**缺点：**                                                                                                                                                                                                                                                       
- 在添加新产品时，需要编写新的具体产品类，而且还要提供与之对应的具体工厂类，系统中类的个数将成对增加，在一定程度上增加了系统的复杂度，有更多的类需要编译和运行，会给系统带来一些额外的开销。
- 由于考虑到系统的可扩展性，需要引入抽象层，在客户端代码中均使用抽象层进行定义，增加了系统的抽象性和理解难度，且在实现时可能需要用到DOM、反射等技术，增加了系统的实现难度。

### 5. 抽象工厂模式  
工厂方法模式不管工厂怎么拆分抽象，都只是针对一类产品。如果要生成另一种产品，如果用上述工厂方法方式，除去对应的产品实体类还需要新增抽象工厂及具体工厂实现，随着产品的增多，会导致类爆炸。这时就需要使用到抽象工厂模式。
抽象工厂是应对产品族概念的。比如说，每个饮料厂可能要同时生产茶，汽水，咖啡，那么每一个工厂都要有创建茶，汽水车和咖啡的方法。
抽象工厂模式是工厂方法模式的升级版本。例如上面的饮料厂引入了的新的饮品种类：茶。我们可以将世界各地的饮料厂抽象为一个饮料厂接口，这个饮料厂生产两种饮料：咖啡和茶。咖啡又分为卡布奇诺和拿铁等种类，需要将咖啡进行抽象。茶分为红茶和绿茶，也需要对茶进行抽象。在中国和美国都有饮料厂，他们属于饮料厂接口的实现，拥有生产咖啡和茶的功能。至于中国和美国的饮料厂生产的咖啡是卡布奇诺还是摩卡，生产的茶是红茶还是绿茶需要自己去实现。

例如：中国的饮料厂生产拿铁咖啡和红茶。美国的饮料厂生产卡布奇诺和绿茶，代码实现为：
 1. 添加新的产品茶，并且创建其实现类：红茶和绿茶。
    ```
    public interface Tea {
        /**
         * 获取茶的名称
         * @return
         */
        public abstract String getName();
    }
    ```

    ```
    public class RedTea implements Tea {
        @Override
        public String getName() {
            return "红茶";
        }
    }
    ```

    ```
    public class GreenTea implements Tea {
        @Override
        public String getName() {
            return "绿茶";
        }
    }
    ```
2. 定义饮料抽象工厂，及中国饮料工厂和美国饮料工厂的实现。
    ```
    public interface DrinkFactory {
    
        //制造咖啡
        Coffee createCoffee();
    
        //制造茶
        Tea createTea();
    }
    ```

    ```
    public class ChinaDrinkFactory implements DrinkFactory {
        @Override
        public Coffee createCoffee() {
            return new LatteCoffee();
        }
    
        @Override
        public Tea createTea() {
            return new RedTea();
        }
    }
    ```

    ```
    public class AmericaDrinkFactory implements DrinkFactory{
        @Override
        public Coffee createCoffee() {
            return new CappuccinoCoffee();
        }
    
        @Override
        public Tea createTea() {
            return new GreenTea();
        }
    }
    ```
3.测试类，创建中国工厂和美国工厂进行生产。
    ```
    public class FactoryTest {
            public static void main(String[] args) {
                ChinaDrinkFactory chinaDrinkFactory = new ChinaDrinkFactory();
                Coffee coffee = chinaDrinkFactory.createCoffee();
                Tea tea = chinaDrinkFactory.createTea();
    
                AmericaDrinkFactory americaDrinkFactory = new AmericaDrinkFactory();
                Coffee coffee1 = americaDrinkFactory.createCoffee();
                Tea tea1 = americaDrinkFactory.createTea();
            }
    }
    ```

**特点：**
用来生产不同的产品族的全部产品，增加新的产品线很容易，但是无法增加新的产品。
抽象工厂模式与工厂方法模式最大的区别：抽象工厂中每个工厂可以创建多种类的产品；而工厂方法每个工厂只能创建一类。

**优点：**
- 可以在类的内部对产品族中相关联的多等级产品共同管理，而不必专门引入多个新的类来进行管理。
- 当增加一个新的产品族时不需要修改原代码，满足开闭原则。

**缺点：**
当产品族中需要增加一个新的产品时，所有的工厂类都需要进行修改。

>抽象工厂在使用中出现的很少,除非要建立多个产品种类的情况,一般情况用工厂方法即可解决.

参考资料：
[为什么用枚举类来实现单例模式越来越流行？](https://zhuanlan.zhihu.com/p/80127173)
[Java 设计模式之抽象工厂模式](https://juejin.im/entry/6844903509729476621)
[Android设计模式之一个例子让你彻底明白工厂模式(Factory Pattern)](https://blog.csdn.net/nugongahou110/article/details/50425823)