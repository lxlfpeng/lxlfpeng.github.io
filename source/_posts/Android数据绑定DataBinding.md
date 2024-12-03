---
title: Android数据绑定DataBinding
---

# 一.DataBinding简介
MVVM架构的核心就是数据驱动，数据驱动的意思就是，数据更新的时候，自动刷新UI。采用MVVM架构会节省大量的更新UI的代码，并且数据更新后主动出发UI更新这种方式，更难出错，鲁棒性更强。且不需要关注数据变化的时机，是需要关注数据变化的结果即可。
### 1.开启DataBinding功能
- 使用最新版的AndroidStudio，至少AS3.0以上。
- 在项目module下的build.gradle的android闭包下，配置 databinding{enabled=true}。
- 对于布局的xml文件，将原有的正常布局，外面用<layout></layout>包裹作为跟节点。<data></data>节点下存放用于xml布局的一些变量，工具类之类的。

> 打开布局文件，选中根布局的 ViewGroup，按住 Alt + 回车键，点击 “Convert to data binding layout”，就可以生成 DataBinding 需要的布局规则
![](/images/fcbe0c5b3ef8f844edb62047bd46cf39.webp)

### 2.DataBinding简单使用

##### (1.)声明一个数据对象

```
package com.peng.databindingdemo.model
data class User(val Name: String, val Age: String)
```

> 对象的属性必须可以直接访问，或者提供访问方法。

##### (2.)布局文件中声明需要绑定的类
接下来，在Layout布局文件的"data"标签当中声明要使用到的变量、类的全路径。 如下
```
<data>
      <variable name="userInfo"
                type="com.peng.databindingdemo.model.User"/>
</data>
```
也可以采用「import」的方式引进来，这样我们就不用每次都指明整个包名的路径了:
```
<data>
     <import type="com.peng.databindingdemo.model.User"/>
     <variable name="userInfo"
               type="User"/>
</data>
```
如果我们「import」相同，我们还可以采用增加「alias」字段来指定别名:
```
<data>
    <import type="com.peng.databindingdemo.model.User"/>
    <import type="com.peng.databindingdemo.model2.User"
            alias="User2"/>
    <variable name="userInfo"
              type="User"/>
    <variable name="user2Info"
              type="User2"/>
</data>
```

##### (3.)布局文件中使用变量和类
```
<layout xmlns:tools="http://schemas.android.com/tools">
    <!--用于xml布局中binding数据的一些变量，类的声明引用-->
    <data>
        <!--导入Map和List集合支持-->
        <import type="java.util.Map" />
        <import type="java.util.List" />
        <!--可使使用alias 命名别名，就可以在xml内部应用时候使用别名，优化书写和区分-->
        <import type="com.example.module_test.databinding.data.User" />

        <!--变量声明 ，使用variable 需要在代码中初始化和赋值。 基础数据类型的使用-->
        <variable
            name="title"
            type="String" />

        <!--List和Map类型，在xml中，个别字符需要转义符号-->
        <variable
            name="listData"
            type="List&lt;String>" />

        <variable
            name="mapData"
            type="Map&lt;Integer,String>" />

        <variable
            name="userInfo"
            type="User" />

    </data>

    <LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:orientation="vertical"
        android:padding="10dp">
        <!--使用databinding，则会将每个配置id的控件在对应的Java的binding类中，生成控件引用。使用@{}符号引用导入/定义的属性-->

        <!--普通的应用变量，int要转为string，使用拼接，或者valueOf，toString都可以。-->
        <androidx.appcompat.widget.AppCompatTextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_margin="2dp"
            android:text="@{`标题是`+title}" />

        <!--使用List和Map-->
        <androidx.appcompat.widget.AppCompatTextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="@{listData[0]+mapData[0]}"
            android:textColor="@android:color/holo_purple" />

        <!--使用对象Bean的属性-->
        <androidx.appcompat.widget.AppCompatTextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="@{userInfo.name}" />

        <androidx.appcompat.widget.AppCompatTextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="@{userInfo.age}" />
    </LinearLayout>

</layout>
```

> 布局中使用 @{} 来设置属性

##### (4.)绑定数据
系统会自动为我们的绑定布局生成绑定类，规则是布局文件名+Binding，例如上面的布局文件名是：activity_main.xml，那么自动生成的绑定类就是TestActivityDataBindingBinding。该类包含布局属性到布局视图的所有绑定，并知道如何为绑定表达式指定值。
```
class DataBindingActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.test_activity_data_binding)
        val viewDataBinding: TestActivityDataBindingBinding =
            DataBindingUtil.setContentView(this, R.layout.test_activity_data_binding)
        viewDataBinding.title = "三国演艺"
        viewDataBinding.listData = mutableListOf("刘备", "曹操", "孙权")
        viewDataBinding.mapData = mutableMapOf(0 to "赵云")
        viewDataBinding.userInfo = User("关羽", "52")
    }
}
```

如果是在其他地方绑定不觉也可以使用如下两种方式进行布局绑定:

```
ListItemBinding binding = ListItemBinding.inflate(layoutInflater, viewGroup, false);
// 或者
ListItemBinding binding = DataBindingUtil.inflate(layoutInflater, R.layout.list_item, viewGroup, false);
```

##### (5.)运行结果

![](/images/94981b71bdf55c98b40ccf27bc6e950c.webp)

### 3.DataBinding中使用include
对于 include 的布局文件，一样是支持通过 dataBinding 来进行数据绑定，此时一样需要在待 include 的布局中依然使用 layout 标签，声明需要使用到的变量
view_include.xml:
```
<?xml version="1.0" encoding="utf-8"?>
<layout xmlns:android="http://schemas.android.com/apk/res/android">

    <data>

        <import type="com.example.module_test.databinding.data.User" />

        <variable
            name="userInfo"
            type="User" />
    </data>

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="vertical">

        <TextView
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:gravity="center"
            android:padding="20dp"
            android:text="@{userInfo.email}" />

        <Button
            android:id="@+id/btn_include"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:text="include引用布局" />
    </LinearLayout>
</layout>
```

在主布局文件中将相应的变量传递给 include 布局，从而使两个布局文件之间共享同一个变量

```
 <include
     android:id="@+id/include_view"
     layout="@layout/test_view_include"
     app:userInfo="@{userInfo}" />
```

### 4.Databinding支持的基础运算符
DataBinding 支持在布局文件中使用以下运算符、表达式和关键字:
- 算术 + - / * %
- 字符串合并+
- 逻辑&& ||
- 二元& | ^
- 一元 + - ! ~
- 移位>> >>> <<
- 比较== > < >= <=
- Instanceof
- Grouping ()
- character, String, numeric, null
- Cast
- 方法调用
- Field 访问
- Array访问 []
- 三元?:

### 5.Databinding事件绑定
Databinding事件绑定，分两种方式：方法引用和监听绑定
```
public class UserPresenter {
  public void onUserNameClick(User user) {
      Toast.makeText(Main5Activity.this, "用户名：" + user.getName(), Toast.LENGTH_SHORT).show();
  }

  public void afterTextChanged(Editable s) {
      user.setName(s.toString());
      activityMain5Binding.setUserInfo(user);
  }

  public void afterUserPasswordChanged(Editable s) {
      user.setPassword(s.toString());
      activityMain5Binding.setUserInfo(user);
  }
}

```
```
<?xml version="1.0" encoding="utf-8"?>
<layout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

    <data>
        <import type="com.leavesc.databinding_demo.model.User" />
        <import type="com.leavesc.databinding_demo.MainActivity.UserPresenter" />
        <variable
            name="userInfo"
            type="User" />
        <variable
            name="userPresenter"
            type="UserPresenter" />
    </data>

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:layout_margin="20dp"
        android:orientation="vertical"
        tools:context="com.leavesc.databinding_demo.MainActivity">

        <TextView
            ···
            android:onClick="@{()->userPresenter.onUserNameClick(userInfo)}"
            android:text="@{userInfo.name}" />

        <TextView
            ···
            android:text="@{userInfo.password}" />

        <EditText
            ···
            android:afterTextChanged="@{userPresenter.afterTextChanged}"
            android:hint="用户名" />

        <EditText
            ···
            android:afterTextChanged="@{userPresenter.afterUserPasswordChanged}"
            android:hint="密码" />

    </LinearLayout>

</layout>
```
方法引用的方式与调用函数的方式类似，既可以选择保持事件回调方法的签名一致：**@{userPresenter.afterTextChanged}**，此时方法名可以不一样，但方法参数和返回值必须和原始的回调函数保持一致。也可以引用不遵循默认签名的函数：**@{()->userPresenter.onUserNameClick(userInfo)}**，这里用到了 Lambda 表达式，这样就可以不遵循默认的方法签名，将`userInfo`对象直接传回点击方法中。此外，也可以使用方法引用 **::** 的形式来进行事件绑定
![image](/images/9e114b7b6b37c520c1fd4ae28c5727f9.webp)
> 方法引用和监听器绑定之间的主要区别在于实际监听器实现是在绑定数据时创建的，而不是在事件触发时创建的。

### 6.Databinding使用类静态方法
1. 首先定义一个静态方法
```
public class StringUtils {

    public static String toUpperCase(String str) {
        return str.toUpperCase();
    }

}
```
2. 在 data 标签中导入该工具类
```
 <import type="com.leavesc.databinding_demo.StringUtils" />
```
3. 然后就可以像对待一般的函数一样来调用了
```
  <TextView
     android:layout_width="match_parent"
     android:layout_height="wrap_content"
     android:onClick="@{()->userPresenter.onUserNameClick(userInfo)}"
     android:text="@{StringUtils.toUpperCase(userInfo.name)}" />
```
# 二.DataBinding绑定适配器

### 1.DataBinding自动选择方法
当在布局中使用属性绑定表达式时，每当绑定的变量值发生更改时，生成的绑定类必须使用绑定表达式调用 View 上的 setter方法. ``Data Binding 允许你为任何 setter 方法创建绑定属性。``对于名为 example 的属性，DataBinding 库会自动尝试查找接受兼容类型作为参数的 setExample(arg)方法，例如``android:text="@{user.name}"``，DataBinding 库将查找 user.getName() 返回的值设置给 setText(arg) 方法；

### 2.DataBinding自定义指定方法名称
**DataBinding默认可以在布局中使用具有setter方法的View的属性**， 但是如果有些 View 属性具有不按属性名匹配的 setter 方法，在这种情况下你可以使用@BindingMethods 注解来关联对应的 setter 方法，需要通过创建一个自定义属性来关联一个类中已有的方法，注解是写在一个类上面，它可以包含多个 @BindingMethod 注解，每个注解对应着一个属性的关联方法。
```
@BindingMethods({@BindingMethod(type = android.widget.TextView.class, attribute = "myBackgroundColor",
        method = "setBackgroundColor")})
public class MyTextView extends AppCompatTextView {


    public MyTextView(Context context) {
        super(context);
    }

    public MyTextView(Context context, @Nullable AttributeSet attrs) {
        super(context, attrs);
    }

    public MyTextView(Context context, @Nullable AttributeSet attrs, int defStyleAttr) {
        super(context, attrs, defStyleAttr);
    }
}
```
这里为TextView的setBackgroundColor方法设置了另外的一个属性名叫做myBackgroundColor，它的命名空间是app。如果想设置为android就需要在在前面显示的设置android命名空间。如：”android:myBackgroundColor”
```
<com.example.module_test.databinding.adapter.MyTextView
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:text="BindingMethods"
    app:myBackgroundColor="@{@color/colorPrimary}" />
```
可以看到在MyTextView的属性设置中我们使用了myBackgroundColor属性。
> 大多数情况下，你不需要写这样的注解，因为大多数 View 的属性都有相匹配的 setter 方法，它会以自动选择方法的方式找到。

### 3.DataBinding提供自定义逻辑
有些属性需要自定义绑定逻辑。 例如，ImageView 的 android:src 属性，它没有相匹配的 setter 方法，但它有 setImagexxx 方法。 可以使用带有@BindingAdapter 注解的静态绑定适配器方法来达到自定义调用 setter 方法。

```
public class BindAdapter {
    @BindingAdapter("app:image")
    public static void bindImage(ImageView view, int resId) {
        view.setImageResource(resId);
    }
}
```

这个自定义方法名可以是任意的。 第一个参数确定与该属性关联的 View 的类型，也就是说为 ImageView 声明了一个 app:image 属性。 第二个参数确定给定属性的绑定表达式中接受的类型。

```
<?xml version="1.0" encoding="utf-8"?>
<layout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto">
    <data>
        <variable name="resId" type="int" />
    </data>
    <ImageView
        ...
        app:image="@{resId}"
        ... />
</layout>
```

这样一个自定义逻辑的绑定方法就写好了，可以在方法中自定义任何逻辑，当有一些重复繁琐的操作时，很合适写一个自定义逻辑绑定适配器。 上面讲的@BindMethods都是建立在已有的方法之上的。通过@BindAdapter还可以自定义属性名以及它所做的逻辑。
```
@BindingAdapter(value = { "imageUrl", "error" }, requireAll = false)
    public static void loadImage(ImageView view, String url, Drawable error) {
    Glide.with(view.getContext()).load(url).into(view);
}
```
- 修饰方法， 要求方法必须public static
- 第一个参数必须是控件或其父类
- 方法名随意
- 最后这个boolean类型是可选参数. 可以要求是否所有参数都需要填写. 默认true.如果requireAll为false， 你没有填写的属性值将为null. 所以需要做非空判断.
```
<?xml version="1.0" encoding="utf-8"?>
<layout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto">
    <data>
        <variable
            name="imageUrl"
            type="String" />
        <variable
            name="error"
            type="android.graphics.drawable.Drawable" />
    </data>
    <ImageView
        android:layout_width="match_parent"
        android:layout_height="200dp"
        app:error="@{error}"
        wuyanzu:imageUrl="@{imageUrl}"
    />
</layout>
```

可以看到命名空间可以随意， 但是如果在BindingAdapter的数组内你定义了命名空间就必须完全遵守

# 三.Databinding单向数据绑定
在上文中讲到，通过DataBinding进行绑定控件以及进行相关操作，但是绑定的变量发生变化的时候，每次都要重新向 ViewDataBinding 传值进行更新操作之后才能刷新UI。Observable 就是为此而生的概念，通过Observable为当数据改变时同时使视图刷新。

### 1.BaseObservable可观察对象
一个类里面的属性被更新后，UI并不会自动更新。而数据绑定后，自然会期望数据变更后 UI 会即时刷新，Observable 就是为此而生的概念。DataBinding的本身是对View层状态的一种观察者模式的实现，通过让View与ViewModel层可观察的对象进行绑定，当ViewModel层数据发生变化，View层也会自动进行UI的更新。**BaseObservable** 提供了 **notifyChange()** 和 **notifyPropertyChanged()** 两个方法，前者会刷新所有的值域，后者则只更新对应 **BR** 的 **flag**，该 BR 的生成通过注释 **@Bindable** 生成，可以通过 **BR notify** 特定属性关联的视图。
```
public class Person extends BaseObservable {
    //如果是 public 修饰符，则可以直接在成员变量上方加上 @Bindable 注解
    @Bindable
    public String name;
    //如果是 private 修饰符，则在成员变量的 get 方法上添加 @Bindable 注解
    private String age;
    public Person(String name, String details) {
        this.name = name;
        this.age = details;
    }

    public void setName(String name) {
        this.name = name;
        //只更新本字段
        notifyPropertyChanged(BR.name);
    }

    @Bindable
    public String getAge() {
        return age;
    }
    public void setAge(String details) {
        this.age = details;
        //更新所有字段
        notifyChange();
    }
}
```
在 **setName()** 方法中更新的只是本字段，而 **setAge()** 方法中更新的是所有字段。
```
<?xml version="1.0" encoding="utf-8"?>
<layout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools">

    <data>

        <import type="com.example.module_test.databinding.data.Person" />

        <variable
            name="personInfo"
            type="Person" />
    </data>

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:orientation="vertical"
        android:padding="20dp"
        tools:context=".Main3Activity">

        <TextView
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:text="@{`姓名:`+personInfo.name}" />

        <TextView
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:text="@{`年龄:`+personInfo.age}" />

        <Button
            android:id="@+id/btn_change"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:text="改变 name 和 age属性"
            android:textAllCaps="false" />
    </LinearLayout>
</layout>
```

```
class SingleDataBindingActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.test_activity_single_data_binding)
        val viewDataBinding: TestActivitySingleDataBindingBinding =
            DataBindingUtil.setContentView(this, R.layout.test_activity_single_data_binding)
        val person = Person("关羽", "52")
        viewDataBinding.personInfo = person
        findViewById<Button>(R.id.btn_change).setOnClickListener {
            person.setName("刘备")
            person.age = "60"
        }
    }
}
```

![](/images/0f53b95e4b48945d2dfb365d7e073d42.webp)

### 2.ObservableField可观察字段
继承于 Observable 类相对来说使用起来会复杂一些，且需要自己进行 notify 操作才能刷新UI，因此为了简单起见可以选择使用 **ObservableField**。ObservableField 可以理解为官方对 BaseObservable 中字段的注解和刷新等操作的封装，官方原生提供了对基本数据类型的封装，例如 **ObservableBoolean、ObservableByte、ObservableChar、ObservableShort、ObservableInt、ObservableLong、ObservableFloat、ObservableDouble**以及 **ObservableParcelable** ，也可通过 **ObservableField** 泛型来申明其他类型
```
public class UserBean {
    public ObservableField<String> name;
    public ObservableInt number;

    public UserBean(ObservableField<String> name, ObservableInt number) {
        this.name = name;
        this.number = number;
    }
}
```

```
<?xml version="1.0" encoding="utf-8"?>
<layout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools">

    <data>

        <import type="com.example.module_test.databinding.data.UserBean" />

        <variable
            name="userBean"
            type="UserBean" />
    </data>

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:orientation="vertical"
        android:padding="20dp"
        tools:context=".Main3Activity">

        <TextView
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:text="@{`姓名:`+userBean.name}" />

        <TextView
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:text="@{`电话:`+userBean.number}" />

        <Button
            android:id="@+id/btn_change"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:text="改变 name 和 number属性"
            android:textAllCaps="false" />
    </LinearLayout>
</layout>
```

```
class ObservableFieldActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.test_activity_observable_field)
        val viewDataBinding: TestActivityObservableFieldBinding =
            DataBindingUtil.setContentView(this, R.layout.test_activity_observable_field)
        val user = UserBean(ObservableField<String>("赵云"), ObservableInt(10086))
        viewDataBinding.userBean = user
        findViewById<Button>(R.id.btn_change).setOnClickListener {
            user.name.set("马超")
            user.number.set(10010)
        }
    }
}
```

对 ObservablePerson 属性值的改变都会立即触发 UI 刷新，概念上与 Observable 区别不大。
![](/images/5900bebc60c9bb3653d6266665b15c2f.webp)

### 3.ObservableCollection可观察集合
dataBinding 也提供了包装类用于替代原生的 `List` 和 `Map`，分别是 `ObservableList` 和 `ObservableMap`，当其包含的数据发生变化时，绑定的视图也会随之进行刷新。
```
<?xml version="1.0" encoding="utf-8"?>
<layout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

    <data>
        <import type="android.databinding.ObservableList"/>
        <import type="android.databinding.ObservableMap"/>
        <variable
            name="list"
            type="ObservableList&lt;String&gt;"/>
        <variable
            name="map"
            type="ObservableMap&lt;String,String&gt;"/>
        <variable
            name="index"
            type="int"/>
        <variable
            name="key"
            type="String"/>
    </data>

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:orientation="vertical">

        <TextView
            ···
            android:padding="20dp"
            android:text="@{list[index],default=aa}"/>

        <TextView
            ···
            android:layout_marginTop="20dp"
            android:padding="20dp"
            android:text="@{map[key],default=bb}"/>

        <Button
            ···
            android:onClick="onClick"
            android:text="改变数据"/>

    </LinearLayout>
</layout>

```

# 四.双向数据绑定
### 1.实现双向数据绑定
双向绑定的意思即为当数据改变时同时使视图刷新，而视图改变时也可以同时改变数据，上文中我们实现了数据改变时同时使视图刷新，下面探讨视图改变时同时改变数据，数据绑定框架已经为常用的双向绑定属性和属性改变监听器提供了双向绑定的实现。android:text属性就是其中之一。
```
public class StaffBean {
    public ObservableField<String> name;
    public String code;

    public StaffBean(ObservableField<String> name, String code) {
        this.name = name;
        this.code = code;
    }

    public ObservableField<String> getName() {
        return name;
    }

    public String getCode() {
        return code;
    }

    public void setName(ObservableField<String> name) {
        this.name = name;
    }

    public void setCode(String code) {
        this.code = code;
    }
}
```
布局文件:
```
<?xml version="1.0" encoding="utf-8"?>
<layout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools">

    <data>

        <import type="com.example.module_test.databinding.data.StaffBean" />

        <variable
            name="staffBean"
            type="StaffBean" />
    </data>

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:orientation="vertical"
        android:padding="20dp"
        tools:context=".Main3Activity">

        <TextView
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:text="@{`员工姓名:`+staffBean.name}" />

        <TextView
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:text="@{`员工编号:`+staffBean.code}" />

        <EditText
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:hint="请输入Name"
            android:text="@={staffBean.name}" />

        <EditText
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:hint="请输入Name"
            android:inputType="number"
            android:text="@={staffBean.code}" />
    </LinearLayout>
</layout>
```
Activity中
```
class TwoWayBindActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.test_activity_two_way_bind)
        val viewDataBinding: TestActivityTwoWayBindBinding =
            DataBindingUtil.setContentView(this, R.layout.test_activity_two_way_bind)
        val staffBean = StaffBean(ObservableField(""), "0")
        viewDataBinding.staffBean = staffBean
    }
}
```
![动画8.gif](/images/f965b33b9a690a520c369c51b2994c17.webp)
通过ObservableField可以将数据的变化通知到Ui进行修改，@={}可以将UI数据的变化通知到数据类进行变化,这样就实现了数据的双向绑定.
### 2.双向数据绑定避免死循环
死循环绑定：因为数据源改变会通知view刷新，而view改变又会通知数据源刷新，这样一直循环往复，就形成了死循环绑定 看看dataBinding源码中是如何解决的，路径：android.databinding.adapters.TextViewBindingAdapter：
```
@BindingAdapter("android:text")
public static void setText(TextView view, CharSequence text) {
    final CharSequence oldText = view.getText();
    if (text == oldText || (text == null && oldText.length() == 0)) {
        return;
    }
    if (text instanceof Spanned) {
        if (text.equals(oldText)) {
            return; // No change in the spans, so don't set anything.
        }
    } else if (!haveContentsChanged(text, oldText)) {
        return; // No content changes, so don't set anything.
    }
    view.setText(text);
}
```

>从上面的源码可以看到，在处理双向绑定的业务逻辑时，要对新旧数据进行比较，只处理新旧数据不一样的数据，对于新旧数据一样的数据作return处理，通过这种方式来避免死循环绑定。

参考资料:
[DataBinding官方文档](https://developer.android.com/topic/libraries/data-binding)

[Android DataBinding 从入门到进阶](https://www.jianshu.com/p/bd9016418af2)
[Android_Databinding使用整理](https://www.jianshu.com/p/fd3bd18a0d48)
[Android Jetpack系列——细说DataBinding](https://www.jianshu.com/p/2b715d788423)
[DataBinding最全使用说明](https://juejin.im/post/5a55ecb6f265da3e4d7298e9)