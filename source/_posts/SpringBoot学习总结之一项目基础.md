---
title: SpringBoot学习总结之一项目基础
---

# 一.SpringBoot简介
### 1.什么是SpringBoot
SpringBoot是由Pivotal团队提供的框架，其设计目的是用来``简化Spring应用的初始搭建以及开发过程``。该框架使用了特定的方式来进行配置，从而使开发人员不再需要定义样板化的配置。SpringBoot是Spring项目中的一个子工程，与大家所熟知的Spring-framework 同属于Spring的产品。使用SpringBoot，可以让我们快速的构建庞大的Spring项目(包括web 持久化)，并且尽可能的减少一切xml配置，做到开箱即用，迅速上手，让我们关注业务而非配置。

### 2.为什么要使用SpringBoot
SpringBoot的出现解决了传统Spring项目的以下问题：
- 配置复杂繁多:每一个组件集成Spring都需要编写对应配置文件，比如appplicationContext-xxx.xml等。
- 混乱的依赖管理:在Spirng中想集成对应组件时，需要导入N多的pom，并且还要考虑版本。
>使用SpringBoot创建java应用，只需填写很少配置和依赖就能快速搭建，并使用java –jar 启动它，就能得到一个生产级别的web工程，非常方便。

### 3.SpringBoot的特点
- 使用注解配置，无需xml。
- 快速搭建，开发。
- 简化的maven。
- 方便的和三方框架集成。
- 内嵌tomcat，部署简单。
- 内置健康检查，监控等。
- 自动配置，让配置更加简单。

### 4.Spring和SpringMVC以及SpringBoot的区别
- Spring 是一个开源框架，为简化企业级应用开发而生。
- SpringMVC是基于Spring功能之上添加的Web框架，想用SpringMVC必须先依赖Spring。
- SpringBoot不是Spring官方的框架模式，是一个轻量级，简化配置和开发流程的web整合框架，只是一个配置工具，整合工具，辅助工具。

>``简单来说：``Spring 最初利用“工厂模式”(DI)和“代理模式”(AOP)解耦应用组件。大家觉得挺好用，于是按照这种模式搞了一个 MVC框架(一些用Spring 解耦的组件)，用来开发 web 应用( SpringMVC )。然后发现每次开发都写很多样板代码，为了简化工作流程，于是开发出了一些“懒人整合包”(starter)，这套就是 SpringBoot。

# 二.搭建一个SpringBoot项目
### 1.SpringBoot环境要求
- 开发环境JDK1.8
- 项目管理工具(Maven)
- 开发工具(Eclipse/idea)

### 2.通过Idea创建Springboot项目
1. idea安装Springboot插件
![](/images/38b1af0e0a391aae044b71ebc0358e4d.webp)
2. 创建新的工程
![](/images/e5238eed52a7972f3f354fd76455864e.webp)

![](/images/a9a2a2cd20239567bafd46366d579e69.webp)

![](/images/d2fc6bef8ec2da9ddd1094f2152872d3.webp)

![](/images/d6c519d18da4b136fea1f9a3e5b09311.webp)

### 3.通过spring.io创建Springboot项目
1. 在浏览器输入网址：https://start.spring.io/
2. 选择、填写如下信息：
![](/images/d165a8862ee97e1938585fdcf72fb813.webp)
3. 点击下方图标，即可下载项目压缩包，下载好后将其解压：
![](/images/443f609484959dafd221f3668cb2c5c1.webp)
4. 使用idea将其打开即可

# 三.SpringBoot项目结构
![](/images/5e71322d36fa1634d2562b7fdd9e3daa.webp)

### 1.路径说明
- src/main/java:程序代码
- src/main/resources:资源
- src/test/java:测试代码
- src/test/resources:测试资源

### 2.文件说明
- application.properties: 项目和 SpringBoot 的配置文件。
- xxxApplication.java: 项目启动引导类(bootstrap class)，也是 Spring 主配置类。
- xxxApplicationTests.java: 测试类骨架。
- pom.xml: 主要描述了项目的maven坐标，依赖关系，开发者需要遵循的规则，缺陷管理系统，组织和licenses，以及其他所有的项目相关因素，是项目级别的配置文件。
- build.gradle: Gradle构建说明文件(项目是Gradle构建才有)。

# 四.运行Springboot项目
### 1.在src/main/java下编写配置类：ApplicationConfig：
```
/**
 * 主配置类
 */
@SpringBootApplication
public class ApplicationConfig implements WebMvcConfigurer{

    public static void main(String[] args) {
        SpringApplication.run(ApplicationConfig.class, args);
    }
}
```

### 2.创建一个controller测试是否搭建完成。
```
@RestController
public class HelloController {
    @RequestMapping("/")
    public String list(){
        return "hello spring boot !";
    }
}
```

### 3.启动SpringBoot项目
![](/images/62ed3d27275c3b2119e33ebe37bf90ff.webp)

### 4.浏览器访问：http://localhost:8080/
![](/images/1875bd6dbd5ff92d574f7c0affc37e88.webp)

# 五.SpringBoot项目配置
### 1.SpringBoot全局配置文件
SpringBoot使用一个全局的配置文件，配置文件名是固定的；SpringBoot可以识别两种格式的配置文件:分别是yml文件与properties文件，所以可以将application.properties文件换成application.yml。yaml相对于properties而言，语法更加简洁明了，而且使用的场景也更多，很多的开源项目都是使用yaml进行配置。除了简洁，yaml还有另外一个特点，就是yaml中的数据是有序的， properties中的数据是无序的。在一些需要路径匹配的的配置中，顺序就显得尤为重要，一般采用yaml。
- application.properties
- application.yml

### 2.SpringBoot修改全局配置
配置文件的作用是修改SpringBoot自动配置的默认值，SpringBoot在底层自动配置好； application.properties默认放在：src/main/resource目录下，SpringBoot会自动加载。
例如要配置访问的端口号，properties文件如下:
```
# 修改端口号为80
server.port=80
```
yaml文件如下：
```
# 修改端口号为80
server:
  port: 80
```
>如果两种类型的配置文件同时存在，properties文件的优先级大于yaml文件。

### 3.将配置映射到实体类
SpringBoot支持直接将properties或者yml中的属性映射到某个实体类。
例如properties中有如下配置:
```
mysql:
 url: jdbc:mysql:///SpringBoot
 port: 3306
 user: root
 pass: root
```
现在有个mysql的连接信息，将其映射到实体类中去有两种方式：
- @ConfigurationProperties指定从配置文件中读取属性，prefix指定对应yaml文件中的名称。
- @Value获取配置的属性值。
##### (1.) @ConfigurationProperties方式
使用IDEA当我们添加了@ConfigurationProperties注解后，在页面上回出现一个错误提示，需要加入依赖。
```
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-configuration-processor</artifactId>
  <optional>true</optional>
</dependency>
```
编写JAVA类MySQLInfo.java:
```
//java类
@ConfigurationProperties(prefix = "mysql")
@Component
public class MySQLInfo {
 private String url;
 private Integer port;
 private String user;
 private String pass;
 //省略getset
}
```
>只需要指定prefix即可，就会加载yml配置前置为mysql的属性。

##### (2.) @Value方式
使用这个注解来获取属性使用方式是：
```
//java类
@Component
public class MySQLInfo {
 @Value("${mysql.url}")
 private String url;
 @Value("${mysql.port}")
 private Integer port;
 @Value("${mysql.user}")
 private String user;
 @Value("${mysql.pass}")
 private String pass;
 //省略get,set
}
```

##### (3.)两种映射方式的适用场合
- 当只需要为某个值提供注入时，推荐使用@Value方式。
- 当需要对整个对象的整体进行赋值时，使用@ConfigurationProperties。

>注意如果需要使用表达式只有@Value映射方式才可以使用。

# 六.SpringBoot依赖管理
如果使用maven构建工具则是通过POM文件来进行依赖管理，使用Gradle构建项目的话则使用build.gradle来进行依赖管理，本下文是maven构建工具进行构建。
### 1.安装配置maven(idea创建的项目会自带maven环境)
- 下载maven，配置maven的path环境。
- maven配置阿里云镜像。在maven的conf文件夹中的settings.xml里的mirrors下添加mirror标签。
```
<mirror>
  <id>alimaven</id>
  <name>aliyun maven</name>
  <url>http://maven.aliyun.com/nexus/content/groups/public/</url>
  <mirrorOf>central</mirrorOf>
</mirror> 
```
![](/images/7713f1f51579077f32d2b61adf49a21a.webp)

### 2.依赖SpringBoot启动器
如果使用Spring Initializr创建一个SpringBoot项目的话，那么会发现项目的POM文件中会加入了一个parent元素：
```
<parent>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-parent</artifactId>
  <version>2.2.7.RELEASE</version>
  <relativePath/> 
</parent>
```
spring-boot-starter-parent模块是SpringBoot 的父级依赖，只有继承它项目才是 SpringBoot 项目。spring-boot-starter-parent相当于作为了当前项目的父模块，在父模块里面管理了当前指定的SpringBoot版本2.2.7.RELEASE所有依赖的第三方库的统一版本管理， 通过spring-boot-starter-parent上溯到最顶层的项目，会找到一个properties元素，里面统一管理Spring框架和所有依赖到的第三方组件的统一版本号， 这样就能确保对于一个确定的SpringBoot版本，它引入的其他starter不再需要指定版本，同时所有的第三方依赖的版本也是固定的。
```
<!-- 暂时省略其他的配置属性 -->
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>2.3.1.RELEASE</version>
    <relativePath/> <!-- lookup parent from repository -->
</parent>
<groupId>com.example</groupId>
<artifactId>demo</artifactId>
<version>0.0.1-SNAPSHOT</version>
<name>demo</name>
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
        <scope>test</scope>
        <exclusions>
            <exclusion>
                <groupId>org.junit.vintage</groupId>
                <artifactId>junit-vintage-engine</artifactId>
            </exclusion>
        </exclusions>
    </dependency>
</dependencies>
```
>只需要修改parent元素中的版本号，就能全局更变所有starter的版本号。这种做法其实本质上是把当前项目作为spring-boot-starter-parent的子项目，其实在一定程度上并不灵活。当然也可以使用另一种方式：dependencyManagement。

### 3.SpringBoot项目添加依赖
```
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-web</artifactId>
</dependency>
```
>添加启动器依赖，当然也可以使用第三方启动器依赖。

### 4.SpringBoot项目添加插件
```
<plugin>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-maven-plugin</artifactId>
</plugin>
```
spring-boot-maven-plugin 插件是将 SpringBoot 的应用程序打包成 jar 包的插件。将所有应用启动运行所需要的 jar 包都包含进来，从逻辑上将具备了独立运行的条件。 当运行"mvnpackage"进行打包后，使用"java -jar"命令就可以直接运行。

### 5.SpringBoot标准的依赖配置文件
```
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    
    <!-- pom模型版本 -->
    <modelVersion>4.0.0</modelVersion>
    
    <!-- 项目信息 -->
    <groupId>demo</groupId><!-- 项目唯一标识 -->
    <artifactId>SpringBoot</artifactId><!-- 项目名 -->
    <version>0.0.1-SNAPSHOT</version><!-- 版本 -->
    <packaging>jar</packaging><!-- 打包方式 (pom,war,jar) -->

    <name>SpringBoot</name><!-- 项目的名称， Maven 产生的文档用 -->
    <description>Demo project for SpringBoot</description><!-- 项目的描述, Maven 产生的文档用 -->

    <!-- 父级项目 -->
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.3.1.RELEASE</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>
    
    <!-- 属性设置 -->
    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding><!-- 编译字符编码为utf-8 -->
        <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding><!-- 输出字符编码为UTF-8  -->
        <java.version>1.8</java.version><!-- jdK版本 -->
    </properties>
    
    <!-- 依赖关系 -->
    <dependencies>
        <!-- 测试 -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
        <!-- springmvc -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <!-- jpa(持久层) -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
        <!-- mysql(数据库) -->
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
            <scope>runtime</scope>
        </dependency>
        <!--支持Spring web-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
            <version>RELEASE</version>
            <scope>compile</scope>
        </dependency>
    </dependencies>
    
    <!-- 编译 -->
    <build>
        <!-- 插件 -->
        <plugins>
            <!-- maven插件 -->
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
```

# 七.SpringBoot常用注解
- @SpringBootApplication:是 SpringBoot 的启动类。此注解等同于@Configuration+@EnableAutoConfiguration+@ComponentScan 的组合。
- @SpringBootConfiguration:@SpringBootConfiguration 注解是@Configuration 注解的派生注解，跟@Configuration注解的功能一致，标注这个类是一个配置类，只不过@SpringBootConfiguration 是 SpringBoot的注解，而@Configuration 是 spring 的注解
- @Configuration:通过对 bean 对象的操作替代 spring 中 xml 文件
- @EnableAutoConfiguration:SpringBoot 自动配置(auto-configuration)：尝试根据你添加的 jar 依赖自动配置你的Spring 应用。是@AutoConfigurationPackage 和@Import(AutoConfigurationImportSelector.class)注解的组合。
- @AutoConfigurationPackage:@AutoConfigurationPackage 注解，自动注入主类下所在包下所有的加了注解的类(@Controller，@Service 等)，以及配置类(@Configuration)
- @Import({AutoConfigurationImportSelector.class})直接导入普通的类 导入实现了 ImportSelector 接口的类 导入实现了 ImportBeanDefinitionRegistrar 接口的类
- @ComponentScan:组件扫描，可自动发现和装配一些 Bean。
- @ConfigurationPropertiesScan:@ConfigurationPropertiesScan 扫描配置属性。@EnableConfigurationProperties 注解的作用是使用 @ConfigurationProperties 注解的类生效。

# 八.Springboot获取Http参数
### 1.@RequestMapping 和 @GetMapping @PostMapping 区别
- @GetMapping是一个组合注解，是``@RequestMapping(method = RequestMethod.GET)``的缩写。
- @PostMapping是一个组合注解，是``@RequestMapping(method = RequestMethod.POST)``的缩写。

### 2.获取Get请求参数详解
##### (1.)直接形参提交
直接把表单里面的参数写进 Controller 相应方法的形参中去，这个获取参数的方法适合get提交，而不适合post提交。
```
@GetMapping("/hello")
public String hello(String name,String age) {
    System.out.println("name is:"+name+" age is:"+age);
    return "name is:"+name+" age is:"+age;
}
```
>请求形式：http://127.0.0.1:8080/hello?name=张三&age=123，提交的参数名称必须和Controller方法中定义的参数名称一致。

##### (2.)用注解@RequestParam绑定请求参数到方法入参
```
@GetMapping("/hello")
public String hello(@RequestParam("name") String name,@RequestParam("age") String age){
    System.out.println("name is:"+name+" age is:"+age);
    return "name is:"+name+" age is:"+age;
}
```
- 可以在注解 @RequestParam 上添加  ``required = false`` 设置参数为非必输项。
- 可以在注解 @RequestParam 上添加  ``defaultValue=`` 参数 设置默认值。

>请求形式：http://127.0.0.1:8080/hello?name=张三&age=123，提交的参数名称必须和Controller方法中定义的参数名称一致。

##### (3.)直接在请求路径中(Restful风格) 
假设请求地址是如下这种 RESTful 风格，Springboot 这个参数值直接放在路径里面:
```
@GetMapping("/hello/{name}/{age}")
public String hello(@PathVariable("name") String name,@PathVariable("age") String age){
    System.out.println("name is:"+name+" age is:"+age);
    return "name is:"+name+" age is:"+age;
}
```
>请求形式：http://127.0.0.1:8080/张三/123

##### (4.)通过map来接收参数
```
@GetMapping("/hello")
public String hello(@RequestParam Map<String, Object> map){
 System.out.println("name is: " + map.get("name") +  " age is:" + map.get("age"));
 return "name is: " + map.get("name") +  " age is:" + map.get("age");
}
```

##### (5.)通过对象接收 JSON 数据
如果一个 get 请求的参数太多，我们构造一个对象来简化参数的接收方式。
```
@GetMapping("/hello")
public String hello(@RequestBody  User user){
 System.out.println("name is: " + user.getName() +  " age is:" + user.getAge());
 return "name is: " + user.getName() +  " age is:" + user.getAge();
}
```

### 3.获取Post请求参数详解
##### (1.)接收Form表单数据
创建 Controller 接收 form-data 格式的 POST 数据，如下所示：
```
@PostMapping("/save")
public String save(@RequestParam("name") String name,
                   @RequestParam("age") int age){
    System.out.println("name：" + name + ", age: " + age);
    return "name：" + name + ", age: " + age;
}
```
- 可以在注解 @RequestParam 上添加  ``required = false`` 设置参数为非必输项。
- 可以在注解 @RequestParam 上添加  ``defaultValue=`` 参数 设置默认值。

##### (2.)使用map集合来接收表单数据
用 map 接收 Controller 直接接收所有的请求参数：
```
@PostMapping("/save")
public String save(@RequestParam Map<String, Object> map){
    System.out.println("name：" + map.get("name") + ", age: " + map.get("age"));
    return "name：" + map.get("name") + ", age: " + map.get("age");
}
```

##### (3.)使用map集合来接收JSON数据
用 map 接收 Controller 直接接收所有的请求参数：
```
@PostMapping("/save")
public String save(@RequestBody Map<String, Object> map){
    System.out.println("name：" + map.get("name") + ", age: " + map.get("age"));
    return "name：" + map.get("name") + ", age: " + map.get("age");
}
```

##### (4.)通过对象接收 JSON 数据
如果一个 get 请求的参数太多，我们构造一个对象来简化参数的接收方式。
```
@PostMapping("/save")
public String save(@RequestBody  User user){
 System.out.println("name is: " + user.getName() +  " age is:" + user.getAge());
 return "name is: " + user.getName() +  " age is:" + user.getAge();
}
```

# 九.Springboot打包发布
Springboot打包一般分为两种；一种是打包成 jar 包直接执行，另一种是打包成 war 包放到 tomcat 等外部服务器下。
>Springboot内置了tomcat，所以把它打包成jar包就可以免去tomcat的配置了(如果是打包成war包，那还是要配置tomcat的)。

### 1.检查端口
打包前确认工程中指定的端口在服务器在未被占用
application.properties文件中:
```
server.port=8090
```
>使用外部Tomcat部署访问的时候，application.properties(或者application.yml)中配置的 server.port= server.servlet.context-path= 将失效，请使用tomcat的端口/tomcat/webapps下项目名进行访问。

### 2.确保数据源连接参数正确
开发时若使用的是本地数据库，那在打包前将数据库连接参数修改为目标数据库 在application.properties文件中配置数据库连接属性:
```
#datasource
spring.datasource.driver-class-name=com.mysql.jdbc.Driver
spring.datasource.url=jdbc:mysql://数据库所在主机ip:3306/数据库名?useSSL=true&characterEncoding=utf-8
spring.datasource.username = ***
spring.datasource.password = ***
```

### 3.通过jar包发布
SpringBoot内置了tomcat，打包成jar包就可以直接运行了。
##### (1.)运行打包任务
![](/images/ce73061e321e2f673f4d88ef8ef234db.webp)
##### (2.)生成jar包
打包任务完成以后会生成target文件夹。
![](/images/b0c767585cfdf8b2561d3b6e534a865e.webp)
##### (3.)运行jar包
在自己的云服务器上面或者是本地服务器上面(必须要安装jdk环境)启动项目。
```
java -jar xxx.jar
```
##### (4.)通过浏览器访问
通过浏览器访问Ip地址加端口号就可以访问了。

### 4.通过war包发布
##### (1)修改默认打包方式，将打包方式改为war
```
<project>
  <version>0.0.1-SNAPSHOT</version><!--打包时版本号-->
  <name>demo</name><!--打包时名称-->
  <description>Demo project for SpringBoot</description><!--打包时简介-->

  <!--在打包到生产环境Tomcat时指明打包方式-->
  <packaging>war</packaging>
</project>
```
##### (2)排除SpringBoot内置的tomcat的容器
```
<!--当打war包到tomcat时，自动排除内置的tomcat，避免二者产生冲突-->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-tomcat</artifactId>
    <!--打包的时候可以不用包进去，别的环境依然会提供。事实上该依赖理论上可以参与编译，测试，运行等周期。相当于compile，但是打包阶段做了exclude操作-->
    <scope>provided</scope>
</dependency>
```
##### (3)继承SpringBootServletInitializer类，并重写config方法
全称：org.springframework.boot.web.servlet.support.SpringBootServletInitializer，官方文档也有详细介绍为什么要继承。
```
@SpringBootApplication
public class Application extends SpringBootServletInitializer {
    @Override
    protected SpringApplicationBuilder configure(SpringApplicationBuilder application) {
        return application.sources(Application.class);
    }
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```
##### (4)端口，路径设置
这里需要注意两点:
- 在application.properties或者在application.yml中对tomcat配置的port和context-path对war文件是不起作用的，那个配置只对SpringBoot内置的tomcat起作用。当把war部署到生产环境时，端口就是生产环境服务器所配置好的端口，context-path就是war的文件名，或者自己在tomcat中配置的其他名字。
- 为了防止应用上下文所导致的项目访问资源加载不到的问题，建议pom.xml文件中<build></build>标签下添加<finalName></finalName>标签：
```
<build>
  <!--打war包到生产环境时配置-->
  <finalName>photoSystem</finalName>
  <plugins>
      <plugin>
          <groupId>org.springframework.boot</groupId>
          <artifactId>spring-boot-maven-plugin</artifactId>
      </plugin>
  </plugins>
</build>
```
##### (5)打包
打开maven projects任务:
1. 执行clean任务
2. 执行package任务
   ![](/images/627557550f4e536efb889ee75c47f22b.webp)
##### (6)将war包配置到tomcat
1.将war包放置到tomcat的webapps里面去。
2.在浏览器里面访问 http://localhost:8080/demo-0.0.1-SNAPSHOT/hello。


参考资料:
[SpringBoot开发详解](https://blog.csdn.net/qq_31001665)

[基于SpringBoot开发](https://blog.csdn.net/xwd718)

[SpringBoot项目部署到阿里云服务器全流程](https://blog.csdn.net/Mou_Yang/article/details/102137861)

[使用SpringBoot打war包，并部署到tomcat下](https://juejin.im/post/5e6a4dc66fb9a07c7c2d76e5)

[SpringBoot打war包，部署到外部tomcat](https://www.jiweichengzhu.com/article/99a9f76a28b14c1dbeb726c652c2ca88)

[SpringBoot项目部署到阿里云服务器全流程](https://blog.csdn.net/Mou_Yang/article/details/102137861)

[使用springboot打war包，并部署到tomcat下](https://juejin.im/post/5e6a4dc66fb9a07c7c2d76e5)

[springboot打war包，部署到外部tomcat](https://www.jiweichengzhu.com/article/99a9f76a28b14c1dbeb726c652c2ca88)

[基于SpringBoot搭建应用开发框架](https://www.cnblogs.com/chiangchou/p/sunny-1.html)

[SpringBoot基础教程](https://blog.nowcoder.net/youzhihua/archive)

[快速入门 Java 后端开发的正确姿势](https://juejin.im/post/5d5f8927e51d4561da620168)

[后端开发教程系列-java向](https://blog.csdn.net/zhou307/article/details/82352405)

[Redis的介绍及使用](https://www.cnblogs.com/baichunyu/p/11631660.html)

[Java后端开发框架](https://blog.csdn.net/lorogy/article/details/100663659)

[后端成长之路：从菜鸟到架构](https://www.jianshu.com/p/f62379fe9f80)

[Spring Boot 集成教程](https://www.qikegu.com/docs/2523)

[SpringBoot系列](https://blog.csdn.net/xcbeyond/category_7781626.html)

[SpringBoot系列之学习教程汇总](https://juejin.im/post/5f185508f265da22f1474317)

[SpringBoot系列文章](http://spring.hhui.top/spring-blog/SpringBoot/)

[Spring Boot干货系列](http://tengj.top/categories/Spring-Boot%E5%B9%B2%E8%B4%A7%E7%B3%BB%E5%88%97/)

[Spring Boot学习笔记](https://blog.csdn.net/gnail_oug/category_9274381.html)




