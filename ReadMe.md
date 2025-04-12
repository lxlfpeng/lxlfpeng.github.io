# 一.使用步骤
### 1.克隆仓库
- 克隆主仓库
    ```
    git clone git@github.com:lxlfpeng/lxlfpeng.github.io.git
    ```
- 克隆子仓库
    ```
    cd lxlfpeng.github.io
    #此命令会读取 .gitmodules 文件中的子模块信息并进行初始化。
    git submodule init 
    #该命令会根据初始化的配置，从远程仓库拉取子模块的内容到本地。
    git submodule update 
    ```

### 2.安装hexo
```
#全局安装 Hexo 命令行工具
npm install hexo-cli -g
#在 Hexo 项目中安装 hexo-deployer-git 插件，并且将该插件添加到项目的依赖列表里,使用 Hexo 搭建好博客之后，需要将生成的静态文件部署到 Git 仓库，就可以使用 hexo-deployer-git 插件
npm install hexo-deployer-git --save
```

### 3.安装依赖
```
#安装项目所有依赖
npm install
```

### 4.本地查看初始化hexo效果
```
#清除 Hexo 生成的缓存文件和静态文件
hexo clean
#将你编写的 Markdown 文章等源文件生成静态的 HTML 文件
hexo generate 
#在本地启动一个服务器，方便你预览 Hexo 博客
hexo server
```

### 5. 部署博客到github
若本地预览无误，你可以将生成的静态文件部署到远程服务器，如 GitHub Pages、GitLab Pages 等。前提是你已经安装了相应的部署插件（如 hexo - deployer - git），并且在 _config.yml 文件中完成了部署配置。
```
# 部署博客
hexo deploy
```
# 二.添加新的文章
### 1.确认文章格式
要保证你的 Markdown 文章具备正确的 YAML 头信息（Front - Matter），这部分信息会被 Hexo 用来解析文章的元数据，像标题、日期、标签、分类等。示例如下：
```
---
title: 编程算法基础总结
date: 2015-03-25
categories: 
  - 编程基础
tags: 
  - 编程基础
  - 算法
  - 数据结构
  - Java基础
---
```

### 2. 将文章放置到指定目录
Hexo 默认会从 source/_posts 目录读取文章。你只需把写好的 Markdown 文件复制到这个目录即可。

### 3. 生成静态文件
把文章复制到指定目录后，你要执行 hexo generate（可简写为 hexo g）命令，让 Hexo 把 Markdown 文件转换为静态的 HTML 文件。

### 4. 本地预览（可选）
你可以启动本地服务器，在浏览器中预览博客效果，确认文章是否正确显示。
```
# 启动本地服务器
hexo server
```
启动成功后，在浏览器里访问 http://localhost:4000 就能查看博客。

### 5. 图片和资源
如果文章里包含图片等资源，你可以把这些资源放到 source 目录下的合适位置，比如 source/images 目录，然后在 Markdown 文件中使用相对路径引用这些资源。
```
![图片描述](/images/my - image.jpg)
```

# 三.创建新项目
### 1. 安装 Node.js 和 npm
Hexo 是基于 Node.js 的，所以要先安装 Node.js 和 npm（Node.js 的包管理器）。你可以从 Node.js 官方网站 下载并安装适合你操作系统的版本。安装完成后，在命令行中输入以下命令，验证是否安装成功：
```bash
node -v
npm -v
```

### 2. 全局安装 Hexo CLI
安装好 Node.js 和 npm 之后，使用以下命令全局安装 Hexo 命令行工具（Hexo CLI）：
```bash
npm install hexo-cli -g
```
此命令会把 Hexo CLI 安装到系统全局环境中，这样你就能在任意目录下使用 hexo 命令。
### 3. 创建新的 Hexo 项目
使用 hexo init 命令创建新的 Hexo 项目。例如，要创建一个名为 my-blog 的项目，可以执行以下命令：
```bash
hexo init my-blog
```
该命令会在当前目录下创建一个名为 my-blog 的文件夹，并且在其中初始化 Hexo 项目的基本结构。
### 4. 安装项目依赖
项目初始化完成后，进入项目目录并安装所需的依赖：
```bash
cd my-blog
npm install
```
### 5. 创建文章
用 hexo new 命令创建新文章
```
hexo new "My First Article"
```
执行此命令后，Hexo 会在 `source/_posts` 目录下生成一个名为 `My First Article.md` 的文件，文件内容包含默认的 YAML 头信息，示例如下：


```markdown
---
title: My First Article
date: 2025-04-12 17:00:00
tags: 
categories: 
---
```
你可以在这个文件中编写文章的具体内容。
### 6. 启动本地服务器预览博客
安装完依赖后，你可以启动本地服务器，在浏览器中预览新创建的博客：
```bash
hexo server
```
启动成功后，在浏览器中访问 http://localhost:4000 ，就能看到初始的 Hexo 博客页面。
### 6. 停止本地服务器
若要停止本地服务器，在命令行中按下 Ctrl + C 组合键即可。

# 四.项目结构
当你使用 hexo init <项目名称> 命令创建一个新的 Hexo 项目后，会生成一个特定的项目结构:
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

### 项目根目录

项目根目录包含多个关键的配置文件和子目录，以下是主要的文件和目录：

* ​**`_config.yml`**​：这是 Hexo 的主配置文件，用于配置博客的各种设置，如博客标题、副标题、描述、URL、主题、部署等信息。例如，你可以在这里修改博客的标题和 URL：

```yaml
# 博客标题
title: My Hexo Blog
# 博客的基础 URL
url: https://example.com
```

* ​**`package.json`**​：该文件记录了项目的元数据以及项目依赖的 Node.js 包信息。当你需要安装或更新项目依赖时，`npm` 会根据这个文件来操作。例如：

```json
{
  "name": "hexo-site",
  "version": "0.0.0",
  "private": true,
  "scripts": {
    "build": "hexo generate",
    "clean": "hexo clean",
    "deploy": "hexo deploy",
    "server": "hexo server"
  },
  "hexo": {
    "version": ""
  },
  "dependencies": {
    "hexo": "^6.3.0",
    "hexo-cli": "^4.3.0",
    "hexo-deployer-git": "^4.0.0",
    "hexo-generator-archive": "^2.0.0",
    "hexo-generator-category": "^2.0.0",
    "hexo-generator-index": "^3.0.0",
    "hexo-generator-tag": "^2.0.0",
    "hexo-renderer-ejs": "^2.0.0",
    "hexo-renderer-marked": "^6.0.0",
    "hexo-renderer-stylus": "^2.1.0",
    "hexo-server": "^3.0.0"
  }
}
```

* ​**`scaffolds` 目录**​：存放文章模板文件。当你使用 `hexo new` 命令创建新文章时，Hexo 会根据这里的模板文件生成文章的初始内容。例如，`post.md` 是文章的默认模板，其内容可能如下：

```markdown
---
title: {{ title }}
date: {{ date }}
tags: 
categories: 
---
```

* ​**`source` 目录**​：这是存放博客源文件的主要目录，大部分内容的编辑工作都在这个目录下进行：
  * ​**`_posts` 目录**​：用于存放博客文章的 Markdown 文件。每篇文章对应一个 `.md` 文件，这些文件包含文章的标题、日期、标签、分类等元数据以及文章的具体内容。
  * ​**`_drafts` 目录（可选）**​：存放草稿文章。草稿文章不会被发布到博客上，除非你将其移动到 `_posts` 目录或者使用 `hexo publish` 命令将其发布。
  * ​**其他资源文件**​：可以在 `source` 目录下创建其他文件夹，用于存放图片、CSS、JavaScript 等静态资源。例如，你可以创建一个 `images` 文件夹来存放博客文章中使用的图片。
* ​**`themes` 目录**​：该目录用于存放 Hexo 主题。Hexo 支持多种主题，你可以从 [Hexo 主题官网](https://hexo.io/themes/) 下载喜欢的主题，并将其解压到这个目录下。每个主题对应一个子目录，你可以在 `_config.yml` 文件中指定要使用的主题。例如，使用 `landscape` 主题：

```yaml
theme: landscape
```

* ​**`public` 目录**​：当你执行 `hexo generate` 命令后，Hexo 会将 `source` 目录下的 Markdown 文件等源文件转换为静态的 HTML、CSS、JavaScript 文件，并将这些生成的静态文件存放在 `public` 目录中。这个目录的内容就是最终要部署到服务器上的内容。
* ​**`node_modules` 目录**​：存放项目依赖的 Node.js 包。当你执行 `npm install` 命令时，`npm` 会根据 `package.json` 文件下载并安装所需的包到这个目录。


# 五.选择主题
[官方主题](https://hexo.io/themes/)：官方提供的各种主题.
### 1.安装主题的方式
1. 通过 Git 克隆主题
```
git clone https://github.com/hexojs/hexo-theme-landscape.git themes/landscape
```
2. 通过Git的submodule子模块的方式安装主题.

3. 通过npm进行安装``npm install hexo-theme-landscape``.

4. 手动下载主题到theme文件中.

>总结:推荐将自己喜欢的主题克隆到自己的github仓库,再通过Git的submodule子模块进行安装,这样既可以在原有的主题上可以进行修改,也可以在主题仓库升级的过程中进行升级.

### 2.更换主题
将项目根目录中创建一个以_config.开头的以主题名为结束的.yml,主题相关的配置都可以写到这个里面,然后在主配置文件_config.yml中指定主题即可.``theme: hexo-theme-landscape``

# 六.Hexo博客上传到 GitHub
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

# 七.Hexo的文章多分类和子分类问题
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

# 八.Hexo 常用命令
- hexo new post 文章名称 # 新建文章
- hexo clean # 清除缓存
- hexo generate # 生成静态页面至 public 目录
- hexo server # 开启预览访问端口（默认端口 4000，’ctrl + c’关闭 server）
- hexo deploy # 部署到 GitHub
- hexo help # 查看帮助
- hexo version # 查看 Hexo 的版本

# 九.Hexo添加评论功能
纯静态网站或博客，由于没有数据存储功能，经常借助第三方的评论系统以插件的方式集成进来，而又以 Github 的 Discussions和 Issues 功能实现的居多。

- giscus - 可借助组件库在 React、Vue 和 Svelte 中使用，支持多种语言
- gitalk - 基于 Github Issue 和 Preact 开发的评论插件
- utterances - 借助 Github issues 实现的轻量的评论组件，giscus 灵感就是来源于它


## 使用giscus给Hexo添加评论
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