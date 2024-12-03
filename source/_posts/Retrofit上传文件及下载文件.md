---
title: Retrofit上传文件及下载文件
date: 2016-07-18
categories: 
  - Android开发
---

# 一.Retrofit文件上传
## 1.文件上传注意点
1.文件上传一般用post请求。
2.文件上传的API接口中不能带@FormUrlEncoded参数。
3.一般要携带@Multipart(上传文件的标志)。
## 2.接口示例
```
@Multipart
@POST("UploadServlet")
Call<String> uploadFile(@PartMap Map<String, RequestBody> params);
```
或者:
```
//description为描述信息可以不填。
@Multipart
@POST("UploadServlet")
Call<ResponseBody> upload(@Part("description") RequestBody description,
                          @Part MultipartBody.Part file);
```
## 3.单文件上传
```
File file = new File("/sdcard/Pictures/myPicture/test.jpg");//文件
//multipart/form-data表示将数据以二进制的形式传入
RequestBody requestFile =RequestBody.create(MediaType.parse("multipart/form-data"), file);
//第一个参数是 和后端约定好Key，这里的partName是用image，第二个参数是文件名
MultipartBody.Part body = MultipartBody.Part.createFormData("image", file.getName(), requestFile);
//文件描述
String descriptionString = "hello, 这是文件描述";
RequestBody description =RequestBody.create(MediaType.parse("multipart/form-data"), descriptionString);
//文件上传
...
service.upload(description, body);
```
## 4.多文件上传
### 1.方式一
```
@Multipart
@POST("UploadServlet")
Call<ResponseBody> upload(@Part("description") RequestBody description,
                          @Part MultipartBody.Part file,
                          @Part MultipartBody.Part file2);
```
```
File file = new File("/sdcard/Pictures/myPicture/index.jpg");
File file1 = new File("/sdcard/Picuures/myPicture/me.txt");
RequestBody requestFile =RequestBody.create(MediaType.parse("applicaiton/otcet-stream"), file);

RequestBody requestFile1 =RequestBody.create(MediaType.parse("applicaiton/otcet-stream"), file1);

MultipartBody.Part body1 =MultipartBody.Part.createFormData("aFile", file.getName(), requestFile);

MultipartBody.Part body2 =MultipartBody.Part.createFormData("aFile", file.getName(), requestFile1);

String descriptionString = "This is a description";
RequestBody description =RequestBody.create(MediaType.parse("multipart/form-data"), descriptionString);

Call<ResponseBody> call = service.upload(description, body1,body2);
```
### 1.方式二@PartMap的形式实现多文件上传.
```
@Multipart
@POST("UploadServlet")
Call<String> uploadFile(@PartMap Map<String, RequestBody> params);
```
```
File file = new File("/sdcard/Pictures/myPicture/index.jpg");
File file1 = new File("/sdcard/Picuures/myPicture/me.txt");
RequestBody requestBody = RequestBody.create(MediaType.parse("multipart/form-data"), file);
RequestBody requestBody1 = RequestBody.create(MediaType.parse("multipart/form-data"), file1);
Map<String, RequestBody> params = new HashMap<>();

params.put("file\"; filename=\""+ file.getName(), requestBody);
params.put("file\"; filename=\""+ file1.getName(), requestBody1);

Call<String> model = service.uploadFile(params);
```
## 5.上传文件进度监听
### 1.定义接口用于回调
```
public abstract class RetrofitCallback {
    //用于进度的回调
    public abstract void onLoading(long total, long progress);
}
```
### 2.自定义requestbody
```
public class FileRequestBody<T> extends RequestBody {
    /**
     * 实际请求体
     */
    private RequestBody requestBody;
    /**
     * 上传回调接口
     */
    private RetrofitCallback callback;
    /**
     * 包装完成的BufferedSink
     */
    private BufferedSink bufferedSink;
    public FileRequestBody(RequestBody requestBody, RetrofitCallback callback) {
        super();
        this.requestBody = requestBody;
        this.callback = callback;
    }
    @Override
    public long contentLength() throws IOException {
        return requestBody.contentLength();
    }
    @Override
    public MediaType contentType() {
        return requestBody.contentType();
    }
    @Override
    public void writeTo(BufferedSink sink) throws IOException {
        if (bufferedSink == null) {
            //包装
            bufferedSink = Okio.buffer(sink(sink));
        }
        //写入
        requestBody.writeTo(bufferedSink);
        //必须调用flush，否则最后一部分数据可能不会被写入
        bufferedSink.flush();
    }
    /**
     * 写入，回调进度接口
     * @param sink Sink
     * @return Sink
     */
    private Sink sink(Sink sink) {
        return new ForwardingSink(sink) {
            //当前写入字节数
            long bytesWritten = 0L;
            //总字节长度，避免多次调用contentLength()方法
            long contentLength = 0L;
            @Override
            public void write(Buffer source, long byteCount) throws IOException {
                super.write(source, byteCount);
                if (contentLength == 0) {
                    //获得contentLength的值，后续不再调用
                    contentLength = contentLength();
                }
                //增加当前写入的字节数
                bytesWritten += byteCount;
                //回调
                callback.onLoading(contentLength, bytesWritten);
            }
        };
    }
}
```
### 3.上传数据的时候使用回调
```
...
RetrofitCallback callback = new RetrofitCallback() {
            @Override
            public void onLoading(long total, long progress) {
                //此处进行进度更新
                Log.d(TAG, "total---" + total);
                Log.d(TAG, "progress---" + progress);
                // Log.d(TAG, "progress---" + ((double) progress / (double) total));
            }
        };
RequestBody requestFile = RequestBody.create(MediaType.parse("multipart/form-data"), file);
FileRequestBody fileRequestBody = new FileRequestBody(requestFile, callback);
MultipartBody.Part body = MultipartBody.Part.createFormData("uploaded_file", file.getName(), fileRequestBody);
Call<ResponseBody> resultCall = service.uploadImage(body);
```
# 二.Retrofit文件下载
## 1.下载普通文件
##### (1.)定义下载接口
```
@GET("/mobilesafe/shouji360/360safesis/360MobileSafe_6.2.3.1060.apk")
Call<ResponseBody> retrofitDownload();
```
##### (2.)下载接口调用
```
RetrofitClient.create(FileDownloadService.class).downloadFileWithDynamicUrlSync(fileUrl).enqueue(new Callback<ResponseBody>() {  
    @Override
    public void onResponse(Call<ResponseBody> call, Response<ResponseBody> response) {
        if (response.isSuccess()) {
             writeToDisk(response.body());
        } 
    }
    @Override
    public void onFailure(Call<ResponseBody> call, Throwable t) {
        Log.e(TAG, "error");
    }
});
```
## 2.监听下载文件的进度
##### (1.)定义一个下载文件的请求与其他请求几乎无异：
```
 /*下载文件*/
    @GET("/mobilesafe/shouji360/360safesis/360MobileSafe_6.2.3.1060.apk")
    Call<ResponseBody> retrofitDownload();
```
##### (2.)定义一个接口监听下载的进度
```
public interface ProgressListener {
    /**
     * @param progress     已经下载或上传字节数
     * @param total        总字节数
     * @param done         是否完成
     */
    void onProgress(long progress, long total, boolean done);
}
```
##### (3.)这里通过拦截器的方式监听到进度,拦截器设置
```
public class ProgressResponseBody extends ResponseBody {
    private final ResponseBody responseBody;
    private final ProgressListener progressListener;
    private BufferedSource bufferedSource;

    public ProgressResponseBody(ResponseBody responseBody, ProgressListener progressListener) {
        this.responseBody = responseBody;
        this.progressListener = progressListener;
    }

    @Override
    public MediaType contentType() {
        return responseBody.contentType();
    }

    @Override
    public long contentLength() {
        return responseBody.contentLength();
    }

    @Override
    public BufferedSource source() {
        if (bufferedSource == null) {
            bufferedSource = Okio.buffer(source(responseBody.source()));
        }
        return bufferedSource;
    }

    private Source source(Source source) {
        return new ForwardingSource(source) {
            long totalBytesRead = 0L;

            @Override
            public long read(Buffer sink, long byteCount) throws IOException {
                long bytesRead = super.read(sink, byteCount);
                totalBytesRead += bytesRead != -1 ? bytesRead : 0;
                progressListener.onProgress(totalBytesRead, responseBody.contentLength(), bytesRead == -1);
                return bytesRead;
            }
        };
    }
}
```
##### (4.)进行设置并监听下载进度
```
ProgressListener progressListener = new ProgressListener() {
        //该方法在子线程中运行
        @Override
        public void onProgress(final long progress, final long total, boolean done) {
            Log.d("progress:", String.format("%d%% done\n", (100 * progress) / total));  
        }
    };
//下载逻辑
    private void downLoad() {
        OkHttpClient.Builder builder = new OkHttpClient.Builder();
        //添加拦截器，自定义ResponseBody，添加下载进度
        builder.networkInterceptors().add(new Interceptor() {
            @Override
            public okhttp3.Response intercept(Chain chain) throws IOException {
                okhttp3.Response originalResponse = chain.proceed(chain.request());
                return originalResponse.newBuilder().body(
                        new ProgressResponseBody(originalResponse.body(), progressListener))
                        .build();
            }
        });
        Retrofit.Builder retrofitBuilder = new Retrofit.Builder()
                .baseUrl("http://msoftdl.360.cn");
        ApiService retrofit = retrofitBuilder
                .client(builder.build())
                .build().create(ApiService.class);
        Call<ResponseBody> call = retrofit.retrofitDownload();
        call.enqueue(new Callback<ResponseBody>() {
            @Override
            public void onResponse(Call<ResponseBody> call, Response<ResponseBody> response) {
                try {
                    InputStream is = response.body().byteStream();
                    File file = new File(Environment.getExternalStorageDirectory(), "360app.apk");
                    FileOutputStream fos = new FileOutputStream(file);
                    BufferedInputStream bis = new BufferedInputStream(is);
                    byte[] buffer = new byte[1024];
                    int len;
                    while ((len = bis.read(buffer)) != -1) {
                        fos.write(buffer, 0, len);
                        fos.flush();
                    }
                    fos.close();
                    bis.close();
                    is.close();
                } catch (IOException e) {
                    Toast.makeText(DownLoadActivity.this, "e-->" + e.toString(), Toast.LENGTH_SHORT).show();
                    e.printStackTrace();
                }
                Toast.makeText(DownLoadActivity.this, "下载成功", Toast.LENGTH_SHORT).show();
            }
            @Override
            public void onFailure(Call<ResponseBody> call, Throwable t) {
                Toast.makeText(DownLoadActivity.this, "失败" + t.toString(), Toast.LENGTH_SHORT).show();
            }
        });
    }
```
## 3.大文件下载
上述的方式一般用来下载比较小的文件。这种方式实际上是写把文件写入运存里面然后在写入到磁盘的因此一般用于比较小的文件下载，如果下载大文件的话就会造成oom。下载大文件的时候我们需要给接口加上@Streaming注解，这种方式是直接把网络文件写入到磁盘里，因此如果继续使用上述的方式调用代码则会出现NetworkOnMainThreadException异常。这是将回调放入异步线程就好了。
```
/*下载文件*/
    @Streaming
    @GET("/mobilesafe/shouji360/360safesis/360MobileSafe_6.2.3.1060.apk")
    Call<ResponseBody> retrofitDownload();

    ExecutorService executorService = Executors.newFixedThreadPool(1);//获取异步线程
        Retrofit.Builder retrofitBuilder = new Retrofit.Builder()
                .addConverterFactory(GsonConverterFactory.create())
                .baseUrl("http://msoftdl.360.cn");
        ApiService retrofit = retrofitBuilder
                .client(builder.build())
                .callbackExecutor(executorService)//让回调在异步线程里进行
                .build().create(ApiService.class);
        final Call<ResponseBody> call = retrofit.retrofitDownload();

```
>在下载文件的时候要将okhttp的日志监听器关闭,否则容易造成oom.