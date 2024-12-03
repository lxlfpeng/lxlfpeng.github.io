---
title: Git命令及GIt Flow工作流
---

# 一.Git简介
Git是目前世界上最先进的分布式版本控制系统。它就没有中央服务器的，每个人的电脑就是一个完整的版本库，这样，工作的时候就不需要联网了，因为版本都是在自己的电脑上。
完成开发以后再将各自的修改推送给对方，就可以互相看到对方的修改了(为了便于项目中的所有开发者分享代码，我们将代码存放远程 Git 仓库例如github)。与此对应的是SVN是集中式版本控制系统，
版本库是集中放在中央服务器的，而干活的时候，用的都是自己的电脑，所以首先要从中央服务器哪里得到最新的版本，然后干活，干完后，需要把自己做完的活推送到中央服务器。而且集中式版本控制系统是必须联网才能工作。

# 二.Git文件状态
- **Untracked**: 未跟踪, 此文件在文件夹中, 但并没有加入到git库, 不参与版本控制. 通过`git add` 状态变为`Staged`
- **Unmodify**: 文件已经入库, 未修改, 即版本库中的文件快照内容与文件夹中完全一致. 这种类型的文件有两种去处, 如果它被修改, 而变为`Modified`. 如果使用`git rm`移出版本库, 则成为`Untracked`文件
- **Modified**: 文件已修改, 仅仅是修改, 并没有进行其他的操作. 这个文件也有两个去处, 通过`git add`可进入暂存`staged`状态, 使用`git checkout` 则丢弃修改过, 返回到`unmodify`状态, 这个`git checkout`即从库中取出文件, 覆盖当前修改
- **Staged**: 暂存状态. 执行`git commit`则将修改同步到库中, 这时库中的文件和本地文件又变为一致, 文件为`Unmodify`状态. 执行`git reset HEAD filename`取消暂存, 文件状态为`Modified`
![](/images/343cb650fbda3c1cfa84ea20f54e5605.webp)


# 三.Git常见命令
### 1.设置相关
- ``git config --list``查看配置
- ``git config user.name``查看用户名
- ``git config user.email``查看邮箱
- ``git config --global user.name "nameVal"``配置全局用户名
- ``git config --global user.email "eamil@qq.com"``配置全局邮箱
- ``git config --global credential.helper store``全局缓存登录凭证
- ``git config user.name “xxxx” ``配置单个项目用户名(需进入到项目文件夹根目录里面)
- ``git config user.email "xxxx@xx.com" ``配置单个项目邮箱(需进入到项目文件夹根目录里面)
- ``git config –global credential.helper cache`` 设置记住密码（默认**15分钟**）
- ``git config credential.helper ‘cache –timeout=3600’``设置记住密码自定义过期时间（这里设置一个小时之后失效）
- ``git config –global credential.helper store``设置记住密码长期存储
- ``git config --global credential.helper wincred``清除缓存登录凭证
- ``git credential-manager uninstall``清除缓存在git中的用户名和密码
- ``git version``查看git软件的版本号。

### 2.创建
- ``git init``初始化
- ``git clone git@git... .git``克隆项目(git:// 协议)
- ``git clone http://... .git``克隆项目(http(s)://)
- ``git clone http://邮箱（或用户名）:密码@仓库地址``指定邮箱或者用户名克隆项目,如果用户名或者邮箱及密码中包含了@符号，所以需要把@转码一下代替:@-->%40
- ``git clone -b  要clone的分支名  仓库地址``克隆指定分支的项目.

### 3.添加到暂存区及提交
- ``git add readme.txt ``将文件提交到暂存区
- ``git add . ``把工作区域内的所有变化提交到暂存区，包括文件内容修改(modified)以及新文件(new)，但不包括被删除的文件。
- ``git add -u``仅监控已经被add的文件（即tracked file）将被修改的文件提交到暂存区。add -u 不会提交新文件（untracked file）。（git add --update的缩写）
- ``git add -A``是上面两个的合集,提交所有变化。（git add --all的缩写）
- ``git commit -m "first"``提交到版本库
- ``git status``状态查看(查看工作目录中的状态例如:有没有没被提交的文件之类的)
### 4.删除
- ``git rm 我的文件``在本地仓库删除文件
- ``git rm -r 我的文件夹/``在本地仓库删除文件夹 此处-r表示递归所有子目录，如果你要删除的，是空的文件夹，此处可以不用带上-r。
>删除的文件可以通过 git reset head file 和git checkout file恢复.
### 5.branch(分支)
- ``git branch [branch-name]``新建一个分支，但依然停留在当前分支
- ``git checkout -b [branch-name]``新建一个分支，并切换到该分支
- ``git branch``    列出所有的分支(所有本地分支)
- ``git branch -r`` 列出所有的分支(所有远程分支)
- ``git branch -a`` 列出所有的分支(所有本地和远程分支)
- ``git checkout [branchname]``切换到指定分支，并更新工作区
- ``git branch -d [branchname]``删除本地分支
- ``git push origin --delete [branchName]``删除远程分支
- ``git branch -m [oldname] [newName]``分支重命名
- ``git reflog --date=local | grep nikeglass``查看当前分支的父分支
- ``git merge [branchname]``  将branchname分支上的修改合并到当前分支上
- ``git rebase [branchname]`` 对当前分支基于branchname进行变基操作

### 6.远程分支.
- ``git checkout -b [分支名] [远程名]/[分支名]`` 在本地建立分支并和远程分支同步
- ``git remote add origin [远程git地址]本地项目关联远程仓库(origin 是默认的远程版本库名称,添加多个不同的远端需要不同的标识)``
- ``git remote``列出所有关联的远端仓库.
- ``git remote update origin --prune``更新远程分支列表
- ``git remote -v``列出所有关联的远端仓库(详细信息).
- ``git remote rm origin:origin(远程关联仓库的别称)``删除关联的远程仓库。
- ``fetch+merge`` 拉取远程仓库与本地仓库进行合并(git fetch 相当于是从远程获取最新到本地，不会自动merge)
  ```
  git fetch origin master //将远程仓库的master分支下载到本地当前branch中
  git log -p master...origin/master //比较本地的master分支和origin/master分支的差别
  git merge origin/master //进行合并
  ```
- ``git pull origin master``相当于是从远程获取最新版本并merge到本地。
- ``git push <远程主机名> <本地分支名>:<远程分支名>``推送到远程仓库.如果当前分支只有一个追踪分支，那么主机名和后面都都可以省略:``git push``。
如果当前分支与多个主机存在追踪关系，那么这个时候-u选项会指定一个默认主机，这样后面就可以不加任何参数使用git push:``git push -u origin(远程主机名) master:master(本地分支名:远程分支名)``。

- ``git pull origin master --allow-unrelated-histories``分支进行强行合并


>git fetch和git pull 区别: fetch 和 pull 的不同: fetch 相当于是从远程获取最新版本到本地，不会自动merge，所以本地仓库的代码还未被更新，
然后比较本地分支和远程分支的差别,最后通过 git merge origin/master 来合并这两个版本，可以把它理解为合并分支一样的。 
pull 相当于是从远程获取最新版本并merge到本地(相当于git fetch 和 git merge)。如果想要更加可控一点的话推荐使用fetch + merge,因为
git fetch更安全一些,在merge前，我们可以查看更新情况，然后再决定是否合并

### 7.标签
- ``git tag`` 列出所有tag
- ``git show [tag]``查看tag信息
- ``git tag [tagname]``打轻量标签
- ``git tag -a [tagname] -m [message]``打标签并附注标签(例如，打v1.0标签``git tag -a v1.0 -m 'v1.0 release'``)
- ``git tag -a [tagname] [commit_id]``对过去的提交打标签
- ``git tag -d [tagname]``删除本地tag
- ``git push origin --delete tag <tagname>``删除远程tag
- ``git push [remote] [tag]``提交指定tag(例如，将v1.0标签推送到远程服务器上``git push origin v1.0``)
- `` git push [remote] --tags``提交所有tag
- ``git checkout [tagname]``切换到对应标签状态(这时候 git 可能会提示你当前处于一个“detached HEAD" 状态。 因为 tag 相当于是一个快照，是不能更改它的代码的。如果要在 tag 代码的基础上做修改，你需要一个分支：``git checkout -b [branchname] [tagname]``)

### 8.日志
- ``git log``每一次操作记录
- ``git reflog``可以查看所有分支的所有操作记录（包括（包括commit和reset的操作），包括已经被删除的commit记录，git log则不能察看已经删除了的commit记录，而且跟进结果可以回退到某一个修改。
- ``git log --oneline --graph`` 查看历史中什么时候出现了分支、合并
- ``git diff``比较工作区和暂存区的所有文件差异变化
- ``git diff <file name>``比较工作区和暂存区的指定文件的差异
- ``git diff --stat``比较工作区和暂存区的所有文件变化列表
- ``git shortlog -n-`` 按每位作者的提交次数排序分组输出。
- ``git show commit_id``查看某个提交的详细


### 8.撤销修改版本回溯

- ``git checkout -- file``丢弃工作区内文件的修改(例如:git checkout -- readme.md)
- ``git checkout .  ``放弃对工作区内所有的文件修改
>命令`git checkout -- readme.txt`意思就是，把`readme.txt`文件在工作区的修改全部撤销，这里有两种情况：一种是`readme.txt`自修改后还没有被add到暂存区，现在，撤销修改就回到和之前版本库一模一样的状态；
一种是`readme.txt`已经添加add到暂存区后，又作了修改，现在，撤销修改就回到添加到暂存区后的状态。总之，就是让这个文件回到最近一次`git commit`或`git add`时的状态。

- ``git reset HEAD <file>``撤销已经add到暂存区的文件.
- ``git reset HEAD .``撤销所有的已经add到暂存区的文件.
>如果文件已经被add到暂存区,再使用git checkout是没有用的.此时应该使用git reset HEAD将文件撤销添加到暂存区的操作,然后再使用git checkout操作让文件恢复到最近一次commit.

- ``git reset --hard HEAD^``        回退到上个版本
- ``git reset --hard commit_id``    退到/进到 指定commit_id

####  撤销修改分为三种情况
**情况一:未使用 git add 缓存代码时:**
放弃单个文件修改``git checkout -- filepathname``,注意不要忘记中间的"--",不写就成了检出分支了! 放弃所有的文件修改``git checkout .  ``

**情况二:已经使用了  git add 缓存了代码:**
可以使用 ``git reset HEAD filepathname`` （比如： ``git reset HEAD readme.md``）来放弃指定文件的缓存，放弃所有的缓存可以使用 ``git reset HEAD .``**`` 命令。此命令用来清除 git对于文件修改的缓存。相当于撤销 git add 命令所在的工作。

**情况三:已经用 git commit  提交了代码:**
可以使用 ``git reset --hard HEAD^ ``来回退到上一次commit的状态。此命令可以用来回退到任意版本：``git reset --hard  commitid ``

# 三.Git忽略
### 1.使用.gitignore文件
在git中如果想忽略掉某个文件，不让这个文件提交到版本库中，可以使用修改根目录中 .gitignore 文件的方法（如无，则需自己手工建立此文件）。

##### 创建.gitignore
``touch .gitignore``打开 Git Bash->导航到 Git 仓库的位置->为仓库创建.gitignore文件

##### .gitignore匹配规则
```
  # 此为注释 – 将被 Git 忽略
  *.a   # 忽略所有 .a 结尾的文件
  !lib.a# 但 lib.a 除外
  /TODO # 仅仅忽略项目根目录下的 TODO 文件，不包括 subdir/TODO
  build/# 忽略 build/ 目录下的所有文件
  doc/*.txt # 会忽略 doc/notes.txt 但不包括 doc/server/arch.txt 
```

##### .gitignore不生效问题
把某些目录或文件加入忽略规则，按照上述方法定义后发现并未生效，原因是**.gitignore只能忽略那些原来没有被追踪的文件**，如果某些文件已经被纳入了版本管理中，仅修改.gitignore是无效的。
所以如果需要忽略的文件已经提交到本地仓库，则需要从本地仓库中删除掉该文件，如果已经提交到远端仓库，则需要从远端仓库中删除该文件，.gitignore文件才能实际生效。
解决方法就是先把本地缓存删除（改变成未被追踪状态），然后再提交(push)，这样就不会出现忽略的文件了。`git`清除本地缓存命令如下：
```
  git rm -r --cached .              去掉已经托管的所有文件
  git add .                         添加文件 
  git commit -m '本地提交的comment'   提交
```

### 2.忽略本地修改
- 本地开发中需要用的文件，不能提交到远程，但是还不能写入.gitignore文件。
- 远程仓库里已存在的文件,在本地进行修改了.但是不想提交到远程仓库里面去(例如一些编辑器的配置文件,不同版本的编辑器配置文件可能不同.但是初始化仓库时没有做好.gitignore的配置导致配置文件被添加到版本库里面了
此时,要么在.gitignore里面添加忽略规则再把缓存修改)。

``git update-index --assume-unchanged /XX/XX/XXX.file`` 本地忽略单个文件

``git ls-files -z | xargs -0 git update-index --assume-unchanged``进入文件夹中(忽略文件夹中所有的文件)

``git ls-files -v | grep '^h\ '``找出所有被忽略的文件

``git ls-files -v | grep '^h\ ' | awk '{print $2}'``找出所有被忽略的文件路径

``git update-index –no-assume-unchanged –path /XX/XX/XXX.file`` 取消单个忽略文件

``git ls-files -v | grep '^h' | awk '{print $2}' |xargs git update-index --no-assume-unchanged``取消所有被忽略的文件

> 注意: 这种方式也有一个副作用，如果本地被忽略的该文件在本地被修改了，远程的该文件也被其他人修改了。那在拉取远程分支时，由于本地和远程文件存在不一致的更新，会导致拉取不成功的问题。此时应该先取消文件忽略，再进行拉取操作。


# 四.Git分支合并
### merge两种模式
merge一般有两种模式:
- Fast forward模式
通常，合并分支时，如果没有分歧解决，就会直接移动文件指针，这就是Fast forward模式，也是merge默认的模式。
>举例来说，开发一直在master分支进行，但忽然有一个新的想法，于是新建了一个dev的分支，并在其上进行一系列提交，完成时，回到master分支，
此时，master分支在创建dev分支之后并未产生任何新的commit。master分支合并dev分支并不会产生新的commit. 以后当合并分支被删除时，也就不知道对应的提交是来自于哪个分支。
此时的合并就叫fast forward。如果想在这样的的情况下也自动生成一个commit，记录此次合并就可以用：git merge --no-ff模式。

- --no-ff模式
``git merge --no-ff -m "merge with no-ff" dev``因为本次合并要创建一个新的commit，所以加上-m参数，把commit描述写入。
![](/images/ae00297981cd55708f131ccb73a8df56.webp)


总结：fast forward能够保证不会强制覆盖别人的代码，确保了多人协同开发。尽量不要使用non fast forward方法提交代码。


### merge冲突问题
git冲突的场景:
- 情景一：多个分支代码合并到一个分支时；
- 情景二：多个分支向同一个远端分支推送代码时；
实际上，push操作即是将本地代码merge到远端库分支上。push和pull其实就分别是用本地分支合并到远程分支 和 将远程分支合并到本地分支 所以这两个过程中也可能存在冲突。

git的合并中产生冲突的具体情况：
1. 两个分支中修改了同一个文件（不管什么地方）
2. 两个分支中修改了同一个文件的名称
两个分支中分别修改了不同文件中的部分，不会产生冲突，可以直接将两部分合并。

### merge解决冲突
1. 先本地直接提交代码：git push origin master
2. 如果别人在自己之前提交了修改，git会提示push失败，需要先pull远程代码：git pull origin/master
3. （拉取远程仓库进行自动合并） 如果能自动合并，git会提示auto merge成功，这时可以直接git push origin master如果不能自动merge，git会提示auto merge失败，
4. 需要手动解决冲突：git status  查看冲突情况修改冲突git status  查看冲突解决情况git add .git commit -m '解决冲突的注释说明'git push origin master



### 避免产生冲突
现代软件开发项目中，代码冲突是不可避免的，但我们应该尽量减少冲突的产生，避免不必要的冲突。下面列举一下实践经验：
1. 工作在不同的分支上，并经常性的同步主代码，如果由于项目要求，比如长期开发一个功能使得该功能代码在开发完成之前合并到主分支，此时我们虽然没有办法经常合并代码到主分支，也至少需要经常性的同步主分支代码到开发分支上
，避免在最终合并到主分支上时产生过多冲突。
2. 尽量使用短生命周期分支而非长期分支。
3. 除了技术层面的手段，也可以通过项目管理上的手段来尽量避免，例如：不要同时将相同组件开发的不同任务分给不同的开发者，否则在合并代码时该组件将会产生过多的冲突。
各组件开发小组之间经常性的沟通，互相了解各自的开发状态，在可能产生冲突的时候及时采取手段。

### merge和rebase(变基)
merge 会把公共分支和你当前的commit 合并在一起，形成一个新的 commit 提交:
![](/images/5fd18eb90e17cebe03a2d2cda15f759a.webp)


rebase会把你当前分支的 commit 放到公共分支的最后面,所以叫变基。就好像你从公共分支又重新拉出来这个分支一样。
举例:如果你从 master 拉了个feature分支出来,然后你提交了几个 commit,这个时候刚好有人把他开发的东西合并到 master 了,
这个时候 master 就比你拉分支的时候多了几个 commit,如果这个时候你 rebase master 的话，就会把你当前的几个 commit，放到那个人 commit 的后面。此时切换到master分支再用merge进行合并即可.

**优点**
- rebase最大的好处是你的项目历史会非常整洁
- rebase 导致最后的项目历史呈现出完美的线性——你可以从项目终点到起点浏览而不需要任何的 fork。这让你更容易使用 git log、git bisect 和 gitk 来查看项目历史
**缺点**
- 安全性，如果你违反了 rebase 黄金法则，重写项目历史可能会给你的协作工作流带来灾难性的影响
- 可跟踪性，rebase 不会有合并提交中附带的信息——你看不到 feature 分支中并入了上游的哪些更改
![](/images/5dbacaeed9971409e0e1cf89bbdea58c.webp)


1. 可以看出merge结果能够体现出时间线，但是rebase会打乱时间线。
2. 而rebase看起来简洁，但是merge看起来不太简洁。
3. 最终结果是都把代码合起来了，所以具体怎么使用这两个命令看项目需要。

注意:
1. 不要在公共分支使用rebase
2. 本地和远端对应同一条分支,优先使用rebase,而不是merge

# 五.Git暂存与恢复
### git stash命令作用
1. 当正在dev分支上开发某个项目，这时项目中出现一个bug，需要紧急修复，但是正在开发的内容只是完成一半，还不想提交，这时可以用git stash命令将修改的内容保存至堆栈区，
然后顺利切换到hotfix分支进行bug修复，修复完成后，再次切回到dev分支，从堆栈中恢复刚刚保存的内容。
2. 由于疏忽，本应该在dev分支开发的内容，却在master上进行了开发，需要重新切回到dev分支上进行开发，可以用git stash将内容保存至堆栈中，切回到dev分支后，再次恢复内容即可。

>git stash命令的作用就是将目前还不想提交的但是已经修改的内容进行保存至堆栈中，后续可以在某个分支上恢复出堆栈中的内容。这也就是说，stash中的内容不仅仅可以恢复到原先开发的分支，也可以恢复到其他任意指定的分支上。  
git stash作用的范围包括工作区和暂存区中的内容，也就是说没有提交的内容都会保存至堆栈中。

- ``git stash``能够将所有未提交的修改（工作区和暂存区）保存至堆栈中，用于后续恢复当前工作目录。
- ``git stash save "notes"``作用等同于git stash，区别是可以加一些注释
- ``git stash list ``查看当前stash中的内容
- ``git stash pop id``将当前stash中的内容弹出，并应用到当前分支对应的工作目录上,id是可选项，默认时上一次暂存,通过git stash list可查看具体值。只能恢复一次.
- ``git stash apply id``将堆栈中的内容应用到当前目录，不同于git stash pop，该命令不会将内容从堆栈中删除，可以恢复多次.也就说该命令能够将堆栈的内容多次应用到工作目录中，适应于多个分支的情况。
- ``git stash drop stash id`` 删除某个保存，id是可选项，通过git stash list可查看具体值
- ``git stash clear`` 删除所有保存的快照

# 六.Git去除大文件
1. 首先找出git中前五大的文件：
    ```
    git verify-pack -v .git/objects/pack/pack-*.idx | sort -k 3 -g | tail -5
    ```
   或者:
   ```
   git rev-list --objects --all | grep "$(git verify-pack -v .git/objects/pack/*.idx | sort -k 3 -n | tail -5 | awk '{print$1}')"
   ```
   或者:
   ```
   git rev-list --all | xargs -rL1 git ls-tree -r --long | sort -uk3 | sort -rnk4 | head -10
   ```
2. 用第一步文件的id找出文件名：
    ```
    git rev-list --objects --all | grep fileId 
    ```
3. 删除文件提交记录
    ```
    git filter-branch --index-filter 'git rm --cached --ignore-unmatch <your-file-name>'
    rm -rf .git/refs/original/
    git reflog expire --expire=now --all
    git fsck --full --unreachable
    git repack -A -d
    git gc --aggressive --prune=now
    git push --force 
    ```
# 七. Git Flow(版本管理工作流)
Git 作为一个源码管理系统，不可避免涉及到多人协作。为了避免协作过程中产生混乱，必须有一个规范的工作流程，让大家有效地合作，使得项目井井有条地发展下去。
Gitflow是基于Git的强大分支能力所构建的一套***软件开发工作流***，这些流程应被视作为指导方针，而非“铁律”。Gitflow使用``多个分支来记录项目开发的历史，而不是使用单一的master分支``。
![](/images/401d6d180524cc88c189d8e565b7021d.webp)

## 1. 主要分支

主要分支包括``Master``和``Develop(Dev)``，前者用于正式发布，后者用于日常开发。常设分支只需要这两条就够了，不需要其他的了。

**Master分支（主）:**
Git主分支的名字，默认叫做Master。该分支上的代码随时可以部署到生产环境， 这个分支只能从其他分支合并，并且不能在这个分支做任何直接修改。
每次版本封版后由主程序员合并`release`分支代码进来，发布完成以后打上tag，开发人员不可以随意操作。

**develop分支（开发）：**
用来开发的分支，通常可以直接在其上进行开发，在每次发布版本``（release）``和线上紧急``bug（hotfix）修复后``，需要同步到其上。理论上此版本只在开发阶段使用，提测时不可以直接修改，
而在测试结束后由`release`分支合并到其上。如果想正式对外发布，就在Master分支上，对Develop分支进行"合并"（merge）。

## 2. 临时性分支

除了常设分支以外，还有一些临时性分支，用于应对一些特定目的的版本开发。临时性分支主要有三种：``功能分支 （feature），预发布分支 (release)，修补bug分支 (fixbug)``，这三种分支都属于临时性需要，
使用完以后，应该删除，使得代码库的常设分支始终只有Master和Develop。

**release分支（预发布）：**
在发布正式版本之前（即develop合并到Master分支之前），我们可能需要有一个预发布的版本进行测试。预发布分支是从Develop分支上面分出来的，所有测试阶段的bug全部在此分支修复，测试结束后，必须合并进Develop和Master分支。
它的命名，可以采用release-xx的形式。

**feature分支（功能）：**
为了开发某种特定功能，从Develop分支上面分出来的。开发完成后，要再并入Develop。功能分支的名字，可以采用feature-XX的形式命名。如果在团队开发时，有一个功能的开发周期要长过本次版本开发周期，
建议开启一个 `feature` 进行单独开发，当需要此功能的时候，只需要将 `feature` 合并入 `develop` 分支，下次一并提测即可。
这样设计可以避免这个功能在尚未开发完成或者通过测试的时候混入发布的版本，而导致不可预知的不稳定。当然也可以同时开启多个 `feature` 分支进行不同新功能开发，在合适的时候合并提测即可。

**hotfix分支（bug修复）：**
软件正式发布以后，难免会出现bug。这时就需要创建一个分支，进行bug修补。修补bug分支是从Master分支上面分出来的。修补结束以后，再合并进Master和Develop分支。它的命名，可以采用fixbug-XX的形式。
线上bug修复的热补丁分支，应由 `master` 拉出，并在修复完成后合并入 `master` 和 `develop` 保证两分支的bug已修复。

### 3. 新功能开发中，各角色的工作流程

##### (1.)前置阶段(新功能启动)

- 开发主管->基于**master**主干创建一个**develop**分支。

**现有主干分支: master、develop**
##### (2.)开发阶段(开始开发)

- 功能开发人员->基于**develop**分支创建一个**feature_XX**分支。
- 功能开发人员->在**feature_XX**分支上开发新功能。
- 功能开发人员->新功能开发完成以后，在git上发起**Pull request**把代码合并到到**develop**分支上。
- 开发主管->确认代码没问题，通过该合并请求。

**现有主干分支: master、develop、feature_XX**

##### (3.)测试阶段(开发完毕)

- 开发主管->基于**develop**分支创建一个分支名为**release-1.0.0**的预发布版本。
- 测试人员->对**release-1.0.0**分支的代码进行测试，测试通过在git发起**Pull request**把**release-1.0.0**代码合并到到**master**分支上。

**现有主干分支: master、develop、feature_XX、release-1.0.0**

##### (4.)发布阶段(测试通过)

- 开发主管->基于**master**分支创建一个里程碑版本(tag)名为**1.0.0-Release**。
- 删除完成使命的其他分支:**feature_login**、**release-1.0.0**。

**现有主干分支: master、develop、1.0.0-Release(tag)**

### 4.线上代码出现bug时，各角色的工作流程

##### (1.)前置阶段(提交bug)

- 测试人员->发现问题，基于**1.0.0-Release**里程碑版本在git上新建一个issue。

**现有主干分支: master、develop、1.0.0-Release(tag)**

##### (2.)修复阶段(开始修复bug)

- 功能开发人员->基于**1.0.0-Release**tag创建一个**hotfix_XX**(该issue序号)分支，开发人员在**hotfix_XX**分支上修复bug，修复完成后，在git上发起**Pull request**把代码合并到到**master**主干上。
- 开发主管->确认代码没问题，通过该合并请求。

**现有主干分支: master、develop、1.0.0-Release(tag)、hotfix_0001**

##### (3.)测试阶段(bug修复完毕)

- 测试人员->对**master**分支的代码进行测试。

**现有主干分支: master、develop、1.0.0-Release(tag)、hotfix_0001**

##### (4.)发布阶段(测试通过)

开发主管->基于**master**分支创建一个里程碑修复版本(tag)名为**1.0.1-Release，**删除完成使命的其他分支:**hotfix_XX**。

**现有主干分支: master、develop、1.0.0-Release(tag)、1.0.1-Release(tag)**

# 八.常见问题.

1. 第一次输入错误的gitlab用户名和密码，第二次clone不弹框提示输入用户名和密码的解决方案。
```
git clone remote: HTTP Basic: Access denied
```
![](/images/c965c4b3eb916df6443519b9e0c48b19.webp)

### **方式一:在控制面板里面将凭证删除.**
![](/images/cea03591b71baa3b9c26ae2eb30bb0b9.webp)

![](/images/02df0dc3c6cf7e8cfaba30d394e89785.webp)

**方式二:使用git命令重置凭证.**

```
git config --system --unset credential.helper
git config --global credential.helper store
```


# Git子模块

1.1使用场景
某个工作中的项目需要包含并使用另一个项目。 也许是第三方库，或者你独立开发的，用于多个父项目的库。想要把它们当做两个独立的项目，同时又想在一个项目中使用另一个。

1.2 基本关系
首先明确，父项目和子项目没有实际关系，他们就是各自完全独立的两个git仓库而已。只是父项目中需要用到子项目。所以父项目和子项目的管理是分开进行的，即他们的代码拉取和提交都要分别进行。

默认情况下，父模块会将子项目放到一个与子仓库同名的目录中，可以在父项目中查看和修改子项目文件。每次更新子项目代码，子项目就会产生一个新的版本号。父项目中会记录所用子项目的版本号，如果子项目更新了版本号，而父项目不重新获取新版本的子项目，父项目就还是使用的旧版本的子项目代码。


### 子模块的添加
添加子模块非常简单，命令如下：
```
git submodule add <url> <path>
```
其中，url为子模块的路径，path为该子模块存储的目录路径。

执行成功后，git status会看到项目中修改了.gitmodules，并增加了一个新文件（为刚刚添加的路径）

git diff --cached查看修改内容可以看到增加了子模块，并且新文件下为子模块的提交hash摘要

git commit提交即完成子模块的添加

### 子模块的使用
克隆项目后，默认子模块目录下无任何内容。需要在项目根目录执行如下命令完成子模块的下载：
```
git submodule init
git submodule update
```
或：
```
git submodule update --init --recursive
```


执行后，子模块目录下就有了源码，再执行相应的makefile即可。

### 在父项目中修改并提交子项目代码
子项目中有三种状态，一是以版本编号命名的游离态，二是主分支master，三是自己创建的分支。一般是在自己的分支进行修改。

//先cd到子项目的目录下，然后右键git bash here，执行以下语句：
```
git checkout <分支名>
git add .
git commit -m "说明信息"
git push origin <远程分支名>

```
可以看到，其操作流程是和普通项目的提交一样的。


### 子模块的更新
```
git clone <repository> --recursive 递归的方式克隆整个项目
```


子模块的维护者提交了更新后，使用子模块的项目必须手动更新才能包含最新的提交。
在项目中，进入到子模块目录下，执行 git pull更新，查看git log查看相应提交。
完成后返回到项目目录，可以看到子模块有待提交的更新，使用git add，提交即可。

在父项目中执行以下命令：
```
git submodule update --init  //初始化版本
git submodule update --remote  //更新到最新版本

```



### 删除子模块
有时子模块的项目维护地址发生了变化，或者需要替换子模块，就需要删除原有的子模块。

删除子模块较复杂，步骤如下：

rm -rf 子模块目录 删除子模块目录及源码
vi .gitmodules 删除项目目录下.gitmodules文件中子模块相关条目
vi .git/config 删除配置项中子模块相关条目
rm .git/module/* 删除模块下的子模块目录，每个子模块对应一个目录，注意只删除对应的子模块目录即可
执行完成后，再执行添加子模块命令即可，如果仍然报错，执行如下：

git rm --cached 子模块名称

完成删除后，提交到仓库即可。


### 在父项目中提交子项目版本
```
git submodule update --init
git submodule update --remote
git add 子项目所在文件夹
git commit -m "说明信息"
git push
```
这部分操作是为了提交父项目中子项目的版本号

### Git本地修改子模块URL
初始化模块
如果已经初始化过了，也不要慌。可以使用 git submodule deinit [moduleName] 来取消对某一个模块的初始化，或者使用 git submodule deinit --all 取消对所有模块的初始化

```git submodule init```
修改模块的 URL
修改名为 hello 子模块的 url 为 ssh://baidu@baidu.com: git config submodule.hello.url ssh://baidu@baidu.com
当然在初始化子模块以后，也可以通过直接修改 .git/config 文件来修改 url，但是 并不推荐
```git config submodule.[moduleName].url ssh://user@server/path```
更新模块
```git submodule update --recursive --remote```


### 修改submodule的url
1.clone项目
2.将.gitmodules文件中的地址换成新的地址
3.删除原先的submodule文件夹
4. 执行``git submodule init ``和``git submodule update --remote``




