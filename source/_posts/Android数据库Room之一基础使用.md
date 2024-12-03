---
title: Android数据库Room之一基础使用
date: 2020-06-10
categories: 
  - Android开发
---

# 一.Room简介
Room是Google推出的数据库框架，是一个 ORM (Object Relational Mapping)对象关系映射数据库、其底层还是对SQLite的封装。 使用ORM可以让开发者更加关注业务逻辑，而不是SQL 语句。在JavaWeb领域也有类似的ORM 数据库框架Hibernate、MyBatis等等。

### 1.Android平台数据库框架
在 Android 中常见的数据库框架：
* [Greendao ](https://github.com/greenrobot/greenDAO)
* [Realm ](https://github.com/realm/realm-java)
* [DBFlow](https://github.com/agrosner/DBFlow)
* [LitePal](https://github.com/guolindev/LitePal)
* [Jetpack-Room](https://developer.android.com/reference/androidx/room/package-summary)

🦝**Greendao**: 是 room 之前用得最广泛的 ORM 数据库框架，不过官方目前已经不再积极维护（官方在推新品 [ObjectBox](https://github.com/objectbox/objectbox-java) )在 ROOM,，出来以后据非官方数据统计多种场景下(插入、更新、删除)，ROOM 性能上也只是和 greendao 不相上下，强得有限，毕竟底层都还是 Android 的 SQLite 只能通过包装层和生成语句去优化。Greendao的缺点是配置复杂，不支持监听数据表/Kotlin/协程等特性。
🦁**Realm**: 不是基于 SQLite ，它是底层用C语言写的数据库引擎，号称速度比 SQLite 快 10 倍。跨平台，支持多种平台设备(Android/iOS/Mac/Windows)，支持RxJava/Kotlin， 但不支持嵌套类而且要求字段指定默认值， 自定义数据库引擎，因此会要求导入JNI库， 会导致apk体积增加， 函数设计比较复杂， 官方图形工具相对简陋但实时更新。
🦄**DBFlow**: 主要使用函数操作数据库， 学习成本高，原生支持数据库加密，支持监听数据库，支持协程/Kotlin/RxJava， 在国内比较冷门。
🐶**LitePal**: 是国内Android开发者郭霖开源并维护的，也是对SQLite数据库的再次封装，方便调用。
🐰**Room**: 是当前的主流数据库框架， 支持SQL语句， 操作数据库需要编写抽象函数， 由Google官方维护，它是JetPack组件中的数据库框架，支持嵌套对象，支持Kotlin 协程/RxJava，具备SQL语句高亮和编译期检查(具备AndroidStudio的支持)。

**综合所有的 Android 平台 ORM 数据库来看，ROOM 有优秀的效率、支持内存映射、支持与 LiveData 绑定 、编译期检查(Room会在编译的时候验证每个@Query和@Entity等，它不仅检查语法问题，还会检查是否有该表，这就意味着几乎没有任何运行时错误的风险) 并且最重要的是有着Google Android 官方团队去维护，所以 ORM ROOM 是当前最值得使用的Android数据库框架。**

### 2.Room的三个组件

**Room**主要由3个部分组成：

* [**Entity:**](https://developer.android.com/training/data-storage/room/defining-data.html)
  表示数据库中的表，数据实体，对应数据库中的表。
* [**DAO:**](https://developer.android.com/training/data-storage/room/accessing-data.html)
  包含用于访问数据库的方法，数据访问对象，包含访问数据库的方法，数据访问对象是Room的主要组件，负责定义访问数据库的方法。
* [**Database:**](https://developer.android.google.cn/reference/android/arch/persistence/room/Database)
  包含数据库持有者，并作为应用程序持久关系数据的基础连接的主要访问点：数据库扩展了RoomDatabase的抽象类。可以通过databaseBuilder或Room.inMemoryDatabaseBuilder获得它的一个实例。

![Room组件架构图](/images/d3c68a1489a57f9199abe051eaa582fa.webp)

# 二.Room使用

### 1.引入Room依赖

在project的build.gradle中加入google的Maven仓库(高版本的AS自动添加)：

```
allprojects {
    repositories {
        google()
    }
}

```

在app的build.gradle中添加依赖：

```
apply plugin: 'kotlin-kapt'//kotlin开启katp
dependencies {
    def room_version = "2.2.5"
    implementation "androidx.room:room-runtime:$room_version"
    // Kotlin 使用 kapt 替代 annotationProcessor
    kapt "androidx.room:room-compiler:$room_version"
    //Java用 annotationProcessor
    //annotationProcessor "androidx.room:room-compiler:$room_version" 
    //可选 - Kotlin扩展和协程支持
    //implementation "androidx.room:room-ktx:$room_version"
    //可选 - RxJava 支持
    //implementation "androidx.room:room-rxjava2:$room_version"
}
```

### 2.配置编译器选项(可选)

```
//配置编译器代码
android {
    ...
    defaultConfig {
        ...
        javaCompileOptions {
            annotationProcessorOptions {
                arguments += [
                    "room.schemaLocation":"$projectDir/schemas".toString(),
                    "room.incremental":"true",
                    "room.expandProjection":"true"]
            }
        }
    }
}
```

配置编译器解释

1. ``"room.schemaLocation":"$projectDir/schemas".toString():`` 的作用是将配置并启把据库架构导出json文件到指定目录。
2. ``"room.incremental":"true":``启用 Gradle 增量注解处理器。
3. ``"room.expandProjection":"true":`` 配置 Room 以重写查询，使其顶部星形投影在展开后仅包含 DAO 方法返回类型中定义的列。

如果配置了schemaLocation，编译后，会在对应路径生成schemas文件夹，json包含了各个版本的概要，表结构等信息：
![](/images/40d72af4335ce21b071905ef52d56c57.webp)


如果在创建数据库的时候未指定具体位置生成的位置则是在 data/data/包名/database 下，如果需要指定额外的位置则在上文数据库构建的时候传数据库名前面带上你需要指定的路径。
### 3.创建Entity（创建表）

```
@Entity(tableName = "Book")
class Book{
    @PrimaryKey(autoGenerate=true)
    var id :Int = 0
    
    @ColumnInfo(name = "book_name")
    var bookName:String? = null
        
    var anchor:String? = null
    
    @Ignore
    var price :Int = 0

}
```

创建表一般会用到下面几个注解：
**@Entity(tableName="表名称"):** @Entity表示定义数据库中的一个表，通常Room会使用类名作为数据库的表名，如果你希望自定义表名可以配置@Entity(tableName = "my_book")，注意：**SQLite中，表名是不区分大小写的。**

**@PrimaryKey(autoGenerate=true):** 定义主键 autoGenerate 用于设置主键自增，默认为false。

**@ColumnInfo(name = "别名"):** Room默认用变量名称作为数据库表的字段名称，如果你希望字段名称和变量名称不一样，则需要给变量添加@ColumnInfo注解。

**@Ignore:** 忽略该字段，加上该注解不会将该字段映射到数据库中去。

**索引和唯一性**:根据操作数据的方式可能需要通过索引来提高查询数据库的速度，通过@Entity添加indices属性，有些字段设置唯一性，可以通过@Index注解下设置unique为true。

```
@Entity(indices = [Index(value =["bookName"], unique = true)])
class Book {
    var bookName:String? = null
}
```

> ROOM要求每个数据库序列化字段为public访问权限。

### 4.创建Dao(表操作)

然后DAO接口，提供一些增删改查的方法。

```
@Dao
abstract class BookDao {

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    abstract fun insert(book: Book)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    abstract fun insert(books: List<Book>)
    
    @Delete
    abstract fun delete(book:Book)

    @Update
    abstract fun update(book:Book)

    @Query("select * from Book where id =:id")
    abstract fun queryById(id:Int) : Book

    @Query("select * from Book")
    abstract fun queryAll():List<Book>

    @Query("select count(*) from Book")
    abstract fun bookCount() : Int
    
    @Query("delete from Book")
    abstract fun deleteAll();
}
```

Room 使用注解处理器映射了数据库的增删改查，即 **@Insert**、**@Delete**、**@Update**、**@Query** 代表我们常用的插入、删除、更新、查询数据库操作。

@Query非常的强大，你可以编写任意sql语句并得到你想要的结果。

> 如果在query时返回值类型和查询的表名和返回值类型或查询的表名不相同时，在程序编译会编译失败，这也降低了程序在运行时出现的风险。

### 5.创建DataBase类(管理表)

使用 [@**Database**](https://developer.android.google.cn/reference/android/arch/persistence/room/Database) 注解的类应满足以下条件：

* 是一个继承于[**RoomDatabase**](https://developer.android.com/reference/androidx/room/RoomDatabase.html) 的抽象类。
* 在注解中包括与数据库相关联的实体列表。
* 包含一个没有参数的抽象方法并且返回一个带有注解的[@**Dao**](https://developer.android.com/reference/androidx/room/Dao.html)。

在运行时，我们可以通过调用 [Room.databaseBuilder()](https://developer.android.google.cn/reference/android/arch/persistence/room/Room#databaseBuilder%28android.content.Context,%20java.lang.Class%3CT%3E,%20java.lang.String%29)或 [Room.inMemoryDatabaseBuilder()](https://developer.android.google.cn/reference/android/arch/persistence/room/Room#inMemoryDatabaseBuilder%28android.content.Context,%20java.lang.Class%3CT%3E%29)
来获取 [Database](https://developer.android.google.cn/reference/android/arch/persistence/room/Database) 的实例。

`RoomDatabase`实例的内存开销较大，建议使用`单例模式`管理:

```
@Database(entities = [Book::class], version = 1)
abstract class AppRoomDataBase : RoomDatabase() {
        //创建DAO的抽象类
        abstract fun bookDao(): BookDao

        companion object {
                private val DATABASE_NAME = "simple_app.db"
                @Volatile
                private var databaseInstance: AppRoomDataBase? = null
                @Synchronized
                open fun getInstance(): RoomDaoManager {
                        if (databaseInstance == null) {
                                databaseInstance = Room.databaseBuilder(MyApplication.instance(),RoomDaoManager::class.java,DATABASE_NAME)
                                        .allowMainThreadQueries()//允许在主线程操作数据库，一般不推荐；设置这个后主线程调用增删改查不会报错，否则会报错
                                        .build()
                        }
                        return databaseInstance!!
                }
     }
}
```

* `@Database` 表示继承自`RoomDatabase`的抽象类，`entities`指定`Entities`表的实现类，`version`指定了DB版本。
* 必须提供获取`DAO`接口的抽象方法，比如上面定义的`bookDao()`，`RoomDatabase`将通过这个方法实例化`DAO`接口。
* `RoomDatabase`实例的内存开销较大，建议使用`单例模式`管理。
* 点击Build编译项目，Room会自动生成对应的_Impl实现类，此处将生成`AppRoomDataBase_Impl.java`文件。

> 注意:数据库的实例化是很昂贵的，所以建议我们使用单例模式来初始化，而且也很少情况下需要访问多个实例。

#### Room构建Builder相关API

构造数据库之前 build 提供了很多功能的 [API](https://developer.android.google.cn/reference/kotlin/androidx/room/RoomDatabase.Builder#summary) 给我们调用，其中包含一些相当重要的 API。我们需要对其了解:

```
Room.databaseBuilder(MyApplication.instance(),RoomDaoManager::class.java,DATABASE_NAME)
    // .xxx 
    // .xxx
    .build();
```

| 接口 | 释义 |
| --- | --- |
| addCallback | 数据库创建、打开、破坏性迁移的回调 |
| addMigrations | 数据库迁移 |
| addTypeConverter | 添加非基本数据类型的数据库转换器，例如 long 转 date |
| allowMainThreadQueries | 允许主线程访问数据库 |
| createFromAsset().createFromFile().createXX | 允许通过其他方式文件、流预填充数据库 |
| enableMultiInstanceInvalidation | 如果您的应用在多个进程中运行，请在数据库构建器调用中包含 enableMultiInstanceInvalidation()。这样，如果您在每个进程中都有一个 AppDatabase 实例，就可以在一个进程中使共享数据库文件失效，并且这种失效会自动传播到其他进程中的 AppDatabase 实例，默认不开启。 |
| fallbackToDestructiveMigration | 不提供数据库迁移，又不想引发 crash 。但是注意数据会丢失删除数据库重建 |
| fallbackToDestructiveMigrationOnDowngrade | 如果您仅在从较高数据库版本迁移到较低数据库版本时才希望 Room 回退到破坏性重新创建，请用该方法 |
| openHelperFactory | 设置数据库的工厂类，如果没有设置。则默认使用内置的 [FrameworkSQLiteOpenHelperFactory](https://developer.android.google.cn/reference/kotlin/androidx/sqlite/db/framework/FrameworkSQLiteOpenHelperFactory.html) |
| setAutoCloseTimeout | 启用一个数据库打开后空闲没有使用资源的自动关闭策略 |
| setJournalMode | 设置数据库的日志模式，如果使用内存数据库构建请忽略此值 |
| setQueryCallback | 每当数据库执行查询操作时候回调，不建议在生产环境使用 |
| setQueryExecutor | 设置查询的线程池一般不需要设置，会使用默认的 ArchTaskExecutor 内置线程池 |
| setTransactionExecutor | 设置事务线程池一般不需要设置，会使用查询方法的默认线程池，详可见源码 RoomDatabase.java#build() |

# 三.DAO的使用进阶

### 1.@Insert

`@Insert`支持设置冲突策略，默认为``OnConflictStrategy.ABORT``即插入相同数据会中止并回滚。还可以指定为其他策略:

* ``OnConflictStrategy.REPLACE`` 冲突时替换为新记录。
* ``OnConflictStrategy.IGNORE`` 忽略冲突(不建议使用)。
* ``OnConflictStrategy.ROLLBACK`` 废弃了，使用ABORT替代。
* ``OnConflictStrategy.FAIL`` 废弃了，使用ABORT替代。

`@Insert`修饰的方法的返回值可为空，也可为插入行的ID或ID列表:

```
fun insert(book: Book?)
fun insert(book: Book?): Long?
fun insert(vararg books: Book?): LongArray?
```

### 2.@Delete

和`@Insert`一样，支持不返回删除结果。

### 3.@Update

和`@Insert`一样支持设置冲突策略和定制返回更新结果。此外需要注意的是`@Update`操作将匹配参数的主键id去更新字段。

### 4.@Query

@Query指定不同的SQL语句即可获得相应的查询结果。在**编译阶段**就将验证语句是否正确，避免错误的查询语句影响到运行阶段。

- 查询所有字段

```
@Query("SELECT * FROM book")
```

- 查询指定字段

```
@Query("SELECT id, book_name, actor_name, post_year, review_score FROM book")
```

- 排序查询

```
@Query("SELECT * FROM book ORDER BY post_year DESC") 比如查询最近发行的书籍列表
```

- 匹配查询

```
@Query("SELECT * FROM book WHERE id = :id")
```

- 多字段匹配查询

```
@Query("SELECT * FROM book WHERE book_name LIKE :keyWord " + " OR author_name LIKE :keyWord") 比如查询名称和作者中**匹配**关键字的书籍
```

- 模糊查询

```
@Query("SELECT * FROM book WHERE book_name LIKE '%' || :keyWord || '%' " + " OR author_name LIKE '%' || :keyWord || '%'")  比如查询名称和作者中**包含**关键字的书籍
```

- 限制行数查询

```
@Query("SELECT * FROM book WHERE book_name LIKE :keyWord LIMIT 3") 比如查询名称匹配关键字的前三部书籍
```

- 参数引用查询

```
@Query("SELECT * FROM book WHERE review_score >= :minScore") 比如查询评分大于指定分数的书籍
```

- 多参数查询

```
@Query("SELECT * FROM book WHERE post_year BETWEEN :minYear AND :maxYear")  比如查询介于发行年份区间的书籍
```

- 不定参数查询*

```
@Query("SELECT * FROM book WHERE book_name IN (:keyWords)")
```

- Cursor查询

```
@Query("SELECT * FROM book WHERE book_name LIKE '%' || :keyWord || '%' LIMIT :limit")
fun searchMoveCursorByLimit(keyWord: String?, limit: Int): Cursor? 
```

> 注意：Cursor需要保证查询到的字段和取值一一对应，所以不推荐使用。

### 5.将简单参数传递给查询

大多数情况下，在DAO中定义的方法需要接受参数，根据这些参数执行过滤操作。Room 支持在查询中将方法参数用作绑定参数。
例如，以下代码定义了一个返回特定年龄以上的所有用户的方法：

```
@Dao
interface UserDao {
  //将minAge作为查询参数传递给Sql语句
  @Query("SELECT * FROM user WHERE age > :minAge")
  fun loadAllUsersOlderThan(minAge: Int): Array<User>
}  
```

### 6.将一组参数传递给查询
某些 DAO 方法可能要求您传入数量不定的参数，参数的数量要到运行时才知道。Room 知道参数何时表示集合，并根据提供的参数数量在运行时自动将其展开。
例如，以下代码定义了一个方法，该方法返回了部分地区的所有用户的相关信息：
```
@Dao
interface UserDao {
  //将regions集合作为查询参数传递给Sql语句
  @Query("SELECT * FROM user WHERE region IN (:regions)")
  fun loadUsersFromRegions(regions: List<String>): List<User>
}
```

### 7.查询多个表获取数据
有时候部分查询可能需要访问多个数据表才能计算出结果。可以在 SQL 查询中使用 `JOIN` 子句来引用多个表。
以下代码定义了一种方法将三个表联接在一起，以便将当前已出借的图书返回给特定用户：
```
@Dao
interface UserBookDao {
  @Query(
        "SELECT * FROM book " +
        "INNER JOIN loan ON loan.book_id = book.id " +
        "INNER JOIN user ON user.id = loan.user_id " +
        "WHERE user.name LIKE :userName"
  )
  fun findBooksBorrowedByNameSync(userName: String): List<Book>
  }
```
此外，您还可以定义简单对象以从多个联接表返回列的子集，如[返回表格列的子集](https://developer.android.com/training/data-storage/room/accessing-data#return-subset)中所述。
以下代码定义了一个 DAO，其中包含一个返回用户姓名和借阅图书名称的方法：
```
// 您也可以在单独的文件中定义此类
data class UserBook(val userName: String?, val bookName: String?)

@Dao
interface UserBookDao {
      @Query(
            "SELECT user.name AS userName, book.name AS bookName " +
            "FROM user, book " +
            "WHERE user.id = book.user_id"
      )
      fun loadUserAndBookNames(): LiveData<List<UserBook>>
}
```

### 8.查询实体之间的关系
由于 SQLite 是关系型数据库，因此您可以定义各个实体之间的关系。尽管大多数对象关系映射库都允许实体对象互相引用，但 Room 明确禁止这样做。如需了解此决策背后的技术原因，请参阅[了解 Room 为何不允许对象引用](https://developer.android.com/training/data-storage/room/referencing-data#understand-no-object-references)。Room 的数据实体类跟数据库表是对应的，所以，有些表关系可以直接通过定义数据实体类之间的关系来实现，这样就可以无需编写 SQL 语句实现插入和查询过操作。 在 Room 中，您可以通过两种方式定义和查询实体之间的关系：``使用具有嵌入式对象的中间数据类``或``具有多重映射返回值类型的关系型查询方法``来建立关系。
#### 🤖查询返回多重映射(推荐使用)
在 Room 2.4 及更高版本中，您还可以通过编写返回[多重映射](https://en.wikipedia.org/wiki/Multimap)的查询方法来查询多个表中的列，而无需定义其他数据类。
请参考[查询多个表](https://developer.android.com/training/data-storage/room/accessing-data#multiple-tables)部分中的示例。
您可以直接从您的查询方法返回 `User` 和 `Book` 的映射，而不是返回保存有 `User` 和 `Book` 实例配对的自定义数据类的实例列表。
```
@Dao
interface UserBookDao {
  @Query(
        "SELECT * FROM user" +
        "JOIN book ON user.id = book.user_id"
  )
  fun loadUserAndBookNames(): Map<User, List<Book>>
}
```
查询方法返回多重映射时，您可以编写使用 `GROUP BY` 子句的查询，以便利用 SQL 的功能进行高级计算和过滤。例如，您可以修改 `loadUserAndBookNames()` 方法，以便仅返回已借阅的三本或更多图书的用户：

```
@Dao
interface UserBookDao {
  @Query(
        "SELECT * FROM user" +
        "JOIN book ON user.id = book.user_id" +
        "GROUP BY user.name WHERE COUNT(book.id) >= 3"
  )
  fun loadUserAndBookNames(): Map<User, List<Book>>
}
```

如果您不需要映射整个对象，还可以通过在查询方法的 [`@MapInfo`](https://developer.android.com/reference/kotlin/androidx/room/MapInfo) 注解中设置 [`keyColumn`](https://developer.android.com/reference/kotlin/androidx/room/MapInfo#keycolumn) 和 [`valueColumn`](https://developer.android.com/reference/kotlin/androidx/room/MapInfo#valuecolumn) 属性，返回查询中特定列之间的映射：

```
@Dao
interface UserBookDao {
  @MapInfo(keyColumn = "userName", valueColumn = "bookName")
  @Query(
        "SELECT user.name AS username, book.name AS bookname FROM user" +
        "JOIN book ON user.id = book.user_id"
  )
  fun loadUserAndBookNames(): Map<String, List<String>>
}
```

#### 🐱‍👤通过中间数据类查询
这一块的内容比较多，存在一对一，一对多，多对多等结构，后续笔者会出一篇文章专门讲解这一块的知识。

# 四.Room结合Android组件使用
### 1.Rxjava和Room配合使用

```
//Rxjava2和Rxjava3 可以选择使用
def room_version = "2.3.0"
// optional - RxJava2 support for Room
implementation "androidx.room:room-rxjava2:$room_version"

// optional - RxJava3 support for Room
implementation "androidx.room:room-rxjava3:$room_version"
```

```
//定义使用Rxjava的方法
@Query("SELECT * FROM book where id = :id")
fun queryFlowable(id : Int): Flowable<Book?>?
```

### 2.LiveData和Room配合使用

```
//Livedata依赖
def lifecycle_version = "2.2.0"
implementation "androidx.lifecycle:lifecycle-viewmodel-ktx:$lifecycle_version"
```

```
//返回值使用Livedata
@Query("SELECT * FROM book where id = :id")
fun queryLiveData(id : Int): LiveData<Book?>?

//通dao对象调用查询的方法
bookDao?.queryLiveData(1)?.observe(this, Observer {
    Log.i("book-query","${it?.name}")
})

```

第一次添加观察者的时候会收到一次数据 onChanged 的回调，其次数据库中的 book 表的数据发生变化都会收到 onChanged 的观察回调，但是这里我们需要注意一个细节，如果你的 @insert 注解是使用的 replace 策略(OnConflictStrategy.REPLACE)，这样插入重复的数据也会导致事务的产生旧数据被替换插入 onChanged 也因为重复数据的插入频繁回调！

### 3.Flow和Room配合使用
可观察查询是指在查询引用的任何表发生更改时发出新值的读取操作。您可能需要用到可观察查询的一种情形是，帮助您在向底层数据库中插入项或者更新或移除其中的项时及时更新显示的列表项。下面是可观察查询的一些示例：
```
@Dao
interface UserDao {
      @Query("SELECT * FROM user WHERE id = :id")
      fun loadUserById(id: Int): Flow<User>

      @Query("SELECT * from user WHERE region IN (:regions)")
      fun loadUsersByRegion(regions: List<String>): Flow<List<User>>
}
```

**注意**：Room 中的可观察查询有一项重要限制 - 只要对表中的任何行进行更新（无论该行是否在结果集中），查询就会重新运行。通过应用相应库中的 `distinctUntilChanged()` 运算符 ，可以确保仅在实际查询结果发生更改时通知界面。
- [Fow流](https://kotlin.github.io/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/distinct-until-changed)
- [RxJava](http://reactivex.io/documentation/operators/distinct)
- [LiveData](https://developer.android.com/reference/androidx/lifecycle/Transformations#distinctUntilChanged(androidx.lifecycle.LiveData%3CX%3E))

# 五.Room数据库升级、降级和数据迁移
### 1.数据库升级和降级
在@Entities类里增加了新字段后，重新运行已创建过DB的demo会发生崩溃。 ``Room cannot verify the data integrity. Looks like you've changed schema but forgot to update the version number. ``这里的意思是提醒我们数据库对应的实体类发生了变化，但是没有更新数据库的版本号。将@Database的version升级为2之后再次运行仍然发生崩溃。 ``A migration from 1 to 2 was required but not found. Please provide the necessary Migration path via RoomDatabase.Builder.addMigration(Migration ...) or allow for destructive migrations via one of the RoomDatabase.Builder.fallbackToDestructiveMigration* methods.``根据报错的意思是，当数据库表的版本进行升级时，需要提供自定义的Migration进行处理，如果不提供自定义的Migration，可以调用`fallbackToDestructiveMigration()`允许升级失败破坏性地删除DB。

### 2.删除数据库并重建(不推荐)

不提供自定义Migration，又不想引发crash，那么可以试试这个：

```
database = Room.databaseBuilder(MyApplication.instance(),AppRoomDataBase::class.java,DB_NAME)
        .fallbackToDestructiveMigration()
        .build();
```

fallbackToDestructiveMigration方法表示Room启动时将检测version是否发生增加，如果有，那么将找到自定义Migration去执行特定的操作。如果没有自定义Migration， 因为设置了fallbackToDestructiveMigration()，将会删除数据库并重建，所有数据丢失。

### 3.自定义Migration升级版本

但是DB升级后，无论原有数据被删除还是重新初始化都是用户难以接受的。我们可以通过`addMigrations()`指定升级之后的迁移处理来达到保留旧数据和增加新字段的情况。 在Room中，数据库迁移使用的是Migration对象，定义如下：

```
public abstract class Migration {
    public final int startVersion;
    public final int endVersion;

    public Migration(int startVersion, int endVersion) {
        this.startVersion = startVersion;
        this.endVersion = endVersion;
    }

    public abstract void migrate(@NonNull SupportSQLiteDatabase database);
}
```

**startVersion**是旧版本号，**endVersion**是新版本号。数据库版本发生变更（如升级）会回调migrate函数，我们需要在此回调中编写版本变更的相关代码，例如创建表、添加列等等。

- addMigrations(Migration migrations…):该方法接收的是一个数组，因此可以对多个版本进行迁移处理。
- Migration(int startVersion， int endVersion):每次迁移都必须定义初始版本和目标版本。
- 在重写的migrate方法中执行更新的sql，同时需要在对应的Entity类中添加相同的字段，来保证字段相同。

例如需要给Book表添加一个评分的字段score，并且将数据库版本从版本2升级到版本3:

1. 在对应的Entity类中添加相同的字段:

   ```
   @Entity(tableName = "Book")
   class Book{
       ...    
       var score:String? = null
   }
   ```

2. 增加数据库version，例如上一个版本是2，增加了字段现在版本变成3:

   ```
   @Database(entities = [Book::class], version = 3)
   abstract class AppRoomDataBase : RoomDatabase() {
       ...
   }
   ```

3. 自定义Migration，实现迁移逻辑:

   ```
   val MIGRATION_2_3 = object : Migration(2, 3) {
       override fun migrate(database: SupportSQLiteDatabase) {
           //对Book表增加一个score字段
           database.execSQL("ALTER TABLE Book ADD COLUMN score TEXT NOT NULL DEFAULT ''")
       }
   }
   ```

4. 提供自定义的Migration:

   ```
   @Database(entities = [Book::class], version = 1)
   abstract class AppRoomDataBase : RoomDatabase() {
           //创建DAO的抽象类
           abstract fun bookDao(): BookDao

           val MIGRATION_2_3 = object : Migration(2, 3) {
               override fun migrate(database: SupportSQLiteDatabase) {
                   //对Book表增加一个score字段
                   database.execSQL("ALTER TABLE Book ADD COLUMN score TEXT NOT NULL 	DEFAULT ''")
               }
           }
       companion object {
               private val DATABASE_NAME = "simple_app.db"
               @Volatile
               private var databaseInstance: AppRoomDataBase? = null
               @Synchronized
               open fun getInstance(): RoomDaoManager {
                       if (databaseInstance == null) {
                               databaseInstance = Room.databaseBuilder(MyApplication.instance(),RoomDaoManager::class.java,DATABASE_NAME)
                                       .allowMainThreadQueries()//允许在主线程操作数据库，一般不推荐；设置这个后主线程调用增删改查不会报错，否则会报错
                                       .addMigrations(MIGRATION_2_3)  
                                       .build()
                       }
                       return databaseInstance!!
               }
            }
   }
   ```

注意：

* 数据库降级的话则是调用`fallbackToDestructiveMigrationOnDowngrade()`来指定在降级的时候删除原有DB，当然可以像上述那样提供自定义的Migration来进行迁移处理。
* 如果想要迁移数据，无论是升级还是降级，必须要给`@Database`的`version`指定正确的目标版本。

### 4.跨版本升级迁移

在用户使用App的过程中数据库的升级并不总是按部就班的从 `version: 1->2，2->3，3->4`。例如用户目前App的数据库版本号是1，并且2，3两个版本的app用户并没有更新下载，因此数据库并没有升级，目前最新的App的数据库版本是4，
用户直接下载最新的App进行升级，如果我们定义了`migrations：version 1 到 2， version 2 到 3， version 3 到 4`， Room 会一个接一个的触发所有 `migration`。

1. `version：1->2`:

    ```
    static final Migration MIGRATION_1_2 = new Migration(1, 2) {
        @Override
        public void migrate(SupportSQLiteDatabase database) {
            //do something
        }
    };
    ```

2. `version：2->3`:
    
    ```
    static final Migration MIGRATION_2_3 = new Migration(2, 3) {
        @Override
        public void migrate(SupportSQLiteDatabase database) {
          //do something
        }
    };
    ```

3. `version：3->4`:

    ```
    static final Migration MIGRATION_3_4 = new Migration(3, 4) {
        @Override
        public void migrate(SupportSQLiteDatabase database) {
          //do something
        }
    };
    ```

4. 把migration 添加到 Room database builder:

    ```
    database = Room.databaseBuilder(MyApplication.instance(),RoomDaoManager::class.java,DATABASE_NAME)
            .addMigrations(MIGRATION_1_2, MIGRATION_2_3, MIGRATION_3_4)
            .build();
    ```

Room 还可以处理大于 1 的版本增量：可以一次性定义一个从`1 到4 的 migration`，提升迁移的速度。

1. `version：1->4`:

    ```
    static final Migration MIGRATION_1_4 = new Migration(1, 4) {
        @Override
        public void migrate(SupportSQLiteDatabase database) {
          //do something
        }
    };
    ```

2. 接着，我们只需把它添加到 `migration` 列表中：

    ```
    database = Room.databaseBuilder(MyApplication.instance(),RoomDaoManager::class.java,DATABASE_NAME)
            .addMigrations(MIGRATION_1_2, MIGRATION_2_3, MIGRATION_3_4, MIGRATION_1_4)
            .build();
    ```

3. Room会优先执行MIGRATION_1_4里面的逻辑，其他的一步一步升级的逻辑不会执行。

4. 如果没有匹配到对应的升级Migration配置，则app 直接 crash为了防止crash，可添加fallbackToDestructiveMigration方法配置 直接删除所有的表，重新创建表:

    ```
    database = Room.databaseBuilder(MyApplication.instance(),RoomDaoManager::class.java,DATABASE_NAME)
            .addMigrations(MIGRATION_1_2, MIGRATION_2_3, MIGRATION_3_4, MIGRATION_1_4)
            .fallbackToDestructiveMigration()// 如果没有匹配到Migration，则直接删除所有的表，重新创建表
            .build();
    ```

# 六.Room数据库注解大全
@Entity

| 返回值 | 方法名 | 作用 | 
| - | - | - | 
| `ForeignKey[]` | `foreignKeys()` | `实体的外键约束列表` | 
| `String` | `tableName()` | `数据库表名，默认是类名` | 
| `Index[]`| `indices()` | `索引列表` | 
| `boolean` | `inheritSuperIndices()` | `如果设置为true，在该类的父类中定义的任何索引将被转移到当前实体` | 
| `String[]` | `ignoredColumns()` | `忽略的列名列表` |
| `String[]` | `primaryKeys()` | `主键列名的列表` |

@Dao

| 注解名称 | 参数类型 | 作用 | 
| - | - | - | 
| `@Query()` | `String` | `查询sql` | 
| `@Delete` | `Class` | `删除一条对应的实体` |
| `@Insert` | `参数1.Class 参数2.onConflict`| `1.添加一条对应的实体类 2.发生冲突的是做法(共五种策略，默认是事务回滚)` |

@Database

| 注解名称 | 参数类型 | 作用 |
| - | - | - | 
| `AutoMigration[]` | `autoMigrations()` | `可在此数据库上执行的自动迁移列表` | 
| `Class[]` | `entities()` | `数据库中包含的实体列表` |
| `boolean` | `exportSchema()` | `您可以设置注释处理程序参数(Room . schemalocation)来告诉Room将数据库模式导出到一个文件夹中` | 
| `int` | `version()` | `数据库版本` | 
| `Class[]`| `views()` | `数据库中包含的数据库视图列表。` |


参考资料:
[Room官方文档](https://developer.android.com/training/data-storage/room)