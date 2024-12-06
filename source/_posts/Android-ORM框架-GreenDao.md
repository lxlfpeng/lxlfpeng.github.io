---
title: Android-ORM框架-GreenDao
date: 2018-07-05
categories: 
  - Android开发
tags:
  - 数据库
  - sqlite
---

# 一.GreenDao简介
GreenDAO是一个基于**sqlite**的对象关系映射(ORM)的数据库框架，**ORM（Object Relation Mapping对象关系映射）**，其表现形式就是通过GreenDao将数据库和Bean对象关联起来。使用greendao可以节省自己编写SQL语句进行CRUD的时间。
[GreenDao官网](http://greenrobot.org/greendao/)
[GitHub地址](https://github.com/greenrobot/greenDAO)
![greendao原理](/images/31e0493a22955d3dc02b9c6ebacc9b1b.webp)

# 二.项目工程引入GreenDao
### 1.引入GreenDao
In root build.gradle file
```
buildscript {
    repositories {
        google()
        jcenter()
    }
    dependencies {
         ...
        classpath 'org.greenrobot:greendao-gradle-plugin:lastVersion' // add plugin
    }
}
```
In app modules app/build.gradle file:
```
...
apply plugin: 'org.greenrobot.greendao' // apply plugin
 
dependencies {
    implementation 'org.greenrobot:greendao:lastVersion' // add library
}
```

### 2.配置GreenDao
项目中使用kotlin时引入greendao最好配置一下targetGenDir  否则可能编译报错。
```
android{
    ...
}
greendao{
    schemaVersion 2 // 数据库版本号
  //  daoPackage  'com.doris.sample.greendao'//greenDao 自动生成的代码保存的包名
    targetGenDir   'src/main/java' //自动生成的代码存储的路径，默认是 build/generated/source/greendao.
   // generateTests false //true的时候自动生成测试单元
  //  targetGenDirTests: 测试单元的生成目录默认是 src/androidTest/java
}
```

# 三.GreenDao关键类
**DaoMaster:** 保存数据库对象（SQLiteDatabase）并管理特定模式的Dao类。它具有静态方法来创建表或将他们删除。其内部类OpenHelper和DevOpenHelper是在SQLite数据库中创建模式的SQLiteOpenHelper实现。
**DaoSession:**管理特定模式的所有可用Dao对象，您可以使用其中一个getter方法获取。DaoSession还为实体提供了一些通用的持久性方法，如插入，加载，更新，刷新和删除。最后，DaoSession对象也跟踪一个身份范围。
**XXDAO:**数据访问对象(Dao)持续存在并查询实体。对于每个实体，GreenDao生成一个Dao,它比DaoSession有更多的持久化方法。
**Entities(实体对象):**持久对象，通常实体是使用标准Java属性(如POJO或JavaBean)来表示数据库的对象。

# 四.GreenDao使用
### 1.初始化GreenDao
一般我们在Application里面进行初始化.
```
public class BaseApplication extends SuperApplication {
    private DaoMaster.DevOpenHelper mHelper;
    private SQLiteDatabase db;
    private DaoMaster mDaoMaster;
    public  DaoSession mDaoSession;
    @Override
    public void onCreate() {
        super.onCreate();
        ...
      // 通过 DaoMaster 的内部类 DevOpenHelper，你可以得到一个便利的 SQLiteOpenHelper 对      象。
     // 可能你已经注意到了，你并不需要去编写「CREATE TABLE」这样的 SQL 语句，因为 GreenDAO 已经帮你做了。
     // 注意：默认的 DaoMaster.DevOpenHelper 会在数据库升级时，删除所有的表，意味着这将导致数据的丢失。
     // 所以，在正式的项目中，你还应该做一层封装，来实现数据库的安全升级。
    // 此处green-db表示数据库名称 可以任意填写
       mHelper = new DaoMaster.DevOpenHelper(this, "green-db", null);
       db = mHelper.getWritableDatabase();
     // 注意：该数据库连接属于 DaoMaster，所以多个 Session 指的是相同的数据库连接。
       mDaoMaster = new DaoMaster(db);
       mDaoSession = mDaoMaster.newSession();
      }
    public  DaoSession getDaoSession() {
        return mDaoSession;
    }
    public SQLiteDatabase getDb() {
        return db;
    }
}
```

### 2.创建实体类
```
@Entity(
        nameInDb = "USERS",// 指定该表在数据库中的名称，默认是基于实体类名
        indexes = {@Index(value = "text, date DESC", unique = true)},// 定义跨多个列的索引
        createInDb = true,// 高级标志，是否创建该表。默认为true。如果有多个实体映射一个表，或者该表已在外部创建，则可置为false
        //schema = "bqt_schema",// 告知GreenDao当前实体属于哪个schema。属于不同模式的实体应不具有关系。
        active = true,// 标记一个实体处于活动状态，活动实体(设置为true)有更新、删除和刷新方法。默认为false
        generateConstructors = true,//是否生成所有属性的构造器。注意：无参构造器总是会生成。默认为true
        generateGettersSetters = true//是否应该生成属性的getter和setter。默认为true
)
public class User{
    @Id(autoincrement = true) //主键自增,类型为包装类型Long,如果使用long就会报错。插入数据时第一个参数是ID，如果插入值为null，字段会自动增长。
    private Long id;

    @NotNull//在保存到数据库中之前需要保证此值不为null，否则会报 IllegalArgumentException ，并直接崩溃
    private String name;

    @Transient //表明此字段不存储到数据库中，用于不需要持久化的字段，比如临时状态
    private String nickName;

    @Property(nameInDb = "TIME") //为该属性在数据库中映射的字段名设置一个非默认的名称,，默认是的使用字段名
    private Date brithday;

    @Convert(converter = UserTypeConverter.class, columnType = String.class) //类型转换类，自定义的类型在数据库中存储的类型
    private UserType type; //在保存到数据库时会将自定义的类型 NoteType 通过 UserType TypeConverter 转换为 String 类型。反之亦然
 
    private long createTime = System.currentTimeMillis();//设置默认值
}
```
greendao支持的数据类型
```
boolean, Boolean
int, Integer
short, Short
long, Long
float, Float
double, Double
byte, Byte
byte[]
String
Date
```

### 3.生成类文件
编写好实体类并添加自己需要的注解之后，点击build --> Make Project，就会自动生成相应的 setter 和 getter 方法。并且在项目的build目录下(或者自己设定的目录:src/main/java)下看到生成的三个类文件。DaoMaster、DaoSession、XXXDao

# 五.GreenDao增删改查
### 1.插入数据
```
//获取dao
DaoSession daoSession = ((App) getApplication()).getDaoSession();
UserDao userDao = daoSession.getUserDao();

//准备数据
User user=new User(null,"张三"...)

//插入数据
int id=userDao.insert(user); 
```
- insert 插入一条数据

- insertInTx 批量插入数据

- insertOrReplace 插入数据，传入的对象主键如果存在于数据库中，有则更新，否则插入

- insertOrReplaceInTx 批量插入数据 同上

- save 插入数据，判断对象是否有Key值，有则更新，否则插入

### 2.删除数据
```
//获取dao
DaoSession daoSession = ((App) getApplication()).getDaoSession();
UserDao userDao = daoSession.getUserDao();
//删除数据
userDao.deleteByKey(id);
```
- delete 删除单个数据

- deleteInTx 批量删除数据

- deleteByKey 通过主键删除数据

- deleteByKeyInTx 通过主键批量删除数据

- deleteAll 删除全部数据

### 3.修改数据
```
//获取dao
DaoSession daoSession = ((App) getApplication()).getDaoSession();
UserDao userDao = daoSession.getUserDao();

//准备数据
User user=new User(1,"李四"...)

//修改数据
userDao.update(user); 
```
- update 单个修改数据

- updateInTx 批量修改数据

### 4.查询数据
```
//获取dao
DaoSession daoSession = ((App) getApplication()).getDaoSession();
UserDao userDao = daoSession.getUserDao();
//查询所有的数据
List<User> list=userDao.loadAll(); 

//按条件查询
User unique = userDao.queryBuilder().where(UserDao .Properties.Name.eq("张三")).unique();

```
1. or(WhereCondition cond1, WhereCondition cond2, WhereCondition... condMore): 嵌套条件或者，用法同or。
2.  and(WhereCondition cond1, WhereCondition cond2, WhereCondition... condMore): 嵌套条件且，用法同and。



- load 根据主键查询

- loadAll 查询所有数据

- where 条件查询

- like 模糊查询

- list 以ArrayList返回

- unique 返回唯一或null

- eq 查询该字段的数据

- notEq 查询不是该字段的数据

### 5.排序、条件限制
- order 排序，我们可以对查询的结果进行排序。orderAsc:（依据的属性名称，可以有多个属性），正序 orderDesc: 倒序
- limit 限制,当你根据条件查询，返回N条数据的时候，但是你只想要里面的前十个的时候.需要做分页的时候offset(start).limit(10)

### 6.Debug查询
```
QueryBuilder.LOG_SQL = true;
QueryBuilder.LOG_VALUES = true;
```
设置这两个属性就可以看到log

# 六.GreenDao数据库版本迁移
在版本迭代时，我们经常需要对数据库进行升级，而GreenDAO默认的DaoMaster.DevOpenHelper在进行数据升级时，会把旧表删除，然后创建新表，并没有迁移旧数据到新表中，从而造成数据丢失。
查看DaoMaster源码可知:
![](/images/2efcace7338d84d771015bab0cd9214d.webp)
[解决方式](https://github.com/yuweiguocn/GreenDaoUpgradeHelper)

参考资料:
[GreenDao官网](http://greenrobot.org/greendao/)
[一篇技术好文之Android数据库 GreenDao的使用完全解析](https://www.jianshu.com/p/53083f782ea2)

