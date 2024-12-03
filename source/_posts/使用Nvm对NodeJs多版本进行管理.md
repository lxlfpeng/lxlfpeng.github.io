---
title: 使用Nvm对NodeJs多版本进行管理
date: 2021-02-19
categories: 
  - NodeJs
---

# 一.Nvm解决了什么问题
在我们使用NodeJs的过程中，时常会出现版本兼容问题，例如某工程A需要高版本的NodeJs环境，某工程B需要低版本的NodeJs环境，但是我们的计算机上面只能同时配置一个NodeJs版本，这样就出现了一个问题：我们需要根据不同的情况切换不同的NodeJs版本环境。之前笔者是使用git方式切换不同的nodeJs版本分支来实现的这种需求的，但是有没有更好的方式实现这一功能呢?当然有，这里就引出了一个Nodejs版本管理工具Nvm; [Nvm](https://github.com/nvm-sh/nvm)是 Node.js 的版本管理工具，可以创建不同版本 Node 的隔离环境，从而避免不同版本包之间的干扰。
# 二.下载安装Nvm
### 1.卸载之前安装的Nodejs
安装Nvm之前最好是将现有的全局 Node 进行卸载，否则可能会发生异常。
### 2.下载Nvm安装包
[github下载地址](https://github.com/coreybutler/nvm-windows/releases)
Windows系统下载第三个包：nvm-setup.zip，将下载下来的软件进行安装。
### 3.安装Nvm程序
在安装nvm时，点击 Next 时，会出现默认安装路径，选择nvm的本地安装目录时，注意，nvm的安装路径名称中最好不要有空格和中文，以免出现问题。
安装完成以后命令行输入:
```
nvm version
```
成功出现版本号那么安装nvm成功。

# 三.Nvm配置淘宝镜像
由于nvm默认的下载地址http://nodejs.org/dist/是外国外服务器，速度非常慢，因而可以切换到淘宝的镜像，下载速度会快很多。
```
官方地址：https://github.com/npm/cli/archive/

淘宝镜像：https://npm.taobao.org/mirrors/npm/
```
配置方法：打开nvm的安装路径，打开settings.txt，加入如下内容：
```
root: H:\nvm\nvm
path: H:\nodeJs
node_mirror: http://npm.taobao.org/mirrors/node/
npm_mirror: https://npm.taobao.org/mirrors/npm/
```
# 四.使用Nvm管理不同的NodeJs版本
### 1.Nvm安装指定的NodeJs版本
```
nvm  install NodeJsVersion
```
version就是要安装的nodejs版本，[官网版本](https://nodejs.org/en/download/releases/)。
比如：
```
nvm install v17.0.0
nvm install 17.0.0
```
等待一会儿，安装完成会显示:
```
Downloading node.js version 17.0.0 (64-bit)...
Extracting...
Complete

Installation complete. If you want to use this version, type

nvm use 17.0.0
```
打开nvm对应的目录也可以看到对应的NodeJs版本已经被下下来了。

### 2.Nvm切换NodeJs版本
```
nvm use NodeJsVersion
```
比如：nvm use 17.0.0，这样就NodeJs切换到了17.0.0的版本了。
切换成功以后查看NodeJs版本:
```
$ node -v
v17.0.0

$ npm -v
8.1.0
```
>如果nvm切换nodeJs没有成功并且输出乱码，此时切换cmd命令行为管理员权限，重新安装Nodejs即可。
### 3.npm设置镜像
设置淘宝镜像:
```
npm config set registry https://registry.npm.taobao.org
```
验证是否设置成功：
```
npm config get registry
```
# 五.Nvm常见命令
- nvm list或者nvm ls：查看当前安装的所有nodejs版本，nodejs版本前面有个*，代表当前使用的nodejs版本。
- nvm list installed：查看已经安装的版本。
- nvm list available：查看网络可以安装的版本。
- nvm install：安装最新版本nvm。
- nvm use version：切换使用指定的版本node。
- nvm current：显示当前使用的Nodejs版本。
- nvm alias name version：给对应的Nodejs版本号添加别名。
- nvm unalias name：删除已定义的Nodejs版本号别名。
- nvm on：打开nodejs控制。
- nvm off：关闭nodejs控制。
- nvm proxy 查看设置与代理。
  nvm node_mirror url：设置或者查看setting.txt中的node_mirror，如果不设置的默认是 https://nodejs.org/dist/。
  nvm npm_mirror  url：设置或者查看setting.txt中的npm_mirror，如果不设置的话默认的是： https://github.com/npm/npm/archive/。
- nvm uninstall version：卸载制定的NodeJs版本。
- nvm root：设置和查看nvm的路径。