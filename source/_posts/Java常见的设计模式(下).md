---
title: Java常见的设计模式(下)
date: 2020-03-11
categories: 
  - 编程基础
tags: 
  - 设计模式
---

# 一. 常见的软件设计模式
接上一篇，我们说到面向对象设计模式总体来说23种设计模式分为三大类：
### 创建型模式（5种）
单例模式、建造者模式、工厂方法模式、抽象工厂模式、原型模式。

### 结构型模式（7种）
适配器模式、装饰器模式、代理模式、外观模式、桥接模式、组合模式、享元模式。

### 行为型模式（11种）
策略模式、模板方法模式、观察者模式、迭代子模式、责任链模式、命令模式、备忘录模式、状态模式、访问者模式、中介者模式、解释器模式。

# 二. 适配器模式
#### 1. 概念
将一个类的接口转换成客户希望的另外一个接口，从而使原本因接口不匹配而无法在一起工作的两个类能够在一起工作。
例子：笔记本电脑电源一般用的都是5V电压，但是我们的家用电是220V，我们要让笔记本充上电，最好的办法应该是通过一个工具把220V的电压转换成5V，这个工具就是适配器。
![](/images/724553622152891467bd6260bad90552.webp)
#### 2. 适配器模式涉及3个角色
- **目标 Target（目标抽象类）：**目标抽象类定义客户所需接口，可以是一个抽象类或接口，也可以是具体类，相当于插座。
- **适配器 Adapter（适配器类）：**适配器可以调用另一个接口，作为一个转换器，对Adaptee和Target进行适配，适配器类是适配器模式的核心，在对象适配器中，它通过继承Target并关联一个Adaptee对象使二者产生联系，相当于插头转换器。
- **源 Adaptee（适配者类）：**适配者即被适配的角色，它定义了一个已经存在的接口，这个接口需要适配，适配者类一般是一个具体类，包含了客户希望使用的业务方法，在某些情况下可能没有适配者类的源代码，相当于插头。

#### 3. 适配器模式分类
适配器模式主要分为三类：``类的适配器模式、对象的适配器模式、接口的适配器模式。``

#### 4. 类适配器模式
一般手机充电器输出的直流电压为5V，我们把交流电220V称为源，希望得到的直流电5V称为目标，而充电器即为适配器。
```
//源，交流电 已存在的、具有特殊功能、但不符合我们既有的标准接口的类
public class AC {
    public int outputAC(){
        return 220;
    }
}
//目标接口，或称为标准接口，直流电
public interface IDC {
    int outputDC();
}
//适配器
public class ClsAdapter extends AC implements IDC{

    @Override
    public int outputDC() {
        return outputAC()/44;  //直流电为交流电的电压值除以44
    }

    public static void main(String[] args) {
        ClsAdapter adapter = new ClsAdapter();
        System.out.println("交流电电压:" + adapter.outputAC());
        System.out.println("直流电电压:" + adapter.outputDC());
    }
}

/** 
输出结果为：
交流电电压:220
直流电电压:5
*/
```
可以看到，类适配器是通过继承源类，实现目标接口的方式实现适配的。但是，由于Java单继承的机制，这就要求目标必须是接口，有一定的局限性。

#### 5. 对象适配器模式          
对象适配器，不是继承源类，而是依据关联关系，持有源类的对象，这也隐藏了源类的方法。在这里，适配器和源类的关系不是继承关系，而是组合关系。
```
public class ObjAdapter implements IDC {
    //持有源类的对象
    private AC ac;

    public ObjAdapter(AC ac){
        this.ac = ac;
    }

    public int outputAC(){
        return ac.outputAC();
    }

    @Override
    public int outputDC() {
        return ac.outputAC()/44;
    }

    public static void main(String[] args) {
        ObjAdapter adapter = new ObjAdapter(new AC());
        System.out.println("交流电电压:" + adapter.outputAC());
        System.out.println("直流电电压:" + adapter.outputDC());
    }
}
//输出结果同上
```
#### 6.适配器模式优点
- 客户端通过适配器可以透明的调用目标接口。
- 复用了现存的类，程序员不需要修改原有代码而重用现有的适配者类。
- 将目标类和适配类解耦，解决了目标类和适配类接口不一致的问题。

#### 7.适配器模式缺点
- 对类适配器来说，更换适配器的过程比较复杂。
>需要注意的是，在设计阶段，不要想着用适配器模式，这根本就是用于修改不合理的设置才产生的.并且过多地使用适配器，会让系统非常零乱，不易整体进行把握。比如，明明看到调用的是 A 接口，其实内部被适配成了 B 接口的实现，一个系统如果太多出现这种情况，无异于一场灾难。因此如果不是很有必要，可以不使用适配器，而是直接对系统进行重构。

# 三. 装饰器模式
### 1. 概念
装饰器模式( Decorator Pattern ) ，也称为包装模式( Wrapper Pattern )。装饰器模式是一种结构型的设计模式。在不改变原有对象的基础之上，将功能附加到对象上，扩展原有对象的功能。
使用该模式的目的是为了较为灵活的对类进行扩展，而且不影响原来类的结构。


### 2. 在装饰器模式中的角色有：

**抽象构件(Component)角色：**给出一个抽象接口，已规范准备接收附加责任的对象。
**具体构件(ConcreteComponent)角色：**定义一个将要接收附加责任的类
**装饰(Decorator)角色：**持有一个构件(Component)对象的实例，并定义一个与抽象构件接口一致的接口。
**具体装饰(ConcreteDecorator)角色：**负责给构件对象“贴上”附加的责任。

### 3. 代码实现
1. 以绘制形状为例，平时绘制的形状五花八门，可能有圆形、矩形、三角形...等等，我们抽取出一个抽象的形状接口：
    ```
    /**
     * 形状接口
     */
    public interface Shape {
        //定义公用的形状绘制方法
        void draw();
    }
    ```
2. 接下来，假如我们要绘制一个圆形，会实现Shape接口，定义具体绘制圆形的方法：
    ```
         /**
         * 圆形类
         */
        public class Cicle implements Shape {
            @Override
            public void draw() {
                System.out.println("绘制一个圆形");
            }
        }
    ```
3. 如果某一天，有一个特殊的需求，需要绘制一个红色的圆形，但又不允许更改Circle类，如果是按继承写法会是如下：
    ```   
       /**
        * 红色的圆形
        */
       public class RedCircle extends Circle{
           @Override
           public void onDraw() {
               super.onDraw();
               System.out.println("给圆形填充上红色");
           }
       }
    ```
4. 效果是实现了，等到某一天，又来了个需求，要绘制一个带边框的红色圆，且依然不能修改原来的类，那就继续继承RedCircle实现就行了...如此反复循环，继承的具体形状类会越来越多，且可能会嵌套了很多层，不利于代码的维护。   
将以上改为装饰器模式来实现的话，可以先定义一个抽象装饰者来装饰Shape：
    ```
    /**
     * 抽象装饰者类，对Shape接口进行包装 
     */
    public  class ShapeDecorator implements Shape {
        protected Shape shape;
    
        public ShapeDecorator(Shape shape) {
            this.shape = shape;
        }
    
        @Override
        public void draw() {
            shape.draw();
        }
    }
    ```

5. 假如是实现一个带边框的红色圆形.使用装饰器来实现如下:
    ```
    /**
     * 创建一个继承了抽象装饰器类实体装饰器类
     *
     * 具体的装饰器类，实现具体要向被装饰对象添加的功能。用来装饰具体的组件对象或者另外一个具体的装饰器对象
     *
     */
    public class RedOutlineCircleDecorator extends ShapeDecorator {
        public RedOutlineCircleDecorator(Shape shape) {
            //调用父类的构造方法，将参数传给父类
            super(shape);
        }
    
        @Override
        public void draw() {
            //这里可以选择性的调用父类的方法，如果不调用则相当于完全改写了方法，
            super.draw();
            System.out.println("给圆形填充上红色");
            System.out.println("给圆形画上边框");
        }
    }

    ```
     
6. 第五步测试
    ```
    public static void main(String agrs[]){
       Shape circle = new Circle();
       //绘制一个带边框的红色圆形
       RedOutlineCircleDecorator redOutlineCircleDecorator = new RedOutlineCircleDecorator(circle);
       redOutlineCircleDecorator.onDraw();
    }
    ```
![](/images/62ee37b9179c9f886f0d3a834c95a0ab.webp)

**优点：**
- 相比与静态的继承，装饰器模式正如它定义的，那样可以动态的给一个对象添加额外的职责， 显得更加灵活。静态继承的情况下，如果要添加其他的功能就需要添加新的子类实现功能，然后相互之间继承，以达到一个组合的功能，对于每一个要添加的功能都要，新建类，显得特别麻烦，也使得系统越来越复杂，而对于装饰器来说，为一个特定的Component提供多种不同的Decorator，对于一些要达成的功能，相互组合就可以达成目的。
- 装饰类和被装饰类可以独立发展，而不会相互耦合。
- 装饰模式是继承关系的一个替代方案。我们看装饰类Decorator，不管装饰多少层，返回的对象还是Component，实现的还是is-a的关系。

**缺点：**
对于装饰模式记住一点就足够了：多层的装饰是比较复杂的。为什么会复杂呢？你想想看，就像剥洋葱一样，你剥到了最后才发现是最里层的装饰出现了问题，想象一下工作量吧，因此，尽量减少装饰类的数量，以便降低系统的复杂度。


>装饰模式和前面的代理模式有点类似，容易把装饰模式看成代理模式。装饰模式是继承的一种替代方案，主要为所装饰的对象增强功能，动态的增加方法。而代理模式主要是为了控制对原有对象的访问权限，不对原有对象进行功能增强。
 
# 四. 代理模式
### 1. 概念
代理(Proxy)是一种设计模式，提供了对目标对象另外的访问方式；即通过代理对象访问目标对象。这样做的好处是：可以在目标对象实现的基础上，增强额外的功能操作，即扩展目标对象的功能。这里使用到编程中的一个思想：不要随意去修改别人已经写好的代码或者方法，如果需改修改，可以通过代理的方式来扩展该方法。
- 中介隔离作用：在某些情况下，一个客户类不想或者不能直接引用一个委托对象，而代理对象可以在客户类和委托对象之间起到中介的作用(代理类和委托类实现相同的接口)。
- 开放封闭原则：可以通过给代理类增加额外的功能来扩展委托类的功能，这样只需要修改代理类而不需要再修改委托类，符合开闭原则。代理类本身并不真正实现服务，而是同过调用委托类的相关方法，来提供特定的服务。使用代理模式，可以在调用委托类业务功能的前后加入一些公共的服务(例如鉴权、计时、缓存、日志、事务处理等)，甚至修改委托类的业务功能。


### 2. 代理模式主要角色
- Subject（抽象主题角色）：定义代理类和真实主题的公共对外方法，也是代理类代理真实主题的方法。比如：广告、出售等。
- RealSubject（真实主题角色）：真正实现业务逻辑的类。比如实现了广告、出售等方法的厂家（Vendor）。
- Proxy（代理主题角色）：用来代理和封装真实主题。比如，同样实现了广告、出售等方法的超时（Shop）。

### 3. 代理模式的分类
代理可以分为静态代理和动态代理。
- 静态代理是由程序员编写代理类的源码，再编译代理类。所谓静态也就是在程序运行前就已经存在代理类的字节码文件，代理类和委托类的关系在运行前就已确定。
- 动态代理是代理类的源码是在程序运行期间由编译器动态的生成(如JVM根据反射等机制生成代理类)。代理类和委托类的关系在程序运行时确定。

###  4.静态代理
1. 创建服务类接口
    ```
        // 定义接口
        public interface ShoesStore {
            void sell();
        }
    ```
2. 实现服务接口
    ```
        // 真正的鞋子类
        public class NikeShoesStore implements ShoesStore {
            @Override
            public void sell() {
                System.out.println("卖出了一双Nike鞋子");
            }
        }
    ```
3. 创建代理类
    ```
        //微商 代理
        public class MicroSell implements ShoesStore {
            NikeShoesStore nikeShoesStore;
        
            public MicroSell(NikeShoesStore nikeShoesStore) {
                this.nikeShoesStore = nikeShoesStore;
            }
        
            @Override
            public void sell() {
                beforeSell();
                nikeShoesStore.sell();
                afterSell();
            }
        
            public void beforeSell() {
                System.out.println("买之前宣传：我们的鞋子质量杠杠的，快来买一双吧。");
            }
        
            public void afterSell() {
                System.out.println("买之后推销：欢迎下次光临");
            }
        }
    ```
4. 编写测试类
    ```
        public static void main(String[] args) {
            NikeShoesStore nikeShoes = new NikeShoesStore();
            MicroSell microSell = new MicroSell(nikeShoes);
            microSell.sell();
        }
    ```
![](/images/38455377871e51dc78c2b2c792dc39a9.webp)


**优点：**
可以做到在符合开闭原则的情况下对目标对象进行功能扩展。

**缺点：**
我们得为每一个服务都得创建代理类，工作量太大，不易管理。同时接口一旦发生改变，代理类也得相应修改。 

### 4.JDK动态代理
在JDK动态代理中我们不再需要再手动的创建代理类，我们只需要编写一个动态处理器就可以了。真正的代理对象由JDK再运行时为我们动态的来创建。
1. 改造静态代理的代码为：
    ```
        public class DynamicMicroSell implements InvocationHandler {
            Object shoes;
        
            public DynamicMicroSell(Object shoes) {
                this.shoes = shoes;
            }
        
            @Override
            public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
                beforeSell();
                method.invoke(shoes);
                afterSell();
                return null;
            }
        
            public void beforeSell() {
                System.out.println("买之前宣传：我们的鞋子质量杠杠的，快来买一双吧。");
            }
        
            public void afterSell() {
                System.out.println("买之后推销：欢迎下次光临");
            }
        }
    ```
2. 测试类:
    ```
        public static void main(String[] args) {
            NikeShoesStore realShoes = new NikeShoesStore();
            DynamicMicroSell dynamicMicroSell = new DynamicMicroSell(realShoes);
            ShoesStore nikeProxy = (ShoesStore) Proxy.newProxyInstance(NikeShoesStore.class.getClassLoader(), NikeShoesStore.class.getInterfaces(), dynamicMicroSell);
            nikeProxy.sell();
        }
    ```
![](/images/53941910570c5c4a9f04e4bc5aca4408.webp)


可以看到并没有像静态代理那样重新实现一个代理类，而是实现了 InvocationHandler 接口的invoke方法实现的代理。通过Proxy.newProxyInstance()创建了一个代理类来执行sell方法。
此时如果想要拓展一个阿迪鞋子的接口，很简单：
1. 新建一个AdidasShoes还是实现ShoesStore接口
    ```
        public class AdidasShoes implements ShoesStore {
            @Override
            public void sell() {
                System.out.println("卖出去一双阿迪~");
            }
        }
    ```
2. 测试类:
    ```
        public static void main(String[] args) {
            AdidasShoes adidasShoes = new AdidasShoes();
            DynamicMicroSell dynamicMicroSell1 = new DynamicMicroSell(adidasShoes);
            Shoes shoes = (Shoes) Proxy.newProxyInstance(AdidasShoes.class.getClassLoader(), AdidasShoes.class.getInterfaces(), dynamicMicroSell1);
            shoes.sell();
        }
    ```

**缺点：**
虽然相对于静态代理，动态代理大大减少了我们的开发任务，同时减少了对业务接口的依赖，降低了耦合度。但是还是有一点点小小的遗憾之处，那就是它始终无法摆脱仅支持interface代理，因为它的设计注定了这个遗憾。


### 3.CGLIB代理
##### CGLIB代理的作用
JDK实现动态代理需要实现类通过接口定义业务方法，对于没有接口的类，如何实现动态代理呢，这就需要CGLib了。
[Cglib(Code Generation Library)](https://github.com/cglib/cglib)是个功能强大、高性能、开源的代码生成包，它可以为没有实现接口的类提供代理。运行时在内存中动态生成一个子类对象从而实现对目标对象功能的扩展。
CGLib采用了非常底层的字节码技术，其原理是通过字节码技术为一个类创建子类，并在子类中采用方法拦截的技术拦截所有父类方法的调用，顺势织入横切逻辑。
但因为采用的是继承，所以不能对final修饰的类进行代理。JDK动态代理与CGLib动态代理均是实现Spring AOP的基础。
Cglib动态代理的特点如下：

- 需要引入Cglib的jar文件。
- CGLIB是一个强大的高性能的代码生成包，它可以在运行期扩展Java类与实现Java接口。
它广泛的被许多AOP的框架使用，例如Spring AOP和dynaop，为他们提供方法的interception（拦截）。
- CGLIB包的底层是通过使用一个小而快的字节码处理框架ASM，来转换字节码并生成新的类。
不鼓励直接使用ASM，因为它需要你对JVM内部结构包括class文件的格式和指令集都很熟悉。
- 委托类不能为final，否则报错java.lang.IllegalArgumentException: Cannot subclass final class xxx。
- 不会拦截委托类中无法重载的final/static方法，而是跳过此类方法只代理其他方法。

##### cglib与JDK动态代理的区别
- 使用动态代理的对象必须实现一个或多个接口
- 使用cglib代理的对象则无需实现接口，达到代理类无侵入。

### 4. 动态代理在AOP中的应用
AOP（Aspect Orient Programming），我们一般称为面向方面（切面）编程，作为面向对象的一种补充，用于处理系统中分布于各个模块的横切关注点，比如事务管理、日志、缓存等等。
AOP可以两种动态代理来实现拦截切入功能：jdk动态代理和cglib动态代理。两种方法同时存在，各有优劣。 jdk动态代理是由java内部的反射机制来实现的，cglib动态代理底层则是借助asm来实现的。 
总的来说，反射机制在生成类的过程中比较高效，执行时候通过反射调用委托类接口方法比较慢；而asm在生成类之后的相关代理类执行过程中比较高效（可以通过将asm生成的类进行缓存，这样解决asm生成类过程低效问题）。 
还有一点必须注意：jdk动态代理的应用前提，必须是委托类基于统一的接口。如果没有上述前提，jdk动态代理不能应用。 由此可以看出，jdk动态代理有一定的局限性，cglib这种第三方类库实现的动态代理应用更加广泛，且在效率上更有优势。

AOP实现主要分为 静态代理 和 动态代理 。
- 静态代理 主要是 AspectJ
- 动态代理 主要是 Spring AOP



# 五. 观察者模式
### 1. 概念
观察者模式（Observer），又叫发布-订阅模式（Publish/Subscribe），定义对象间一种一对多的依赖关系，使得每当一个对象改变状态，则所有依赖于它的对象都会得到通知并自动更新。
被观察者和观察者一般是一对多的关系，一个被观察者对应多个观察者，当一个被观察者的状态发生改变时，被观察者通知观察者， 然后可以在观察者内部 进行业务逻辑的处理。

#### 2. 观察者模式的主要角色
**Subject（抽象的被观察者）**
是一个接口（实际上也有人使用抽象类），主要包含了3个方法：
1. addObserver方法可以添加观察者对象，可以理解为观察者把自己注册到了被观察者这里，只有注册了的观察者，才能接到被观察者的通知。
2. deleteObserver方法是将观察者移除，被移除的观察者自然就不能再接到通知了。
3. notifyObserves方法可以把通知发送给所有的已注册的观察者，至于观察者们后续做什么事情，被观察者是完全不关心的。

**Observer（抽象的观察者）**
也是一个接口，必须实现的只有一个通知方法，被观察者通过调用这个方法，让观察者了解到事件的发生。

**ConcreteSubject（被观察者的具体实现）**
实现抽象被观察者接口，是被观察者的具体业务逻辑，另外还需要一个存储观察者的集合。当主题的内部状态改变时，向所有集合中的观察者发出通知。

**ConcreteObserver（观察者的具体实现）**
实现抽象观察者接口，处理不同具体观察者的不同业务逻辑。

#### 3. 代码实现:
1. 抽象的被观察者:
    ```
        /**
         * 被观察者观察者抽象接口（发布者、被观察者）
         */
        public interface Observerable {
            /**
             * 注册观察者
             */
            void addObserver(Observer observer);
        
            /**
             * 移除观察者
             */
            void deleObserver(Observer observer);
        
            /**
             * 通知观察者
             */
            void notifyObserver();
        }
    ```
2. 抽象的观察者:
    ```
        /**
         * 观察者抽象接口
         */
        public interface Observer {
            /**
             * 接收变动通知
             */
            void upData(String message);
        }
        
    ```
3. 被观察者的具体实现:
    ```
        public class NewServer implements Observerable {
            private List<Observer> mObservers = new ArrayList<>();
            private String news;
        
            @Override
            public void addObserver(Observer observer) {
                mObservers.add(observer);
            }
        
            @Override
            public void deleObserver(Observer observer) {
                mObservers.remove(observer);
            }
        
            @Override
            public void notifyObserver() {
                for (Observer mObserver : mObservers) {
                    mObserver.upData(news);
                }
            }
        
            public void setNews(String news) {
                this.news = news;
                notifyObserver();
            }
        }
    ```
4. 观察者的具体实现:
    ```
        public class User implements Observer {
            private String name;
        
            public User(String name) {
                this.name = name;
            }
        
            @Override
            public void upData(String news) {
                System.out.println("我是观察者" + name + "我收到的消息是:" + news);
            }
        }
    ```
5. 测试类:
    ```
        public static void main(String[] args) {
            NewServer wechatServer = new NewServer();
            User user = new User("张三");
            User user1 = new User("李四");
            User user2 = new User("王五");
            wechatServer.addObserver(user);
            wechatServer.addObserver(user1);
            wechatServer.addObserver(user2);
            wechatServer.setNews("国乒勇夺冠军!");
            wechatServer.deleObserver(user1);
            wechatServer.setNews("国足惨遭淘汰!");
        }
    ```
结果:
![](/images/79addbe1cf33317966bc0226d24fb3a8.webp)
#### 4. 优点
- 观察者和被观察者之间建立一个抽象的耦合，降低了目标与观察者之间的耦合关系。
- 观察者模式支持广播通讯的触发机制。

#### 5. 缺点
- 如果一个被观察者对象有很多的直接和间接的观察者的话，将所有的观察者都通知到会花费很多时间。
- 如果观察者和观察目标间有循环依赖，可能导致系统崩溃。
- 没有相应的机制让观察者知道所观察的目标对象是怎么发生变化的。
#### 6. 使用场景
- 关联行为场景。
- 事件多级触发场景。
- 跨系统的消息变换场景，如消息队列的处理机制。




参考资料:
[Android开发之设计模式-适配器模式](https://blog.csdn.net/yun382657988/article/details/82991964)
[Android 适配器模式(ListView与Adapter)](https://www.jianshu.com/p/fb558642823e)
[android设计模式二十三式（七）——装饰器模式（Decorator）](https://blog.csdn.net/CSDN_xiaoxiaocainiao/article/details/90256847)
[谈谈 23 种设计模式在 Android 项目中的应用](https://juejin.cn/post/6844903638503161870#heading-110)
