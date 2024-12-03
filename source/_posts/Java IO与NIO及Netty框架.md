---
title: Java IO与NIO及Netty框架
date: 2017-11-19
categories: 
  - Java开发
---

# 一.I/O模型
### 1.什么是IO
IO在计算机中指Input/Output，也就是``输入和输出``。由于程序和运行时数据是在内存中进行，比如，声明变量，创建数组，创建集合。如果需要与外部设备，比如键盘，显示器，硬盘等进行数据的交互，就需要用到IO。通过数据线、网线、NFC、蓝牙之类的东西将计算机与外部设备连接起来，连接起来之后，通过特定的比特流进行沟通。
一个比特（bit）就表示一个二进制数，可以是0或者1。但是因为一个bit所表示的内容太有限了，所以计算机中更常见的基本单位是字节，一个字节由8个bit组成(设备上的数据无论是图片或者视频，文字，它们都以二进制存储的)。
当足够多的字节连续地从外部设备传入计算机、或者从计算机传入外部设备，这种情况就是比特流或者叫字节流(Stream)，在IO编程中，Stream（流）是一个很重要的概念，可以把流想象成一个水管，
数据就像是是水管里的水。Input Stream就是数据从外面（磁盘、网络）流进内存，Output Stream就是数据从内存流到外面去。

### 2. Liunx IO模型分类
IO (Input/Output，输入/输出)即数据的读取（接收）或写入（发送）操作，通常用户进程中的一个完整IO分为两阶段：用户进程空间<-->内核空间、内核空间<-->设备空间（磁盘、网络等）。IO有内存IO、网络IO和磁盘IO三种，通常我们说的IO指的是网络IO和磁盘IO。

LINUX中进程无法直接操作I/O设备，其必须通过系统调用请求kernel来协助完成I/O动作；内核会为每个I/O设备维护一个缓冲区。
对于一个输入操作来说，进程IO系统调用后，内核会先看缓冲区中有没有相应的缓存数据，没有的话再到设备中读取，因为设备IO一般速度较慢，需要等待；内核缓冲区有数据则直接复制到进程空间。

所以，对于一个网络输入操作通常包括两个不同阶段：
- 等待网络数据到达网卡→读取到内核缓冲区，数据准备好；
- 从内核缓冲区复制数据到进程空间。

IO主要分为两大类:一类是同步IO,一类是异步IO.

>一般来讲：阻塞IO模型、非阻塞IO模型、IO复用模型(select/poll/epoll)、信号驱动IO模型都属于同步IO，因为阶段2是阻塞的(尽管时间很短)。只有异步IO模型是符合POSIX异步IO操作含义的，不管在阶段1还是阶段2都可以干别的事。
只有同步时才有阻塞和非阻塞之分.

### 3. 同步IO
非阻塞io在进行磁盘io的时候，虽然不需要等磁盘io这个过程，但是当磁盘io完成之后，他还需要把数据从内核空间移动到用户空间，这个时间也是阻塞的，这就是同步.

>同步IO又分为阻塞IO,非阻塞IO,多路复用IO.
#### (1.)阻塞(blocking) IO

传统的IO流都是阻塞式的。也就是说，当一个线程调用read()或者write()方法时，该线程将被阻塞，直到有一些数据读读取或者被写入，在此期间，该线程不能执行其他任何任务。
在完成网络通信进行IO操作时，由于线程会阻塞，所以服务器端必须为每个客户端都提供一个独立的线程进行处理，当服务器端需要处理大量的客户端时，性能急剧下降。

阻塞IO，指的是需要内核IO操作彻底完成后，才返回到用户空间执行用户的操作。阻塞指的是用户空间程序的执行状态。传统的IO模型都是同步阻塞IO。再Java中，默认创建的socket都是阻塞的。
非阻塞IO，指的是用户空间的程序不需要等待内核IO操作彻底完成，可以立即返回用户空间执行用户操作，即处于非阻塞的状态，与此同时内核会立即返回给用户一个状态值。
简单来说：阻塞是指用户空间（调用线程）一直在等待，而不能干别的事情；非阻塞是指用户空间（调用线程）拿到内核返回的状态值就返回自己的空间，IO操作可以干就干，不可以干，就去干别的事情。

  进程发起IO系统调用后，进程被阻塞，转到内核空间处理，整个IO处理完毕后返回进程。操作成功则进程获取到数据。

1、典型应用：阻塞socket、Java BIO；

2、特点：

进程阻塞挂起不消耗CPU资源，及时响应每个操作；

实现难度低、开发应用较容易；

适用并发量小的网络应用开发；

不适用并发量大的应用：因为一个请求IO会阻塞进程，所以，得为每请求分配一个处理进程（线程）以及时响应，系统开销大。

#### (2.)非阻塞(non-blocking)IO
进程发起IO系统调用后，如果内核缓冲区没有数据，需要到IO设备中读取，进程返回一个错误而不会被阻塞；进程发起IO系统调用后，如果内核缓冲区有数据，内核就会把数据返回进程。

对于上面的阻塞IO模型来说，内核数据没准备好需要进程阻塞的时候，就返回一个错误，以使得进程不被阻塞。

1、典型应用：socket是非阻塞的方式（设置为NONBLOCK）

2、特点：

进程轮询（重复）调用，消耗CPU的资源；

实现难度低、开发应用相对阻塞IO模式较难；

适用并发量较小、且不需要及时响应的网络应用开发；

#### (3.)复用模型IO
  多个的进程的IO可以注册到一个复用器（select）上，然后用一个进程调用该select， select会监听所有注册进来的IO；

       如果select没有监听的IO在内核缓冲区都没有可读数据，select调用进程会被阻塞；而当任一IO在内核缓冲区中有可数据时，select调用就会返回；

       而后select调用进程可以自己或通知另外的进程（注册进程）来再次发起读取IO，读取内核中准备好的数据。

       可以看到，多个进程注册IO后，只有另一个select调用进程被阻塞。

1、典型应用：select、poll、epoll三种方案，nginx都可以选择使用这三个方案;Java NIO;

2、特点：

专一进程解决多个进程IO的阻塞问题，性能好；Reactor模式;

实现、开发应用难度较大；

适用高并发服务应用开发：一个进程（线程）响应多个请求；

3、select、poll、epoll

Linux中IO复用的实现方式主要有select、poll和epoll：

Select：注册IO、阻塞扫描，监听的IO最大连接数不能多于FD_SIZE；

Poll：原理和Select相似，没有数量限制，但IO数量大扫描线性性能下降；

Epoll ：事件驱动不阻塞，mmap实现内核与用户空间的消息传递，数量很大，Linux2.6后内核支持；

### 4. 异步(asynchronous) IO
所谓同步就是一个任务的完成需要依赖另外一个任务时，只有等待被依赖的任务完成后，依赖的任务才能算完成，这是一种可靠的任务序列。要么成功都成功，失败都失败，两个任务的状态可以保持一致。

所谓异步是不需要等待被依赖的任务完成，只是通知被依赖的任务要完成什么工作，依赖的任务也立即执行，只要自己完成了整个任务就算完成了。至于被依赖的任务最终是否真正完成，依赖它的任务无法确定，所以它是不可靠的任务序列。

同步：调用端会一直等待服务端响应，直到返回结果。
异步：调用端发起调用之后不会立刻返回，不会等待服务端响应。服务端通过通知机制或者回调函数来通知客户端。
阻塞：服务端返回结果之前，客户端线程会被挂起，此时线程不可被CPU调度，线程暂停运行。
非阻塞：在服务端返回前，函数不会阻塞调用端线程，而会立刻返回。


当进程发起一个IO操作，进程返回（不阻塞），但也不能返回果结；内核把整个IO处理完后，会通知进程结果。如果IO操作成功则进程直接获取到数据。

1、典型应用：JAVA7 AIO、高性能服务器应用

2、特点：

不阻塞，数据一步到位；Proactor模式；

需要操作系统的底层支持，LINUX 2.5 版本内核首现，2.6 版本产品的内核标准特性；

实现、开发应用难度大；

非常适合高性能高并发应用；

# 二.Java I/O模型 
BIO、NIO、AIO
为了处理计算机的输入、输出流，Java给出了一套IO框架，它的工作原理也就是读取、写入流。Java中对应的抽象类就是InputStream和OutputStream。这俩就是我们对流进行操作的基础了。

首先Java中的IO都是依赖操作系统内核进行的，我们程序中的IO读写其实调用的是操作系统内核中的read&write两大系统调用。
那内核是如何进行IO交互的呢？

网卡收到经过网线传来的网络数据，并将网络数据写到内存中。
当网卡把数据写入到内存后，网卡向cpu发出一个中断信号，操作系统便能得知有新数据到来，再通过网卡中断程序去处理数据。
将内存中的网络数据写入到对应socket的接收缓冲区中。
当接收缓冲区的数据写好之后，应用程序开始进行数据处理。

对应抽象到java的socket代码简单示例如下：
```
public class SocketServer {
  public static void main(String[] args) throws Exception {
    // 监听指定的端口
    int port = 8080;
    ServerSocket server = new ServerSocket(port);
    // server将一直等待连接的到来
    Socket socket = server.accept();
    // 建立好连接后，从socket中获取输入流，并建立缓冲区进行读取
    InputStream inputStream = socket.getInputStream();
    byte[] bytes = new byte[1024];
    int len;
    while ((len = inputStream.read(bytes)) != -1) {
      //获取数据进行处理
      String message = new String(bytes, 0, len,"UTF-8");
    }
    // socket、server，流关闭操作，省略不表
  }
}
```
可以看到这个过程和底层内核的网络IO很类似，主要体现在accept()等待从网络中的请求到来然后bytes[]数组作为缓冲区等待数据填满后进行处理。  
而BIO、NIO、AIO之间的区别就在于这些操作是同步还是异步，阻塞还是非阻塞。

JavaNIO是非阻塞式的。当线程从某通道进行读写数据时，若没有数据可用时，该线程会去执行其他任务。
线程通常将非阻塞IO的空闲时间用于在其他通道上执行IO操作，所以单独的线程可以管理多个输入和输出通道。
因此NIO可以让服务器端使用一个或有限几个线程来同时处理连接到服务器端的所有客户端。

在JDK 1.4之前，基于Java的所有Socket通信都使用了同步阻塞模式（Blocking I/O），这种一请求一应答的通信模型简化了上层开发，但性能可靠性存在巨大瓶颈，对高并发和低时延支持不好
在JDK 1.4之后，提供了新的NIO(New I/O)类库，Java也可以支持非阻塞I/O了，新增了java.nio包，提供了很多异步I/O开发的API和类库。
JDK 1.7发布后，将原来的NIO类库进行了升级，提供了AIO功能，支持基于文件的异步I/O操作和针对套接字的异步I/O操作等功能
### BIO
使用BIO通信模型的服务端，通常通过一个独立的Acceptor线程负责监听客户端的连接，监听到客户端连接请求后为每一个客户端创建一个新的线程链路进行处理，  
处理完成通过输出流回应客户端，线程消耗，这就是典型一对一答模型，下面我们通过代码对BIO模式进行具体分析，我们实现客户端发送消息服务端将消息回传我们的功能。
```
 int port = 3000;
    try(ServerSocket serverSocket = new ServerSocket(port)) {
        Socket socket = null;
        while (true) {
            //主程序阻塞在accept操作上
            socket = serverSocket.accept();
            new Thread(new BioExampleServerHandle(socket)).start();
        }
    } catch (Exception e) {
        e.printStackTrace();
    }
```
通过代码我们可以发现BIO的主要问题在于，每当一个连接接入时我们都需要new一个线程进行处理，这显然是不合适的，因为一个线程只能处理一个连接，如果在高并发的情况下，  
我们的程序肯定无法满足性能需求，同时我们对线程创建也缺乏管理。可以通过线程池技术，解决线程频繁创建的问题。
```
    int port = 3000;
    ThreadPoolExecutor socketPool = null;
    try(ServerSocket serverSocket = new ServerSocket(port)) {
        Socket socket = null;
        int cpuNum = Runtime.getRuntime().availableProcessors();
        socketPool = new ThreadPoolExecutor(cpuNum, cpuNum * 2, 1000,
                TimeUnit.SECONDS, new ArrayBlockingQueue<Runnable>(1000));
        while (true) {
            //accept()阻塞,直到获取到连接
            socket = serverSocket.accept();
            //将任务交给线程池，执行相关逻辑
            socketPool.submit(new BioExampleServerHandle(socket));
        }
    } catch (Exception e) {
        e.printStackTrace();
    } finally {
        socketPool.shutdown();
    }

```
可以看到每当有新连接接入，我们都将他投递给线程池进行处理，由于我们设置了线程池大小和阻塞队列大小，因此在并发情况下都不会导致服务崩溃，但是如果并发数大于阻塞队列大小，  
或服务端处理连接缓慢时，阻塞队列无法继续处理，会导致客户端连接超时，影响用户体验。
>实际上仅仅只是对之前I/O线程模型的一个简单优化，使用线程池解决了频繁创建线程的问题。它无法从根本上解决同步I/O导致的通信线程阻塞问题。
### NIO
Java中的NIO 是new IO的意思。其实是NIO加上IO多路复用技术。普通的NIO是线程轮询查看一个IO缓冲区是否就绪，而Java中的new IO指的是线程轮询地去查看一堆IO缓冲区中哪些就绪，这是一种IO多路复用的思想。  
IO多路复用模型中，将检查IO数据是否就绪的任务，交给系统级别的select或epoll模型，由系统进行监控，减轻用户线程负担。
NIO主要有buffer、channel、selector三种技术的整合，通过零拷贝的buffer取得数据，每一个客户端通过channel在selector（多路复用器）上进行注册。  
服务端不断轮询channel来获取客户端的信息。channel上有connect,accept（阻塞）、read（可读）、write(可写)四种状态标识。根据标识来进行后续操作。  
所以一个服务端可接收无限多的channel。不需要新开一个线程。大大提升了性能。

NIO为非阻塞的IO，其出现之前，Java是通过socket来实现基本的网络 通信功能的。socket本身是阻塞的，如果客户端没有对服务器端发起链接请求，那么accept就i会阻塞。
如果连接成功，当数据还在准备阶段，对read的操作同样会阻塞。当处理多个连接时，就需要采用多线程的方式，当处理多个连接时，就需要采用多线程的方式，
由于每个线程都拥有自己的栈空间，而且由于阻塞会导致大量线程进行上下文切换，使得程序运行非常低下，因此j2se1.4中引入了NIO来解决这个问题。
NIO通过selector、channel和buffer老师先非阻塞的IO操作。
NIO非阻塞的实现主要采用了Reactor设计模式，这个设计模式与observer设计模式类似，只不过observer设计模式只处理一个事件源，而reactor设计模式可以来处理多个事件源。
channel可以被看作一个双向的非阻塞通道。在实现中需要把channel的io事件注册给selector。selector的内部实现原理为：对所有注册的channel进行轮询访问，  
一旦轮询到一个channel1有注册事件发生，它就通过回传selection-key的方式通知开发人员对channel1进行数据的读写。这种通过轮询的方式处理多线程请求时不需要上下文的切换，因此nio有较高的执行效率。


NIO 弥补了同步阻塞I/O的不足，它提供了高速、面向块的I/O，我们对一些概念介绍一下：
Buffer: Buffer用于和NIO通道进行交互。数据从通道读入缓冲区，从缓冲区写入到通道中,它的主要作用就是和Channel进行交互。
Channel: Channel是一个通道，可以通过它读取和写入数据，通道是双向的，通道可以用于读、写或者同时读写。
Selector: Selector会不断的轮询注册在它上面的Channe,如果Channel上面有新的连接读写事件的时候就会被轮询出来，一个Selector可以注册多个Channel，  
只需要一个线程负责Selector轮询，就可以支持成千上万的连接，可以说为高并发服务器的开发提供了很好的支撑。

这块我的理解是, 都是渴了去接水, 传统IO是到水龙头那地儿张着嘴喝饱再走. 而NewIO是把水杯(Buffer缓冲区)放在水龙头下面,然后找个人(Selector)帮自己看着水有没有接满,
接满了告诉自己一声,收到哪个人的信号后NewIO再来拿杯子一饮而尽, 这样的好处就是接水的时间NewIO就可以忙自己的事情了.此处如果没有Selector这个对象的话,NIO也是需要拿着杯子等着了


这段时间时间一直在看NIO，嗯，看的一脸闷逼，一直想不通，IO多路复用是为啥能提高效率的。
下面是的理解：socket连接与多线程没有啥联系，最基本的socket连接，无需多线程，只是会阻塞主线程，进而阻塞下一个连接。采用一个socket连接一个线程，连接会不阻塞。而nio相当于几个ocket连接给一个线程处理

那NIO究竟是什么东西呢？NIO的全称是NoneBlocking IO，非阻塞IO，区别与BIO，BIO的全称是Blocking IO，阻塞IO。那这个阻塞是什么意思呢？  
Accept是阻塞的，只有新连接来了，Accept才会返回，主线程才能继Read是阻塞的，只有请求消息来了，Read才能返回，  
子线程才能继续处理Write是阻塞的，只有客户端把消息收了，Write才能返回，子线程才能继续读取下一个请求所以传统的多线程服务器是BlockingIO模式的，从头到尾所有的线程都是阻塞的。  
这些线程就干等在哪里，占用了操作系统的调度资源，什么事也不干，是浪费。那么NIO是怎么做到非阻塞的呢。它用的是事件机制。  
它可以用一个线程把Accept，读写操作，请求处理的逻辑全干了。如果什么事都没得做，它也不会死循环，它会将线程休眠起来，直到下一个事件来了再继续干活，这样的一个线程称之为NIO线程。

```
public class NIOServer {
    public static void main(String[] args) throws IOException {
        //1.打开多路复用器
        Selector selector = Selector.open();
        //2.打开服务器通道
        ServerSocketChannel ssc = ServerSocketChannel.open();
        //3.设置非阻塞模式
        ssc.configureBlocking(false);
        //4.绑定监听地址
        ssc.bind(new InetSocketAddress(8080));
        //5.把服务器通道注册到多路复用器上，监听阻塞状态
        ssc.register(selector, SelectionKey.OP_ACCEPT);
        while (true){
            //多路复用器开始监听
            selector.select(1000);
            //返回所有注册到多路复用器上通道的SelectionKey----就是通道的状态，如读写
            Set<SelectionKey> keys = selector.selectedKeys();
            Iterator<SelectionKey> iterator = keys.iterator();
            while(iterator.hasNext()){
                SelectionKey key = iterator.next();
                //判断当前状态是否有效
                if (key.isValid()){
                    if (key.isAcceptable()){
                        accept(key,selector);
                    }
                    if (key.isReadable()){
                        read(key);
                    }
                }
                iterator.remove();
            }
        }
    }

    /**
     *
     * @param key
     */
    private static void read(SelectionKey key) {
        try{
            //1.获取服务器通道
            SocketChannel sc = (SocketChannel) key.channel();
            ByteBuffer buffer = ByteBuffer.allocate(1024);
            //2.读取channel中的数据放到buffer中
            int read = sc.read(buffer);
            //buffer中有数据
            if (read > 0){
                buffer.flip();
                byte[] bytes = new byte[buffer.remaining()];
                buffer.get(bytes);
                // 换行符会跟着消息一起传过来
                String content = new String(bytes, "UTF-8").replace("\r\n", "");
                if (content.equalsIgnoreCase("quit")) {
                    key.cancel();
                    sc.close();
                } else {
                    System.out.println("当前线程："+Thread.currentThread().getName()+" receive msg: " + content);
                }

            }
        }catch (Exception e){

        }

    }

    /**
     * 处理连接事件
     * @param key
     * @param selector
     */
    public static void accept(SelectionKey key, Selector selector){
        try{
            //1.获取服务器通道
            ServerSocketChannel ssc = (ServerSocketChannel) key.channel();
            //2.执行阻塞方法进行监听
            SocketChannel sc = ssc.accept();
            //3.设置为非阻塞模式
            sc.configureBlocking(false);
            //4.注册到多路复用器上，并设置读取标志
            sc.register(selector,SelectionKey.OP_READ);
        }catch (Exception e){

        }

    }
}
```
### AIO
AIO是真正意义上的异步非阻塞IO模型。
上述NIO实现中，需要用户线程定时轮询，去检查IO缓冲区数据是否就绪，占用应用程序线程资源，其实轮询相当于还是阻塞的，并非真正解放当前线程，因为它还是需要去查询哪些IO就绪。  
而真正的理想的异步非阻塞IO应该让内核系统完成，用户线程只需要告诉内核，当缓冲区就绪后，通知我或者执行我交给你的回调函数。
AIO可以做到真正的异步的操作，但实现起来比较复杂，支持纯异步IO的操作系统非常少，目前也就windows是IOCP技术实现了，而在Linux上，底层还是是使用的epoll实现的。


NIO2.0 引入了异步通道的概念，提供了异步文件通道和异步套接字通道的实现，我们可以通过Future类来表示异步操作结果，也可以在执行异步操作的时候传入一个Channels,实现CompletionHandler接口为操作回调。

Java 异步 IO 提供了两种使用方式，分别是返回 Future 实例和使用回调函数。

# 三.NIO框架Netty
### 1.JDK JDK 原生 NIO 程序的问题
Netty是业界最流行的NIO框架之一，它的健壮性、功能、性能、可定制性、可扩展性在同类框架中都是首屈一指的，它已经得到了成百上千的商用项目的证明。对于为什么使用Netty这个话题，我们先看一下使用原生的NIO有什么缺点：
1. NIO 的类库和 API 繁杂，使用麻烦：你需要熟练掌握 Selector、ServerSocketChannel、SocketChannel、ByteBuffer 等。
2. 需要具备其他的额外技能做铺垫：例如熟悉 Java 多线程编程，因为 NIO 编程涉及到 Reactor 模式，你必须对多线程和网路编程非常熟悉，才能编写出高质量的 NIO 程序。
3. 可靠性能力补齐，开发工作量和难度都非常大：例如客户端面临断连重连、网络闪断、半包读写、失败缓存、网络拥塞和异常码流的处理等等。NIO 编程的特点是功能开发相对容易，但是可靠性能力补齐工作量和难度都非常大。
4. JDK NIO 的 Bug：例如臭名昭著的 Epoll Bug，它会导致 Selector 空轮询，最终导致 CPU 100%。官方声称在 JDK 1.6 版本的 update 18 修复了该问题，但是直到 JDK 1.7 版本该问题仍旧存在，只不过该 Bug 发生概率降低了一些而已，它并没有被根本解决。

也正是因为有种种缺点，因此不建议使用原生的NIO而是建议使用一些比较成熟的NIO框架例如Netty、Mina，这一系列文章讲的是Netty，Netty作为一款高性能NIO框架，其优点总结有：

- API使用简单、开发门槛低
- 功能强大，预置了多种编码解码功能，支持多种主流协议
- 定制能力强，可以通过ChannelHandler对通信框架进行灵活扩展
- 性能高，与业界其他主流NIO框架对比，Netty性能最优
- 成熟、稳定，Netty修复了已经发现的所有JDK NIO的BUG，业务开发人员不需要再为NIO的BUG而烦恼
- 社区活跃、版本迭代周期短，发现的BUG可以被及时修复，同时，更多的新功能会被加入
- 经历了大规模的商业应用考验，质量得到验证


有了Netty，你可以实现自己的HTTP服务器，FTP服务器，UDP服务器，RPC服务器，WebSocket服务器，Redis的Proxy服务器，MySQL的Proxy服务器等等。  
如果你想知道Nginx是怎么写出来的，如果你想知道Tomcat和Jetty是如何实现的，如果你也想实现一个简单的Redis服务器，那都应该好好理解一下Netty，它们高性能的原理都是类似的。  
我们回顾一下传统的HTTP服务器的原理创建一个ServerSocket，监听并绑定一个端口一系列客户端来请求这个端口服务器使用Accept，获得一个来自客户端的Socket连接对象启动一个新线程处理连接读Socket，  
得到字节流解码协议，得到Http请求对象处理Http请求，得到一个结果，封装成一个HttpResponse对象编码协议，将结果序列化字节流写Socket，将字节流发给客户端继续循环步骤3HTTP服务器之所以称为HTTP服务器，  
是因为编码解码协议是HTTP协议，如果协议是Redis协议，那它就成了Redis服务器，如果协议是WebSocket，那它就成了WebSocket服务器，等等。

使用Netty你就可以定制编解码协议，实现自己的特定协议的服务器。上面我们说的是一个传统的多线程服务器，这个也是Apache处理请求的模式。在高并发环境下，线程数量可能会创建太多，  
操作系统的任务调度压力大，系统负载也会比较高。那怎么办呢？于是NIO诞生了，NIO并不是Java独有的概念，NIO代表的一个词汇叫着IO多路复用。  
它是由操作系统提供的系统调用，早期这个操作系统调用的名字是select，但是性能低下，后来渐渐演化成了Linux下的epoll和Mac里的kqueue。  
我们一般就说是epoll，因为没有人拿苹果电脑作为服务器使用对外提供服务。而Netty就是基于Java NIO技术封装的一套框架。为什么要封装，  
因为原生的Java NIO使用起来没那么方便，而且还有臭名昭著的bug，Netty把它封装之后，提供了一个易于操作的使用模式和接口，用户使用起来也就便捷多了。  


正因为这些优点，Netty逐渐成为了Java NIO变成的首选框架。

流行基于Java NIO通信框架有Mina、Netty、Grizzly等。不管是什么NIO框架。本身其实都是对Java底层的一种在封装。封装一套更简便，更易于扩展的一套东西以方便开发者使用。

Netty是一个提供异步事件驱动的网络应用框架，用以快速开发高性能、高可靠性的网络服务器和客户端程序。

换句话说，Netty是一个NIO框架，使用它可以简单快速地开发网络应用程序，比如客户端和服务端的协议。Netty大大简化了网络程序的开发过程比如TCP和UDP的 Socket的开发。


Netty是一个提供异步事件驱动的网络应用框架，用以快速开发高性能、高可靠性的网络服务器和客户端程序。

换句话说，Netty是一个NIO框架，使用它可以简单快速地开发网络应用程序，比如客户端和服务端的协议。Netty大大简化了网络程序的开发过程比如TCP和UDP的 Socket的开发。


Nety是为了简化高性能网络应用程序的开发，如果你需要开发网络应用，有服务器，有客户端有基于TCP或UDP的网络协议，Netty能提供高性能的网络通讯机制，提供基于事件和流水线的編程模型，  
提供一些协议的支持，比如HTTP,Websockets,SSL等。用Netty，你可以容易地利用Java nio来提高服务端的性能。

比如你想写个tomcat一样的Server，可以用netty。

你想写一个即时通讯的应用，可以用netty。

你想实现一个高性能Rpc框架，可以用netty。


只要是和网络有关，基本都可以用netty。


``implementation 'io.netty:netty-all:4.1.36.Final'``

# 参考资料:
[Netty(三) 什么是 TCP 拆、粘包？如何解决？](https://crossoverjie.top/2018/08/03/netty/Netty(3)TCP-Sticky/)
[Java中的NIO与Netty框架](https://blog.csdn.net/fuzhongmin05/article/details/78819120)
[Socket 之 BIO、NIO、Netty 简单实现](https://zhuanlan.zhihu.com/p/344831741)
[JAVA NIO入门一](https://blog.csdn.net/qq_36500178/article/details/107428338)
[Java NIO浅析](https://tech.meituan.com/2016/11/04/nio.html)
[java NIO理解分析与基本使用](https://www.cnblogs.com/buptleida/p/12633675.html)
[轻松理解java中的IO与NIO](https://zhuanlan.zhihu.com/p/27204492)
[首先了解下所谓的java nio是个什么东西！](https://blog.csdn.net/weixin_34166847/article/details/85998886)
[8分钟深入浅出搞懂BIO、NIO、AIO](https://zhuanlan.zhihu.com/p/83597838)
[史上最强Java NIO入门：担心从入门到放弃的，请读这篇！](https://zhuanlan.zhihu.com/p/71564123)
[如何理解BIO、NIO、AIO的区别？](https://juejin.cn/post/6844903985158045703)
[常用4种IO模型（同步/异步/阻塞/非阻塞的概念）](https://www.cnblogs.com/straybirds/p/9479158.html)
[基于Netty实现服务端与客户端通信](https://juejin.cn/post/6844904122441809934)
[Netty入门——客户端与服务端通信](https://www.cnblogs.com/linjiqin/p/10117382.html)
[Java中的IO框架设计思想](https://blog.csdn.net/w366549434/article/details/106397764)
[为什么我觉得 Java 的 IO 很复杂？](https://www.zhihu.com/question/67535292)



