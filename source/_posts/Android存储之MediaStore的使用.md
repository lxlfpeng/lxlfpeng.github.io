---
title: Android存储之MediaStore的使用
date: 2021-10-19
categories: 
  - Android开发
tags:
  - Android存储
  - Android分区存储
---

### Android系统内容提供者ContentProvider
安卓系统会在每次开机之后``扫描所有文件并分类整理存入数据库``，这个数据库保存了手机上存储的所有文件的信息。该数据库文件存放在Android设备的``/data/data/com.android.providers.media/databases``或``/data/data/com.android.providers.media.module/databases``目录当中，该目录下有两个数据库文件分别是**internal.db**(内部存储数据库文件)和**external.db**(外部存储数据库文件)， 这两个数据库文件中的数据表和表结构都大体相似，区别在于internal.db是用来存放内部存储中的文件信息的，而external.db是用来存储外部存储中的文件信息的。因此可以通过访问这两个数据库获取例如媒体文件(音频、视频、图片)等的文件信息， 而不必通过遍历媒体文件的方式来获取文件信息。但是在android设备中是禁止应用程序直接对这个数据进行直接操作的，而是将这个数据库的操作通过**ContentProvider(内容提供者)**将数据操作提供出来， 如要要对ContentProvider中的数据进行操作，可以通过**ContentResolver(数据调用者)** 对象结合Uri进行调用 来实现 。 ContentResolver(数据调用者)可以实现与ContentProvider进行通信，然后再通过ContentResolver调用ContentProvider的添加(insert)、删除(delete)、查询(query)、修改(update)等操作的同名方法，从而让ContentProvider对象接收数据请求、执行请求的操作并返回结果，这是一套标准的Android内容提供者数据模型。

### 为什么要使用ContentProvider(内容提供者)来实现这一功能呢?
1. Android设备系统中有些数据很重要，不能让别的应用程序随便访问并操作，对于需要用到这些数据的应用程序，可以通过ContentProvider这个机制，提供安全的数据访问操作方式。
2. ContentProvider还有一个重要的特点就是它是可以使得某些数据可以被跨进程访问，会自动处理安全性和跨进程通信。
3. Android系统通过ContentProvider暴露自己的数据，可以使得开发者在开发时无需知道数据是如何存储的，是使用数据库还是使用文件?开发者只需要通过这一套标准及统一的接口和数据打交道。

### ContentResolver如何使用?
获取ContentResolver实例:
```
val mResolver = context.getContentResolver();
```

ContentResolver实例获得后，就可以进行各种增删改查的方法 ，ContentResolver类也提供了与ContentProvider类相对应的四个方法可供调用：
| 返回值| 函数声明|说明|
| -|- |-|
| final Uri    | insert(Uri url, ContentValues values)|该方法用于往ContentProvider添加数据。|
| final int    | delete(Uri url, String where, String[] selectionArgs)|该方法用于从ContentProvider删除数据。|
| final Cursor | query(Uri uri, String[] projection, String selection, String[] selectionArgs, String sortOrder)|该方法用于从ContentProvider中获取数据。|
| final int    | update(Uri uri, ContentValues values, String where, String[] selectionArgs)| 该方法用于更新ContentProvider中的数据。|

ContentResolver是通过Uri来查询ContentProvider中提供的数据的。因此想操作ContentProvider，必须要知道内容提供者的Uri，在正确得到Uri之后，就可以通过ContentResolver对象来操作ContentProvider中的数据了。

### 什么是Uri?
上文中提到了Android提供内容的叫ContentProvider，那么在Android中怎么区分各个Provider？有的是提供联系人的，有的是提供图片的，有的是提供视频的等等。所以就需要有一个唯一的标识来标识这个Provider，Uri(通用资源标识符 Universal Resource Identifier)就是起到了这个标识的作用。每一个ContentProvider都会有一个唯一的Uri地址，通过这个Uri标识可以获取到ContentProvider和其中的数据，然后进行数据操作。
ContentProvider使用的Uri语法结构如下：
```
content://media/external/images/media
```
- **content://** 是通用前缀，表示该Uri用于ContentProvider定位资源。
- **authority** 是授权者名称，用来确定具体由哪一个ContentProvider提供资源。因此一般authority都由类的小写全称组成，以保证唯一性。
- **data_path** 是数据路径，用来确定请求的是哪个数据集。
- **id** 是数据编号，用来请求单条数据。如果是多条这个字段忽略。


对于系统已经提供了如通讯录、多媒体、短信等的URI，可以直接用ContentResolver调用这些URI，对系统数据库进行增删改查等操作，从而保证整个Android设备中数据的统一。

### 如何获取Uri?

以``content://media/external/images/media``为例，其URI有三种写法：

```
Uri uri1 = Uri.parse("content://media/external/images/media");
Uri uri2 = MediaStore.Images.Media.getContentUri("external");
Uri uri3 = MediaStore.Images.Media.EXTERNAL_CONTENT_URI;
```

Android 提供了 MediaStore 类来对数据库的的多媒体数据进行封装。

我们知道Android系统中的每一种媒体文件有两种地址描述方式:

* 第一种模式，在Android中，ContentProvider是用来存储和获取公共数据的统一接口，Content Provider为每一类资源分配了URI地址比如图片的Uri地址就包括``MediaStore.Images.Media.INTERNAL_CONTENT_URI``和``MediaStore.Images.Media.EXTERNAL_CONTENT_URI``这两个地址，其值分别是``content://media/internal/images/media``和``content://media/external/images/media``，对应内部库和外部库地址。每一张图片的地址基本上是上面的基础URL地址下加上图片的内部ID。例如外部存储上的图片ID为52，其对应的Uri地址就是 content://media/external/images/media/52. 知道了这个地址，基本上就可以操作这张图片的所有信息了。同样，对于其他多媒体文件例如外部库的音频 Uri 地址为 **MediaStore.Audio.Media.EXTERNAL_CONTENT_URI** ，其它 Uri 地址都是类似的。
* 另外一种描述文件地址标识就是传统的文件路径模式了。比如一张存储卡上的图片地址可能描述为：/mnt/sdcard/images/52.jpg。其实这个路径存储在文件储存库中的data字段中，有了这点关联，可以在这两种模式下进行任意切换。


通过上文可以知道Android为多媒体提供的ContentProvider的Uri都记录在MediaStore这个类里。MediaStore获取文件信息，是通过文件的mime-type来获取的，也就说文件储存库中有mime-type这个字段。

**MediaStore内部类**
-  class MediaStore.Audio：所有音频内容的类。
-  class MediaStore.Files：文件储存库中所有文件的索引，包括非媒体文件和媒体文件类。
-  class MediaStore.Images：所有图片内容的类。
-  interface MediaStore.MediaColumns：文件储存库中表的公共字段。
-  class MediaStore.Video：所有视频内容的类。


**MediaStore内部类对外提供的多媒体Uri常量有如下**
- MediaStore.Audio.Media.EXTERNAL_CONTENT_URI：存储在手机外部存储器上的音频文件Uri路径。
- MediaStore.Audio.Media.INTERNAL_CONTENT_URI：存储在手机内部存储器上的音频文件Uri路径。
- MediaStore.Images.Media.EXTERNAL_CONTENT_URI：存储在手机外部存储器上的图片文件Uri路径。
- MediaStore.Images.Media.INTERNAL_CONTENT_URI：存储在手机内部存储器上的图片文件Uri路径。
- MediaStore.Video.Media.EXTERNAL_CONTENT_URI：存储在手机外部存储器上的视频文件Uri路径。
- MediaStore.Video.Media.INTERNAL_CONTENT_URI：存储在手机内部存储器上的视频文件Uri路径。

>注意：MediaStore.Downloads.EXTERNAL_CONTENT_URI是Android10版本新增API，用于创建、访问非媒体文件。

Android系统给我们定义好了许多的媒体文件对应的URI路径如下表:
| 媒体类型 | Uri路径|MediaStore内部类常量|默认存储目录 | 允许存储目录|
| - | - |- |  - | - |
| Image(图片)    | content://media/external/images/media|MediaStore.Images.Media.EXTERNAL_CONTENT_URI |Pictures| DCIM、Pictures|
| Audio(音频)    | content://media/external/audio/media |MediaStore.Audio.Media.EXTERNAL_CONTENT_URI |Music| Alarms、Music、Notifications、Podcasts、Ringtones |
| Video(视频)    | content://media/external/video/media |MediaStore.Video.Media.EXTERNAL_CONTENT_URI |Movies| DCIM 、Movies|
| Download(下载文件) | content://media/external/downloads|MediaStore.Downloads.EXTERNAL_CONTENT_URI |Download| Download|


有了对应的Uri 地址，我们可以通过**ContentResolver**调用添加(insert)、删除(delete)、查询(query)、 修改(update)等操作了。

### 使用ContentResolver查询数据

有了 Uri 地址，我们可以通过**ContentResolver**的 *query()* 方法来获取到 Cursor，从而获取到数据库资源。
```
public final Cursor query (Uri uri, String[] projection,String selection,String[] selectionArgs, String sortOrder)
```
ContentResolver的query方法接受几个参数，参数意义如下:
- Uri：这个Uri代表要查询的内容提供者的Uri。上文说到多媒体类型的Uri一般都直接从MediaStore里取得，例如我要取所有图片的信息，就必须利用MediaStore.Images.Media.EXTERNAL_CONTENT_URI这个Uri。
- projection： 代表告诉Provider要返回的字段内容（列Column），用一个String数组来表示。用null表示返回Provider的所有字段内容（列Column）。
- selection：相当于SQL语句中的where子句，就是代表查询条件。null表示不进行添加筛选查询。
- selectArgs：如果selection里有？这个符号时，这里可以以实际值代替这个问号。如果Selections这个没有？的话，那么这个String数组可以为null。
- sortOrder：说明查询结果按什么来排序。相当于SQL语句中的Order by，升序 asc /降序 desc，null为默认排序。

示例:
```
//查找所有图片的信息
Cursor cursor = contentResolver.query(MediaStore.Images.Media.EXTERNAL_CONTENT_URI,
        null,
        null,
        null,
        null);

//查找所有图片的信息的DISPLAY_NAME字段
Cursor cursor = contentResolver.query(MediaStore.Images.Media.EXTERNAL_CONTENT_URI,
        new String[]{MediaStore.Images.Media.DISPLAY_NAME},
        null,
        null,
        null);

//查找图片名字叫“xx.png”的图片信息,null表示不进行筛选。
Cursor cursor = contentResolver.query(MediaStore.Images.Media.EXTERNAL_CONTENT_URI,
        new String[]{MediaStore.Images.Media.DISPLAY_NAME},
        //第三个参数设置条件，相当于SQL语句中的where。
        //null表示不进行筛选。
        MediaStore.Images.Media.DISPLAY_NAME + "='xx.png'",
        null,
        null);
        
//查找图片名字叫“xx.png”的图片信息,如果在selection参数里面有？，那么你在selectionArgs写的数据就会替换掉？，
 Cursor cursor = contentResolver.query(MediaStore.Images.Media.EXTERNAL_CONTENT_URI,
        new String[]{MediaStore.Images.Media.DISPLAY_NAME},
        MediaStore.Images.Media.DISPLAY_NAME + "=?",
        new String[]{"xx.png"},
        null);
        
//默认排序是升序。注意：desc前有空格
Cursor cursor = contentResolver.query(MediaStore.Images.Media.EXTERNAL_CONTENT_URI,
        null,
        null,
        null,
        ContactsContract.Contacts._ID + " DESC");
```
上面就是各个参数的意义，它返回的查询结果一个Cursor结果集。那么如何使用Cursor对象获取数据?
Cursor就是游标，把查询到的结果集封装在一个Cursor对象当中。我们知道只要是数据表都是可以通过行和列定位到具体的位置然后数据将其取出，Cursor也不例外，可以通过``cursor.moveToNext()``让行向后移动，然后根据``getColumnIndex(String columnName)``获取到列名的索引位置。有了每一行的的列名索引位置就可以就可以取出每一行中对应的数据了。当然这些数据类型也是多种多样的，Cursor也给我们提供了以下的方法去获取不同类型的值:
- 以字节数组的形式返回请求列的值：byte[] getBlob(int columnIndex)
- 以字符串形式返回请求列的值：String getString(int columnIndex)
- 以整数形式返回请求列的值：int getInt(int columnIndex)
- 以 long 形式返回请求列的值：long getLong(int columnIndex)
- 以浮点数形式返回请求列的值：float getFloat(int columnIndex)
- 以双精度形式返回请求列的值：double getDouble(int columnIndex)
- 返回给定列值的数据类型：int getType(int columnIndex)
- 列值是否为空：boolean isNull(int columnIndex)
- 以短形式返回请求列的值：short getShort(int columnIndex)

示例:使用ContentResolver通过Uri获取图片文件相关的信息集Cursor，然后通过Cursor取出图片文件相关的信息:
```
// 先拿到图片提供者的Uri
val imageUri = MediaStore.Images.Media.EXTERNAL_CONTENT_URI
// 需要获取图片数据表中的哪几列信息，注意这里需要和cursor取出的列名相对应否则会出现空指针
val projection = arrayOf(
    //获取ID列的数据
    MediaStore.Images.Media._ID,
    //获取MIME_TYPE列的值
    MediaStore.Images.Media.MIME_TYPE,
    //获取DISPLAY_NAME列的值
    MediaStore.Images.Media.DISPLAY_NAME
)

// 查询条件：因为是查询全部图片，传null
//String selection = MediaStore.Images.Media.DISPLAY_NAME +"= ?";
// 条件参数：因为是查询全部图片，传null
//String[] args = new String[] {“xxx.png”}
// 排序：可以添加排序
// val order = MediaStore.Files.FileColumns._ID + "DESC"
// 开始查询
val cursor = contentResolver.query(imageUri, projection, null, null, null)

//获取我们需要的数据在数据的第几列，这里需要和projection查询的数据对应起来，因为cursor结果集只包含projection的列信息，否则会出现空指针
if (cursor != null) {
    // 获取id字段是第几列
    val idIndex = cursor.getColumnIndexOrThrow(MediaStore.Images.Media._ID)
    val mimeTypeIndex = cursor.getColumnIndexOrThrow(MediaStore.Images.Media.MIME_TYPE)
    val displayNameIndex = cursor.getColumnIndex(MediaStore.Images.Media.DISPLAY_NAME)

    //循环取出cursor每一行的数据
    while (cursor.moveToNext()) {
        //根据列的坐标，取出对应行数的数据
        val id = cursor.getLong(idIndex)
        //根据列的坐标，取出对应行数的数据
        val type = cursor.getString(mimeTypeIndex)
        //根据列的坐标，取出对应行数的数据
        val disName = cursor.getString(displayNameIndex)
        //根据ID和图片提供者的Uri可以合成图片的Uri
        val imageUri = ContentUris.withAppendedId(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, id)
        //TODO
    }
    //关闭游标
    cursor.close()
}
```
通过上面的例子，可以获取到手机外部存储中所有的图片文件信息的ID、MIME_TYPE、DISPLAY_NAME等信息，如果要获取到文件大小等其他的信息也是可以的，只需要在projection集合中添加对应的列名然后，在cursor中找到每一行对应的列的索引值就可以取出对应的值，这些列名可以在MediaStore.MediaColumns取公共常量字段，也可以根据文件类型的不同在MediaStore的内部类中取值:
图片文件比较常见的列名有:
-  MediaStore.Images.Media._ID：磁盘上文件的路径
-  MediaStore.Images.Media.DATA：磁盘上文件的路径
-  MediaStore.Images.Media.DATE_ADDED：文件添加到media provider的时间（单位秒）
-  MediaStore.Images.Media.DATE_MODIFIED：文件最后一次修改单元的时间
-  MediaStore.Images.Media.DISPLAY_NAME：文件的显示名称
-  MediaStore.Images.Media.HEIGHT：图像/视频的高度，以像素为单位
-  MediaStore.Images.Media.MIME_TYPE：文件的MIME类型
-  MediaStore.Images.Media.SIZE：文件的字节大小
-  MediaStore.Images.Media.TITLE：标题
-  MediaStore.Images.Media.WIDTH：图像/视频的宽度，以像素为单位。

视频文件比较常见的列名有:
- MediaStore.Video.Media.TITLE  名称
- MediaStore.Video.Media.DURATION 总时长
- MediaStore.Video.Media.DATA 地址
- MediaStore.Video.Media.SIZE 大小
- MediaStore.Video.Media.WIDTH：视频的宽度，以像素为单位。
- MediaStore.Video.Media.HEIGHT：视频的高度，以像素为单位

音频文件比较常见的列名有:
- MediaStore.Audio.Media.TITLE：歌名
- MediaStore.Audio.Media.ARTIST：歌手
- MediaStore.Audio.Media.DURATION：总时长
- MediaStore.Audio.Media.DATA：地址
- MediaStore.Audio.Media.SIZE：大小

### 使用ContentResolver插入数据
如果需要插入数据只需要调用``contentResolver.insert(uri, contentValues)``;构造一个 ContentValues 对象，通过 ContentResolver.insert 插入到对应的目录中，该方法会返回一个 Uri，通过对该 Uri 进行文件流写入即可:
```
private fun saveImage(bitmap: Bitmap){
    val values = ContentValues()
    val insertUri = contentResolver.insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI,values)
    insertUri?.let {
        contentResolver.openOutputStream(it).use {outputStream->
            bitmap.compress(Bitmap.CompressFormat.PNG,100,outputStream)
        }
    }
}
```
ContentValues类和Bundle类很类似，都是使用HashMap的泛型形式来存储的，并且都是HashMap<String, Object>()。通过ContentValues可以设置列的数据，和上文中提到的一样可以在MediaStore.MediaColumns中
取公共常量字段也可以在MediaStore.MediaColumns取公共常量字段:
```
private fun saveImage(bitmap: Bitmap){
    val values = ContentValues().apply {
      //设置文件的 MimeType
      put(MediaStore.Images.Media.MIME_TYPE,"image/png")
      //指定保存的文件名，
      put(MediaStore.Images.Media.DISPLAY_NAME,"${System.currentTimeMillis()}.png")
      //指定保存的文件目录,如果不设置这个值，则会被默认保存到对应的媒体类型的文件夹下，
      if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
           put(MediaStore.Images.Media.RELATIVE_PATH,"${Environment.DIRECTORY_PICTURES}/DemoPicture")
      } else {
           put(MediaStore.MediaColumns.DATA,"${Environment.getExternalStorageDirectory().path}${File.separator}${Environment.DIRECTORY_DCIM}${File.separator}${System.currentTimeMillis()}.png")
      }
     
    }
    //插入文件数据库并获取到文件的Uri
    val insertUri = contentResolver.insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI,values)
    
    insertUri?.let {
        //通过outputStream将图片文件内容写入Url
        contentResolver.openOutputStream(it).use {outputStream->
            bitmap.compress(Bitmap.CompressFormat.PNG,100,outputStream)
        }
    }
}
```
需要注意的有点:
1. 是对于 Android 中的媒体类型，应该按照不同的MimeType放到对应的公共目录媒体文件夹下:

| MimeType      | 对应文件夹                                        |
| - | - |
| 图片(image/*) | DCIM,Pictures                                     |
| 音频(audio/*) | Alarms, Music, Notifications, Podcasts, Ringtones |
| 视频(video/*) | Movies                                            |
| 文档(file/*)  | Documents,Download                                |

当然，这些也都可以通过 MediaStore 放到 `Downloads` 文件夹下

2. 是MediaStore.Images.Media.RELATIVE_PATH这个值如果不设置，则系统会取当前的时间戳作为文件名例如，图片文件(mimeType = image/*)会被保存到Pictures(Environment#DIRECTORY_PICTURES) 中，需要注意的是，不能将文件放置到不对应的顶级文件夹下，比如将一个 mimeType 为 audio/mpeg 放大 Pictures 这样的行为是不被允许的，也就是如果设置 MIME_TYPE = audia/* 并将 RELATIVE_PATH 设置为 Environment#DIRECTORY_PICTURES 这样是会 Throw IllegalArgumentException 的。

3. 是MediaStore.Images.Media.RELATIVE_PATH是在Android10才被添加进来的因此需要做好不同版本的适配。

