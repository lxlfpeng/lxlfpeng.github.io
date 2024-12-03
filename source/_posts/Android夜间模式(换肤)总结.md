---
title: Android夜间模式(换肤)总结
---

# 一.Android 平台常见的换肤方案
Android 平台常见的额换肤方式总结起来有如下三种：
### 1.设置setTheme 主题来切换
- 原理：通过在values文件夹下的attrs.xml和style.xml文件中配置不同的风格的主题，在Activity中的onCreate()方法中，调用setContentView()方法前调用setTheme()方法来设置主题。
- 优点：利用系统自带的机制实现，根据标志位setTheme()即可。
- 缺点：在主题切换界面不重启的情况下，不能自动完成界面主题的刷新。笨重，灵活性较低，不易于扩展。
- 例如：
[android 设置自定义主题及切换方案](https://blog.csdn.net/u011106915/article/details/101108937)

###  2.借助于第三方库完成换肤
- 原理：LayoutInflater有一个内部接口Factory，系统会使用它去做XML到View的转换，而系统也提供了setFactory的方法，用户设置了，则用我们设置的，这样系统就会走我们Factory的onCreateView,他会返回一个我们定制化的View。
- 优点：不用重启activity，不闪屏；可以为程序提供多种皮肤方案不局限于夜间/白天模式。
- 缺点：在制作方面代价过大，侵入性较强，需要以来第三方库完成，可靠性不能得到保证。
- 例如：
[ChangeSkin](https://github.com/hongyangAndroid/ChangeSkin)
[Android-skin-support](https://github.com/ximsfei/Android-skin-support)

### 3：使用DayNight主题实现来支持日间/夜间模式的切换
- 优点：Google自家产品，可靠性高，配置简单，省心省力，在仅仅需要实现夜间/日间模式的应用内强烈推荐。
- 缺点：不支持多皮肤切换，只支持日间模式和夜间模式。

# 二.官方DayNight主题方案实现
### 1.导入依赖
```
implementation 'androidx.appcompat:appcompat:1.0.2'
```

### 2.修改style文件
```
<style name="AppTheme" parent="Theme.AppCompat.DayNight">
        <!-- Customize your theme here. -->
        <item name="colorPrimary">@color/colorPrimary</item>
        <item name="colorPrimaryDark">@color/colorPrimaryDark</item>
        <item name="colorAccent">@color/color_blue</item>
 </style>
```
在这里需要将主题改为Theme.AppCompat.DayNight 或者它的子主题。只有这样才支持白夜模式的切换。
这会将应用程序的主题与系统控制的夜间模式标志相关联，当系统的主题切换时，应用也会随之切换主题。

### 3.新增夜间模式下的color文件
既然App需要在白夜模式下互相切换，就需要两套的颜色资源文件和图片资源文件。
**颜色资源文件**
原有的color.xml文件内的颜色系统默认作为白天模式下的颜色取值。对于夜间模式，我们需要新增values-night文件夹，里面包含一个新建的color文件
**图片资源文件**
如果适配图片的话，就创建对应的 drawable-night-xxhdpi目录，mipmap-night-xxhdpi目录然后将图片资源放到对应的目录里面。
![](https://upload-images.jianshu.io/upload_images/3067896-60e69b80c76e0043.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![](https://upload-images.jianshu.io/upload_images/3067896-ff07cba6e58c21b4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

在这个文件中的颜色名需与默认的color文件内颜色名一一对应
```
//默认的color文件内颜色值
<color name="color_1">#f2f2f2</color>
<color name="color_2">#8E8E93</color>
<color name="color_3">#3385FF</color>
```
```
//values-night 内的color文件内颜色值
<color name="color_1">#616161</color>
<color name="color_2">#E0E0E0</color>
<color name="color_3">#E0E0E0</color>
```

### 4.切换模式
开始前我们要确保我们的Activity继承自AppCompatActivity.
两种方法：
第一种：调用AppCompatActivity里的getDelegate()获取AppCompatDelegate对象，然后在调用setLocalNightMode()方法设置夜间模式
```
if(isNi) {  
getDelegate().setLocalNightMode(AppCompatDelegate.MODE_NIGHT_NO);  
} else {  
getDelegate().setLocalNightMode(AppCompatDelegate.MODE_NIGHT_YES);  
}  
```
第二种：在onCreate()方法里的setContentView()方法前，直接调用AppCompatActivity里的静态方法setDefaultNightMode()来设置
```
//日间 切换 夜间
AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_NO)
recreate()

//夜间 切换 日间  
AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_YES)
recreate()
```
**两种方法的区别**
第一种方法是立刻生效的，且只在当前Activity有效，代码执行之后会重新创建当前Activity；而第二种方法是在Activity被创建的时候生效，且对App内的所有Activity都生效。

使用上述两种方案就完成了切换。当然这样切换是很生硬的，没有过渡动画，看起来不是很舒服 我们可以在recreate()之前给它加个过渡动画.
```
getWindow().setWindowAnimations(R.style.OutInAnimation);
```
AppCompatDelegate一共有四种模式:
- MODE_NIGHT_NO. Always use the day (light) theme(一直应用日间(light)主题).
- MODE_NIGHT_YES. Always use the night (dark) theme(一直使用夜间(dark)主题).
- MODE_NIGHT_AUTO. Changes between day/night based on the time of day(根据当前时间在day/night主题间切换).自动模式，当我们的APP有网络及定位权限时。系统会根据当地的时间判断当前时处于白天还是黑夜，从而自动加载不同的模式。
- MODE_NIGHT_FOLLOW_SYSTEM(默认选项). This setting follows the system’s setting, which is essentially MODE_NIGHT_NO(跟随系统，通常为MODE_NIGHT_NO).

当我们的App启动时就需要显示为夜间模式时，我们可以在Application内设置
```
class BaseApplication : Application() {
static {
    AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_YES);
}
    override fun onCreate() {
        super.onCreate()
}
```
但一般情况下，我们都会在切换模式时将当前模式保存至本地，下次启动时再根据保存的值加载不同的模式
```
class BaseApplication : Application() {
    override fun onCreate() {
        super.onCreate()
        if (SPManager.getBoolean(applicationContext, SPContent.SP_MODE, false)) 
            AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_YES) else 
            AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_NO)
    }
}
```

### 5.注意
- 1.切换只作用于新生成的组件，对原先处于任务栈中的Activity不起作用。（解决方法：发送广播，让它重启）如果直接在Activity的onCreate()中调用切换代码，可以不需要调用recreate()。对于一些数据的保存与切换后的显示我们可以用savedInstanceState来保存与复原
- 2.在切换后可以不调用recreate()，而是自己添加一个重启该Activity的方法，然后加个过度动画
- 3.解决动态切换主题时activity重启闪屏的问题:[NightModel](https://github.com/achenglike/NightModel)

感谢：
[Android 10适配要点，深色主题-郭霖](https://blog.csdn.net/sinyu890807/article/details/106061657)
[android夜间模式浅析](https://www.dazhuanlan.com/2019/10/24/5db11f896b650/)
[一种Android换肤机制的实现](https://www.dazhuanlan.com/2019/11/15/5dcde8406dc41/)
