---
title: 如何做好CodeReview代码审查
date: 2021-06-09
categories: 
  - 代码审查
---

# 1 review的好处
代码review是代码质量保障的手段之一，同时开发成员之间代码review也是一种技术交流的方式，虽然会占用一些时间，但对团队而言，总体是个利大于弊的事情。如何借助现有工具在团队内部形成代码review的流程与规范，是team leader或技术管理者需要考虑的问题。
# 2 设置成员角色
首先需要对你团队的成员分配角色，在Gitlab groups里选择一个group，然后左边菜单栏点击 Members，可在 Members 页面添加或编辑成员角色.
![image.png](/images/311b5f053b421a4ba5b5e5dc1c5a6594.webp)
其中角色包含如下几类：

- Guest：权限最小，基本查看功能
- Reporter：只能查看，不能push
- Developer：能push，也能merge不受限制的分支
- Master：除了项目的迁移、删除等管理权限没有，其它权限基本都有
- Owner：权限最大，包括项目的迁移、删除等管理权限
详细权限参考： [gitlab](https://docs.gitlab.com/ee/user/permissions.html)

确定团队中技术水平、经验较好的成员为Master，负责代码的review与分支的合并；其他成员为Developer，提交合并请求，接受review意见；Master之间可以互相review。
# 3.配置代码分支保护
在项目页面左侧菜单栏 Settings -> Repository-> Beanches-> project settings-> Protected branches， 进入“Protected Branches”部分配置分支保护。
![image.png](/images/2184778afeace5cba94b8f2becbaf984.webp)
![image.png](/images/8d5cd6af67fee9a55c8713486ba8f61a.webp)
在这里可以针对每个分支，设置允许什么角色可以merge，允许什么角色可以push，选项包括三个：“Masters”， “Developers + Masters”， “No one”。这里设置成只允许master可以直接push与merge这几个常设分支的代码。
（如果更严格一点，可以将“Allowed to push”设置成“No one”）

# 4 代码review流程
### 4.1. 开发（开发者负责）
1. 本地切到develop分支， 拉取最新代码（相关命令如下，GUI工具操作自行查相关文档）
```
git branch #查看当前位于哪个分支，前面打星号即为当前分支
git checkout develop   #切换到develop分支
git pull  #拉取最新代码
```
2. 从develop分支切出子分支
```
git checkout -b feature-1101  #从当前分支切出子分支，命名为"feature-1101"
```
3. 编码、本地自测完之后，提交子分支到远程仓库
```
git add *  #加入暂存区
git commit -m "commit msg" #提交到本地仓库
git push origin feature-1101 #提交到远程仓库 
```
### 4.2 发起Merge请求（开发者负责）
1.  在项目主页面，依次点击左侧“Merge Requests”（下图1），“New merge request”（下图2），打开新建Merge请求页面3.2 发起Merge请求（开发者负责）
![image.png](/images/b504b8ad6e7beca6172847a633241f11.webp)
2. 在新建Merge请求页面，选择merge的源分支，及目标分支，如下图源分支为“feature-1101”，目标分支为“develop”，点击“Compare branches and continue”按钮进入对比与提交页面.
![image.png](/images/b5624d97eb2b6bfc18db8349ab640c5f.webp)
4. 添加好代码说明,点击添加create merge request按钮.
页面中选择Assignee，指定reviewer，指定人会受到邮件。下面的approvers以及Approvals required，是批准人和最少批准个数。
填写Approvals required后，必须经过指定个数以上的人批准才能合并。
![image.png](/images/864e319860ad4410ad5b0481034ee14d.webp)



### 4.3 代码Review（code reviewer负责
1. 负责代码Review的同事收到申请后，点击merge请求地址，打开页面，查看“Changes”。这里可通过“Inline”单边查看，也可以通过“Side-by-side”两个版本对比查看
![image.png](/images/d4d614aa7a748220006a3e4e97d1a012.webp)
2. review完成后，若无问题，则可点击”Merge”按钮完成merge，同时可删除对应的子分支“feature-1101”；若有问题，则可点击“Close merge request”按钮关闭该merge请求（也可以不关闭复用该merge请求），同时通知开发者进行相应调整，重新提交代码发起merge请求（如果之前没关闭merge请求，则刷新即可看到调整）。

收到邮件的reviewer通过merge request 页面可以看到代码修改记录，并增加commond，其他人也可以通过commond进行讨论，

无问题可以点击merge通过或者不通过则点击右下角的close merge request。


### 4.4 冲突解决（开发者负责）
1. merge的时候，可能存在代码冲突，这时，开发者可从develop分支重新拉取最新代码进行本地merge， 解决冲突后重新提交代码进行review
```
git pull origin develop #在当前子分支拉取develop分支的最新代码进行本地merge

# 解决冲突代码

# 提交
git add *
git commit -m "fix merge conflict"
git push origin feature-1101

```
自行解决不了时，寻求协助

遇到冲突怎么办
多个分支向一个分支合并代码等流程中，往往会形成版本冲突。此时，提交merge request后的页面如下：

[](https://upload-images.jianshu.io/upload_images/15616439-d20c289ec3f32caa.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)
冲突页面.png
我们发现，merge按钮置灰，同时出现了resolve conflicts以及merge locally的按钮。点击resolve conflicts。出现解决冲突的页面
[](https://upload-images.jianshu.io/upload_images/15616439-76f67e0ff8759946.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)
解决冲突.png
页面可以通过use ours指定使用当前分支（发起merge request的源分支）代码或者use theirs来指定使用目标分支代码。或者点击 edit inline直接通过编辑页面编辑（更通用）。
[](https://upload-images.jianshu.io/upload_images/15616439-53bb6bd18bed7a8c.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)
edit inline.png
ok，我们已经处理完冲突，点击下方submit按钮。
返回merge request页面，等待远端冲突解决完成后，merge按钮正常。
[](https://upload-images.jianshu.io/upload_images/15616439-545436b00f92f845.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)




[Gitlab Code Review流程使用向导](https://blog.csdn.net/my_chenjie/article/details/84959946)
[GitLab轻松创建一个Merge Request](https://zmcdbp.com/gitlab-merge-request-simple-use/)
[基于gitlab的code review](https://www.jianshu.com/p/5d764b52ea88)
