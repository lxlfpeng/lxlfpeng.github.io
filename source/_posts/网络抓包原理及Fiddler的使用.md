---
title: 网络抓包原理及Fiddler的使用
date: 2019-08-12
categories: 
  - 网络基础
tags:
  - 抓包
  - Fiddler
---

![](/images/e55567f9cf38efa380d41574d8e5b6ac.webp)
# 一. 什么是抓包?
在应用的开发调试中，查看软件实际运行时HTTP/HTTPS通信的请求数据和返回数据，从而分析问题的过程就叫做抓包。通常我们说的抓包主要是分为两种：
- 使用Wireshark抓取传输层的TCP/UDP通信包。
- 使用Fiddler或者Charles抓取应用层的HTTP/HTTPS通信包。

>在大部分场景下，我们只是需要抓取应用层的``HTTP/HTTPS数据包``也就是第二种方式。

# 二. 抓包的原理.

抓包的原理其实很简单，PC上的Fiddler监听一个端口，比如8888，在Android测试机上连接同一个局域网，配置网络代理，指向该PC的8888端口，这样一来测试机的所有网络通信都会被转发到PC的8888端口，进而被Fiddler捕获，然后就可以对数据包进行分析。经常用的网络协议分为HTTP和HTTPS，HTTPS在HTTP上进行了加密操作，所以对这两种请求进行抓包也有不同。
###  对HTTP请求进行抓包
对于HTTP协议，因为本身就是``明文传输``，所以可以直接看到数据报文，除非对这些明文在传输时进行二次加密，但那是另一种情况，这里暂不分析。

### 对HTTPS请求进行抓包
对于双向加密的HTTPS，正常情况下，即使能以``中间人的方式拿到通信报文``，但是因为没有密钥，同样也不能看到具体的传输内容。基于HTTPS加密通信的建立过程，和密钥交换方式，如果在加密通信建立之前，``截取服务端发送的包含证书的报文，伪装成服务端，把自己的证书发给客户端，然后拿到客户端返回的包含对称加密通信密钥的报文，以服务端自己的公钥加密后发给服务端，``这样一来，双向加密通信建立完成，而中间人实际拿到了通信的密钥，所以可以查看、修改HTTPS的通信报文，这就是典型的``Man-in-the-middle attack即MITM中间人攻击。``
这样似乎看起来，HTTPS也不是那么安全，当然不能这么说了，实现MITM最关键的一点，是中间人要把服务端证书替换成自己的证书发给客户端，让客户端相信自己就是服务端，那么问题是，客户端为什么会信任而进行替换呢？HTTPS之所以安全，是因为它用来建立加密通信的证书是由权威的``CA机构签发``的，受信的CA机构的根证书都会被内嵌在Windows, Linux, macOS, Android, iOS这些操作系统里，用来验证服务端发来的证书是否是由CA签发的。CA机构当然不可能随便给一个中间人签发不属于它的域名证书，那么只有一个很明显的办法了，把中间人的根证书，导入到客户端的操作系统里，以此来完成建立加密通信时对中间人证书的验证。
>所以，在一定的情况下，HTTPS通信是可以被监听的，抓包的实现基础，是Android测试机导入Fiddler或者Charles的根证书。

无论是fidder和charles都是充当了一个中间人代理的角色来对HTTPS进行抓包:
- 截获客户端向发起的HTTPS请求，佯装客户端，向真实的服务器发起请求。
- 截获真实服务器的返回，佯装真实服务器，向客户端发送数据。
- 获取了用来加密服务器公钥的非对称秘钥和用来加密数据的对称秘钥。
![HTTPS中间人攻击](/images/72e5c8dd9bce0e49b8e6a2abe30813ec.webp)

# 三. Android设备抓包问题
### 1. Android6.0 及以下系统
可以直接使用FIddler进行抓包。
### 2. Android7.0 及以上系统
在Android 7.0及以上的设备上测试时，发现又抓不到HTTPS了。原因是，Google在Android 7.0时更改了App对操作系统本地证书的信任机制，在Android 7.0之前，默认信任系统预置证书和用户自导入证书，在Android 7.0(API 24)之后，为了保障App的通信安全，避免被第三方抓包,做了些改动，App默认只信任系统预置证书，而不再信任用户自导入证书(把MITM的ssl证书，安装到 受信任的凭据 -> 用户)抓出来的https的请求，都是加了密的，无法看到原文了.解决的方式有如下几种:
- 修改App的AndroidManifest网络安全配置，信任用户自导入证书。
- Root测试机或自编译系统，把Fiddler根证书设置为系统预置证书。
- 在Android 7.0以下的测试机中抓包。
- targetSDK版本设置为24以下。

**方式一**
如果是自己公司开发的应用那么在 Android 工程目录的 res 底下创建一个 xml 文件夹，然后在内部创建一个名为 “network_security_config.xml” 的文件。

```
	  <network-security-config>
	    <base-config cleartextTrafficPermitted="true">
	        <trust-anchors>
	            <certificates src="system" overridePins="true" />
	            <certificates src="user" overridePins="true" />
	        </trust-anchors>
	    </base-config>
	  </network-security-config>
```

在 AndroidManifest 里的标签中，添加代码:

```
	android:networkSecurityConfig="@xml/network_security_config"
```
>这种方式只适用于能自己修改源码的应用。

**方式二**
- root手机
Root手机将用户下载的CA协议移动到系统信任的证书目录下。
- 非root手机可以VirtualXposed插件
[VirtualXposed下载地址](https://github.com/android-hacker/VirtualXposed)
[JustTrustMe下载地址](https://github.com/Fuzion24/JustTrustMe)

>方式三和方式四用的比较少.

# 四. 选择抓包工具
主流的Http/Https抓包工具有``Fiddler、Charles``等。Mac上用的较多的一般是Charles。两种工具的使用方式大同小异，本文主要讲Fiddler抓包工具的使用。
### 1. 下载Fiddler:
[官网下载](https://www.telerik.com/fiddler)
[百度云](https://pan.baidu.com/s/1zih7wAZhCv_PEnAVjfkU9A) 提取码：fqdr
### 2. 安装Fiddler:
- 将安装包进行安装。
- 找到安装的目录,将启动文件发送到桌面快捷方式。
![image.png](/images/0174d2606a92d973194e03b41dffa7e5.webp)
### 3. Fiddler工作原理.
Fiddler是以代理WEB服务器的形式工作的，它默认使用代理地址**:127.0.0.1**， 端口**:8888**。 当Fiddler开启时会自动设置代理， 退出的时候它会自动注销代理，这样就不会影响别的程序。不过如果Fiddler非正常退出，这时候因为Fiddler没有自动注销，会造成网页无法访问。解决的办法是重新启动下Fiddler。
![](/images/9933f1506d99a285328c25f65a0d943e.webp)

# 五. Fiddler相关设置
### 1. 浏览器设置代理.
当Fiddler启动后，会默认将代理设为了127.0.0.1 端口号为8888。有些浏览器需要手动设置代理，在浏览器设置里面进行代理设置：
![](/images/37501cdd58f255a3e2c2f276d3b60f61.webp)
### 2. Fiddler开启抓包.
要使用Fiddler进行抓包，首先需要确保Capture Traffic是开启的（安装后是默认开启的），勾选File->Capture Traffic3。
![](/images/6cea2cab8f1abe370c42366e17d0182a.webp)
### 3. Fiddler工具面板.
![](/images/3eaa90a5ef62a65325b09cffaa239763.webp)
说明注释、重新请求、删除会话、继续执行、流模式/缓冲模式、解码、保留会话、监控指定进程、寻找、保存会话、切图、计时、打开浏览器、清除IE缓存、编码/解码工具、弹出控制监控面板、MSDN、帮助。
两种模式：
- **缓冲模式（Buffering Mode）**Fiddler直到HTTP响应完成时才将数据返回给应用程序。可以控制响应，修改响应数据。但是时序图有时候会出现异常。
- **流模式（Streaming Mode）**Fiddler会即时将HTTP响应的数据返回给应用程序。更接近真实浏览器的性能。时序图更准确，但是不能控制响应。
### 4. Fiddler会话面板.
![](/images/61aa809ddd4f21d80fde531718a40211.webp)
各种图标的含义:
![](/images/68cb380fc254c10ba7669c4df9c83db1.webp)

### 5. Fiddler页签功能.
![](/images/b27374d3854754eb7549feb53afbac6e.webp)
###### 5.1 Statistics
这一部分是统计信息视图，显示了所有HTTP通信，展示了哪些文件生成了当前请求的页面。可以选择一个或多个会话，然后得出所选会话的统计信息:
![](/images/bd8c287d25069e0b47157c3291d71052.webp)
###### 5.2 Inspectors
分为上下两个部分，上半部分是请求头部分，下半部分是响应头部分。对于每一部分，提供了多种不同格式查看每个请求和响应的内容。JPG 格式使用 ImageView 就可以看到图片，HTML/JS/CSS 使用 TextView 可以看到响应的内容。Raw标签可以查看原始的符合HTTP标准的请求和响应头。Auth则可以查看授权Proxy-Authorization 和 Authorization的相关信息。Cookies标签可以看到请求的cookie和响应的set-cookie头信息。
![](/images/84e307780d174747ebcb088f3a5d3f75.webp)

###### 5.3 AutoResponder
Fiddler比较重要且比较强大的功能之一。可用于拦截某一请求，并重定向到本地的资源，或者使用Fiddler的内置响应。可用于调试服务器端代码而无需修改服务器端的代码和配置，因为拦截和重定向后，实际上访问的是本地的文件或者得到的是Fiddler的内置响应。

###### 5.4 Composer
HTTP Request发射器。功能是创建HTTPRequest，然后发送。

###### 5.5 Filter([过滤器](https://www.cnblogs.com/sjl179947253/p/7627250.html))
- **开启过滤功能:**
![](/images/8b1e07f7477da5f41d18e1db7c4057c1.webp)
- **加载过滤功能:**
![](/images/ac8a12dc232a72df913708ebefd2a663.webp)


### 6. Fiddler过滤方式
##### 6.1 内外网过滤:
![](/images/9b082a81ae87e94784ecac08ed80ecde.webp)
##### 6.2 对host过滤:
![](/images/c092fc4f2cbd1c18a01686b94b16b488.webp)
输入多个HOST，多个之前用半角逗号或者回车分隔；
支持通配符：*,baidu.com；
![](/images/2f6430ebd485a154149b2fd40ab2d02e.webp)
##### 6.3 Client Process(进程)过滤
- Show only traffic from：你可以指定只捕获哪个Windows进程中的请求；
- Show only Internet Explorer traffic：只显示IE发出的请求；
- Hide Windows RSS platform traffic：隐藏Windows RSS平台发出的请求；

![image.png](/images/617a96eb64407aa9202de2c7eb837593.webp)

![image.png](/images/1c8cf8e931a8612b565a119b1bf0432b.webp)

##### 6.4 Request Headers过滤
请求header过滤规则：
  经常使用：Show only if URL contains；
  Flag requests with headers：标记带有特定header的请求；
  Delete request headers：删除请求header；
  Set request header设置请求的header；
![image.png](/images/fc95a7328432219d72c52b5a5215b0cb.webp)

#####  6.5 Breakpoints
断点设置规则：
  Break request on HTTP POST：给所有POST请求设置断点；
  Break request on HTTP GET with QueryString：给所有带参数的GET请求设置断点；
  Break response on Content-Type：给特定的Content-Type设定断点；
![](/images/f68aa32c1db816c22143089de1ecc4ff.webp)


#####  6.6 Response Status Code过滤
响应HTTP状态过滤规则：
  Hide success(202,204,206)：隐藏响应成功的session(202,204,206)；
  Hide Authentication demands(401)：隐藏未经授权被拒绝的session(401)；
  Hide redirects(300,301,302,303,307)：隐藏重定向的session(300,301,302,303,307)；
  Hide Not Modified(304)：隐藏无变更的session(304)；
![](/images/91ea3fa84aa721d2c9be3add2affd1d3.webp)

#####  6.7 Response Type and Size
响应类型和大小过滤规则：
  Show all Content-Type：显示所有响应类型；
  Hide smaller than ？KB：隐藏小于指定大小的session；
  Hide larger than ？KB：隐藏大于指定大小的session；
  Time HeatMap：获得即时数据（绿色阴影代表响应时间在50毫秒以内；超过50毫秒但在300毫秒之内的响应条目没有颜色；响应时间在300至500毫秒之间的会涂以黄色；超过500毫秒的用红色底纹显示）；
  Block script files：阻止脚本文件，显示为404；
  Block image files：阻止图片文件；
  Block SWF files：阻止SWF文件；
  Block CSS files：阻止CSS文件；
##### 6.8 Response Headers
响应header过滤规则：
  Flag response that set cookies：标记会设置cookie的响应；
  Flag response with headers：标记带有特定header的响应；
  Delete response headers：删除响应header；
  Set response header：设置响应的header；
![](/images/7be4504177d7904b91d3616383ca1d20.webp)

# 六. Fiddler断点功能
断点的主要作用：篡改和伪造数据。
1.为什么要打断点呢？
比如一个购买的金额输入框，输入框前端做了限制100-1000，那么我们测试的时候，需要测试小于100的情况下。很显然前端只能输入大于100的。这时我们可以先抓到接口，修改请求参数，绕过前端，传一个小于100的数，检查服务端的功能是否OK。也就是说接口测试其实是不需要管前端的，主要测后端的功能。
**例如：**
使用支付宝购买虚拟商品，往支付宝跳转时，篡改了小的金额，结果购买虚拟商品成功了。（原本10元的商品，0.01元就搞定了）。多么可怕的一个bug。

断点可以打到两个地方:
1. before response：这个是打在request请求的时候，未到达服务器之前。
2. after response：也就是服务器响应之后，在Fiddler将响应传回给客户端之前。
![](/images/3e743419b11be0ac329942775f50fe61.webp)
![](/images/18432177aac75fc8272fc8ff9fcc475e.webp)
选中before requests选项后，请求一个网址：
![](/images/4dc796949bf6fe0ac91c3ded6995d434.webp)
进入到断点了
![](/images/281816fec40bffe17a730e711626121d.webp)

对数据进行拦截并且修改：
![](/images/b493d6ce5c342460f35912dc5ecf342e.webp)
![](/images/4400dd7566b4d57de6b1c405c3fa89c2.webp)
![](/images/273d24cb6a7fd4bb763854fecc0bd406.webp)
通过最后的结果可以看到数据已经被我们拦截并且修改成功了。

# 七. Fiddler抓取https请求
[fiddler抓取https原理](https://www.jianshu.com/p/54dd21c50f21)
[Fiddler处理HTTPS请求的原理](https://zhuanlan.zhihu.com/p/25591288)
[Fiddler抓取https原理-知乎](https://www.zhihu.com/question/24484809)
在抓取https的数据包时，fiddler会话栏目会显示“Tunnel to….443”的信息，这个是什么原因呢？
connect表示https的握手（也就是认证信息，只要是https就要进行认证），只要不是满篇的Tunnel to….443，就没有任何问题。我们可以选择将这类信息进行隐藏。
![](/images/9ac1b00753aae598c8b54a02ef2e3a88.webp)
![](/images/2f89c4a879d9ebc59d2080458a91bf9f.webp)
![](/images/3b2a300d88d7549ea3d972fe399c65fc.webp)
![](/images/6799c04ed5de0c2b53d5257b6eaa328d.webp)
![](/images/ec854db86852637747bcc94e12ca591a.webp)
查看一下证书，Actions—>open windows certificate Manager
![](/images/514c1bab362ab308923b96771f3bf518.webp)
![](/images/6b908069119f736362bc721081729d91.webp)
如果还是不能抓包成功参考一下解决:
[强烈推荐（原创亲测）！！！Fiddler抓取https设置详解（图文）](https://www.cnblogs.com/joshua317/p/8670923.html)

### 八. 移动设备抓包.
#### 1. Fiddler设置允许手机远程连接。
如果想要捕获手机上的通信数据，就需要手机连接上Fiddler代理，而Fiddler默认是不允许其他设备进行连接的，解决办法：点击 Fiddler->Tools -> Options，在 Connections 面板选中 Allow remote computers to connect 允许其他设备连接（此操作需重启Fiddler生效）。
![](/images/bb7aebe934912bb71077bbbec6562e3c.webp)

#### 2. 获取安装Fiddler的Pc的ip地址。
- 通过fiddler里面查看
![](/images/c4fc543fd9e485dc0aa3d16eafc439f5.webp)
- 通过windows命令行查看
![](/images/bb1425b4207488b630abb3d9d1479905.webp)

#### 3. Android设备抓包
***注意:需要手机和电脑在同一局域网里面才可以进行抓包***
在手机设置里面找到自己连接的WiFi长按，弹出修改网络弹窗，选择修改网络，点击高级选项的下拉菜单，选择手动，配置好主机和端口号，然后确定就可以对手机进行抓包了。
![](/images/f816e9dfa4ed7526ef564422893672c5.webp)
![](/images/1b335858a07ddc884a62e5664934b3b1.webp)
![](/images/20198fc41977d40eae7d2abf87592dc9.webp)
![](/images/4495ce412d8711f6e0d6a84006586114.webp)
#### 4. IOS设备抓包
![](/images/82f90fc26108a4779bd61d483c552a29.webp)
![](/images/84a8c54b3977099cdef61c5ced930010.webp)
##### 手机安装根证书。
在手机上需要安装Fiddler根证书，因为Fiddler是通过自己生成的证书对网络请求重新签名进行https会话解密的，如果不安装证书的话只能抓取HTTP请求。
打开手机浏览器，输入Fiddler Server地址， 跳转到 Fiddler Echo Service 证书下载页，点击FiddlerRoot certificate下载并安装；
![](/images/ac2feee4c492147c5dc43f6d27f8a2e9.webp)
![](/images/d281b677ccda2e78fb10a76895b0d610.webp)
然后输入手机密码，安装好证书。
>注意：如果手机设置代理后，测玩之后记得恢复原样(去掉手动设置的代理)，要不然手机无法正常上网。
