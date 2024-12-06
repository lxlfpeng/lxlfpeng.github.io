---
title: Node.js教程
date: 2022-06-29
categories: 
  - NodeJs
tags:
  - NodeJs
---

# Node.js简介
### 什么是Node.js
js 属于一种脚本性语言，然而脚本语言运行需要一个解析器来解析，对于我们原来写的 js 代码大部分都是运行在网页上，所以浏览器本身就担当了解析器的角色。而现在对于独立运行在服务器的 js 代码，node 就属于那个解析器。
Node.js 是基于Chrome V8 引擎的JavaScript 运行环境，简单理解就是一个可以让JavaScript脱离浏览器，执行的平台，并对JavaScript功能进行了增强（文件系统，模块，包，操作系统API，网络通讯，数据库操作等）

Node.js官网的描述:
- Node.js 是一个基于 Chrome V8 引擎的 JavaScript 运行环境
- Node.js 使用了一个事件驱动、非阻塞式 I/O 的模型，使其轻量又高效

> V8 属于 Google Chrome 浏览器的一个高性能引擎，可以直接将 JavaScript 编译为本地机器代码，而其他的语言如 PHP 和 Ruby，Java 每次访问时都必须通过解释器运行。

### Node.js的应用领域
* Web 应用这也是 Node 诞生要解决的主要问题，相对于多线程，Node.js 异步 I/O 是更理想的解决方案，现在也有了 egg、nest 等优秀的企业级 web 框架，前端可以轻松开发 web 应用。
* 各种命令行工具，例如 比较实用的 vue-cli
* 跨平台客户端 像微信小程序使用的 nw.js Electron 等
* 前端组件化构建相关工具 Gulp 、Webpack 等
* 客户端产品Electron让前端也可以写一些复杂的跨平台客户端应用，我们最熟悉的应该是 VS code

### Node.js劣势

* 计算密集型应用 如果非要把 Javascript 和 C 去拼计算性能，结果可想而知。
* 内存控制 把 js 和 java 比较复杂数据类型定义的话，也是不明智的。因为 js 的面向对象是基于 JSON 的，而 java 是直接使用内存结构。所以，通过 JSON 序列化和反序列的过程控制内存，js 在开始就已经败了。
* 静态服务器，I/O 密集应用固然是 node 的优势，但是你非要把它和 Nginx 这种专业处理静态资源服务放一起对比的话那本身就已经输了
* 本身不需要异步处理的应用：比如自行化脚本，如果使用 node 的话效果上先不说好不好，光从写代码人文角度，一些异步回调的处理就给我们带来不必要的麻烦

# Windows安装Node.js

## 1.下载

**[Node.js官网下载](http://nodejs.cn/download/)** 根据自身系统下载对应的安装包

## 2.安装
双击安装包，点击Next，勾选使用许可协议，点击Next，选择安装位置（可根据个人情况更换路径）,可以选择勾选Add to Path,将Node.js环境添加到系统变量里面去。

## 3.验证是否安装成功

进入cmd命令行窗口，输入node -v查看Node.js版本

```
node -v
```
如果安装正常就可以看到Node.js的版本。

## 4.交互模式
在命令提示符输入node，此刻你将进入Node.js的交互环境。 在交互环境下，你可以输入任意JavaScript语句，例如100+200，回车后将得到输出结果。 
```
C:\Users\peng>node
Welcome to Node.js v16.14.2.
Type ".help" for more information.
> 100+100
200
```
要退出Node.js交互环境，连按两次Ctrl+C。

也可以写一个`test.js`的文件，内容如下：
```
console.log(100 + 200 + 300);
```
再执行如下命令，就可以看到结果：

```
C:\Workspace>node calc.js
600
```
Node的交互模式和直接运行`.js`文件有什么区别？
- 直接输入`node`进入交互模式，相当于启动了Node解释器，但是等待你一行一行地输入源代码，每输入一行就执行一行。
- 直接运行`node hello.js`文件相当于启动了Node解释器，然后一次性把`hello.js`文件的源代码给执行了，你是没有机会以交互的方式输入源代码的。

# Npm包管理工具
### Npm包管理简介
npm是一个基于Node.js的JavaScript包管理工具，全称叫做node package manager，所谓的包呢，其实就是可复用的代码，每个人都可以把自己编写的代码库发布到npm的源，英文叫做registry，上面进行管理，你也可以下载别人开发好的包，
在你自己的应用当中使用。 我们所熟知的，jQuery/Bootstrap/React等框架或库都被托管在npm上。通过使用npm作为项目的包管理工具，我们可以很方便地在我们的开发项目中引入以及管理第三方的框架或者库，
而不需要像以前前端开发的原始时期一样，手动复制粘贴代码文件。更重要的是，如果我们要使用模块A，而模块A又依赖于模块B，模块B又依赖于模块X和模块Y，npm可以根据依赖关系，把所有依赖的包都下载下来并管理起来。否则，靠我们自己手动管理，肯定既麻烦又容易出错。npm已经在Node.js安装的时候顺带装好了。在命令提示符或者终端输入npm -v，就可以看到Npm的版本。

### Npm常见命令
1. **`npm -v`：**查看npm版本。
2. **`npm init`：**初始化后会出现一个`package.json`配置文件。可以在后面加上`-y` ，快速跳过问答式界面。
3. **`npm install`：**会根据项目中的`package.json`文件自动下载项目所需的全部依赖。
4. **`npm install 包名 --save-dev`(`npm install 包名 -D`)：**安装的包只用于开发环境，不用于生产环境，会出现在`package.json`文件中的`devDependencies`属性中。
5. **`npm install 包名 --save`(`npm install 包名 -S`)：**安装的包需要发布到生产环境的，会出现在package.json文件中的`dependencies`属性中。
6. `npm list`：查看当前目录下已安装的node包。
7. `npm list -g`：查看全局已经安装过的node包。
8. `npm --help`：查看npm帮助命令。
9. `npm update 包名`：更新指定包。
10. `npm uninstall 包名`：卸载指定包。
11. `npm config list`：查看配置信息。
12. `npm 指定命令 --help`：查看指定命令的帮助。
13. `npm info 指定包名`：查看远程npm上指定包的所有版本信息。
14. `npm config set registry https://registry.npm.taobao.org`： 修改包下载源，此例修改为了淘宝镜像。
15. `npm root`：查看当前包的安装路径。
16. `npm root -g`：查看全局的包的安装路径。
17. `npm ls 包名`：查看本地安装的指定包及版本信息，没有显示empty。
18. `npm ls 包名 -g`：查看全局安装的指定包及版本信息，没有显示empty。

### 修改Npm缓存目录
npm 默认缓存目录是 ``C:\Users\Administrator\AppData\Roaming\npm-cache ``，不仅不便于管理而且占用C盘空间，为了保留C盘的剩余空间，有必要，把 npm的 缓存路径修改到其他盘符下。
1. 设置 npm 缓存路径
```
npm config set cache "D:\nodejs\npm_cache"
```
修改完成之后， 使用``npm config ls ``命令就会看到变化。而且 .npmrc 文件也会有变化，这个文件在C盘的用户目录下，比如 C:\Users\Administrator。

2. 恢复npm默认路径
- 通过命令``npm config ls``,获取到.npmrc文件的位置。
- 删除.npmrc文件，这个文件在C盘的用户目录下，比如 ``C:\Users\Administrator``。

### Npm清空缓存
```
npm cache clean -f
```

### Npm设置淘宝镜像源
由于npm官方的服务器在国外，在国内使用可能会遇到很多网络问题，而且速度也非常慢，为了方便我们的开发，我们需要手动切换npm到国内的镜像源。国内最稳定的镜像源是淘宝提供的。
1. 使用如下命令设置为淘宝的镜像源：
```
npm config set registry https://registry.npm.taobao.org
```
2. 使用如下命令检验是否成功：
```
npm config get registry
```

3. 如果想还原npm仓库地址，只需再把地址配置成npm镜像就可以了
```
npm config set registry https://registry.npmjs.org/
```

### 安装淘宝CNpm
还可以使用淘宝镜像提供的`cnpm`工具，通过`cnpm`来安装包一般速度会更快一些
1. 安装cnpm 输入以下命令
```
npm install -g cnpm --registry=https://registry.npm.taobao.org
```

2. 输入cnpm -v输入是否正常。
```
cnpm -v
```

### yarn包管理工具
yarn是由facebook推出的包管理客户端，它会缓存已经下载过的包并做了一些其他方面的优化，速度要比npm快，还添加了一些别的npm不具备的特性。
##### 安装yarn包管理工具
1. 进行全局安装:
```
npm  install -g yarn
```
2. 检查是否安装成功：
```
yarn -v
```
3. 查看 yarn 配置
```
yarn config get registry
```
或者
```
yarn config list
```

##### yarn 换源
换成淘宝的镜像源:
```
yarn config set registry https://registry.npm.taobao.org
```

##### yarn 常用命令
- yarn init // 同npm init，执行输入信息后，会生成package.json文件
- yarn config list // 显示所有配置项
- yarn config get <key> //显示某配置项
- yarn config delete <key> //删除某配置项
- yarn config set <key> <value> [-g|--global] //设置配置项
- yarn install //安装package.json里所有包，并将包及它的所有依赖项保存进yarn.lock
- yarn install --flat //安装一个包的单一版本
- yarn install --force //强制重新下载所有包
- yarn install --production //只安装dependencies里的包
- yarn install --no-lockfile //不读取或生成yarn.lock
- yarn install --pure-lockfile //不生成yarn.lock
- yarn add [package] // 在当前的项目中添加一个依赖包，会自动更新到package.json和yarn.lock文件中
- yarn add [package]@[version] // 安装指定版本，这里指的是主要版本，如果需要精确到小版本，使用-E参数
- yarn add [package]@[tag] // 安装某个tag（比如beta,next或者latest）
- yarn add --dev/-D // 加到 devDependencies
- yarn add --peer/-P // 加到 peerDependencies
- yarn add --optional/-O // 加到 optionalDependencies
- yarn add --exact/-E // 安装包的精确版本。例如yarn add foo@1.2.3会接受1.9.1版，但是yarn add foo@1.2.3 --exact只会接受1.2.3版
- yarn add --tilde/-T // 安装包的次要版本里的最新版。例如yarn add foo@1.2.3 --tilde会接受1.2.9，但不接受1.3.0
- yarn publish 发布包
- yarn remove <packageName>：移除一个包，会自动更新package.json和yarn.lock
- yarn upgrade 用于更新包到基于规范范围的最新版本
- yarn run 用来执行在 package.json 中 scripts 属性下定义的脚本
- yarn info <packageName> 可以用来查看某个模块的最新版本信息
- yarn cache list # 列出已缓存的每个包 yarn cache dir # 返回 全局缓存位置 yarn cache clean # 清除缓存

##### Yarn修改缓存位置修改
npm、yarn的cache都是磁盘占用大户，如果缓存在系统盘导致系统盘越来越小，可以考虑更改cache指定到其他盘。

查询yarn缓存目录
```
yarn cache dir
```
改变yarn缓存位置
```
yarn config set cache-folder "路径"
```
查询npm某个包的版本，例如yarn
```
npm ls yarn
```
查看 yarn 全局cache位置
```
yarn cache dir
```
修改缓存的位置
```
yarn config set cache-folder “D:\yarn\cache”
```

# Webpack打包
## Webpack简介
官网[https://webpack.docschina.org/](https://webpack.docschina.org/)。webpack是一个前端资源加载/打包工具。它将根据模块的依赖关系进行静态分析，然后将这些模块按照指定的规则生成对应的静态资源。如下图所示：
![](/images/26a141e60d1c55553eeb9805eb61ddf7.webp)

## 安装Webpack
首先确保本地环境支持Node.js，再使用npm安装webpack，如果觉得npm安装速度慢，可使用淘宝镜像及其命令cnpm

* 全局安装webpack命令行如下
* ```coffeescript
  npm install webpack -g
  ```
* 项目安装webpack命令行如下
* ```css
  npm install webpack --save-dev
  ```

## 使用Webpack进行打包
体验一下webpack是如何解析依赖关系并打包的，本地目录里新建两个子目录app（开发用目录）和release（发布用目录）。
1. app目录里新建一个Hello.js：
```
module.exports = function() {
    var showTxt = document.createElement('div');
    showTxt.textContent = "Hello webpack!";
    return showTxt;
};
```
2. app目录里新建一个main.js，并依赖Hello.js：
```
var showTxt = require('./Hello.js');
document.getElementById('root').appendChild(showTxt());
```
3. release目录里新建一个index.html：
```
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>WebpackTest</title>
</head>
<body>
<div id='root'>
</div>
<script src="bundle.js"></script>
</body>
</html>
```
该html的body里加载的bundle.js哪里来的？这就是接下来webpack需要做的。

4. 将app下开发者写的main.js和Hello.js打包生成bundle.js，并放进release目录。执行：
```
webpack ./app/main.js ./release/bundle.js
```

会发现release目录下多了个bundle.js。观察上述打包过程，webpack先解析main.js，发现它依赖Hello.js，于是将这两个文件打包进指定的release目录，生成bundle.js。用浏览器打开index.html会看到页面正确显示了Hello webpack!。

5. webpack提供了web服务器，先安装：
```
npm install --save-dev webpack-dev-server
```
6. 安装完后，执行：
```
webpack-dev-server
```
现在访问`http://localhost:8080`就能看到我们第一个webpack页面了。

# Node.js示例
使用Node.js搭建一个的本地静态文件服务器的方法:
### Node.js原生代码示例

server.js(不需要引入任何第三方依赖)

```javascript
var url = require("url"),
    fs = require("fs"),
    http = require("http"),
    path = require("path");
http.createServer(function (req, res) {
    var pathname = __dirname + url.parse("/public"+req.url).pathname;//资源指向public目录
    if (path.extname(pathname) == "") {
        pathname += "/";
    }
    if (pathname.charAt(pathname.length - 1) == "/") {
        pathname += "index.html";
    }
    fs.exists(pathname, function (exists) {
        if (exists) {
            switch(path.extname(pathname)){
                case ".html":
                    res.writeHead(200, {"Content-Type": "text/html"});
                    break;
                case ".js":
                    res.writeHead(200, {"Content-Type": "text/javascript"});
                    break;
                case ".css":
                    res.writeHead(200, {"Content-Type": "text/css"});
                    break;
                case ".gif":
                    res.writeHead(200, {"Content-Type": "image/gif"});
                    break;
                case ".jpg":
                    res.writeHead(200, {"Content-Type": "image/jpeg"});
                    break;
                case ".png":
                    res.writeHead(200, {"Content-Type": "image/png"});
                    break;
                default:
                    res.writeHead(200, {"Content-Type": "application/octet-stream"});
            }
            fs.readFile(pathname, function (err, data) {
                res.end(data);
            });
        } else {
            res.writeHead(404, {
                "Content-Type": "text/html"
            });
            res.end("<h1>404 Not Found</h1>");
        }
    });
}).listen(3003);
console.log("监听3003端口");
```

### 使用serve-static框架示例

第一步：在Node.js安装目录安装：

```
npm install connect
```

第二步：在Node.js安装目录安装：

```
npm install serve-static
```

第三步：新建server.js (可以放在项目里去运行也可以放在Node.js安装目录下运行)：

```
var connect = require("connect");
var serveStatic = require("serve-static");

var app = connect();
app.use(serveStatic("D:\项目文件夹"));

app.listen(5000);
```

第四步：

```
运行node server.js
```

### 使用express框架示例

1.下载express依赖

```
npm install express
```

2.新建server.js (可以放在项目里去运行也可以放在Node.js安装目录下运行)：

```
//server.js
var express = require('express');
var app = express();

app.use(express.static('public'));//express.static是express提供的内置的中间件用来设置静态文件路径

app.get('/index.htm', function (req, res) {
    res.sendFile(__dirname + "/" + "index.htm");
})

var server = app.listen(3000, function () {
    console.log("监听3000端口")
})
```

3.运行[node](https://so.csdn.net/so/search?q=node&spm=1001.2101.3001.7020) server.js

### 使用koa框架示例

1.安装koa koa-[static](https://so.csdn.net/so/search?q=static&spm=1001.2101.3001.7020)

```
npm install koa koa-static
```

注意：koa要求node的版本较高(node v7.6.0+)，如果出现如下错误，要升级node

```
koa-static@4.0.1@koa-static\index.js:39
return async function serve (ctx, next) {
             ^^^^^^^^
SyntaxError: Unexpected token function
```

2.server.js代码如下

```
const Koa = require('koa');
const app = new Koa();
const path = require('path');
const serve = require('koa-static');

const main = serve(path.join(__dirname+'/public'));
app.use(main);

app.listen(3001,function(){
    console.log("监听3001端口")
});
```

### 使用fastify框架示例

1.安装fastify serve-static

```javascript
npm install fastify serve-static
```

2.server.js代码如下

```javascript
const serveStatic = require('serve-static');
const fastify = require('fastify')();
const path = require('path');
 
fastify.use('/', serveStatic(path.resolve(__dirname, 'public')));
 
fastify.listen(3002, function () {
    console.log("监听3002端口");
})
```

# Deno介绍
Node.js 作者 Ryan Dahl 在 2020 年 5 月发布了 [deno](https://github.com/denoland/deno) 1.0 版本，Deno 是一个 JavaScript/TypeScript 的运行时，默认使用安全环境执行代码，有着卓越的开发体验。
Ryan 在 JS Conf Berlin 上总结了 Node.js 的 7 个设计失误:
1. 没有坚持使用 Promise，这个问题现在影响其实并不大了。
2. 安全问题：作者直说当时要是好好想想 Node.js 安全性可以更好，没有做太多说明。
3. 构建问题：开始 V8 用的 GPY 构建，Node.js 就跟着用了，没想到后来 V8 换成了 GN，结果只有 Node.js 用 GPY 了。
4. package.json：npm 变成了中心化的模块管理仓库，package.json 里面的信息太多了。
5. node_modules：比较冗余。
6. 允许不带 `.js` 拓展名 require('module') ，对模块加载器有写负担（需要分析 .js .json .node），和浏览器也不兼容。
7. 默认引用 `index.js` 有了 package.json 的 main 字段后这个设计没意义。

在  JS Conf Berlin 上 Ryan 也提了一下只有一个月大的 deno 设计目标，结合上 1.0 发布后 deno 主要差异化特性有:

1. 最大相同点是依然基于 V8。
2. 安全控制增强，网络/文件的读写权限需要额外声明。
3. 内置 TS 编译器，支持 webassembly。
4. 没有 npm、node_module、package.json。
5. 内置了很多常见工具：bundle、fmt、test、lint等。


# 参考资料
[七天学会NodeJS](http://nqdeng.github.io/7-days-nodejs/#1)