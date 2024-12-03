---
title: ExoPlayer添加Ffmpeg扩展实现软解功能
date: 2022-05-12
categories: 
  - Android开发
---

# 一.准备环境
有时候Exoplayer自带的解码器不支持一些特殊的格式或者编码，此时我们可以通过给Exoplayer添加Ffmpeg扩展实现软解来支持这些编码。
## 工具版本
1. 系统:Ubuntu 20.04.3 LTS。
2. Exoplayer源码:r2.18.1版本。
3. NDK环境版本:NDK r21。
4. Cmaker版本:3.23.3。
5. Ffmpeg版本:4.2.2。

## 安装好编译环境
1. 下载[AndroidSdk](https://developer.android.google.cn/studio/intro/update#sdk-manager)并配置好环境，本文用的SDK版本为30。
2. 下载[Exoplayer](https://github.com/google/ExoPlayer)2.18.1版本源码。
3. 下载[NDK r21 ](https://github.com/android/ndk/wiki/Unsupported-Downloads)，配置好环境。
4. 下载[CMake](https://cmake.org/download/)3.23.3版本，配置好环境。
5. 下载[ffmpeg](https://github.com/FFmpeg/FFmpeg)4.2.2版本，配置好环境。

# 二.编译FFmpeg源码
1. 设置变量名为FFMPEG_MODULE_PATH的 shell 变量：
```
cd "Exoplayer工程目录"
FFMPEG_MODULE_PATH="$(pwd)/extensions/ffmpeg/src/main"
```
2. 设置变量名为NDK_PATH的 shell 变量：
```
NDK_PATH="NDK的安装目录"
```
3. 设置主机平台变量（Linux 使用linux-x86_64 对于Mac OS X 使用 darwin-x86_64 ）：
```
HOST_PLATFORM="linux-x86_64"
```
4. 设置FFMPEG_PATH的Shell变量：
```
cd "Ffmpeg工程目录"
FFMPEG_PATH="$(pwd)"
```
5. 现在添加解码器，可以使用命令中的空格添加多个解码器。例如，我们现在将添加3个解码器：mp3，aac和ac3：
```
ENABLED_DECODERS=(mp3 aac ac3)
```
>有关可用解码器的详细信息以及它们支持的格式，请参阅支持的[格式页面](https://exoplayer.dev/supported-formats.html#ffmpeg-extension)。
6. 在 FFmpeg 模块目录中添加指向 FFmpeg 源代码的链接：
```
cd "${FFMPEG_MODULE_PATH}/jni" && \
ln -s "$FFMPEG_PATH" ffmpeg
```
如果报错``file exists``可以使用如下命令：
```
cd "${FFMPEG_MODULE_PATH}/jni" && \
ln -sf "$FFMPEG_PATH" ffmpeg
```
7. 使用Ndk编译FFmpeg源码：
```
cd "${FFMPEG_MODULE_PATH}/jni" && \
./build_ffmpeg.sh \
  "${FFMPEG_MODULE_PATH}" "${NDK_PATH}" "${HOST_PLATFORM}" "${ENABLED_DECODERS[@]}"
```
>如果您需要为不同的体系结构构建脚本或者配置ffmpeg编译参数，则可以编辑构建脚本文件：build_ffmpeg.sh脚本，默认支持``armeabi-v7a，arm64-v8a，x86，x86_64``

8. 等待build_ffmpeg.sh编译脚本，结束，可以在``ExoPlayer/extensions/ffmpeg/src/main/jni/ffmpeg``目录下面生成了``android-libs``目录。

# 三.交叉编译JNI接口
在完成上述步骤以后，我们编译好的源码并不能直接在Android系统上使用，因为还未进行过交叉编译。 
1. 使用如下命令交叉编译并生成 aar 文件:
```
cd "Exoplayer工程目录"
./gradlew extension-ffmpeg:assembleRelease
```
2. 生成成功后，可以在 ffmpeg 生成文件夹中获取 aar 并将其导入到项目中。
```
/ExoPlayer/extensions/ffmpeg/buildout/output/aar
```
使用 gradle 将 aar 库导入到项目中。

# 四.在自己的项目中使用编译好的aar
1. 依赖之前编译好的aar:

```
implementation files('libs/extension-ffmpeg-release.aar')
```

2. 新建FfmpegRenderersFactory，并打开这个扩展:

```
class FfmpegRenderersFactory extends DefaultRenderersFactory {

    public FfmpegRenderersFactory(Context context) {
        super(context);
        setExtensionRendererMode(EXTENSION_RENDERER_MODE_PREFER);
    }

    @Override
    protected void buildAudioRenderers(Context context, int extensionRendererMode, MediaCodecSelector mediaCodecSelector, boolean enableDecoderFallback, AudioSink audioSink, Handler eventHandler, AudioRendererEventListener eventListener, ArrayList<Renderer> out) {
        out.add(new FfmpegAudioRenderer());
        super.buildAudioRenderers(context, extensionRendererMode, mediaCodecSelector, enableDecoderFallback, audioSink, eventHandler, eventListener, out);

    }
}

```

3. 播放器实例化:

```
ExoPlayer.Builder(MyApp.instance.applicationContext,new FfmpegRenderersFactory())
```

4. 播放链接:

```
val url = ""
val mediaItem: MediaItem = MediaItem.fromUri(url)
player.setMediaItem(mediaItem)
player.prepare()
player.play()
```
