---
title: Android即时通讯Im开发总结
date: 2022-09-23
categories: 
  - Android开发
---

# 实现即时通讯IM的方式
### 一. 使用第三方IM服务
对于短平快的公司，完全可以采用第三方SDK来实现。国内IM的第三方服务商有很多，类似云信、环信、融云、LeanCloud，当然还有其它的很多，这里就不一一举例了，感兴趣的小伙伴可以自行查阅下。
第三方服务商IM底层协议基本上都是TCP。他们的IM方案很成熟，有了它们，我们甚至不需要自己去搭建IM后台，什么都不需要去考虑。如果你甚至连UI都不需要自己做，这些第三方有各自一套IM的UI，拿来就可以直接用。
但是缺点也很明显，定制化程度不太高，很多东西我们不可控。当然还有一个最最重要的一点，就是太贵了...作为真正社交为主打的APP，仅此一点，就足以让我们望而却步。 当然，如果IM对于APP只是一个辅助功能，那么用第三方服务也无可厚非。
主流的第三方IM服务:
- 环信IM。
- 融云IM。
- 野火IM(半开源)。
### 二. 自己实现
自己实现大约有三种方案:
- 客户端不断通过http轮询服务端获取消息(不建议)。
- 使用第三方推送服务将消息推送到客户端(不建议)。
- 自己使用长连接技术保持和服务端的连接获取到消息(建议)。
#### 1. 客户端轮询
客户端不断的查询服务器，检索新内容。这种方式的缺点十分明显，如果轮询频率过快，会大量消耗网络带宽和电池；
#### 2. 第三方消息推送
利用推送的及时性来做im也是可以的。
在推送这一分支领域有许许多多的第三方推送服务，例如：极光，个推等。
**优点**：集成方便。
**缺点**：大量推送数据后，付费服务是在所难免。而且因为是通用共享云，所以你的服务质量是否有保证，也就不能要求太多了，必竟你一毛钱也没出或者也不打算出。
#### 3. 客户端和服务端长连接
# 三.长连接
### 1.传输协议的选择
- 基于Scoket原生：代表框架 CocoaAsyncSocket。
- 基于WebScoket：代表框架 SocketRocket。
- 基于MQTT：代表框架 MQTTKit。
- 基于XMPP：代表框架 XMPPFramework。
### 2.IM传输格式的选择
##### (1.)JSON
##### (2.)Protobuf
ProtoBuf是Google的一个开源项目。作用于数据存储、数据通信和语言无关平台无关，扩展便捷。它是一个灵活、高效、自动化的序列化和结构化数据格式，比XML协议的数据格式更小，更快和更简单。
你可以定义你想要的数据结构，然后使用ProtoBuf提供的编译器生成相应平台的源代码，编译器自动化会生成读写你结构化数据代码，然后可以把源码应用于各种语言，你甚至可以在更新数据结构情况下不破坏已经部署基于老格式编译程序。
Google Protocol Buffers 简称 Protobuf，类似 json 或 XML，是一种序列化结构数据的机制，但是比它们更小、更快、更简单。同时支持多语言，跨平台。 目前主要有两个大版本：proto2 和 proto3。 其中 proto2 支持 Java、Python、 Objective-C、和 C++。 proto3 增加了对Go、JavaNano、Ruby、和 C#的支持。

**优点**:
- 传输效率快（序列化后体积较小）
- 支持跨平台多语言
- 序列化/反序列化速度很快

**缺点**:
- 可读性较差（二进制格式）
- 缺乏自描述
- 使用不太方便（貌似找不到支持原生c语言的protobuf，大都是经过别人编译后的库）

**适用场景**:
- 数据量大并且要求传输效率较高的场景。

#### 3. 重连机制(心跳)

# 四.推送
### 1.自己做推送进行保活(不建议保活难度大且随着系统升级会失效)

### 2.使用第三方推送
- 极光推送
- 个推
- 友盟推送
- 阿里推送

**优点**:
- 集成方便

**缺点**:
- 收费
- sdk推动黑产行为

### 3.开源框架
- [XPush](https://github.com/xuexiangjys/XPush)
- [MixPush](https://github.com/taoweiji/MixPush)


参考资料：
[开源一个自用的Android IM库，基于Netty+TCP+Protobuf实现](https://juejin.cn/post/6844903815846559757)

[即时通讯](https://blog.csdn.net/u011518806/article/details/83586692?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522161128240716780255282263%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=161128240716780255282263&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_v2~rank_v29-2-83586692.pc_search_result_cache&utm_term=%E5%8D%B3%E6%97%B6%E9%80%9A%E8%AE%AF&spm=1018.2226.3001.4187)

[自已开发IM有那么难吗？手把手教你自撸一个Andriod版简易IM (有源码)](https://zhuanlan.zhihu.com/p/74649303)

[Android 开源的IM SDK，基于Netty+TCP+Protobuf+Okhttp设计思路实现的一款可定制化的开源库](https://blog.csdn.net/smile__dream/article/details/105681018)

[跟我一起开发商业级IM（1）—— 技术选型及协议定义](https://juejin.cn/post/6850037279839387662#heading-6)

[跟我一起开发商业级IM（2）—— 接口定义及封装](https://juejin.cn/post/6858448694644703246#heading-12)

[iOS即时通讯，从入门到“放弃”？](https://www.jianshu.com/p/2dbb360886a8)

[即时通信（IM）和实时通信（RTC）的区别](https://blog.csdn.net/elesos/article/details/82021493?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522161128240716780255282263%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=161128240716780255282263&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_v2~rank_v29-4-82021493.pc_search_result_cache&utm_term=%E5%8D%B3%E6%97%B6%E9%80%9A%E8%AE%AF&spm=1018.2226.3001.4187)

[Android 即时通讯开发小结（一）](https://blog.csdn.net/netease_im/article/details/80804071?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522161128363316780274130920%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=161128363316780274130920&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_v2~rank_v29-11-80804071.pc_search_result_cache&utm_term=Android%20IM&spm=1018.2226.3001.4187)

[通讯协议与即时通讯](https://www.jianshu.com/p/ca4aeabf55f6)

[Android Protobuf 使用初探](https://juejin.cn/post/6862238253194412039)

[即时通讯IM技术领域提高篇](https://juejin.cn/post/6844903555493527565)

[IM即时通讯](https://juejin.cn/post/6920147277906444301)

[IM 即时通讯技术在多应用场景下的技术实现，以及性能调优（ iOS 视角）（附 PPT 与 2 个半小时视频）](https://www.jianshu.com/p/8cd908148f9e)

[为什么说基于TCP的移动端IM仍然需要心跳保活？](http://www.52im.net/thread-281-1-1.html)