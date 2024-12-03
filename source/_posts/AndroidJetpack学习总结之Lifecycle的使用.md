---
title: AndroidJetpack学习总结之Lifecycle的使用
---

# 一.Lifecycle为何被创造出来
在Android开发中我们必备的基础知识就是掌握Activity.Fragment的生命周期.在不同的生命周期中我们做不同的操作.如果是在Activity我们是很容易感知到其生命周期的变化的.但是在Activity之外要与Activity生命周期绑定就比较麻烦,必须要在Activity对应的生命周期中调用该类的方法才能实现.例如:我们在使用MVP架构时,我们的Activity关闭时必须要将网络请求移除.所以我们在Presenter中会定义一个onFinish(),当Activity关闭时我们在其onDestroy()调用Presenter的onFinish()来通知Presenter我们的Activity关闭了.常规的方式就是这样,这样做有什么问题吗?显然时没有的.但是这样做的弊端在哪?其一:每一个Activity的onDestroy()调用Presenter的onFinish(),如果自己忘写了,就坑爹了.其二我们在Activity的onDestroy()方法里面还有其他的类需要做处理例如:定位功能等.如果都写道Activity对应的生命周期中就会显得很臃肿,不利于维护.针对于这种情况.google在2017的开发者大会上推出Lifecycle组件来解决此类问题?
# 二.Lifecycle的定义
lifecycle是androidx的一个框架库，实现与Activity/Fragment等View的生命周期的同步处理。activity 和fragment 是有声明周期的，有时候，我们的很多操作需要写在声明周期的方法中，比如，  下载，文件操作等，这样很多情况下回导致，我们在activity中的声明周期方法中写越来越多的代码，  activity或者fragment 越来越臃肿，代码维护越来越困难。 使用lifecycle就可以很好的解决这类问题。lifecycle代码简洁，我们可以通过实现LifecycleObserver 接口，来监听声明周期，  然后我们在activity和fragment中去注册监听。
# 三.Lifecycle如何使用
####  1.添加依赖：在app或者module目录下的build.gradle中，添加依赖：
```
dependencies {
    ......
    implementation "android.arch.lifecycle:extensions:1.1.1"
    // 如果你使用java8开发，可以添加这个依赖，里面只有一个类
    implementation "android.arch.lifecycle:common-java8:1.1.1"
}
```
#### 2.实现LifecycleObserver接口
- java7中
```
public class Java7Observer implements LifecycleObserver {
    private static final String TAG = Java7Observer.class.getSimpleName();

    @OnLifecycleEvent(Lifecycle.Event.ON_CREATE)
    public void onCreate() { Log.d(TAG, "onCreate"); }

    @OnLifecycleEvent(Lifecycle.Event.ON_START)
    public void onStart() { Log.d(TAG, "onStart"); }

    @OnLifecycleEvent(Lifecycle.Event.ON_RESUME)
    public void onResume() { Log.d(TAG, "onResume"); }

    @OnLifecycleEvent(Lifecycle.Event.ON_PAUSE)
    public void onPause() { Log.d(TAG, "onPause"); }

    @OnLifecycleEvent(Lifecycle.Event.ON_STOP)
    public void onStop() { Log.d(TAG, "onStop"); }

    @OnLifecycleEvent(Lifecycle.Event.ON_DESTROY)
    public void onDestroy() { Log.d(TAG, "onDestroy"); }
}
```

- java8中
```
   public class Java8Observer implements DefaultLifecycleObserver {
       private static final String TAG = Java8Observer.class.getSimpleName();
   
       @Override
       public void onCreate(@NonNull LifecycleOwner owner) { Log.d(TAG, "onCreate"); }
   
       @Override
       public void onStart(@NonNull LifecycleOwner owner) { Log.d(TAG, "onStart"); }
   
       @Override
       public void onResume(@NonNull LifecycleOwner owner) { Log.d(TAG, "onResume"); }
   
       @Override
       public void onPause(@NonNull LifecycleOwner owner) { Log.d(TAG, "onPause"); }
   
       @Override
       public void onStop(@NonNull LifecycleOwner owner) { Log.d(TAG, "onStop"); }
   
       @Override
       public void onDestroy(@NonNull LifecycleOwner owner) { Log.d(TAG, "onDestroy"); }
   }
```
#### 3.将LifecycleObserver添加到Lifecycle的观察者列表
```
public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        // 直接调用getLifecycle()，添加Observer
        getLifecycle().addObserver(new Java7Observer());
        getLifecycle().addObserver(new Java8Observer());
    }
}
#### 4.查看执行结果
```
![执行结果](https://upload-images.jianshu.io/upload_images/3067896-78039b72daecdcfe.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

问题1：它是什么？

ActivityLifecycleCallBacks是Application的一个内部接口，一般用于APP的Application类，让我们自定义的Application实现它；



问题2：原理:

     Activity 的每一个生命周期都对应 ActivityLifecycleCallbacks 接口中的一个方法，比如 onActivityCreated 回调是在 Activity 的 onCreate 方法中调用 getApplication().dispatchActivityCreated(this, savedInstanceState) 完成对 Activity 生命周期跟踪监听。

问题3: 使用时需要注意什么？

     要求 API 14+

问题4：为什么要用它？

     我们的Application实现ActivityLifecycleCallbacks接口后，系统会在每个Activity执行完对应的生命周期后，调用这个类中所有实现的方法；

问题5：使用场景

应用新开进程假重启处理（低内存回收、修改权限）

管理 Activity 页面栈

获取当前 Activity 页面

判断应用前后台

保存恢复状态值 savedInstanceState

页面分析统计埋点



使用场景一：管理Activity，随时随地退出程序，避免退出程序后，之前进入第三方库的Activity未被销毁清除的情况；

                       我们一般在项目中让我们的Activity都继承自BaseActivity，但是有时APP存在打开第三方库Activity的情况，在这

                       种情况下，在BaseActivity的onCreate方法将activity添加到集合中，在onDestory方法中将集合清除，这就出现内存泄露。

                       ActivityLifecycleCallbacks 就派上用场了, App 中的所有 Activity 只要执行完生命周期就一定会调用这个接口实现类的对

                       应方法, 那你就可以在 onActivityCreated 中将所有 Activity 加入集合,这样不管你是不是三方的 Activity 我都可以遍历集

                       合 finish 所有的 Activity

使用场景二：判断APP前后台状态

                       判断应用是否在后台运行，针对前后台运行会做一些处理，比如提示用户应用运行在后台、以及应用前后台切换回

                       调通知等。利用通过监听回调方法 onActivityStarted与onActivityStopped两个方法来判断应用前后台

使用场景三:  应用新开进程假重启处理（低内存回收、修改权限）

                       应用在低内存的情况下退出重新启动，并不会执行正常的启动流程，而是创建新的进程，直接还原上一次的操作页

                       面,导致页面栈信息丢失，页面显示以及返回跳转异常；MainActivity 可能没有执行，部分功能不会初始化。

                       当前操作页面：LoginActivity

                       正常启动使用流程：SplashActivity -> MainActivity -> LoginActivity

                       低内存重启流程：新开进程，直接启动 LoginActivity

                       低内存重启流程存在的问题：页面栈信息丢失，页面显示以及返回跳转异常；MainActivity 可能没有执行，部分功能

                       不会初始化。

解决思路:

                       通过监听回调方法 onActivityCreated，判断应用启动的第一个 Activity 页面是否为 LauncherActivity，如果不是，则强

                       制启动LauncherActivity 来执行正常的启动流程。

使用场景四:

                       获取当前 Activity 页面 

                       通过监听回调方法 onActivityResumed，设置当前 Activity 页面(不常用,React Native 开发会用到)

使用场景五:

                       保存恢复状态值 savedInstanceState

                       Activity 异常退出经常需要保存恢复一些数据，ActivityLifecycleCallbacks 实现数据保存恢复也是比较简单的。 

                      通过监听回调方法onActivityCreated与onActivitySaveInstanceState保存恢复状态值

使用场景六:

                      页面分析统计埋点

                      页面信息统计

[我一行代码都不写实现Toolbar!你却还在封装BaseActivity?](https://juejin.im/post/6844903477169111047#heading-12)


参考:
[Android-Lifecycle超能解析-生命周期的那些事儿](https://www.jianshu.com/p/2c9bcbf092bc)
[硬核讲解 Jetpack 之 LifeCycle 源码篇](https://www.cnblogs.com/bingxinshuo/p/12089035.html)



