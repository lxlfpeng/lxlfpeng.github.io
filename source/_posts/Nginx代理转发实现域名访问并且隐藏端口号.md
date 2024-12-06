---
title: Nginx代理转发实现域名访问并且隐藏端口号
date: 2021-05-25
categories: 
  - 服务器
tags:
  - Nginx
---

1. docker 新建nginx 容器用于代理转发,这里必须要映射到80端口,因为访问宿主机会直接访问80端口
```
docker run -d --name nginx_agent -p 80:80 nginx:latest
```
1. 编辑nginx配置文件/etc/nginx/conf.d/default.conf
```

  server {
        listen       80;         #监听的端口
        server_name  qinglong.cn;    #监听的URL
        location / {
           proxy_redirect off;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_pass http://192.168.142.128:8060;
        }
    }
    server {
        listen       80;         #监听的端口
        server_name  baihu.cn;    #监听的URL
        location / {
           proxy_redirect off;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_pass http://192.168.142.128:8880;
        }
    }

```
3. docker重启nginx服务
```
docker restart nginx_agent
```
4. 修改域名对应ip关系
由于我这里是局域网配置的,因此可以通过修改Docker宿主机的host来实现,打开``vim /etc/hosts``添加
```
127.0.0.1        qinglong.cn
127.0.0.1        baihu.cn
```

5. 测试
此时在Docker宿主机请求qinglong.cn会自动转发到http://192.168.142.128:8060地址,访问 baihu.cn会自动转发到http://192.168.142.128:8880

6. 局域网内其他机器进行访问
有两种方式:一种是每一台机器都修改hosts文件指向docker宿主机,另外一种则是自建dns服务器,让局域网中所有的机器的dns都执行自建的dns服务器来实现。