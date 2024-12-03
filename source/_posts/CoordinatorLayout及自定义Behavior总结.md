---
title: CoordinatorLayout及自定义Behavior总结
---

# 一. CoordinatorLayout
CoordinatorLayout继承自viewgroup，但是使用类似于framLayout，有层次结构，后面的布局会覆盖在前面的布局之上。它可以``监听子控件的各种事件，协调child之间的联动``。**CoordinatorLayout主要依靠Behavior来进行协调的**。在CoordinatorLayout布局内部，每个child都必须带一个Behavior（其实不携带也可以，不携带就不能被协调），CoordinatorLayout就会根据每个child所携带的Behavior信息进行协调联动。 也就是说CoordinatorLayout是用来协调其子view们之间动作的一个父view，而Behavior就是用来给CoordinatorLayout的子view们实现协调交互的。 
#  二. AppBarLayout
AppBarLayout 继承自LinearLayout，子控件默认为竖直方向排列显示。给AppBarLayout子View配置一个Behavior。而正是这个 Behavior，使得它能够响应依赖对象的位置变化或者是 CoordinatorLayout 中产生的嵌套滑动事件，然后根据特定的规则去和滑动内部的子 View进行联动。
AppbarLayout 需要作为一个 CoordinatorLayout 的直接子 View，才能实现联动效果。否则它在使用时与普通的 LinearLayout 无异。 并且AppBarLayou它本身与 Toolbar 没有直接的关系的，AppBarLayout 内部的子 View 不一定非要是 Toolbar，它可以是任何 View。 AppBarLayout 需要和一个独立的兄弟 View 配合使用，这个兄弟 View 是一个嵌套滑动组件，只有这样 AppBarLayout 才能知道什么时候开始滑动。
它们之间关系的绑定通过给嵌套滑动的组件设立特定的 Behavior，那就是 **AppBarLayout.ScrollingViewBehavior**。AppBarLayout的子控件可以通过在代码里调用setScrollFlags(int)或者在XML里app:layout_scrollFlags来设置它的滑动协调效果。
layout_scrollFlags 可以使用的flag有：
- scroll
- enterAlways
- enterAlwaysCollapsed
- exitUntilCollapsed
- snap
### 1.scroll
Child View将伴随着滚动事件而滚出或滚进屏幕。``如果使用了其他值，必定要使用这个值才能起作用；如果在这个child View前面的任何其他Child View没有设置这个值，那么该Child View的设置将失去作用``。
示例：
```
<androidx.coordinatorlayout.widget.CoordinatorLayout
        android:layout_width="match_parent"
        android:layout_height="match_parent">

        <com.google.android.material.appbar.AppBarLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content">

            <TextView
                android:id="@+id/txt_head"
                android:layout_width="match_parent"
                android:layout_height="200dp"
                android:gravity="center"
                android:minHeight="50dp"
                android:text="头部界面"
                app:layout_scrollFlags="scroll"
                android:textColor="@color/white"
                android:textSize="20sp"
                android:textStyle="bold" />
        </com.google.android.material.appbar.AppBarLayout>

        <androidx.core.widget.NestedScrollView
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            app:layout_behavior="com.google.android.material.appbar.AppBarLayout$ScrollingViewBehavior">

            <TextView
                android:id="@+id/txt_content_text"
                android:layout_width="wrap_content"
                android:text="@string/centent"
                android:layout_height="match_parent" />

        </androidx.core.widget.NestedScrollView>

</androidx.coordinatorlayout.widget.CoordinatorLayout>
```

对应效果图：
![](https://upload-images.jianshu.io/upload_images/3067896-4e37bdb933cec7f0.gif?imageMogr2/auto-orient/strip)

### 2.scroll|enterAlways
快速返回模式。其实就是向下滚动时Scrolling View和Child View之间的滚动优先级问题。对比`scroll`和`scroll | enterAlways`设置，发生向下滚动事件时，前者优先滚动Scrolling View，后者优先滚动Child View，当优先滚动的一方已经全部滚进屏幕之后，另一方才开始滚动。
示例：

```
...
app:layout_scrollFlags="scroll|enterAlways"
...

```
对应效果图：
![动画1.gif](https://upload-images.jianshu.io/upload_images/3067896-0f2d3189498eff57.gif?imageMogr2/auto-orient/strip)

### 3.scroll|enterAlways|enterAlwaysCollapsed
enterAlways的附加值。这里涉及到Child View的高度和最小高度，向下滚动时，Child View先向下滚动最小高度值，然后Scrolling View开始滚动，到达边界时，Child View再向下滚动，直至显示完全。
示例：

```
...
android:layout_height="@dimen/dp_200"
android:minHeight="@dimen/dp_56"
...
app:layout_scrollFlags="scroll|enterAlways|enterAlwaysCollapsed"
...

```
对应效果图：
![动画2.gif](https://upload-images.jianshu.io/upload_images/3067896-02f43f1febbf97bf.gif?imageMogr2/auto-orient/strip)

### 4.exitUntilCollapsed
这里也涉及到最小高度。发生向上滚动事件时，Child View向上滚动退出直至最小高度，然后Scrolling View开始滚动。也就是，Child View不会完全退出屏幕。
示例：

```
...
android:layout_height="@dimen/dp_200"
android:minHeight="@dimen/dp_56"
...
app:layout_scrollFlags="scroll|exitUntilCollapsed"
...

```

对应效果图：

![image](https://upload-images.jianshu.io/upload_images/1094967-6f683857f6d567ca.gif?imageMogr2/auto-orient/strip|imageView2/2/w/338/format/webp)

### 5.scroll|snap
简单理解，就是Child View滚动比例的一个吸附效果。也就是说，Child View不会存在局部显示的情况，滚动Child View的部分高度，当我们松开手指时，Child View要么向上全部滚出屏幕，要么向下全部滚进屏幕， 有点类似ViewPager的左右滑动。

示例：

```
...
android:layout_height="@dimen/dp_200"
...
app:layout_scrollFlags="scroll|snap"
...

```

对应效果图：
![动画3.gif](https://upload-images.jianshu.io/upload_images/3067896-09843347fd437dbf.gif?imageMogr2/auto-orient/strip)

# 三.CollapsingToolbarLayout
CollapsingToolbarLayout继承自FrameLayout，作用是包装Toolbar实现折叠标题栏，给它设置layout_scrollFlags， 它可以控制包含在CollapsingToolbarLayout中的控件(如：ImageView、Toolbar)在响应layout_behavior事件时作出相应的scrollFlags滚动事件(移除屏幕或固定在屏幕顶端)， 因此如要实现折叠等效果则``必须作为AppBarLayout 的子类``，才能发挥出效果。CollapsingToolbarLayout有两种状态分别是 展开(Expanded) 和 折叠(Collapsed)。它内部可以有多个子元素，通常在子布局中放一个Toolbar，而不同子元素也会有不同的表现。这些子元素可以添加layout_collapseMode标志位进而产生不同的行为（折叠模式）。
### 1.折叠模式(layout_collapseMode)
CollapsingToolbarLayout的子布局有3种折叠模式

- COLLAPSE_MODE_OFF (none) ：这个是默认属性，布局将正常显示，没有折叠的行为。

- COLLAPSE_MODE_PIN (pin) ：view固定在适当位置，直到达到CollapsingToolbarLayout底部。就相当于View被整个推上去或者拉下来的效果。（会随着滚动固定在顶部）
![动画4.gif](https://upload-images.jianshu.io/upload_images/3067896-03b48f8f455e7da7.gif?imageMogr2/auto-orient/strip)
可以看到，整个图片就像是更随下面的RecycleView一样，直到到了折叠态，才分开。

- COLLAPSE_MODE_PARALLAX (parallax) ：view将以视差方式滚动，可以结合另外一个属性layout_collapseParallaxMultiplier(设置视差因子，值为0~1)搭配使用。
![动画5.gif](https://upload-images.jianshu.io/upload_images/3067896-fe923bf7dd7d476e.gif?imageMogr2/auto-orient/strip)
上面大图部分的父VIew是CollapsingToolbarLayout，对ImageView设置了parallax，效果就是上下各一半的减少，最后显示的位置是图片的正中央。

### 2.视差因子(layout_collapseParallaxMultiplier)
layout_collapseMode设置为parallax才生效。不设置视差系数，默认为0.5，就是收缩时上下各自收缩一半。视差系数决定收缩比例。

### 3.CollapsingToolbarLayout属性设置
- app:contentScrim ="@color/colorPrimary"   #设置折叠时toolbar的背景颜色，默认是colorPrimary的色值
- app:statusBarScrim="@color/colorAccent"   #设置折叠时状态栏的颜色 ，默认是colorPrimaryDark的色值
- app:titleEnabled="true"                   #是否显示标题
- app:title="CollapsingToolbarLayout"       #标题内容
- app:expandedTitleGravity="left|bottom"    #展开后Title的位置
- app:collapsedTitleGravity="left"          #折叠后Title的位置
- app:scrimAnimationDuration="1200"         #CollapsingToolbarLayout收缩时颜色变化的持续时间
- app:scrimVisibleHeightTrigger="150dp"     #颜色从可见高度的什么位置开始变化
- expandedTitleMargin*                      #扩展态标题的Margin。注意与expandedTitleGravity可能冲突
- expandedTitleMarginStart                  #展开的时候title与左边的距离
- app:collapsedTitleTextAppearance          #折叠状态标题文字的样式
- app:expandedTitleTextAppearance           #展开状态标题文字的样式
- app:toolbarId="@id/toolbar"               #在折叠的时候 显示的toolbar

>注意事项:
Toolbar别设置标题，设置标题也不会起作用。Toolbar的layout_height不要设置成wrap_content，否则会导致CollapsingToolbarLayout的标题就不出现。必须要设置成attr/actionBarSize**或者具体的dp值就没问题。


# 四.Behavior介绍
Behavior是CoordinatorLayout用来和各个子View通信用的代理类，用来协调CoordinatorLayout内部Child Views之间的交互行为，但Behavior只有是用在CoordinatorLayout的直接子View上才有意义。 本质上来说Behavior就是一个应用于View之间的观察者模式，一个View观察另一个View的变化而进行变化。在Behavior中，被观察View 也就是事件源被称为denpendcy，而观察View，则被称为child。
### 1.Behavior构造函数
Behavior是CoordinatorLayout的一个抽象内部类:
```
public abstract static class Behavior<V extends View> {
      public Behavior() {
      
      }
      public Behavior(Context context, AttributeSet attrs) {
      
      }
      ...
}
```
Behavior是CoordinatorLayout的一个内部泛型抽象类。内部类中指定的view类型规定了哪种类型的view的可以使用才Behavior。因此，如果没有特殊需求，直接指定view为View就行了。
>带有参数的这个构造必须要重载，因为在CoordinatorLayout里利用反射去获取这个Behavior的时候就是拿的这个构造。如果不重载会导致错误。

### 2.Behavior方法种类
- onInterceptTouchEvent()：    #是否拦截触摸事件
- onTouchEvent()：             #处理触摸事件
- layoutDependsOn()：          #确定使用Behavior的View要依赖的View的类型
- onDependentViewChanged()：   #当被依赖的View状态改变时回调
- onDependentViewRemoved()：   #当被依赖的View移除时回调
- onMeasureChild()：           #测量使用Behavior的View尺寸
- onLayoutChild()：            #确定使用Behavior的View位置
- onStartNestedScroll()：      #嵌套滑动开始（ACTION_DOWN），确定Behavior是否要监听此次事件
- onStopNestedScroll()：       #嵌套滑动结束（ACTION_UP或ACTION_CANCEL）
- onNestedScroll()：           #嵌套滑动进行中，要监听的子 View的滑动事件已经被消费
- onNestedPreScroll()：        #嵌套滑动进行中，要监听的子 View将要滑动，滑动事件即将被消费（但最终被谁消费，可以通过代码控制）
- onNestedFling()：            #要监听的子 View在快速滑动中
- onNestedPreFling()：         #要监听的子View即将快速滑动

### 3.Behavior方法详解
```
/**
 * 表示是否给应用了Behavior 的View 指定一个依赖的布局，通常，当依赖的View 布局发生变化时
 * 不管被被依赖View 的顺序怎样，被依赖的View也会重新布局
 * @param parent
 * @param child 绑定behavior 的View
 * @param dependency   依赖的view
 * @return 如果child 是依赖的指定的View 返回true,否则返回false
 */
@Override
public boolean layoutDependsOn(CoordinatorLayout parent, View child, View dependency) {
    return super.layoutDependsOn(parent, child, dependency);
}

/**
 * 当被依赖的View 状态（如：位置、大小）发生变化时，这个方法被调用
 * @param parent
 * @param child
 * @param dependency
 * @return
 */
@Override
public boolean onDependentViewChanged(CoordinatorLayout parent, View child, View dependency) {
    return super.onDependentViewChanged(parent, child, dependency);
}

/**
 *  当coordinatorLayout 的子View试图开始嵌套滑动的时候被调用。当返回值为true的时候表明
 *  coordinatorLayout 充当nested scroll parent 处理这次滑动，需要注意的是只有当返回值为true
 *  的时候，Behavior 才能收到后面的一些nested scroll 事件回调（如：onNestedPreScroll、onNestedScroll等）
 *  这个方法有个重要的参数nestedScrollAxes，表明处理的滑动的方向。
 *
 * @param coordinatorLayout 和Behavior 绑定的View的父CoordinatorLayout
 * @param child  和Behavior 绑定的View
 * @param directTargetChild
 * @param target
 * @param nestedScrollAxes 嵌套滑动 应用的滑动方向，看 {@link ViewCompat#SCROLL_AXIS_HORIZONTAL},
 *                         {@link ViewCompat#SCROLL_AXIS_VERTICAL}
 * @return
 */
@Override
public boolean onStartNestedScroll(CoordinatorLayout coordinatorLayout, View child, View directTargetChild, View target, int nestedScrollAxes) {
    return super.onStartNestedScroll(coordinatorLayout, child, directTargetChild, target, nestedScrollAxes);
}

/**
 * 嵌套滚动发生之前被调用
 * 在nested scroll child 消费掉自己的滚动距离之前，嵌套滚动每次被nested scroll child
 * 更新都会调用onNestedPreScroll。注意有个重要的参数consumed，可以修改这个数组表示你消费
 * 了多少距离。假设用户滑动了100px,child 做了90px 的位移，你需要把 consumed［1］的值改成90，
 * 这样coordinatorLayout就能知道只处理剩下的10px的滚动。
 * @param coordinatorLayout
 * @param child
 * @param target
 * @param dx  用户水平方向的滚动距离
 * @param dy  用户竖直方向的滚动距离
 * @param consumed
 */
@Override
public void onNestedPreScroll(CoordinatorLayout coordinatorLayout, View child, View target, int dx, int dy, int[] consumed) {
    super.onNestedPreScroll(coordinatorLayout, child, target, dx, dy, consumed);
}

/**
 * 进行嵌套滚动时被调用
 * @param coordinatorLayout
 * @param child
 * @param target
 * @param dxConsumed target 已经消费的x方向的距离
 * @param dyConsumed target 已经消费的y方向的距离
 * @param dxUnconsumed x 方向剩下的滚动距离
 * @param dyUnconsumed y 方向剩下的滚动距离
 */
@Override
public void onNestedScroll(CoordinatorLayout coordinatorLayout, View child, View target, int dxConsumed, int dyConsumed, int dxUnconsumed, int dyUnconsumed) {
    super.onNestedScroll(coordinatorLayout, child, target, dxConsumed, dyConsumed, dxUnconsumed, dyUnconsumed);
}

/**
 *  嵌套滚动结束时被调用，这是一个清除滚动状态等的好时机。
 * @param coordinatorLayout
 * @param child
 * @param target
 */
@Override
public void onStopNestedScroll(CoordinatorLayout coordinatorLayout, View child, View target) {
    super.onStopNestedScroll(coordinatorLayout, child, target);
}

/**
 * onStartNestedScroll返回true才会触发这个方法，接受滚动处理后回调，可以在这个
 * 方法里做一些准备工作，如一些状态的重置等。
 * @param coordinatorLayout
 * @param child
 * @param directTargetChild
 * @param target
 * @param nestedScrollAxes
 */
@Override
public void onNestedScrollAccepted(CoordinatorLayout coordinatorLayout, View child, View directTargetChild, View target, int nestedScrollAxes) {
    super.onNestedScrollAccepted(coordinatorLayout, child, directTargetChild, target, nestedScrollAxes);
}

/**
 * 用户松开手指并且会发生惯性动作之前调用，参数提供了速度信息，可以根据这些速度信息
 * 决定最终状态，比如滚动Header，是让Header处于展开状态还是折叠状态。返回true 表
 * 示消费了fling.
 *
 * @param coordinatorLayout
 * @param child
 * @param target
 * @param velocityX x 方向的速度
 * @param velocityY y 方向的速度
 * @return
 */
@Override
public boolean onNestedPreFling(CoordinatorLayout coordinatorLayout, View child, View target, float velocityX, float velocityY) {
    return super.onNestedPreFling(coordinatorLayout, child, target, velocityX, velocityY);
}

//可以重写这个方法对子View 进行重新布局
@Override
public boolean onLayoutChild(CoordinatorLayout parent, View child, int layoutDirection) {
    return super.onLayoutChild(parent, child, layoutDirection);
}
```



# 五.自定义Behavior实战
自定义Behavior一般来说分为两种:
### 1.改变其他View的行为
第一种是通过监听一个View的状态，如位置、大小的变化，来改变其他View的行为，这种只需要重写2个方法就可以了，分别是layoutDependsOn 和onDependentViewChanged。layoutDependsOn方法判断是指定依赖的View时，返回true，然后在onDependentViewChanged 里，被依赖的View做需要的行为动作。
```
public boolean layoutDependsOn(CoordinatorLayout parent, V child, View dependency)

public boolean onDependentViewChanged(CoordinatorLayout parent, V child, View dependency) 
```

例如我们要实现一个View监听另一个View移动自身也跟随移动:
##### (1.)定义behavior
```
public class FollowBehavior extends CoordinatorLayout.Behavior<View> {

    public FollowBehavior(Context context, AttributeSet attrs) {
        super(context, attrs);
    }

    //确定所提供的子视图是否具有另一个特定的同级视图作为布局依赖项,确认依赖为true,否则为false
    @Override
    public boolean layoutDependsOn(@NonNull CoordinatorLayout parent, @NonNull View child, @NonNull View dependency) {

        return dependency.getId() == R.id.view_observed; //根据ID添加被观察的控件
        //return dependency instanceof Button;//根据类型添加被观察的控件
    }

    //对孩子依赖性观点的改变做出反应
    //如果行为改变了子视图的大小或位置，否则返回false
    @Override
    public boolean onDependentViewChanged(@NonNull CoordinatorLayout parent, @NonNull View child, @NonNull View dependency) {
        int offset = dependency.getTop() - child.getTop();
        ViewCompat.offsetTopAndBottom(child, offset);
        return true;
    }
}
```
##### (2.)布局文件
```
<androidx.coordinatorlayout.widget.CoordinatorLayout 
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".ui.demo.CoordinatorlayoutActivity">

    <Button
        android:id="@+id/view_observed"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_gravity="left"
        android:text="被依赖的Button"
        android:textAllCaps="false" />

    <Button
        android:id="@+id/view_observer"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_gravity="right"
        android:text="订阅依赖的View"
        android:textAllCaps="false"
        app:layout_behavior="com.base.example.ui.demo.FollowBehavior" />

</androidx.coordinatorlayout.widget.CoordinatorLayout>
```
##### (3.)设置点击按钮开始移动
```
  override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(com.base.example.R.layout.activity_coordinatorlayout)
        findViewById<View>(R.id.view_observed).setOnClickListener {
            //将View向下移动
            ViewCompat.offsetTopAndBottom(it, 300)
        }
    }
```
##### (4.)效果
![动画6.gif](https://upload-images.jianshu.io/upload_images/3067896-fe5ad9eac9f047ef.gif?imageMogr2/auto-orient/strip)

### 2.改变自己的状态
第二种就是重写onStartNestedScroll、onNestedPreScroll、onNestedScroll等一系列方法。view需要根据监听CoordinatorLayout中的子view的滚动行为来改变自己的状态。
```
public boolean onStartNestedScroll(@NonNull CoordinatorLayout coordinatorLayout, @NonNull TextView child, @NonNull View directTargetChild, @NonNull View target, int axes, int type)

public void onNestedPreScroll(@NonNull CoordinatorLayout coordinatorLayout, @NonNull TextView child, @NonNull View target, int dx, int dy, @NonNull int[] consumed, int type)
```
##### (1.)定义behavior
```
public class ScrollBehavior extends CoordinatorLayout.Behavior<View> {
    public ScrollBehavior(Context context, AttributeSet attrs) {
        super(context, attrs);
    }

    @Override
    public boolean onStartNestedScroll(@NonNull CoordinatorLayout coordinatorLayout, @NonNull View child, @NonNull View directTargetChild, @NonNull View target, int axes, int type) {
        return (axes & ViewCompat.SCROLL_AXIS_VERTICAL) != 0;
    }

    @Override
    public void onNestedPreScroll(@NonNull CoordinatorLayout coordinatorLayout, @NonNull View child, @NonNull View target, int dx, int dy, @NonNull int[] consumed, int type) {
        super.onNestedPreScroll(coordinatorLayout, child, target, dx, dy, consumed, type);
        float scaleY = target.getScrollY();
        child.setScrollY((int) scaleY);
    }

    @Override
    public boolean onNestedPreFling(@NonNull CoordinatorLayout coordinatorLayout, @NonNull View child, @NonNull View target, float velocityX, float velocityY) {
        ((NestedScrollView) child).fling((int) velocityY);
        return true;
    }
}

```
- onStartNestedScroll()，这里的返回值表明这次滑动我们要不要关心，我们要关心的是y轴方向上的滑动。
- onNestedPreScroll() child的scrollY的值等于目标的scrollY的值就可以滑动了.
- onNestedFling() 将现在的y轴上的速度传递传递给child，让他fling起来就ok了
##### (2.)布局文件
```
<androidx.coordinatorlayout.widget.CoordinatorLayout 
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".ui.demo.CoordinatorlayoutActivity">
    
    <androidx.core.widget.NestedScrollView
        android:layout_width="100dp"
        android:layout_height="match_parent"
        android:background="@color/red">

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            android:orientation="vertical">

            <TextView
                android:layout_width="match_parent"
                android:layout_height="800dp"
                android:gravity="center"
                android:text="LeftScrollView"
                android:textColor="@color/white" />
        </LinearLayout>
    </androidx.core.widget.NestedScrollView>

    <androidx.core.widget.NestedScrollView
        android:layout_width="100dp"
        android:layout_height="match_parent"
        android:layout_gravity="right"
        android:background="@android:color/holo_green_light"
        app:layout_behavior=".ui.demo.ScrollBehavior">

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            android:orientation="vertical">

            <TextView
                android:layout_width="match_parent"
                android:layout_height="800dp"
                android:gravity="center"
                android:text="RightScrollView"
                android:textColor="@color/white" />
        </LinearLayout>
    </androidx.core.widget.NestedScrollView>
</androidx.coordinatorlayout.widget.CoordinatorLayout>
```
##### (3.)效果：
![](https://upload-images.jianshu.io/upload_images/3067896-e526710a7517f617.gif?imageMogr2/auto-orient/strip)
