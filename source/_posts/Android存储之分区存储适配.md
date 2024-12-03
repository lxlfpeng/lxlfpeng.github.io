---
title: Android存储之分区存储适配
---

# 一.Android存储分区介绍

### 1.简介

Android 存储分为内部存储（Internal storage）和外部存储（External storage）。有许多用户认为外部存储意味着SD存储卡或外部硬盘，这是完全错误的认识。

### 2.内部存储

**内部存储是用于存储Android系统本身和应用程序的存储区域**，Android设备中的Android系统和应用程序都是存在该内部存储区，例如手机的/system/目录、/data/等目录。 如果没有这一块存储区域是无法运行Android系统和应用程序的。其中data/data/包名/目录是Android系统提供给应用存储数据的内部存储空间，由应用程序创建的SharedPreferences、Sqlite数据库、缓存文件等目录都是保存在该文件夹中。该目录只能由该应用程序自身访问，其他应用程序和用户无法访问存储在此空间中的文件，并且该目录会随着的应用的卸载而被移除。

```
//获取手机内部存储空间的绝对路径:/data
Environment.getDataDirectory().getAbsolutePath();
```

> 需要注意的一点是如果Android设备被获取到了最高权限(ROOT)那么是可以访问内部存储空间中的文件数据的!

### 2.外部存储

手机的内部存储空间通常不会很大，一旦手机的内部存储容量被用完， 可能会出现手机无法使用的情形。因此我们需要将一些比较大的媒体文件放置到机身外部存储中。在早先的手机中是具备一个SD存储卡槽的，插入SD存储卡，系统会将Sd储存卡的存储空间挂载成外部存储空间。不过现在大部分手机已经取消支持SD存储卡扩展功能了。取而代之的是手机会自带一个机身内置存储空间，这个机身存储和SD存储卡的功能是完全一样的，Android系统会将内置存储空间的一部分区域划分为内部存储，另一部分划分为外部存储空间，然后通过 Linux 文件挂载的方式将这些存储空间进行挂载。

```
//获取手机外部存储的路径：/storage/emulated/0
Environment.getExternalStorageDirectory().getAbsolutePath();
```

### 3.内部存储和外部存储的区别

上文中讲到在以前的安卓手机中内置存储（机身存储）就是内部存储，外部存储就是扩展的SD卡。但目前很多的中高端机器的自带的内置存储都是很大的储存空间了， 因此Android4.4系统及以上的手机将机身内置存储分为了”内部存储internal” 和”外部存储external”两个不同的储存区域，用来存储不同的数据。如果Android4.4系统及以上的手机还支持单独外接SD卡，那么外接的SD卡一定是外部存储。此时手机上是有两个外部存储空间的。那么如何去区分这两个外部存储?google官方给我们提供了getExternalFilesDirs这样一个API来获取多个外部存储空间， 它返回一个File数组，File数组中就包含了手机自身所带的外部存储和外接SD卡所定义的外部存储了。

```
if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.KITKAT) {
    File[] files = getExternalFilesDirs(Environment.MEDIA_MOUNTED);
    for(File file:files){
        Log.e("Environment", file.getAbsolutePath())
    }
```

>注意：Android手机是支持外接多个外部存储介质空间的，如果用户在设备上移除了介质，则外部存储可能变为不可用状态。 所以在使用外部存储执行任何工作之前， 最好调用 getExternalStorageState() 以检查介质是否可用。

```
//判断外部存储是否可用
if(Environment.MEDIA_MOUNTED.equals(Environment.getExternalStorageState())) {
    ...
}
```
![](/images/3ec191925fd40f626dec9583583c6c47.webp)
对于Android开发者来说只和外部存储和内部存储打交道，Android提供的开发接口也只是获取内部存储和外部存储的目录地址。而对开发者屏蔽了内置存储卡和外置SD卡相关操作。

**结论内部存储和外部存储可以是在同一块存储介质上面的，只是概念上做了区分，内部存储和外部存储是一块存储介质上的不同区域。**

# 二.Android应用存储目录
### 1.内部存储空间中的应用私有目录
对于设备中每一个安装的 App，系统都会在内部存储空间的 data/data 目录下以应用包名为名字自动创建与之对应的文件夹。这个文件夹包含了SharedPreferences 和 SQLiteDatabase 持久化应用相关数据等。该文件夹是应用的私有文件夹，其他应用（和用户）不能访问文件夹里面的内容的(Root用户除外)。每个应用访问自己的内部存储是不需要权限的。 当用户卸载该应用时，这些文件也会被移除。
Android SDK 提供有如下方法可以获取并操作内部存储空间下应用私有目录文件的方法，都位于 Application Context 中，供开发者直接调用：

- 获取当前应用包名文件夹下的files文件夹路径:
    ```
    context.getFilesDir().getAbsolutePath();
    ```
  返回结果:data/data/packagename/files

- 获取当前应用包名文件夹下cache文件夹路径:
    ```
    context.getCacheDir().getAbsolutePath();
    ```
  返回结果:data/data/packagename/cache

- 在内部存储空间内创建（或打开现有的）目录:
    ```
    context.getDir("setting", MODE_PRIVATE).getAbsolutePath();
    ```
  返回结果:data/data/packagename/setting

- 获取内部存储files路径下的所有文件名:
    ```
    context.fileList();
    ```
- 删除内部存储files路径下的文件:
    ```
    //返回true则表示删除成功
    context.deleteFile(filename);
    ```

要在files或者cache其中一个目录中创建新文件，可以使用File()构造函数，传递给File上述方法提供的指定内部存储目录的方法:

```
//保存内容到私有的files目录
public void save(String filename, String content)throws IOException{
    File file= new File(context.getFilesDir(), filename);
    FileOutputStream myfos= new  FileOutputStream(file);
    myfos.write(content.getBytes());
    myfos.close();
}
```

或者是读取文件:

```
//通过文件名来获取私有的files目录中的文件
public String get(String filename) throws IOException {
    File file= new File(context.getFilesDir(), filename);
    FileInputStream fis = new FileInputStream(file);
    ByteArrayOutputStream baos = new ByteArrayOutputStream();
    byte[] data = new byte[1024];
    int len = -1;
    while ((len = fis.read(data)) != -1) {
        baos.write(data, 0, len);
    }
    return new String(baos.toByteArray());
}

```

并且Android系统可以调用Context类中提供了一个openFileOutput()方法，以获取FileOutputStream来对文件进行操作。 openFileOutput()方法接受两个参数：

- 第一个参数是文件名，在文本创建的时候使用的就是这个名称，注意这里指定的文件名不可以包含路径（因为默认存储到/data/data/<packagename>/files/目录下）。
- 第二个参数是文件的操作模式，主要有两种：
  1. MODE_PRIVATE：默认的操作模式，表示当指定同样文件名的时候，当该文件名有内容时，再次调用会覆盖原内容。
  2. MODE_APPEND：表示该文件如果已存在就往文件里面追加内容。

调用 openFileOutput() 来获取 FileOutputStream，得到这个对象后就可以使用Java流的方式将数据写入到文件中了。 写入文件:

```
//保存内容到私有的files目录
public void save(String filename, String content)throws IOException{
    FileoutputStream myfos=context.openFileoutput(filename,Context.MODE_PRIVATE);
    myfos.write(content.getBytes());
    myfos.close();
}
```

读取文件:

```
//通过文件名来获取私有的files目录中的文件
public String get(String filename) throws IOException {
    FileInputStream fis = context.openFileInput(filename);
    ByteArrayOutputStream baos = new ByteArrayOutputStream();
    byte[] data = new byte[1024];
    int len = -1;
    while ((len = fis.read(data)) != -1) {
        baos.write(data, 0, len);
    }
    return new String(baos.toByteArray());
}
```

> 如果要将文件保存在data/data/packagename/cache目录中同样可以使用File进行保存，但是需要注意的一点是此目录适用于临时文件，应定期清理。如果磁盘空间不足，系统可能会删除cache中的文件，因此请确保在读取之前检查缓存文件是否存在。

### 2.外部存储空间中的应用私有目录

外部存储可以是外置SD卡，也可以是内置存储卡的部分分区。 外部存储可分为公共目录和私有目录，同样的操作外部存储的私有目录不再需要 READ_EXTERNAL_STORAGE 或 WRITE_EXTERNAL_STORAGE 权限。 Android SDK 中也提供有便捷的 API供开发人员直接操作外部存储空间下的应用私有目录：

- 获取某个应用在外部存储中的files路径
    ```
    context.getExternalFilesDir(type).getAbsolutePath();
    ```
  返回结果:/storage/emulated/0/Android/data/packagename/files

- 获取某个应用在外部存储中的cache路径
    ```
    context.getExternalCacheDir().getAbsolutePath();
    ```
  返回结果:/storage/emulated/0/Android/data/packagename/cache

当用户卸载应用时，此目录及其内容将被删除。此外，系统媒体扫描程序不会读取这些目录中的文件，因此不能从MediaStore内容提供程序访问这些文件。因此，如果你的媒体文件不需要其他应用使用，则应该存储在外部存储上的私有存储目录。


可以通过调用getExternalFilesDir()并向其传递一个名称来获取一个外部存储的私有目录。

```
public void save(String filename, String content)throws IOException{
    boolean canUse=Environment.getExternalStorageState().equals(Environment.MEDIA_MOUNTED);
    if(canUse){
      File file= new File(context.getExternalFilesDir(Environment.DIRECTORY_PICTURES), "c.txt");
      FileOutputStream myfos= new  FileOutputStream(file);
      myfos.write(content.getBytes());
      myfos.close();
    }
}
```
如果没有提前定义好子文件目录名，则可以调用 getExternalFilesDir()并传递 null，这将返回外部存储上应用程序私有目录的根目录。 type根据文件类型可传``系统预定义的子目录常量``  ，如图片Environment.DIRECTORY_PICTURES，此时返回``/storage/emulated/0/Android/data/包名/files/Pictures``。或者传null直接返回``/storage/emulated/0/Android/data/包名/files``。

>外部存储空间中的应用私有目录在用户卸载应用程序时会删除该目录。如果您保存的文件需要在用户卸载应用程序后仍然可用例如当您的应用程序下载照片并且用户应保留这些照片时，应该将文件保存到外部存储的公共目录中去。

### 3.外部存储空间中的公共目录

通常来说，应用涉及到的持久化数据分为两类：应用相关数据和应用无关数据。前者是指专供宿主 App 使用的数据信息，比如一些应用的配置信息，数据库信息，缓存文件等。当应用被卸载，这些信息也应该被随之删除，避免存储空间产生不必要的占用。应用无关的公共文件这类文件可被其他程序自由访问，当应用被卸载之后，文件仍然保留。比如相机类应用被卸载后，照片仍然存在。在Android中外部存储中的公共目录有 9 大类，均为系统创建的文件夹，如果操作外部存储的公共目录，还是要申请 READ_EXTERNAL_STORAGE 或 WRITE_EXTERNAL_STORAGE 等权限。开发人员可以通过 Environment 类提供的方法直接获取相应目录的绝对路径，传递不同的 type 参数类型即可：
```
Environment.getExternalStorageDirectory().getAbsolutePath()
//这个方法是获取外部存储的根路径 
```
```
Environment.getExternalStoragePublicDirectory(String type); 
//这个方法是获取外部存储的共享目录 
```
Environment 类提供诸多 type 参数的常量，比如：

- Environment.DIRECTORY_DCIM ： 数字相机拍摄的照片
- Environment.DIRECTORY_MUSIC：用户音乐
- Environment.DIRECTORY_PODCASTS：音频 / 视频的剪辑片段
- Environment.DIRECTORY_RINGTONES：铃声
- Environment.DIRECTORY_ALARMS：闹钟的声音
- Environment.DIRECTORY_PICTURES：所有的图片 (不包括那些用照相机拍摄的照片)
- Environment.DIRECTORY_MOVIES：所有的电影 (不包括那些用摄像机拍摄的视频) 和 Download / 其他下载的内容。

> 注意在Android10版本也就是api29以后Android官方开始推荐分区存储，该方案主要是对外部存储空间中的公共目录的文件操作做了相关的限制。

# 三.Android 10分区存储适配
### 1.什么是分区存储?
在上文中我们了解到，外部存储空间分为私有目录和公共目录，在Android10以前，应用程序通过获取READ_EXTERNAL_STORAGE 和 WRITE_EXTERNAL_STORAGE 权限。获得外部存储空间的权限以后直接通过``file path``读取和修改外部存储空间中任意的文件，当然也包括其他应用的外部私有目录文件，这样一来极易造成泄露用户隐私。而且很多应用会在外部存储根目录建一个自己应用的文件夹，用于存放应用的数据。这样会导致用户卸载后，应用数据不会随之删除。导致手机文件特别混乱，长期占用空间。其实 Android 早就提供了 getCacheDir()、getFilesDir()、getExternalFilesDir()、getExternalCacheDir() 等 API 供开发者使用操作应用的私有目录，但是大部分开发者并没有去使用这套规则，几乎所有的App都喜欢在SD卡的根目录下建立一个自己专属的目录，用来存放各类文件和数据。 为了解决这个问题，从 Android 10 开始，Google 添加了一个新特性 Scoped Storage，可以称之为分区存储。
分区存储的重点调整有两点:
- 第一点在于限制了访问外部存储的公共目录必须要需要通过 MediaStore 或者 Storage Access Framework（以下简称 SAF）来获取到文件的Uri来进行访问，不能通过``file path``来访问资源。
  其中媒体文件（图片，音频，视频）能通过 MediaStore 和 SAF 两种方式访问，非媒体文件只能通过 SAF 访问。
- 第二点在于限制了应用程序对外部存储空间的操作权限。就算是通过申请取READ_EXTERNAL_STORAGE 和 WRITE_EXTERNAL_STORAGE 权限后，也不能读写整个外部存储空间中的目录了。应用程序只能访问外部存储中的公共媒体目录， 这里的外部存储的公共目录仅是指android系统创建的几个大类的文件夹，例如 DCIM、Pictures、Alarms， Music， Notifications，Podcasts， Ringtones、Movies、Download等。而对于外部存储的非公共目录，例如外部存储的根目录，其他应用的外部存储中的私有目录等是无法进行访问和操作的。

总的来说分区存储主要有两点变更:1.访问外部储存的文件方式变更。2.访问外部储存的文件权限变更。

### 2.访问外部储存的文件方式变更
在Android 10.0 之前访问外部存储访问目录/文件可通过如下两个方法：
- 通过File路径访问：File路径可以直接构造文件路径也可以通过MediaStore获取文件路径。
- 通过Uri访问：Uri可以通过MediaStore或者SAF获取。

Android 10.0 之后访问外部存储的公共目录中的媒体文件即 `/storage/emulated/0` 目录下的文件，例如 DCIM、Pictures、Alarms， Music， Notifications，Podcasts， Ringtones、Movies、Download等。
必须通过 MediaStore 或者 Storage Access Framework（以下简称 SAF）获取到Uri，然后通过Uri进行访问。非媒体文件只能通过 SAF 获取到Uri进行访问。App无法通过路径File(filePath)直接访问、新建、删除、修改目录/文件等。

### 3.访问外部储存的文件权限变更
**Android 10.0 之前申请权限的操作：**
在Android10之前的系统中无论是通过MediaStore API或者是File Path方式向外部存储中读写数据都需要申请READ_EXTERNAL_STORAGE 和 WRITE_EXTERNAL_STORAGE 读写的权限。

**Android 10.0 之后无需申请权限的操作：**
应用通过 MediaStore API在指定的共享媒体目录下创建媒体文件，或者对该应用所创建的媒体文件集进行查询、修改、删除的操作，不需要申请READ_EXTERNAL_STORAGE 和 WRITE_EXTERNAL_STORAGE 读写的权限。因为在创建的时候系统会将我们的应用的 packageName 写入到系统文件数据库中的 owner_package_name 字段从而在后续的使用中判断这个文件是哪个应用创建的。（如果该应用卸载后重装，之前保存的文件将不属于该应用创建的文件）。

**需要申请READ_EXTERNAL_STORAGE 权限：**
通过 MediaStore API对其他应用在共享媒体目录下贡献的媒体文件(图片、音频、视频)进行查询时需要申请READ_EXTERNAL_STORAGE 权限，如果未申请该权限，通过ContentResolver查询不到其他应用贡献的文件Uri，仅能查询到自己应用贡献的文件。使用MediaStore API 时，就算READ_EXTERNAL_STORAGE 权限， 也仅允许读取其他应用共享的音频、视频和图片等媒体文件，并不允许访问其他应用创建的下载数据和非媒体文件(pdf、office、doc、txt等)。 在 Android 10 里唯一一种访问其他应用贡献的非媒体文件的途径是使用存储访问框架 (Storage Access Framework) 提供的文档选择器向用户申请操作指定的文件。

**需要申请 WRITE_EXTERNAL_STORAGE 权限：**
如果需要编辑修改甚至删除其他应用贡献的媒体文件，则需要申请 WRITE_EXTERNAL_STORAGE 权限。如果当应用没有 WRITE_EXTERNAL_STORAGE 权限时，去修改其他 App 的文件时，
则会 ``throw java.lang.SecurityException: xxxx has no access to content://media/external/images/media/52 ``的异常
当应用拥有了 WRITE_EXTERNAL_STORAGE 权限后，去修改其他应用贡献的媒体文件时，会 throw 另一个 ``Exception android.app.RecoverableSecurityException: xxxxxx has no access to content://media/external/images/media/52``如果我们将这个 RecoverableSecurityException 给 Catch 住，并向用户申请修改该文件的权限，用户操作同意后，我们就可以在 onActivityResult 回调中拿到Uri结果进行操作了。
```
try {
    editFile(editFileUri)
}catch (rse : RecoverableSecurityException){
    requestForOtherAppFiles(REQUEST_CODE_FOR_EDIT_IMAGE,rse)
}
private fun requestForOtherAppFiles(requestCode: Int, rse: RecoverableSecurityException){
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
        startIntentSenderForResult(
            rse.userAction.actionIntent.intentSender
            , requestCode,
            null, 0, 0, 0, null)
    }
}

override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
    super.onActivityResult(requestCode, resultCode, data)
    if (resultCode == Activity.RESULT_OK){
        when(requestCode){
            REQUEST_CODE_FOR_EDIT_IMAGE ->{
                editImage(editImageUri)
            }
            REQUEST_CODE_FOR_DELETE_IMAGE ->{
                contentResolver.delete(deleteImageUri,null,null)
            }
        }
    }
}
```
下面是关于分区存储权限和其他相关项目的表格:
| 类型 | 位置 | 访问应用自己生成的文件 | 访问其他应用生成的的文件 | 访问方法 | 卸载应用是否删除文件 |
| - | - | - | - | - | - |
| 外部存储 | Photo/ Video/ Audio/ | 无需权限  | 需要权限READ_EXTERNAL_STORAGE | MediaStore Ap | 否  |
| 外部存储 | Downloads            | 无需权限  | 无需权限 | 通过存储访问框架SAF，加载系统文件选择器 | 否   |
| 外部存储 | 应用特定的目录         | 无需权限  | 无法直接访问  | getExternalFilesDir()获取到属于应用自己的文件路径 | 是    |

### 4.避免分区存储适配的方式
如果应用程序还未做好分区适配，在 Android 10 得设备上，仍然可以通过以下两种手段避免分区存储：
**方式一:设置targetSdkVersion**
Android 一般升级功能的时候都会配合targetSdkVersion使用。只要targetSdkVersion<=28，分区存储功能就不会开启。也就是说如果你的项目指定的targetSdkVersion低于29，那么即使不做任何作用域存储方面的适配，你的项目也可以成功运行到Android 10及以上版本手机上。

**方式二:禁用分区存储**
如果你的targetSdkVersion已经指定成了29，假如你还不想进行作用域存储的适配，只需要在AndroidManifest.xml 里application标签下添加： ``android:requestLegacyExternalStorage="true"`` 可禁用分区存储：
```
<manifest ... >
  <application android:requestLegacyExternalStorage="true" ...>
    ...
  </application>
</manifest>
```
如上配置以后我们的程序运行在Android10及以下版本的设备上并不会开启分区存储。但是如果将targetSdkVersion修改为30就会强制开启分区存储，requestLegacyExternalStorage 会失效，如果没有适配分区存储，运行应用则会出现问题。 虽然又增加了 preserveLegacyExternalStorage 属性，对于覆盖安装的应用还能继续不使用分区存储，但是新安装得应用不能用。因此不想适配分区存储的方式就只剩下方式一了。

### 5.内部存储和外部存储的私有目录访问
应用私有目录包含内部存储空间中的应用私有目录和外部存储空间中的应用私有目录，这两块没有做相应的变更。还是和以前一样这两个应用私有目录并不需要添加任何权限就可以访问，并且可以通过路径File(filePath)直接访问、新建、删除、修改目录/文件等。 并且当对应的应用程序卸载以后这两个私有目录也会被移除。

>需要注意的是私有目录只能由对应的应用程序访问，(除Root权限外)该应用程序无法访问其他应用程序的内部存储空间中的应用私有目录和外部存储空间中的应用私有目录。

# 四.Android 11分区存储适配
### 1.简介
Android 11 (R) 在 Android 10 (Q) 中分区存储的基础上进行了调整，这里主要的变更有四点:
1. 访问外部储存的文件方式变更。
2. 针对文件管理应用的特殊权限。
3. 对其他应用提供的多个共享文件的操作权限。
4. SAF(Storage Access Framework)调整。

### 2.使用直接文件路径和原生库访问文件
Android 10 中要求所有应用都使用 MediaStore API 来创建或访问照片、视频和音乐等媒体文件。即使是在共享目录DCIM，Pictures，Movies等下也无法使用mkdir，mkdirs，createNewFile等api对文件进行操作。 但是鉴于很多深度依赖基于File Path操作文件的应用和第三方库是很难切换到使用MediaStore API 来。 因此在 Android 11 里，依赖File Path(原始文件路径)的API和库可以再次使用了，简单来说就是又可以通过 File()，mkDir()等API访问有权限访问的媒体文件了。在实际的运行中，依赖File Path(原始文件路径)的 I/O 请求会被重定向到使用 MediaStore API， 当使用这种方式访问本应用存储空间之外的文件时，重定向会造成性能影响，而且直接使用原始文件路径，并不会比使用 MediaStore API 有更多优势，因此Android还是强烈建议直接使用 MediaStore API。
>需要注意的是：此种方式只是访问文件的方式改变了，访问文件的权限并没有被修改。

### 3.针对文件管理应用的特殊权限
针对文件管理器以及一些备份类的应用，它们需要获得共享存储的更广泛的访问权限。Android 11 里引入了一个特别的权限叫做  **MANAGE_EXTERNAL_STORAGE** ，该权限将授权读写所有共享存储内容，这也将同时包含非媒体类型的文件。 但是获得这个权限的应用还是**无法访问其他应用的应用专属目录 (app-specific directory)**，无论是外部存储还是内部存储。 在 Android 11 中，通过Intent申请**MANAGE_EXTERNAL_STORAGE**权限，可以将用户引导至系统设置页面，让用户选择是否允许该应用 "访问所有文件" (All Files Access)。例如下面的两种应用可能会使用到该权限:
- 文件管理器 — 该类应用的主要功能是管理文件；
- 备份和恢复 — 该类应用需要访问大批量的文件 (比如切换设备的时候进行数据迁移，或者将数据备份到云端)。


**如下方法可以判断是否拥有MANAGE_EXTERNAL_STORAGE权限：**

```
Environment.isExternalStorageManager()
```

**声明权限方式如下：**

1. manifest中声明权限:
   ```
   <uses-permission android:name="android.permission.MANAGE_EXTERNAL_STORAGE"/>
   ```

2. 申请权限代码:
   ```
   if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
       startActivity(Intent(Settings.ACTION_MANAGE_ALL_FILES_ACCESS_PERMISSION))
   }
   ```

### 4.批量文件修改权限申请
上文说到,如果要对别的应用程序贡献的媒体文件进行修改，那么只有通过异常捕获者一种方式实现，这一种依赖异常捕获的方式本身就不是很合理，而且每次只能申请一个文件的修改权限。在Android 11向
**MediaStore API** 中添加了多种方法，用于简化特定媒体文件修改流程（例如在原位置编辑照片），分别是：

- **createWriteRequest()** 用户向应用授予对指定媒体文件组的写入访问权限的请求。
- **createFavoriteRequest()** 用户将设备上指定的媒体文件标记为“收藏”的请求。对该文件具有读取访问权限的任何应用都可以看到用户已将该文件标记为“收藏”。
- **createTrashRequest()** 用户将指定的媒体文件放入设备垃圾箱的请求。垃圾箱中的内容会在系统定义的时间段后被永久删除。
* **createDeleteRequest()** 用户立即永久删除指定的媒体文件（而不是先将其放入垃圾箱）的请求。

```
val urisToModify = listOf(uri,uri,...)
val editPendingIntent = MediaStore.createWriteRequest(contentResolver,
        urisToModify)

// 申请权限
startIntentSenderForResult(editPendingIntent.intentSender, EDIT_REQUEST_CODE,
    null, 0, 0, 0)

override fun onActivityResult(requestCode: Int, resultCode: Int,data: Intent?) {
    when (requestCode) {
        EDIT_REQUEST_CODE ->
            if (resultCode == Activity.RESULT_OK) {
                /*获得权限*/
            } else {
                /*未获得权限*/
            }
    }
}
```

传入uri的集合，获取用户的同意后，就可以进行批量操作了。

### 5.对 SAF(Storage Access Framework) 的更新
当Android10推出分区存储对广泛的存储访问进行限制后，一些开发者试图使用 Storage Access Framework (SAF) 遍历整个文件系统。但是，SAF 并不适用于广泛地访问共享存储内容。因此 ，Google对SAF进行了更新，限制了它对某些路径的可见性。

- SAF使用 ACTION_OPEN_DOCUMENT_TREE 或 ACTION_OPEN_DOCUMENT，无法浏览到Android/data/ 和 Android/obb/ 目录及其所有子目录。
- SAF使用 ACTION_OPEN_DOCUMENT_TREE无法授权访问存储根目录、Download文件夹。

# 五.总结
### 情况一:不需要进行分区存储适配
如果应用不需要分区存储适配，那么只需要将targetSdkVersion设置成小于等于28，或者targetSdkVersion=29，requestLegacyExternalStorage="true"。那么在这两种情况下那么程序无论是运行在Android10之上或者之下的设备，都无需进行分区存储适配。 可以继续通过获取READ_EXTERNAL_STORAGE 和 WRITE_EXTERNAL_STORAGE 权限，对外部存储中的所有文件进行操作。也可以继续可以使用``File path``方式在外部存储空间中进行文件操作。

### 情况二:targetSdkVersion=29 开启分区存储
如果应用的targetSdkVersion=29，并且没有配置requestLegacyExternalStorage="true"，那么就会开启分区存储。在代码中我们需要根据Build.VERSION.SDK_INT判断当前系统的版本做不同的适配。例如:
```
fun saveBitmapFile() {
    val bitmap = BitmapFactory.decodeResource(resources,R.mipmap.ic_launcher)
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
        // 拿到 MediaStore.Images 表的uri
        val tableUri = MediaStore.Images.Media.EXTERNAL_CONTENT_URI;
        // 创建图片索引
        val values = ContentValues()
        values.put(MediaStore.Images.Media.DISPLAY_NAME, "${System.currentTimeMillis()}.png")
        values.put(MediaStore.Images.Media.MIME_TYPE, "image/png")
        values.put(MediaStore.Images.Media.DATE_ADDED, System.currentTimeMillis())
        values.put(MediaStore.MediaColumns.RELATIVE_PATH, Environment.DIRECTORY_DCIM)
        // 将该索引信息插入数据表，获得图片的Uri
        val imageUri = contentResolver.insert(tableUri, values)
        try {
            // 通过图片uri获得输出流
            val outputStream = contentResolver.openOutputStream(imageUri!!)
            if (outputStream != null) {
                bitmap.compress(Bitmap.CompressFormat.PNG, 100, outputStream)
                outputStream.close()
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
    } else {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.WRITE_EXTERNAL_STORAGE), 0)
        } else {
            val fileName =
                "${Environment.getExternalStorageDirectory().path}${File.separator}${Environment.DIRECTORY_DCIM}${File.separator}${System.currentTimeMillis()}.png"
            val filePic = File(fileName)
            try {
                val fos: FileOutputStream = FileOutputStream(filePic)
                bitmap.compress(Bitmap.CompressFormat.JPEG, 100, fos)
                fos.flush()
                fos.close()
                // 插入图库
            } catch (e: IOException) {
                e.printStackTrace()

            }
        }
    }
}

```
上面代码通过Build.VERSION.SDK_INT判断当前系统，如果程序运行在Android10及以上版本，无法使用FilePath对文件进行操作，这里用的MediaStore API获取Uri然后将图片进行插入操作，并且如果是对应用程序自己创建的媒体文件完成各种操作是不需要文件读写权限就可以的。如果需要访问别的应用贡献的媒体文件，则需要添加READ_EXTERNAL_STORAGE 权限。如果要对别的应用贡献的媒体文件做修改删除等操作，需要通过异常捕获机制捕获RecoverableSecurityException异常来申请修改的权限。如果程序运行在Android10及以下版本上，无论是访问自己创建的文件媒体文件还是别的应用创建的媒体文件都需要添加储存权限，因此首先需要获取WRITE_EXTERNAL_STORAGE写权限，并且可以利用FilePath对文件进行操作。

### 情况二:targetSdkVersion=30 开启分区存储
如果应用targetSdkVersion设置成了30，那么也需要对应用进行分区存储适配。上文说到在Android11上面又可以使用FilePath对共享的文件进行操作了，但是Android10又不支持FilePath对共享的文件的操作， 此时可以在AndroidManifest.xml 里application标签下添加：``android:requestLegacyExternalStorage="true"`` 可禁用分区存储在Android10上面开启，我们就可以不针对Android10进行单独适配了。
```
fun buttonClick(view: View) {
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
        saveBitmapFile()
    } else {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.WRITE_EXTERNAL_STORAGE), 0)
        } else {
            saveBitmapFile()
        }
    }
}

fun saveBitmapFile() {
    val bitmap = BitmapFactory.decodeResource(
        resources,
        R.mipmap.ic_launcher
    )

    val fileName =
        "${Environment.getExternalStorageDirectory().path}${File.separator}${Environment.DIRECTORY_DCIM}${File.separator}${System.currentTimeMillis()}.png"
    val filePic = File(fileName)
    try {
        val fos: FileOutputStream = FileOutputStream(filePic)
        bitmap.compress(Bitmap.CompressFormat.JPEG, 100, fos)
        fos.flush()
        fos.close()
        ToastUtil.showToastShort("成功!!!")
        // 插入图库
    } catch (e: IOException) {
        e.printStackTrace()
        ToastUtil.showToastShort("失败!!!"+e.message)
    }
}
```
这样可以在所有的系统版本上面都可以使用FilePath对文件进行操作。关于文件访问权限的变更需要参照上文，通过Build.VERSION.SDK_INT判断当前系统 分别对Android10及以上设备和Android10以下设备进行分别处理。

# 六.其它
### 1.切换媒体文件待处理状态
如果应用操作可能非常耗时（例如写入文件），那么在我们操作文件期间应该避免让其他应用有处理文件的机会。我们可以通过将 `ContentValue.put(MediaStore.Audio.Media.IS_PENDING, 1)` 标记的值设为 1 来获取此独占访问权限。
这样就只有我们的的应用可以操作该文件，直到我们的应用将 IS_PENDING 的值改回 0。

#### 照片中的位置信息
一些图片会包含位置信息，因为位置对于用户属于敏感信息， Android 10 应用在分区存储模式下图片位置信息默认获取不到，应用通过以下两项设置可以获取图片位置信息，在manifest 中申请 ``ACCESS_MEDIA_LOCATION ``调用 MediaStore setRequireOriginal(Uri uri) 接口更新图片Uri。

#参考资料
[Android MediaStore Api 使用](https://ppting.me/2020/04/19/2020_04_19_how_to_use_Android_MediaStore_Api/)
[Android 11新特性，Scoped Storage又有了新花样](https://guolin.blog.csdn.net/article/details/113954552)
[Android 10适配要点，作用域存储](https://guolin.blog.csdn.net/article/details/105419420)