---
title: Android音视频开发总结之二Android平台采集、编码、解码
date: 2019-06-17
categories: 
  - Android开发
---

# 一. 音视频采集流程
串联整个音视频录制流程，完成音视频的采集、编码、封包成 mp4 输出。
![流程图](/images/9871c68e4a1502807e06ef6adaea7583.webp)
通过摄像头和麦克风获得实时的音视频数据；

- 播放流程: 获取流—>解码—>播放。
- 录制播放路程: 录制音频视频—>视频处理—>编码—>上传服务器->别人播放。
- 直播过程 : 录制音视频—>编码—>流媒体传输—>服务器—>流媒体传输到其他客户端—>解码—>播放。

视频采样数据 : 一般都是 YUV 或 RGB 格式

音频采样数据 :一般都是PCM格式
![image_13](../image/image_13.png)

# 二.音频采集

### 1.Android如何采集音频
Android SDK对于音频采集提供两套API：``MediaRecorder和AudioRecorder``。
##### AudioRecord
AudioRecord输出是PCM语音数据，得到原始的一帧帧PCM音频数据。如果保存成音频文件，是不能够被播放器播放的，所以必须先写代码实现数据编码以及压缩。
一般直播技术采用的就是 AudioRecorder 采集音频数据。
``PCM(Pulse Code Modulation)``也被称为脉冲编码调制。PCM音频数据是未经压缩的音频采样数据裸流，它是由模拟信号经过采样、量化、编码转换成的标准的数字音频数据。

##### MediaRecorder
MediaRecorder是偏上层的一个API，可以直接把手机麦克风录入的音频数据进行编码压缩为AMR，MP3等并保存文件。

##### MediaRecorder和AudioRecord的区别
- MediaRecorder和AudioRecord都可以录制音频，区别是MediaRecorder录制的音频文件是经过压缩后的，需要设置编码器。并且录制的音频文件可以用系统自带的Music播放器播放。而AudioRecord录制的是PCM格式的音频文件，需要用AudioTrack来播放，AudioTrack更接近底层，PCM经过编码压缩可以为 amr MP3 AAC。
- 当要简单的把数据采集为音频文件，就使用MediaRecorder，如果要对音频做进一步的算法处理就使用AudioRecorder。

##### 优缺点：
AudioRecord
主要是实现边录边播以及对音频的实时处理,这个特性让他更适合在语音方面有优势；
优点：语音的实时处理，可以用代码实现各种音频的封装
缺点：输出是PCM格式文件，如果保存成音频文件，是不能够被播放器播放的，所以必须先写代码实现数据编码以及压缩
MediaRecorder
已经集成了录音、编码、压缩等，支持少量的录音音频格式，大概有，aac，amr，3gp等
优点：集成，直接调用相关接口即可，代码量小
缺点：无法实时处理音频；输出的音频格式不是很多，例如没有输出mp3格式文件


##### 应用：
如果只是想简单地做一个录音机，录制音频文件，就使用 MediaRecorder，而如果需要对音频做进一步的算法处理、或者采用第三方的编码库进行压缩、以及网络传输、直播等应用，则建议使用 AudioRecord。

# 三.视频采集
和音频一样，也有高层和低层的 API，高层就是`` Camera 和 MediaRecorder``，可以快速实现编码，低层就是直接使用`` Camera``，然后将采集的数据进行滤镜、降噪等前处理，
处理完成后由 MediaCodec 进行硬件编码，最后采用 MediaMuxer 生成最终的视频文件。

在 Android 系统下有两套 API 可以进行视频采集，`` Camera 和 Camera2 ``。Camera是以前老的 API ，从 Android 5.0(21)之后就已经放弃了。如今主要使用 Camera2 进行视频的采集。

直播开发中经常需要获取视频原始帧数据然后前置处理例如：美颜、水印、特效等然后通过编码在通过rtmp或者rtsp等协议方式推流出去，可以完成实时图像传递。
那么如何获取原始视频帧数据？android camera api有一个设置回调的方法，可以将可以通过它来获取原始视频数据如nv21 、 nv12 、 yv12 等。

![](/images/606c806e2b6ab13df9b1cc5b86f9348f.webp)


### MediaRecorder实现视频采集
优点:
使用方便，得到就是编码和封装好的音视频文件，可以直接使用。
缺点:
无法获取原始数据，从而无法对原始数据添加一些自己的处理。

### Camera实现视频采集
1、通过MediaCodec创建一个用于输入的Surface
2、通过通过camera预览时的上下文EGL创建OpenGL的环境，根据上面得到的Surface创建EGLSuface。
3、通过camera预览时的绑定的纹理id，进行纹理绘制。
4、交换数据，让数据输入新Surface。使用AudioReocod进行声音的采集
5、通过Mediacodec编码为h264、AAC。
6、通过MediaMuxer进行数据封装为mp4。


# 四. 视频处理
视频或者音频完成采集之后得到原始数据，为了增强一些现场效果或者加上一些额外的效果，我们一般会在将其编码压缩前进行处理，例如：美颜及水印。各种美颜和视频添加特效的App都是基于GPUImage框架实现。

OpenGL ES 可以做什么?
OpenGL ES 是手机、PDA 和游戏主机等嵌入式设备三维 (二维也包括) 图形处理的 API，当然是用来在嵌入式设备上的图形处理了，OpenGL ES 强大的渲染能力使其成为我们在嵌入式设备上进行图形处理的优良选择。我们经常使用的场景有：

图片处理。比如图片色调转换、美颜等。
摄像头预览效果处理。比如美颜相机、恶搞相机等。
视频处理。摄像头预览效果处理可以，这个自然也不在话下了。
3D 游戏。比如神庙逃亡、都市赛车等。

纹理
纹理是表示物体表面的一幅或几幅二维图形，也称纹理贴图（texture）。当把纹理按照特定的方式映射到物体表面上的时候，能使物体看上去更加真实。当前流行的图形系统中，纹理绘制已经成为一种必不可少的渲染方法。在理解纹理映射时，  
可以将纹理看做应用在物体表面的像素颜色。在真实世界中，纹理表示一个对象的颜色、图案以及触觉特征。纹理只表示对象表面的彩色图案，它不能改变对象的几何结构。

1. 音频处理

可以对音频的原始流做处理，如降噪、回音、以及各种 filter 效果。

2. 视频处理

现在抖音、美图秀秀等，在拍摄，视频处理方面，都提供了很多视频滤镜，而且还有各种贴纸、场景、人脸识别、特效、添加水印等。

其实对视频进行美颜和添加特效都是通过 OpenGL 进行处理的。Android 中有 GLSurfaceView，这个类似于 SurfaceView，不过可以利用 Renderer 对其进行渲染。通过 OpenGL 可以生成纹理，通过纹理的 Id 可以生成 SurfaceTexture，而 SurfaceTexture 可以交给 Camera，最后通过纹理就将摄像头预览画面和 OpenGL 建立了联系，从而可以通过 OpenGL 进行一系列的操作。

美颜的整个过程无非是根据 Camera 预览的纹理通过 OpenGL 中 FBO 技术生成一个新的纹理，然后在 Renderer 中的onDrawFrame() 使用新的纹理进行绘制。添加水印也就是先将一张图片转换为纹理，然后利用 OpenGL 进行绘制。添加动态挂件特效则比较复杂，先要根据当前的预览图片进行算法分析识别人脸部相应部位，然后在各个相应部位上绘制相应的图像，整个过程的实现有一定的难度，人脸识别技术目前有 OpenCV、Dlib、MTCNN 等。



# 五.音视频编码和封装
### 1. 为何要对音视频进行编码？
音视频的原始数据非常庞大，难以存储和传输。要解决音视频数据的存储和传输问题，或是为了加密等。
就需要对这些数据进行压缩，``音视频数据压缩技术就是音视频编码``。
编码的目的就是在最小图像或音频信息丢失情况下得到最大的压缩，解码是相对编码的，其目的是最大限度的还原原始图像或声音信息。
``编解码的意义就是便于数据传输和存储``。
### 2. 编解码种类(硬件编码，软件编码)

- 软编码：使用CPU进行编码，实现直接、简单，参数调整方便，升级易，但CPU负载重，性能较硬编码低，低码率下质量通常比硬编码要好一点。

- 硬编码：使用非CPU进行编码，如显卡GPU、专用的DSP、FPGA、ASIC
芯片等，性能高，低码率下通常质量低于软编码器，但部分产品在GPU硬
件平台移植了优秀的软编码算法（如X264）的，质量基本等同于
软编码。


- 软解码，指利用CPU的计算能力来解码，通常如果CPU的能力不是很强的时候，一则解码速度会比较慢，二则手机可能出现发热现象。优点是，由于使用统一的算法，兼容性会很好。

- 硬解码，指的是利用手机上专门的解码芯片来加速解码。通常硬解码的解码速度会快很多，但是由于硬解码由各个厂家实现，质量参差不齐，非常容易出现兼容性问题。

推荐安卓4.3以上使用硬编码，以下使用软编码，而iOS使用全部硬编码。如果是使用播放解码，不管是安卓还是iOS，都使用软解码方案，虽然这样做不可避免的牺牲功耗，但是在部分细节方面表现会较优，且可控性强，兼容性也强，出错情况少。

硬编码：
用设备GPU去实现编解码，这样可以减轻CPU的压力。

软编码：
让CPU来进行编解码，在c层代码来进行编解码，因为c/c++有很多好的编解码库。

软硬编码对比：
硬编的好处主要在于速度快，而且是系统自带的库不需要引入外部的库，但是特性支持有限，而且硬编的压缩率一般偏低，而对于软编码来说，虽然速度较慢，但是压缩率比较高，而且支持的H264特性也会比硬编码多很多，相对来说比较可控。而且硬编码会受硬件设备支持的影响。

在Android 4.1之前没有提供硬编解码的API，所以基本都是采用开源的那些库，比如著名的FFMpeg实现软编解码。但是通常情况下，同一平台同一硬件环境，硬编码的速度快于软件编码，软编码使用CPU来进行计算，会消耗一些app的运算效率。在Android4.1及以上版本可以使用MediaCodec来访问底层的媒体编解码器从而支持硬编码/硬解码。

众所周知， Android API 中有个 MediaCodec 的类，利用 MediaCodec 可实现硬编码，高效且方便，Android API 中还有个叫 MediaMuxer 的类，可以实现音频与视频的合成，
但是 MediaCodec 使用的 API 最低要求是 16，MediaMuxer 则是 18，除此之外如果对视频想做更多的处理还需要做比较多的开发，当然这点纯粹是偷懒。如果使用软编码，
那么 API 限制将不再那么苛刻，笔者开发时调到了 14，然后由于我用的是 FFmpeg 且移植了它的命令行工具，那么对视频很多的处理操作可以使用简单命令即可完成。
视频编码我为 FFmpeg 配置的是 x264 ,其可编码为 H.264 视频格式，除此之外比较出名的还有下一代编码标准 HEVC、VP9。音频我为 FFmpeg 配置的是 libfdk-aac ,
其 libfaac 在新版 FFmpeg 中已经被抛弃了。x264 现在在算法上基本达到了瓶颈，而软编效率很大程度上依赖算法与 cpu ，所以 cpu 就成了决定效率的关键，经过我实验，
虽然其跟硬编码效率还是有差距，但是它在普通 64 位的 cpu 上表现还是不错的，处理 480P、帧率 30 、比特率 1000000 的视频帧基本没有延迟。
### 视频编码封装的可行性方案

- 第一个就是大家熟知的ffmpeg,将ffmpeg移植到anroid平台，编译成so文件，由jni 调用，可以实现音视频的分离、裁剪、拼合、加字幕、滤镜等功能。

- 第二个就是android 自带的MediaCodec 框架，MediaCodec框架底层调用的是StageFright库，StageFright库是默认封装在android系统里面的。

- 第三个，如果只是做视频音频混合的话，可以用这个开源工程mp4parser使用MediaCodec 类进行编码压缩，视频压缩为H.264，音频压缩为aac，使用MediaMuxer 将音视频合成为MP4。




### 可行性方案的优缺点
1. 功能多少方面：
ffmpeg 无疑排第一位，他集合了视频编解码、视频滤镜、流媒体推流、音频各种特效等等，基本上你能想到的功能都在里面。
第二位当是Android的亲儿子，MediaCodec。MediaCodec涵盖了音视频解复用、音频解码、视频解码、音频编码、视频编码、音视频合并的整个流程。跟ffmpeg相比，MediaCodec 更接近底层硬件。这个方案如果想要实现视频的滤镜、字幕、拼接等功能的话，需要自己配合OpenGL ES 来实现，另外，音视频拼接的话，要考虑到不同音频采样率的重采样问题，音频重采用问题，需要懂得傅立叶变换相关的离散信号变换方法，如果要实现音频特效，如变声、均衡器的话，也需要懂得上述信号变换方法。因此，很少公司会采用。
第三位mp4praser,可以实现音视频编解码及编辑。 

2. 学习门槛：如果只是做视频转码、加文字、图片特效等，ffmpeg和MediaCodec 旗鼓相当，mp4parser最低(但是基于mp4parser的资料比较少，其实也未必)。如果是要拼接视频、做音频         的变声、均衡器特效的话，MediaCodec是难度最高的，因为这一切需要你从底层原理做起。

3. 运行效率:MediaCodec硬解硬编最快，ffmpeg硬解硬编方案稍慢(注意,2017年5月以后最新版ffmpeg已经整合了MediaCodec,不再慢了)，mp4parser（只能软解软编）最慢。

4. 稳定性: MediaCodec和ffmpeg 的硬解硬编方案旗鼓相当，mp4parser在低配的机器上可能出现卡顿的问题。

5. 打包占用空间:国内最得最好的ffmpeg硬解硬编方案，其so文件在10.几M,MediaCodec由于是纯java 代码，占用空间很容易做到几百K甚至几十K。mp4parser也是纯Java,开发包同样非常小。

### FFmpeg
ffmpeg 是基于C语言的著名视频编解码方案。具有非常强大的功能包括视频采集功能、视频格式转换、视频抓图、给视频加水印等。国内有也有不少的公司将ffmpeg 移植到iOS和android 平台进行视频处理，例如，美拍、秒拍等。当前众多的视频SDK中, 大都是封装ffmpeg对视频进行转码, 压缩, 裁剪的处理.优点是ffmpeg发展到现在已经相对成熟, 支持的视频格式较多。但是缺点有:
- 速度慢，用cpu来执行视频数据的处理属于软解码, 效率并不高;
- 增加包的体积，一般好的sdk（如阿里云短视频sdk） 有20m上下, 这样的sdk合入应用后, 对应用大小有一定的影响。

FFmpeg本质上可以看做是媒体处理工具的集合，包含了很多的媒体文件处理工具，例如媒体文件格式解析工具、编解码器等，这些工具实际上就是一个个的库，而FFmpeg的命令行程序实际上就是对这些库的一种包装，在调用命令行程序时也是通过底下的这些库来完成操作。这些库有的是编译时可选的，而且FFmpeg也支持一些外部的库，例如x264、MediaCodec。FFmpeg由于提供了很多的编解码器，而且它的媒体操作也很丰富，所以可以支持非常多的媒体类型，同时很多的处理功能也已经由FFmpeg提供，使用者只需要去调用即可，所以不少的编辑处理功能可以相对简单地完成开发。
适用场景：多平台使用（例如不同芯片厂商的手机），短时间摄像。

### MediaCodec
MediaCodec提供的功能就相对单一，它基本上只用来完成编解码相关的功能。以整个视频转码流程举例，大致需要几个步骤：解封装->解码->滤镜处理等操作->编码->封装，``MediaCodec只提供编解码功能，而其它的功能则需要其它组件，如MediaExtractor以及MediaMuxer来完成。``但是MediaCodec在编解码时提供硬件编解码功能，其好处是非常明显的，效率很高，且CPU占用大幅降低。如果不使用硬件编解码的话，很多的转码过程的时长实在长得是令人无法忍受，放到APP上简直就是无法使用的功能。毕竟一段很短的视频，转码要好几分钟，发烫还严重，体验肯定是不行的。MediaCodec的缺点就是一定程度上会依赖于设备，由于MediaCodec的硬解码实际上是由厂商所提供的，同时安卓设备的硬件相互之间差异很大，所以在硬解码实现上自然也有所差别，就导致了一样的程序，一些设备上可以正常跑，而在另一些设备上则可能会出问题，此时就需要自行提供兼容性上的支持。
适用场景：有固定的硬件方案，无需移植（例如智能家具产品），需要长时间摄像。
#### 对比

作一个简单的比喻：FFmpeg就像一个工具箱，而MediaCodec就像一类功能强大，但是使用范围相对受限且不够灵活的工具。

- 1.FFmpeg也有对MediaCodec的支持，在编译出合适的库后，可以通过FFmpeg的api来调用MediaCodec，但只能使用解码功能。
- 2.MediaCodec并非只代表硬编解码，它事实上可以看做是一种服务，厂商将自己的编解码方案预先注册于服务中，而用户在需要时再通过服务去调用相应的编解码器来完成任务。MediaCodec支持硬件编解码以及软件编解码，可以自行选择需要使用的编解码器。
- 3.FFmpeg在使用MediaCodec时，使用的方式和JAVA调用是类似的，FFmpeg会通过JNI的callXXmethod去调用MediaCodec的方法，这个过程其实和JAVA中的调用没有区别，但是FFmpeg通过封装MediaCodec的操作，使得MediaCodec可以按照FFmpeg的编解码流程进行调用。
- 4.MediaCodec它本身并不是Codec，它是通过调用底层编解码组件具有Codec能力。



#### 开源方案
基于ffmpeg 的免费软解软编方案在github.com有很多，例如:EpMedia,硬解硬编方案还没有看到。商业收费的方案有趣拍、美摄等。不过这些商业方案是按年收费的有点小贵。

基于MediaCodec 的免费开源方案有m4m，videotranscoder等，不过这些开源方案，表面看上去功能很强大，实际使用的时候会遇到不少坑，只适用于对MediaCodec的原理进行研究。

# 四.音视频解码
![image.png](/images/8778129b244dac7bd2ac63a26b80de24.webp)
解协议的作用，就是将流媒体协议的数据，解析为标准的相应的封装格式数据。视音频在网络上传播的时候，常常采用各种流媒体协议，例如HTTP，RTMP，或是MMS等等。这些协议在传输视音频数据的同时，也会传输一些信令数据。这些信令数据包括对播放的控制（播放，暂停，停止），或者对网络状态的描述等。解协议的过程中会去除掉信令数据而只保留视音频数据。例如，采用RTMP协议传输的数据，经过解协议操作后，输出FLV格式的数据。

### 解封装
解封装的作用，就是将输入的封装格式的数据，分离成为音频流压缩编码数据和视频流压缩编码数据。封装格式种类很多，例如MP4，MKV，RMVB，TS，FLV，AVI等等，它的作用就是将已经压缩编码的视频数据和音频数据按照一定的格式放到一起。例如，FLV格式的数据，经过解封装操作后，输出H.264编码的视频码流和AAC编码的音频码流。
### 解码
解码的作用，就是将视频/音频压缩编码数据，解码成为非压缩的视频/音频原始数据。音频的压缩编码标准包含AAC，MP3，AC-3等等，视频的压缩编码标准则包含H.264，MPEG2，VC-1等等。解码是整个系统中最重要也是最复杂的一个环节。通过解码，压缩编码的视频数据输出成为非压缩的颜色数据，例如YUV420P，RGB等等；压缩编码的音频数据输出成为非压缩的音频抽样数据，例如PCM数据。
### 音频同步
视音频同步的作用，就是根据解封装模块处理过程中获取到的参数信息，同步解码出来的视频和音频数据，并将视频音频数据送至系统的显卡和声卡播放出来。

### 硬解码和软解码
##### 硬解
字面上理解就是用硬件解码。通过显卡的视频加速功能对高清视频进行解码。可以理解为有一个专门的电路板来进行视频的解码工作，是依靠GPU。
调用GPU的专门模块编码来解码，减少CPU运算。显卡核心GPU拥有独特的计算方法，解码效率非常高，这样不但能够减轻CPU的负担，还有着低功耗，发热少等特点。

但是，由于硬解码起步比较晚，软件和驱动对他的支持度很低，基本上硬解码内置什么样的模块，就解码什么样的视频，面对网上各色各样的视频编码样式，兼容性不好。此外，硬解码的滤镜、字幕、画质方面都做的不够理想。

对于android设备，目前用得比较多的芯片就是高通、海思和联发科，这些芯片大都集成了很多的功能，CPU、GUP、DSP、ISP包括视频解码、音频解码等等。
在Android中使用硬件解码直接使用MediaCodec就可以了，虽然MediaPlayer也是硬件解码，但是被封装得太死了，支持的协议很少。而MediaCodec就很好拓展，我们可以根据流媒体的协议和设备硬件本身来自定义硬件解码，代表播放器就是Google的ExoPlayer。
##### 软解
字面上理解就是用软件解码。但是实际上还是要硬件支撑。这个硬件就是CPU。
在软解码过程中，需要对大量的视频信息进行运算，所以对CPU性能的要求非常高。尤其是对高清大码率的视频来说，巨大的运算量就会造成转换效率低，发热量高等问题。
我们最最常见的视频软解码开源库就是``FFmpeg``。目前基于FFmpeg的开源播放器有B站的ijkplayer
不过，软解码不需要过多的硬件支持，兼容性非常高，即使出现新的视频编码格式，只要安装好相应的解码器文件，就可以顺利播放。而且软解码拥有丰富的滤镜，字幕，画面处理优化等效果，只有你CPU够强悍，就能够实现更加出色的画面效果。
##### 总结
在Android设备硬件支持的情况下优先使用Android设备的硬件解码，减少CPU的占用，更加省电。
在Android设备硬解不支持的情况下选择使用软解码，不管怎么样，视频至少能够播放，具有更好的适应性，但是增加了CPU的占用，更加费电，软硬结合才是最好。




# 五.android 平台音视解码播放器选择
在Android中播放视频很简单，可以使用MediaPlayer+SurfaceView或者VideoView设置一个视频文件路径就可以实现播放了。但是如果想对音视频再进行处理，比如视频播放过程中增加水印，或者对视频进行转码，就需要对视频进行编解码处理了。那么Android上视频编解码一般怎么做的呢？
其实正常视频编解码都是分为两种：软解码和硬解码。Android上软解码的代表：ffmpeg，非常成熟和好用的软解码第三方库。硬解码：MediaCodec，Android自带的硬解码库。

### MediaPlayer
在Android系统中对于视频播放器有原生的实现MediaPlayer, 以及将MediaPlayer，SurfaceView封装在一起的VideoView, 两者都只是使用硬解播放，基本上只支持本地和HTTP协议的视频播放，扩展性都很差，只适合最简单的视频播放需求。

Android原生播放器，支持格式较少：支持mp4，3gp，资源文下支持mkv，使用比较简单，但是拓展性比较差。不需要集成第三方库，不占用apk体积。

### ijkplayer
哔哩哔哩开源的基于ffmpeg开发的一款播放器，功能就比较强大了，如果只是使用它进行播放，集成也较为简单，使用也和MediaPlayer差不多，但是要定制化需求，就有一定的门槛高度。支持软硬编解码，支持倍速播放，可以定制化集成需要的功能，集成占用体积也很小。

### ExoPlayer（基本来自于官方文档翻译）
谷歌出品，推荐使用的播放器。同RecyclerView一样定制化程度非常高。并加入了对DASH和HLS等直播协议的支持，但也只支持硬码，如果项目中只需要支持对H264格式的视频播放，以及流媒体协议比较常规（比如HTTP，HLS），基于ExoPlayer定制也是不错的选择。
优点：

支持动态的自适应流HTTP(DASH) 和 平滑流，任何目前MediaPlayer支持的视频格式（同时它还支持HTTP直播了（HLS),MP4,MP3,WebM,M4A,MPEG-TS 和 AAC).
支持高级的HLS特性，例如正确处理 EXT-X-DISCONTINUITY 标签。
无缝合并、连接和循环媒体的能力。
支持自定义和扩治你的使用场景。ExoPlayer专门为此设计，它允许将许多组件替换为自定义实现，它提供了低等级的媒体API，例如：MediaCodec，AudioTrack，MediaDrm，可以用于建立自定义媒体播放的解决方案。。以第三方依赖的方式集成，可以随应用升级版本。更少的适配性问题，更少的设备特定的问题和更少的行为变化, 在不同的设备和android的版本，可以接入ffmpeg。
缺点：
相对于MediaPlayer更耗电：但是Android Q以开发audio affload，可以减低功耗。
最低API16，早期版本不支持自动检查需要播放的媒体格式，后续的版本已经支持。

### 特性

功能支持情况

| 功能 | MediaPlayer | IjkPlayer | ExoPlayer |
| --- | --- | --- | --- |
| 调整显示比例 | 支持 | 支持 | 支持 |
| 滑动调节播放进度、声音、亮度 | 支持 | 支持 | 支持 |
| 双击播放、暂停 | 支持 | 支持 | 支持 |
| 重力感应自动进入/退出全屏以及手动进入/退出全屏 | 支持 | 支持 | 支持 |
| 倍速播放 | 不支持 | 支持 | 支持 |
| 视频截图（使用 SurfaceView 时都不支持，默认用的是 TextureView） | 支持 | 支持 | 支持 |
| 列表小窗全局悬浮播放 | 支持 | 支持 | 支持 |
| 连续播放一个列表的视频 | 支持 | 支持 | 支持 |
| 广告播放 | 支持 | 支持 | 支持 |
| 边播边缓存，使用了[AndroidVideoCache ](https://github.com/danikula/AndroidVideoCache)实现 | 支持 | 支持 | 支持 |
| 弹幕，使用[DanmakuFlameMaster ](https://github.com/Bilibili/DanmakuFlameMaster)实现 | 支持 | 支持 | 支持 |
| 多路播放器同时播放 | 支持 | 支持 | 支持 |
| 没有任何控制 UI 的纯播放 | 支持 | 支持 | 支持 |
| Android 8.0 画中画 | 支持 | 支持 | 支持 |
| 无缝衔接播放 | 支持 | 支持 | 支持 |
| 抖音 | 支持 | 支持 | 支持 |

协议/格式支持情况（只列举常用格式/协议）

| 协议/格式 | MediaPlayer | IjkPlayer | ExoPlayer |
| --- | --- | --- | --- |
| https | 支持 | 支持 | 支持 |
| rtsp | 不支持 | 支持 | 不支持 |
| rtmp | 不支持 | 支持 | 支持 |
| ffconcat | 不支持 | 支持 | 不支持 |
| file（本地视频） | 支持 | 支持 | 支持 |
| android.resource（raw） | 支持 | 支持 | 支持 |
| assets 中的视频 | 支持 | 支持 | 支持 |
| mp4 | 支持 | 支持 | 支持 |
| m3u8 | 支持 | 支持 | 支持 |
| flv | 支持 | 支持 | 可播放，无法 seek 进度 |

### 建议
- 1.如果已知的播放场景比较简单，例如小视频场景，都是mp4视频(h264/aac格式)，建议使用ExoPlayer，没有比这更适合的；
- 2.涉及到多种视频交互形式，直播、长视频等，还是建议引入ijkplayer等软件的形式；
- 3.如果Android平台不介意包大小，推荐使用VLC，VLC更新频繁，官方维护相当给力；如果比较关注包大小，建议选择ijkplayer，ijkplayer目前的缺点是维护的不那么勤了；
- 4.长远来看，国内很多播放器都从接入ijkplayer开始，逐渐演化，去掉不适合自己产品的代码，引入自己需要的module，渐渐变成自己的播放器；

### 开源音视频播放器UI方案
[GSYVideoPlayer](https://github.com/CarGuo/GSYVideoPlayer)
[DKVideoPlayer](https://github.com/Doikki/DKVideoPlayer)

# 音视频数据传输
RTMP

RTSP


参考文章:
[Android 音频采集（原始音频）](https://blog.csdn.net/Java_android_c/article/details/52619737)
[音视频篇 - Android 音视频涉及到的技术](https://blog.csdn.net/u014294681/article/details/89314114)
[Android音视频编码基础一](https://blog.csdn.net/u010126792/article/details/86529743)
[微信 Android 视频编码爬过的那些坑](https://cloud.tencent.com/developer/article/1006240)
[Android视频技术探索之旅：美团外卖商家端的实践](https://blog.csdn.net/MeituanTech/article/details/100789243)
[Android音视频开发之MediaCodec编解码](https://mp.weixin.qq.com/s?__biz=MzI1NDc5MzIxMw==&mid=2247486073&idx=1&sn=9006ae3e0149ebbea2438a83873c4887)
[Android视频处理之MediaCodec-1-简介](https://mp.weixin.qq.com/s?__biz=MzUxODQ3MTk5Mg==&mid=2247483866&idx=1&sn=f5600690c3c034d7d6585a30311a1587&chksm=f989298dcefea09b77fad1d244e722f21d196ffed9da2317866511032f23ea37c4e01bc16cf5&scene=38#wechat_redirect)
[Android视频处理之MediaCodec-2-使用](https://mp.weixin.qq.com/s?__biz=MzUxODQ3MTk5Mg==&mid=2247483867&idx=1&sn=f483a25c52c9dd679015b4a0e2674d0f&chksm=f989298ccefea09af9aa701be7a9cbacf1ee7876a3f46eb746784d0880f18ecb4a08a162c8e9&scene=38#wechat_redirect)
[Android视频处理之MediaCodec-3-播放视频](https://mp.weixin.qq.com/s?__biz=MzUxODQ3MTk5Mg==&mid=2247483868&idx=1&sn=99dec978a4640136c870965ba853c204&chksm=f989298bcefea09dddae613023139e0c6bd2f4eaaa9dc3ec16400645fc4a0764414134ad73ea&scene=38#wechat_redirect)
[Android视频处理之MediaCodec-4-视频帧转图片](https://mp.weixin.qq.com/s?__biz=MzUxODQ3MTk5Mg==&mid=2247483869&idx=1&sn=d242e33a36bbfcc02c018a4dd5d84377&chksm=f989298acefea09c6990223061947e6a2c2bd4831839ca08d0e231283a9dd832371c7cf9ff66&scene=38#wechat_redirect)
[Android视频处理之MediaCodec-5-生成mp4视频](https://mp.weixin.qq.com/s?__biz=MzUxODQ3MTk5Mg==&mid=2247483870&idx=1&sn=eace73e3ae9c428ee425ad4e661f7366&chksm=f9892989cefea09f85d3ff3d50c3563a948dba17e0541dfcdf74bae43459381af7a89bc56fd3&scene=38#wechat_redirect)
[Android视频处理之MediaCodec-6-给视频加水印](https://mp.weixin.qq.com/s?__biz=MzUxODQ3MTk5Mg==&mid=2247483871&idx=1&sn=03f5dbe5fee6b48ddba89ed8557d8d86&chksm=f9892988cefea09e67d0384fa5e8fa61624d269d7f5e2b4214df9b159373350531394a28d1b4&scene=38#wechat_redirect)
[Android 音视频编辑经验总结及开源工程分享](https://blog.csdn.net/u011495684/article/details/78437060?utm_source=blogxgwz9)
[Android 音视频开发学习思路](https://www.cnblogs.com/renhui/p/7452572.html)
[从开发小白到音视频专家](https://blog.csdn.net/weixin_34390996/article/details/85102677?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromBaidu-5.nonecase&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromBaidu-5.nonecase)
[android音视频开发基础4--FFmpeg 入门](https://blog.csdn.net/DTJ_74/article/details/86748798)
[视音频编解码技术零基础学习方法](https://blog.csdn.net/leixiaohua1020/article/details/18893769)
[Ijkplayer、ExoPlayer、VLC播放器综合比较](https://www.jianshu.com/p/e66b96436bfe)
[ijkplayer点播和直播视频 问题 解决及优化，视频播放中可能有的bug](https://blog.csdn.net/shareus/article/details/78585260)
[Android视频编辑器（一）通过OpenGL预览、录制视频以及断点续录等](https://blog.csdn.net/qqchenjian318/article/details/77396653)
[DevYK](https://juejin.cn/user/3368559355637566/posts)
[cain_huang](https://www.jianshu.com/u/fd6f2b25d0f4)
[Android openGl开发详解(二)——通过SurfaceView，TextureView，GlSurfaceView显示相机预览（附Demo）](https://blog.csdn.net/qq_32175491/article/details/79755424)
[开发的猫](https://juejin.cn/user/3175045310197255/posts)
[Android | 音视频方向进阶路线及资源合集](https://juejin.cn/post/6844904082881118221#heading-3)
