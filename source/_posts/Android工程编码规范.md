---
title: Android工程编码规范
---

# 一. AndroidStudio开发工具规范
1. 使用最新的稳定版本.
2. 统一文件的编码格式为utf-8.
![](/images/0f96a62ef7972365a0f44923dec209c6.webp)
3. 清除每个类里面的无效的import导包.
4. 代码样式统一,比如，tab缩进4个空格，或者 tab size等如果没有特殊情况使用默认的配置即可。
5. 每行字数每行字符数不得超过 160 字符，设置 Editor -> Code Style.
![](/images/1b2eea0aa33e36e90c2cb4a886da568c.webp)
6. 编辑完 .java、.kt、.xml 等文件后必须格式化.

# 二. 命名规范
## 1. 包名
包名全部小写，不允许出现中文、大写字母或者下划线。

## 2. 类名
类名采用大驼峰命名法，用名词或名词词组命名，每个单词的首字母大写。尽量避免缩写，除非该缩写是众所周知的， 比如 HTML、URL，如果类名称中包含单词缩写，则单词缩写的每个字母均应大写。
| 类  | 描述 | 例如  |
| - | - | - |
| `Activity`类                               | 模块名 +`Activity`             | 闪屏页类`SplashActivity`            |
| `Fragment`类                               | 模块名 +`Fragment`             | 主页类`HomeFragment`                |
| `Service`类                                | 模块名 +`Service`              | 时间服务`TimeService`               |
| `BroadcastReceiver`类                      | 功能名 +`Receiver`             | 推送接收`JPushReceiver`             |
| `ContentProvider`类                        | 功能名 +`Provider`             | `ShareProvider`                     |
| 自定义 View                                 | 功能名 + View/ViewGroup(组件名称)  | `ShapeButton`                       |
| Dialog对话框                                | 功能名+Dialog                      | `ImagePickerDialog`                 |
| `Adapter`类                                | 模块名 +`Adapter`              | 课程详情适配器`LessonDetailAdapter` |
| 解析类                                      | 功能名 +`Parser`               | 首页解析类`HomePosterParser`        |
| 工具方法类                                   | 功能名 +`Utils`或`Manager` | 线程池管理类：`ThreadPoolManager`   |
| 日志工具类：`LogUtils`（`Logger`也可）         |                                    |
| 打印工具类：`PrinterUtils`                    |                                    |
| 数据库类                                     | 功能名 +`DBHelper`             | 新闻数据库：`NewsDBHelper` |
| 自定义的共享基础类                             | `Base`+ 基础                   | `BaseActivity`,`BaseFragment` |
| 抽象类                                       | `Base`/`Abstract`开头      | `AbstractLogin` |
| 异常类                                         | `Exception`结尾                | `LoginException` |


接口（interface）：命名规则与类一样采用大驼峰命名法。

## 3. 方法名

方法名都以 `lowerCamelCase` 风格编写。方法名通常是动词或动词短语。

| 方法                               | 说明                                                               |
| ------------------------------------ | -------------------------------------------------------------------- |
| `initXX()`                     | 初始化相关方法，使用 init 为前缀标识，如初始化布局`initView()` |
| `isXX()`,`checkXX()`       | 方法返回值为 boolean 型的请使用 is/check 为前缀标识                |
| `getXX()`                      | 返回某个值的方法，使用 get 为前缀标识                              |
| `setXX()`                      | 设置某个属性值                                                     |
| `handleXX()`,`processXX()` | 对数据进行处理的方法                                               |
| `displayXX()`,`showXX()`   | 弹出提示框和提示信息，使用 display/show 为前缀标识                 |
| `updateXX()`                   | 更新数据                                                           |
| `saveXX()`,`insertXX()`    | 保存或插入数据                                                     |
| `resetXX()`                    | 重置数据                                                           |
| `clearXX()`                    | 清除数据                                                           |
| `removeXX()`,`deleteXX()`  | 移除数据或者视图等，如`removeView()`                           |
| `drawXX()`                     | 绘制数据或效果相关的，使用 draw 前缀标识                           |

## 4. 变量命名

这里的变量为广义的变量，包括了常量、局部变量、全局变量等，它们的基础规则是：

* 类型需要是名词 / 名词短语；
* 采用 `lowerCamelCase` 风格；

在具体的变量命名时，会根据该变量的类型不同而附加额外的命名规则：

| 类型                               | 说明                                                                                     | 例如                            |
| ------------------------------------ | ------------------------------------------------------------------------------------------ | --------------------------------- |
| 常量                                  | 大写 & 下划线隔开，Kotlin 一定要 const val                                               | `const val TYPE_NORMAL = 1` `static final TYPE_NORMAL = 1`|                                                                                      |
| 临时变量名                             | 整型：`i`、`j`、`k`、`m`、`n`，字符型一般用`c`、`d`、`e` | `for(int i = 0;i < len; i++)`   |
| 其他变量                               | `lowerCamelCase`风格即可，私有变量也不要使用`m`开头                              | `private int tmp;` |
| Kotlin                                | 只读变量使用`val`，可变变量使用`var`，尽可能使用`val`                        | `var tmp = 0` `val defaultIndex = 0` |


## 5. 资源文件
资源文件命名为全部小写，采用下划线命名法。

###  动画资源文件（anim/ 和 animator/）
安卓主要包含属性动画和视图动画，其视图动画包括补间动画和逐帧动画。属性动画文件需要放在 `res/animator/` 目录下，视图动画文件需放在 `res/anim/` 目录下。命名规则：`{模块名_}逻辑名称`。

> 说明：`{}` 中的内容为可选，`逻辑名称` 可由多个单词加下划线组成。例如：`refresh_progress.xml`、`market_cart_add.xml`、`market_cart_remove.xml`。

如果是普通的补间动画或者属性动画，可采用：`动画类型_方向` 的命名方式。

例如：

| 名称                    | 说明           |
| ------------------------- | ---------------- |
| `fade_in`           | 淡入           |
| `fade_out`          | 淡出           |
| `push_down_in`      | 从下方推入     |
| `push_down_out`     | 从下方推出     |
| `push_left`         | 推向左方       |
| `slide_in_from_top` | 从头部滑动进入 |
| `zoom_enter`        | 变形进入       |
| `slide_in`          | 滑动进入       |
| `shrink_to_middle`  | 中间缩小       |

### 图片资源文件（drawable/ 和 mipmap/）

`res/drawable/` 目录下放的是位图文件（.png、.9.png、.jpg、.gif）或编译为可绘制对象资源子类型的 XML 文件，而 `res/mipmap/` 目录下放的是不同密度的启动图标，所以 `res/mipmap/` 只用于存放启动图标，其余图片资源文件都应该放到 `res/drawable/` 目录下。

命名规则：`类型{_模块名}_逻辑名称`、`类型{_模块名}_颜色`。

> 说明：`{}` 中的内容为可选；`类型` 可以是可绘制对象资源类型，也可以是控件类型最后可加后缀 `_small` 表示小图，`_big` 表示大图。

例如：

| 名称                          | 说明                                           |
| ------------------------------- | ------------------------------------------------ |
| `btn_main_about.png`      | 主页关于按键`类型_模块名_逻辑名称`         |
| `btn_back.png`            | 返回按键`类型_逻辑名称`                    |
| `divider_maket_white.png` | 商城白色分割线`类型_模块名_颜色`           |
| `ic_edit.png`             | 编辑图标`类型_逻辑名称`                    |
| `bg_main.png`             | 主页背景`类型_逻辑名称`                    |
| `btn_red.png`             | 红色按键`类型_颜色`                        |
| `btn_red_big.png`         | 红色大按键`类型_颜色`                      |
| `ic_avatar_small.png`     | 小头像图标`类型_逻辑名称`                  |
| `bg_input.png`            | 输入框背景`类型_逻辑名称`                  |
| `divider_white.png`       | 白色分割线`类型_颜色`                      |
| `bg_main_head.png`        | 主页头部背景`类型_模块名_逻辑名称`         |
| `def_search_cell.png`     | 搜索页面默认单元图片`类型_模块名_逻辑名称` |
| `ic_more_help.png`        | 更多帮助图标`类型_逻辑名称`                |
| `divider_list_line.png`   | 列表分割线`类型_逻辑名称`                  |
| `sel_search_ok.xml`       | 搜索界面确认选择器`类型_模块名_逻辑名称`   |
| `shape_music_ring.xml`    | 音乐界面环形形状`类型_模块名_逻辑名称`     |

如果有多种形态，如按钮选择器：`sel_btn_xx.xml`，采用如下命名：

| 名称                        | 说明                                   |
| ----------------------------- | ---------------------------------------- |
| `sel_btn_xx`            | 作用在`btn_xx`上的`selector`   |
| `btn_xx_normal`         | 默认状态效果                           |
| `btn_xx_pressed`        | `state_pressed`点击效果            |
| `btn_xx_focused`        | `state_focused`聚焦效果            |
| `btn_xx_disabled`       | `state_enabled`不可用效果          |
| `btn_xx_checked`        | `state_checked`选中效果            |
| `btn_xx_selected`       | `state_selected`选中效果           |
| `btn_xx_hovered`        | `state_hovered`悬停效果            |
| `btn_xx_checkable`      | `state_checkable`可选效果          |
| `btn_xx_activated`      | `state_activated`激活效果          |
| `btn_xx_window_focused` | `state_window_focused`窗口聚焦效果 |

> 注意：使用 Android Studio 的插件 SelectorChapek 可以快速生成 selector，前提是命名要规范。

### 布局资源文件（layout/）

命名规则：`类型_模块名`、`{模块名_}类型_逻辑名称`。(也采用 PBF，方便查看，尤其在大项目中)

> 说明：`{}` 中的内容为可选。

例如：

| 类型                  | 名称                     | 说明                                       |
| ----------------------- | -------------------------- | -------------------------------------------- |
| `Activity`        | `main_activity.xml`  | 主窗体`模块名_类型`                    |
| `Fragment`        | `music_fragment.xml` | 音乐片段`模块名_类型`                  |
| `Dialog`          | `loading_dialog.xml` | 加载对话框`逻辑名称_类型`              |
| `PopupWindow`     | `info_ppw.xml`       | 信息弹窗（PopupWindow）`逻辑名称_类型` |
| `adapter`的列表项 | `main_song_item.xml` | 主页歌曲列表项`模块名_类型_逻辑名称`   |

### 布局资源 id 命名
命名规则：view 缩写{_模块名}_逻辑名，例如： btn_main_search、btn_back。
**注意:使用databinding,viewbinding 直接获取布局文件控件的时候，id 命名采用驼峰样式。**

### 菜单资源文件（menu/）

菜单相关的资源文件应放在该目录下。命名规则：`{模块名_}逻辑名称`

> 说明：`{}` 中的内容为可选。

### 字符串资源文件strings

`<string>` 的 `name` 命名使用下划线命名法，采用以下规则：`{模块名_}逻辑名称`，这样方便同一个界面的所有 `string` 都放到一起，方便查找。

| 名称                    | 说明           |
| ------------------------- | ---------------- |
| `main_menu_about`   | 主菜单按键文字 |
| `friend_title`      | 好友模块标题栏 |
| `friend_dialog_del` | 好友删除提示   |
| `login_check_email` | 登录验证       |
| `dialog_title`      | 弹出框标题     |
| `button_ok`         | 确认键         |
| `loading`           | 加载文字       |


### 样式资源文件tyles
`<style>` 的 `name` 命名使用大驼峰命名法，几乎每个项目都需要适当的使用 `styles.xml` 文件，因为对于一个视图来说，有一个重复的外观是很常见的，将所有的外观细节属性（`colors`、`padding`、`font`）放在 `styles.xml` 文件中。在应用中对于大多数文本内容，最起码你应该有一个通用的 `styles.xml` 文件，例如：
```
<style name="ContentText">
    <item name="android:textSize">@dimen/font_normal</item>
    <item name="android:textColor">@color/basic_black</item>
</style>
```
应用到 TextView 中：
```
<TextView
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:text="@string/price"
    style="@style/ContentText"/>
```
或许你需要为按钮控件做同样的事情，将一组相关的和重复 android:xxxx 的属性放到一个通用的 <style> 中。

### 颜色资源文件（color/）

color/ 是专门用于存放颜色相关资源的文件夹。命名规则：`类型{_模块名}_逻辑名称`。

> 说明：`{}` 中的内容为可选。例如：`sel_btn_font.xml`。


`<color>` 的 `name` 命名使用下划线命名法，在你的 `colors.xml` 文件中应该只是映射颜色的名称一个 ARGB 值，而没有其它的。不要使用它为不同的按钮来定义 ARGB 值。

<?xml version="1.0" encoding="utf-8"?>
<resources>

      <!-- grayscale -->
      <color name="white"     >#FFFFFF</color>
      <color name="gray_light">#DBDBDB</color>
      <color name="gray"      >#939393</color>
      <color name="gray_dark" >#5F5F5F</color>
      <color name="black"     >#323232</color>

      <!-- basic colors -->
      <color name="green">#27D34D</color>
      <color name="blue">#2A91BD</color>
      <color name="orange">#FF9D2F</color>
      <color name="red">#FF432F</color>

</resources>

向应用设计者那里要这个调色板，名称不需要跟 `"green"`、`"blue"` 等等相同。`"brand_primary"`、`"brand_secondary"`、`"brand_negative"` 这样的名字也是完全可以接受的。像这样规范的颜色很容易修改或重构，会使应用一共使用了多少种不同的颜色变得非常清晰。通常一个具有审美价值的 UI 来说，减少使用颜色的种类是非常重要的。

**注意：如果某些颜色和主题有关，那就单独写一个 `colors_theme.xml`。**

# 注释规范

## 4.1 类注释

每个类完成后应该有作者姓名和联系方式的注释，对自己的代码负责。
```
/**
 * @Author ：xxx
 * @Date   ：xxxx/xx/xx
 * @Email  ：xxxxxx@xxx.com
 * @Desc   ：欢迎界面
 */
public class WelcomeActivity {
    ...
}
```


具体可以在 AS 中自己配制，进入 Settings -> Editor -> File and Code Templates -> Includes -> File Header，输入
```
/**
 * @Author : ${USER}
 * @Date   : ${YEAR}/${MONTH}/${DAY}
 * @Email  : xxx@xx
 * @Desc   :
 */
```
这样便可在每次新建类的时候自动加上该头注释。

## 4.2 方法注释

每一个成员方法（包括自定义成员方法、覆盖方法、属性方法）的方法头都必须做方法头注释，在方法前一行输入 `/** + 回车` 或者设置 `Fix doc comment`（Settings -> Keymap -> Fix doc comment）快捷键，AS 便会帮你生成模板，我们只需要补全参数即可。

## 4.3 块注释
块注释与其周围的代码在同一缩进级别。它们可以是 `/* ... */` 风格，也可以是 `// ...` 风格（ **`//` 后最好带一个空格** ）。对于多行的 `/* ... */` 注释，后续行必须从 `*` 开始， 并且与前一行的 `*` 对齐。


## 4.4 全局变量的注释

全局变量的注释样式如下（注意注释之间有空格）：

```
/**
 * The next available accessibility id.
 */
private static int nextAccessibilityViewId;
/**
 * The animation currently associated with this view.
 */
protected Animation currentAnimation = null;
```

## 4.5 其他一些注释

AS 已帮你集成了一些注释模板，我们只需要直接使用即可，在代码中输入 `TODO`、`FIXME` 等这些注释模板，回车后便会出现如下注释。

```
// TODO: 17/3/14 需要实现，但目前还未实现的功能的说明
// FIXME: 17/3/14 需要修正，甚至代码是错误的，不能工作，需要修复的说明
```

## 4.5 注释必须遵守的规范
- 提测的代码不应该有 TODO 这样的注释

# GIT管理规范

