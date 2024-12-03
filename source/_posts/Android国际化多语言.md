---
title: Android国际化多语言
---

# 一、静态配置
Android系统通过判断当前系统的Local配置，来使用对应的strings.xml文件。
建立不同语言的strings.xml文件，新建Resource File，选择Local，点击>>，选择需要的语言
values-->strings.xml默认语言(简体中文)
```
<resources>
    <string name="app_name">多语言演示</string>
    <string name="multi_language_setting">多语言设置</string>
</resources>
```
values-zh-rHK-->strings.xml繁体中文
```
<resources>
    <string name="app_name">多語言演示</string>
    <string name="multi_language_setting">多語言設置</string>
</resources>

```
values-en-->strings.xml英语
```
<resources>
    <string name="app_name">MultiLanguageDemo</string>
    <string name="multi_language_setting">MultiLanguageSetting</string>
</resources>
```
通过上面的设置，当我们切换系统语言时，程序会自动对应相应的strings.xml文件，前提是有对应的语言。
# 二、应用内语言切换(动态切换)
静态配置只能依靠系统的语言变更来改变语言，我们最常见的还是在应用中设置需要的语言，因此系统也提供了对应的方法来更改。
1. Android 7.0之上和Android7.0之下需要切换多语言的方式不一样.
2. 只需要在Activity(BaseActivity)的attachBaseContext中分别对 Android 7.0之上和Android7.0之下进行多语言处理就可以实现动态切换多语言了.
3. 如果不想在Activity(BaseActivity)的attachBaseContext中进行多语言处理可以使用ActivityLifecycleCallbacks中,在onActivityCreated函数中判断当前Activity
的语言是否是我们需要的语言然后进行切换.如果有些Activity不是继承子BaseActivity也需要用这种方式来进行处理

> 在Application中的attachBaseContext设置多语言亲测没有效果(可能部分机型需要适配).

终极方案: 如果需要完美的适配则先在Application中的attachBaseContext设置多语言,然后在Activity(BaseActivity)的attachBaseContext中分别对 Android 7.0之上和Android7.0之下进行多语言处理就可以实现动态切换多语言
最后使用ctivityLifecycleCallbacks中,在onActivityCreated函数中判断当前Activity的语言是否是切换到我们需要的语言如果没有切换则再次进行语言切换.


参考资料:
[记APP实现多语言（国际化）过程，兼容Android 8.0以上](https://blog.csdn.net/finddreams/article/details/78470768?spm=1001.2014.3001.5501)
[Android原生多语言切换方案，兼容Android10](https://juejin.cn/post/6844904137226878984)
[Android语言切换原理](https://kidsea.github.io/2017/11/19/Android%E8%AF%AD%E8%A8%80%E5%88%87%E6%8D%A2%E5%8E%9F%E7%90%86/)
[Android 仿微信多语言切换](https://www.jianshu.com/p/0f957ead4fa0)
[MultiLanguages](https://github.com/getActivity/MultiLanguages)
[MichaelJokAr/MultiLanguages](https://github.com/MichaelJokAr/MultiLanguages)






