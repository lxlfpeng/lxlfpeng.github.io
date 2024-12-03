---
title: Android后台任务Services和WorkManager总结
date: 2022-09-18
categories: 
  - Android开发
---

# Android后台服务限制
Android O对应用在后台运行时可以执行的操作施加了限制，称为``后台执行限制（Background Execution Limits）``，这可以大大减少应用的内存使用和耗电量，提高用户体验。后台执行限制分为两个部分：`` 后台服务限制（Background Service Limitations）、 广播限制（BroadcastLimitations）``。
除了下面情况外都是后台应用:
1. 具有可见的Activity
2. 具有前台服务
3. 另一个前台应用已关联到该应用（通过bindService或者使用该应用的ContentProvider）。

应用在后台期间保留其后台服务的能力将受到限制。如果应用处于后台时调用了`` startService() ``将会抛出`` IllegalStateException ``，除非：
- **应用已经处于前台，则可以调用 ``startService()``，不会抛出`` IllegalStateException ``**，但一旦进入后台，后台应用将被置于一个**临时白名单**中，位于白名单中时，在这段时间内，``应用可以无限制地启动服务，其后台服务也可以运行``。但这个时间期一过(Nexus 5X 8.0 系统上测试不到1分钟)，应用就会进入空闲状态，后台服务就会被销毁。

因此，通过startservices启动的服务有如下特点:
1. 在后台运行的服务在几分钟内会被stop掉（模拟器测试在1分钟左右后被kill掉）。在这段时间内，应用仍可以创建和使用服务。
2. 在应用处于后台几分钟后（模拟器测试1分钟左右），应用将不能再通过startService创建后台服务，如果创建则抛出以下异常
```
Caused by: java.lang.IllegalStateException: Not allowed to start service Intent { cmp=com.example.xxxx.test/.TestService }: app is in background
```
> 也就是说，当你的应用不在前台，时间窗结束后，会变成闲置状态，系统就杀死你的后台服务。网上一系列Service保活，创建永不停止Service，经过验证，都已失效。即你无法在使用后台服务在后台偷偷执行需要长时间的任务，例如监控GPS状态，记录步数等等。限制后台服务使用的原因是，当你的app使用服务在后台运行时，你的app消耗了宝贵的资源：- 内存 - 电池。最佳的做法是：操作完成后，服务应自行停止。许多应用程序具有长时间运行的后台服务，这些服务基本上运行无限时间以维持与服务器的Socket连接或监视某些任务或用户活动。这些服务会导致电池耗尽，并且还会不断消耗内存。鉴于以上原因：后台服务已经无法再在后台执行长时间任务。安卓推出了以下方案来解决此类问题:

- **前台服务**Android 8.0 引入了一种全新的方法，即Context.startForegroundService()，以在前台启动新服务。在系统创建服务后，应用有五秒的时间来调用该服务的startForeground() 方法以显示新服务的用户可见通知。如果应用在此时间限制内未调用
startForeground()，则系统将停止服务并声明此应用为 ANR。
- **WorkManager**:WorkManager适用于那些即使应用程序退出，系统也能够保证这个任务正常运行的场景，比如将应用程序数据上传到服务器。它不适用于应用进程内的后台工作，如果应用进程消失，就可以安全地终止。
- **JobScheduler:** JobScheduler 作业替换后台服务。 例如，CoolPhotoApp需要检查用户是否已经从朋友那里收到共享的照片，即使该应用未在前台运行。

# 前台服务
对于需要立即运行并且必须执行完毕的由用户发起的工作，请使用[前台服务](https://developer.android.com/guide/components/services)。使用前台服务可告知系统应用正在执行重要任务，不应被终止。前台服务通过通知栏中的不可关闭通知向用户显示。
1. 修改启动方式
```
Intent service = new Intent(this, MyBackgroundService.class);
service.putExtra("startType", 1);
if (Build.VERSION.SDK_INT >= 26) {
    startForegroundService(service);
} else {
    startService(service);
}
```
2. 启动完前台service, 一定记得在5s以内要执行startForeground方法，不然就会出现ANR。
```
public class MyBackgroundServiceextends Service {

    @Override
    public void onCreate() {
        super.onCreate();

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            //适配安卓8.0
            String channelId = getChannelId() + "";
            String channelName = getChannelName();
            NotificationChannel channel = new NotificationChannel(channelId, channelName,
                    NotificationManager.IMPORTANCE_MIN);
            NotificationManager manager = (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);
            manager.createNotificationChannel(channel);
            startForeground(getChannelId(), getNotification());
        }
    }
    ...
}

```
一样还是先判断系统版本, 如果高于26就调用startForeground方法好了, 使用startForegroundService 方法启动后台service这么使用即可。不过这样会在通知栏里面弹出弹出通知。

# WorkManager
WorkManager适用于那些即使应用程序退出，系统也能够保证这个任务正常运行的场景，比如将应用程序数据上传到服务器。它不适用于应用进程内的后台工作，如果应用进程消失，就可以安全地终止
WorkManager 不适用于需要在特定时间触发的任务，也不适用立即任务。针对特定时间触发的任务使用 AlarmManager，立即执行的任务使用 ForegroundService。
WorkManager适用于那些在应用退出之后任务还需要继续执行的需求(比如应用数据上报服务器的情况)，对应那些在应用退出的之后任务也需要终止的情况就需要选择ThreadPool、AsyncTask来实现。
对于可延迟的工作以及预计即使您的设备或应用重启也会运行的工作，请使用[WorkManager](https://developer.android.com/topic/libraries/architecture/workmanager)。WorkManager 是一个 Android 库，可在满足工作的条件（例如网络可用性和电源）时妥善运行可延迟的后台工作。
WorkManager 提供向后兼容的 API（兼容 API 级别 14 及更高级别），利用[`JobScheduler`](https://developer.android.com/reference/android/app/job/JobScheduler)API（API 级别 23 及更高级别）帮助优化更低级别设备上的电池续航时间、批量作业以及[`AlarmManager`](https://developer.android.com/reference/android/app/AlarmManager)和[`BroadcastReceiver`](https://developer.android.com/reference/android/app/BroadcastReceiver)的组合。
WorkManager是一个用于排队可延迟工作的库，保证在满足约束条件后的某个时间执行。 WorkManager允许观察工作状态和创建复杂工作链的能力。
WorkManager旨在通过为系统驱动的后台处理提供一流的API来简化开发人员体验。它适用于即使应用程序不再位于前台也应运行的后台作业。在可能的情况下，它使用JobScheduler或Firebase JobDispatcher来完成工作; 如果你的应用程序在前台，它甚至会尝试直接在你的过程中完成工作。
应用场景：每15分钟跟踪用户位置
> WorkManager 和AsyncTask, ThreadPool, RxJava的区别:这三个和WorkManager并不是替代的关系. 这三个工具, 能帮助你在应用中开后台线程干活, 但是应用一被杀或被关闭, 这些工具就干不了活了. 而WorkManager不是, 它在应用被杀, 甚至设备重启后仍能保证你安排给他的任务能得到执行.

### 定义 Worker
咱们定义 MainWorker 继承 Worker，发现须要重写 doWork 方法，而且须要返回任务的状态 WorkerResult：
```
class MainWorker : Worker() {
    override fun doWork(): WorkerResult {
        // 要执行的任务
        return WorkerResult.SUCCESS
    }
}
```
### 定义 WorkRequest
在 MainActivity 中定义 WorkRequest：
```
val request = OneTimeWorkRequest.Builder(MainWorker::class.java).build()
```
OneTimeWorkRequest 意味着这个任务只需执行一遍。

### 加入任务队列
要让任务执行，须要将 WorkRequest 加入任务队列：
```
WorkManager.getInstance().enqueue(request)
```

# AlarmManager
如果您需要在确切的时间运行某项作业，请使用[`AlarmManager`](https://developer.android.com/reference/android/app/AlarmManager)。`AlarmManager`会在您指定的时间启动应用（如有必要），以便运行该作业。但是，如果您的作业不需要在确切的时间运行，则`WorkManager`是更好的选择；`WorkManager`能更好地平衡系统资源。例如，如果您需要大约每小时运行一次某项作业，但不需要在特定时间运行该作业，则应使用`WorkManager`设置周期性作业。

# DownloadManager
如果您的应用执行长时间运行的 HTTP 下载，请考虑使用[DownloadManager](https://developer.android.com/reference/android/app/DownloadManager)。客户端可能会请求将 URI 下载到位于应用进程之外的特定目标文件中。内容下载管理器会在后台执行下载操作，它负责处理 HTTP 互动，在下载失败或连接发生更改以及系统重新启动后重新尝试下载。

# 后台任务选择
|场景|推荐|
|-|-|
| 需系统触发，不必完成  | ThreadPool + Broadcast |
| 需系统触发，必须完成，可推迟  | WorkManager |
| 需系统触发，必须完成，立即  | ForegroundService + Broadcast |
| 不需系统触发，不必完成  | ThreadPool|
| 不需系统触发，必须完成，可推迟  | WorkManager|
| 不需系统触发，必须完成，立即  | ForegroundService|

参考资料:
[Android Jetpack - 使用 WorkManager 管理后台任务](https://www.jianshu.com/p/e495ee6e84de)
[Android后台Service已死 WorkManager崛起](https://blog.csdn.net/Sunxiaolin2016/article/details/97266490)
[Android P后台服务被终止，创建永不终止的后台服务](https://blog.csdn.net/Sunxiaolin2016/article/details/97128681)
[Android后台任务](https://www.cnblogs.com/liguo-wang/p/13140034.html)
[学习Android Jetpack? 实战和教程这里全都有！](https://juejin.im/post/5d2be05ff265da1bd605d49a)
[Android Jetpack - 使用 WorkManager 管理后台任务](https://blog.csdn.net/a49220824/article/details/80869182)
[Android 手机运存越来越大，为什么后台应用还是会被「杀」？](https://sspai.com/post/56818)
