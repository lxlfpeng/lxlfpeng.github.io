---
title: Java多线程模型及线程安全问题总结
---

# 一.线程和进程
### 1.什么是进程
进程是系统中正在运行的一个程序，程序一旦运行就是进程。进程可以看成程序执行的一个实例。进程是系统资源分配的独立实体，每个进程都拥有独立的地址空间。一个进程无法访问另一个进程的变量和数据结构，如果想让一个进程访问另一个进程的资源，需要``使用进程间通信``，比如``管道，文件，套接字``等。

### 2.什么是线程
线程从属于进程，是程序的实际执行者。一个进程至少包含一个主线程，也可以有更多的子线程。

### 3.进程和线程的区别与联系
- 线程是进程的一部分，一个线程只能属于一个进程，而一个进程可以有多个线程，但至少有一个线程。
- 资源分配给进程，同一进程的所有线程共享该进程的所有资源。
- 虚拟机分给线程，即真正在虚拟机上运行的是线程。
- 线程在执行过程中，需要协作同步。不同进程的线程间要利用消息通信的办法实现同步。

# 二.Java线程的创建
Java中线程的创建常见有如下三种基本形式:
### 1.继承Thread类，重写该类的run()方法
```
public class MyThread extends Thread {
    @Override
    public void run() {
        super.run();
        for (; ; ) {
            System.out.println(Thread.currentThread().getName());
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}
```
```
public class Main {
    public static void main(String[] args) {
        MyThread myThread = new MyThread();
        myThread.start();
    }
}
```
**start()和run()区别**:run没有另起线程，而start才是真正意义的新开线程。

### 2.实现Runnable接口，并重写该接口的run()方法
```
public class MyRunnable implements Runnable {
    @Override
    public void run() {
        for (; ; ) {
            System.out.println(Thread.currentThread().getName());
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}
```
```
public class Main {
    public static void main(String[] args) {
            MyRunnable myRunnable = new MyRunnable();
            Thread thread = new Thread(myRunnable);
            thread.start();
    }
}
```

>实现Rnnable接口的好处在于:避免了单继承的局限性。 在定义线程时，建议使用实现Rnnable方式。

### 3.通过线程池启动多线程
线程池，其实就是一个容纳多个线程的容器，其中的线程可以反复使用，省去了频繁创建线程对象的操作，无需反复创建线程而消耗过多资源。

# 三.Java线程池
### 1.线程池的定义
直接创建线程的话，每个线程都要通过new Thread(xxRunnable).start()的方式来创建并运行一个线程，线程少的话这不会是问题，而真实环境可能会开启多个线程让系统和程序达到最佳效率，当线程数达到一定数量就会耗尽系统的CPU和内存资源，也会造成GC频繁收集和停顿，因为每次创建和销毁一个线程都是要消耗系统资源的，如果为每个任务都创建线程这无疑是一个很大的性能瓶颈。如果线程数量多的话，频繁的创建和销毁线程会大大浪费时间和效率，更重要的是浪费内存，因为正常来说线程执行完毕后死亡，线程对象就会变成垃圾。为了解决这个问题在Java中引入了线程池技术。
谈到线程池就会想到池化技术，其中最核心的思想就是把宝贵的资源放到一个池子中；每次使用都从里面获取，用完之后又放回池子供其他人使用。ThreadPoolExecutor可以减少销毁和创建的次数，每个工作线程可以重复利用，可执行多个任务。

### 2.Java四种线程池的使用
![](https://upload-images.jianshu.io/upload_images/3067896-a98e011c492b9cb2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
JDK为我们封装了一套操作多线程的框架Executors，帮助我们可以更好的控制线程池，Executors下提供了一些线程池的工厂方法：Java通过Executors提供四种线程池，分别为：
##### (1.)newFixedThreadPool
创建固定长度的线程池，线程池中的线程数量是固定的。超出的线程会在队列中等待。每次提交一个任务就创建一个线程，直到线程达到线程池的最大大小，线程池的大小一旦达到最大值就会保持不变。如果某个线程因为执行异常而结束，线程池会补充一个新的线程。
```
ExecutorService fixedThreadPool = Executors.newFixedThreadPool(3);
       for (int i = 0; i < 10; i++) {
           fixedThreadPool.execute(new Runnable() {
               @Override
               public void run() {
                   System.out.println(Thread.currentThread().getName());
               }
           });
       }
```
执行结果
```
pool-1-thread-2
pool-1-thread-1
pool-1-thread-3
pool-1-thread-2
pool-1-thread-3
pool-1-thread-3
pool-1-thread-1
pool-1-thread-3
pool-1-thread-2
pool-1-thread-1
```
这里限制了线程池里最多有3 个线程，哪怕有 10 个任务需要执行，也只有 1-3 这 3 个线程可以运行。

**缺点**：不支持自定义拒绝策略，大小固定，难以扩展。
##### (2.)newCacheThreadPool
创建的是一个大小无界的缓冲线程池。它的任务队列是一个同步队列。任务加入到池中，如果池中有空闲线程，则用空闲线程执行，如无则创建新线程执行。池中的线程空闲时间超过60秒，将被销毁释放。线程数随任务的多少变化。适用于执行耗时较小的异步任务。池的核心线程数=0，最大线程=Integer.MAX_VALUE
创建一个可缓存的线程池，如果线程池的大小超过了处理任务所需要的线程数，那么就会回收部分空闲(60秒不执行任务)的线程；当任务数增加时，此线程池又可以智能的添加新线程来处理任务。此线程池不会对线程池大小做限制，线程池大小完全依赖于操作系统(或JVM)能够创建的最大线程大小。
```
ExecutorService cachedThreadPool = Executors.newCachedThreadPool();
for (int i = 0; i < 10; i++) {
    final int index = i;
    try {
        Thread.sleep(index * 1000);
    } catch (InterruptedException e) {
        e.printStackTrace();
    }

    cachedThreadPool.execute(new Runnable() {

        @Override
        public void run() {
            System.out.println(index);
        }
    });
}
```
**缺点**：一旦线程无限增长，会导致内存溢出。
##### (3.)newSingleThreadExecutor
创建一个单线程的线程池，这个线程池只有一个线程在工作，也就是串行执行所有任务。如果这个唯一的线程因为异常结束，那么会有一个新的线程来替代它。此线程池保证所有任务的执行顺序按照任务的提交顺序执行。
```
ExecutorService singleThreadExecutor = Executors.newSingleThreadExecutor();
for (int i = 0; i < 10; i++) {
    final int index = i;
    singleThreadExecutor.execute(new Runnable() {

        @Override
        public void run() {
            try {
                System.out.println(index);
                Thread.sleep(2000);
            } catch (InterruptedException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
        }
    });
}
```
##### (4.)newScheduledThreadPool
创建一个定长线程池，支持定时及周期性任务执行。
```
ScheduledExecutorService scheduledThreadPool = Executors.newScheduledThreadPool(5);
scheduledThreadPool.schedule(new Runnable() {

    @Override
    public void run() {
        System.out.println("delay 3 seconds");
    }
}, 3, TimeUnit.SECONDS);
```
**缺点**：任务是单线程方式执行，一旦一个任务失败其他任务也受影响。

### 3.ThreadPoolExecutor类
这四种线程池实际调用的还是ThreadPoolExecutor的构造方法。Executors实际上调用的是ThreadPoolExecutor的构造方法(newScheduledThreadPool调用的是ScheduleThreadPoolExecutor的构造)，我们看一下ThreadPoolExecutor参数最多的构造
```
public ThreadPoolExecutor(int corePoolSize,//线程核心线程数。线程池长期维持的线程数，即使线程处于idle状态也不会回收
                              int maximumPoolSize,//线程允许的最大线程数
                              long keepAliveTime,//空闲线程存活时间。当前线程池总数大于核心线程数时，终止多余的空闲线程的时间
                              TimeUnit unit,//销毁时间。超过这个时间，多余的线程会被回收
                              BlockingQueue<Runnable> workQueue,//存储等待执行线程的工作队列
                              ThreadFactory threadFactory,//创建线程工厂，定制线程的创建过程
                              RejectedExecutionHandler handler) //拒绝策略。当工作队列、线程池全满时如何拒绝新任务
```

**拒绝策略:**
- AbortPolicy简单粗暴，直接抛出拒绝异常，这也是默认的拒绝策略
- CallerRunsPolicy如果线程池未关闭，则会在调用者线程中直接执行新任务，这会导致主线程提交线程性能变慢
- DiscardPolicy表示不处理新任务，即丢弃
- DiscardOldestPolicy抛弃最老的任务，从队列中取出最老的任务然后放入新的任务执行

**提交线程任务:**
- execute没有返回值，如果不需要直到线程的结果就使用execute()
- submit()返回一个Future对象，如果想知道线程结果就使用submit()提交，而且它能在主线程中通过Future的get方法捕获线程中的异常

**线程池的关闭:**
- shutdown()不再接受新的任务，之前提交的任务等执行结束再关闭线程池
- shutdownNow()不再接受新的任务，试图停止池中的任务再关闭线程池，返回所有未处理线程列表

# 四.Java线程的生命周期
### 1.新建状态(new)
当程序使用new关键字创建一个线程以后，该线程就处于新建状态，此时它和其他的JAVA对象一样，仅仅由JAVA虚拟机为其分配内存，并初始化成员变量的值。此时的线程对象没有表现出任何线程的动态特征，程序也不会执行线程的线程执行体。

### 2.就绪状态(Runnable)
当线程对象调用start()方法以后，该线程进入就绪状态，JAVA虚拟机会为其创建方法调用栈和程序计数器。处于这种状态中的线程并没有开始运行，只是表示当前线程可以运行了，至于什么时候运行，则取决于JVM里线程调度器的调度。所以线程的执行是由底层平台控制， 具有一定的随机性。并不是说执行了t.start()此线程立即就会执行。

### 3.运行状态(Running)
如果就绪状态的线程获取到了CPU资源，就可以执行 run()(所以run()方法是由线程获得CPU以后自动执行)，此时线程便处于运行状态。如果一个计算机只有一个CPU，那么在任意时刻只有一个线程处于运行状态。
相对的，如果有多个CPU，那么在同一时刻就可以有多个线程并行执行。但是，当处于就绪状态的线程数大于处理器数时，仍然会存在多个线程在同一CPU上轮换执行的现象，只是计算机的运行速度非常快，人感觉不到而已。当
一个线程开始运行后，它不可能一直持有CPU(除非该线程执行体非常短，瞬间就执行结束了)。所以，线程在执行过程中会被中断，目的是让其它线程获得执行的CPU的机会。线程的调度细节取决于底层平台所采用的策略。
对于抢占式策略的系统而言，系统会给每一个可执行线程一个时间段来处理任务，当该时间结束后，系统就会剥夺该线程所占用资源(即让出CPU)，让其它线程获得执行机会。所有的现代桌面和服务器操作系统
都采用抢占式调度策略，但一些小型设备，如：手机，则可能采用协作式调度策略。在这样的系统中，只有当一个线程调用了它的sleep()或yield()方法后才会放弃所占用的资源。也就是说，此时必须该线程主动放弃占用资源，
才能轮到其他就绪状态的线程获得CPU，不然必须要等当前线阻塞/死亡以后，其他线程才有机会运行。处于运行状态的线程最为复杂，它可以变为阻塞状态、就绪状态和死亡状态。

### 4.阻塞状态(Blocked)
当如下情况发生时，线程会进入阻塞状态：
- 线程调用sleep()等方法主动放弃占用的处理器资源，通过调用线程的 sleep() 或 join() 发出了 I/O 请求时，线程就会进入到阻塞状态。当sleep() 状态超时，join() 等待线程终止或超时，或者 I/O 处理完毕，线程重新转入就绪状态；
- 线程调用了一个阻塞式IO方法，在该方法返回以前，该线程被阻塞；
- 线程试图获得一个同步监视器，但该监视器被其他线程持有；
- 运行状态中的线程执行 wait() 方法，使线程进入到等待阻塞状态；
- 线程调用suspend()方法将该线程挂起；

当正在执行的线程被阻塞以后，其他线程可以获得执行的机会，被阻塞的线程会在合适的时候进入就绪状态，而不是进入运行状态。也就是说，当线程阻塞解除后，必须重新等待线程调度器再次调度它，而不是马上获得CPU。所以针对上述线程阻塞情况，如何让线程重新进入就绪状态，有如下几种情况：
- 调用sleep()方法的线程经过了指定时间；
- 线程调用的阻塞式IO方法已经返回；
- 线程成功地获得了试图取得的同步监视器；
- 线程在等待通知时，其他线程发出了一个通知；
- 处于挂起状态的线程被调用了resume()恢复方法；

### 5.死亡状态(Dead)
一个运行状态的线程完成任务或者其他终止条件发生时，该线程就切换到终止状态。 线程会在如下几种情况结束(结束后就处于死亡状态)：
- run()/call()方法执行完成，线程正常结束；
- 线程抛出一个未捕获的Exception或Error；
- 直接调用线程的stop()方法结束该线程->该方法容易导致死锁，通常不建议使用。


如果主线程结束了以后，其他线程会不会受影响呢？结果是不会，一旦当子线程启动以后，它就拥有和主线程一样的地位，它不会受主线程的影响。

>注意：当线程死亡以后，不能再次调用start()方法来启动该线程，调用会返回IllegalThreadStateException异常。程序只能对处于新建状态的线程调用start()方法，而对处于新建状态的线程两次调用start()方法也是错误的，这都会引发IllegalThreadStateException异常。

### 6.总结
![](https://upload-images.jianshu.io/upload_images/3067896-b94777c8d3b90753.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
线程从阻塞状态只能进入就绪状态，而不能直接进入运行状态。而就绪状态到运行状态之间的转换通常不受程序控制，而由系统线程调度所决定，当处于就绪状态的线程获得处理器资源时，该线程进入运行状态；当处于运行状态的线程失去处理器器资源时，该线程进入就绪状态。但有一个方法可以控制线程从运行状态转为就绪状态，那就是yiled()方法。

# 五.Java线程调度方法
在某一个时刻，只能有一个程序在运行(多核除外)。cpu在做着快速的切换，以达到看上去是同时运行的效果。可以形象把多线程的运行行为认为是在互相抢夺cpu的执行权。这就是多线程的一个特性：随机性。谁抢到谁执行，至于执行多长，cpu说了算。
- start()方法的调用后并不是立即执行多线程代码，而是使得该线程变为可运行态(Runnable)，线程什么时候运行是由操作系统决定的。
- 从程序运行的结果可以发现，多线程程序是乱序执行。因此，只有乱序执行的代码才有必要设计为多线程。
- Thread.sleep()方法调用目的是不让当前线程独自霸占该进程所获取的CPU资源，以留出一定时间给其他线程执行的机会。
- 实际上所有的多线程代码执行顺序都是不确定的，每次执行的结果都是随机的。
### 1. 线程的优先级
调整线程优先级：Java线程有优先级，优先级高的线程会获得较多的运行机会，Java线程的优先级用整数表示，取值范围是1~10，Thread类有以下三个静态常量：
- static int MAX_PRIORITY：线程可以具有的最高优先级，取值为10。
- static int MIN_PRIORITY：线程可以具有的最低优先级，取值为1。
- static int NORM_PRIORITY：分配给线程的默认优先级，取值为5。

>Thread类的setPriority()和getPriority()方法分别用来设置和获取线程的优先级。每个线程都有默认的优先级。主线程的默认优先级为Thread.NORM_PRIORITY。 线程的优先级有继承关系，比如A线程中创建了B线程，那么B将和A具有相同的优先级。JVM提供了10个线程优先级，但与常见的操作系统都不能很好的映射。如果希望程序能移植到各个操作系统中，应该仅仅使用Thread类有以下三个静态常量作为优先级，这样能保证同样的优先级采用了同样的调度方式。

### 2.线程睡眠
Thread.sleep(long millis)方法，使线程转到阻塞状态。millis参数设定睡眠的时间，以毫秒为单位。当睡眠结束后，就转为就绪(Runnable)状态。sleep()平台移植性好。

### 3.线程等待
Object类中的wait()方法，导致当前的线程等待，直到其他线程调用此对象的 notify() 方法或 notifyAll() 唤醒方法。这个两个唤醒方法也是Object类中的方法，行为等价于调用 wait(0) 一样。

### 4.线程让步
Thread.yield() 方法，暂停当前正在执行的线程对象，把执行机会让给相同或者更高优先级的线程。

### 5.线程加入
join()方法，等待其他线程终止。在当前线程中调用另一个线程的join()方法，则当前线程转入阻塞状态，直到另一个进程运行结束，当前线程再由阻塞转为就绪状态。

### 6.线程唤醒
Object类中的notify()方法，唤醒在此对象监视器上等待的单个线程。如果所有线程都在此对象上等待，则会选择唤醒其中一个线程。选择是任意性的，并在对实现做出决定时发生。线程通过调用其中一个 wait 方法，在对象的监视器上等待。 直到当前的线程放弃此对象上的锁定，才能继续执行被唤醒的线程。被唤醒的线程将以常规方式与在该对象上主动同步的其他所有线程进行竞争；例如，唤醒的线程在作为锁定此对象的下一个线程方面没有可靠的特权或劣势。类似的方法还有一个notifyAll()，唤醒在此对象监视器上等待的所有线程。

# 六.Java多线程导致的安全问题
### 1.并行和并发
##### (1.)并行执行
两个或多个处理逻辑在``同个一时刻内发生``，cpu同时执行，是真正的同时。
##### (2.)并发执行
并发是轮流处理多个任务，同一个时间段内多个任务同时都在执行，并且都没有执行结束。并发任务强调在一个时间段内同时执行，而一个时间段由多个单位时间累积而成，所以说并发的多个任务在单位时间内不一定同时在执行。
主要的CPU调度算法有如下两种：
1. 分时调度：每个线程轮流获取CPU使用权，各个线程平均CPU时间片。
2. 抢占式调度：Java虚拟机使用的就是这种调度模型。这种调度方式会根据线程优先级，先调度优先级高的线程，如果线程优先级相同，会随机选取线程执行。

### 2.内存模型
##### (1.)现代计算机内存模型
计算机在执行程序时，每条指令都是在CPU中执行的，而执行指令过程中，势必涉及到数据的读取和写入。由于程序运行过程中的临时数据是存放在主存(物理内存)当中的，这时就存在一个问题，由于CPU执行速度很快，而从内存读取数据和向内存写入数据的过程跟CPU执行指令的速度比起来要慢的多，因此如果任何时候对数据的操作都要通过和内存的交互来进行，会大大降低指令执行的速度。因此在CPU里面就有了高速缓存。也就是当程序在运行过程中，会将运算需要的数据从主存复制一份到CPU的高速缓存当中，那么CPU进行计算时就可以直接从它的高速缓存读取数据和向其中写入数据，当运算结束之后，再将高速缓存中的数据刷新到主存当中。这是计算机硬件对于主存数据的访问方式。
![](https://upload-images.jianshu.io/upload_images/3067896-665e9c2de6a39f0f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
##### (2.)Java内存模型(JMM)
前面介绍过了计算机内存模型，这是解决多线程场景下并发问题的一个重要规范。那么具体的实现是如何的呢，不同的编程语言，在实现上可能有所不同。众所周知，Java程序是需要运行在Java虚拟机上面的，Java内存模型即Java Memory Model，简称JMM。Java内存模型(JMM)定义了Java虚拟机(JVM)在计算机内存(RAM)中的工作规范。在硬件内存模型中，各种CPU架构的实现是不尽相同的，Java作为跨平台的语言，JMM用来屏蔽掉各种硬件和操作系统的内存访问差异，以实现让Java程序在各平台下都能够达到一致的内存访问效果。JMM是一个抽象的概念，并不是物理上的内存划分。
![Java内存模型(JMM)](https://upload-images.jianshu.io/upload_images/3067896-aa15ce1c74f97309.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- 所有的变量都存储在主内存中。
- 每个线程都有自己独立的工作内存，里面保存该线程使用到的变量的副本(主内存中该变量的一份拷贝)。
- 线程对共享变量的所有操作都必须在自己的工作内存中进行，不能直接从主内存中读写。
- 不同线程之间无法直接访问其他线程工作内存中的变量，线程间变量值的传递需要通过主内存来完成。

### 3.Java多线程安全问题产生的原因
通过上文可以了解到在多线程并发执行时，每一个线程都自己独立的工作内存，里面保存该线程使用到的变量的副本，线程对共享变量的所有操作都必须在自己的工作内存中进行，不能直接从主内存中读写。CPU执行线程是随机进行的，因此当多条语句在操作同一个线程共享数据时，一个线程对多条语句只执行了一部分，还没有执行完，另一个线程参与进来执行，导致共享数据的错误。
要产生多线程安全问题需要同时满足以下两个条件：
- 多个线程在操作共享的数据。
- 操作共享数据的线程代码有多条。

线程安全问题体现在三个方面：``原子性、可见性、有序性``

# 七.原子性、可见性、有序性
### 1.原子性(Atomic)
原子性即一个操作或者多个操作 要么全部执行并且执行的过程不会被任何因素打断，要么就都不执行。对于别的线程而言，他要么看到的是该线程还没有执行的情况，要么就是看到了线程执行后的情况，不会出现执行一半的场景，简言之，其他线程永远不会看到中间结果。
```
x = 10;        //语句1
y = x;         //语句2
x++;           //语句3
x = x + 1;     //语句4
```
- 语句1是直接将数值10赋值给x，也就是说线程执行这个语句的会直接将数值10写入到工作内存中。是保证原子性的。
- 语句2实际上包含2个操作，它先要去读取x的值，再将x的值写入工作内存，虽然读取x的值以及 将x的值写入工作内存 这2个操作都是原子性操作，但是合起来就不是原子性操作了。
- 语句3 x++和 语句4 x = x+1包括3个操作：读取x的值，进行加1操作，写入新的值。因此不是原子性操作。

**只有简单的读取、赋值(而且必须是将数字赋值给某个变量，变量之间的相互赋值不是原子操作)才是原子操作。**

Java内存模型只保证了基本读取和赋值是原子性操作，如果要实现更大范围操作的原子性，可以通过synchronized和Lock来实现。由于synchronized和Lock能够保证任一时刻只有一个线程执行该代码块，那么自然就不存在原子性问题了，从而保证了原子性。

### 2.可见性
可见性是指当多个线程访问同一个变量时，一个线程修改了这个变量的值，其他线程能够立即看得到修改的值。
例如:
```
//线程1执行的代码
int i = 0;
i = 10;
 
//线程2执行的代码
j = i; 
println(j);//输出 0
```
假若执行线程1的是CPU1，执行线程2的是CPU2。由上面的分析可知，当线程1执行 i =10这句时，会先把i的初始值加载到CPU1的高速缓存中，然后赋值为10，那么在CPU1的高速缓存当中i的值变为10了，却没有立即写入到主存当中。此时线程2执行 j = i，它会先去主存读取i的值并加载到CPU2的缓存当中，注意此时内存当中i的值还是0，那么就会使得j的值为0，而不是10。这就是可见性问题，在多线程环境下，一个线程对共享变量的操作对其他线程是不可见的。线程1对变量i修改了之后，线程2没有立即看到线程1修改的值。

Java提供了volatile关键字来保证可见性。。当一个共享变量被volatile修饰时，它会保证修改的值会立即被更新到主内存，当有其他线程需要读取时，会去主存中读取新值。而普通的共享变量不能保证可见性，因为普通共享变量被修改之后，什么时候被写入主存是不确定的，当其他线程去读取时，此时内存中可能还是原来的旧值，因此无法保证可见性。

下面用一段代码来做测试:
```
public class VisibilityTest extends Thread{
　　//如果没有关键字volatile，会发现这个线程停不掉，可自行测试。
    private volatile boolean stop;

    public void run() {
        int i = 0;
        while (!stop) {
            i++;
        }
        System.out.println("finish loop,i=" + i);
    }

    public void stopIt() {
        stop = true;
    }

    public boolean getStop() {
        return stop;
    }

    public static void main(String[] args) throws InterruptedException {
        VisibilityTest visibilityTest = new VisibilityTest();
        visibilityTest.start();
        visibilityTest.sleep(1000);
        visibilityTest.stopIt();
        System.out.println(visibilityTest.getStop());

    }
}
```
除了volatile还有两种解决可见性问题的方法：
1. final关键字，能够解决的原因：final常量会进常量区(以前的方法区，现在的Metaspace)，常量区是线程安全的，线程安全就是一个线程占有着此资源的时候，其他线程不能占有，所以可想而知，只要A线程在对此资源做任何操作，B线程都是等待着的，当A释放了，B才去jvm拿值，这样也算保证了可见性。
2. synchronized和Lock也能够保证可见性，synchronized和Lock能保证同一时刻只有一个线程获取锁然后执行同步代码，并且在释放锁之前会将对变量的修改刷新到主存当中。因此可以保证可见性。

### 3.有序性
按照日常的思维，程序的执行过程是从上至下一行一行执行的，就是说按照代码的顺序来执行。那么JVM在实际中一定会这样吗？ 答案是否定的。
```
a = 5;     //1
b = 20;    //2
c = a + b; //3
```
编译器优化后可能变成
```
b = 20;    //1
a = 5;     //2
c = a + b; //3
```
在这个例子中，编译器调整了语句的顺序(指令重排序(Instruction Reorder))，但是不影响程序的最终结果。

##### (1.)指令重排序
Java语言是运行在 Java 自带的 JVM(Java Virtual Machine) 环境中，在JVM环境中源代码(.class)的执行顺序与程序的执行顺序(runtime)不一致，或者程序执行顺序与编译器执行顺序不一致的情况，就称程序执行过程中发生了指令重排序。

**编译器为了提高程序运行效率，可能会对输入代码进行优化。它不保证程序中各个语句的执行先后顺序同代码中的顺序一致，但是它会保证程序最终执行结果和代码顺序执行的结果是一致的(单线程情况下)。**

##### (2.)指令重排序导致出现有序性问题
编译器的指令重排序，这种修改可以优化指令的执行顺序，提升程序的性能和执行速度，使语句执行顺序发生改变，出现重排序，但最终结果看起来没什么变化，``在单线程程序里面没问题``。但是在多多线程环境下就可能会出现有序性问题。有序性问题指的是在多线程环境下，由于执行语句重排序后，重排序的这一部分没有一起执行完，就切换到了其它线程，导致的结果与预期不符的问题。这就是编译器的编译优化给并发编程带来的程序有序性问题。
单例模式的双重检查锁:
```
public class SingletonDemo {

    private /** volatile*/ static SingletonDemo instance;

    public static SingletonDemo getInstance() {
        if (instance == null) {
            synchronized (SingletonDemo.class) {
                if (null == instance) {
                    instance = new SingletonDemo();
                }
            }
        }
        return instance;
    }
}
```
这里为什么不能缺少volatile关键字呢？主要在于instance = new Instance()这个语句实际上包含了三个操作：
1. 分配对象内存空间；
2. 初始化对象；
3. 设置instance指向刚分配的内存地址

前文中提到一个线程内看其他线程中的指令执行顺序可能是乱序的，有可能是如下顺序：
1. 分配对象内存；
2. 设置instance指向刚分配的内存；
3. 初始化对象
那么其他线程可能取得的是没有初始化的对象，出现并发bug。

在java里可以通过volatile来保证一定的有序性，另外也可以通过synchroized和lock来保证有序性。synchroized和lock是保证每个时刻是只有一个线程执行同步代码，相当于是让线程顺序执行代码从而保证有序性。Java具备一些先天的有序性(不需要任何手段就能保证有序性)，即happens-before原则(先行发生原则)。如果两个操作的执行次序无法从happens-before原则推导出来，那么它们就不能保证有序性。虚拟机可以随意的对它们进行重排序。总结起来：在JMM中，提供了以下三种方式来保证有序性：``volatile机制，synchronized机制，happens-before原则``

##### (3.)happens-before原则
1. 程序次序规则(Program Order Rule)：在一个线程内，按照程序代码顺序，书写在前面的操作先行发生于书写在后面的操作。 准确地说，应该是控制流顺序而不是程序代码顺序，因为要考虑分支、 循环等结构。
2. 管程锁定规则(Monitor Lock Rule)：一个unlock操作先行发生于后面对同一个锁的lock操作。 这里必须强调的是同一个锁，而“后面”是指时间上的先后顺序。
3. volatile变量规则(Volatile Variable Rule)：对一个volatile变量的写操作先行发生于后面对这个变量的读操作，这里的“后面”同样是指时间上的先后顺序。
4. 线程启动规则(Thread Start Rule)：Thread对象的start()方法先行发生于此线程的每一个动作。
5. 线程终止规则(Thread Termination Rule)：线程中的所有操作都先行发生于对此线程的终止检测，我们可以通过Thread.join()方法结束、 Thread.isAlive()的返回值等手段检测到线程已经终止执行。
6. 线程中断规则(Thread Interruption Rule)：对线程interrupt()方法的调用先行发生于被中断线程的代码检测到中断事件的发生，可以通过Thread.interrupted()方法检测到是否有中断发生。
7. 对象终结规则(Finalizer Rule)：一个对象的初始化完成(构造函数执行结束)先行发生于它的finalize()方法的开始。
8. 传递性(Transitivity)：如果操作A先行发生于操作B，操作B先行发生于操作C，那就可以得出操作A先行发生于操作C的结论。
例如:
```
private int value=0；
pubilc void setValue(int value){
    this.value=value；
}
public int getValue(){
    return value；
}
```
假设两个线程A和B，线程A先(在时间上先)调用了这个对象的setValue(1)，接着线程B调用getValue方法 对照着happens-before原则，上面的操作满不满足下面的任何条件：
- 不是同一个线程，所以不涉及：程序次序规则；
- 不涉及同步，所以不涉及：管程锁定规则；
- 没有volatile关键字，所以不涉及：volatile变量规则
- 没有线程的启动，中断，终止，所以不涉及：线程启动规则，线程终止规则，线程中断规则
- 没有对象的创建于终结，所以不涉及：对象终结规则
- 更没有涉及到传递性

所以一条规则都不满足，尽管线程A在时间上与线程B具有先后顺序，但是，却并不满足happens-before原则，也就是有序性并不会保障，所以线程B的数据获取是不安全的。时间先后顺序与先行发生原则之间基本没有太大的关系，所以我们衡量并发安全问题的时候不要受到时间顺序的干扰，一切必须以先行发生原则为准。只有真正满足了happens-before原则，才能保障安全。

**如果不能满足happens-before原则，就需要使用下面的synchronized机制和volatile机制机制来保证有序性。**

### 4.volatile关键字
通过volatile关键字来保证一定的“有序性”，volatile的底层是使用内存屏障来保证有序性的。写volatile变量时，可以确保volatile写之前的操作不会被编译器重排序到volatile写之后。读volatile变量时，可以确保volatile读之后的操作不会被编译器重排序到volatile读之前。

> 当第二个操作是volatile写时，不管第一个操作是什么，都不能重排序。这个规则确保volatile写之前的操作不会被编译器重排序到volatile写之后。 当第一个操作是volatile读时，不管第二个操作是什么，都不能重排序。这个规则确保volatile读之后的操作不会被编译器重排序到volatile读之前。 当第一个操作是volatile写，第二个操作是volatile读时，不能重排序。

**内存屏障有两个能力：**
- 就像一套栅栏分割前后的代码，阻止栅栏前后的没有数据依赖性的代码进行指令重排序，保证程序在一定程度上的**有序性**。
- 强制把写缓冲区/高速缓存中的脏数据等写回主内存，让缓存中相应的数据失效，保证数据的**可见性**。

一旦一个共享变量（类的成员变量、类的静态成员变量）被volatile修饰之后，那么就具备了两层语义：
- 保证了不同线程对这个变量进行操作时的可见性，即一个线程修改了某个变量的值，这新值对其他线程来说是立即可见的。
- 禁止进行指令重排序。

>在Java并发编程中，如果要保证代码的安全性，则必须保证代码的原子性、可见性和有序性。

参考资料:
[全面理解Java内存模型(JMM)及volatile关键字](https://blog.csdn.net/javazejian/article/details/72772461)
[Java内存模型JMM 高并发原子性可见性有序性简介 多线程中篇(十)](https://www.cnblogs.com/noteless/p/10401193.html)
[Java内存模型(JMM)那些事](https://www.cnblogs.com/hello-shf/p/12100799.html)
[Java并发编程：volatile关键字解析](https://www.cnblogs.com/dolphin0520/p/3920373.html)