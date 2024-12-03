---
title: Vue前端开发
---

# 一.Vue简介
Vue是和jQuery一样是一个前端框架，它的中心思想就是用数据驱动UI。在使用jQuery的时代，如果要改变某一个DOM元素的值，jQuery首先要获取到dom对象，然后对dom对象进行进行值的修改等操作; 而Vue.js 则是专注于 MVVM 模型的 ViewModel 层，Vue首先会把值和ViewModel对象进行绑定，然后修改ViewModel对象的值，Vue这个框架就会自动做好Dom的相关操作，这种dom元素跟随ViewModel对象值的变化而变化叫做单向数据绑定，如果ViewModel对象的值也跟随着dom元素的值的变化而变化就叫做双向数据绑定。

# 二.引入vue.js
在使用Vue.js之前我们需要先引入Vue.js才能使用，引入Vue.js一般有三种方式:本地引入，CDN引入，Npm脚手架引入。
### 1.下载vue.js到本地引入
可以在Vue.js的官网上直接下载vue.js，并在.html中通过``<script>``标签中引用vue.js进行使用。
>开发环境不要使用最小压缩版，不然会没有错误提示和警告！

### 2.使用CDN方法引入vue.js
- [BootCDN（国内不稳定）](https://cdn.bootcss.com/vue/2.2.2/vue.min.js)
- [unpkg（会保持和 npm 发布的最新的版本一致，推荐使用）](https://unpkg.com/vue/dist/vue.js)
- [cdnjs](https://cdnjs.cloudflare.com/ajax/libs/vue/2.1.8/vue.min.js)

示例如下:
```
<!DOCTYPE html>
<html>
	<head>
		<title>Vue学习</title>
		<meta charset="utf-8">
		<script type="text/javascript" src="https://cn.vuejs.org/js/vue.js"></script>
	</head>
	<body>
		...
	</body>
</html>
```

### 3.NPM脚手架的方式(推荐)
推荐使用该种方式，后续会详解，本篇先略过。

# 三.Vue入门案例
1.定义Vue的工作区域。
2.导入函数类库。
3.实例化Vue对象。
4.数据引用-使用插值表达式。
```
<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title>入门案例</title>
	</head>
	<body>
		<!-- 1.定义vue工作的区域 -->
		<div id="app">
			<h1>vue的入门案例</h1>
			<!-- 4数据的引用 插值表达式-->
			{{hello}}
		</div>

		<!-- 2.导入函数类库 -->
		<script src="https://cdn.jsdelivr.net/npm/vue@2.5.21/dist/vue.js"></script>

		<!-- 3.实列化vue对象 -->
		<script>
			const app=new Vue({
				//关键字el：标识vue对哪个元素有效
				el: "#app",
				data: {
					hello:"你好Vue"
				}
			});
		</script>
	</body>
</html>
```

# 四.Vue模板语法
Vue.js 使用了基于 HTML 的模板语法，允许开发者声明式地将 DOM 绑定至底层 Vue 实例的数据。Vue.js 的核心在于允许使用简洁的模板语法来声明式的将数据渲染进 DOM 的系统。 结合响应系统，在应用状态改变时， Vue 能够智能地计算出重新渲染组件的最小代价并应用到 DOM 操作上。
在Html中包含的语法代码Vue.js分为两种：
-  插值语法（双大括号表达式）。
-  指令（以 v-开头）。
### 1.Vue插值语法
1. 功能: 用于解析标签体内容。
2. 语法: {{xxx}} ，xxxx 会作为 js 表达式解析到Html中。
```
<!DOCTYPE html>
<html>
	<head lang="en">
		<meta charset="UTF-8">
		<title>Vue插值语法</title>
		<!--1.引入vue.js-->
		<script src="https://cdn.jsdelivr.net/npm/vue@2.5.21/dist/vue.js"></script>
	</head>
	<body>
		<!--view视图-->
		<div id="app">
			{{message}}
		</div>
		<script>
			var vue=new Vue({
			        <!--关联id为app的元素-->
			        el:"#app",
			         /*model数据*/
			         data:{
			             message:"hello,vue"
			         }
			     });
		</script>
	</body>
</html>
```

### 2.Vue指令语法
1. 功能: 解析标签属性、解析标签体内容、绑定事件。
2. 举例：``v-bind:href = 'xxxx' ``，xxxx 会作为 js 表达式被解析。
```
<!DOCTYPE html>
<html>
	<head lang="en">
		<meta charset="UTF-8">
		<title>Vue指令语法</title>
		<!--1.引入vue.js-->
		<script src="https://cdn.jsdelivr.net/npm/vue@2.5.21/dist/vue.js"></script>
	</head>
	<body>
		<!--view视图-->
		<div id="app">
			<a v-bind:href="url">点我</a>
		</div>
		<script>
			var vue=new Vue({
			        el:"#app",
			         /*model数据*/
			         data:{
			           url: "http://www.baidu.com",
			         }
			     });
		</script>
	</body>
</html>
```

Vue常用的内置指令:

|指令	|描述|
|-|-|
|v-text | 和插值一样也是使用vue中的变量，会覆盖原本的内容，插值不会 |
|v-html | 显示HTML的内容 |
|v-if   | 如果为 true， 当前标签才会输出到页面 |
|v-else | 如果为 false， 当前标签才会输出到页面 |
|v-show | 通过控制 display 样式来控制显示/隐藏 |
|v-for  | 遍历数组/对象 |
|v-on   | Vue提供的事件绑定机制，缩写是:’@’ |
|v-bind | Vue提供的属性绑定机制，缩写是 ‘:’ |
|v-model| 双向数据绑定 |
|v-cloak| 解决 插值表达式闪烁的问题 |

##### v-bind
v-bind就是用于绑定数据和元素属性的
完整示例：
```
<body>
    <div class="app">
        <a v-bind:href="url">点击</a>
    </div>
 <script>
     var app = new Vue({
         el:'.app',
         data:{
             url:"https://www.baidu.com",
         }
     });
 </script>
</body>
```
注意： v-bind后面是：属性名=，表示绑定这个属性，绑定之后，对应的值要去vue的数据里面找。当我们在控制台改变url时，对应也会变化。
相同的，还可以绑定图片src属性、超链接的class:
```
<body>
    <div class="app">
        <a v-bind:href="url">点击</a>
        <img v-bind:src="imgsrc" width="200px"/>
    </div>
 <script>
     var app = new Vue({
         el:'.app',
         data:{
             url:"https://www.baidu.com",
             imgsrc:"https://cn.vuejs.org/images/logo.png"
         }
     });
 </script>
</body>
```
注意：
```
<div class="app">
	  <a v-bind:href="url">点击</a>
</div>  
```
通常我们可以将v-bind：简写成：
```
<div class="app">
  <a :href="url">点击</a>
</div>
```

##### v-if，v-else
```
<body>
    <div id="app">
        <div v-if="ok">YES</div>
        <div v-else>NO</div>
    </div>
     <script>
         var app = new Vue({
             el:"#app",
             data:{
                 ok:true,
             }
         });
     </script>
</body>
```
##### v-for
1. v-for循环普通数组
    ```
    <body>
        <div id="app">
            <p v-for="(item,index) in list">{{item}}----索引:{{index}}</p>
        </div>
         <script>
             var app = new Vue({
                 el:"#app",
                 data:{
                    list:[1,2,3,4,5],
                 }
             });
         </script>
    </body>
    ```
2. v-for循环对象数组
    ```
    <body>
        <div id="app">
            <p v-for="(user,index) in list">{{user.id}}---{{user.name}}-----索引:{{index}}</p>
        </div>
         <script>
             var app = new Vue({
                 el:"#app",
                 data:{
                    list:[
                        {id:1,name:'张三'},
                        {id:2,name:'李四'},
                        {id:3,name:'王五'}
                    ],
                 }
             });
         </script>
    </body>
    ```
3. v-for循环对象
    ```
    <body>
        <div id="app">
            <p v-for="(val,key,index) in user">值：{{val}}---键：{{key}}-----索引:{{index}}</p>
        </div>
         <script>
             var app = new Vue({
                 el:"#app",
                 data:{
                    user:{
                        name:"张三",
                        age:"18",
                        sex:"男"
                    }
                 }
             });
         </script>
    </body>
    ```

### 3.Vue数据绑定
##### 单向数据绑定
语法：``v-bind:href ="xxx"`` 或简写为 ``:href``
特点：数据只能从 data 流向视图页面。

##### 双向数据绑定
语法：v-mode:value="xxx" 或简写为 v-model="xxx"
特点：数据不仅能从 data 流向视图页面，还能从视图页面流向 data。
注意：v-model 会忽略所有表单元素的 value、checked、selected 特性的初始值而总是将 Vue 实例的数据作为数据来源。应该通过 JavaScript 在组件的 data 选项中声明初始值!
示例：
```
<body>
    <div id="app">
        <input type="text"  v-model="message"/>{{message}}
    </div>
     <script>
         var app = new Vue({
             el:"#app",
             data:{message:'' }
         });
     </script>
</body>
```

### 4.Vue事件处理
可以用 v-on 指令监听 DOM 事件，并在触发时运行一些 JavaScript 代码。v-on 还可以接收一个需要调用的方法名称。
完整示例：
```
<!DOCTYPE html>
<html xmlns:v-on="https://cn.vuejs.org/">
<head lang="en">
    <meta charset="UTF-8">
    <title>事件绑定</title>
    <!--1.引入vue.js-->
    <script src="https://cdn.jsdelivr.net/npm/vue@2.5.21/dist/vue.js"></script>
</head>
<body>
    <div id="app">
       {{count}}
        <!--触发时运行一些 JavaScript 代码--> 
        <button v-on:click="count+=1">点我加1</button>
        <!--触发时调用js方法--> 
        <button v-on:click="sub">点我减1</button>
    </div>
     <script>
         var app = new Vue({
             el:"#app",
             data:{count:1 },
             methods:{
                 sub:function(){
                    this.count-=1;
                 }
             }
         });
     </script>
</body>
</html>
```
注意：
- v-bind可以简写为 ：
- v-on: 可以简写@

### 5.el的两种写法

第一种写法:

```
<script type="text/javascript">
    new Vue({
        el: '#root', //绑定id为root的容器
        data: {
       		//定义数据 
    	}
    })
</script>
```

第二种写法:

```
<script type="text/javascript">
    const vm = new Vue({
        data: {
       		//定义数据 
    	}
    })
    vm.$mount('#root') //绑定id为root的容器
</script>
```

两种方式的区别在于第一种创建Vue对象的时候就要绑定容器；第二种先创建Vue对象，可以做一些其他操作后再绑定容器。

### 6.data的两种写法
data的对象可以用对象式写法和函数式写法:
对象式写法:

```
<script type="text/javascript">
    new Vue({
        el: '#root',
        //定义data对象，然后在其中定义属性
        data: {
       		name:'Nicki Minaj' 
    	}
    })
</script>
```

函数式写法:

```
<script type="text/javascript">
    new Vue({
        el: '#root',
        //定义data函数，然后在返回值中定义属性
        data(){
            return{
                //返回值是定义的数据
                name:'Nicki Minaj' 
            }
        }
    })
</script>
```
注意：
1. 使用组件时，必须使用函数式定义数据。
2. 由 Vue 管理的函数不能写成箭头函数，如果使用箭头函数，则函数中的 `this` 表示的是 window，如果使用普通函数格式，则 `this` 表示 Vue对象。

# 五.Vue组件化开发
### 1.Vue组件化概念
组件(Component)是可复用的 Vue 实例， 把一些公共的模块抽取出来，将其抽出为一个组件进行复用(用来实现局部(特定)功能效果的代码集合(html/css/js/image…..)) 然后写成单独的的工具组件或者页面，在需要的页面中就直接引入即可。
![](/images/17995dd41a5f2b5466b9bb2ae0053941.webp)
例如 页面头部、侧边、内容区，尾部，上传图片，等多个页面要用到一样的就可以做成组件，提高了代码的复用率。如果要使用组件那么有三大步骤:定义组件（创建组件）=>注册组件=>使用组件（写组件标签）
```
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <title>Document</title>
  <!-- 1. 导入Vue包 -->
  <script src="https://cdn.jsdelivr.net/npm/vue@2.5.17/dist/vue.js"></script>
</head>

<body>
  <class class="app">
    <!-- 3、使用组件 -->
    <my-com></my-com>
  </class>
  <script>
    // 1、创建组件构造器
    const myComponent = Vue.extend({
        template: `
          <div>
            <h2>组件标题</h2>
            <p>我是组件中的一个段落内容</p>
          </div>
        `,
      })
      // 2、注册组件，并且定义组件标签的名称
      Vue.component("my-com", myComponent)
      
      //创建vm....
  </script>
</body>
</html>
```

### 2.Vue定义组件（创建组件）
使用 Vue.extend(options) 创建，其中 options 和 new Vue(options) 时传入的 options 几乎一样，但也有点区别:
1. el 不要写，因为最终所有的组件都要经过一个 vm 的管理，由 vm 中的 el 决定服务哪个容器。
2. data 必须写成函数，函数每次都会返回一个新的对象，避免组件被复用时，数据存在引用关系。

定义组件简写方式:
```
const book = Vue.extend(options) 
```
可简写为：
```
const book = options
```

### 3.Vue注册组件
组件需要注册后才可以使用，注册有全局注册和局部注册两种方式。
1.局部注册：靠new Vue的时候传入components选项
2.全局注册：靠Vue.component('组件名'，组件)

##### 全局组件注册
**Vue.component()注册**
直接使用 Vue.component()注册的组件为全局组件，它可以在vue的任何实例当中被使用。 调用Vue.component()是将刚才的组件构造器注册为一个组件，并且给它起一个组件的标签名称。 因此需要传入两个参数：注册组件的标签名、组件构造器。
```
<!DOCTYPE html>
<html>
	<head>
		<title>vue组件测试</title>
		<meta charset="utf-8">
		<script src="https://cdn.jsdelivr.net/npm/vue@2.5.17/dist/vue.js"></script>
	</head>
	<body>
		<div id="app">
			<!-- 组件复用如下 -->
			<button-counter></button-counter>
			<br />
			<br />
			<button-counter></button-counter>
			<br />
			<br />
			<button-counter></button-counter>
		</div>
		<script type="text/javascript">
			// button-counter是组件名，
			    Vue.component('button-counter', {
			       // 和实例对象不一样，这里data不再返回对象，必须要是个函数，而且必须return
			      data: function() {
			        return {
			          count: 0
			        }
			      },
			      template: '<button @click="count++">You clicked me {{ count }} times.</button>'
			    });
			    new Vue({
			      el: '#app'
			    });
		</script>
	</body>
</html>
```
注意：当我们定义 button-counter 组件的时候，data 必须为一个函数，不能是一个对象，比如不能是如下的对象:
```
data: {
  count: 0
};
```
因为每个实例可以维护一份被返回对象的独立拷贝。如果是一个对象的话，那么它每次调用的是共享的实列，因此改变的时候会同时改变值。 官方文档是这么说的：当一个组件被定义时，data必须声明为返回一个初始数据对象的函数，因为组件可能被用来创建多个实列。如果data仍然是一个纯粹的对象，则所有的实列将共享引用同一个数据对象。 通过提供data函数，每次创建一个新实列后，我们能够调用data函数，从而返回初始数据的一个全新副本的数据对象。

**在Vue.extend的配置对象里面注册**
Vue.extend(options); Vue.extend 返回的是一个 "扩展实列构造器"， 不是具体的组件实列， 它一般是通过 Vue.component 来生成组件。
- 调用Vue.extend()创建的是一个组件构造器。
- 通常在创建组件构造器时，传入template代表我们自定义组件的模板。
- 该模板就是在使用到组件的地方，要显示的HTML代码。
```
<!DOCTYPE html>
<html>
	<head>
		<title>vue组件测试</title>
		<meta charset="utf-8">
		<script src="https://cdn.jsdelivr.net/npm/vue@2.5.17/dist/vue.js"></script>
	</head>
	<body>
		<div id="app">
			<!-- 组件复用如下 -->
			<button-counter></button-counter>
			<br />
			<br />
			<button-counter></button-counter>
			<br />
			<br />
			<button-counter></button-counter>
		</div>
		<!-- 全局组件在 id为app2下也能使用的 -->
		<div id="app2">
			<button-counter></button-counter>
		</div>
		<script type="text/javascript">
			var buttonCounter = Vue.extend({
			      name: 'button-counter',
			      data: function() {
			        return {
			          count: 0
			        }
			      },
			      template: '<button @click="count++">You clicked me {{ count }} times.</button>'
			    });
			    /*
			      Vue.component 是用来全局注册组件的方法, 其作用是将通过 Vue.extend 生成的扩展实列构造器注册为一个组件 
			    */
			    Vue.component('button-counter', buttonCounter);
			    // 初始化实列app
			    new Vue({
			      el: '#app'
			    });
			    // 初始化实列app2
			    new Vue({
			      el: '#app2'
			    });
		</script>
	</body>
</html>
```
效果和上面也是一样的。如上可以看到， 全局组件不仅仅在 '#app' 域下可以使用， 还可以在 '#app2' 域下也能使用。这就是全局组件和局部组件的区别。

### 4.局部组件注册
局部组件，就是只能在某个VUE对象内部才能使用的组件，虽然在定义的时候我们只是按照对象的方式在定义，但是当我们将其纳入到VUE对象的 compoments 中后，它就成为了一个Vue实例，只能在引入的Vue实例内部使用。
例如：
```
import HelloWorld from './components/HelloWorld'
export default {
  components: {
      HelloWorld
  }
}
```
区别：全局组件是挂载在 Vue.options.components 下，而局部组件是挂载在 vm.$options.components 下，这也是全局注册的组件能被任意使用的原因。
```
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="UTF-8">
		<title>Title</title>
		<script src="../../js/vue.js"></script>
	</head>
	<body>
		<div id="app">
			<my-button></my-button>
			<my-button></my-button>
			<my-button2></my-button2>
		</div>
		<div id="app1">
			<my-button></my-button>
			<!--在这里不能用 <my-button2></my-button2>-->
		</div>
		<script type="text/javascript">
			const temp = Vue.extend({
				template: `
			                <h2>Welcome to Vue</h2>
			            `
			})
			//全局组件
			Vue.component('myButton', temp);
			const app = new Vue({
				el: "#app",
				data: {},
				//局部组件
				components: {
					myButton2: temp
				}
			})
			const app1 = new Vue({
				el: "#app1",
			})
		</script>
	</body>
</html>
```
局部注册组件
```
<div id="app">
	<child-component></child-component>
</div>
<script type="text/javascript">
	var child = {
	    template: "<h1>我是局部组件</h1>"
	  };
	  new Vue({
	    el: '#app',
	    components: {
	      "child-component": child
	    }
	  })
</script>
```
在浏览器中会被渲染成html代码如下:
```
<div id='app'><h1>我是局部组件</h1></div>
```
如上代码是局部组件的一个列子， 局部组件只能在 id 为 'app' 域下才能使用， 在其他id 下是无法访问的。如下如下代码:
```
<div id="app">
	<child-component></child-component>
</div>
<div id="app2">
	<child-component></child-component>
</div>
<script type="text/javascript">
	var child = {
	    template: "<h1>我是局部组件</h1>"
	  };
	  new Vue({
	    el: '#app',
	    components: {
	      "child-component": child
	    }
	  });
	  new Vue({
	    el: '#app2'
	  })
</script>
```
如上代码， 我们在 id 为 '#app2' 的域下使用 child-component 组件是使用不了的， 并且在控制台中会报错的。因为该组件是局部组件， 只能在 '#app' 域下才能使用。

### 5.引入使用组件（写组件标签）
关于组件标签:
第一种写法：``<book></book>``
第二种写法：``<book/>``
>备注：不用使用脚手架时，<book/>会导致后续组件不能渲染。（多次使用只能渲染第一次的）


关于组件名:
一个单词组成：
- 第一种写法(首字母小写)：book
- 第二种写法(首字母大写)：Book

多个单词组成：
- 第一种写法(kebab-case命名)：my-book
- 第二种写法(CamelCase命名)：MyBook (需要Vue脚手架支持)

备注：
(1).组件名尽可能回避HTML中已有的元素名称，例如：h2、H2都不行。
(2).可以使用name配置项指定组件在开发者工具中呈现的名字。

### 6.非单文件组件和单文件组件
单文件组件（.vue）与非单文件组件（.html）。
##### 非单文件组件
1. 模板编写没有提示。
2. 没有构建过程， 无法将 ES6 转换成 ES5。
3. 不支持组件的 CSS。
4. 真正开发中几乎不用。
##### 单文件组件
一个.vue 文件的组成(3 个部分)
1. 模板页面
```
<template>
    页面模板
</template>
```
2. JS 模块对象
```
<script>
export default {
    data() {return {}}, methods: {}, computed: {}, components: {}
}
</script>
```
3. 样式
```
<style>
    样式定义
</style>
```
App.vue文件，在Vue中，官网叫它做组件，单页面的意思是结构，样式，逻辑代码都写在同一个文件中，当我们引入这个文件后，就相当于引入对应的结构、样式和JS代码，
```
<template>
	<div id="app">
		<img src="./assets/logo.png">
		<router-view></router-view>
	</div>
</template>

<script>
	export default {
	  name: 'app'
	}
</script>

<style>
	#app {
	  font-family: 'Avenir', Helvetica, Arial, sans-serif;
	  -webkit-font-smoothing: antialiased;
	  -moz-osx-font-smoothing: grayscale;
	  text-align: center;
	  color: #2c3e50;
	  margin-top: 60px;
	}
</style>
```
node端之所以能识别.vue文件，是因为前面说的webpack在编译时将.vue文件中的html，js，css都抽出来合成新的单独的文件。

# 六.Vue组件的传值
组件间传值分为以下几种情况的传值：
1. 父子组件的传值。
2. 兄弟组件间的传值。
3. 祖先与后代元素间的传值。
   针对以上情况那么都会有相应的解决方案，如下表所示:

| 需要进行传值的组件关系 | 解决方案 |
| - | - |
| 父 -> 子（祖先 -> 后代） | `props`、`消息总线`、`发布订阅`、`provide/inject` |
| 子 -> 父(后代 -> 祖先) | `消息总线`、`发布订阅`、`$refs`、`事件绑定($on/$emit)` |
| 兄弟组件 | `消息总线`、`发布订阅` |

### 1.使用props进行传值
1. 作用：用于父组件给子组件传递数据
2. 读取方式一: 只指定名称
   ```
   props: ['name', 'age', 'setName']
   ```
类型 可以是下列原生构造函数中的一个：

- String
- Number
- Boolean
- Array
- Object
- Date
- Function
- Symbol

3. 读取方式二: 指定名称和类型
   ```
   props: {
    name: String, age: Number, setNmae: Function
   }
   ```
4. 读取方式三: 指定名称/类型/必要性/默认值
   ```
   props: {
   name: {type: String, required: true, default:xxx}, }
   ```


##### 示例
```
<body>
    <div id="app">
        <!--组件：使用props把值传递给组件-->
        <blog-post v-for="item in items" v-bind:value="item"></blog-post>
    </div>
     <script>
         Vue.component("blog-post",{
             props:['value'],
             template:'<li>{{value}}</li>'
         });
         var app = new Vue({
             el:"#app",
             data:{
                 items:['张三','李四','王五']
             }
         });
     </script>
</body>
```
说明：
v-for=“item in items”：遍历 Vue 实例中定义的名为 items 的数组，并创建同等数量的组件。
v-bind:value=“item”：将遍历的 item 项绑定到组件中 props 定义的名为 value属性上；= 号左边的 value 为 props 定义的属性名，右边的为 item in items 中遍历的 item 项的值。

基本原则
1) 不要在子组件中直接修改父组件的状态数据。
2) 数据在哪， 更新数据的行为(函数)就应该定义在哪。

### 2.组件间通信之vue自定义事件
绑定事件监听
方式一: 通过 v-on 绑定:
```
@click="deleteTodo"
```
方式二: 通过$on() 绑定自定义事件(delete_todo)监听:
```
<TodoHeader ref="xxx"/>
this.$refs.xxx.$on('delete_todo', function (todo) {
this.deleteTodo(todo)
})
```
触发事件:
```
// 触发事件(只能在父组件中接收)
this.$emit(eventName, data)
```
>注意： 此方式只用于子组件向父组件发送消息(数据) 隔代组件或兄弟组件间通信此种方式不合适。

### 3.组件间通信之消息订阅与发布
1. 订阅消息:
    ```
    PubSub.subscribe('msg', function(msg, data){})
    ```
2. 发布消息:
    ```
    PubSub.publish('msg', data)
    ```

>注意：此方式可实现任意关系组件间通信(数据)比如我们订阅一个消息，实现数组的删除操作

##### 示例
```
mounted () {
   // 订阅消息(deleteTodo)
   PubSub.subscribe('deleteTodo', (msg, index) => {
      this.deleteTodo(index)
   })
}

methods: {
   deleteTodo (index) {
      this.todos.splice(index, 1)
   },
}

<button class="btn btn-danger" v-show="isShow" @click="deleteItem">删除</button>
deleteItem () {
   // 发布消息(deleteTodo)
   PubSub.publish('deleteTodo', this.index)
}
```

# 七.Vue网络通信-Axios
### 1.引入axios
- 使用 npm引入:
    ```
    npm install axios
    ```
- 使用 cdn引入:
    ```
    <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
    ```
### 2.axios简介
axios是一个基于 promise 的 HTTP 库， 主要用于：**发送异步请求获取数据**。

常见的方法：
- axios(config)
- axios.get(url, [config])
- axios.post(url, [data])

##### 发送数据config常用参数：

```
{
    url: '请求的服务器',
	method: '请求方式', // 默认是 get
    // GET请求参数
    params: {
    	参数名: 参数值
    },
	// POST请求参数, 如果使用axios.post,则参数在url之后直接书写,不需要该位置传递参数
    data: {
    	参数名: 参数值
    },
	// 响应数据格式,默认json
	responseType: 'json'
}
```

##### 响应数据常用参数：

```
{
    data: {},		//真正的响应数据(响应体)
    status: 200,	//响应状态码
    statusText: 'OK',	 //响应状态描述
    headers: {},	//响应头
    config: {}		//其他配置信息
}
```

### 3.axios发送Get请求

```
var app = new Vue({
    el: "#app",
    data: {
        user: {}
    },
    //当页面加载完毕后
    created() { 
        //发送GET请求axios.get("请求路径",{ config });
       axios.get("请求路径",{
            //get请求参数
            params: {
                name:"zhangsan",
                age:23
            },
            //响应数据格式为"json"
            responseType: 'json'
        }).then(res => {
            //打印响应数据
            console.log(res);
            //把响应数据赋值给Vue中的user属性
            app.user = res.data;
        }).catch(err => {
            //打印响应数据(错误信息)
            console.log(err);
        });
    }
});
```

### 4.axios发送Post请求

```
var app = new Vue({
    el: "#app",
    data: {
        user: {}
    },
    //当页面加载完毕后
    created() { 
        //发送POST请求axios.post("请求路径",{ 参数 });
        axios.post("请求路径",{
                name:"zhangsan",
                age:23
            }).then(res => {
                console.log(res);
                app.user = res.data;
            }).catch(err => {
                console.log(err);
            });
    }
});
```

### 5.Vue跨域问题
##### 跨域问题产生的原因
跨域问题的出现是因为浏览器存在同源策略问题，所谓同源:即两个页面具有相同的协议（protocol：http、https），主机（host）和端口（port），它是浏览器最核心也是最基本的功能，如果没有同源策略，浏览器将会十分危险，
随时都可能受到攻击。当我们请求一个接口获取数据的时候，出现如：“Access-Control-Allow-Origin” 等报错信息即说明该请求跨域。一般跨域问题都是由后端解决,当然通过前端可以解决。
##### Vue中如何解决跨域问题
1. 在vue.config.js中设置如下代码片段

```
module.exports = {
		dev: {
			// Paths    
			assetsSubDirectory: 'static',
			assetsPublicPath: '/',
			proxyTable: {
				// 配置跨域   
				'/api': {
					target: `http://www.baidu.com`,
					//请求后台接口        
					changeOrigin: true,
					// 允许跨域        
					pathRewrite: {
						'^/api': ''
						// 重写请求       
					}
				}
			},
		}
```

2、创捷axioss实例时，将baseUrl设置为 ‘/api’

```
const http = axios.create({
	timeout: 1000 * 1000000,
	withCredentials: true,
	BASE_URL: '/api'
	headers: {
		'Content-Type': 'application/json; charset=utf-8'
	}
})
```

# 八.Vue生命周期
常用的生命周期方法
![](/images/777369c56ba6604fbf993d7e99b51708.webp)
- beforeCreate：此时data、method和$el均没有初始化。
- created：此时data和method初始化完成，但是DOM节点并没有挂载。
- beforeMount：编译模板，并且将此时在el上挂载一个虚拟的DOM节点。
- mounted：编译模板，且将真实的DOM节点挂载在el上，可做数据请求。
- beforeUpdate：在数据有更新时，进入此钩子函数，虚拟DOM被重新创建。
- updated：数据更新完成时，进入此钩子函数。
- beforeDestory：组件销毁前调用，移除watchers、子组件和事件等。
- destoryed：组件销毁后调用。

```
<template>
  <div>
    <div class="label-head">
      <label>生命周期详解</label>
    </div>
    <div :data="count">{{count}}</div>
    <p>
      <button @click="add">添加</button>
    </p>
  </div>
</template>
<script>
export default {
  data() {
    return {
      count: "",
      filter: "all",
      states: ["all", "active", "completed"]
    };
  },
  methods: {
    add() {
      this.count++;
    }
  },
  beforeCreate() {
    console.log("=========" + "beforeCreated:初始化之前" + "======");
    console.log(this.$el);
    console.log(this.$data);
    console.log(this.filter);
  },
  created() {
    console.log("==========" + "created：创建完成" + "===========");
    console.log(this.$el);
    console.log(this.$data);
    console.log(this.filter);
  },
  beforeMount() {
    console.log("==========" + "beforeMount：挂载之前" + "=======");
    console.log(this.$el);
    console.log(this.$data);
    console.log(this.filter);
  },
  mounted() {
    console.log("==========" + "mounted：被挂载之后" + "==========");
    console.log(this.$el);
    console.log(this.$data);
    console.log(this.filter);
  },
  beforeUpdate() {
    console.log("========" + "beforeUpdate：数据更新前" + "========");
    console.log(this.$el);
    console.log(this.$data);
    console.log(this.filter);
  },
  updated() {
    console.log("========" + "updated：被更新之后" + "============");
    console.log(this.$el);
    console.log(this.$data);
    console.log(this.filter);
  },
  beforeDestroy() {
    console.log("=========" + "beforeDestroy：销毁之前" + "========");
    console.log(this.$el);
    console.log(this.$data);
    console.log(this.filter);
  },
  destroyed() {
    console.log("==========" + "destroyed：销毁之后" + "===========");
    console.log(this.$el);
    console.log(this.$data);
    console.log(this.filter);
  },
  activated() {
    console.log("");
  },
  deactivated() {
    console.log("");
  }
};
</script>
<style scoped>
.label-head {
  text-align: center;
  font-size: 40px;
}
</style>
```

# 九.Vue项目工程
### 1.单页面应用和多页面应用
**SPA单页面应用（SinglePage Web Application）** ，指只有一个主页面的应用（一个html页面），一开始只需要加载一次js、css的相关资源。所有内容都包含在主页面，对每一个功能模块组件化。单页应用跳转，就是切换相关组件，仅仅刷新局部资源。
**MPA多页面应用（MultiPage Application）** ，指有多个独立页面的应用（多个html页面），每个页面必须重复加载js、css等相关资源。多页应用跳转，需要整页资源刷新。
|-|SPA应用|MPA应用|
|-|-|-|
|刷新方式|相关组件切换，页面局部刷新或更改|整页刷新|
|路由模式|可以使用hash，也可以使用history|普通链接跳转|
|用户体验|页面片段间时间的切换快，用户体验良好，当初次加载文件过多时，需要做相关调优|页面切换加载缓慢，流畅度不够，用户体验比较差，尤其网速慢的时候|
|转场动画|容易实现转场动画|MPA：无法实现转场动画|
|数据传递|容易实现数据传递，方法有很多（通过路由带参数传值，Vuex传值等等）|依赖url传参，cookie，本地存储|
|搜索引擎优化（SEO）|需要单独方案，实现较为困难，不利于SEO检索，可利用服务器端渲染（SSR）优化|实现方法容易|
|使用范围|高要求的体验度，追求界面流畅的应用|适用于追求高度支持搜索引擎的应用|
|开发成本|较高，长需要借助专业的框架|较低，但也页面代码重复的多|
|维护成本|相对容易| 相对复杂|
|结构|一个主页面+许多模块的组件|许多完整的页面|
|资源文件|组件公用的资源只需要加载一次|每个页面都需要自己加载公用的资源|
### 2.使用Vue脚手架方式生成工程（推荐使用）
Vue脚手架指的是vue-cli，它是一个专门为单页面应用快速搭建繁杂的脚手架，它可以轻松的创建新的应用程序而且可用于自动生成vue和webpack的项目模板。 利用vue-cli脚手架来构建Vue项目需要先安装Node.js和NPM环境。
##### 安装vue-cli
vue-cli是官方提供的项目脚手架，用来进行项目构建等操作。
安装命令
```
cnpm install -g @vue/cli
```
验证安装
```
vue --version
@vue/cli 4.5.8
```
##### 创建Vue项目工程
```
vue create hello-world
```
![](/images/62bf2459d73cb295110ae338bff90d75.webp)
之后我们看到一个hello-world的文件夹，里边包括教授叫默认生成的一些配置和App.vue，main.js等程序文件。
##### 运行Vue项目工程
cd到hello-world文件夹中，运行如下命令启动一个本地Node服务器来运行Vue项目
```
npm run serve
```
之后会启动对应的服务，通过地址和端口访问，就能看到默认的页面。

##### Vue项目部署支持
既然提到了部署，默认的部署使用npm/cnpm进行，如下命令，输出内容在/dist目录。
```
npm run build
```
可以使用参数来设置，得到符合不同需要的编译结果。之后即可以将打包的文件部署到服务器上。

### 3.Vue项目工程目录结构
模板项目的结构
├── node_modules
├── public
│ ├── favicon.ico: 页签图标
│ └── index.html: 主页面
├── src
│ ├── assets: 存放静态资源
│ │ └── logo.png
│ │── component: 存放组件
│ │ └── HelloWorld.vue
│ │── App.vue: 汇总所有组件
│ │── main.js: 入口文件
├── .gitignore: git 版本管制忽略的配置
├── babel.config.js: babel 的配置文件
├── package.json: 应用包配置文件
├── README.md: 应用描述文件
├── package-lock.json：包版本控制文件

- .eslintrc.js: 这个是 eslint 的配置文件，可以通过它来管理你的校验规则。
- babel.config.js: 这个是 Babel 的配置文件，可以在开发中使用 JavaScript 的新特性，并且将其转换为在生产环境中可以跨浏览器运行的旧语法代码。你也可以在这个里配置额外的 babel 插件。
- .browserslistrc: 这个是 Browserslist 的配置文件，可以通过它来控制需要对哪些浏览器进行支持和优化。
- public: 这个目录包含一些在 Webpack 编译过程中没有加工处理过的文件（有一个例外：index.html 会有一些处理）。
    - favicon.ico: 这个是项目的图标，当前就是一个 Vue 的 logo。
    - index.html: 这是应用的模板文件，Vue 应用会通过这个 HTML 页面来运行，也可以通过 lodash 这种模板语法在这个文件里插值。
      注意：这个不是负责管理页面最终展示的模板，而是管理 Vue 应用之外的静态 HTML 文件，一般只有在用到一些高级功能的时候才会修改这个文件。
- src: 这个是 Vue 应用的核心代码目录
    - main.js：这是应用的入口文件。目前它会初始化 Vue 应用并且制定将应用挂载到  index.html 文件中的哪个 HTML 元素上。通常还会做一些注册全局组件或者添额外的 Vue 库的操作。
    - App.vue：这是 Vue 应用的根节点组件，往下看可以了解更多关注 Vue 组件的信息。
    - components：这是用来存放自定义组件的目录，目前里面会有一个示例组件。
    - assets：这个目录用来存放像 CSS 、图片这种静态资源，但是因为它们属于代码目录下，所以可以用 webpack 来操作和处理。意思就是你可以使用一些预处理比如 Sass/SCSS 或者 Stylus。

#### 4.组件的分类
一般来说，组件大致可以分为三类：
- 页面级别的组件。
- 业务上可复用的基础组件。
- 与业务无关的独立组件。
##### 页面级别的组件
页面级别的组件，通常是pages目录下的.vue组件，是组成整个项目的一个大的页面。一般不会有对外的接口。我们通常开发时，主要就是编写这种组件。如下所示：pages下面的Home.vue(主页)和About.vue(关于我们)等都是一个独立的页面，也是一个独立的组件。
```
pages
├─ About.vue
└─ Home.vue
```
##### 业务上可复用的基础组件
这一类组件通常是在业务中被各个页面复用的组件，这一类组件通常都写到components目录下，然后通过import在各个页面中使用。这一类组件通常是实现某个功能，比如外卖中各个页面都会使用到的评分系统。这个部分就可以实现评分功能，可以写成一个独立的业务组件。比如下面的components中的Star.vue就是一个业务组件。这一类组件的编写通常涉及到组件常用的props，slot和自定义事件等。
```
components
└─ Star.vue
```
##### 与业务无关的独立组件
这一类组件通常是与业务功能无关的独立组件。这类组件通常是作为基础组件，在各个业务组件或者页面组件中被使用。目前市面上比较流行的ElementUI和iview等中包含的组件都是独立组件。如果是自己定义的独立组件，比如富文本编辑器等，通常写在utils目录中。

# 十.Vue路由
### 1.Vue路由入门使用
Vue Router 是 [Vue.js](http://cn.vuejs.org/) 官方的路由管理器。它和 Vue.js 的核心深度集成，让构建单页面应用变得易如反掌。

要在项目中使用 `vue-router` 有四个步骤:
1. 引入 `vue-router` 插件。
2. 使用插件。
3. 创建路由实例并配置路由信息。
4. 将路由实例添加到Vue的实例中。

**main.js**
```
// 引入 vue-router
import VueRouter from 'vue-router'
import Home from './views/Home'
import About from './views/About'

// 使用 VueRouter 插件
Vue.use(VueRouter)

// 添加路由信息
const router = new VueRouter({
    routes: [
        { path: '/', redirect: '/home', },
        { path: '/home', component: Home },
        { path: '/about', component: About },
    ]
})

new Vue({
    router,  // 纳入到 Vue 的实例中
    render: h => h(App),
}).$mount('#app')
```

**App.vue**

```html has-numbering
<template>
    <div>
        <ul>
            <li>
                <router-link to="/home">Home</router-link>
            </li>
            <li>
                <router-link to="/about">About</router-link>
            </li>
        </ul>
        <router-view></router-view>
    </div>
</template>
```

### 2.router-link的参数
`<router-link>` 有几个重要的参数:
- `active-class` 当前激活的路由的样式。
- `tag` 使用指定的标签替换默认的 a 标签。
- `exact-active-class` 精确匹配路由。
- `replace` 不保存当前的路由信息到历史记录中。
- `event` 触发路由的事件，默认是点击事件。

### 3.编程式路由
除了使用 `<router-link>` 创建 a 标签来定义导航链接，我们还可以借助 router 的实例方法，通过编写代码来实现，在 Vue 实例内部，可以通过 `$router` 访问路由实例，通过调用 `this.$router.push`，它等同于 `<router-link to="" />`，编程式路由对应着如下几个方法：
- push() 请求到某个路径
- replace() 请求到某个路径，不会像history中添加新的记录
- go(n) 前进或者后退，不常用

```
goto(p, n) {
    /**
    * 通过路径的方式实现路由的跳转，catch(() => {}) 主要的目的是为了不出现当
    * 用户点击重复的路由而在浏览器端出现的错误
    */
    // this.$router.push(p).catch(() => { })

    // 也可以通过组件的名字实现跳转
    // this.$router.push({name: n}).catch(() => { })

    // 通过组件的名字实现页面的跳转，但是不保存历史记录
    this.$router.replace({ name: n }).catch(() => { })
}
```

### 4.路由的嵌套

实际生活中的应用界面，通常由多层嵌套的组件组合而成，通过在某个父级路由下添加 `children` 属性来包含多个子路由信息。

```
const router = new VueRouter({
    routes: [
        { path: '/', component: Index, name: 'index' },
        {
            path: '/home',
            component: Home,
            name: 'home',
            // 添加子路由信息
            children: [
                { path: '', redirect: 'user' },
                { path: 'student', component: Student },
                { path: 'user', component: User }
            ]
        },
        { path: '/about', component: About, name: 'about' },
    ]
})
```

### 5.参数的传递
当从一个路由跳转到另外一个路由的时候，我们往往需要携带参数，例如查询某个用户的详情信息等。

#### 动态路由传参
在 router 的配置中，我们将 `path` 的值是写固定写死的，然后在有些场景下path是可以是多样化的，例如要查询 id 为某个值的详细信息，id是变化的，那么就需要用到动态路由，其语法非常的简单，如下所示:

```
// ---------------------------路由配置-------------------------------
{ path: 'detail/:id', component: Detail, name: 'about-detail' }

// ---------------------------路由跳转-------------------------------
goto(n) {
    // 如下两行代码，意思是一样的，如果不写，默认就是path
    // this.$router.push(`/about/detail/${n}`).catch(() => { })
    // this.$router.push({ path: `/about/detail/${n}` }).catch(() => { })

    // 使用params参数的方式，必须使用组件名
    this.$router.push({ name: 'about-detail', params: { id: n } })
}

// ----------------------------页面取值-------------------------------
data() {
    return {
    	id: ''
    }
},
created() {
	this.id = this.$route.params.id
}
```

对于上面这种方式，官方更加推荐使用 `props` 的方式来取值，这样就实现了取值的方式就实现了与 $route的解耦。

```
// ---------------------------路由配置-------------------------------
{ path: 'detail/:id', component: Detail, name: 'about-detail',props: true }

// ---------------------------路由跳转-------------------------------
goto(n) {
    // 如下两行代码，意思是一样的，如果不写，默认就是path
    // this.$router.push(`/about/detail/${n}`).catch(() => { })
    // this.$router.push({ path: `/about/detail/${n}` }).catch(() => { })

    // 使用params参数的方式，必须使用组件名
    this.$router.push({ name: 'about-detail', params: { id: n } })
}

// ----------------------------页面取值-------------------------------
export default {
	// props中的值要与路由配置中的id对应
	props: ['id']
}
```

##### query传参
query传参其实是将参数携带在url地址中

```
// ---------------------------路由配置-------------------------------
{ path: 'detail', component: Detail, name: 'about-detail'}

// ---------------------------路由跳转-------------------------------
goto(n) {
    // 可以在路径中直接携带
    // this.$router.push({ path: `/about/detail?id=${n}` })

    this.$router.push({
        //path: '/about/detail',  
        // 可以为路径也可以是名字
        name: 'about-detail',
        query: { id: n }
    })
}

// ----------------------------组件中取值-------------------------------
created() {
    this.id = this.$route.query.id
}

```

##### 定义参数

定义参数就是在就路由配置文件中写的固定的数据，可以使用 `meta` 和 `props` 来携带

##### 面临的问题

当用户去切换数据的时候，由于组件的复用（也就是同一个路由的时候，组件并不会销毁），就无法获取用户传递的值。可以使用 `watch` 和 `beforeRouterUpdate` 两种方式来实现数据的获取。

```
// watch 的方式实现数据切换的时候，参数的获取
watch: {
    // 获取直接监听 $route 也可以
    '$route.params': function (newVal) {
    	this.id = newVal.id
    }
}

// ----------------------使用beforeRouterUpdate的方式获取----------------
// to表示到哪里去，from从哪里来，next是个函数，表示接着往下走
beforeRouteUpdate(to, from, next) {
    this.id = to.params.id
    next()  // 一定要调用 next() 方法
}

```

### 6.路由守卫

路由守卫，就是路由变化的回调钩子函数，可以在这些函数中判定来进行一些流程的控制、权限的验证等等的工作。路由守卫有组件路由守卫和全局路由守卫。

##### 组件路由守卫
组件路由守卫映射到几个组件生命周期函数：
-  `beforeRouteEnter` 当路由准备进入组件，`此时组件还没有被创建(实例的生命周期还没有开始)`，该方法就已经执行。我们可在此处判断用户是否可以进入该页面。
-  `beforeRouteUpdate`，当在页面中更新路由的时候，该方法会被调用了，该方法使用比较的局限，就是当同一个组件下，实现路由切换。
-  `beforeRouteLeave` ，当离开页面即将进入下一个路由的时候，该方法被调用，了解。

`注意上面三个方法都需要调用 next() 方法实现流程的继续`

```
// 进入到对应的路由还没到达组件
beforeRouteEnter(to, from, next) {
    console.log('进入路由');
    next()
},
// 路由更新
beforeRouteUpdate(to, from, next) {
    console.log('更新路由');
    next()
},
// 路由退出
beforeRouteLeave(to, from, next) {
    console.log('退出');
    next()
}


```

##### 全局路由守卫(重点)
全局路由守卫是所有的路由都会执行的钩子函数，在 VueRouter 的实例中进行添加，最常用的方法为：

`beforeEach`: 在路由实例中找到对应的路由就执行。

```
router.beforeEach((to, from, next) => {
    console.log('全局路由守卫');
    next()
})
```

# 十一.使用Vuex进行状态管理
Vuex 是实现组件全局状态（数据）管理的一种机制，可以方便的实现组件之间数据的共享。

### 1.使用 Vuex 统一管理状态的好处
Vuex能够在Vuex 中集中管理共享的数据，易于后期开发和维护 ，Vuex能够高效的实现组件之间的数据共享，提高开发效率，存储在Vuex中的数据都是响应式的，能够实时保持数据与页面的同步一般情况下，只有组件之间共享的数据，才有必要存储到Vuex中，对于组件中的私有数据，依旧存储在组件自身的data中即可。

### 2.Vuex 的使用
##### 安装 Vuex 依赖包
```
npm install vuex --save
```
##### 导入Vuex 包
```
import Vuex from 'vuex'
Vue.use(Vuex)
```
##### 创建 store 对象
```
const store = new Vuex.store({
// state 中存放的就是全局共享的数据
    state: {
        count: 0
    }
})
```
##### 将 store 对象挂在到 vue 实例中
```
new Vue({
	el: '#app',
	render: h => h(app),
	router,
	// 将创建的共享数据对象，挂在到 Vue 全局实例中
	// 所有的组件，就可以直接从 store 中获取全局的数据了
	store,
})
```
### 3.Vuex 的核心概念
- state
  对象类型，类似于实例的 data属性，存放数据
- getters
  对象类型，类似于实例的计算属性 computed
- mutations
  对象类型，类似于实例的 methods，但是不能处理异步方法
- actions
  对象类型，类似于实例的 methods，可以处理异步方法
- modules
  对象类型，当state内容比较多时，通过该属性分割成小模块，每个模块都拥有自己的 state、mutation、action、getter
#####  State
State 提供唯一的公共数据源，所有共享的数据都要通义放到 Store 的 State 中进行存储

// 创建store数据源，提供唯一公共数据
```
const store = new Vuex.Store({
	state: {
		count: 0
	}
})
```

### 4.getter
Vuex 允许我们在 store 中定义“getter”（可以认为是 store 的计算属性）。就像计算属性一样，getter 的返回值会根据它的依赖被缓存起来，且只有当它的依赖值发生了改变才会被重新计算。
意思就是当对state里面的值进行一些比较复杂的运算时，可以调用这个属性，在getter里面进行计算并返回计算后的值。
比如：

```
getters: {
  doneTodos: state => {
      return state.todos.filter(todo => todo.done)
    }
  }
```

此计算会返回过滤后的token值

Getter 会暴露为 store.getters 对象，你可以以属性的形式访问这些值：

这里表示当你注册好了vuex时，你可以在组件中访问getter，并取到计算后的state值。比如：

```
store.getters.doneTodos // [{ id: 1, text: '...', done: true }]
```

### 5.mutation

更改 Vuex 的 store 中的状态的唯一方法是提交 mutation。Vuex 中的 mutation 非常类似于事件：每个 mutation 都有一个字符串的 事件类型 (type) 和 一个 回调函数 (handler)。

***注意：***改变状态管理器中的值，唯一的方法就是利用mutation，比如

```
mutations: {
    increment (state) {
      // 变更状态
      state.count++
    }
  }
```

然后我们在组件中调用这个方法

```
store.commit('increment')
```

此时相当于执行了increment方法，将count加1

### 6.action
Action 类似于 mutation，不同在于：
- Action 提交的是 mutation，而不是直接变更状态。
- Action 可以包含任意异步操作。

下面是一个简单的实例

```
const store = new Vuex.Store({
  state: {
    count: 0
  },
  mutations: {
    increment (state) {
      state.count++
    }
  },
  actions: {
	    incrementAsync ({ commit }) {
	    setTimeout(() => {
	      commit('increment')
	    }, 1000)
	  }
  }
})
```

***注意*** *Action 通过 store.dispatch 方法触发：*

在组件中使用：

```
store.dispatch('incrementAsync', {
  amount: 10
})
```

***我们可以在 action 内部执行异步操作：***

### 7.module
由于使用单一状态树，应用的所有状态会集中到一个比较大的对象。当应用变得非常复杂时，store 对象就有可能变得相当臃肿。
为了解决以上问题，Vuex 允许我们将 store 分割成模块（module）。每个模块拥有自己的 state、mutation、action、getter、甚至是嵌套子模块——从上至下进行同样方式的分割：

像这样：

```
const moduleA = {
  state: { ... },
  mutations: { ... },
  actions: { ... },
  getters: { ... }
}

const moduleB = {
  state: { ... },
  mutations: { ... },
  actions: { ... }
}

const store = new Vuex.Store({
  modules: {
    a: moduleA,
    b: moduleB
  }
})

store.state.a // -> moduleA 的状态
store.state.b // -> moduleB 的状态
```

# 十二.vue拓展
- vue-cli: vue 脚手架
- vue-resource(axios): ajax 请求
- vue-router: 路由
- vuex: 状态管理
- vue-lazyload: 图片懒加载
- vue-scroller: 页面滑动相关
- mint-ui: 基于 vue 的 UI 组件库(移动端)
- element-ui: 基于 vue 的 UI 组件库(PC 端)

参考资料:
[Vue教程语雀](https://www.yuque.com/cessstudy/kak11d/pevvin)
[Vue教程有道云](https://note.youdao.com/ynoteshare/index.html?id=5a9cd6d6c0234679ed6a1c02e04ca52d&type=note&_time=1648606410966)
[Vue教程Github](https://github.com/Panyue-genkiyo/vue-advance)
[Vue 组件化开发](https://cloud.tencent.com/developer/article/1707915)
[vue系列---Vue组件化的实现原理（八）](https://www.cnblogs.com/tugenhua0707/p/11761280.html)
[vue全套教程(实操)](https://blog.csdn.net/beixishuo/article/details/104870999)
[vue超详细教程，手把手教你完成vue项目](https://blog.csdn.net/sylvia_lily/article/details/118739460)
[Vue之组件](https://www.cnblogs.com/lxfpy/p/11045218.html)
[Vue (9) — 模块与组件、非单文件组件、单文件组件](https://blog.csdn.net/m0_59897687/article/details/121858189)
[vue组件化编程](https://blog.csdn.net/fy_java1995/article/details/110918284)
[手把手教你使用Vuex，猴子都能看懂的教程](https://tehub.com/a/3EvY5cOxsu)