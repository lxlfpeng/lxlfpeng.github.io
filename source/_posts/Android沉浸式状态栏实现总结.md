---
title: Android沉浸式状态栏实现总结
date: 2022-10-28
categories: 
  - Android开发
tags:
  - Android状态栏
---


# Android api 30+ 可用新的api实现沉浸式状态栏等方案
状态栏字体颜色修改：
//状态栏字体改为白色
```kotlin
WindowCompat.getInsetsController(window,window.decorView).isAppearanceLightStatusBars = false
```
//状态栏字体改为黑色
```kotlin
WindowCompat.getInsetsController(window,window.decorView).isAppearanceLightStatusBars = true
```


在API 11及其以上 Window Tranfer flag已经过时了，我们使用如下的方法
```kotlin      
window.statusBarColor = Color.TRANSPARENT
window.navigationBarColor = Color.TRANSPARENT
//内容扩展到状态栏
WindowCompat.setDecorFitsSystemWindows(window, false)
​
ViewCompat.getWindowInsetsController(window.decorView)?.run {
     //隐藏系统栏
    this.hide(WindowInsetsCompat.Type.statusBars())
    this.hide(WindowInsetsCompat.Type.navigationBars())
    //系统栏的行为：滑动显示系统栏
    this.systemBarsBehavior = BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE
}

```
[Android 沉浸式状态/导航栏的实现以及布局重叠的适配（Kotlin）](https://juejin.cn/post/7252231214529282085)
[Android Detail：Window 篇—— WindowInsets 与 fitsSystemWindow](https://juejin.cn/post/7038422081528135687#heading-28)
[WindowInsetsControllerCompat使用，新方式实现状态栏、导航栏、键盘控制](https://blog.csdn.net/StjunF/article/details/121840122)
[Android 实现沉浸式全屏的总结](https://juejin.cn/post/7139495545206210590)
[【Android爬坑日记】沉浸式状态栏](https://juejin.cn/post/7133619873376108558)
[Android 系统 Bar 沉浸式完美兼容方案](https://juejin.cn/post/7075578574362640421)
[Android 全屏显示和沉浸式显示](https://juejin.cn/post/7120815750880690190)