---
title: Android数据库Room之二实体之间的关系
---

# 一.定义对象之间的关系
由于 SQLite 是关系型数据库，因此您可以定义各个实体之间的关系。尽管大多数对象关系映射库都允许实体对象互相引用，但 Room 明确禁止这样做。如需了解此决策背后的技术原因，请参阅[了解 Room 为何不允许对象引用](https://developer.android.com/training/data-storage/room/referencing-data#understand-no-object-references)。Room 的数据实体类跟数据库表是对应的，所以，有些表关系可以直接通过定义数据实体类之间的关系来实现，这样就可以无需编写 SQL 语句实现插入和查询过操作。
## 🐼两种可能的方法
在 Room 中，您可以通过两种方式定义和查询实体之间的关系：``使用具有嵌入式对象的中间数据类``或``具有多重映射返回值类型的关系型查询方法``来建立关系。
### 🐻中间数据类
在中间数据类方法中，您可以定义数据类，以便在 Room 实体之间建立关系。此数据类保存一个实体的实例与另一个实体的实例之间的对应方式（作为[嵌入式对象](https://developer.android.com/training/data-storage/room/relationships#nested-objects)）。然后，查询方法可以返回此数据类的实例，通过此数据类的实例我们就可以拿到对应实体的数据。

例如，您可以定义 `UserBook` 数据类来表示已借阅特定图书的图书馆用户，并定义一个查询方法用于从数据库中检索 `UserBook` 实例的列表：

```
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

### 🦝多重映射返回值类型
**注意**：Room 在 2.4 及更高版本中仅支持多重映射返回值类型。在多重映射返回值类型方法中，您无需定义任何其他数据类，而是根据所需的映射结构为您的方法定义[多重映射](https://en.wikipedia.org/wiki/Multimap)返回值类型，并直接在 SQL 查询中定义实体之间的关系。

例如，以下查询方法会返回 `User` 和 `Book` 实例的映射，用于表示已借阅特定图书的图书馆用户：

```
@Query(
    "SELECT * FROM user" +
    "JOIN book ON user.id = book.user_id"
)
fun loadUserAndBookNames(): Map<User, List<Book>>
```

### 🐵选择一种方法
Room 同时支持上述两种方法，您应使用最适合您的应用的一种方法。本部分讨论了您可能会倾向于使用其中一种的原因。中间数据类方法可让您避免编写复杂的 SQL 查询，但由于需要额外的数据类，它还可能会导致代码复杂性增加。简而言之，多重映射返回值类型方法需要 SQL 查询完成更多工作；而中间数据类方法需要代码完成更多工作。如果您没有使用中间数据类的特定理由，我们建议您使用多重映射返回值类型方法。如需详细了解此方法，请参阅[返回多重映射](https://developer.android.com/training/data-storage/room/accessing-data#multimap)。
**本文的其余部分演示了如何使用中间数据类方法定义关系。**

# 二.创建内嵌的对象
有时，我们希望将实体或Java对象（POJO）表示为数据库逻辑中的一个组合体，也就是让该对象包含其他对象的多个字段。在这种情况下，我们可以使用注解 [@Embedded](https://developer.android.google.cn/reference/android/arch/persistence/room/Embedded)，使用 `@Embedded` 注解标注对象，表示要将此对象分解成为数据表的子字段。这样就可以跟查询其他字段一样查询这些内嵌的字段。如下示例所示：

```
// 内嵌类
data class Coordinates (
  val latitude: Double,
  val longitude: Double
)

// 数据实体类
@Entity(tableName = "address")
data class Address(@PrimaryKey(autoGenerate = true) val id: Int?, val street: String,, @Embedded val coordinates: Coordinates)
```

以上的示例中，数据实体类 `Address` 内嵌了 `Coordinates` 类，在数据库中对应的表中，会将 `Coordinates` 类的所有字段都分解称为表的字段，最终数据库的表结构为:
![image.png](/images/b3d7be3eed81d50e494ae16319b254f1.webp)

注意事项：

1. 内嵌类内部还可以内嵌其他类达到套娃的目的。
2. 内嵌类可以不是数据实体类（也就是说被嵌套的类可以无需 `@Entity` 注解标注）。
3. 如果内嵌类跟数据实体属性名有冲突，必须通过 `@ColumnInfo` 注解重命名数据库表中的列名称（不是数据实体类也可以使用 `@ColumnInfo` 注解标注字段）。
4. 如果有多个内嵌类，必须保证内嵌类之间、内嵌类和数据实体类之间对应列名均唯一。

# 三.定义一对一关系
假设有一个音乐在线播放应用，用户在该应用中具有一个属于自己的歌曲库。每个用户只能有一个歌曲库，而且每个歌曲库恰好对应于一个用户。因此，User 实体和 Library 实体之间就应存在一种一对一的关系。

### 🐄第一步：创建两个数据实体类（父实体和子实体）

首先，为两个实体分别创建一个类。其中一个实体必须包含对另一个实体的主键的引用。

```
@Entity
data class User(
    @PrimaryKey val userId: Long,
    val name: String,
    val age: Int
)

// Library 类的userOwnerId属性变量对应 User 类的 userId 属性变量
@Entity
data class Library(
    @PrimaryKey val libraryId: Long,
    val userOwnerId: Long,
    val music:String
)
```

> **注意事项：定义一一对应关系的两个数据实体类，其中一个数据实体类中必须包含引用另个一数据实体类主键的属性变量。**

### 🦓第二步：定义一对一对应关系
如果要在获得所有的音乐库和它们对应的用户，如果要使用 Sqlite 完成此次查询  ，需要如下两个步骤:
1. 进行两次Sql查询，先查询出User表中所有的用户，然后在根据用户的userId在Library表中查询出所有的歌曲库:
   ```
   SELECT * FROM User
   SELECT * FROM Library WHERE userOwnerId IN (userId1, userId2, …)
   ```
2. 将查询从数据库中的查出来的数据映射到LibraryAndUser对象中  ，不同的LibraryAndUser组成List<LibraryAndUser>数据:
   创建了一个数据类 `LibraryAndUser`定义一个User字段和一个Library对象 ：
   ```
   data class LibraryAndUser(
       val user: User,
       val library: Library
   )
   ```
如果通过 Room 来获取到 `List<LibraryAndUser>` ，就不再不需要自己实现两次查询和对象映射操作，仅仅通过添加 `@Relation` 注解即可。在上面的例子中，由于Library 拥有用户的userid，所以在 歌曲库 变量上添加 `@Relation` 注解：指定 User 表中的 `userId` 和 Library 表中的 `userOwnerId` 是相对应的即可。

```
data class UserAndLibrary(
    @Embedded val user: User,
    @Relation(
         parentColumn = "userId",
         entityColumn = "userOwnerId"
    )
    val library: Library
)
```

### 🦄第三步：在 DAO 类中添加查询方法
最后，向 DAO 类添加一个方法，用于返回将父实体与子实体配对的数据类的所有实例。该方法需要 Room 运行两次查询，因此应向该方法添加 @Transaction (事务)注解，以确保整个操作以原子方式执行。
```
@Dao
interface MusicDao {
    @Transaction
    @Query("SELECT * FROM User")
    fun getUsersAndLibraries(): List<UserAndLibrary>
}
```
调用 DAO的 查询方法时， SQL 语句只需要查询父实体数据表，Room 会自动根据定义的关系查询子实体表。 经过以上步骤，就可以调用 DAO 中对应的接口进行连表查询结果了，查询返回的结果中包含一一对应的两个实体对象。

# 四.定义一对多关系

在音乐在线播放应用示例中，如果每个用户可以创建任意数量的播放列表，但每个播放列表只能由一个用户创建。因此，User (用户)实体和 Playlist (播放列表)实体之间应存在一种一对多关系。

### 🐇第一步：创建两个数据实体类（父实体和子实体）

首先，为两个实体分别创建一个类。与上个示例中一样，子实体必须包含一个变量，且该变量是对父实体的主键的引用。
```
@Entity
data class User(
    @PrimaryKey val userId: Long,
    val name: String,
    val age: Int
)

@Entity
data class Playlist(
    @PrimaryKey val playlistId: Long,
    //Playlist 类的userCreatorId属性变量对应 User 类的 userId 属性变量
    val userCreatorId: Long,
    val playlistName: String
)
```

### 🦨第二步：定义一对多对应关系

为了查询用户列表和对应的播放列表，必须先在两个实体之间建立一对多关系。为此，需要创建一个新的数据类，来描述这两个实体类之间的对应关系,其中每个实例都包含父实体的一个实例和与之对应的所有子实体实例的列表。父实体采用内嵌的方式，使用 `@Embedded` 注解标注  ，将 @Relation 注解添加到子实体的实例，同时将 parentColumn 设置为父实体主键列的名称，并将 entityColumn 设置为引用父实体主键的子实体列的名称。

```
data class UserWithPlaylists(
    @Embedded val user: User,
    @Relation(
          parentColumn = "userId",
          entityColumn = "userCreatorId"
    )
    val playlists: List<Playlist>
)
```

### 🦈第三步：在 DAO 中添加查询方法

最后，向 DAO 类添加一个方法，用于返回将父实体与子实体配对的数据类的所有实例。和上述情况一样该方法需要 Room 运行两次查询，因此应向该方法添加 @Transaction 注释，以确保整个操作以原子方式执行。

```
@Dao
interface MusicDao {
	@Transaction
	@Query("SELECT * FROM User")
	fun getUsersWithPlaylists(): List<UserWithPlaylists>
}
```

> **注意：编写 DAO 查询方法时， SQL 语句只需要查询父实体数据表，Room 会自动根据定义的关系查询子实体表。**

# 五.定义多对多关系

在音乐在线播放应用示例中，再次考虑用户定义的播放列表。 每个播放列表都可以包含多首歌曲，每首歌曲都可以包含在多个不同的播放列表中。因此，`Playlist`(播放列表) 实体和 `Song`(歌曲) 实体之间应存在多对多的关系。

多对多关系与其他类型的关系是有区别的，多对多关系在子实体中通常是没有父实体主键列的引用，而是创建一个第三方关联实体类（称之为交叉关系表）来表示两个实体之间的关联关系。交叉关系表中必须包含多对多关系中的每个实体类对应的数据表的主键列（即通过主键列进行关联）。


### 🐧第一步：创建两个实体类

首先，为您的两个实体分别创建一个类。

```
@Entity
data class Playlist(
    @PrimaryKey val playlistId: Long,
    val playlistName: String
)

@Entity
data class Song(
    @PrimaryKey val songId: Long,
    val songName: String,
    val artist: String
)


```

### 🐦第二步：创建第三方类（交叉关系表）

多对多关系与其他关系类型均不同的一点在于，子实体中通常不存在对父实体的引用。因此，需要创建第三个类来表示两个实体之间的[关联实体](https://en.wikipedia.org/wiki/Associative_entity)（即交叉引用表）。交叉引用表中必须包含表中表示的多对多关系中每个实体的主键列。在本例中，交叉引用表中的每一行都对应于 `Playlist` 实例和 `Song` 实例的配对，其中引用的歌曲包含在引用的播放列表中。

```
// 交叉关系表的主键列名必须跟对应的数据实体类主键列名一致，如果变量名跟列名不一致，可以使用 @columnInfo 注解指定列名
@Entity(primaryKeys = ["playlistId", "songId"])
data class PlaylistSongCrossRef(
	 // Playlist 实体类主键列名是playlistId， Song 实体类主键列名是songId
    val playlistId: Long,
    val songId: Long
)
```

> **注意事项：第三方类（交叉关系表）中必须包含多对多关系的每个数据实体类的主键列，而且必须保证列名跟数据实体的主键列名一致（否则编译会报错）。**

### 👽第三步：定义对应关系（根据查询需求）


这一步取决于您想如何查询这些相关实体。多对多关系跟其他对应关系不一样，需要根据查询需求定义相应的对应关系，其实就是将多对多关系，根据查询需求分解成一对多关系，查询需要的数据,于是就变成了以哪个数据实体类为父实体的问题。例如，查询某个播放列表所包含的歌曲，那么 ``Playlist``就是父实体， ``Song``就是子实体；反过来查询歌曲包含在哪些播放列表中，那么 ``Song``就成了父实体，而 ``Playlist``就成了子实体。于是，定义对应关系就跟定义一对多关系差不多的操作，唯一不同的就是需要在 `@Relation` 注解的 `associateBy` 属性指定第三方类（交叉关系表类）。

* 如果您想查询播放列表和每个播放列表所含歌曲的列表，则应创建一个新的数据类，其中包含单个 `Playlist` 对象，以及该播放列表所包含的所有 `Song` 对象的列表。
* 如果您想查询歌曲和每首歌曲所在播放列表的列表，则应创建一个新的数据类，其中包含单个 `Song` 对象，以及包含该歌曲的所有 `Playlist` 对象的列表。

在这两种情况下，都可以通过以下方法在实体之间建立关系：在上述每个类中的 [`@Relation`](https://developer.android.com/reference/kotlin/androidx/room/Relation) 注释中使用 [`associateBy`](https://developer.android.com/reference/kotlin/androidx/room/Relation#associateby) 属性来确定提供 `Playlist` 实体与 `Song` 实体之间关系的交叉引用实体。

```
// 查询播放列表的歌曲（查询 Playlist 表, 联合获取 Song 信息）
data class PlaylistWithSongs(
    @Embedded val playlist: Playlist,
    @Relation(
         parentColumn = "playlistId",
         entityColumn = "songId",
         associateBy = Junction(PlaylistSongCrossRef::class)
    )
    val songs: List<Song>
)
// 查询歌曲包含在哪些播放列表当中（查询 Song 表, 联合获取 Playlist 信息）
data class SongWithPlaylists(
    @Embedded val song: Song,
    @Relation(
         parentColumn = "songId",
         entityColumn = "playlistId",
         associateBy = Junction(PlaylistSongCrossRef::class)
    )
    val playlists: List<Playlist>
)
```

### 🐉第四步：在 DAO 中添加查询方法

最后，向 DAO 类添加一个方法，用于提供您的应用所需的查询功能。在前面提到，多对多关系的查询，限定条件之后，跟一对多的查询类似，但是需要注意的是，不同的限定条件，父类和子类会发生变化，查询的表也就不一样（查询父实体所对应的的表）。例如：查询某个播放列表所包含的歌曲（限定条件为播放列表）， ``Playlist``就是父实体， `Song` 就是子实体，此时查询 `Playlist` 表；反过来，查询歌曲包含在哪些播放列表中（限定条件是歌曲），那么 `Song` 就成了父实体，而 `Playlist` 就成了子实体，此时查询 `Song` 表。

* `getPlaylistsWithSongs`：该方法会查询数据库并返回查询到的所有 `PlaylistWithSongs` 对象。
* `getSongsWithPlaylists`：该方法会查询数据库并返回查询到的所有 `SongWithPlaylists` 对象。

这两个方法都需要 Room 运行两次查询，因此应为这两个方法添加 [`@Transaction`](https://developer.android.com/reference/kotlin/androidx/room/Transaction) 注释，以确保整个操作以原子方式执行。

```
@Dao
interface MusicDao {
	@Transaction
	@Query("SELECT * FROM Playlist")
	fun getPlaylistsWithSongs(): List<PlaylistWithSongs>
	
	@Transaction
	@Query("SELECT * FROM Song")
	fun getSongsWithPlaylists(): List<SongWithPlaylists>
}
```

**注意**：如果 `@Relation` 注解不适用于您的特定用例，如果无法满足，可以在需要在 SQL 查询中使用 `JOIN` 关键字进行手动关联确切的关联关系。如需详细了解如何手动查询多个表，请参阅[使用 Room DAO 访问数据](https://developer.android.com/training/data-storage/room/accessing-data#query-multiple-tables)。

# 六.定义嵌套关系
有时候，你需要查询三个或者更多相互关联的表，在这种情况下，你需要在这些表之间定义内嵌关系。所谓的嵌套关系，就是一个关系的查询中嵌套另一个关系的查询。在音乐在线播放应用示例中，假设您想要查询所有用户、每个用户的所有播放列表以及每个用户的各个播放列表中包含的所有歌曲。用户与播放列表之间存在[一对多关系](https://developer.android.com/training/data-storage/room/relationships#one-to-many)，而播放列表与歌曲之间存在[多对多关系](https://developer.android.com/training/data-storage/room/relationships#many-to-many)。简单来说就是要同时查询用户、播放列表、播放列表关联歌曲的数据。下面将详细讲解下如何定义嵌套关系。

### 🦏第一步：定义实体类

以下代码示例显示了代表这些实体以及播放列表与歌曲之间多对多关系的交叉引用表的类：

```
@Entity
data class User(
    @PrimaryKey val userId: Long,
    val name: String,
    val age: Int
)

@Entity
data class Playlist(
    @PrimaryKey val playlistId: Long,
    val userCreatorId: Long,
    val playlistName: String
)

@Entity
data class Song(
    @PrimaryKey val songId: Long,
    val songName: String,
    val artist: String
)


```

### 🐯第二步：定义多对多关系的交叉关系表

定义多对多关系的第三方类，也就是交叉关系表对应的数据实体类。

```
// 这里必须使用实体的主键一致的列名
@Entity(primaryKeys = ["playlistId", "songId"])
data class PlaylistSongCrossRef(
    val playlistId: Long,
    val songId: Long
)
```

### 🦁第三步：定义对应关系

首先，按照常规方法使用数据类和 [`@Relation`](https://developer.android.com/reference/kotlin/androidx/room/Relation) 注释在集合中的两个表格之间建立关系。以下示例展示了一个 `PlaylistWithSongs` 类，该类可在 `Playlist` 实体类和 `Song` 实体类之间建立多对多关系：

```
//查询播放列表的歌曲（查询 Playlist 表, 联合获取 Song 信息）
data class PlaylistWithSongs(
    @Embedded val playlist: Playlist,
    @Relation(
         parentColumn = "playlistId",
         entityColumn = "songId",
         associateBy = Junction(PlaylistSongCrossRef::class)
    )
    val songs: List<Song>
)
```

接下来是用户跟歌曲之间的关系，所以还需要再定义一个实体类，用于在集合中的另一个表与第一个关系类之间建立关系，并将现有关系嵌套到新关系中。这实体类 `User` 为父实体，歌曲与播放列表对应关系实体为子实体（即上面定义的 `PlaylistWithSongs` 实体为子实体）。在 `@Relation` 注解中，子实体与父实体主键对应的列名为 `User` 类中父实体的主键对应的列（`song` 为 `PlaylistWithSongs` 关系类的父实体）。

以下示例展示了一个 `UserWithPlaylistsAndSongs` 类，该类可在 `User` 实体类和 `PlaylistWithSongs` 关系类之间建立一对多关系：

```
data class UserWithPlaylistsAndSongs(
    @Embedded val user: User
    @Relation(
        entity = Playlist::class,
        parentColumn = "userId",
        entityColumn = "userCreatorId"
    )
    val playlists: List<PlaylistWithSongs>
)
```

`UserWithPlaylistsAndSongs` 类间接地在以下三个实体类之间建立了关系：`User`、`Playlist` 和 `Song`。

图展示了该关系。

![](/images/d2655d8c59ff6faaf8243c741fa83285.webp)
音乐在线播放应用示例中关系类的示意图。

如果集合中还有其他表，则可以创建类在剩余的每个表和关系类（此类可在之前的所有表之间建立关系）之间建立关系。这样会在您要查询的所有表之间创建一系列嵌套关系。

### 🐺第四步：在 DAO中 添加查询方法

最后，向 DAO 类添加一个方法，用于提供您的应用所需的查询功能。该方法需要 Room 运行多次查询，因此应添加 [`@Transaction`](https://developer.android.com/reference/kotlin/androidx/room/Transaction) 注释，以便确保整个操作以原子方式执行。查询结果为 `UserWithPlaylistsAndSongs` 关系实体类，所以 SQL 只需要查询 `UserWithPlaylistsAndSongs` 关系类中的父实体数据类对应的表即可。

```
@Dao
interface MusicDao {
	@Transaction
	@Query("SELECT * FROM User")
	fun getUsersWithPlaylistsAndSongs(): List<UserWithPlaylistsAndSongs>
}
```

> 注意事项：
>
> 1. 嵌套关系只能对第一层（SQL 所查询的表） 进行条件查询，如果需要更加复杂的条件查询，可以在 SQL 查询语句中使用 `JOIN` 关键字进行手动关联确切的关联关系，更多详情请参考： [Android Room 数据访问对象（DAO）详解](https://blog.csdn.net/yingaizhu/article/details/117573618#t5)；
> 2. 在定义对应关系时，`@Relation` 注解中，`parentColumn` 属性值为对应关系的父实体主键列，`entityColumn` 必须是内嵌的对应关系主实体的主键列。
> 3. 使用嵌套关系查询数据需要 Room 处理大量数据，可能会影响性能。因此，请在查询中尽量少用嵌套关系。

# 七.外键约束
### 🐶使用ForeignKey外键约束
外键的作用是是用来加强在表之间的约束  ，Room允许通过**外键(Foreign Key)**来表示Entity之间的关系。在room中使用[@ForeignKey](https://developer.android.google.cn/reference/androidx/room/ForeignKey)注解来关联两个实体对象的关系。
```
@Entity(foreignKeys = @ForeignKey(entity = User.class,
                                  parentColumns = "id",
                                  childColumns = "user_id"))
class Book {
    @PrimaryKey
    public int bookId;

    public String title;

    @ColumnInfo(name = "user_id")
    public int userId;
}
```

如上面代码所示，Book对象与User对象是属于的关系。Book中的user_id,对应User中的id。 那么当一个User对象被删除时， 对应的Book会发生什么呢？

`@ForeignKey`注解中有两个属性`onDelete`和`onUpdate`， 这两个属性对应`ForeignKey`中的`onDelete()`和`onUpdate()`  ， 通过这两个属性的值来设置当User对象被删除／更新时，Book对象作出的响应。这两个属性的可选值如下：

* `CASCADE`：User删除时对应Book一同删除； 更新时，关联的字段一同更新
* `NO_ACTION`：User删除时不做任何响应
* `RESTRICT`：禁止User的删除／更新。当User删除或更新时，Sqlite会立马报错。
* `SET_NULL`：当User删除时， Book中的userId会设为NULL
* `SET_DEFAULT`：与`SET_NULL`类似，当User删除时，Book中的userId会设为默认值

>外键的作用非常强大，因为它允许我们指定：引用的实体类更新时发生的情况。SQLite 中的外键会创建索引，并且会在更新或者删除表中数据时做级联操作。因此您要根据实际情况来判断是否使用外键功能。
### 🐂@ForeignKey和@Relation的区别
虽然这两个概念都用于为 Room 数据库提供结构，但它们的用例的不同之处在于：
- `@ForeignKey`用于在*插入/修改*数据时强制实施关系结构
-  `@Relation`用于在*检索/查看*数据时强制实施关系结构。

为了更好地理解ForeignKeys 的需求，请考虑以下示例：
```
@Entity
data class Artist(
    @PrimaryKey val artistId: Long,
    val name: String
)
@Entity
data class Album(
    @PrimaryKey val albumId: Long,
    val title: String,
    val artistId: Long
)
```
使用此数据库的应用程序有权假定**对于 Album** 表中的每一行，**Artist** 表中都存在相应的行。遗憾的是，如果用户使用外部工具编辑数据库，或者如果应用程序中存在 Bug，则可能会在 **Album** 表中插入与 **Artist** 表中的任何行都不对应的行。或者，可能会从“艺术家”（Artist） 表格中删除行，从而在“相册*表格中留下与*“艺术家*”中的任何剩余行都不对应的孤立行。这可能会导致应用程序在以后出现故障，或者至少使应用程序编码更加困难。

一种解决方案是向数据库架构添加 SQL 外键约束，以强制实施*艺术家*和*唱片集*表之间的关系。

```
@Entity
data class Artist(
    @PrimaryKey val id: Long,
    val name: String
)

@Entity(
    foreignKeys = [ForeignKey(
        entity = Artist::class,
        parentColumns = arrayOf("id"),
        childColumns = arrayOf("artistId"),
        onUpdate = ForeignKey.CASCADE,
        onDelete = ForeignKey.CASCADE
    )]
)
data class Album(
    @PrimaryKey val albumId: Long,
    val title: String,
    val artistId: Long
)
```

现在，每当您插入新专辑时，SQL都会检查是否存在具有该给定ID的艺术家，只有这样您才能继续交易。此外，如果您更新艺术家的信息或将其从*艺术家*表格中删除，SQL会检查该艺术家的任何专辑并更新/删除它们。这就是`ForeignKey.CASCADE`所起的作用。但这不会在查询期间自动使它们一起返回，因此请使用：`@Relation`
```
// 我们以前的数据类
@Entity
data class Artist(
    @PrimaryKey val id: Long,
    val name: String
)

@Entity(
    foreignKeys = [ForeignKey(
        entity = Artist::class,
        parentColumns = arrayOf("id"),
        childColumns = arrayOf("artistId"),
        onUpdate = ForeignKey.CASCADE,
        onDelete = ForeignKey.CASCADE
    )]
)
data class Album(
    @PrimaryKey val albumId: Long,
    val title: String,
    val artistId: Long
)

// 现在嵌入以实现高效查询
data class ArtistAndAlbums(
    @Embedded val artist: Artist,
    @Relation(
         parentColumn = "id",
         entityColumn = "artistId"
    )
    val album: List<Album> // <-- 这是一对多的关系，因为每个艺术家都有很多专辑，因此在这里返回一个列表
)
```

现在，您可以使用以下内容轻松获取艺术家及其专辑的列表：

```
@Dao
interface MusicDao{
    @Transaction 
    @Query("SELECT * FROM Artist")
    fun getArtistsAndAlbums(): List<ArtistAndAlbums>
}
```
以前，您必须编写长样板 SQL 查询才能加入查询并返回对应的数据关系。
>注意：需要注释才能使 SQLite 一次性执行两个搜索查询（一个在 Artist 表中查找，一个在 Album 表中查找），而不是单独执行。`@Transaction`





参考资料:
[Room官方文档](https://developer.android.com/training/data-storage/room)