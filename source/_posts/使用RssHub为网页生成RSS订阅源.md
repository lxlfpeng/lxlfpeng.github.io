---
title: 使用RssHub为网页生成RSS订阅源
---

# 一.RSSHub简介
众所周知，网站提供 RSS 并不能为他的站点带来更多的流量，反而会减少主站的访客数。因此很多的网站没有提供Rss订阅源供大家使用。 RSSHub就是这样的一款神器，借助 RSSHub 可以方便地通过 RSS 订阅知乎、豆瓣、Facebook 等现代媒体社交平台。[RSSHub](https://github.com/DIYgod/RSSHub) RSSHub 是一个开源、简单易用、易于扩展的 RSS 生成器，可以给任何奇奇怪怪的内容生成 RSS 订阅源。 RSSHub 借助于开源社区的力量快速发展中，聚集了众多 RSS 爱好者来为现代的网站构建 RSS 订阅源，目前已适配数百家网站的上千项内容。
- GitHub开源地址：https://github.com/DIYgod/RSSHub
- 官方文档：https://docs.rsshub.app/usage.html#sheng-cheng-ding-yue-yuan
- 部署文档：https://docs.rsshub.app/install/
>可以配合浏览器扩展 RSSHub Radar 和 移动端辅助 App RSSBud (iOS) 与 RSSAid (Android) 使用，找出网页的订阅源。

# 二.RSSHub的使用
### 1.生成订阅源
例如希望订阅 Twitter 上一个名为 DIYgod 的用户的时间线，根据 Twitter 用户时间线路由的文档，路由为 /twitter/user/:id， 把 :id 替换为用户名，得到路径为 /twitter/user/DIYgod，再加上域名 https://rsshub.app，一个订阅源就生成了：https://rsshub.app/twitter/user/DIYgod 然后我们可以把 https://rsshub.app/twitter/user/DIYgod ，添加到任意 RSS 阅读器里来使用， 其中域名 https://rsshub.app 可以替换为你自部署的域名，另外 RSSHub 支持很多实用的参数，比如内容过滤、全文输出等，可以在 通用参数 文档了解具体使用方法。
### 2.通用参数
提示:所有通用参数可以使用 & 连接组合使用，效果叠加。
##### (1.)内容过滤
可以使用以下 URL query 过滤内容，支持通过正则表达式过滤。
- filter 选出想要的内容。
- filter: 过滤标题和描述。
- filter_title: 过滤标题。
- filter_description: 过滤描述。
- filter_author: 过滤作者。
- filter_time: 过滤时间，仅支持数字，单位为秒。返回指定时间范围内的内容。如果条目没有输出pubDate或者格式不正确将不会被过滤。

举例: 
1. https://rsshub.app/bilibili/fav/2267573/801952073?filter=编曲|摄影 
2: https://rsshub.app/nga/forum/489?filter_time=600

- filterout 去掉不要的内容。
- filterout: 过滤标题和描述。
- filterout_title: 过滤标题。
- filterout_description: 过滤描述。
- filterout_author: 过滤作者。

举例: 
https://rsshub.app/bilibili/fav/2267573/801952073?filterout=编曲|摄影

- filter_case_sensitive 过滤是否区分大小写，filter 和 filterout同时适用 默认为 true，区分大小写。

举例: 
https://rsshub.app/bilibili/user/coin/2267573?filter=diyGOD|RSShub&filter_case_sensitive=false

##### (2.)条数限制
可以使用 limit 参数限制最大条数，主要用于排行榜类 RSS。

举例: bilibili 排行榜前 10 :
https://rsshub.app/bilibili/ranking/0/3?limit=10

##### (3.)全文输出
可以使用 mode 参数来开启自动提取全文内容功能。

举例: bilibili 专栏全文输出 :
https://rsshub.app/bilibili/user/article/334958638?mode=fulltext

##### (4.)访问控制
可以使用 code 或 key 进行访问控制。参考[访问控制配置](https://docs.rsshub.app/install/#pei-zhi-fang-wen-kong-zhi-pei-zhi)。RSSHub 支持使用访问密钥 / 码，白名单和黑名单三种方式进行访问控制。开启任意选项将会激活全局访问控制，没有访问权限将会导致访问被拒绝。同时可以通过 ALLOW_LOCALHOST: true 赋予所有本地 IP 访问权限。
**黑白名单**
WHITELIST: 白名单，设置白名单后黑名单无效。

**BLACKLIST: 黑名单**

黑白名单支持 IP、路由和 UA，模糊匹配，设置多项时用英文逗号 , 隔开，例如 WHITELIST=1.1.1.1,2.2.2.2,/qdaily/column/59

**访问密钥 / 码**
ACCESS_KEY: 访问密钥，用于直接访问所有路由或者生成访问码。访问码为 访问密钥 + 路由 共同生成的 md5。

##### (5.)输出 Telegram 即时预览链接
可以输出 Telegram 可识别的即时预览链接，主要用于文章类 RSS。 Telegram 即时预览模式需要在官网制作页面处理模板，请前往[官网](https://instantview.telegram.org/)了解更多。
tgiv: 模板 hash，可从模板制作页面分享出来的链接末尾获取（&rhash=后面跟着的字符串）
举例: 
https://rsshub.app/novel/biquge/94_94525?tgiv=bd3c42818a7f7e

##### (6.)输出 Sci-hub 链接
可以输出 Sci-hub 链接，用于知名期刊或输出 DOI 的科学期刊类 RSS。
scihub: 任意值开启
举例:
https://rsshub.app/pnas/latest?scihub=1

##### (7.)中文简繁体转换
opencc: s2t 简体转繁体、t2s 繁体转简体，其它可选值见 simple-wasm - Configurations，
举例: 
https://rsshub.app/dcard/posts/popular?opencc=t2s，

##### (8.)输出格式
RSSHub 同时支持 RSS 2.0 和 Atom 输出格式，在路由末尾添加 .rss 或 .atom 即可请求对应输出格式，缺省为 RSS 2.0
举例:
- 缺省 RSS 2.0 - https://rsshub.app/jianshu/home，
- RSS 2.0 - https://rsshub.app/jianshu/home.rss，
- Atom - https://rsshub.app/jianshu/home.atom，
和 filter 或其他 URL query 一起使用 https://rsshub.app/bilibili/user/coin/2267573.atom?filter=微小微|赤九玖|暴走大事件
  
##### (9.)debug
在路由末尾添加 .debug.json且实例运行在debugInfo=true的情况下，RSShub 将会返回插件设置在ctx.state.json的内容。
这功能皆在方便开发者调试问题，方便用户自行开发需要的功能。插件作者可以酌情考虑使用，没有格式要求。
举例：
/furstar/characters/cn.debug.json

##### (4.)输出简讯
可以使用 brief 参数输出特定字数 ( ≥ 100 字 ) 的纯文本内容
举例：
输出 100 字简讯: ?brief=100

# 三.本地部署RSSHub服务的优势
既然RSSHub官方提供的服务已经足够满足我们大多数情况的Rss订阅源的问题，那么为什么我们还需要自行部署RSSHub服务呢?原因如下:
1. RSSHub 使用非常简单，但随着使用者增多，微博、知乎加大了反爬限制。
2. RSSHub 的免费官方实例用户较多，许多路由因遭到了目标站点反爬虫措施的反制而无法使用。
3. 目前RSSHub已经被墙，如果没有梯子在墙内是无法访问的。
4. 目前大量第三方源都无法直接使用，只能自建 RSSHub 来解决稳定性。
5. 需要自己对一些特殊的网址进行自定义的规则。

>本文主要讲解的是内网部署服务，如果要部署到外网同理，请准备好域名和服务器，做好域名解析即可。

# 四.本地部署RSShub的三种方式
1. 手动部署:部署难度较高。
2. docker部署:部署难度较低。
3. docker-compose部署:部署难度较低(推荐)。
   
### 1.手动部署RSSHub服务
需要同步部署其他的运行环境，优点是可定制化较高，可以自由搭配，部署前安装好如下环境:
- git
- nodejs
- npm
##### (1.)安装RSSHub服务
部署 RSSHub 最直接的方式就是手动部署，可以按照以下步骤将 RSSHub 部署在您的电脑、服务器或者其他任何地方。
首先是下载 RSSHub 的源码:
```
$ git clone https://github.com/DIYgod/RSSHub.git
$ cd RSSHub
```
下载完成后，需要安装依赖（开发不用加 --production 参数）。
使用 npm:
```
$ npm ci --production
```
或 yarn:
```
$ yarn install --production
```
由于众所周知的原因，在国内使用 npm 下载依赖十分缓慢，建议挂一个代理或者考虑使用 NPM 的国内镜像。

##### (2.)启动RSSHub服务
然后在 RSSHub 文件夹中运行下面的命令就可以启动:
```
$ npm start
```
或
```
$ yarn start
```
在浏览器中打开 http://127.0.0.1:1200/。

>详细使用说明参照 指南 ，，替换所有路由例子中的 https://rsshub.app/ 为 http://localhost:1200 即可正常使用。

##### (3.)修改配置RSSHub服务
可以通过设置环境变量来配置 RSSHub:
在项目根目录新建一个 .env 文件，每行以 NAME=VALUE 格式添加环境变量，例如:
```
CACHE_TYPE=redis
CACHE_EXPIRE=600
```    
注意它不会覆盖已有的环境变量，更多配置项请看 [配置](https://docs.rsshub.app/install/#pei-zhi)

> 手动部署方式不包括 puppeteer 和 redis 依赖，如有需要请改用 Docker Compose 部署方式或自行部署外部依赖。

##### (4.)更新RSSHub服务版本
在 RSSHub 文件夹中运行下面的命令就从 github 仓库拉取最新版本即可:
```
$ git pull
```

### 2.Docker部署RSSHub服务
部署前置环境:
- docker环境
##### (1.)安装RSSHub服务
默认推荐使用diygod/rsshub即diygod/rsshub:latest最新版镜像以获取最新路由。 当diygod/rsshub:latest存在问题时，可以使用以日期为标签的近期镜像临时使用，例如:
```
$ docker pull diygod/rsshub:2021-06-18/diygod/rsshub:latest
```
待最新镜像更新后在切换回diygod/rsshub:latest最新版镜像。
运行下面的命令下载 RSSHub 镜像:
```
$ docker pull diygod/rsshub
```
然后指定好端口号运行 RSSHub 容器即可:
```
$ docker run -d --name rsshub -p 1200:1200 diygod/rsshub
```
在浏览器中打开 http://127.0.0.1:1200/
##### (2.)更新RSSHub版本
docker删除旧容器，然后拉取新镜像再生成容器:
```
$ docker stop rsshub
$ docker rm rsshub
```
或者进入容器对RSSHub版本进行升级。

##### (3.)更新RSSHub服务配置
配置运行在 docker 中的 RSSHub，最便利的方法是使用 docker 环境变量。
以设置缓存时间为 1 小时举例，只需要在运行时增加参数：-e CACHE_EXPIRE=3600:
```
$ docker run -d --name rsshub -p 1200:1200 -e CACHE_EXPIRE=3600 -e GITHUB_ACCESS_TOKEN=example diygod/rsshub
```
>该部署方式不包括 puppeteer 和 redis 依赖，如有需要请改用 Docker Compose 部署方式或自行部署外部依赖。

###3. Docker Compose 部署(推荐)
部署前置环境:
- docker环境
- Docker-Compose环境
##### (1.)创建安装目录
赋予要执行的Docker-Compose目录相应权限:
```
sudo chmod +x /usr/local/bin/docker-compose
```
创建docker-compose配置文件:
```
touch docker-compose.yml
```
编辑docker-compose配置文件:
```
version: '3'

services:
    rsshub:
        image: diygod/rsshub
        restart: unless-stopped
        ports:
            - '1200:1200'
        environment:
            NODE_ENV: production
            CACHE_TYPE: redis
            REDIS_URL: 'redis://redis:6379/'
            PUPPETEER_WS_ENDPOINT: 'ws://browserless:3000'
        depends_on:
            - redis
            - browserless

    browserless:
        image: browserless/chrome:1.43-chrome-stable
        restart: unless-stopped

    redis:
        image: redis:alpine
        restart: unless-stopped
        volumes:
            - redis-data:/data

volumes:
    redis-data:
```

##### (2.)创建RSSHub实例
先前台执行观察输出:
```
docker-compose up
```
若确认无误后便可置于后台持续运行:
```
docker-compose up -d
```
##### (3.)RSSHub版本更新
删除旧容器:
```
$ docker-compose down
```
如果之前已经下载 / 使用过镜像，下方命令可以帮助你获取最新版本：
```
$ docker pull diygod/rsshub
```
然后重复安装步骤。

##### (4.)更新RSSHub加配置
修改 docker-compose.yml 中的 environment 进行配置。

# 五.使用RSSHub自建服务
通过上面三种部署，我们就已经安装好了RssHub，服务使用方式如下:
1. 打开 RSSHub 接口指南，搜索需要订阅的网站。RSSHub 支持国内大部分的主流网站。
2. 将生成源  https://rsshub.app/xxx/xxx 其中域名 https://rsshub.app 替换为你自部署的域名，如http://192.168.52.131:1200/xxx/xxx 。

>在上文中我们通过三种不同的方式部署了RssHub服务，这里有个前提，就是自建 RSS 阅读器与自建 RSSHub 需要在同一内网内，这样才可以本地调用。如果要再外网使用需要将服务部署到云端并配置好域名。

如果不想去费时间搭建RSSHub，那么可以直接使用别人搭建好的:
```
https://rss.shab.fun/
https://rss.injahow.cn/
http://i.scnu.edu.cn/sub
http://rsshub.sksren.com/
https://rsshub-7x3pyolbs.vercel.app/
```
>如果侵权请联系笔者删除。

# 六.RssHub自定义订阅源规则
Rsshub官方和社区提供了很多的Rss订阅源，如果找不到你需要的Rss订阅源。可以通过添加自定义规则实现。若想添加自己的规则，则需要在服务器自行搭建Rsshub服务，通过对Rsshub源码进行修改就可以实现自定义规则的Rss订阅源。Rsshub是用Javascript写的，因此要修改源码，必须要要具备Javascript编程知识。
### 1.添加脚本路由
在源码的 /lib/router.js ，里添加路由
### 2.编写脚本
在源码的 /lib/routes/ ，中的路由对应路径下创建新的 js 脚本，主要有两个步骤:
1. 获取网页数据。
2. 对数据进行处理生成RSS源。
##### (1.)获取源数据
- 获取源数据的主要手段为使用 got ，发起 HTTP 请求（请求接口或请求网页）获取数据。
- 个别情况需要使用 puppeteer ，模拟浏览器渲染目标页面并获取数据。
- 返回的数据一般为 JSON 或 HTML 格式。
- 对于 HTML 格式的数据，使用 cheerio ，进行处理。
##### (2.)数据处理生成RSS源
对获取到的网页数据数据进行进一步处理，生成符合 RSS 规范的对象，把获取的标题、链接、描述、发布时间等数据赋值给 ctx.state.data， 生成 RSS 源:
```
ctx.state.data = {
    // 源标题
    title: `${name} 的 bilibili 投币视频`,
    // 源链接
    link: `https://space.bilibili.com/${uid}`,
    // 源说明
    description: `${name} 的 bilibili 投币视频`,
    //遍历此前获取的数据
    item: data.map((item) => ({
        // 文章标题
        title: item.title,
        // 文章正文
        description: `${item.desc}<br><img src="${item.pic}">`,
        // 文章发布时间
        pubDate: new Date(item.time * 1000).toUTCString(),
        // 文章链接
        link: `https://www.bilibili.com/video/av${item.aid}`,
    })),
};
```
### 3.总结
这里只讲解了如何自定义一个比较简单的Rss源，需要更多资料请查阅[文档](https://docs.rsshub.app/joinus/quick-start.html)。

# 七.使用RSSHub Radar插件
### 1.RSSHub Radar简介
[RSSHub Radar](https://github.com/DIYgod/RSSHub-Radar) 是 [RSSHub](https://github.com/DIYgod/RSSHub) 的衍生项目， 它是一个可以帮助你快速发现和订阅当前网站 RSS 和 RSSHub 的浏览器扩展。

* 快速发现和订阅当前页面自带的 RSS。
* 快速发现和订阅当前页面支持的 RSSHub。
* 快速发现当前网站支持的 RSSHub。
* 支持一键订阅 RSS 到 Tiny Tiny RSS、Miniflux、FreshRSS、Nextcloud News、Feedly、Inoreader、Feedbin、The Old Reader、Feeds.Pub、BazQux Reader、本地阅读器。

### 2.RSSHub Radar使用
1. 在浏览器Chorme商店里搜索并安装改插件。
2. 我们在进入一个新页面时， RSSHub Radar 会自动检测当前页面有没有 RSS 和 RSSHub 支持，检测到则会显示一个角标，如果我们想订阅当前页面的 RSS，点击扩展图标， 会弹出一个列表，如下图所示，列表有两项内容：当前页面上的 RSS、适用于当前页面的 RSSHub 你可以选择复制链接或一键订阅到Rss阅读器。
![image.png](https://upload-images.jianshu.io/upload_images/3067896-691e39784cc835fc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![image.png](https://upload-images.jianshu.io/upload_images/3067896-73619c18ccf7d5f3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


参考资料:
[rsshub官方文档](https://docs.rsshub.app/)
[rsshub开源地址](https://github.com/DIYgod/RSSHub)
[RSSHub-Radar开源地址](https://github.com/DIYgod/RSSHub-Radar)