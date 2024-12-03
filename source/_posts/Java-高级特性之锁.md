---
title: Java-高级特性之锁
date: 2016-12-11
categories: 
  - Java开发
---

Java多线程开发中，如果涉及到共享资源操作场景，那就必不可少要和Java锁打交道。

Java中的锁机制主要分为Lock和Synchronized，本文主要分析Java锁机制的使用和实现原理，按照Java锁使用、JDK中锁实现、系统层锁实现的顺序来进行分析，话不多说，let's go~

Java锁使用
在Lock接口出现之前，Java程序是靠synchronized关键字实现锁功能的，而JavaSE 5之后，并发包中新增了Lock接口（以及相关实现类）用来实现锁功能，它提供了与synchronized关键字类似的同步功能，只是在使用时需要显式地获取和释放锁。虽然它缺少了（通过synchronized块或者方法）隐式获取释放锁的便捷性，但是却拥有了锁获取与释放的可操作性、可中断的获取锁以及超时获取锁等多种synchronized关键字所不具备的同步特性。

Java锁使用示例：

Lock lock = new ReentrantLock();  
lock.lock();  
try {  
// ..
} finally {
lock.unlock();
}
注意：在finally块中释放锁，目的是保证在获取到锁之后，最终能够被释放。不要将获取锁的过程写在try块中，因为如果在获取锁（自定义锁的实现）时发生了异常，异常抛出的同时，会提前进行unlock导致IllegalMonitorStateException异常。

Lock相较于Synchronized优势如下：

可中断获取锁：使用synchronized关键字获取锁的时候，如果线程没有获取到被阻塞了，那么这个时候该线程是不响应中断(interrupt)的，而使用Lock.lockInterruptibly()获取锁时被中断，线程将抛出中断异常。
可非阻塞获取锁：使用synchronized关键字获取锁时，如果没有成功获取，只有被阻塞，而使用Lock.tryLock()获取锁时，如果没有获取成功也不会阻塞而是直接返回false。
可限定获取锁的超时时间：使用Lock.tryLock(long time, TimeUnit unit)。
同一个所对象上可以有多个等待队列（Conditin，类似于Object.wait()，支持公平锁模式）。
Lock除了更多的功能之外，有一个很大的优势：synchronized的同步是jvm底层实现的，对一般程序员来说程序遇到出乎意料的行为的时候，除了查官方文档几乎没有别的办法；而显示锁除了个别操作用了底层的Unsafe类(LockSupport封装了Unsafe类)之外，几乎都是用java语言实现的，我们可以通过学习显示锁的源码，来更加得心应手的使用显示锁。

当然，Lock也不是完美的，否则java就不会保留着synchronized关键字了，显示锁的缺点主要有两个：

使用比较复杂，这点之前提到了，需要手动加锁，解锁，而且还必须保证在异常状态下也要能够解锁。而synchronized的使用就简单多了。
效率较低，synchronized关键字毕竟是jvm底层实现的，因此用了很多优化措施来优化速度(偏向锁、轻量锁等)，而显示锁的效率相对低一些。
Synchronized
Synchronized在JVM里的实现是基于进入和退出Monitor对象来实现方法同步和代码块同步的。monitorenter指令是在编译后插入到同步代码块的开始位置，而monitorexit是插入到方法结束处和异常处，JVM要保证每个monitorenter必须有对应的monitorexit与之配对。任何对象都有一个monitor与之关联，当且一个monitor被持有后，它将处于锁定状态。线程执行到monitorenter指令时，将会尝试获取对象所对应的monitor的所有权，即尝试获得对象的锁。

synchronized用的锁是存在Java对象头里的。如果对象是数组类型，则虚拟机用3个字宽（Word）存储对象头，如果对象是非数组类型，则用2字宽存储对象头。






Synchronized和Lock
其实我们真正用到的锁也就那么两三种，只不过依据设计方案和性质对其进行了大量的划分。

以下一个锁是原生语义上的实现



Synchronized，它就是一个：非公平，悲观，独享，互斥，可重入的重量级锁

以下两个锁都在JUC包下，是API层面上的实现

ReentrantLock，它是一个：默认非公平但可实现公平的，悲观，独享，互斥，可重入，重量级锁。

ReentrantReadWriteLocK，它是一个，默认非公平但可实现公平的，悲观，写独享，读共享，读写，可重入，重量级锁。








# 一、锁的种类
锁作为并发共享数据，保证一致性的工具，在JAVA平台有多种实现(如 synchronized 和 ReentrantLock等等 ) 。这些已经写好提供的锁为开发提供了便利，但是锁的具体性质以及类型却很少被提及。Java 锁的分类没有严格意义的规则，我们常说的分类一般都是依据锁的特性、锁的设计、锁的状态等进行归纳整理的。平时大家听到用到的锁有很多种：公平锁/非公平锁、可重入锁/不可重入锁、共享锁/排他锁、乐观锁/悲观锁、分段锁、偏向锁/轻量级锁/重量级锁、自旋锁。这些都是在不同维度或者锁优化角度对锁的一种叫法，我们在程序中用到的也就那么几种，比如``synchronized，ReentrantLock，ReentrantReadWriteLock。``

锁的分类
- 从各种锁的设计，抽象出的概览思想可以分为 悲观锁 和 乐观锁。
- 根据线程获取锁的抢占机制，和锁的公平性又可以分为公平锁 和 非公平锁。
- 从根据锁是否重复获取可以分为 可重入锁 和 不可重入锁。
- 根据锁能否被多个线程持有，可以把锁分为独占锁(排他锁)和共享锁。
- 根据Synchronized锁升降级的状态可以分为 偏向锁 / 轻量级锁 / 重量级锁。
- 从资源已被锁定，获取锁的阻塞装填可以分为 自旋锁。
- 从对使用锁的粒度设计而言可以分为 分段锁。

#### 1.乐观锁/悲观锁
- **悲观锁的概念：**总是假设最坏的情况，每次拿数据都认为别人会修改数据，所以要加锁，别人只能等待，直到我释放锁才能拿到锁；数据库的行锁、表锁、读锁、写锁都是这种方式。java中的synchronized和Lock的实现类也是悲观锁的思想。

- **乐观锁的概念：**总是假设最好的情况，每次拿数据都认为别人不会修改数据，所以不会加锁，但是更新的时候，会判断在此期间有没有人修改过；一般基于版本号机制实现。java中的乐观锁最常见的是CAS算法。

乐观锁和悲观锁的应用场景：
- 乐观锁适用于读多写少的情况，因为不加锁直接读可以让系统的性能大幅度的提高 。
- 悲观锁适用于写多读少的情况，因为等待到锁被释放后，可以立即获得锁进行操作。

#### 2.公平锁/非公平锁

- **公平锁：**指多个线程在等待同一个锁时，必须按照申请锁的先后顺序来一次获得锁。

- **非公平锁：**指多个线程获取锁的顺序并不是按照申请锁的顺序，有可能后申请的线程比先申请的线程优先获取锁。

公平锁的好处是等待锁的线程不会饿死，但是整体效率相对低一些；非公平锁的好处是整体效率相对高一些，但是有些线程可能会饿死或者说很早就在等待锁，但要等很久才会获得锁。其中的原因是公平锁是严格按照请求所的顺序来排队获得锁的，而非公平锁时可以抢占的，即如果在某个时刻有线程需要获取锁，而这个时候刚好锁可用，那么这个线程会直接抢占，而这时阻塞在等待队列的线程则不会被唤醒。
- 在java中，公平锁可以通过new ReentrantLock(true)来实现；非公平锁可以通过new ReentrantLock(false)或者默认构造函数new ReentrantLock()实现。

- synchronized是非公平锁，并且它无法实现公平锁。

#### 3.可重入锁/不可重入锁
- **可重入锁：**又名递归锁，直指同一个线程在外层方法获得锁之后，在进入内层方法时，会自动获得锁。ReentrantLock和Synchronized都是可重入锁。可重入锁的好处之一就是在一定程度上避免死锁。

- **不可重入锁：**就是不可重复调用的锁，在外面方法使用锁之后，在里面就不能使用锁了，这个时候锁会阻塞直到你外面的锁释放后才会获得里面的锁。会产生死锁这种情况 。

#### 4. 独享锁/共享锁
- **独享锁：**是指该锁一次只能被一个线程持有；

- **共享锁：**指该锁可以被多个线程持有；

对于Java ReentrantLock而言，其是独享锁。但是对于Lock的另一个实现类ReentrantReadWriteLock，其读锁是共享锁，其写锁是独享锁。读锁的共享锁可保证并发读是非常高效的，读写，写读 ，写写的过程是互斥的。独享锁与共享锁也是通过AQS来实现的，通过实现不同的方法，来实现独享或者共享。对于Synchronized而言，当然是独享锁。

- **轻量级锁：**当偏向锁

#### 5. 偏向锁/轻量级锁/重量级锁
- **偏向锁：**Java偏向锁是java6引入的一项多线程优化。偏向锁，顾名思义，它会偏向第一个访问锁的线程，如果在运行过程中，同步锁只有一个线程访问，不存在多线程争用的情况，则线程是不需要触发同步的，这种情况下，就会给线程加一个偏向锁，它通过消除资源无竞争情况下的同步原语，进一步提高了程序的运行性能。如果在运行过程中，遇到了其他线程抢占锁，则持有偏向锁的线程会被挂起，JVM就会消除它身上的偏向锁，将锁恢复到标准的轻量级锁。
  不满足，也就是有多线程并发访问，锁定同一个对象的时候，先提升为轻量级锁。也是使用标记 ACC_SYNCHRONIZED 标记记录的。ACC_UNSYNCHRONIZED 标记记录未获取到锁信息的线程。就是只有两个线程争抢锁标记的时候，优先使用轻量级锁。（自旋锁）当获取锁的过程中，未获取到。为了提高效率，JVM 自动执行若干次空循环，再次申请锁，而不是进入阻塞状态的情况。称为自旋锁。自旋锁提高效率就是避免线程状态的变更

- **重量级锁：**在自旋过程中，为了避免无用的自旋(比如获得锁的线程被阻塞住了)，锁就会被升级为重量级锁。在重量级锁的状态下，其他线程视图获取锁的时候都会被阻塞住，只有持有锁的线程释放锁之后才会唤醒那些阻塞的线程，这些线程就开始竞争锁。

#### 6. 自旋锁（java.util.concurrent包下的几乎都是利用锁）

- **自旋锁：**在Java中，自旋锁是指尝试获取锁的线程不会立即阻塞，而是采用循环的方式去尝试获取锁，这样的好处是减少线程上下文切换的消耗，缺点是循环会消耗CPU。

  自旋锁原理非常简单，如果持有锁的线程能在很短时间内释放锁资源，那么那些等待竞争锁的线程就不需要做内核态和用户态之间的切换进入阻塞挂起状态，它们只需要等一等（自旋），等持有锁的线程释放锁后即可立即获取锁，这样就避免用户线程和内核的切换的消耗。

  自旋锁尽可能的减少线程的阻塞，适用于锁的竞争不激烈，且占用锁时间非常短的代码块来说性能能大幅度的提升，因为自旋的消耗会小于线程阻塞挂起再唤醒的操作的消耗

  但是如果锁的竞争激烈，或者持有锁的线程需要长时间占用锁执行同步块，这时候就不适合使用自旋锁了，因为自旋锁在获取锁前一直都是占用cpu做无用功，同时有大量线程在竞争一个锁，会导致获取锁的时间很长，线程自旋的消耗大于线程阻塞挂起操作的消耗，其它需要cpu的线程又不能获取到cpu，造成cpu的浪费。

#### 7.分段锁
- **分段锁：**分段锁是对锁的一种优化，就是将锁细分的粒度更多，比如将一个数组的每个位置当做单独的锁。JDK8以前ConcurrentHashMap就使用了锁分段技术，它将散列数组分成多个Segment，每个Segment存储了实际的数据，访问数据的时候只需要对数据所在的Segment加锁就行。

# 二、Java锁的实现

本文章主要讲的是Java多线程加锁机制，有两种：
- Synchronized(隐式锁)
- Lock(显式锁)

# 三、Synchronized
synchronized是在JVM层面上实现的，不但可以通过一些监控工具监控synchronized的锁定，而且在代码执行时出现异常，JVM会自动释放锁定。Synchronized是一个：非公平，悲观，独享，互斥，可重入的重量级锁。表现形式为：``同步代码块``和``同步方法``。在JDK1.5之前都是使用synchronized关键字保证同步的，它可以把任意一个非NULL的对象当作锁。

- 作用于方法时，锁住的是对象的实例(this)；
- 当作用于静态方法时，锁住的是Class实例，又因为Class的相关数据存储在永久带PermGen（jdk1.8则是metaspace），永久带是全局共享的，因此静态方法锁相当于类的一个全局锁，会锁所有调用该方法的线程；
- synchronized作用于一个对象实例时，锁住的是所有以该对象为锁的代码块。


### 1. 同步代码块
```
synchronized(对象)
{
	需要被同步的代码
}
```
对象如同锁，持有锁的线程可以执行同步代码。
没有持有锁的线程即使获取cpu的执行权，也进不去执行同步代码，因为没有获取锁。
``同步的前提：``
-  必须要有两个或者两个以上的线程。
-  必须是多个线程使用同一个锁。

``原理:``同步代码块保证了同步中只能有一个线程在运行，因此解决了安全的问题。

``好处：``解决了多线程的安全问题。
``弊端：``多个线程需要判断锁，较为消耗资源。

### 2. 同步函数
```
public synchronized void show()
{
	需要被同步的代码		
}
```
函数需要被对象调用。那么函数都有一个所属对象引用。就是this。所以同步函数使用的锁是this对象。

如果同步函数被静态修饰后:
```
public static synchronized void show()
{
	需要被同步的代码	
}
```
锁不再是this。因为静态方法中也不可以定义this。静态函数里，内存中没有本类对象，但是一定有该类对应的字节码文件对象。因此:静态的同步方法，使用的锁是该方法所在类的字节码文件对象,类名.class

### 3. 死锁问题。

多线程中要进行资源的共享,就需要同步,但是同步过多,就可能造成死锁的问题。
产生原因:同步中嵌套同步。
```
public class DaneLock {
    public static void main(String[] args) {
        DieLock d1=new DieLock(true);
        DieLock d2=new DieLock(false);
        Thread t1=new Thread(d1);
        Thread t2=new Thread(d2);
        t1.start();
        t2.start();
    }
}
class MyLock{
    public static Object obj1=new Object();
    public static Object obj2=new Object();
}
class DieLock implements Runnable{
    private boolean flag;
    DieLock(boolean flag){
        this.flag=flag;
    }
    public void run() {
        if(flag) {
            while(true) {
                synchronized(MyLock.obj1) {
                    System.out.println(Thread.currentThread().getName()+"....if...obj1...");
                    synchronized(MyLock.obj2) {
                        System.out.println(Thread.currentThread().getName()+".....if.....obj2.....");

                    }
                }
            }
        }
        else {
            while(true){
                synchronized(MyLock.obj2) {
                    System.out.println(Thread.currentThread().getName()+"....else...obj2...");
                    synchronized(MyLock.obj1) {
                        System.out.println(Thread.currentThread().getName()+".....else.....obj1.....");
                    }
                }
            }
        }
    }
}
```
产生死锁的条件：

- 互斥条件：指进程对所分配到的资源进行排它性使用，即在一段时间内某资源只由一个进程占用。如果此时还有其它进程请求资源，则请求者只能等待，直至占有资源的进程用毕释放。

- 请求和保持条件：指进程已经保持至少一个资源，但又提出了新的资源请求，而该资源已被其它进程占有，此时请求进程阻塞，但又对自己已获得的其它资源保持不放。

- 不剥夺条件：进程已获得的资源，在未使用完之前，不能被剥夺，只能在使用完时由自己释放。

- 环路等待条件：指在发生死锁时，必然存在一个进程——资源的环形链，即进程集合{P0，P1，P2，···，Pn}中的P0正在等待一个P1占用的资源；P1正在等待P2占用的资源，……，Pn正在等待已被P0占用的资源。

预防死锁：破坏四个必要条件中的一个或多个。

# 四、Lock
与synchronized不同的是，Lock锁是纯Java实现的，与底层的JVM无关。在java.util.concurrent.locks包中有很多Lock的实现类，常用的有ReentrantLock、ReadWriteLock（实现类ReentrantReadWriteLock），其实现都依赖java.util.concurrent.AbstractQueuedSynchronizer类（简称AQS）




```
public interface Lock {

    /**
     * 获取锁，调用该方法的线程会获取锁，当获取到锁之后会从该方法但会
     */
    void lock();

    /**
     * 可响应中断。即在获取锁的过程中可以中断当前线程
     */
    void lockInterruptibly() throws InterruptedException;

    /**
     * 尝试非阻塞的获取锁，调用该方法之后会立即返回，如果获取到锁就返回true否则返回false
     */
    boolean tryLock();

    /**
     * 超时的获取锁，下面的三种情况会返回
     * ①当前线程在超时时间内获取到了锁
     * ②当前线程在超时时间内被中断
     * ③超时时间结束，返回false
     */
    boolean tryLock(long time, TimeUnit unit) throws InterruptedException;

    /**
     * 释放锁
     */
    void unlock();

    /**
     * 获取等待通知组件，该组件和当前锁绑定，当前线程只有获取到了锁才能调用组件的wait方法，调用该方法之后会释放锁
     */
    Condition newCondition();
}
```

• void lock() 获取锁,调用该方法当前线程将会获取锁，当锁获取后，该方法将返回。
• void lockInterruptibly() throws InterruptedException 可中断获取锁，与lock()方法不同之处在于该方法会响应中断，即在锁的获取过程中可以中断当前线程
• boolean tryLock() 尝试非阻塞的获取锁，调用该方法立即返回，true表示获取到锁
• boolean tryLock(long time,TimeUnit unit) throws InterruptedException 超时获取锁，以下情况会返回：时间内获取到了锁，时间内被中断，时间到了没有获取到锁。
• void unlock() 释放锁


1. ReentrantLock，它是一个：默认非公平但可实现公平的，悲观，独享，互斥，可重入，重量级锁。
2. ReentrantReadWriteLocK，它是一个，默认非公平但可实现公平的，悲观，写独享，读共享，读写，可重入，重量级锁。
### 1. ReentrantLock
ReentrantLock是Lock接口一种常见的实现，它是支持重进入的锁即表示该锁能够支持一个线程对资源的重复加锁。该锁还支持获取锁时的公平与非公平的选择。

``特性``
公平性：支持公平锁和非公平锁。默认使用了非公平锁。
可重入
可中断：相对于 synchronized，它是可中断的锁，能够对中断作出响应。
超时机制：超时后不能获得锁，因此不会造成死锁。
ReentrantLock 是一个独占/排他锁。相对于 synchronized，它更加灵活。但是需要自己写出加锁和解锁的过程。它的灵活性在于它拥有很多特性。

> ReentrantLock 需要显示地进行释放锁。特别是在程序异常时，synchronized 会自动释放锁，而 ReentrantLock 并不会自动释放锁，所以必须在 finally 中进行释放锁。

它的特性：

*   公平性：支持公平锁和非公平锁。默认使用了非公平锁。
*   可重入
*   可中断：相对于 synchronized，它是可中断的锁，能够对中断作出响应。
*   超时机制：超时后不能获得锁，因此不会造成死锁。

ReentrantLock 是很多类的基础，例如 ConcurrentHashMap 内部使用的 Segment 就是继承 ReentrantLock，CopyOnWriteArrayList 也使用了 ReentrantLock。

### 2. ReentrantReadWriteLock

它拥有读锁(ReadLock)和写锁(WriteLock)，读锁是一个共享锁，写锁是一个排他锁。

它的特性：

*   公平性：支持公平锁和非公平锁。默认使用了非公平锁。
*   可重入：读线程在获取读锁之后能够再次获取读锁。写线程在获取写锁之后能够再次获取写锁，同时也可以获取读锁（锁降级）。
*   锁降级：先获取写锁，再获取读锁，然后再释放写锁的过程。锁降级是为了保证数据的可见性。
使用ReentrantLock必须在finally控制块中进行解锁操作。

在资源竞争不激烈的情形下，性能稍微比synchronized差点点。但是当同步非常激烈的时候，synchronized的性能一下子能下降好几十倍，而ReentrantLock确还能维持常态。

高并发量情况下使用ReentrantLock。


在Java中，我们一般会有下面这么几种办法来实现线程安全问题：

- 无状态(没有共享变量)

- 使用final使该引用变量不可变(如果该对象引用也引用了其他的对象，那么无论是发布或者使用时都需要加锁)

- 加锁(内置锁，显示Lock锁)

- 使用JDK为我们提供的类来实现线程安全(此部分的类就很多了)

- 原子性（就比如上面的count++操作，可以使用AtomicLong来实现原子性，那么在增加的时候就不会出差错了！)

- 容器(ConcurrentHashMap等等…)








方法三：使用线程本地存储ThreadLocal。当多个线程操作同一个变量且互不干扰的场景下，可以使用ThreadLocal来解决。它会在每个线程中对该变量创建一个副本，即每个线程内部都会有一个该变量，且在线程内部任何地方都可以使用，线程之间互不影响，这样一来就不存在线程安全问题，也不会严重影响程序执行性能。在很多情况下，ThreadLocal比直接使用synchronized同步机制解决线程安全问题更简单，更方便，且结果程序拥有更高的并发性。通过set(T value)方法给线程的局部变量设置值；get()获取线程局部变量中的值。当给线程绑定一个 Object 内容后，只要线程不变,就可以随时取出；改变线程,就无法取出内容.。这里提供一个用法示例：
```
public class ThreadLocalTest {
private static int a = 500;
public static void main(String[] args) {
new Thread(()->{
ThreadLocal<Integer> local = new ThreadLocal<Integer>();
while(true){
local.set(++a);   //子线程对a的操作不会影响主线程中的a
try {
Thread.sleep(1000);
} catch (InterruptedException e) {
e.printStackTrace();
}
System.out.println("子线程："+local.get());
}
}).start();
a = 22;
ThreadLocal<Integer> local = new ThreadLocal<Integer>();
local.set(a);
while(true){
try {
Thread.sleep(1000);
} catch (InterruptedException e) {
e.printStackTrace();
}
System.out.println("主线程："+local.get());
}
}
}
```

ThreadLocal线程容器保存变量时，底层其实是通过ThreadLocalMap来实现的。它是以当前ThreadLocal变量为key ，要存的变量为value。获取的时候就是以当前ThreadLocal变量去找到对应的key，然后获取到对应的值。源码参考如下：
```
public void set(T value) {
Thread t = Thread.currentThread();
ThreadLocalMap map = getMap(t);
if (map != null)
map.set(this, value);
else
createMap(t, value);
}
ThreadLocalMap getMap(Thread t) {
return t.threadLocals; //ThreadLocal.ThreadLocalMap threadLocals = null;Thread类中声明的
}
void createMap(Thread t, T firstValue) {
t.threadLocals = new ThreadLocalMap(this, firstValue);
}
```
观察源码就会发现，其实每个线程Thread内部有一个ThreadLocal.ThreadLocalMap类型的成员变量threadLocals，这个threadLocals就是用来存储实际的变量副本的，键值为当前ThreadLocal变量，value为变量副本（即T类型的变量）。

初始时，在Thread里面，threadLocals为空，当通过ThreadLocal变量调用get()方法或者set()方法，就会对Thread类中的threadLocals进行初始化，并且以当前ThreadLocal变量为键值，以ThreadLocal要保存的副本变量为value，存到threadLocals。

然后在当前线程里面，如果要使用副本变量，就可以通过get方法在threadLocals里面查找即可。



[Java锁机制了解一下](https://juejin.cn/post/6844903598011187208)
[](https://segmentfault.com/a/1190000038320670)
[Java进阶（二）当我们说线程安全时，到底在说什么](http://www.jasongj.com/java/thread_safe/)