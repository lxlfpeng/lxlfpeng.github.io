---
title: 网页拉起Android应用实现
---

# 
- 如果目标App没有启动，那么就拉起App,并跳转到App内指定页面
- 如果目标App已经启动，那么就把App拉到前台并跳转App内指定页面

命令行adb测试deeplink
  直接使用命令行adb测试deeplink，使用命令：
```
adb shell am start -a android.intent.action.VIEW -d "rsdkdemo://rs.com/test?referer=Deeplink_Test"
```
# 方式一
## 将MainActivity设置为scheme接受方,并且设置launchMode
```
<activity
    android:name="com.example.imageloader.MainActivity"
    android:exported="true"
    android:launchMode="singleTask">
    <intent-filter>
        <action android:name="android.intent.action.VIEW" />
         <category android:name="android.intent.category.DEFAULT" />
        <category android:name="android.intent.category.BROWSABLE" />
         <data
            android:host="rs.com"
            android:pathPrefix="/test"
            android:scheme="rsdkdemo" />
    </intent-filter>
</activity>
```
## SplashActivity跳转MainActivity在Intent中增加一个参数
```
class SplashActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_splash)
        Handler(Looper.getMainLooper()).postDelayed({
            val mainIntent = Intent(this, MainActivity::class.java)
            //读取到传递过来的intent数据再次将其传递到MainActivity
            if (getIntent() != null && getIntent().data != null) {
                mainIntent.data = getIntent().data
            }
            mainIntent.putExtra(IS_SPLASH_LANCHER, true)
            startActivity(mainIntent)
            finish()
        }, 2000)
    }

    companion object {
        val IS_SPLASH_LANCHER = "is_splash_lancher"
    }
}
```
## 在Mainactivity中进行判断
```
class MainActivity : AppCompatActivity() {
    override fun onNewIntent(intent: Intent?) {
        super.onNewIntent(intent)
        schemeIntent(intent)
    }
    
    /**
     * 处理intent的值
     */
    private fun schemeIntent(intent: Intent?) {
        if (intent == null || intent.data == null) {
            return
        }
        //通过getIntent()获取到MainActivity是否是从SplashActivity过来的
        if (!getIntent().getBooleanExtra(SplashActivity.IS_SPLASH_LANCHER, false)) {
            //不是SplashActivity过来的将要打开SplashActivity,并且将intent数据传递传递过去
            val splashIntent = Intent(this, SplashActivity::class.java)
            splashIntent.data = intent.data
            startActivity(splashIntent)
            finish()
        } else {
            val referer = intent.data?.getQueryParameter("referer") ?: "未找到值"
            if (referer == "Deeplink_Test") {
                startActivity(Intent(this, VideoActivity::class.java))
            }
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        schemeIntent(intent)
    }

}
```
# 方式二
## 在BaseApplication创建一个值来标识是否是通过SplashActivity进行初始化的
```
class BaseApplication : Application() {
    companion object {
        //app是否是通过SplashActivity进行初始化
        var is_app_init = false
    }
}
```
## SplashActivity中将BaseApplication中的标识赋值,并且将intent数据进行传递
```
class SplashActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_splash)
        Handler(Looper.getMainLooper()).postDelayed({
            val mainIntent = Intent(this, MainActivity::class.java)
            //读取到传递过来的intent数据再次将其传递到MainActivity
            if (getIntent() != null && getIntent().data != null) {
                mainIntent.data = getIntent().data
            }
            startActivity(mainIntent)
            //修改BaseApplication中的标识
            BaseApplication.is_app_init = true
            finish()
        }, 2000)
    }
    companion object {
        val IS_SPLASH_LANCHER = "is_splash_lancher"
    }
}
```
## 专门创建一个Activity来接受scheme
```
<activity
    android:name=".SchemeActivity"
    android:exported="true"
    android:launchMode="singleTask">
    <intent-filter>
        <action android:name="android.intent.action.VIEW" />
        <category android:name="android.intent.category.DEFAULT" />
        <category android:name="android.intent.category.BROWSABLE" />
        <data
            android:host="rs.com"
            android:pathPrefix="/test"
            android:scheme="rsdkdemo" />
    </intent-filter>
</activity>
```
## 在SchemeActivity写逻辑进行判断
```
class SchemeActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
      //  setContentView(R.layout.activity_scheme)
        schemeIntent(intent)
    }

    override fun onNewIntent(intent: Intent?) {
        super.onNewIntent(intent)
        schemeIntent(intent)
    }

    private fun schemeIntent(intent: Intent?) {
        if (intent == null || intent.data == null) {
            return
        }
        //app是否是通过SplashActivity进行初始化
        if (BaseApplication.is_app_init) {
            val referer = intent?.data?.getQueryParameter("referer") ?: "未找到值"
            if (referer.equals("Deeplink_Test")) {
                startActivity(Intent(this, VideoActivity::class.java))
            }
        } else {
            //打开SplashActivity并将数据进行传递
            val splashIntent = Intent(this, SplashActivity::class.java)
            splashIntent.data = intent.data
            startActivity(splashIntent)
        }
        finish()
    }
}
```
## 在MainActivity处理SplashActivity页面传递过来的数据内容
```
class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        //获取到传递过来的值然后进行跳转
        val referer = intent?.data?.getQueryParameter("referer") ?: "未找到值"
        if (referer.equals("Deeplink_Test")) {
            startActivity(Intent(this, VideoActivity::class.java))
        }
    }

}
```

# 总结
方式一:可以解决冷启动和App在后台在恢复到前台的情况,但是会有一个问题,app已经处于运行中的话会将当前的Activity挤掉,强制进入MainActivity中.
方式二:可以解决冷启动和App在后台在恢复到前台的情况,app已经处于运行中的话并不会关闭之前打开的Activity任务栈.


# 参考资料
[Android Deeplink原理与应用](https://www.jianshu.com/p/11ef719a9281)
[Android Deeplink(二)](https://www.jianshu.com/p/3be82e1e65c2)
[Android中的DeepLink](https://blog.csdn.net/huideveloper/article/details/85219752)
[Android外部调用自身App(scheme DeepLink、AppLink详解)](https://www.jianshu.com/p/f061ab61618b)