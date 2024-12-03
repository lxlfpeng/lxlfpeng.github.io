---
title: 使用Feed43为网页生成RSS订阅源
---

# 简介
在我们使用Rss时候发现很多的网站并不支持Rss服务，如果自己使用Rsshub，Huginn等搭建订阅源，不单单需要懂一些编程和服务器部署的知识，还需要买服务器。如果只是轻度的使用那么完全可以试试FEED43，通过FEED43提供的免费服务可以为静态网页生成订阅源。

# 步骤总览
1. 准备好需要解析的网站网址(必须是服务端渲染页面网站，也就是常说的静态网页)。
2. 注册好Feed43的账号，并登录。
3. 使用Feed43解析网页源码。
4. 分析网页源码，找到哪一动态部分内容是自己需要的。
5. 根据分析出来的自己需要获取的动态内容编写提取规则。
4. 根据提取出来的内容调整优化提取规则。
5. 将提取出来的内容匹配到信息流。
6. 生成Rss订阅源，完成订阅。

# 准备好网址
这里我们用[电脑爱好者](https://www.cfan.com.cn/)这个网站，我们需要爬取这一个列表里面的内容。
![](https://img-blog.csdnimg.cn/img_convert/d3b0ac4c800976e57e8f42614eac05e6.png)

>必须是服务端渲染页面网站，也就是常说的静态网页。网页端渲染的页面是无法获取内容的。
# 注册账号
1. [Feed43](https://feed43.com/)官网注册好账号。
2. 打开[Feed43](https://feed43.com/)官方网站，点击Create your first RSS feed。

# 使用Feed43解析出网页源码

![image.png](https://img-blog.csdnimg.cn/img_convert/5f625ba4be5f2858cd17af21c532452b.png)

填入网址进行解析:

![](https://img-blog.csdnimg.cn/img_convert/c9bccffe8393bd9f6ee0e776d614a1c7.png)

点击 Reload，你就会在下面的选框中看到当前网页的源代码了。

# 分析网页源码

![](https://img-blog.csdnimg.cn/img_convert/c74be631d23e86d523726cf2e632a109.png)

Feed43 它会自动捕捉一些标记标题的源码，并标识成粉红色，当然也不是很准确，需要自己酌情修改。通过比对源码我们发现，有如下代码是一致的，只是内容不同，也就是我们需要的列表里面的内容:

```
<a href="https://www.cfan.com.cn/2022/0411/136391.shtml" target="_blank" title="系统小技巧：按需显示 文件夹查看方式我做主">
<div class="left-post-pic" style="background:url(https://upload.cfan.com.cn/2022/0411/1649641391945.png)no-repeat center;background-size:cover;"></div>
<div class="left-post-info" style="position:relative;">
<h1 class="left-post-title">系统小技巧：按需显示 文件夹查看方式我做主</h1>
<div class="left-post-txt">为了便于查看和整理文件，我们经常会对文件夹的查看方式进行专门的设置，比如查看图片文件夹习惯于使用缩略图的方式，查看文档则喜欢使用列表形式，而对于文档、图片混合的...</div>
</a>
```

# 定义提取规则
定义提取规则。将标题、链接等变化的字段删去用``{%}``代替。将固定且多余的字段删去用``{*}``代替。源码中有换行的地方均需要添加``{*}``。
```
<a href={%} {*} title={%}>{*}
<div class="left-post-pic" style="background:url({%})no-repeat center;background-size:cover;"></div>{*}
<div class="left-post-info" style="position:relative;">{*}
<h1 class="left-post-title">{%}</h1>{*}
<div class="left-post-txt">{%}</div>{*}
</a>{*}
```
# 检查匹配规则
将上一步我们定义好的规则进行填入:
![](https://img-blog.csdnimg.cn/img_convert/d5e2e0adfb3eee35d35acf41e7cef6b7.png)
显示绿色的OK (N items found)，则代表成功了。看一看抓取到的内容是否有格式错误的地方。如果没有抓取到内容，或者有格式错误，则需要继续仔细分析然后进行调整。

# 匹配信息流数据

这一步需要将定义提取规则获取到的动态内容和我们Rss信息流匹配起来，Item Title Template（标题）、Item Link Template（链接）、Item Content Template（全文内容），将第二步获取到的内容输入，{ \ % 数字}的形式

![](https://img-blog.csdnimg.cn/img_convert/f42f2d9104f46ce240a1fb6d88cf2d68.png)

# 生成Rss订阅源
![](https://img-blog.csdnimg.cn/img_convert/01014ed517d61758d03808c522d98091.png)
当然，你也可以随时修改或者删除此RSS订阅源。
# 总结
使用 Feed43 最大的好处就是，不需要自己搭建服务器就可以将那些不支持 RSS 的页面变成 RSS 方便订阅。Feed43的缺点，免费版只会每6小时抓取一次，每次只提取20条消息。