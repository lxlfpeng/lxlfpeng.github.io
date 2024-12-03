---
title: Java-高级特性之反射和注解
date: 2016-09-11
categories: 
  - Java开发
---

# 一.Java反射机制。
#### 1.反射机制的定义。
Java反射机制是指在运行状态中,
对于任意一个类，都能知道这个类的所有属性和方法；
对于任何一个对象，都能够调用它的任何一个方法和属性；
这样动态获取新的以及动态调用对象方法的功能就叫做反射。
#### 2.反射机制的作用。
- 在运行时判断任意一个对象所属的类；

- 在运行时构造任意一个类的对象；

- 在运行时判断任意一个类所具有的成员变量和方法；

- 在运行时调用任意一个对象的方法；
#### 3.获取字节码。
**1. 获取字节码**
方式|解析
--|--
Class clazz1 = Class.forName("全限定类名");　| 通过Class类中的静态方法forName，直接获取到一个类的字节码文件对象，此时该类还是源文件阶段，并没有变为字节码文件。
Class clazz2  = Person.class;　| 　当类被加载成.class文件时，此时Person类变成了.class，在获取该字节码文件对象，也就是获取自己， 该类处于字节码阶段。
Class clazz3 = p.getClass(); |  通过类的实例获取该类的字节码文件对象，该类处于创建对象阶段　
**2. 实例化字节码**
(1.) 无参构造。
```
 Class<?> aClass = Class.forName("com.demo.myapplication.Person");
  Person person = (Person) aClass.newInstance();//无参构造
```
(2.) 有参构造。
```
   Class<?> aClass = Class.forName("com.demo.myapplication.Person");
   Constructor<?> constructor = aClass.getConstructor(int.class, String.class);
   Person xiaoming = (Person) constructor.newInstance(10, "小明");
```
#### 4.反射的实现。
例如有一个类:
```
package com.yousheng.demo;

public class Person {
    //私有属性
    private int age = 19;
    //公共属性
    public String name = "小明";

    //私有方法
    public String getName() {
        return name;
    }

    //私有方法
    private String getNameAndAge(String name, int age) {
        this.name = name;
        this.age = age;
        return "姓名为:" + name + "年龄为" + age;
    }
}
```
测试调用私有属性和私有方法。
```
  try {
    Class<?> aClass = Class.forName("com.yousheng.myapplication.Person");
    Person person = (Person) aClass.newInstance();
    //访问公共属性
    System.out.println("访问公共属性-->"+person.name);

    //访问私有属性
    Field ageField = aClass.getDeclaredField("age");
    //允许访问私有字段
    ageField.setAccessible(true);
    //获得私有字段值
    int age= (int) (ageField).get(person);
    System.out.println("访问私有属性-->"+age);

    //访问私有方法.
    //name为方法名
    //String.class 是第一个参数的类型
    //int.class 是第二个参数的类型
    Method getNameAndAge = aClass.getDeclaredMethod("getNameAndAge",String.class,int.class);
    //允许公共访问
    getNameAndAge.setAccessible(true);
    //调用方法
    String result = (String) getNameAndAge.invoke(person, "比尔盖茨", 52);
    System.out.println("访问私有方法-->"+result);

} catch (Exception e) {
    e.printStackTrace();
}
```
结果为:
```
    访问公共属性-->小明
    访问私有属性-->19
    访问私有方法-->姓名为:比尔盖茨年龄为52
```
#二.java注解。
#### 1.系统自带的注解。
例如:
```
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.SOURCE)
public @interface Override {

}
```
#### 2.元注解。
给自定义注解使用的注解就是元注解。
java中元注解有四个： ``@Retention @Target @Document @Inherited``；
**1.  @Target**
表示该注解可以用于什么地方
- ElementType.TYPE：作用于接口、类、枚举、注解,可以给一个类型进行注解，比如类、接口、枚举；
- ElementType.FIELD：作用于成员变量（字段、枚举的常量）,可以给属性进行注解；
- ElementType.METHOD：作用于方法,可以给方法进行注解；
- ElementType.PARAMETER：作用于方法的参数,可以给一个方法内的参数进行注解；
- ElementType.CONSTRUCTOR：作用于构造函数,可以给构造方法进行注解；
- ElementType.LOCAL_VARIABLE：作用于局部变量,可以给局部变量进行注解；
- ElementType.ANNOTATION_TYPE：作用于Annotation,可以给一个注解进行注解。
- ElementType.PACKAGE：作用于包名,可以给一个包进行注解；
- ElementType.TYPE_PARAMETER：java8新增，但无法访问到；
- ElementType.TYPE_USE：java8新增，但无法访问到；

**2. @Retention**

表示需要在什么级别保存该注解信息。可选的RetentionPolicy参数包括：

- SOURCE：只在*.java源文件的时候有效,编译成class就没用了；

- CLASS：只在*.java或者*.class中的文件有效，但是在运行时无效；

- RUNTIME：VM将在运行期间保留注解，因此可以通过反射机制读取注解的信息。包含以上两种，并且运行时也会有效果，一般我们都会选用该参数。

**3. @Document**

将注解包含在Javadoc中

**4. @Inherited**

允许子类继承父类中的注解

####3. 注解的属性
注解的属性也叫做成员变量。注解只有成员变量，没有方法。
注解的成员变量在注解的定义中以“无形参的方法”形式来声明，其方法名定义了该成员变量的名字，其返回值定义了该成员变量的类型。
```
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
public @interface Test {
    int id();
    String name();
}
```
上面代码定义了 Test 这个注解中拥有 id 和 name两个属性。在使用的时候，我们应该给它们进行赋值。
```
@TestAnnotation(id=3,name="hello annotation")
public class Test {
}
```

赋值的方式是在注解的括号内以 value=”” 形式，多个属性之前用 ，隔开。
 在注解中一般会有一些元素以表示某些值。注解的元素看起来就像接口的方法，唯一的区别在于可以为其制定默认值。没有元素的注解称为标记注解。
注解中属性可以有默认值，默认值需要用 default 关键值指定。比如：
```
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
public @interface Test {
    public int id() default -1;
    public String name() default "Hello";
}
```
有默认值的话就可以不用进行赋值了。
```
@Test ()
public class Test {}
```
元素不能有``不确定的值``，即要么有默认值，要么在使用注解的时候提供元素的值。而且元素不能使用null作为默认值

另外，还有一种情况。如果一个注解内仅仅只有一个名字为 value 的属性时，应用这个注解时可以直接接属性值填写到括号内。
```
public @interface Test {
    String value();
}
```
上面代码中，Test 这个注解只有 value 这个属性。所以可以这样应用。
```
@Test ("hello")
int a;
```
这和下面的效果是一样的
```
@Test (value="hello")
int a;
```
最后，还需要注意的一种情况是一个注解没有任何属性。比如
```
public @interface Test {}
```
那么在应用这个注解的时候，括号都可以省略。
#### 4、解析提取注解参数
Java通过反射机制获取类、方法、属性上的注解，因此java.lang.reflect提供AnnotationElement支持注解，主要方法如下：
|方法|说明|
|-|-|
boolean is AnnotationPresent(Class<?extends Annotation> annotationClass)|判断该元素是否被annotationClass注解修饰|
|<T extends Annotation> T getAnnotation(Class<T> annotationClass)|获取 该元素上annotationClass类型的注解，如果没有返回null
|Annotation[] getAnnotations()|返回该元素上所有的注解
|<T extends Annotation> T[] getAnnotationsByType(Class<T> annotationClass)|返回该元素上指定类型所有的注解
|Annotation[] getDeclaredAnnotations()|返回直接修饰该元素的所有注解
|<T extends Annotation> T[] getDeclaredAnnotationsByType(Class<T> annotationClass)|返回直接修饰该元素的所有注解

### 5.结合注解和反射写一个简单的版本的butternife。
运行时注解是通过反射来实现的，这种方式的效率会受到一定的影响，因此现在大多数的开源注解框架都是采用编译时注解的方式实现的，这种方式是在编译的时候生成所需的代码，不会影响运行的效率


#####方式一(运行时（Runtime）通过反射机制运行处理的注解):
1. 先自定义两个注解。
```
@Target(ElementType.FIELD)
@Retention(RetentionPolicy.RUNTIME)//运行时注解
public @interface FindViewById {
    //使用value命名，则使用的时候可以忽略，否则使用时就得把参数名加上
    int value();
}
```
```
@Target(ElementType.FIELD)
@Retention(RetentionPolicy.RUNTIME)
public @interface SetOnClickListener {
    int id();
    String methodName();
}
```
2. 创建注解解析器。
```
public class AnnotationParse {
    public static void parse(final Activity activity) {
        try {
            //反射获取Class对象
            Class<? extends Activity> aClass = activity.getClass();
            //获取所有的字段
            Field[] declaredFields = aClass.getDeclaredFields();
            //遍历字段
            for (Field declaredField : declaredFields) {
                //获取字段的所有的注解信息
                Annotation[] annotations = declaredField.getAnnotations();
                //遍历注解信息
                for (Annotation annotation : annotations) {
                    if (annotation instanceof FindViewById) {
                        //注解类型为 FindViewById
                        FindViewById findViewByIdAnnotation = declaredField.getAnnotation(FindViewById.class);
                        //设置可修改该字段
                        declaredField.setAccessible(true);
                        //获取该注解value所对的值
                        int viewID = findViewByIdAnnotation.value();

                        View view = activity.findViewById(viewID);

                        if (view != null)
                            declaredField.set(activity, view);
                        else
                            throw new Exception("不能找到该View" + declaredField.getName() + ".");

                    } else if (annotation instanceof SetOnClickListener) {
                        //注解类型为 SetOnClickListener
                        SetOnClickListener clickAnnotation = declaredField.getAnnotation(SetOnClickListener.class);
                        //设置可修改该字段
                        declaredField.setAccessible(true);
                        //获取该注解id所对的值
                        int viewId = clickAnnotation.id();
                        //获取该注解的methodName所对应的值
                        String methodName = clickAnnotation.methodName();
                        //获取view
                        View view = (View) declaredField.get(activity);
                        if (view == null) {
                            // 如果对象为空，则重新查找对象
                            view = activity.findViewById(viewId);
                            if (view != null)
                                declaredField.set(activity, view);
                            else
                                throw new Exception("");
                        }
                        //获取目标对象的所有方法集
                        Method[] declaredMethods = aClass.getDeclaredMethods();
                        //遍历方法集
                        for (final Method declaredMethod : declaredMethods) {
                            //判断方法名是否和注解的methodName相同
                            if (declaredMethod.getName().equals(methodName)) {
                                //设置点击事件
                                view.setOnClickListener(new View.OnClickListener() {
                                    @Override
                                    public void onClick(View v) {
                                        try {
                                            //调用方法
                                            declaredMethod.invoke(activity);
                                        } catch (IllegalAccessException e) {
                                            e.printStackTrace();
                                        } catch (InvocationTargetException e) {
                                            e.printStackTrace();
                                        }
                                    }
                                });
                                break;
                            }
                        }
                    }
                }
            }
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }
}
```
3. 调用
mian_activity.xml
```
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:orientation="vertical"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/txt_main"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:textColor="@color/colorPrimary"/>

    <Button
        android:id="@+id/btn_main"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="click me"/>

</LinearLayout>
```
MainActivity.java
```
 @FindViewById(R.id.txt_main)
    private TextView mTxtMain;
    @SetOnClickListener(id = R.id.btn_main, methodName = "onClick")
    private Button mBtnMain;

    /**
     * 点击事件
     */
    public void onClick() {
        Toast.makeText(this, "Hello world", Toast.LENGTH_SHORT).show();
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        AnnotationParse.parse(this);
        mTxtMain.setText("测试代码");
}
```
#####方式二(运行时（Runtime）通过反射机制运行处理的注解):



部分内容节选自:
[java注解-最通俗易懂的讲解](https://blog.csdn.net/qq1404510094/article/details/80577555)
