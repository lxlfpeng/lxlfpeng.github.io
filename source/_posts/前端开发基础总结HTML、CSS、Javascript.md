---
title: 前端开发基础总结HTML、CSS、Javascript
date: 2019-03-18
categories: 
  - Web前端
tags:
  - CSS
  - Javascript
  - Html
---

# 一.Html网页
### 1. HTML标签
HTML 是用来描述网页的一种语言。HTML 标签是由尖括号包围的关键词，比如 <html> HTML 标签通常是成对出现的，比如 <b> 和 </b>。成对出现的标签中，第一个标签称为开始标签，第二个标签称为结束标签（闭合标签）。HTML 中的不同标签具有不同的含义，学习 HTML 其实就是学习各个标签的含义，根据实际场景的需要，选择合适的标签，从而制作出精美的网页。
HTML中每个标签都有自己的语义（含义），例如<p>标签代表段落，<b>标签代表加粗。根据标签的不同，浏览器会使用不同的方式展示标签中的内容。一般情况下，一个 HTML 标签由开始标签、属性、内容和结束标签组成，``标签的名称不区分大小写，但大多数属性的值需要区分大小写``，如下所示：
```
	  属性
	   ↓
<div class="foo">C语言中文网</div>
 ↑            ↑     ↑
开始标签        内容   结束标签
```
除了 class 属性外，开始标签中还可以包含其它属性信息，比如 id、title 等属性，当使用浏览器打开我们编写的 HTML 文档时，浏览器会从上到下依次读取文档中的内容，并根据 HTML 标签和属性将标签中的内容呈现在浏览器中。

### 2.HTML标签的通用属性
HTML 标签中有一些通用的属性，如 id、title、class、style 等，这些通用属性可以在大多数 HTML 标签中使用。

##### (1.)标签的id属性
id 属性用来赋予某个标签唯一的名称（标识符），当我们使用 CSS 或者 JavaScript 来操作这个标签时，就可以通过 id 属性来找到这个标签
```
<div id="content">测试代码</div>
```
##### (2.)标签的class属性
与 id 属性类似，class 属性也可以为标签定义名称（标识符），不同的是 class 属性在整个 HTML 文档中不必是唯一的，我们可以为多个标签定义相同的 class 属性值。
```
<div class="content">测试代码</div>
```
##### (3.)标签的style属性
使用 style 属性我们可以在 HTML 标签内部为标签定义 CSS 样式，例如设置文本的颜色、字体等
```
  <p style="color:red;">测试代码</p>
```

### 3.HTML文档流
文档流，又称为普通流或者常规流。在HTML中任何一个元素其实就是一个对象，也是一个盒子。文档流就是HTML在没有对样式进行设计前，网页行元素、块元素等的默认排列顺序。比如div的上下排布，p的左右排布等。
>浮动(float)、绝对定位(absolute)、固定定位(fixed)三种方式定位会脱离文档流(下文会讲解)。

### 4.HTML块级元素
``定义:``
正常流时，每个块级元素默认占一行高度 ，一行内添加一个块级元素后一般无法添加其他元素，元素样式的display:block都是块级元素。
`` 特点：``
- 总是在新行上开始。
- 高度，行高以及外边距和内边距都可控制。
- 宽度缺省是它的容器的100%，除非设定一个宽度。
- 它可以容纳内联元素和其他块元素。
``示例``

div、h1（大标题） 、 p（段落）  、hr、table

![](/images/74710f62de94973a6be0a7845e0ee3f5.webp)

### 5.HTML行内元素
``定义:``
行内元素不会另起一行,只占据它对应的标签的边框所包含内容的空间,元素样式的display : inline的都是行内元素。
``特点:``
- 和其他元素都在一行上；
- 高，行高及外边距和内边距不可改变；
- 宽度就是它的文字或图片的宽度，不可改变
- 内联元素只能容纳文本或者其他内联元素
``示例:``
a、  span、iframe、br（换行）、em（强调）、img（图片）、input、label、select 、textarea（多行文本输入框）
![](/images/a248db9f323fec8ca768b80eb9f904ef.webp)

# 二.CSS样式
CSS样式全称为Cascading Style Sheets，中文翻译为“层叠样式表”，简称样式表,CSS的作用就是定义如何显示html元素，设置他的背景、字体大小颜色、边框等等。
### 1.HTML中引入CSS
在HTML中引入CSS共有三种方式：行内样式就是把样式写在HTML元素里面，用style属性声明样式。
##### (1.)行内样式表(内联样式)
```
<text style="color:red;background-color:blue">hello world</text>
```
##### (2.)内部样式表
内部样式就是把CSS代码写在HTML文件里面，不同于行内样式，它是把CSS代码集中写在HTML文件的头部，就是<head></head>标签里面，用<style></style>标签注明。
```
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title></title>
    <style type="text/css">
        #p1{
            font-family:黑体;/*字体类型为黑体*/
            font-size:13px;/*文字大小为12像素*/
            font-weight:bold;/*文字加粗*/
            font-style:normal;/*文字正常，不设置斜体*/
            color:red;/*文字颜色为红色*/
        }
        #p2{
            font-family:微软雅黑;/*字体类型为微软雅黑*/
            font-size:19px;/*文字大小为16像素*/
            font-weight:normal;/*文字正常，不加粗*/
            font-style:italic;/*文字设置为斜体*/
            color:#1000FF;/*文字颜色取值用16进制RGB表示*/
        }
    </style>
</head>
<body>
    <div><!--CSS样式统一写在头部标签里面-->
        <p id="p1">hello</p>
        <p id="p2">hello</p>
    </div>
</body>
</html>
```
##### (3.)外部样式表(常用)
在实际开发当中，一般使用外部样式，就是把HTML和CSS分别写在不同的文件里，然后在HTML中用link标签来引用。这种方式能提高网站的性能，并且能方便网站的维护。
.wxml文件
```
//写在head标签中引入css文件，href属性中的为绝对路径，当前在同一级目录下
<head>
      <link href="style.css" rel="stylesheet" type="text/css" />
</head>
<body>
      <div class="outter">
          <div class="inner"></div >
      </div >
</body>
```
.wxss文件
```
.outter{
  
    padding: 20px;
	background-color: #2980B9;/*深蓝色*/
}
.inner{

    margin-top: 50px;
    width: 50px;
    margin: 50px;
    height: 50px;
    background-color: blueviolet
}
```

### 2.CSS基础语法
CSS 的核心功能是将 CSS 属性设定为特定的值。一个属性与值的键值对被称为声明（declaration）。
```
color: red;
```
而如果将一个或者多个声明用 {} 包裹起来后，那就组成了一个声明块（declaration block）。
```
{
    color: red;
    text-align: center;
}
```
声明块如果需要作用到对应的 HTML 元素，那还需要加上选择器。选择器和声明块组成了CSS 规则集（CSS ruleset），常简称为 CSS 规则。
```
text {
    color: red;
    text-align: center;
}
```

### 3.CSS中的注释
```
/* 单行注释 */

/*
    多行
    注释
*/
```

### 4.CSS选择器
在css中，通过模式匹配规则来决定给HTML的元素应用什么样的样式。这些模式规则就被称为选择器。CSS选择器是是CSS最重要的部分之一。它们使你能够在网页上针对你想要的HTML元素设置样式。

##### (1.)CSS 元素（标签）选择器
CSS元素选择器根据元素名来选择HTML元素。在HTML中，元素名就是类似于h1、 p的东西。
```
h3 {
 text-align: center;
 color: blue;
}

/** 设置元素p为红色 **/
p {
　　color: red;  
}

```
##### (2.)CSS ID 选择器
ID选择器选择具有匹配的ID属性的HTML元素。由于在一个HTML文档中不能有一个以上具有相同ID的元素，这个选择器允许你选择一个单独的元素。
```
/** 设置 id="myid" 的元素为红色 **/
#myid {
　　color: red;
}
```
##### (3.)CSS 类选择器
类选择器选择具有相同的class属性的HTML元素。类选择器对于定位多个元素很有用，比如你想要匹配样式的卡片或图像。
```
/** 设置 calss="myclass" 的元素为红色 **/
.myClass {
　　color: red
}
```

**多类选择器**
```
/** 设置 calss="myclass myotherclass" 的元素为红色 **/
.myClass.myotherclass {
　　color: red
}
```
##### (4.)CSS 通用选择器
通用选择器用来选择所有的HTML元素，这意味者你页面上的每一个元素，从标题到页脚。
```
/** 设置所有元素为红色 **/
* {
　　color: red;  
}
```

### 5.CSS盒子模型
html文档中的每个元素都被描绘成矩形盒子，这些矩形盒子通过一个模型来描述其占用空间，这个模型称为盒模型。
盒模型通过四个边界来描述：margin（外边距），border（边框），padding（内边距），content（内容区域）
[](https://upload-images.jianshu.io/upload_images/3067896-8d11825c69cff7b3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
一个盒子中主要的属性就5个：width、height、padding、border、margin。如下：
- width和height：内容的宽度、高度（不是盒子的宽度、高度）。
- padding：内边距。
- border：边框。
- margin：外边距。

### 6.CSS块级/行内元素转换。
display是CSS中最重要的用于控制布局的属性。每个元素都有一个默认的 display 值，这与元素的类型有关。对于大多数元素它们的默认值通常是 block或 inline。一个 block 元素通常被叫做块级元素。一个 inline 元素通常被叫做行内元素。
块级元素	|行内元素
-|-
独占一行,默认情况下，其宽度自动填满其父元素宽度	|相邻的行内元素会排列在同一行里，直到一行排不下，才会换行，其宽度随元素的内容而变化
可以设置width，height属性	|行内元素设置width，height属性无效
可以设置margin和padding属性	|行内元素起边距作用的只有margin-left、margin-right、padding-left、padding-right，其它属性不会起边距效果。
对应于display:block	| 对应于display:inline；

```
display:block; 转化为块状元素；一个块状元素独占一行；可设宽、高、行高、顶和底边距离；宽默认为父元素的100%；

display:inline;转化为行内元素；和其他元素共处一行；不可设宽、高、行高、顶和底边距离；宽即所包含的文字图片之宽；

display:inline-block:可用{display:inline-block;}转化为内联块状元素；和其他元素共处一行；可设宽、高、行高、顶和底边距离；
```

### 7.CSS定位
**文档普通流:**就是元素标签正常在HTML里的顺序，块级元素从上至下排列，行内元素从左到右排列。css中有三种手段可以使一个元素脱离标准文档流，分别为``浮动``和``绝对定位``,``固定定位``。
|属性|描述|
|-|-|
|absolute| 生成绝对定位的元素，相对于最近一级定位不是static的父元素来进行定位。元素的位置通过 "left", "top", "right" 以及 "bottom" 属性进行规定。|
|relative|生成相对定位的元素，相对于其所在普通的文档流位置进行定位。因此，"left:20" 会向元素的 LEFT 位置添加 20 像素。|
|static|默认值，没有定位，元素出现在正常的文档流中;|
|fixed|老IE不支持，和absolute一致，相对于窗口进行定位，当出现滚动条时，不随着滚动而滚动。元素的位置通过 "left", "top", "right" 以及 "bottom" 属性进行规定；|
|sticky|(CSS3)有兼容性问题，它就像是relative和fixed的合体，当在屏幕中时按常规流排版，当卷动到屏幕外时则表现如fixed。该属性的表现是现实中你见到的吸附效果。|

##### (1.)相对定位
```
position: relative
```
**元素相对于它自己原来的位置进行移动。**

``注意，相对定位使元素仍然占据原来的位置。``

如果将div2设置为相对定位，它会相对自己原来的位置移动，且会发现它原来的位置仍然占据着,不会被别的标签占据。
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <style type="text/css">
        div {
            width: 100px;
            height: 100px;
        }
    </style>

</head>
<body>
<body>
<div style="background-color: chartreuse">1</div>
<div style="background-color: darkblue;position: relative;top: 20px;left: 20px">2</div>
<div style="background-color: red">3</div>
</body>
</body>
</html>
```
![](/images/b6e758f3e20254bcb74d15522bd2e5e7.webp)

##### (2.).绝对定位
```
position: absolute
```
设置为绝对定位的元素框从文档流完全删除，并相对于其包含块定位，包含块可能是文档中的另一个元素或者是初始包含块。元素原先在正常文档流中所占的空间会关闭，就好像该元素原来不存在一样。元素定位后生成一个块级框，而不论原来它在正常流中生成何种类型的框。

如果将div2设置为绝对定位，会发现它会相对于HTML定位，因为没有已经定位的祖先元素，且原来的位置被div3补上了。
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <style type="text/css">
        div {
            width: 100px;
            height: 100px;
        }
    </style>

</head>
<body>
<body>
<div style="background-color: chartreuse">1</div>
<div style="background-color: darkblue;position: absolute;top: 20px;left: 20px">2</div>
<div style="background-color: red">3</div>
</body>
</body>
</html>
```
![](/images/0b180a83bafb57ea557e4b22d661fb9c.webp)

### 8.CSS浮动
##### (1.)CSS浮动基础
```
 float: left;
```
``定义:``
浮动,float，浮动的元素可以向左或向右移动，直到它的外边缘碰到包含的元素边框或另一个浮动元素的边框为止。
``注意:``
浮动会脱离标准文档流，所以文档的普通流的其他元素表现得就像浮动元素不存在一样。
**例子1:**
![](/images/12f96db3c626e41ac0dcbab77c992b11.webp)
``解释:``当框1向右浮动的时候,他会脱离文档流向右移动,直到他的右边缘碰到包含框的右边缘。
**例子2:**
![](/images/96e5a68132a516053f66db8ad59f7e4f.webp)
``解释:``当框1向左浮动时,他脱离文档流并且向左移动,知道他的左边缘碰到包含框的左边缘。因为它不再处于文档流中,所以他不占据空间,框2就会替代框1的位置,而由于框1浮在上方就会将框2覆盖住,使框2从视图中消失。
**例子3**
![](/images/9d1db7b73a82c140bd7a4cfa530395e8.webp)
``解释:``如果包含框太窄,无法容纳水平排列的三个浮动元素,那么其他的浮动块向下移动,直到有足够的空间。如果浮动元素的高度不同,那么当它们向下移动时可能被其他元素"卡住"。

##### (2.)float实现文字环绕
```
<div>
    <img style="background-color: chartreuse; width: 100px;height: 100px;float: left"/>
    <p>时光的单车飞快驶去，岁月的倒影也将消失，白天与黑夜不停的交替，轮回的四季斑驳了谁的岁月，
        蹉跎了谁的年华。一个人静静地与岁月交错，于平淡之中细细体会生活的深意，去注视，去聆听，
        去感受那些带着希望的别离以及那些经受沧桑的相逢，不论时光如何飞转，那些落花一样的往事，
        依然鲜活地存在于我的脑海之中。当岁月和美丽的回忆已成为风中的叹息，我们伤感的眼里也许依
        然残存旧时的泪痕，模糊了视线，不敢轻易触碰。</p>
</div>
```
![](/images/559b98249e64806d4b68c34b5b914536.webp)

##### (3.)CSS清除浮动
``为何要清除浮动?``
清除浮动主要是为了解决，父元素因为子级元素浮动引起的内部高度为0的问题。
``例如:``
创建给父容器设置边框和背景色。
```
<div style="border-style: outset;width: 400px;background-color: darkorange" >
    <div style="width: 200px;height: 200px;background-color: red">big</div>
    <div style="width: 100px;height: 100px;background-color: chartreuse">small</div>
</div>
```
![正常情况](/images/06dc83494fd894afd37e72a8c65ba680.webp)
将子控件设置为浮动
```
<div style="border-style: outset;width: 400px;background-color: darkorange" >
    <div style="width: 200px;height: 200px;background-color: red;float: left">big</div>
    <div style="width: 100px;height: 100px;background-color: chartreuse;float: left">small</div>
</div>
```
![父控件高度塌陷](/images/435018e62db91c884fc3b1c72b028bfb.webp)
当父元素不给高度的时候，内部元素不浮动时会撑开而浮动的时候，父元素变成一条线。
解决方式:
**方式一:给父级元素设置高度，但一般写页面高度都是不固定的。**
```
   #father {
            height: 300px;
        }
```
**方式二:给父级元素设置overflow:hidden或overflow:auto,zoom:1是为了浏览器的兼容性（IE大家都懂的），这种方法要注意溢出的元素。**
```
#father{
    overflow:hidden;
    zoom:1;
}
```
**方式三:给父级设置浮动，这种方法适用于本来父级就需要浮动的，如果父级不需要浮动，影响布局，还是没解决根本问题。**
```
#father{
    float:left;
}
```
**方式四:使用before和after双伪元素清除浮动（推荐）**
这种方法是推荐使用的，bootsrtap也在使用，应该掌握，不然太low了，他的原理就是通过伪元素选择器，在div后面添加了一个clear:both的属性，跟第三种方法是一样的道理。
```
 .clearfix:before, .clearfix:after {
            content: "";
            display: table;
        }

        .clearfix:after {
            clear: both;
        }

        .clearfix { /*照顾ie6*/
            zoom: 1;
            border-style: outset;
            width: 400px;
            background-color: darkorange;

        }
```
```
<div class="clearfix">
    <div style="width: 200px;height: 200px;background-color: red;float: left;">big</div>
    <div style="width: 100px;height: 100px;background-color: chartreuse;float: left;">small</div>
</div>
```

# 三.弹性布局Flex
### 1.Flex基础使用
网页布局在flex出来之前，是由盒模型为底子，float，position，table，百分比来进行布局的，重绘的比较多，影响性能，复杂又不好维护。flex布局，可以简便、完整、响应式地实现各种页面布局。
``概念``
采用Flex布局的元素，称为Flex容器（flex container），简称”容器”。（任何一个容器都可以指定为Flex布局，块级元素，行内元素也可。）
它的所有子元素自动成为容器成员，称为Flex项目（flex item），简称”项目”。

``主轴和交叉轴``
主轴和交叉轴取决于flex-direction的取值.如果flex-direction=raw那么水平方向上面的轴是主轴,垂直方向上面的轴是交叉轴。如果flex-direction=column那么垂直方向上面的轴是主轴,水平方向的轴是交叉轴。
 justify-content:用于主轴上的子元素的对齐方式。
align-items:用于交叉轴上的子元素的对齐方式。
``注意``
设为Flex布局以后，子元素的float、clear和vertical-align属性将失效。

display: flex; 将对象作为弹性伸缩盒展示，用于块级元素
display: inline-flex; 将对象作为弹性伸缩盒展示，用于行内元素

**例子:**
```
<div class="box"> <!--容器-->
  <div class="item">1</div> <!--子项-->
  <div class="item">2</div>
  <div class="item">3</div>
</div>
```
```
.box {
  width: 200px;
  height: 200px;
  background-color: #58a;
}
.item {
  width: 50px;
  height: 50px;
  margin: 2px;
  background-color: #fb3;
}
```

### 2.Flex 作用于Box容器上的属性
##### (1.) flex-direction
``定义:``
用于指定Flex主轴的方向，继而决定 Flex子项在Flex容器中的位置
``取值:``
**row , row-reverse , column , column-reverse**
``代码:``
```
box {
            width: 200px;
            height: 200px;
            background-color: chartreuse;
            display: flex;
            flex-direction: column-reverse;
            border: 5px solid red;
        }
```

**1. row：**
默认值，表示水平方向从左到右排列，此时水平方向轴线为主轴
![](/images/10fdef92ae6819e59c1f93d83b7da6c0.webp)

**2. row-reverse：**
与row相反,主轴为水平方向，起点在容器的右端。 
![](/images/173cbfebb2520eb6e7268fd324aa6291.webp)

**3. column：**
表示垂直方向从上到下排列，此时垂直方向轴线为主轴
![](/images/026d18a4bc1ac3355fb0b70b233682b1.webp)

**4. column-reverse：**
与column相反,主轴为垂直方向，起点在容器的下沿。 
![](/images/dfc029b4ba1ef5ec03095c851c868cba.webp)
##### (2.) flex-wrap
``定义:``
用于指定Flex子项是否换行。
``取值:``
nowrap , wrap , wrap-reverse
``代码:``
```
 .box {
            width: 200px;
            height: 200px;
            background-color: chartreuse;
            display: flex;
            flex-wrap: wrap;
            border: 5px solid red;
        }
```
**1. nowrap**
默认值，表示不换行，Flex子项平均分配。(不换行，在一行显示，即使子元素的宽度或者高度大于父元素的宽度或者高度，也在一行显示)
![](/images/7483f20b66fe7aecb448d8a655a82ca1.webp)

**2. wrap**
表示换行，溢出的Flex子项会被放到下一行。(解决间距的方式就是将Flex子项的父项目的高度设置为两行的高度)
![](/images/d5d07ed0db354f050a23ba9ee4d68a1b.webp)

**3. wrap-reverse**
表示反方向换行(换行后有两条轴线，reverse就是把轴线排列的顺序倒置过来)
![](/images/9b89e840d154f89c6299df7ef11ea185.webp)
##### (3.) justify-content
``定义:``
用于指定主轴(水平方向)上Flex子项的对齐方式
``取值``
flex-start , flex-end , center , space-between , space-around
``代码:``
```
 .box {
            width: 200px;
            height: 200px;
            background-color: chartreuse;
            display: flex;
            justify-content:flex-start;
            border: 5px solid red;
        }
```
**1. flex-start**
start侧对齐，左对齐
![](/images/c8021353ce18fe74858f5e30c4fe29ce.webp)

**2. flex-end**
end侧对齐，右对齐
![](/images/7ed7606cc3c0a857e9d22f8509b95897.webp)

**3. center**
中心对齐
![](/images/d76841875c7e3a10473d25f5e5b8a3a7.webp)

**4. space-between**
左边的靠左对齐,右边的靠右对齐,中间的等距排列。(两端对齐)
![](/images/e46faa4e3a20d52483da4f512c38e7fd.webp)

**5. space-around**
对于flex的子元素他们每侧的距离均相等(等距分布)
1和2之间的距离包含了1的下边距和2的上边距。
![](/images/c8b571251e4f706b7c32d8362a12572d.webp)
##### (4.) align-items
``定义``
用于指定交叉轴(又叫侧轴指的是垂直方向)上Flex子项的对齐方式
``取值``
stretch , flex-start , flex-end , center , baseline
``代码``
```
.box {
            width: 200px;
            height: 200px;
            background-color: chartreuse;
            display: flex;
            align-items:flex-start;
            border: 5px solid red;
        }
```
**1. stretch**
默认值，当Flex子项未设置高度或者高度值为auto时，stretch起作用，将Flex子项高度设置为行高度。这里需要注意，在只有一行的情况下，行的高度为容器的高度，即Flex子项高度为容器的高度
![](/images/140e7df5036346f3923a1ae9772ee34e.webp)


**2. flex-start**
表示与侧轴开始位置对齐
![](/images/44c0b4a2aed467d7f0346435c8d4954f.webp)
**3. flex-end**
表示与侧轴的结束位置对齐
![](/images/bae260cb8467f068cfb2f007bdfa2cf1.webp)

**4. center**
表示与侧轴中间对齐
![](/images/1a8d1d4c5acee87f427d3471834dc7f5.webp)

**5. baseline**
表示基线对齐，当行内轴与侧轴在同一线上，即所有Flex子项的基线在同一线上时，效果等同于flex-start。
![](/images/f0b08fecebdf9a93a5e560e62d9d0f4a.webp)
##### (5.) align-content
``定义:``
该属性只作用于多行的情况下，用于多行的对齐方式
``取值:``
stretch , flex-start , flex-end , center , space-between , space-around
```
.box {
            width: 200px;
            height: 200px;
            background-color: chartreuse;
            display: flex;
            align-content:flex-start;
            border: 5px solid red;
        }
```
**1. stretch**
默认值，当Flex子项未设置高度或者高度值为auto时，stretch起作用，将Flex子项高度设置为行高度。
**2. flex-start**
表示各行与侧轴开始位置对齐，第一行紧靠侧轴开始边界，之后的每一行都紧靠前面一行
flex-end：表示各行与侧轴的结束位置对齐，最后一行紧靠侧轴结束边界，之后的每一行都紧靠前面一行
**3. flex-start**
表示各行与侧轴中间对其
**4. space-between**
表示两端对齐，中间间距相等。要注意特殊情况，当剩余空间为负数时，效果等同于flex-start
space-around：表示各行之间间距相等，中间间距是两端间距的2倍。要注意特殊情况，当剩余空间为负数时，效果等同于center
再次强调：该属性只作用于多行的情况，在只有一行的Flex容器上无效，另外该属性可以很好的处理，换行以后相邻行之间产生的间距。

### 3. Flex 作用于子项上的6个属性介绍
##### (1.)  order
该属性用来指定Flex子项的排列顺序，数值越小，越靠前，可以为负数

取值：数值，默认值为0

##### (2.)  flex-grow

用来指定Flex子项的扩展比例，不可以为负数，Flex容器会根据Flex子项设置的扩展比例作为比率来分配剩余空间

取值：数值，默认值为0，表示即使存在剩余空间，Flex子项也不会扩展

##### (3.)  flex-shrink

用来指定Flex子项的收缩比例，不可以为负数，Flex容器会根据Flex子项设置的收缩比例作为比率来收缩各个Flex子项

取值：数值，默认值为1，表示所有子项在剩余空间为负数时，等比例收缩

注意：flex-shrink只能在不换行的情况下使用

##### (4.)flex-basis

用来指定Flex子项的占据的空间，不可以为负数

取值：auto | length | percentage | content

auto：默认值，计算规则：检索Flex子项是否设置了width值（或者height值，取决于flex-direction），如果设置了非auto的值，则使用width值（或者height值），若没有则使用content
length：用长度值定义宽度，不可为负数
percentage：使用百分比定义宽度，不可为负数

容器宽度为200px，Item1原始宽度为50px，设置 flex-basis: 50%;后宽度变成100px，扩展后宽度为110.5px；而Item2原始宽度为50px，扩展后为81.5px，比例正好是1:3

# 四.JavaScript简介
JavaScript一种直译式脚本语言，是一种``动态类型``、``弱类型``、基于原型的语言，内置支持类型。它的解释器被称为JavaScript引擎，为浏览器的一部分，广泛用于客户端的脚本语言，最早是在HTML（标准通用标记语言下的一个应用）网页上使用，用来给HTML网页增加动态功能。
### 1.JavaScript发展
##### (1.)ECMAScript
因为JavaScript兼容于ECMA标准，因此也称为ECMAScript。JavaScript 由 ECMA（欧洲电脑制造商协会）通过 ECMAScript 实现语言的标准化。
![](/images/dd79e9f6bbb82f237ff46382663b8e56.webp)

##### (2.)TypeScript
TypeScript 是 JavaScript 的一个超集(TypeScript包含所有的JavaScript功能)，支持 ECMAScript 6 标准。TypeScript 由微软开发的自由和开源的编程语言。

##### (3.)JavaScript常见框架
 ``AngularJS、ReactJS、VueJS、NodeJS``
 

### 2.HTML中引入JavaScript
##### (1.)HTML引入内部的 JavaScript
如需在 HTML 页面中插入 JavaScript，<script> 和 </script> 会告诉 JavaScript 在何处开始和结束。

```
<html>
<body>
<script>
function myFunction(){
	alert("JavaScript运行了");
}
</script>
<button type="button" onclick="myFunction()">点击这里</button>
</body>
</html>
```

##### (2.)HTML引入外部的 JavaScript
也可以把脚本保存到外部文件中。外部文件通常包含被多个网页使用的代码。
外部 JavaScript 文件的文件扩展名是 .js。
如需使用外部文件，请在 <script> 标签的 "src" 属性中设置该 .js 文件：
myJs.js:
```
function myFunction(){
	alert("JavaScript运行了");
}
```
html:
```
<html>
<body>
<script src="myJs.js">
</script>
<button type="button" onclick="myFunction()">点击这里</button>
</body>
</html>
```

# 五.JavaScript语法
### 1.JavaScript变量
JavaScript的变量是松散类型的,不用给变量指定数据类型,它会根据变量的值推导出自己的数据类型。
#### (1.)变量的定义规则
- 变量必须以字母开头
- 变量也能以 $ 和 _ 符号开头（不推荐）
- 变量名称对大小写敏感（y 和 A 是不同的变量）
``JavaScript 语句和 JavaScript 变量都对大小写敏感。 ``

#### (2.)变量作用域
##### 全局作用域(全局变量)
1. 生命周期将存在于整个程序之内。
2. 在函数定义外声明的变量是全局变量。
3. 全局变量有 全局作用域，它的值可在整个程序中访问和修改。
4. 如果变量在函数内没有声明（没有使用 var 关键字），该变量为全局变量。
**显式声明：**
```
<script>
    var testFile = 123456;
    var testFunc = function () {
        console.log('test')
    };
    console.log(window.testFunc)        // ƒ () { console.log('test') }
    console.log(window.testFile)		// 123456
</script>
```
**隐式声明：**
不带有声明关键字的变量,会被声明成全局变量。
```
<script>
    function test() {
        result = 123;	                // 没有var等修饰
    }

    test()                              //调用该方法
    console.log(window.result);			// 123
</script>
```
##### 函数作用域(局部变量)
1. 在函数定义内声明的变量是局部变量。
2. 因为局部变量只作用于函数内，所以不同的函数可以使用相同名称的变量。
3. 每当执行函数时，都会创建和销毁该变量，且无法通过函数之外的任何代码访问该变量。
4. 函数外无法访问函数内的变量，函数内却可以访问函数外的变量。
```
  function bar() {
        var testValue = 'inner';
    }
    bar()
    console.log(testValue);		// 报错：ReferenceError: testValue is not defined
```
##### 块级作用域
块级作用域指在If语句，switch语句，循环语句等语句块中定义变量，这意味着变量不能在语句块之外被访问。如果想要实现 块级作用域 那么我们需要用 let 关键字声明。
var声明的变量不能实现块级作用域
```
for(var i = 0; i < 5; i++) {
  // ...
}
console.log(i)				// 5
```
let声明的变量是可以实现块级作用域
```
if (true) {
  const a = 'inner';
}
console.log(a);				// 报错：ReferenceError: a is not defined
```

### 2.JavaScript数据类型
##### (1.)基本数据类型
字符串（String）、数字(Number)、布尔(Boolean)、对空（Null）、未定义（Undefined）

##### (2.)引用数据类型
对象(Object)、数组(Array)、函数(Function)。

##### (3.)类型判断
**typeof**
typeof返回一个表示数据类型的字符串，返回结果包括：number、string、boolean、object、undefined、function。typeof可以对基本类型number、string  、boolean、undefined做出准确的判断,而对于引用类型，除了function之外返回的都是object。
**constructor**
constructor 属性返回所有 JavaScript 变量的构造函数。

##### (4.)类型转换
全局方法 String() 可以将数字转换为字符串。
全局方法 Number() 可以将字符串转换为数字。

### 3.JavaScript数据容器
#### (1.)创建数组
一般有两种方式进行定义。
**方式一:**
```
var array=new Array(); 
array[0]="1";       
array[1]="2";
array[2]="3";
```
**方式二:**
```
var array=["1","2","3"];
```
#### (2.)数组元素访问
使用array[角标] 取出元素。
```
var array=["1","2","3"];
var index=array[0];//取出数组的第一个元素
```
#### (3.)数组常用方法
方法|解释
--|--
arr.lenth |返回数组的长度
arr.push(value1, ..., valueN)	|在数组末尾增加一个或多个数组元素，并返回增加元素后的数组长度。
arr.unshift(value1, ..., valueN)|在数组头部增加一个或多个数组元素，并返回增加元素后的数组长度。
arr.shift()	| 删除数组的第一个元素，并返回该被删元素的值。
arr.splice(start,delteCount)|	从start指定的位置开始，删除delteCount个数组元素。
arr.cancat(array1,array2,...) |	将多个数组合并为一个新的数组。
arr.join(separator)	|使用指定的分隔符（separator）将数组元素依次拼接起来，形成一个字符串返回。
arr.reverse()	| 颠倒数组中元素的顺序。
arr.slice(start,end)|从现有数组中提取指定个数的数据元素，形成一个新的数组。所提取元素的下标从start开始，到end结束，但不包括end。
arr.sort(orderfunc)|将数组元素排序。参数orderfunc可选。省略该参数时，按字母顺序或汉字的拼音方式排序。可以使用orderfunc来指定排序方式。orderfunc为排序函数的名称，该函数应该使用两个参数，并返回一个整数值。返回值的要求是：当第一个参数大于第二个参数时，返回值大于0；当第一个参数等于第二个参数时，返回值等于0；当第一个参数小于第二个参数时，返回值小于0。
arr.toString()	|返回数组的字符串表示。
#### (4.)清空数组
**方式一:给数组的长度赋值为0**
```
var arr = [1,2,3];
arr.lenth=1
```
**方式二:使用slice函数**
```
var arr = [1,2,3];
arr .splice(0,arr .length);
```
**方式三:给数组赋值为[]**
```
var arr = [1,2,3];
arr=[]
```

### 4.JavaScript运算符
#### (1.)JavaScript 算数运算符。
``+加法 - 减法 *乘法 /除法 %系数 ++递加 --递减``
#### (2.)JavaScript 赋值运算符。
``=	+=	-=	*=	/=	%=``
#### (3.)JavaScript 比较运算符。
![](/images/a6229cd2d60cec037981867bba4ae714.webp)
#### (4.)JavaScript 逻辑运算符。
![](/images/ea2b695272c82c5ca944f47382940aa7.webp)

### 5.JavaScript流程控制
#### (1.)判断语句
if 语句 - 只有当指定条件为 true 时，使用该语句来执行代码
if...else 语句 - 当条件为 true 时执行代码，当条件为 false 时执行其他代码
if...else if....else 语句- 使用该语句来选择多个代码块之一来执行
#### (2.)选择语句
```
switch(n)
{
    case 1:
        执行代码块 1
        break;
    case 2:
        执行代码块 2
        break;
    default:
        与 case 1 和 case 2 不同时执行的代码
}
```
#### (3.)循环语句
##### for循环
```
for (var i=0; i<5; i++)
{
      x=x + "该数字为 " + i + "<br>";
}
```
For/In 循环
```
var person={fname:"John",lname:"Doe",age:25}; 
 
for (x in person)  // x 为属性名
{
    txt=txt + person[x];
}
```
##### while 循环
```
while (条件)
{
    需要执行的代码
}
```
#### (4.)Break 和 Continue 语句
- break 语句用于跳出循环。
- continue 用于跳过循环中的一个迭代。

### 6.JavaScript函数
#### (1.)JavaScript函数的分类
- 自定义函数(我们自己编写的函数)，如：function funName(){}
- 系统函数(JavaScript自带的函数)，如alert函数。
#### (2.)函数声明
JavaScript 使用关键字 function 定义函数。
```
function functionName(parameters) {
  执行的代码
}
```

### 7.JavaScript对象
#### (1.)创建对象。
**方式一:通过object创建**
```
 var person = new Object();
 person.name = "peng";
 person.age = 27;
```
**方式一:通过”字面量“方式创建。**
```
var person ={
  name: "peng",
  age: 27,
}
```
#### (2.)对象属性访问。
```
var person ={
  name: "peng",
  age: 27,
}
person.name//获取name元素
```

### 8.JavaScript类的导出与导入
```
class Home{
    constructor(){
    }
//获取数据
    getData(){
     
    }
};
export {Home};
```
```
import {Home} from 'home-model.js';

var home = new Home(); 
Page({
    data: {
    },
    onLoad: function () {
       home.getBannerData(() => {
        });
    }
})
```

[CSS选择器详解](https://www.cnblogs.com/laixiangran/p/8735202.html)


