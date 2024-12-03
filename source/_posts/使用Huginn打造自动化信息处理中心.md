---
title: 使用Huginn打造自动化信息处理中心
---

# 一.Huginn简介
在北欧神话中，奥丁的肩膀上坐着两只乌鸦，一只名叫 Huginn，一只名叫 Muninn。这两只乌鸦告诉奥丁他们的所见所闻，毫无遗漏。奥丁在黎明时派出它们，它们飞遍全世界然后在晚餐之前回来汇报，因此，奥丁能知晓很多事情。在[Huginn](https://github.com/huginn/huginn)的项目主页上，作者对它有详细的介绍。我们同样可以通过Huginn创建不同的代理，通过这些代理发送HTTP请求获得相关数据，然后将获取到的数据进行处理，就可以在互联网上面收集到各类我们需要的信息了。通过Huginn我们可以比较方便的实现如下功能:

- 监控你关心的事项例如知乎、微博、贴吧等平台指定的信息，一旦监控到信息，邮件通知你。
- 监控各大购物平台商品信息，一旦发现折扣信息，邮件通知你。
- 支持各种形式的发送和接收 WebHooks。
- 抓取网页内容并且在它们发生变化时发送邮件给你。
- 将获得的数据进行相应的格式处理并输出，例如RSS。
- 跟踪天气的变化，如果监测到明天要下雨或下雪，就会发邮件提醒你。

总得来说，Huginn可以帮助我们做好两件事情，一是定制化推送或提醒，二是聚合数据。

### 1.定制化推送或提醒
首先，定制化推送或提醒就像你平时设定闹钟一样，设定好时间或条件后，当时间或条件满足时，Huginn就会把信息推送给你，或提醒你该去做某件事情。比如说，明天下雨，提醒你带伞；电视剧或漫画更新，提醒你去观看或直接推送给你；感兴趣的商品降价，提醒你去购买；发生有趣的热点新闻，也会推送给你...诸如此类生活中很多零散的信息地处理，我们每天都在接收并处理这些信息。

### 2.聚合数据
聚合数据是指在将自己关注的包括但不仅限于微信公众号、知乎、简书、豆瓣、微博、Instagram等相关平台的资讯信息收集起来，在同一个平台进行阅读，RSS技术就能实现上述的功能，但是因为很多网站官方都没有提供Rss支持，那么可以通过Huginn将自己关注的信息渠道都制作成一个个RSS源，然后在RSS阅读器中集中阅读。

# 二.安装Huginn
### 1.常规手动安装Huginn
如果是常规安装方式，需要安装依赖包、ruby 环境、数据库、nginx、huginn 及各种配置。容易出错，因此不推荐此种安装方式，具体安装步骤可以参考[官网教程](https://github.com/huginn/huginn/wiki/Novice-setup-guide)。

### 2.Docker安装Huginn(推荐)
1. 首先你需要安装配置好Docker环境。

2. 然后通过 docker 来部署:

   ```
   docker search huginn/huginn
   docker pull huginn/huginn
   docker run -it -p 3000:3000 huginn/huginn
   ```

3. 然后在浏览器打开`` http://localhost:3000 ``即可看到效果，使用默认账号登录：

   ```
   用户名： admin
   密码：password
   ```

### 3.Huginn更换Mysql数据库
安装Huginn时会附带有一个轻量的数据库，但Huginn一删里面的数据就没了，所以非常有必要将Huginn的数据存储在mysql中可以方便我们对数据进行管理。
1. 在docker中配置好mysql和huginn。

2. 创建huginn容器时指定mysql数据库的信息。

   ```
   docker run  --name huginn -p 3000:3000 -e MYSQL_PORT_3306_TCP_ADDR=172.0.0.1 -e HUGINN_DATABASE_NAME=huginn -e HUGINN_DATABASE_USERNAME=root -e HUGINN_DATABASE_PASSWORD=123456 huginn/huginn
   ```

3. 最后在浏览器中输入http://你的服务器IP:3000并访问。

### 4.将huginn部署到 Heroku

[Heroku]([About Heroku | Heroku](https://www.heroku.com/about))是一个支持多种编程语言的云平台即服务，该平台提供了一些免费的云计算服务，如果我们不想自己购买云服务器，可以将huginn部署到Heroku。如果你要使用免费方案的话，你需要注意以下几点：

* 使用 Heroku 免费方案的用户，其每个网站在 30 分钟内无人访问后便会自动关闭，再有人访问时才会自动重新打开，因此为了使 Huginn 网站能长时间运行，可以使用类似[uptimerobot](https://uptimerobot.com/) 的[网站监控](https://cloud.tencent.com/product/cat?from=10680)服务，不停地ping你的 Huginn 网站地址；
* Heroku 免费方案只允许用户所有的应用每个月运行的总时长不超过 550 个小时（绑定信用卡的用户可额外再获得 450 个小时），这意味着你无法保证部署好的 Huginn 网站每个月每天都在运行，因此，你可选择绑定信用卡，或者让你的 Huginn 网站每天只允许 18 个小时，这样的话，你的网站每天都可以在运行；
* Heroku免费方案提供给用户的 Postgres[数据库](https://cloud.tencent.com/solution/database?from=10680)只有5M，存储的数据不能超过 10000 行，因此你需要控制 Agent 生成的事件的保留周期，同时限制数据库中 Agent 日志文件的长度，比如`heroku config:set AGENT_LOG_LENGTH=20`。
* Huginn安装在heroku的过程中默认使用的是SendGrid的邮箱服务器，这还需要我们添加SendGrid插件才能正常使用，但是添加插件需要先添加信用卡，因此，非信用卡用户无法使用SendGrid的邮箱服务器，建议添加其它邮箱服务器，比如，gmail邮箱服务器。

##### 部署到Heroku的操作步骤：

1. 注册[Heroku](https://www.heroku.com/) 平台账号，然后下载安装[Heroku Toolbelt](https://toolbelt.heroku.com/)；
2. 远程登录 Heroku：`heroku login`
3. 创建 app：`heroku create xxx`（xxx 为 app 的名字，下同）；
4. 将 app 下载到本地：`heroku git:clone --app xxx`
5. 将[huginn](https://github.com/cantino/huginn) 源代码全部下载拷贝到本地 app 的文件夹内；
6. 进入 app 文件目录，依次执行命令：`cp .env.example .env` 和`bundle`；
7. 提交代码变更：`git add .`、`git commit -am 'commit code'`；
8. 最后，执行脚本：`bin/setup_heroku`，完成部署。

> 如果嫌自己部署过于麻烦，也可以参考[Huginn官方(https://github.com/huginn/huginn#deployment)的一键部署到Heroku平台的方案。

##### 使用自己的邮箱[服务器](https://cloud.tencent.com/product/cvm?from=10680)

在安装过程中默认使用的是 SendGrid 的邮箱服务器（安装后需要自行配置），你也可以使用其他邮箱服务器，下面以谷歌邮箱服务器为例，需要进行以下配置：

`heroku config:set SMTP_DOMAIN=google.com`
`heroku config:set`[`[email protected]`](https://huginn.cn/cdn-cgi/l/email-protection)
` heroku config:set SMTP_PASSWORD=somepassword`
` heroku config:set SMTP_SERVER=smtp.gmail.com`
`heroku config:set`[`[email protected]`](https://huginn.cn/cdn-cgi/l/email-protection)` # 指定显示的发件人邮箱地址`

# 三.Huginn基本概念

如果将Huginn比如成一个数据加工工厂，每个Agents就像是一个个具有不同功能的车间，Agent可以接收数据并对数据进行加工，然后将加工好的数据输出。一组串联起来的Agents通过不断传递加工Event(产品)组成了一条流水线(scenarios)。

### 1.Agent：
Agent就是一个代理，例如抓取网页数据，清洗网页数据，输出为Rss源，这里的每一步都相当于是一个不同种类的车间，他们可以彼此依赖形成流水线，也可以单独工作。

### 2.Scenario：
Scenario就是一系列Agent的集合，就相当于是包含了很多车间的流水线，主要是对一系列Agent的集合进行归类，方便识别。

### 3.Event：
每一个Agent执行一次，输出就是Event，相当于是车间加工出来的产品，前一个`车间/Agent`输出的Event可以传递给下一个`车间/Agent`使用，再次进行加工。

>显然，Huginn能做什么，不能做什么，关键看它提供了哪些Agent。

# 四.入门实例-Huginn下雨天通知带雨具
例如，我们想把某个城市的天气预报数据抓取，对数据进行分析，判断明天是否会下雨，然后通过邮件提前通知明天带雨伞。 那么，我们需要写三个Agents，第一个Agent抓取天气预报的数据，第二个Agent会对天气预报的数据进行判断，判断明天是否会下雨， 最后一个Agent通过邮件通知明天下雨需要带雨伞。在Huginn中，会按照下图所示的流程进行工作：
![image.png](/images/4e11b363667bd5a3b02466c7dca0581e.webp)
### 1.创建抓取天气数据的Agent
#### 创建Agent代理
先登录Huginn，然后在左上角处点击创建新代理（New Agent）:
![image.png](/images/9d620e45030a39d0d00310e0945d0856.webp)

#### 选择代理类型
由于我们是对html网页类型进行解析,因此创建一个Website的代理:
![image.png](/images/b9eeea1adad51ac21ec6544a6de3026a.webp)

#### 基本信息填写
![image.png](/images/e0f7887ac0bf703e39d5c8d7765ebf91.webp)
- 红色部分为基本信息功能。
- 黄色部分为指导说明文档。
- 蓝色部分为抓取选项配置。
- 绿色部分为调试保存功能。

下面先看基本信息区主要有如下几个选项:
- Type(代理类型):选择代理的类型上一步我们选择的是Website,因此这里就不再选择了。
- Name(名称)：给这个 agent 取个名字，自己随便起一个就行。
- Schedule(日程)：调度周期，表示在什么时候自动执行这个 agent，比如 Every 1d 表示每一天执行一次、Every 2h 表示每2小时执行一次、8pm 表示每天下午8点执行等等；选择 3pm，每天下午3点执行一次，根据实际需要设置，比如你抓取的内容更新比较频繁，就把时间间隔设置的小一些，Every 5m、Every 10m之类的。
- Controllers(控制):除了系统定义之外，此代理上面的计划可以由这些用户定义的代理运行或控制，不用填写。
- Keep events(事件保留时间)：表示事件保留的时间；我们从网页上面获取到的信息都是一个 event，Huginn会把这些 event 保留在本地，你可以通过这个参数来设置这些 events 在本地保留多少时间，超过这个时间，Huginn会把数据清除，暂时设置成forever永不清除。
- Sources(来源端)：表示这个 agent 处理的数据来源是哪个 agent。我们现在创建的 agent 是第一个 agent，所以不需要从其他 agent 传递数据（也就是上面说的 events）过来，所以这个留空。
- Receivers(接收端)：表示这个 agent 处理完数据之后把这些数据传入到哪个 agent。用来转化数据，数据转化完之后，可能还需要其他 agent 把这些数据做进一步的转化。
- Scenarios(场景分类)：表示这个 agent 是数据哪个 Scenario 的，就是把这一系列的代理打个组这个分类，比较方便查看。

#### Options 配置填写
Options：这个非常关键，就是通过这个配置文件（JSON）来进行网络请求和数据解析相关的操作的，Options 配置其实就是一个 JSON 文件，最右上角的切换视图（Toggle View）可以切换视图和源码的编辑模式:
![image.png](/images/bd33621c497b08aa2bcca0b7ea92541d.webp)
Website Agent 的 Options 主要的元素有如下：
* url：网站地址，表示我需要从哪个网站获取数据。
* type：数据解析的类型，支持的类型有 `xml`、`html`、`json`、`text` 四种，当前网址返回的是 html，所以这里我们填写 `html`。如果其他场景，返回的类型可能就是 `json` 或者 `xml`了,需要具体分析。
* mode：表示获取数据的模式，这里选择 `on_change`。
   * on_change：在数据有更改时才会获取作为 events。
   * merge：把新数据和输入的数据进行合并。
   * all：获取所有数据。
* extract：用来配置（JSON）从这个网站解析出真正我们想要的数据。如果 `type` 是 `html`，则每个数据通过 `css` 选择器或者 `xpath` 来定位元素的位置然后解析出真正的数据。

打开[深圳天气预报,深圳7天天气预报,深圳15天天气预报,深圳天气查询 (weather.com.cn)](http://www.weather.com.cn/weather1d/101280601.shtml)，f12呼出开发者工具，然后分析网页的内容，可以看到元素对应的关系如下:
![image.png](/images/385754b30176d50aa3a3a330fb28da0f.webp)

根据如上网页的对应关系，编写Options如下:
```
{
	"expected_update_period_in_days": "2",
	"url": "http://www.weather.com.cn/weather1d/101280601.shtml",
	"type": "html",
	"mode": "on_change",
	"extract": {
		"day": {
			"css": "#today .clearfix li[1] .wea",
			"value": "text()"
		},
		"day_temperature": {
			"css": "#today .clearfix li[1] .tem span",
			"value": "text()"
		},
		"day_wind": {
			"css": "#today .clearfix li[1] .win span",
			"value": "normalize-space(.)"
		},
		"night": {
			"css": "#today .clearfix li[2] .tem span",
			"value": "text()"
		},
		"night_temperature": {
			"css": "#today .clearfix li[2] .win span",
			"value": "normalize-space(.)"
		},
		"night_wind": {
			"css": "#today .clearfix li[2] .wea",
			"value": "text()"
		}
	}
}
```
获取抓取到的结果:
![image.png](/images/d49247b39a99490d3b699248b3204d72.webp)

>如果想看抓取到的页面具体的数据有哪些可以在extract中定义一个``"html内容": {"css": "html","value": "."}``将html标签中的所有内容输出进行查看。



**Json格式数据解析**
1. 如果网页获取到的是如下的JSon数据：
   ```
   { "results": {
       "data": [
         {
           "title": "Lorem ipsum 1",
           "description": "Aliquam pharetra leo ipsum."
           "price": 8.95
         },
         {
           "title": "Lorem ipsum 2",
           "description": "Suspendisse a pulvinar lacus."
           "price": 12.99
         },
         {
           "title": "Lorem ipsum 3",
           "description": "Praesent ac arcu tellus."
           "price": 8.99
         }
       ]
     }
   }
   ```
2. 填写抓取规则：
   ```
   "extract": {
     "title": { "path": "results.data[*].title" },
     "description": { "path": "results.data[*].description" }
   }
   ```
3. 抓取到的数据：
   ```
   [
     {
       "title": "Lorem ipsum 1",
       "description": "Aliquam pharetra leo ipsum."
     },
     {
       "title": "Lorem ipsum 2",
       "description": "Suspendisse a pulvinar lacus."
     },
     {
       "title": "Lorem ipsum 3",
       "description": "Praesent ac arcu tellus."
     }
   ]
   ```

### 2.过滤天气数据Agent
#### 创建TriggerAgents
过滤Agent用的是`TriggerAgent`。建立一个TriggerAgent。把刚才创建的WeatherAgent设置为源。TriggerAgents 包含一套规则，所有这一切都必须为触发匹配。![image.png](/images/237e3a183353f1f9b667320b2b75ec78.webp)

#### Agents配置填写
keep event这里选择的是false，意思是不生成过滤之后的事件，直接传递message的内容给下一个agent。如果你希望对过滤后余下的信息进一步利用，比如再次过滤之类，可以选择true以保留事件。`type`指的是类型，regex指的是正则匹配，系统会检测上一个agent生成的内容（这里选择的是`path：title`，意思是把传递过来的事件中的title作为过滤的对象），和`value`中内容进行比较，如果这个event中包含这些`value`，那么生成事件，否则不生成。`value`中的竖分割线指的是或的意思，出现其中任何一个词即可通过过滤器，生成事件。!regix 指的是不匹配，它会检测`path`和`value`的相似程度，如果`path`中出现`value`的值，则不输出，反之，则通过过滤器并输出、生成事件。
![image.png](/images/e835805aacad65d67eef63bbe220b980.webp)

### 3.通知用户的Agent
将huginn event的内容推送到通知平台。这样的服务商比较不错的有两个：
- 邮件agent。
- slack agent。

其中邮件推送最经济实惠，不受平台约束；slack是一个和企业微信比较像的国外交流软件，可能面临着封杀的危险，但是功能丰富，支持桌面端、Chrome插件、iOS和Android端，界面漂亮，并且可以自己选择把消息推送到哪一个群组。

# 五.进阶实例抓取Github点赞最多的项目列表生成Rss
抓取Github数据生成Rss需要进行三个步骤也就是需要三个Agent:
1. 获取Github点赞最多的十条项目列表数据的Agent。

2. 根据列表数据获取项目详情数据的Agent。

3. 将数据组合生成Rss数据进行输出的Agent。
   ![image.png](/images/6fab76d1341a7d64be08158e6c4de123.webp)

> 以下内容是针对静态网页的抓取步骤指南，如果需要抓取动态网页（大型网站有一些用的是动态，普通网站还是静态为主），其实就在以下步骤之前多一步，用Phantom Js Cloud Agent渲染动态网页成静态页面后接下文的步骤即可。

### 1.创建Agent抓取列表数据

#### 新建列表页的Agent
先登录Huginn，然后在左上角处点击创建新代理（New Agent）:
![image.png](/images/22485c9c2daac7d6424c6f7e41df43ae.webp)

#### 选择代理类型
由于我们是对html网页类型进行解析，因此创建一个Website的代理:
![image.png](/images/e9d5588914faa28674f829fbda6228aa.webp)

#### 基本信息填写
抓取[github star最多star的项目](https://github.com/search?q=stars%3A%3E10000)
- 1.通过F12查看元素，可以看到左边每一条项目对应的是右边源代码里面class为repo-list的ul标签中的li标签，对应关系如下:
  ![d1f1179bfdf64ca03593189516cf782.png](/images/e0c8276eb2d0341155138040b97073d4.webp)

- 2.编写解析规则，通过Css选择器和Xpath进行元素定位都可以。

   - 使用Css选择器进行元素定位取出数据:

     ```
     {
       "expected_update_period_in_days": "2",
       "url": "https://github.com/search?q=stars%3A%3E10000",
       "type": "html",
       "mode": "on_change",
       "extract": {
         "title": {
           "css": ".repo-list .v-align-middle",
           "value": "text()"
         },
         "url": {
           "css": ".repo-list .v-align-middle",
           "value": "@href"
         },
         "desc": {
           "css": ".repo-list  .mb-1",
           "value": "text()"
         },
         "stars": {
           "css": ".repo-list .mr-3 .Link--muted",
           "value": "text()"
         }
       }
     }
     ```

   - 使用xpath进行元素定位取值:
     ```
     {
       "expected_update_period_in_days": "2",
       "url": "https://github.com/search?o=desc&q=stars%3A%3E10000&s=stars&type=Repositories",
       "type": "html",
       "mode": "on_change",
       "extract": {
         "title": {
           "xpath": "//*[@id=\"js-pjax-container\"]/div/div[3]/div/ul/li[*]/div[2]/div[1]/div[1]/a",
           "value": "string(.)"
         },
        "url": {
          "xpath": "//*[@id=\"js-pjax-container\"]/div/div[3]/div/ul/li[*]/div[2]/div[1]/div[1]/a",
           "value": "@href"
         },
         "desc": {
           "xpath": "//*[@id=\"js-pjax-container\"]/div/div[3]/div/ul/li[*]/div[2]/p",
           "value": "normalize-space(.)"
         },
         "stars": {
           "xpath": "//*[@id=\"js-pjax-container\"]/div/div[3]/div/ul/li[*]/div[2]/div[2]/div/div[1]/a",
           "value": "normalize-space(.)"
         }
       }
     }
     ```

> - title和url,desc，stars表示对抓取字段映射的名称，可随意命名；
> - 属性用@属性名进行取值 @href表示抓取对应css标签的href属性值，还有@src，@title等等；
> - 如果要抓取对应标签的值，可填`.`(包括html代码的全部内容），`string(.)`（只包含对应标签的值），text()等同string(.)
> - normalize-space是xpath的语法可以去除多余的空格。


- 3.调试，点击dry run:
  ![image.png](/images/298fb84a00dce923ec6c1ed25dafe46f.webp)
- 4.可以看到我们抓取到的数据了:
  ![image.png](/images/70c017fe24bc055ad7b8d4a3abf08b4a.webp)

然后点击save保存，保存后run一下，然后就会有生产出很多events，就是获取到的数据。如果没有获取到可能是数据库的问题。这里我们已经抓到Github列表页的数据了，下面我们根据列表页抓到的的Url取去抓详情页的数据。

### 2.创建Agent抓取GIthub项目的详情页

#### 新建详情页的Agent
同样的，Type选择``Website Agent``，由于详情是需要依赖列表中跳转详情的列表链接，Sources选中刚才创建的列表Agent，选择框勾选好:
![image.png](/images/74de2e70147d735687b12c03afb83138.webp)

#### 根据依赖的Agent获取详情页数据
{% raw %}
{{url}}即第一个Agent传过来的超链接参数，需要用到第一个agent的参数需要用{{}}包起来就可以了，这里mode一定填写merge，这样两个Agent的字段就组合到一起了:
![image.png](/images/6790c781a366989f078a70f7a3bebef7.webp)
{% endraw %}
```
{
  "expected_update_period_in_days": "2",
  "url": "https://github.com{{url}}",
  "type": "html",
  "mode": "merge",
  "extract": {
    "hovertext": {
      "css": "html",
      "value": "."
    }
  }
}
```

#### 调试详情页Agent

同样的选择一个接受到的event测试一下
![image.png](/images/8e538cc2b6c97611c4429db9119cfa2a.webp)

可以看到数据已经组合起来了:
![image.png](/images/7eb651b6b464156e743298205d9049e6.webp)

#### 保存详情页Agent
点击Save保存，此时我们点击github列表数据Agent的run功能生成数据:

![image.png](/images/b3106845630beb9ff4fa89e6248126eb.webp)

查看生成的Events数据:

![image.png](/images/f40042112b6b590eef73431cf1331e0d.webp)

可以看到列表Agent的时候也将详情的Agent进行执行了，并且将数据合并生成:

![image.png](/images/709a1591d58d37193205625db01a1db9.webp)

### 3.创建输出成RSS数据的Agent
#### 新建Rss输出的Agent
Type选择Data output Agent
![image.png](/images/a579f44f180b7cfd4d11d5a314870148.webp)

#### 依赖详情页Agent
Sources选择详情页Agent，secrets填写RSS地址自定义的末尾名称，item下就是RSS中的每一条信息了，填写上对应参数，其他默认即可。最后点击保存
![image.png](/images/e356baf88a22c109a25679aef39b287d.webp)
```
{
  "secrets": [
    "Github"
  ],
  "expected_receive_period_in_days": 2,
  "template": {
    "title": "Github点赞数前十名排行榜",
    "description": "本数据来自于GitHub官方",
    "item": {
      "title": "{{title}}",
      "description": "Secret hovertext: {{hovertext}}",
      "link": "{{url}}"
    }
  },
  "ns_media": "true"
}
```
至此，一个专属RSS源就已生成

#### 添加到Rss源到Rss阅读器
点击Agent
![image-20220419231802798.png](/images/e4d757b9af70bd8850b6d3284ab749f3.webp)
点击Agent就能看到下图所示，把它添加到RSS阅读器上去吧。
![image.png](/images/f0d471b7cca9b354bda6c6ff1a51d000.webp)
后续只要定时或者是手动执行第一个获取列表数据的Agent就回去执行后续的两个Agent生成Rss数据源，通过RSS阅读器进行订阅我们就可以看到抓取的信息流了。

# 六.补充知识Html元素定位
上文中笔者使用了Css选择器来定位元素，关于在HTML中定位元素常用的方式有三种正则表达式，xpath提取，css选择器。之前笔者在Python爬虫的相关文章中也有专门的讲解，有兴趣的同学欢迎前去考古。
### 1.Css选择器定位元素
在 CSS 中，选择器是一种模式，用于选择需要添加样式的元素。Css的定位更灵活，因为他它用到的更多的匹配符和规格。"CSS" 列指示该属性是在哪个 CSS 版本中定义的。（CSS1、CSS2 还是 CSS3。）
|选择器	|例子|	例子描述|	CSS|
|-|-|-|-|
|.class|	.intro	|选择 class="intro" 的所有元素。|	1|
|#id	|#firstname	|选择 id="firstname" 的所有元素。|	1|
|*	|*	|选择所有元素。|2|
|element|	p	|选择所有 <p> 元素。|1|
|element,element	|div,p	|选择所有 <div> 元素和所有 <p> 元素。	|1|
|element element	|div p	|选择 <div> 元素内部的所有 <p> 元素。	|1|
|element>element	|div>p	|选择父元素为 <div> 元素的所有 <p> 元素。	|2|
|element+element	|div+p	|选择紧接在 <div> 元素之后的所有 <p> 元素。	|2|
|[attribute]	|[target]	|选择带有 target 属性所有元素。	|2|
|[attribute=value]	|[target=_blank]	|选择 target="_blank" 的所有元素。	|2|
|[attribute~=value]	|[title~=flower]|	选择 title 属性包含单词 "flower" 的所有元素。	|2|
|[attribute\|=value]	|[lang\|=en]	|选择 lang 属性值以 "en" 开头的所有元素。	|2|
|:link	|a:link	|选择所有未被访问的链接。	|1|
|:visited	|a:visited|	选择所有已被访问的链接。	|1|
|:active	|a:active|	选择活动链接。	|1|
|:hover|	a:hover	|选择鼠标指针位于其上的链接。	|1|
|:focus	|input:focus	|选择获得焦点的 input 元素。	|2|
|:first-letter	|p:first-letter	|选择每个 <p> 元素的首字母。	|1|
|:first-line	|p:first-line	|选择每个 <p> 元素的首行。	|1|
|:first-child	|p:first-child	|选择属于父元素的第一个子元素的每个 <p> 元素。	|2|
|:before	|p:before	|在每个 <p> 元素的内容之前插入内容。	|2|
|:after	|p:after	|在每个 <p> 元素的内容之后插入内容。	|2|
|:lang(language)	|p:lang(it)	|选择带有以 "it" 开头的 lang 属性值的每个 <p> 元素。	|2|
|element1~element2	|p~ul	|选择前面有 <p> 元素的每个 <ul> 元素。	|3|
|[attribute^=value]	|a[src^="https"]	|选择其 src 属性值以 "https" 开头的每个 <a> 元素。	|3|
|[attribute$=value]	|a[src$=".pdf"]	|选择其 src 属性以 ".pdf" 结尾的所有 <a> 元素。	|3|
|[attribute*=value]	|a[src*="abc"]	|选择其 src 属性中包含 "abc" 子串的每个 <a> 元素。	|3|
|:first-of-type	|p:first-of-type|	选择属于其父元素的首个 <p> 元素的每个 <p> 元素。	|3|
|:last-of-type	|p:last-of-type	|选择属于其父元素的最后 <p> 元素的每个 <p> 元素。	|3|
|:only-of-type	|p:only-of-type	|选择属于其父元素唯一的 <p> 元素的每个 <p> 元素。	|3|
|:only-child	|p:only-child	|选择属于其父元素的唯一子元素的每个 <p> 元素。	|3|
|:nth-child(n)	|p:nth-child(2)	|选择属于其父元素的第二个子元素的每个 <p> 元素。	|3|
|:nth-last-child(n)	|p:nth-last-child(2)	|同上，从最后一个子元素开始计数。	|3|
|:nth-of-type(n)	|p:nth-of-type(2)	|选择属于其父元素第二个 <p> 元素的每个 <p> 元素。	|3|
|:nth-last-of-type(n)	|p:nth-last-of-type(2)	|同上，但是从最后一个子元素开始计数。	|3|
|:last-child	|p:last-child	|选择属于其父元素最后一个子元素每个 <p> 元素。	|3|
|:root	|:root	|选择文档的根元素。	|3|
|:empty	|p:empty	|选择没有子元素的每个 <p> 元素（包括文本节点）。	|3|
|:target	|#news:target	|选择当前活动的 #news 元素。	|3|
|:enabled	|input:enabled	|选择每个启用的 <input> 元素。	|3|
|:disabled	|input:disabled	|选择每个禁用的 <input> 元素	|3|
|:checked	|input:checked	|选择每个被选中的 <input> 元素。	|3|
|:not(selector)	|:not(p)	|选择非 <p> 元素的每个元素。	|3|
|::selection	|::selection	|选择被用户选取的元素部分。	|3|

CSS选择器有很多，像标签选择器、类选择器、ID选择器、关系选择器、伪类选择器、分组选择器等等，但是只需要掌握常用的几种就可以满足定位元素的需求。

以下述HTML为例，总结下CSS选择器的用法：

```
<div id="menu" class="menu" title="menu">
	<ul>
		<li id="first" class="catagory book">
			<a id="book">
			</a>
		</li>
		<li id="second" class="catagory food">
			<a id="food">
			</a>
		</li>
		<li>
			<a id="clothes">
			</a>
		</li>
		<li title="submenu">
			<a id="furniture">
			</a>
		</li>
	</ul>
	<a href="....">
		Welcome to Our Store
	</a>
</div>
```

1. 标签选择器
   使用HTML标签来选择元素，例如：
   ```
   driver.findElement(By.cssSelector("li"));   //将选择所有li元素
   driver.findElement(By.cssSelector("*a*")); //将选择所有a元素
   ```
2. 类选择器
   使用类名来选择元素，使用方法：.class， 例如：
   ```
   driver.findElement(By.cssSelector("div.menu")); //将选择class为menu的div元素
   driver.findElement(By.cssSelector(".catagory")); //将选择id为first的元素和id为second的元素，因为这两个元素的class里都含有catagory
   ```
3. ID选择器
   使用ID来选择元素，使用方法：#id，例如：
   ```
   driver.findElement(By.cssSelector("a#clothes")); //将选择id为clothes的a元素
   ```
   也可以写成：
   ```
   driver.findElement(By.cssSelector("#clothes")); //因为id是唯一的所以还是会选择id为clothes的a元素
   ```
4. 关系选择器
   **div,p** 作用：选择所有div元素和p元素
   **div>p** 作用：选择div的直接子元素中的所有p元素
   **div p**   作用：选择div的后代元素中的所有p元素

5. 属性选择器
   **[title]**   作用：选择所有具有title属性的元素
   **[title='menu']**   作用：选择所有title属性值等于'menu'的元素
   **[title~='menu']**   作用：选择所有title属性值包含menu的元素，注意：menu必须是一个word，且有空格与其他单词分开
   **[title*='menu']**   作用：选择所有title属性值包含menu的元素，注意：此时menu为substring，而不是word
   **[title|='menu']   **作用：选择所有title属性值以menu开头或者等于menu的元素
   **[title^='menu']**   作用：选择所有title属性值以menu开头的元素
   **[title$='menu']**   作用：选择所有title属性值以menu结尾的元素
   **div[title='menu']**   作用： 选择所有title属性值等于menu的div元素

6. 通用选择器
   方法：*
   ```
   div ul *; //选择div ul 下的所有子元素，包括li和a元素
   ```
7. 伪类选择器
   伪类选择器很多，只总结下用过的:nth-child(n)
   ```
   p:nth-child(2) 作用：选择作为第二孩子的p元素
   ```

### 2.Xpath定位元素
XPath 是一门在 XML 文档中查找信息的语言。XPath 可用来在 XML 文档中对元素和属性进行遍历。XPath 使用路径表达式来选取 XML 文档中的节点或者节点集。这些路径表达式和我们在常规的电脑文件系统中看到的表达式非常相似。XPath 含有超过 100 个内建的函数。这些函数用于字符串值、数值、日期和时间比较、节点和 QName 处理、序列处理、逻辑值等等。. 在 XPath 中，有七种类型的节点：元素、属性、文本、命名空间、处理指令、注释以及文档节点（或称为根节点）。[XML](https://so.csdn.net/so/search?q=XML&spm=1001.2101.3001.7020) 文档是被作为节点树来对待的。树的根被称为文档节点或者根节点。详情请参考[XPath 教程 (w3school.com.cn)](https://www.w3school.com.cn/xpath/index.asp)

### 3.定位元素总结
在浏览器中按F12打开开发者工具，然后选择你要的元素，**右键**选择 **Inspect**。可以看到 审查元素信息已经出来了。**右键**选择之后然后复制。我们既可以复制成Xpath的也可以复制成Css选择器的路径。

# 七.Huginn总结
Huginn可以订阅任意你想要订阅的网站与平台，例如微信公众号、简书、知乎、博客、图虫、等等，只要有网页同时生成了CSS，你就可以派出你的“Agent”去把他们抓回来，然后将他们“分门别类”，任意处置了。Huginn的门槛就在于环境的部署以及Website Agent规则的制定。虽然说Huginn有scenarios可供导入导出，但是目前为止还没有一个大规模的scenarios库，所以Huginn普及是非常困难的。目前，大家可以在这里找到几个可供使用的脚本库：http://huginnio.herokuapp.com/scenarios。

参考资料:

[huginn/huginn: Create agents that monitor and act on your behalf. Your agents are standing by! (github.com)](https://github.com/huginn/huginn)

[上手huginn的第一篇教程：一个定时监控黄金价格的rss - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/75730603)

[简单上手的huginn教程（2）——将抓取的内容推送至微信 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/80725216)

[简单上手的huginn教程（3）——对监控的时间进行更精确的控制 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/83507407)

[huginn|全网数据监控与通知工具—安装教程、全方位介绍 | VPS精选网 (vpsjxw.com)](https://www.vpsjxw.com/vps_use/huginn_intro/)

[利用Huginn抓取任意网站RSS和微信公众号更新-打造一站式信息阅读平台 | 麦田一棵葱 (52maicong.com)](https://www.52maicong.com/shiyong/8314.html)

[超详细!如何利用Huginn制作专属RSS - 谁是小菜鸡 - 博客园 (cnblogs.com)](https://www.cnblogs.com/liujiangblog/p/12115804.html)