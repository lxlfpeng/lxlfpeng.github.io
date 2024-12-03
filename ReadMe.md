# 使用步骤
### 安装hexo
```
npm install hexo-cli -g
npm install hexo-deployer-git --save
```
### hexo初始化
```
hexo init hexo-blog
cd hexo-blog
npm install
```
### 本地查看初始化hexo效果
```
hexo g
hexo server
```
### 完成初始化的项目目录如下：
```
.
├── _config.yml
├── package.json
├── scaffolds
|   └── post.md
├── source
|   └── _posts
└── themes

```
其中，常用配置文件如下

- _config.yml：是 hexo 的主要配置文件，网页的基本配置都在这里完成。
- package.json：记录项目安装的 npm 插件。
- scaffolds/post.md：新建文章时的文章模板。
- source/_posts：文章的默认创建与读取目录。
- themes：主题文件的默认安装目录。

### 文章发布
```
hexo new yourtitle
hexo server
```

### 更换主题
官方默认主题很丑，那我们别的不做，首先来替换一个好看点的主题。

[官方主题](https://hexo.io/themes/)：官方提供的各种主题


# Hexo 博客上传到 GitHub
1. 安装 Hexo Git 部署插件
   ```
   npm install hexo-deployer-git --save
   ```
2.  配置 _config.yml 文件
    ```
    deploy:
    type: git
    repo: https://github.com/你的用户名/你的仓库名.git
    branch: main   # 或 master，取决于你的仓库设置
    ``` 
3. 生成并部署博客
    ```
    hexo clean       # 清理缓存和旧文件
    hexo generate    # 生成静态文件
    hexo deploy      # 部署到 GitHub
    ```

# Hexo的文章多分类和子分类问题
### 没有[方括号]的情况
这种情况不能列多分类，只能列子分类:
```
categories:
    - 母分类
    - 子分类
    - 子子分类
    ......

```
例如，我想把文章放到 软件开发的前端的Vue.js分类里：
```
categories:
    - 软件开发
    - 前端
    - Vue.js
```
### 有[方括号]的情况
```
  categories:
    - [母分类1,子分类1,子子分类1,...]
    - [母分类1,子分类2,...]
    - [母分类2,子分类3,...]
```
例如，我写了一篇文章是关于后端的，包含php和SQL，并且我也想把它放到防踩坑分类里：
```
categories:
    - [后端,php]
    - [后端,SQL]
    - [防踩坑]
```

# Hexo 常用命令
- hexo new post 文章名称 # 新建文章
- hexo clean # 清除缓存
- hexo generate # 生成静态页面至 public 目录
- hexo server # 开启预览访问端口（默认端口 4000，’ctrl + c’关闭 server）
- hexo deploy # 部署到 GitHub
- hexo help # 查看帮助
- hexo version # 查看 Hexo 的版本

# 参考资料    
[Hexo Fluid 用户手册](https://hexo.fluid-dev.com/docs/guide/)

[Nunjucks Error: 解决方案](https://blog.csdn.net/weixin_45333934/article/details/108274320)

[Nunjucks Error: 解决方案2](https://huanglizhu.github.io/2020/05/21/hexo%20deploy%E4%B8%AD%E6%8A%A5%E9%94%99_Nunjucks%20Error/)