---
title: Android之Handler机制
---

# 一. Handler其实有两大主要作用
- 线程间通信
- 可以指定messgage和runnable在未来的某个时间节点执行，也就是按照一定的时间顺序执行
# 二.Handler的使用
Handler的简单使用
使用handler发送消息，需要两步，首先是创建一个Handler对象，并重写handleMessage方法，然后需要消息通信的地方，通过Handler的sendMessage方法发送消息。
这里我们创建了一个子线程，模拟子线程向主线程发送消息代码如下：
```
public class MainActivity extends Activity {
    private Handler mHandler;
    private static final int MSG_SUB_TO_MAIN= 100;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        // 1.创建Handler，并重写handleMessage方法
        mHandler = new Handler() {
            @Override
            public void handleMessage(Message msg) {
                super.handleMessage(msg);
                // 处理消息
                switch (msg.what) {
                    case MSG_SUB_TO_MAIN:
                        // 打印出处理消息的线程名和Message.obj
                        Log.e(TAG, "接收到消息： " +    Thread.currentThread().getName() + ","+ msg.obj);
                        break;
                    default:
                        break;
                }
            }
        };
       // 创建一个子线程，在子线程中发送消息
       new Thread(new Runnable() {
           @Override
           public void run() {
               Message msg = Message.obtain();
               msg.what = MSG_SUB_TO_MAIN;
               msg.obj = "这是一个来自子线程的消息";
               // 2.发送消息
               mHandler.sendMessage(msg);
           }
       }).start();
    }
}
```
这样就完成子线程向主线程发送消息。
如果想要主线程向子线程发送消息是否也只要在子线程中创建Handler对象，然后在主线程中拿到子线程的Handler以后，调用sendMessage发送消息。
```

public class MainActivity extends Activity {
    private static final String TAG = "MainActivity";
    private Handler mHandler;
    private static final int MSG_SUB_TO_MAIN= 100;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        // 1.创建Handler，并重写handleMessage方法
        // 创建一个子线程，并在子线程中创建一个Handler，且重写handleMessage
              new Thread(new Runnable() {
                  @Override
                  public void run() {
                      subHandler = new Handler() {
                          @Override
                          public void handleMessage(Message msg) {
                              super.handleMessage(msg);
                              // 处理消息
                              switch (msg.what) {
                                  case MSG_MAIN_TO_SUB:
                                      Log.e(TAG, "接收到消息： " +  Thread.currentThread().getName() + ","+ msg.obj);
                                      break;
                                  default:
                                      break;
                              }
                          }
                      };
                  }
              }).start();

        findViewById(R.id.btn) .setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
              Message msg = Message.obtain();
              msg.what = MSG_MAIN_TO_SUB;
              msg.obj = "这是一个来自主线程的消息";
              // 主线程中发送消息
              mHandler.sendMessage(msg);
            }
        });
    }
}
```
![](/images/24bd46715e85f975e5da9507eed43c0e.webp)
原因说的是在使用Handler之前没有调用Looper.prepare()。既然如此我们给它加上Looper.prepare()和Looper.loop();
```
public class MainActivity extends Activity {
   @Override
     protected void onCreate(Bundle savedInstanceState) {
             ...
            // 1.创建Handler，并重写handleMessage方法
              new Thread(new Runnable() {
                  @Override
                  public void run() {
                      Looper.prepare(); 
                      subHandler = new Handler() {
                          @Override
                          public void handleMessage(Message msg) {
                              super.handleMessage(msg);
                              // 处理消息
                              switch (msg.what) {
                                  case MSG_MAIN_TO_SUB:
                                      Log.e(TAG, "接收到消息： " +  Thread.currentThread().getName() + ","+ msg.obj);
                                      break;
                                  default:
                                      break;
                              }
                          }
                      };
                    Looper.loop();
                  }
              }).start();
            ...
     }
}
```
### 1. 创建Handler对象
handler初始化部分源码:
```
public class Handler {
    ... 省略部分代码
    public Handler() {
        this(null, false);
    }

    public Handler(Callback callback, boolean async) {
      // 不相关代码
       ......
        //得到当前线程的Looper，其实就是调用的sThreadLocal.get
        mLooper = Looper.myLooper();
        // 如果当前线程没有Looper就报运行时异常
        if (mLooper == null) {
            throw new RuntimeException(
                "Can't create handler inside thread that has not called Looper.prepare()");
        }
        // 把得到的Looper的MessagQueue让Handler持有
        mQueue = mLooper.mQueue;
        // 初始化Handler的Callback，其实就是最开始图中的回调方法的2
        mCallback = callback;
        mAsynchronous = async;
    }
     ... 省略部分代码
}

```
从上面代码中我们了解到在一个线程中创建handle时会调用Looper.myLooper()方法：
```
public class Looper {
    ... 省略部分代码
    static final ThreadLocal<Looper> sThreadLocal = new ThreadLocal<Looper>();
    public static @Nullable Looper myLooper() {
        return sThreadLocal.get();
    }
    ... 省略部分代码
}
```
这里我们看到有一个ThreadLocal类。这个类的作用是干啥的呢？ThreadLocal是存放某个线程上下文的变量。
```
public class ThreadLocalTest {
    static ThreadLocal<String> mThreadLocal = new ThreadLocal<>();
    public static void main(String[] args) {
        Thread t1  = new Thread(new Runnable() {
            @Override
            public void run() {
                //设置线程1中本地变量的值
                mThreadLocal.set("local1");
                //调用打印方法
                print("thread1");
                //打印本地变量
                System.out.println("after remove : " + mThreadLocal.get());
            }
        });

        Thread t2  = new Thread(new Runnable() {
            @Override
            public void run() {
                //设置线程2中本地变量的值
                mThreadLocal.set("local2");
                //调用打印方法
                print("thread2");
                //打印本地变量
                System.out.println("after remove : " + mThreadLocal.get());
            }
        });

        t1.start();
        t2.start();
    }
    static void print(String str) {
        //打印当前线程中本地内存中本地变量的值
        System.out.println(str + " :" + mThreadLocal.get());
        //清除本地内存中的本地变量
        mThreadLocal.remove();
    }
}
```
输出结果为：
```
thread1 :local1
thread2 :local2
after remove : null
after remove : null
```
ThreadLocal提供了线程的局部变量，每个线程都可以通过set()和get()来对这个局部变量进行操作，但不会和其他线程的局部变量进行冲突，实现了线程的数据隔离。也就是说往ThreadLocal中填充的变量属于当前线程，该变量对其他线程而言是隔离的。

既然Looper.myLooper()方法调用了``sThreadLocal.get()``获得了空的Looper对象，说明我们并没有调用``sThreadLocal.set()``方法给ThreadLocal赋值，找到sThreadLocal的set赋值函数：
```
public class Looper {
    ... 省略部分代码
       public static void prepare() {
           prepare(true);
       }
       private static void prepare(boolean quitAllowed) {
           if (sThreadLocal.get() != null) {
               throw new RuntimeException("Only one Looper may be created per thread");
           }
           sThreadLocal.set(new Looper(quitAllowed));
       }
    ... 省略部分代码
}
```
我们看到要调用Looper的prepare方法就是可以给sThreadLocal赋值。
好了，到这里我们就知道怎么解决刚才的子线程报错的问题了。就是我们在初始化Handler时没有调用Looper的prepare方法给线程初始化Looper对象导致的，因此做出如下修改：
```
public class MainActivity extends Activity {
   @Override
     protected void onCreate(Bundle savedInstanceState) {
             ...
            // 1.创建Handler，并重写handleMessage方法
              new Thread(new Runnable() {
                  @Override
                  public void run() {
                      Looper.prepare(); 
                      subHandler = new Handler() {
                          @Override
                          public void handleMessage(Message msg) {
                              super.handleMessage(msg);
                              // 处理消息
                              switch (msg.what) {
                                  case MSG_MAIN_TO_SUB:
                                      Log.e(TAG, "接收到消息： " +  Thread.currentThread().getName() + ","+ msg.obj);
                                      break;
                                  default:
                                      break;
                              }
                          }
                      };
                  }
              }).start();
            ...
     }
}
```


通过ThreadLocal.get获取到当前线程的looper（所以如果一个线程没有初始化过looper就报运行时异常），  通过Looper对象获取到MessagQueue对象让Handler持有，设置处理回调的Callback对象。

Handler的创建过程主要有以下几点:
1. 创建Handler对象。
2. 得到当前线程的Looper对象，并判断是否为空。
3. 让创建的Handler对象持有Looper、MessageQueu、Callback的引用。


使用Handler通信之前需要有以下四步：
- 调用Looper.prepare()
- 创建Handler对象
- 调用Looper.loop()
- handler发送消息

### 1. 创建Handler对象
在一个线程中创建handle时会通过Looper.myLooper()获取到``当前线程的looper``（所以如果一个线程没有初始化过looper就报运行时异常）。Looper对象会持有MessagQueue对象，
通过Looper可以获取到MessagQueue对象让Handler持有。并且设置处理回调的Callback对象。

handler初始化部分源码:
```
public class Handler {
    ···
    public Handler() {
        this(null, false);
    }
    public Handler(Callback callback, boolean async) {
      // 不相关代码
       ......
        //得到当前线程的Looper，其实就是调用的sThreadLocal.get
        mLooper = Looper.myLooper();
        // 如果当前线程没有Looper就报运行时异常
        if (mLooper == null) {
            throw new RuntimeException(
                "Can't create handler inside thread that has not called Looper.prepare()");
        }
        // 把得到的Looper的MessagQueue让Handler持有
        mQueue = mLooper.mQueue;
        // 初始化Handler的Callback
        mCallback = callback;
        mAsynchronous = async;
    }
    ···
}
```
Handler的创建过程主要有以下几点:
1. 创建Handler对象。
2. 得到当前线程的Looper对象，并判断是否为空。
3. 让创建的Handler对象持有Looper、MessageQueu、Callback对象的引用。

### 2. Looper.prepare()
一个线程最多只有一个Looper对象。在线程里通过Looper.prapre()生成looper对象，当没有Looper对象时，去创建一个Looper，并存放到ThreadLocal中。
ThreadLocal存储了Looper对象的副本，并且可以通过它取得当前线程在之前存储的Looper的副本。looper对象的构造函数中会创建MessageQueue()对象。
Looper将持有MessageQueue对象。
Looper.prepare()源码:
```
public class Looper {
    public static void prepare() {
        prepare(true);
    }

    private static void prepare(boolean quitAllowed) {
        // 规定了一个线程只有一个Looper，也就是一个线程只能调用一次Looper.prepare()
        if (sThreadLocal.get() != null) {
            throw new RuntimeException("Only one Looper may be created per thread");
        }
        // 如果当前线程没有Looper，那么就创建一个，存到sThreadLocal中
        sThreadLocal.set(new Looper(quitAllowed));
    }
}
```
Looper的构造方法源码:
```
public class Looper {
   private Looper(boolean quitAllowed) {
        // 创建了MessageQueue，并供Looper持有
        mQueue = new MessageQueue(quitAllowed);
        // 让Looper持有当前线程对象
        mThread = Thread.currentThread();
    }
}
```

Looper.prepare()的作用主要有以下三点：
1. 为当前线程创建Looper对象。
2. 创建MessageQueue对象，并让Looper对象持有。
3. 让Looper对象持有当前线程。


###### 为何在android主线程中没有调用Looper.prepare()也可以在在主线程中使用handler？
原因是android主线程在ActivityThread.main方法中调用了Looper.prepare，所以在android主线程中无需再调用Looper.prapre()方法。
ActivityThread.main部分源码:
```
 public static void main(String[] args) {
       // 不相干代码
       ......
       // 1.调用Looper.prepareMainLooper，其实也就是调用的Looper.loop，初始化Looper、MessageQueue等
       Looper.prepareMainLooper();
       // 2.创建ActivityThread的同时，初始化了成员变量Handler mH
       ActivityThread thread = new ActivityThread();
       thread.attach(false);
       // 
       if (sMainThreadHandler == null) {
           // 把创建的Handler mH赋值给sMainThreadHandler
           sMainThreadHandler = thread.getHandler();
       }

       if (false) {
           Looper.myLooper().setMessageLogging(new
                   LogPrinter(Log.DEBUG, "ActivityThread"));
       }
       // 3.调用Looper.loop()方法，开启死循环，从MessageQueue中不断取出Message来处理
       Looper.loop();

       throw new RuntimeException("Main thread loop unexpectedly exited");
   }
```


### 3. Looper.loop()
Looper.loop()也会检查当前线程是否有Looper，然后通过Looper对象得到当前线程的MessageQueue。Looper.loop()会开启一个死循环，不断的从Looper对象的MessageQueue的next方法取出MessageQueue中的Message，然后使用message的target（实际上就是handler）进行分发。当MessageQueue中没有消息时，next方法会阻塞，导致当前线程挂起。

Looper.loop()部分源码:
```
 public static void loop() {
        // 得到当前线程的Looper对象
        final Looper me = myLooper();
        if (me == null) {
            throw new RuntimeException("No Looper; Looper.prepare() wasn't called on this thread.");
        }
        // 得到当前线程的MessageQueue对象
        final MessageQueue queue = me.mQueue;
        
        // 无关代码
        ......
        
        // 死循环
        for (;;) {
            // 不断从当前线程的MessageQueue中取出Message，当MessageQueue没有元素时，方法阻塞
            Message msg = queue.next(); // might block
            if (msg == null) {
                // No message indicates that the message queue is quitting.
                return;
            }
            // Message.target是Handler，其实就是发送消息的Handler，这里就是调用它的dispatchMessage方法
            msg.target.dispatchMessage(msg);
            // 回收Message
            msg.recycleUnchecked();
        }
    }
```
handler分发消息源码:
```
/*
这里我们看到，mLooper()方法里我们取出了，当前线程的looper对象，然后从looper对象开启了一个死循环 
不断地从looper内的MessageQueue中取出Message，只要有Message对象，就会通过Message的target调用
dispatchMessage去分发消息，通过代码可以看出target就是我们创建的handler。我们在继续往下分析Message的分发
*/
public void dispatchMessage(Message msg) {
    if (msg.callback != null) {
        handleCallback(msg);
    } else {
        if (mCallback != null) {
            if (mCallback.handleMessage(msg)) {
                return;
            }
        }
        handleMessage(msg);
    }
}
/*好了，到这里已经能看清晰了
可以看到，如果我们设置了callback（Runnable对象）的话，则会直接调用handleCallback方法
*/
private static void handleCallback(Message message) {
        message.callback.run();
    }
//即，如果我们在初始化Handler的时候设置了callback（Runnable）对象，则直接调用run方法。比如我们经常写的runOnUiThread方法：
runOnUiThread(new Runnable() {
            @Override
            public void run() {
                
            }
        });
public final void runOnUiThread(Runnable action) {
      if (Thread.currentThread() != mUiThread) {
          mHandler.post(action);
      } else {
          action.run();
      }
  }
  /*
而如果msg.callback为空的话，会直接调用我们的mCallback.handleMessage(msg)，即handler的handlerMessage方法。由于Handler对象是在主线程中创建的，
所以handler的handlerMessage方法的执行也会在主线程中。
```


### 4. handler发送消息
Handler的sendMessage方法：
```
 public final boolean sendMessage(Message msg)
    {
        return sendMessageDelayed(msg, 0);
    }

    public final boolean sendMessageDelayed(Message msg, long delayMillis)
    {
        if (delayMillis < 0) {
            delayMillis = 0;
        }
        return sendMessageAtTime(msg, SystemClock.uptimeMillis() + delayMillis);
    }

    public boolean sendMessageAtTime(Message msg, long uptimeMillis) {
        // 这里拿到的MessageQueue其实就是创建handler时的MessageQueue，默认情况是当前线程的Looper对象的MessageQueue
        // 也可以指定
        MessageQueue queue = mQueue;
        if (queue == null) {
            RuntimeException e = new RuntimeException(
                    this + " sendMessageAtTime() called with no mQueue");
            Log.w("Looper", e.getMessage(), e);
            return false;
        }
        // 调用enqueueMessage，把消息加入到MessageQueue中
        return enqueueMessage(queue, msg, uptimeMillis);
    }
```
首先看看handler的enqueueMessage的实现，看看该方法：
```
    private boolean enqueueMessage(MessageQueue queue, Message msg, long uptimeMillis) {
        // 把当前Handler对象，也就是发起消息的handler作为Message的target属性
        msg.target = this;
        if (mAsynchronous) {
            msg.setAsynchronous(true);
        }
        // 调用MessageQueue中的enqueueMessage方法
        return queue.enqueueMessage(msg, uptimeMillis);
    }
```
这里把当前Handler设为Message的target属性，方便Looper从MessageQueue中取出Message时进行消息分发的处理。然后调用了MessageQueue的enqueueMessage方法，把handler发送的消息加入到MessageQueue，供Looper去取出来处理。
MessageQueue的enqueueMessage方法：
```
 boolean enqueueMessage(Message msg, long when) {
        if (msg.target == null) {
            throw new IllegalArgumentException("Message must have a target.");
        }
        // 一个Message，只能发送一次
        if (msg.isInUse()) {
            throw new IllegalStateException(msg + " This message is already in use.");
        }

        synchronized (this) {
            if (mQuitting) {
                IllegalStateException e = new IllegalStateException(
                        msg.target + " sending message to a Handler on a dead thread");
                Log.w("MessageQueue", e.getMessage(), e);
                msg.recycle();
                return false;
            }
            // 标记Message已经使用了
            msg.markInUse();
            msg.when = when;
            // 得到当前消息队列的头部
            Message p = mMessages;
            boolean needWake;
            // 当前队列没有其他需要发送的Message。
            //或者当前新添加进来的的Message的时间点为0（即需要立即发送的消息）。
            //或者当前新添加进来的的Message需要发送的时间点小与当前MessageQueue队列头部Message的时间点（即当前添加进来的Message需要在当前MessageQueue队列头部Message之前被发送）时就会将当前新添加的Message插入到了MessageQueue的队首。
            //我们这里when为0，表示立即处理的消息
            if (p == null || when == 0 || when < p.when) {
                // 把消息插入到消息队列的头部
                msg.next = p;
                mMessages = msg;
                needWake = mBlocked;
            } else {
                // 根据需要把消息插入到消息队列的合适位置，通常是调用xxxDelay方法，延时发送消息
                needWake = mBlocked && p.target == null && msg.isAsynchronous();
                Message prev;
                for (;;) {
                    prev = p;
                    p = p.next;
                    if (p == null || when < p.when) {
                        break;
                    }
                    if (needWake && p.isAsynchronous()) {
                        needWake = false;
                    }
                }
                // 把消息插入到合适位置
                msg.next = p; // invariant: p == prev.next
                prev.next = msg;
            }

            // 如果队列阻塞了，则唤醒
            if (needWake) {
                nativeWake(mPtr);
            }
        }
        return true;
    }
```
首先，判断了Message是否已经使用过了，如果使用过，则直接抛出异常，这是可以理解的，如果MessageQueue中已经存在一个Message，但是还没有得到处理，这时候如果再发送一次该Message，可能会导致处理前一个Message时，出现问题。

然后，会判断when，它是表示延迟的时间，我们这里没有延时，所以为0，满足if条件。把消息插入到消息队列的头部。如果when不为0，则需要把消息加入到消息队列的合适位置。

最后会去判断当前线程是否已经阻塞了，如果阻塞了，则需要调用本地方法去唤醒它。

handler发送消息的本质都是：把Message加入到Handler中的MessageQueue中去。


### 主线程中的Looper.loop()为什么不会造成ANR?
显而易见的，如果main方法中没有looper进行循环，那么主线程一运行完毕就会退出。这还玩个蛋啊！

总结：ActivityThread的main方法主要就是做消息循环，一旦退出消息循环，那么你的应用也就退出了。

我们知道了消息循环的必要性，那为什么这个死循环不会造成ANR异常呢？

因为Android 的是由事件驱动的，looper.loop() 不断地接收事件、处理事件，每一个点击触摸或者说Activity的生命周期都是运行在 Looper.loop() 的控制之下，如果它停止了，应用也就停止了。只能是某一个消息或者说对消息的处理阻塞了 Looper.loop()，而不是 Looper.loop() 阻塞它。

也就说我们的代码其实就是在这个循环里面去执行的，当然不会阻塞了。

 

Activity的生命周期都是依靠主线程的Looper.loop，当收到不同Message时则采用相应措施。

如果某个消息处理时间过长，比如你在onCreate(),onResume()里面处理耗时操作，那么下一次的消息比如用户的点击事件不能处理了，整个循环就会产生卡顿，时间一长就成了ANR。

让我们再看一遍造成ANR的原因，你可能就懂了。

造成ANR的原因一般有两种：

    当前的事件没有机会得到处理（即主线程正在处理前一个事件，没有及时的完成或者looper被某种原因阻塞住了）
    当前的事件正在处理，但没有及时完成
而且主线程Looper从消息队列读取消息，当读完所有消息时，主线程阻塞。子线程往消息队列发送消息，并且往管道文件写数据，主线程即被唤醒，从 管道文件读取数据，主线程被唤醒只是为了读取消息，当消息读取完毕，再次睡眠。因此loop的循环并不会对CPU性能有过多的消耗。

总结：Looer.loop()方法可能会引起主线程的阻塞，但只要它的消息循环没有被阻塞，能一直处理事件就不会产生ANR异常。


在Handler机制中，每一个线程有一个Looper，Looper.loop()一直无限循环，为什么没有造成ANR呢？

首先得知道造成ANR的根本原因是：

1.在5秒内没有响应输入的事件（例如，按键按下，屏幕触摸）

2.BroadcastReceiver在10秒内没有执行完毕

造成以上两点的原因有很多，比如在主线程中做了非常耗时的操作，比如说是下载，io异常等。

再看Android主线程：

Java程序我们都知道，入口从main()方法执行，安卓用java，也不例外，入口从ActivityThread的main()；

在main()里执行Looper.loop(),如果Looper不死循环，主线程执行完，就结束了，那APP还有存在意义吗？

造成ANR的不是主线程阻塞，而是主线程的Looper消息处理过程发生了任务阻塞，无法响应手势操作，不能及时刷新UI。

主线程每隔16ms发送一个消息，用于刷新重绘UI，如果这个消息没有及时的消费，那么页面就会有卡顿感，严重的就是Application Not Resposing。


参考资料:
[图解Handler机制](https://www.jianshu.com/p/592fb6bb69fa)
[Handler课后题](https://www.jianshu.com/p/9631eebadd5c)
[Android Handler消息机制原理最全解读（持续补充中）](https://blog.csdn.net/wsq_tomato/article/details/80301851)
[Handler进阶之sendMessage原理探索](https://blog.csdn.net/wsq_tomato/article/details/80893990)
[解析Android中Handler机制原理](https://blog.51cto.com/14347056/2398080?source=dra)
[Handler相关面试题你答对多少？怎样清晰表达拿下面试官？](http://blog.itpub.net/69952849/viewspace-2678752/)
[Android Handler机制](https://segmentfault.com/a/1190000022843928)
[Android Handler机制彻底梳理](https://www.cnblogs.com/webor2006/p/11630538.html)
[一文读懂Handler机制](https://mp.weixin.qq.com/s/C2Q8kfeIOFkrKg82cMYDAg)


