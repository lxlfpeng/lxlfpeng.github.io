---
title: 面向对象设计模式理论总结-Java版
date: 2017-05-19
categories: 
  - 编程基础
tags: 
  - 设计模式
---

# 一. 什么是UML类图?
UML类图是一种结构图，用于描述一个系统的静态结构。类图以反映类结构和类之间关系为目的，用以描述软件系统的结构，是一种静态建模方法。类图中的类，与面向对象语言中的类的概念是对应的，因此又称统一建模语言，类图是使用频率最高的UML图之一。

# 二. 类图中的表示方式
### 1.类在类图中的表示方式
在UML类图中，类使用包含类名、属性(field) 和方法(method) 且带有分割线的矩形来表示，比如下图表示一个Employee类，它包含name、age和email这3个属性，以及modifyInfo()方法。
![](/images/a55e5548bce33cf410160b449545c7f6.webp)
对应代码：
```
public class Employee {
    private String name;
    private int age;
    private String email;
    
    public void modifyInfo() {
        ...
    }
}
```

### 2.类图中可见性符号
UML类图中表示可见性的符号有三种，用来``表示属性或方法的可见性``：
- +：表示public
- -：表示private
- '#'：表示protected

### 3.类图中属性的完整表示
属性的完整表示方式是这样的：
**可见性  名称 ：类型 [ = 缺省值]**
- “可见性”表示该属性对于类外的元素而言是否可见，包括公有(public)、私有(private)和受保护(protected)三种，在类图中分别用符号+、-和#表示。
- “名称”表示属性名，用一个字符串表示。
- “类型”表示属性的数据类型，可以是基本数据类型，也可以是用户自定义类型。
- “缺省值”是一个可选项，即属性的初始值。
>中括号中的内容表示是可选的

### 4.类图中方法的完整表示
方法的完整表示方式如下：
**可见性  名称(参数列表) [ ： 返回类型]**
- “可见性”的定义与属性的可见性定义相同。
- “名称”即方法名，用一个字符串表示。
- “参数列表”表示方法的参数，其语法与属性的定义相似，参数个数是任意的，多个参数之间用逗号“，”隔开。
- “返回类型”是一个可选项，表示方法的返回值类型，依赖于具体的编程语言，可以是基本数据类型，也可以是用户自定义类型，还可以是空类型(void)，如果是构造方法，则无返回类型。
>中括号中的内容是可选的。

只有方法没有属性的表示方式：
![](/images/070d42fcc5d31c2b3d3e85db276a4a6b.webp)
- public方法method1接收一个类型为Object的参数，返回值类型为void。
- protected方法method2无参数，返回值类型为String。
- private方法method3接收类型分别为int、int[]的参数，返回值类型为int。

# 三.类与类之间关系的表示方式
在软件系统中，类并不是孤立存在的，类与类之间存在各种关系，对于不同类型的关系，UML提供了不同的表示方式。在UML类图中，常见的有以下几种关系: ``泛化（Generalization）,  实现（Realization），关联（Association)，聚合（Aggregation），组合(Composition)，依赖(Dependency)``
### 1.泛化关系（继承关系）
泛化(Generalization)关系也就是**继承关系**，用于描述父类与子类之间的关系，父类又称作基类或超类，子类又称作派生类。继承关系对应的是extend关键字，在UML类图中用带空心三角形的直线表示，如下图所示中，Student类与Teacher类继承了Person类。
![](/images/9481a601ddc3b10c0a927bfa278ef63f.webp)
``由子类指向父类。``

### 2.接口实现关系
 接口之间也可以有与类之间关系类似的继承关系和依赖关系，但是接口和类之间还存在一种**实现(Realization)关系**。这种关系对应implement关键字，在UML类图中用带空心三角形的虚线表示。如下图中，Car类与Ship类都实现了Vehicle接口。
![](/images/3dc4a44001b7b08d3d5a760a3927ed1a.webp)
``实现类指向接口``

### 3.组合关系
组合关系与聚合关系见得最大不同在于：这里的“部分”脱离了“整体”便不复存在。比如下图：
![](/images/24fb505ab81e376db15f9ad91440c753.webp)
显然，嘴是头的一部分且不能脱离了头而单独存在。在UML类图中，组合关系用一个带实心菱形和箭头的直线表示。
>整体与部分的关系，但是整体与部分不可以分开。整体指向部分

### 4.聚合关系
聚合是整体与部分的关系，且部分可以离开整体而单独存在。
![](/images/825368394a08a86ba00bb2532a8adf34.webp)
上图中的Car类与Engine类就是聚合关系（Car类中包含一个Engine类型的成员变量）。由上图我们可以看到，UML中聚合关系用带空心菱形和箭头的直线表示。聚合关系强调是“整体”包含“部分”，但是“部分”可以脱离“整体”而单独存在。比如上图中汽车包含了发动机，而发动机脱离了汽车也能单独存在。
>整体和部分的关系，整体与部分可以分开。整体指向部分

### 5.关联关系
表示一个类的属性保存了对另一个类的一个实例（或多个实例）的**引用**。关联关系又可进一步分为单向关联、双向关联和自关联。 关联关系是类与类之间最常用的一种关系，表示一类对象与另一类对象之间有联系。组合、聚合也属于关联关系，只是关联关系的类间关系比其他两种要弱。
#####  (1.)单向关联关系
![](/images/9596a838fb2d8f0f58f7e38320f4d2d7.webp)
我们可以看到，在UML类图中单向关联用一个带箭头的直线表示。上图表示每个顾客都有一个地址，这通过让Customer类持有一个类型为Address的成员变量类实现。

#####  (2.)双向关联关系
![](/images/4d12d92c703d9cad355417df442d87fe.webp)
从上图中我们很容易看出，所谓的双向关联就是双方各自持有对方类型的成员变量。在UML类图中，双向关联用一个不带箭头的直线表示。上图中在Customer类中维护一个Product[]数组，表示一个顾客购买了那些产品；在Product类中维护一个Customer类型的成员变量表示这个产品被哪个顾客所购买。

##### 自关联
![](/images/eae420ba882da507ea312c769458489a.webp)
自关联在UML类图中用一个带有箭头且指向自身的直线表示。上图的意思就是Node类包含类型为Node的成员变量，也就是“自己包含自己”。
``拥有者指向被拥有者``

### 6.依赖关系
依赖关系（Dependence）：假设A类的变化引起了B类的变化，则说名B类依赖于A类。大多数情况下，依赖关系体现在某个类的方法使用另一个类的对象作为参数。依赖(Dependency)关系是一种使用关系，特定事物的改变有可能会影响到使用该事物的其他事物，在需要表示一个事物使用另一个事物时使用依赖关系。大多数情况下，依赖关系体现在某个类的方法使用另一个类的对象作为参数。
![](/images/240413eab421604eb45deb66bf9faac9.webp)
从上图我们可以看到，Driver的drive方法只有传入了一个Car对象才能发挥作用，因此我们说Driver类依赖于Car类。在UML类图中，依赖关系用一条带有箭头的虚线表示。

``使用者指向被使用者``

>这六种类关系中，组合、聚合和关联的代码结构一样，可以从关系的强弱来理解，各类关系从强到弱依次是：**继承→实现→组合→聚合→关联→依赖**。UML类图是面向对象设计的辅助工具。

# 四.软件设计模式
### 1.什么是软件设计模式?
软件设计模式（Software Design Pattern），又称设计模式，是指在软件开发中，经过验证的，用于解决在特定环境下、重复出现的、特定问题的解决方案。

### 2.软件设计模式的目的
设计模式的本质是面向对象设计原则的实际运用，是对类的封装性、继承性和多态性以及类的关联关系和组合关系的充分理解。正确使用设计模式具有以下优点。
- 可以提高程序员的思维能力、编程能力和设计能力。
- 使程序设计更加标准化、代码编制更加工程化，使软件开发效率大大提高，从而缩短软件的开发周期。
- 使设计的代码可重用性高、可读性强、可靠性高、灵活性好、可维护性强。

# 五.面向对象设计的七大原则
- 开闭原则（Open Closed Principle，OCP）
- 单一职责原则（Single Responsibility Principle, SRP）
- 里氏代换原则（Liskov Substitution Principle，LSP）
- 依赖倒转原则（Dependency Inversion Principle，DIP）
- 接口隔离原则（Interface Segregation Principle，ISP）
- 合成/聚合复用原则（Composite/Aggregate Reuse Principle，CARP）
- 迪米特法则（Law of Demeter，LOD） 或者最少知识原则（Least Knowledge Principle，LKP）

>其中，单一职责原则、开闭原则、迪米特法则、里氏代换原则和接口隔离原则的英文首字母拼在一起就是**SOLID（稳定的）**，所以也称之为SOLID原则。

### 1.单一职责原则（Single Responsibility Principle）
对类来说的，即一个类应该只负责一项职责。如类A负责两个不同职责：职责1，职责2。当职责1需求变更而改变A时，可能造成职责2执行错误，所以需要将类A的粒度分解为A1和A2。类的职责要单一，不能将太多的职责放在一个类中。
**例如:大学学生工作管理程序。**
分析：大学学生工作主要包括学生生活辅导和学生学业指导两个方面的工作，其中生活辅导主要包括班委建设、出勤统计、心理辅导、费用催缴、班级管理等工作，学业指导主要包括专业引导、学习辅导、科研指导、学习总结等工作。如果将这些工作交给一位老师负责显然不合理，正确的做 法是生活辅导由辅导员负责，学业指导由学业导师负责，其类图如图所示。
![](/images/b3e1e762f6b029f858cef33dcb6606ae.webp)

单一职责原则注意事项和细节:
- 降低类的复杂度，一个类只负责一项职责。
- 提高类的可读性，可维护性。
- 降低变更引起的风险。
- 通常情况下，我们应当遵守单一职责原则，只有逻辑足够简单，才可以在代码级违反单一职责原则：只有类种方法数量足够少，可以在方法级别保持单一职责原则。

>注意：单一职责同样也适用于方法。一个方法应该尽可能做好一件事情。如果一个方法处理的事情太多，其颗粒度会变得不细，不利于重用。

### 2.开闭原则(Open-Closed Principle)
对扩展开放，对修改关闭。 一般情况，我们接到需求变更的通知，通常方式可能就是修改模块的源代码，然而修改已经存在的源代码是存在很大风险的，尤其是项目上线运行一段时间后，开发人员发生变化，这种风险可能就更大。 所以，为了避免这种风险，在面对需求变更时，我们一般不修改源代码，即所谓的对修改关闭。不允许修改源代码，我们如何应对需求变更呢？答案就是我们下面要说的对扩展开放。 通过扩展去应对需求变化，就要求我们必须要面向接口编程，或者说面向抽象编程。所有参数类型、引用传递的对象必须使用抽象（接口或者抽象类）的方式定义，不能使用实现类的方式定义； 通过抽象去界定扩展，比如我们定义了一个接口A的参数，那么我们的扩展只能是接口A的实现类。这样原则设计出来的系统，遇到增加功能的需求时，几乎不用修改源代码，只是增加几个类，然后调用就好。 这样既增加了新功能满足了需求，又维护了原本系统的稳定性。
**例如:**
1. 首先创建一个手机接口:
```
public interface Phone {
    String getName();//名称

    Double getPrice();//价格
}
```
2. 创建一个IPhone手机实现手机接口:
```
public class IPhone implements Phone {
    private String name;
    private Double price;

    public IPhone(String name, Double price) {
        this.name = name;
        this.price = price;
    }

    @Override
    public String getName() {
        return name;
    }

    @Override
    public Double getPrice() {
        return price;
    }
}
```
3. 使用类
```
public class PhoneSore {
    public static void main(String[] args) {
        Phone phone = new IPhone("Iphone 4S", 6000.00);
        System.out.println("欢迎购买：名字：" + phone.getName() + " 价格：" + String.valueOf(phone.getPrice()));
    }
}
```
上面的代码可以正常地运行，我们可以方便地添加新的手机。但是如果需求发生了变更，手机店推出了打折地活动。如何解决？
有下面三种方法可以解决此问题：
- 修改接口
  在IPhone接口中，增加一个方法getDiscountPrice，专门用于处理打折需求。但是这个方法是有问题的，接口应该是稳定且可靠的，不应该经常发生变化，否则接口作为契约的作用就失去了。且违背了开闭原则，因此否定。

- 修改实现类
  第二种方法是通过修改实现类中的getPrice方法或者增加getDiscountPrice方法实现其需求，但是这样一个类中就存在了两个读取价格的方法，且违背了开闭原则，所以此方法也不是一个最优方案。

- 通过扩展实现变化
  我们可以通过增加一个子类IPhoneDiscount，复写getPrice方法，此方法修改少，对现有的代码没有影响，风险少，是个好方法。

4. 添加打折类
```
public class IPhoneDiscount extends IPhone {
    public IPhoneDiscount(String name, Double price) {
        super(name, price);
    }

    //打折活动
    public Double getPrice() {
        //九折优惠
        return super.getPrice() * 0.90;
    }
}
```


![](/images/447f586d18b8adec5daf3af1ef790e91.webp)

### 3.里式替换原则(Liskov Substitution Principle)
所有引用基类（父类）的地方，都必须能透明地使用其子类的对象。父类可被子类替换，但反之不一定成立。也就是说，代码中可以将父类全部替换为子类，程序不会出现异常。当使用继承时，遵循里氏替换原则。类B继承类A时，除添加新的方法完成新增功能P2外，尽量不要重写父类A的方法，也尽量不要重载父类A的方法。里氏替换原则通俗的来讲就是：子类可以扩展父类的功能，但不能改变父类原有的功能。
例如：我喜欢动物，那我一定喜欢狗，因为狗是动物的子类。但是我喜欢狗，不能据此断定我喜欢动物，因为我并不喜欢老鼠，虽然它也是动物。

>尽量不要重写父类方法，而是增加自己特有的方法。继承给程序设计带来巨大便利的同时，也带来了弊端。如果一个类被其他的类所继承，则当这个类需要修改时，必须考虑到所有的子类，并且父类修改后，所有涉及到子类的功能都有可能会产生BUG。

例如：
1. 先定义一个鸟的接口。
```
public class Bird {
    private int velocity;

    public int getVelocity() {
        return velocity;
    }

    public void setVelocity(int velocity) {
        this.velocity = velocity;
    }
}
```
2. 定义鸵鸟去实现鸟的功能。
```
public class Ostrich extends Bird{

    public int getVelocity() {
        //鸵鸟是不会飞的所以他的飞行时间就为0
        return 0;
    }
}
```
2. 测试
```
public class main {

    public static void main(String[] args) {
        //计算鸟的飞行时间    
        Bird bird = new Bird();
        bird.setVelocity(100);
        int h = flyTime(bird);
        System.out.println("飞行时间是:"+h);

        //计算鸵鸟的飞行时间
        Bird ostrich = new  Ostrich();
        ostrich.setVelocity(100);
        int h = flyTime(ostrich);
        System.out.println("飞行时间是:"+h);
    }
/*
*计算飞行3000米需要的时间
*/
    public static int flyTime(Bird bird)
    {
        return 3000/bird.getVelocity();
    }
}
```
结果：
```
普通鸟运行结果正确，飞行时间是:30。
计算鸵鸟的飞行时间报错。
```

面向对象的语言的三大特点是继承，封装，多态，里氏替换原则是依赖于继承，多态这两大特性。里氏替换原则的定义是，所有引用基类的地方必须能透明地使用其子类的对象。通俗来讲是只要父类能出现的地方子类就可以出现，而且替换为子类也不会产生任何错误和异常。而我们在使用flyTime方法时 ，当使用者flyTime方法里的参数Bird被Ostrich替换掉后，结果出现了异常，那么它明显违背了里氏替换原则。

### 4.接口隔离原则(Interface Segregation Principle)
使用多个专门的接口，而不使用单一的总接口。不要对外暴露没有实际意义的接口。也就是说使用多个专门的接口比使用单一的总接口要好。
例如：对于鸟的实现（Bird），我们可以定义两个功能接口，分别是Fly和Eat，我们可以让Bird分别实现这两个接口。 如果我们还有一个Dog，那么对于Eat接口，可以复用。但是如果只有一个接口（包含Fly和Eat两个功能），对于Dog来说， 它是不会飞（Fly）的，那么就需要针对Dog再声明一个新的接口，这是没有必要的设计。

### 5.依赖倒置原则(Dependence Inversion Principle)
高层模块不应该依赖低层模块，二者都应该依赖其抽象。抽象不应该依赖细节，细节应该依赖抽象 。一开始类A依赖于类B，由于需求发生了改变。要将类A依赖于类C，则我们需要修改类A依赖于类B的相关代码，这样会对程序产生不好的影响。假如需求又发生了改变，我们又需要修改类A的代码。

例如：
```
public class UserService {
    private Plaintext plaintext; // 明文登录注册
    
    public void register(){
        Plaintext.register();    // 调用明文的注册方法
    }
    public void login(){
        Plaintext.login();        // 调用明文的登录方法
    }
}
```
上面的例子可以看出，UserService类依赖于Plaintext类。有一天，由于使用明文登录注册不安全，需求改为使用密文登录注册。我们可以怎么办？
```
//不符合 依赖倒置原则
public class UserService {
    // private Plaintext plaintext;
    private Ciphertext ciphertext;    // 密文登录注册
    
    public void register(){
        // Plaintext.register();
        Ciphertext.register();        // 调用密文的注册方法
    }
    public void login(){
        // Plaintext.login();
        Ciphertext.login();            // 调用密文的登录方法
    }
}
```
在上面的例子，修改一个需求几乎将整个UserService类都修改了一遍，这不但麻烦，而且会给程序带来很多风险。所以上面的例子不符合依赖倒置原则。
```
//符合 依赖倒置原则
public class UserService {
    private Authentication authentication;    // 依赖于接口（抽象）
    
    public UserServer(Authentication auth) {
        //接口与实现类对接
        this.authentication = auth;
    }
    
    public void register(){
        authentication.register();
    }
    public void login(){
        authentication.login();
    }
}


public interface Authentication {
    //...登录注册
}
public class Ciphertext implements Authentication {
    //...使用明文的实现
}
public class Plaintext implements Authentication {
    //...使用密文的实现
}
```
在上面的例子Ciphertext类和Plaintext类实现了Authentication接口。而UserService类依赖于Authentication接口。这样可以在构造函数里随意切换登录注册的模式。 假设以后还需要更改需求，只需要实现Authentication接口然后在构造函数里注入就可以了。

### 6.迪米特法则(Law Of Demeter)
如果两个类不彼此通信，那么这两个类就不应当直接地发生相互作用。如果其中一个类需要另一个类的某一个方法的话，可以通过第三者转发这个调用。 迪米特法则的初衷是降低类之间的耦合，由于每个类都减少了不必要的依赖，因此的确可以降低耦合关系。 但是凡事都有度，虽然可以避免与非直接的类通信，但是要通信，必然会通过一个“中介”来发生联系，过分的使用迪米特原则，会产生大量这样的中介和传递类，导致系统复杂度变大。 所以在采用迪米特法则时要反复权衡，既做到结构清晰，又要高内聚低耦合。

### 7.合成复用原则(Composite/Aggregate Reuse Principle)
合成复用原则目的就是尽量使用对象组合，而不是继承来达到复用的目的。通过继承来进行复用的主要问题在于继承复用会破坏系统的封装性，因为继承会将基类的实现细节暴露给子类，由于基类的内部细节通常对子类来说是可见的， 所以这种复用又称“白箱”复用，子类与父类的耦合度高。父类的实现的任何改变都会导致子类的实现发生变化，这不利于类的扩展与维护。而且它限制了复用的灵活性。 从父类继承而来的实现是静态的，在编译时已经定义，所以在运行时不可能发生变化。

由于组合或聚合关系可以将已有的对象（也可称为成员对象）纳入到新对象中，使之成为新对象的一部分，因此新对象可以调用已有对象的功能，这样做可以使得成员对象的内部实现细节对于新对象不可见，所以这种复用又称为“黑箱”复用，相对继承关系而言，其耦合度相对较低，成员对象的变化对新对象的影响不大，可以在新对象中根据实际需要有选择性地调用成员对象的操作；
合成复用可以在运行时动态进行，新对象可以动态地引用与成员对象类型相同的其他对象。

### 8.总结
![](/images/c374affe87a93bb04cca6fc91b685aa7.webp)



参考资料：
[设计模式概念和七大原则](http://www.throwable.club/2019/05/05/design-pattern-basic-law/)
[设计模式之七大基本原则](https://zhuanlan.zhihu.com/p/24614363)
[万字总结之设计模式七大原则](https://juejin.im/post/6844904065806106632)
[设计模式之七大基本原则](https://zhuanlan.zhihu.com/p/24614363)








