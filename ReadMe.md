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

# 主题
[官方主题](https://hexo.io/themes/)：官方提供的各种主题.
### 安装主题的方式
1. 通过 Git 克隆主题
```
git clone https://github.com/hexojs/hexo-theme-landscape.git themes/landscape
```
2. 通过Git的submodule子模块的方式安装主题.

3. 通过npm进行安装``npm install hexo-theme-landscape``.

4. 手动下载主题到theme文件中.

>总结:推荐将自己喜欢的主题克隆到自己的github仓库,再通过Git的submodule子模块进行安装,这样既可以在原有的主题上可以进行修改,也可以在主题仓库升级的过程中进行升级.

### 更换主题
将项目根目录中创建一个以_config.开头的以主题名为结束的.yml,主题相关的配置都可以写到这个里面,然后在主配置文件_config.yml中指定主题即可.``theme: hexo-theme-landscape``

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

# Hexo添加评论功能
纯静态网站或博客，由于没有数据存储功能，经常借助第三方的评论系统以插件的方式集成进来，而又以 Github 的 Discussions和 Issues 功能实现的居多。

- giscus - 可借助组件库在 React、Vue 和 Svelte 中使用，支持多种语言
- gitalk - 基于 Github Issue 和 Preact 开发的评论插件
- utterances - 借助 Github issues 实现的轻量的评论组件，giscus 灵感就是来源于它


# 使用giscus给Hexo添加评论
giscus 是一个基于 GitHub Discussions 的评论插件。它的特点是简单易用，无需注册，支持多种主题，支持多语言，支持自定义配置。所有评论都存储在你的 GitHub Discussions 中，不会丢失，方便管理。

### 1.在Github上创建仓库
创建一个**公开**的仓库,如果也可以用部署githubPage的仓库.
### 2.打开仓库的Discussions功能

进入到 Github 项目的 Settings -> General -> Features -> Discussions 即可打开该功能。
### 3.安装giscus app
点击链接安装gisacus 在浏览器里面打开https://github.com/apps/giscus,选择Only select repositories仅选择需要的 repo 就可以了，不需要所有的 repo 都放开。选中对应的仓库.

### 4.生成giscus配置
首先，对你的仓库有一些前置要求：
- 必须是 公开的 GitHub 仓库
- 安装了 giscus app
- 在仓库中 启用 Discussions 功能
访问页面 https://giscus.app/zh-CN，在`配置`章节中设置相关的配置，可以获取到类似下面内容：


输入你的仓库，然后我们选择用 <title> 做映射，它会作为 discussion 的标题。

分类选择 announcements。
启用以下特性：

reaction
评论输入框在上方
懒加载

以上配置都搞好以后，会得到一段 script 代码。


### 5.将生成的giscus配置应用到hexo的主题中
https://hexo.fluid-dev.com/docs/guide/#%E8%AF%84%E8%AE%BA

# 参考资料    
[Hexo Fluid 用户手册](https://hexo.fluid-dev.com/docs/guide/)

[Hexo Butterfly 用户手册](https://butterfly.js.org/posts/21cfbf15/)

[Nunjucks Error: 解决方案](https://blog.csdn.net/weixin_45333934/article/details/108274320)

[Nunjucks Error: 解决方案2](https://huanglizhu.github.io/2020/05/21/hexo%20deploy%E4%B8%AD%E6%8A%A5%E9%94%99_Nunjucks%20Error/)