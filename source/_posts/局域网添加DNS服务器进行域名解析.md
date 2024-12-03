---
title: 局域网添加DNS服务器进行域名解析
---

# 一.背景
在家庭局域网中，假如有若干个设备连接在同一台路由其中。路由器便和下属设备形成了一个小型局域网。 可以在局域网中我们可以通过设备的 ip 地址互相访问。 但是管理内部的局域网的机器过多，ip地址也变得越来越多，不想浪费精力在对ip的记忆上，而且使用IP远程登录非常容易搞混，为了解决这种问题， 比较简单的有两种方式。第一种方式是通过修改hosts文件，来完成域名和ip的映射，这种只能对一台机器生效，而且例如手机之类的不容易修改hosts的设备也比较麻烦，不过有些新的路由器或者是软路由可以在路由器层面修改hosts来达到适配所有设备的能力。另外一种解决方法是搭建一个局域网的DNS服务器，使用不同的域名指向不同的机器ip。 使用自建DNS服务器的好处远不止这一个，还有很多其他的好处。例如当IP地址发生变化时，只需要更改DNS服务器的设置即可。

# 二.DNS简介
要搭建DNS服务器，首先需要了解一下什么是DNS。

### 什么是 DNS？
DNS 是将域转换为其服务器的数字 IP 地址的系统，例如将域名``www.web-server.com``转换成ip地址``127.0.0.1``。每当使用域名发出网络请求时，系统都会执行 DNS 查询以确定域名对应的服务器ip地址。

### 为什么要运行自己的 DNS服务器？
自建DNS服务器可以更好地控制网络。例如能够配置网络级域映射，`web-server`到`192.168.0.101`。将路由器配置为使用你自己搭建的 DNS服务器， 可以让任何连接到该路由器设备都能够通过``http://web-server``访问到`192.168.0.101`，自建DNS服务器可以对域名解析进行集中式的管理，而不是在每台设备上单独修改`/etc/hosts`， 自建DNS服务器将适用于你连接到网络的所有内容，包括无法通过其他方式自定义其路由堆栈的嵌入式硬件。自建 DNS 服务器还可以提高性能并提供额外的弹性层。在发生大规模 DNS 中断时可以为你与之交互的关键服务使用具有长期缓存的自定义服务器可以帮助你度过所选上游提供商的停机时间。

### DNS 与 Dnsmasq
Dnsmasq是一个轻量级的 DNS 服务器，大多数 Linux 发行版中都可以安装它。
自建Dnsmasq服务器流程如下所示：

1. 路由器接收来自你连接的设备之一的请求。路由器将配置为使用 Dnsmasq 主机作为其 DNS 服务器。
2. Dnsmasq 会检查它是否有定义的域名路由，例如`web-server`to `192.168.0.101`。如果请求是`http://web-server/example-page`，它将发送`192.168.0.101`回路由器。
3. 当 Dnsmasq 没有匹配的路由时，它会将 DNS 请求转发给 Google 的`8.8.8.8`，从而在公共互联网上启用解析。这确保你在使用自己的 DNS 时仍然可以访问更广泛的网络。

>你无需在客户端设备上进行任何配置更改。路由器后面的所有东西最终都会通过 Dnsmasq 进行 DNS 查询。但是，值得注意的是，所有流行的桌面和移动操作系统都支持设置 DNS 服务器，因此您可以将单个设备配置为使用 Dnsmasq，而无需在路由器级别启用它。

# 三.Dnsmasq搭建DNS服务器
## 1.Dnsmasq简介
[Dnsmasq](https://wiki.archlinux.org/title/Dnsmasq) 是一个小巧且方便地用于配置DNS和DHCP的工具，适用于小型网络，它提供了DNS功能和可选择的DHCP功能。它服务那些只在本地适用的域名，这些域名是不会在全球的DNS服务器中出现的。DHCP服务和DNS服务结合，并且允许DHCP分配的地址能在DNS中正常解析，而这些DHCP分配的地址和相关命令可以配置到每台主机中，也可以配置到一台核心设备中（比如路由器），DNSmasq支持静态和动态两种DHCP配置方式。

## 2.安装Dnsmasq

### Ubuntu安装dnsmasq
```
apt install dnsmasq -y
```

### Docker安装dnsmasq
1. 下载镜像
```
docker pull jpillora/dnsmasq
```
2. 运行镜像
```
docker run \
    --name dnsmasq \
    -d \
    -p 53:53/udp \
# web控制端
    -p 5380:8080 \
# 账号
    -e "HTTP_USER=foo" \
# 密码
    -e "HTTP_PASS=bar" \
    --restart always \
    jpillora/dnsmasq
```

### 3.Linux53端口被systemd-resolve占用的解决方法
在Linux系统中有些软件（如：Dnsmasq解锁Netflix中的Dns等服务）可能要用到53的端口，但有些系统提示已使用（required port 53 already in use ）。使用``lsof -i:53``查看53端口是否是是被systemd-resolved进程所占用了。

1. 先停用 systemd-resolved 服务:

```
systemctl stop systemd-resolved
```

2. 编辑 /etc/systemd/resolved.conf 文件:

```
vi /etc/systemd/resolved.conf
```

3. 修改配置如下:

```
[Resolve]
DNS=8.8.8.8  #取消注释，增加dns
#FallbackDNS=
#Domains=
#LLMNR=no
#MulticastDNS=no
#DNSSEC=no
#Cache=yes
DNSStubListener=no  #取消注释，把yes改为no
```

4. 最后运行下面命令即可:

```
ln -sf /run/systemd/resolve/resolv.conf /etc/resolv.conf
```

## 4.配置Dnsmasq
打开/etc/dnsmasq.conf 配置文件，添加需要映射的域名和ip地址:

```
...
#dnsmasq config, for a complete example, see:
#  http://oss.segetech.com/intra/srv/dnsmasq.conf
#dns解析日志
log-queries
#定义主机与IP映射
address=/www.qinglong.com/172.17.205.28
address=/www.baihu.com/172.17.205.32
...
```

## 5.路由器设置DNS服务器
通过上面的步骤 ，我们已经设置好一个 DNS 服务器。接下来，进入你的路由器管理界面，使用你的设置，把你路由器的 DNS 服务器指向刚才机器在局域网的静态 IP。 也可以配置你的PC电脑的 DNS 指向这个地址。 建议是，保留原始的 DNS 主机地址比如:

```
192.168.1.1

192.168.31.223
```

- 第一个是我的原始路由器的 DNS 地址

- 第二个是我设置的地址，这样子可以作为补充。

![](https://img-blog.csdnimg.cn/74283c8620c941a8ad53cc2e6ae49b0d.png)


> 如果你 dnsmasq 设置没有继承 路由器主机的 DNS 服务，可以设置第二个 DNS 服务器为路由器主机 ，这样可以保证原来的状态。

## 6.远程网页查看Dnsmasq信息
访问Dnsmasq安装主机的8080端口就可以进入管理界面:
```
http://127.0.0.1:8080/
```

