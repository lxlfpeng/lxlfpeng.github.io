---
title: Okhttp3.0配置支持第三方签名Https证书
date: 2017-06-11
categories: 
  - Android开发
tags:
  - Okhttp
  - Https  
---

# 一.Https简介
HTTPS全称为Hyper Text Transfer Protocol over Secure Socket Layer或是Hypertext Transfer Protocol Secure 中文含义为“超文本传输安全协议” 。是以安全为目标的HTTP通道，
在HTTP的基础上通过传输加密和身份认证保证了传输过程的安全性 。HTTPS 在HTTP 的基础下加入SSL，HTTPS 的安全基础是 SSL，因此加密的详细内容就需要 SSL。 HTTPS 存在不同于 HTTP 的默认端口及一个加密/身份验证层（在 HTTP与 TCP 之间）。
这个系统提供了身份验证与加密通讯方法。它被广泛用于万维网上安全敏感的通讯，例如交易支付等方面。

# 二.Okhttp支持Https
okhttp默认情况下是支持https协议的网站的，比如https://www.baidu.com等，可以直接通过okhttp请求就可以获取对应的数据。需要注意的是Okhttp支持的https的网站基本都是CA机构颁发的证书， 默认情况下是可以信任的。如果我们是自己签发的https证书就需要进行处理，才能正确的访问数据。

# 三.okhttp信任所有机构颁发的证书(不建议使用)
### 1.实现X509TrustManager接口
1.新建TrustAllcert类实现X509TrustManager接口：
```
public class TrustAllCerts implements X509TrustManager {  
    @Override    
    public void checkClientTrusted(X509Certificate[] chain, String authType) {}  
    
    @Override    
    public void checkServerTrusted(X509Certificate[] chain, String authType) {}  
    
    @Override    
    public X509Certificate[] getAcceptedIssuers() {return new X509Certificate[0];}    
}    
```
### 2.初始化OKHttpClient进行配置：
```
OkHttpClient.Builder builder = new OkHttpClient.Builder();  
       builder.connectTimeout(DEFAULT_TIMEOUT, TimeUnit.SECONDS);  
       builder.sslSocketFactory(createSSLSocketFactory());  
       builder.hostnameVerifier(new HostnameVerifier() {  
           @Override  
           public boolean verify(String hostname, SSLSession session) {  
               return true;  
           }  
       });  

private static SSLSocketFactory createSSLSocketFactory() {  
        SSLSocketFactory ssfFactory = null;  
  
        try {  
            SSLContext sc = SSLContext.getInstance("TLS");  
            sc.init(null, new TrustManager[]{new TrustAllCerts()}, new SecureRandom());  
  
            ssfFactory = sc.getSocketFactory();  
        } catch (Exception e) {  
        }  
  
        return ssfFactory;  
    }  

```

## 四.okhttp配置支持自签证书(建议)
### 1.放置证书
将证书(一般是cer结尾的文件)放到工程的assets里面。
### 2.将证书的流数据传入生成SSLSocketFactory。
```
 public SSLSocketFactory getSslSocketFactory(InputStream certificates) {
        SSLContext sslContext = null;
        try {
            CertificateFactory certificateFactory = CertificateFactory.getInstance("X.509");

            Certificate ca;
            try {
                ca = certificateFactory.generateCertificate(certificates);

            } finally {
                certificates.close();
            }

            // Create a KeyStore containing our trusted CAs
            String keyStoreType = KeyStore.getDefaultType();
            KeyStore keyStore = KeyStore.getInstance(keyStoreType);
            keyStore.load(null, null);
            keyStore.setCertificateEntry("ca", ca);

            // Create a TrustManager that trusts the CAs in our KeyStore
            String tmfAlgorithm = TrustManagerFactory.getDefaultAlgorithm();
            TrustManagerFactory tmf = TrustManagerFactory.getInstance(tmfAlgorithm);
            tmf.init(keyStore);

            // Create an SSLContext that uses our TrustManager
            sslContext = SSLContext.getInstance("TLS");
            sslContext.init(null, tmf.getTrustManagers(), null);

        } catch (Exception e) {
            e.printStackTrace();
        }

        return sslContext != null ? sslContext.getSocketFactory() : null;
    }
```   
注意:这里可以将证书放到assets文件夹里面然后获取:
```
InputStream inputStream = null;
        try {
            inputStream = BaseApplication.getmAppContext().getAssets().open("s12306.cer");
        } catch (IOException e) {
            e.printStackTrace();
        }
```
也可以将证书copy出来定义成字符串常量进行设置(这样就不用将证书打包到apk里面了):
```
 private String BOOK12306 = "这里填写上证书"
InputStream inputStream1 = null;
        try {
            inputStream1 = new ByteArrayInputStream(BOOK12306.getBytes("UTF-8"));
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        }
```
### 3.对okhttp进行设置就可以了
```
 OkHttpClient okHttpClient = new OkHttpClient.Builder()
                .sslSocketFactory(getSslSocketFactory(inputStream))
                .readTimeout(7676, TimeUnit.MILLISECONDS)
                .connectTimeout(7676, TimeUnit.MILLISECONDS)
                .addInterceptor(logInterceptor)
                .addInterceptor(interceptor)
                .build();
```