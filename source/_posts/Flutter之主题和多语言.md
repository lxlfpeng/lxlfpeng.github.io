---
title: Flutter之主题和多语言
date: 2021-07-05
categories: 
  - Flutter开发
---

# 支持国际化
为了尽可能小而且简单，flutter包中仅提供美国英语值的MaterialLocalizations和WidgetsLocalizations接口的实现（实现类分别为DefaultMaterialLocalizations和DefaultWidgetsLocalizations）。
所以Material组件库和开发人员的UI都需要进行国际化：
  1. Material组件库
    比如：日历组件默认在任何环境下都会以英文显示，所以需要国际化。
    需要依赖flutter_localizations包，包含GlobalMaterialLocalizations和GlobalWidgetsLocalizations的本地化接口的多语言实现。
  2. 开发人员的UI。
    需要实现Localizations。

iOS需要在info.plist中添加Localizations项（在其中添加语言，默认有一个英文）

### 添加依赖
默认情况下，Flutter SDK中的组件仅提供美国英语本地化资源（主要是文本）。要添加对其他语言的支持，应用程序须添加一个名为“flutter_localizations”的包依赖，然后还需要在MaterialApp中进行一些配置。
 要使用flutter_localizations包，首先需要添加依赖到pubspec.yaml文件中：

dependencies:
  flutter:
    sdk: flutter
  flutter_localizations:
    sdk: flutter
    
### 设置MaterialApp
在localizationsDelegates中指定哪些Widget需要进行国际化

用于生产本地化值集合的工厂
我们这里指定了Material、Widgets、Cupertino都使用国际化
supportedLocales指定要支持哪些国际化

我们这里指定中文和英文（也可以指定国家编码）
```
MaterialApp(
  localizationsDelegates: [
    // 本地化的代理类
    GlobalMaterialLocalizations.delegate, // 指定本地化的字符串和一些其他的值
    GlobalCupertinoLocalizations.delegate, // 对应的Cupertino风格
    GlobalWidgetsLocalizations.delegate // 指定默认的文本排列方向, 由左到右或由右到左
  ],
  supportedLocales: [// 当前应用支持的locale列表
    Locale("en"),
    Locale("zh")
  ],
   locale: const Locale('en', 'US'),//手动指定locale
)
```
注意：如果要指定语言代码、文字代码和国家代码，可以进行如下指定方式：

// Full Chinese support for CN, TW, and HK
```
supportedLocales: [
  const Locale.fromSubtags(languageCode: 'zh'), // generic Chinese 'zh'
  const Locale.fromSubtags(languageCode: 'zh', scriptCode: 'Hans'), // generic simplified Chinese 'zh_Hans'
  const Locale.fromSubtags(languageCode: 'zh', scriptCode: 'Hant'), // generic traditional Chinese 'zh_Hant'
  const Locale.fromSubtags(languageCode: 'zh', scriptCode: 'Hans', countryCode: 'CN'), // 'zh_Hans_CN'
  const Locale.fromSubtags(languageCode: 'zh', scriptCode: 'Hant', countryCode: 'TW'), // 'zh_Hant_TW'
  const Locale.fromSubtags(languageCode: 'zh', scriptCode: 'Hant', countryCode: 'HK'), // 'zh_Hant_HK'
],    
 ```   

###  监听系统语言切换
当我们更改系统语言设置时，APP中的Localizations组件会重新构建，Localizations.localeOf(context) 获取的Locale就会更新，最终界面会重新build达到切换语言的效果，但是这个过程是隐式完成的。

我们可以通过localeResolutionCallback或localeListResolutionCallback回调来监听locale改变的事件。
 ``` 
Widget widget1 = MaterialApp(
      // typedef LocaleResolutionCallback = Locale? Function(Locale? locale, Iterable<Locale> supportedLocales);
      localeResolutionCallback: (Locale? locale, Iterable<Locale> supportedLocales){
        //local: 当前的当前的系统语言设置
        //supportedLocales: 为当前应用支持的locale列表，是开发者在MaterialApp中通过supportedLocales属性注册的
        // return Locale?
      },
      // typedef LocaleListResolutionCallback = Locale? Function(List<Locale>? locales, Iterable<Locale> supportedLocales);
      localeListResolutionCallback: (List<Locale>? locales, Iterable<Locale> supportedLocales){
        //local: 当前的当前的locales 列表
        //supportedLocales: 为当前应用支持的locale列表，是开发者在MaterialApp中通过supportedLocales属性注册的
        // return Locale?
    },
   );
}
 ``` 
## 国际化开发人员的UI（Localizations）
示例

第一步：实现Localizations资源类（提供本地化资源值，如文本）

// Locale资源类 
// 会根据当前的语言来获取本地化资源值。可以将所有需要支持多语言的文本都在此类中定义，该类的实例会在Delegate类的load方法中创建。
 ``` 
class DemoLocalizations {
  DemoLocalizations(this.isZh);
  // 是否为中文
  bool isZh = false;

  // 为了使用方便，定义一个静态方法
  static DemoLocalizations of(BuildContext context) {
    // MaterialApp组件内部嵌套了Localizations组件，通过第三步配置MaterialApp的localizationsDelegates，会将DemoLocalizationsDelegate传给Localizations组件
    // 获取DemoLocalizations实例
    return Localizations.of<DemoLocalizations>(context, DemoLocalizations);
  }

  // Locale相关值，title为应用标题
  String get title {
    return isZh ? "Flutter应用" : "Flutter APP";
  }
  //... 其它的值  
}

/*
class DemoLocalizations {
  DemoLocalizations(this.locale);
  final Locale locale;
  static DemoLocalizations of(BuildContext context) {
    return Localizations.of<DemoLocalizations>(context, DemoLocalizations);
  }
  static Map<String, Map<String, String>> _localizedValues = {
    'en': {
      'title': 'Hello World',
    },
    'es': {
      'title': 'Hola Mundo',
    },
  };
  String get title {
    return _localizedValues[locale.languageCode]['title'];
  }
}
 ``` 
*/
第二步：实现Delegate类（在Locale改变时会从DemoLocalizations中加载新的本地化资源值）

// Locale代理类
// Delegate类需要继承自LocalizationsDelegate类，实现相应的接口，有一个load方法。
 ``` 
class DemoLocalizationsDelegate extends LocalizationsDelegate<DemoLocalizations> {
  const DemoLocalizationsDelegate();

  // 是否支持某个Local
  @override
  bool isSupported(Locale locale) => ['en', 'zh'].contains(locale.languageCode);

  // Flutter会调用此类加载相应的Locale资源类
  @override
  Future<DemoLocalizations> load(Locale locale) {
    print("$locale");
    return SynchronousFuture<DemoLocalizations>(
        DemoLocalizations(locale.languageCode == "zh")
    );
  }

  // shouldReload的返回值决定当Localizations组件重新build时，是否调用load方法重新加载Locale资源。一般情况下，Locale资源只应该在Locale切换时加载一次，不需要每次在Localizations重新build时都加载，所以返回false即可。事实上，无论shouldReload返回true还是false，每当Locale改变时Flutter都会再调用load方法加载新的Locale。
  @override
  bool shouldReload(DemoLocalizationsDelegate old) => false;

  static DemoLocalizationsDelegate delegate = const DemoLocalizationsDelegate();
}

/*
class DemoLocalizationsDelegate extends LocalizationsDelegate<DemoLocalizations> {
  const DemoLocalizationsDelegate();
  @override
  bool isSupported(Locale locale) => ['en', 'es'].contains(locale.languageCode);
  @override
  Future<DemoLocalizations> load(Locale locale) {
    return new SynchronousFuture<DemoLocalizations>(new DemoLocalizations(locale));
  }
  @override
  bool shouldReload(DemoLocalizationsDelegate old) => false;
  static DemoLocalizationsDelegate delegate = const DemoLocalizationsDelegate();
}
*/
 ``` 
第三步：配置MaterialApp的localizationsDelegates

在MaterialApp或WidgetsApp的localizationsDelegates列表中添加Delegate实例即可完成注册
``` 
localizationsDelegates: [
 // 本地化的代理类
 GlobalMaterialLocalizations.delegate,
 GlobalWidgetsLocalizations.delegate,
 // 注册我们的Delegate
 DemoLocalizationsDelegate(), // 或DemoLocalizationsDelegate.delegate
],
``` 
第四步：在Widget中使用本地化资源值
``` 
return Scaffold(
  appBar: AppBar(
    // 使用Locale title  
    title: Text(DemoLocalizations.of(context).title),
  ),
  ... //省略无关代码
 ）
``` 
## GetX实现多语言
现在换成GetX插件提供的国际化功能，非常好用

import 'package:get/get.dart';
在main.dart的build方法里配置getx：
``` 
GetMaterialApp(
    translations: IntlMsgs(), // 国际化语言包
    locale: Locale('zh', 'CN'),
    fallbackLocale: Locale('en', 'US'),
    localeListResolutionCallback: (locales, supportedLocales) {
      print('当前系统语言环境:$locales');
      return;
    },
    ...
``` 
可以看到MaterialApp替换成了GetMaterialApp，translations参数配置了一个自定义的语言包文件，举个例子：
``` 
class IntlMsgs extends Translations {
  @override
  Map<String, Map<String, String>> get keys => {
        'zh_CN': {
           'english': '英文',
        },
        'en_US': {
           'english': 'english',
        },
  };
}
``` 
创建一个类继承自Translations，重写keys的get方法，在里面配置多种语言的字段，上面的代码只配置了一个english字段，支持中文和英文，我们在使用的时候就可以：
``` 
Text(
   'english'.tr,
),
``` 
字符串后面加个 .tr 就行了，getx会根据当前语言环境获取对应的字段

我们在切换语言的时候，只需要：
``` 
Get.updateLocale(Locale('en_US'));
``` 
就切换到英文了，因为getx自带状态管理，我们不需要考虑页面刷新

下面说深色模式，也是只需要一行：
``` 
Get.changeTheme(isDark
        ? ThemeData(
              brightness: Brightness.dark,
              primaryColor: Utils.hexColor('2c2c2b'),
           )
        : ThemeData(
              brightness: Brightness.light,
              primaryColor: Colors.white,
        ));
``` 
可以用Get.isDarkMode来获取当前是否是深色模式


参考资料:
[Flutter了解之国际化](https://www.jianshu.com/p/a660f18fcd3b)
[Flutter 本地化l10n（多语言i18n）的支持](https://juejin.cn/post/6844903832774770701)
[Flutter 多语言方案调研对比](https://www.jianshu.com/p/92b955b2b0a9)
[flutter实现多语言之项目使用](https://blog.csdn.net/qq_46143850/article/details/115197986)