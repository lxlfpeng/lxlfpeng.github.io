---
title: Android音视频开发之ijkplayer
---

# 一.Ijkplayer
ijk的导入方式有两种，第一种是使用gradle导入ijkplayer发布到jcenter，已经打包好的依赖包，第二种是去[github](https://links.jianshu.com/go?to=https%3A%2F%2Fgithub.com)中下载[ijkplayer](https://links.jianshu.com/go?to=https%3A%2F%2Fgithub.com%2FBilibili%2Fijkplayer)源码，自己进行编译。
### 1.gradle方式导入：
```
 # required, enough for most devices.
    implementation 'tv.danmaku.ijk.media:ijkplayer-java:0.8.8' 
    implementation 'tv.danmaku.ijk.media:ijkplayer-armv7a:0.8.8'

    # Other ABIs: optional
    implementation 'tv.danmaku.ijk.media:ijkplayer-armv5:0.8.8'
    implementation 'tv.danmaku.ijk.media:ijkplayer-arm64:0.8.8'
    implementation 'tv.danmaku.ijk.media:ijkplayer-x86:0.8.8'
    implementation 'tv.danmaku.ijk.media:ijkplayer-x86_64:0.8.8'

    # ExoPlayer as IMediaPlayer: optional, experimental
    implementation 'tv.danmaku.ijk.media:ijkplayer-exo:0.8.8' 
```
### 2.自行编译:
如果我们需要获取更多的视频格式支持（比如mkv，rmvb等）,或是要支持https都需要自行进行编译。一般在Linux os或是Mac Os上进行编译，Windows上面编译的话坑比较多，不建议。
- 准备linux系统 ubuntu14.04
- 安装 git
- 安装 vim(vimcdoc-1.5.0.tar.gz)
- 安装 jdk(jdk-8u151-linux-x64.tar.gz)
- 安装 ndk(android-ndk-r10e-linux-x86_64.bin)
- 配置jdk、sdk和ndk环境
- ijkplayer 编译
- 将已编译源码导入 android studio
![编译完成以后的目录结构](https://upload-images.jianshu.io/upload_images/3067896-37b6aaaea11e5ea6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
其中
- ijkplayer-java是核心代码必须添加，IjkMediaPlayer就在这里面。
- ijkplayer-armv7a是armeabi-v7a下的so库，
- ijkplayer-armv5是armeabi下的so库，
- ijkplayer-arm64是arm64-v8a下的so库，
- ijkplayer-x86是x86下的so库，
- ijkplayer-x86_64是x86_64下的so库
- ijkplayer-exo是谷歌下的IjkExoMediaPlayer
根据项目选择添加即可，一般so只需要一套``armeabi-v7a``就可以了。
# 二.使用
Android系统播放器的使用是``MediaPlayer + Surface``，Surface可以通过``SurfaceView``或``TextureView``获取。
ijkplayer-example中封装了一个类``IjkVideoView,IjkVideoView``中演示了三种播放器实现的调用

``IjkExoMediaPlayer``在Ijkplayer-exo中对google exoplayer的调用封装
``AndroidMediaPlayer``对android系统播放器MediaPlayer的调用封装
``IjkMediaPlayer``在Ijkplayer-java中对ffmpeg的调用封装

### 1.入门使用
##### (1.)在布局中添加播放控件。
```
<com.wshunli.ijkplayer.demo.widget.IjkVideoView
    android:id="@+id/ijkvideoview"
    android:layout_width="match_parent"
    android:layout_height="match_parent">
</com.wshunli.ijkplayer.demo.widget.IjkVideoView>
```
##### (2.)然后在 Activity 中使用就可以了
```
    IjkVideoView ijkVideoView;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        ijkVideoView = findViewById(R.id.ijkvideoview);
        ijkVideoView.setVideoURI(Uri.parse("http://demo-videos.qnsdk.com/movies/qiniu.mp4"));
        //ijkVideoView.setVideoURI(Uri.parse("http://qthttp.apple.com.edgesuite.net/1010qwoeiuryfg/sl.m3u8"));
        ijkVideoView.start();
    }
```
# 二.自定义播放器
官方提供的Demo只是演示视频播放的基本操作，对于视频播放的控制(MediaController)、全屏等操作，还要自己动手做。

# 三.ijkplayer播放视频Http和Https切换以后播放报错，无法播放
### 1.问题描述
在使用ijkplayer开发视频播放器时，视频是连续播放的（也就是上一段播放完成直接播放下一段视频）一直都是没有问题的。今天偶然间发现有的时候部分视频无法正常播放。查看日志信息，报错信息为：
```
E/tv.danmaku.ijk.media.player.IjkMediaPlayer: Error (-10000,0)
E/IJKMEDIA: Option ijkiomanager not found.
```
经过排查分析发现了规律：当首次播放的视频地址是http开头的，等该视频播放以后，切换到https开头的视频是无法播放的，反之亦如此。
### 2.猜测
可能是dns_cache_clear这个设置非首次播放时被还原,所以导致这样的问题产生。
### 3.解决方案
```
ijkPlayer.setOption(IjkMediaPlayer.OPT_CATEGORY_FORMAT, "dns_cache_clear", 1);
```

# 开源音视频播放器UI方案
[GSYVideoPlayer](https://github.com/CarGuo/GSYVideoPlayer)
[DKVideoPlayer](https://github.com/Doikki/DKVideoPlayer)
[Android视频直播、点播播放器哪家强？](https://www.jianshu.com/p/5dd4db66ae69)
[ijkplayer 详尽编译过程](https://blog.csdn.net/junhuahouse/article/details/79194069)
[ijkplayer编译so库真没那么难](https://blog.csdn.net/coder_pig/article/details/79134625)
[ijkplayer编译so文件支持更多格式](https://jessiekate.gitee.io/2019/02/16/IjkplayerSo/)
[IjkPlayer播放器秒开优化以及常用Option设置](https://www.jianshu.com/p/843c86a9e9ad)
[ijkPlayer主流程分析](https://www.jianshu.com/p/a11c724c5b2b)
[音乐播放器实践：MediaPlayer和IjkPlayer方案对比使用](https://kevinwu.cn/p/bdcf2466/#%E5%9C%A8Android%E7%B3%BB%E7%BB%9F%E4%B8%AD%E6%92%AD%E6%94%BE%E5%A3%B0%E9%9F%B3)
