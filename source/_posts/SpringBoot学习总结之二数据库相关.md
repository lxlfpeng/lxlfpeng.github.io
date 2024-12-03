---
title: SpringBoot学习总结之二数据库相关
date: 2021-04-25 
categories: 
  - SpringBoot
---

# 一.常见的数据库访问框架
在Web项目开发中，数据库的访问是必不可少的。
|ORM持久化技术| 模板类|
|-|-|
|JDBC(JdbcTemplate) |	org.springframework.jdbc.core.JdbcTemplate|
|JPA	|org.springfrmaework.orm.jpa.JpaTemplate|
|IBatis(MyBatis)|	org.springframework.orm.ibatis.SqlMapClientTemplate|

### 1.JdbcTemplate
JdbcTemplate是Spring对JDBC的模板封装，提供了一套JDBC模板，能够让我们写持久层代码时减少冗余代码，简化JDBC代码，使代码更加简洁。Spring Boot默认支持JdbcTemplate（无需配置）。JdbcTemplate在实际开发中一般不会使用，``通常都是使用MyBatis、Hibernate等更加成熟、优秀的数据持久层框架``。

### 2.JPA
JPA全称是Java Persistence API，即java持久化API，是sun公司推出的一套基于ORM的``规范``，内部由一系列的接口和抽象类构成。
- Hibernate :JPA是规范，Hibernate除了作为ORM框架之外，它也是一种JPA实现。
- Spring Data JPA :Spring Data JPA是Spring提供的一套对JPA操作更加高级的封装，是在JPA规范下的专门用来进行数据持久化的解决方案。
>JPA（Java Persistence API）是java持久层API，一个简化对象关系映射来管理Java应用程序中关系数据库的规范，可以直接使用对象而不是使用sql语句。在JPA中，我们可以通过实体类轻松地操作数据库中的表。JPA只是一种规范，它需要第三方自行实现其功能，在众多框架中Hibernate是最为强大的一个，Spring Data JPA是Spring提供的一套对JPA操作更加高级的封装，是在JPA规范下的专门用来进行数据持久化的解决方案。

### 3.MyBatis
MyBatis是目前Java平台最为流行的ORM框架

### 4.优缺点比较
- JDBC直接操作:比较古老，开发起来太麻烦。
- JdbcTemplate：spring在jdbc上面做了深层次的封装，使用spring的注入功能，可以把DataSource注册到JdbcTemplate之中。Spring-data-jpa引入的时候，JdbcTemplate必然会被引入的。
- Spring-data-jpa： 使用hibernate作为实现，特点就是所有的 SQL 都用 Java 代码来生成，不用跳出程序去写（看） SQL ，有着编程的完整性，缺点是处理复杂业务时，灵活度差。
- Mybatis插件：比较时髦，比较适合sql复杂，或者对性能要求高的应用，因为sql都是自己写的。

# 二.通过JdbcTemplate访问数据库
### 1.创建数据库表
```
CREATE TABLE `test_user` (
  `id` int(10) NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `username` varchar(30) NOT NULL COMMENT '昵称',
  `age` int(11) NOT NULL COMMENT '年龄',
  `password` varchar(35) NOT NULL COMMENT '密码',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8
```

### 2.POM依赖添加
在POM文件中我们需要引入一些依赖来配置数据源
```
<!--数据库连接jdbc依赖-->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-jdbc</artifactId>
</dependency>
<!--mysql链接依赖-->
<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
</dependency>
```

### 3.配置连接MySQL数据库
```
spring.datasource.url = jdbc:mysql://127.0.0.1:3306/test_tale?useUnicode=true&characterEncoding=utf-8&serverTimezone=GMT%2B8
spring.datasource.username = root
spring.datasource.password = xxxx
spring.datasource.driverClassName = com.mysql.jdbc.Driver
```

### 4.创建实体对象
User.java
```
public class User {
    private int id;
    private String username;
    private int age;
    private String password;

    //类中显示声明有参构造方法后，必选显示声明一个无参构造方法，否则报错误：No default constructor found; nested exception is java.lang.NoSuchMethodException
    public User() {
    }
    public User(int id, String username, int age, String password) {
        this.id = id;
        this.username = username;
        this.age = age;
        this.password = password;
    }
    //省略get/set方法
}
```

### 5.定义接口
UserService.java
```
public interface UserService {
    /**
     * 获取用户总量
     * @return
     */
    String getAllUsers();

    /**
     * 获取全部用户
     * @return
     */
    List<Map<String, Object>> findAll();

    /**
     * 根据id获取用户
     * @param id
     * @return
     */
    User getById(int id);

    /**
     * 增加用户
     * @param user
     * @return
     */
    int addUser(User user);

    /**
     * 根据id删除用户
     * @param id
     * @return
     */
    int deleteUser(int id);
}
```

### 6.通过jdbcTemplate实现接口中定义的数据访问操作
UserServiceImpl.java
```
@Service
public class UserServiceImpl implements UserService{
    @Autowired
    private JdbcTemplate jdbcTemplate;
    @Override
    public String getAllUsers(){
        return jdbcTemplate.queryForObject("select count(1) from test_user", String.class);
    }

    @Override
    public List<Map<String, Object>> findAll() {
        String sql = "select * from test_user";
        List<Map<String, Object>> list = jdbcTemplate.queryForList(sql);
        return list;
    }
    @Override
    public User getById(int id) {
        String sql = "select username,age,password from test_user where id = ? ";
        List<User> usr = jdbcTemplate.query(sql,new Object[]{id},new BeanPropertyRowMapper(User.class));
        User user = null;
        if(!usr.isEmpty()){
            user = usr.get(0);
        }
        return user;
    }
    /**
     * 插入用户-防止sql注入-可以返回该条记录的主键
     * @param user
     * @return
     */
    @Override
    public int addUser(User user) {
        String sql = "insert into test_user(id,username,age,password) values(null,?,?,?)";
        KeyHolder keyHolder = new GeneratedKeyHolder();
        int resRow = jdbcTemplate.update(new PreparedStatementCreator() {
            @Override
            public PreparedStatement createPreparedStatement(Connection connection) throws SQLException {
                PreparedStatement ps = connection.prepareStatement(sql,new String[]{"id"});
                ps.setString(1,user.getUsername());
                ps.setInt(2,user.getAge());
                ps.setString(3,user.getPassword());
                return ps;
            }
        },keyHolder);
        System.out.println("操作记录数："+resRow+" 主键："+keyHolder.getKey());
        return Integer.parseInt(keyHolder.getKey().toString());
    }
    @Override
    public int deleteUser(int id) {
        String sql = "delete from test_user where id = ?";
        return jdbcTemplate.update(sql,id);
    }
}
```

### 7.定义controller
UserController.java
```
@RestController
@RequestMapping("/users")
public class UserController {
    @Autowired
    private UserService service;

    //http://127.0.0.1:8080/users/getAllUsers
    @RequestMapping(value = "/getAllUsers", method = RequestMethod.GET)
    public String getAllUsers() {
        return service.getAllUsers();
    }

    //http://127.0.0.1:8080/users/addUser
    @RequestMapping(value = "/addUser", method = RequestMethod.POST)
    //借助一个注解：@RequestBody，加上这个注解后，Springmvc会从请求体中获取数据并进行相应的转换。
    public int addUser(@RequestBody User user) {
        int res = service.addUser(user);
        return res;
    }

    //http://127.0.0.1:8080/users/findAllUsers
    @RequestMapping(value = "/findAllUsers", method = RequestMethod.GET)
    public List<Map<String, Object>> findAll() {
        List<Map<String, Object>> list = service.findAll();
        return list;
    }

    //http://127.0.0.1:8080/users/getUser
    @RequestMapping(value = "/getUser/{id}", method = RequestMethod.GET)
    public User getUserById(@PathVariable int id) {
        User User = service.getById(id);
        return User;
    }

    //http://127.0.0.1:8080/users/deleteUserByUserId
    @RequestMapping(value = "/deleteUserByUserId/{id}", method = RequestMethod.DELETE)
    public int deleteUser(@PathVariable int id) {
        System.out.println(id);
        int res = service.deleteUser(id);
        return res;
    }
}
```

# 三.通过MyBatis访问数据库
SpringBoot 整合 Mybatis 有两种常用的方式，一种就是我们常见的 xml 的方式 ，还有一种是全注解的方式。我觉得这两者没有谁比谁好，在 SQL 语句不太长的情况下，我觉得全注解的方式一定是比较清晰简洁的。但是，复杂的 SQL 确实不太适合和代码写在一起。
### 1.创建数据表
```
CREATE TABLE `test_user` (
  `id` int(10) NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `username` varchar(30) NOT NULL COMMENT '昵称',
  `age` int(11) NOT NULL COMMENT '年龄',
  `password` varchar(35) NOT NULL COMMENT '密码',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8
```

### 2.配置 pom 文件中的相关依赖
```
<!-- 加载mybatis整合进springboot -->
<dependency>
	<groupId>org.mybatis.spring.boot</groupId>
	<artifactId>mybatis-spring-boot-starter</artifactId>
	<version>2.1.1</version>
</dependency>
```

### 3.配置连接MySQL数据库
```
spring.datasource.url = jdbc:mysql://127.0.0.1:3306/test_tale?useUnicode=true&characterEncoding=utf-8&serverTimezone=GMT%2B8
spring.datasource.username = root
spring.datasource.password = xxxx
spring.datasource.driverClassName = com.mysql.jdbc.Driver
```
>这里使用的数据库配置信息和之前使用JDBC时是一致的，可以无需更改。

### 4.创建用户类 Bean
```
public class User {
    private int id;
    private String username;
    private int age;
    private String password;

    //类中显示声明有参构造方法后，必选显示声明一个无参构造方法，否则报错误：No default constructor found; nested exception is java.lang.NoSuchMethodException
    public User() {
    }
    public User(int id, String username, int age, String password) {
        this.id = id;
        this.username = username;
        this.age = age;
        this.password = password;
    }
    //省略get/set方法
}
```

### 5.MyBatis的全注解的方式
全注解的方式，这种方式和后面提到的 xml 的方式的区别仅仅在于 一个将 sql 语句写在 java 代码中，一个写在 xml 配置文件中。全注方式解转换成 xml 方式仅需做一点点改变即可。
**项目结构**
![](/images/a4c2b53b4ed6251c91b7fbc04f332bca.webp)
##### (1.)Dao层
MyBatisUserDao.java
```
@Mapper
public interface MyBatisUserDao {
    /**
     * 通过名字查询用户信息
     */
    @Select("SELECT * FROM test_user WHERE username = #{username}")
    List<User> findUserByName(@Param("username") String username);

    /**
     * 查询所有用户信息
     */
    @Select("SELECT * FROM test_user")
    List<User> findAllUser();

    /**
     * 插入用户信息
     */
    @Insert("INSERT INTO test_user(username, age,password) VALUES(#{username}, #{age}, #{password})")
    void insertUser(@Param("username") String username, @Param("age") Integer age, @Param("password") String password);

    /**
     * 根据 id 删除用户信息
     */
    @Delete("DELETE from test_user WHERE id = #{id}")
    void deleteUser(@Param("id") int id);
}
```
##### (2.)service层
```
@Service
public class MyBatisUserService {
    @Autowired
    private MyBatisUserDao userDao;

    /**
     * 根据名字查找用户
     */
    public List<User> selectUserByName(String name) {
        return userDao.findUserByName(name);
    }

    /**
     * 查找所有用户
     */
    public List<User> selectAllUser() {
        return userDao.findAllUser();
    }

    /**
     * 插入用户
     */
    public void insertUser(User user) {
        userDao.insertUser(user.getUsername(),user.getAge(),user.getPassword());
    }

    /**
     * 根据id 删除用户
     */

    public void deleteService(int id) {
        userDao.deleteUser(id);
    }
}
```
##### (3.)Controller层
```
@RestController
@RequestMapping("mybatis/user")
public class MyBatisUserController {
    @Autowired
    private MyBatisUserService userService;

    //http://127.0.0.1:8080/mybatis/user/getAllUsers
    @RequestMapping(value = "/getAllUsers", method = RequestMethod.GET)
    public List<User> getAllUsers() {
        return userService.selectAllUser();
    }

    //http://127.0.0.1:8080/mybatis/user/selectUserByName
    @GetMapping("/selectUserByName")
    public List<User> selectUserByName(@RequestParam("userName") String userName) {
        return userService.selectUserByName(userName);
    }

    //http://127.0.0.1:8080/mybatis/user/insert
    @RequestMapping(value = "/insert", method = RequestMethod.POST)
    public List<User> insertUser(@RequestBody User user) {
        userService.insertUser(user);
        return userService.selectAllUser();
    }
    //http://127.0.0.1:8080/mybatis/user/delete
    @RequestMapping(value = "/delete", method = RequestMethod.POST)
    public List<User> testDelete(int id) {
        userService.deleteService(id);
        return userService.selectAllUser();
    }
}
```

### 6.MyBatis的xml的方式
![image.png](/images/3406ae8943bcf37605bf99d492997b1f.webp)
##### (1.)UserMapper文件
只演示一个根据姓名找人的方法，为了让UserMapper能够让别的类进行引用，可以在UserMapper类上添加@Mapper注解：
```
@Mapper
public interface  UserMapper {
    List<User> queryUserByUserName(String username);
}
```
直接在Mapper类上面添加注解@Mapper，这种方式要求每一个mapper类都需要添加此注解，比较麻烦。可以在启动类中添加@MapperScan注解，指定要扫描的Mapper类的包的路径也可以。
```
@SpringBootApplication
//指定要扫描的Mapper类的包的路径
@MapperScan("com.dapeng.springboot.mapper")
public class SpringbootApplication {

}
```

##### (2.)编写UserMapper.xml文件
- namespace中需要与使用@Mapper的接口对应。
- UserMapper.xml文件名称必须与使用@Mapper的接口一致。
- 标签中的id必须与@Mapper的接口中的方法名一致，且参数一致。
```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">

<!--指定需要映射的mapper类的路径-->
<mapper namespace="com.example.springboottest.mybatis.UserMapper">
    <!--指定映射的方法及映射的dao类-->
    <select id="queryUserByUserName" parameterType="String" resultType="com.example.springboottest.domain.User">
        SELECT *
        FROM test_user
        WHERE username = #{username}
    </select>
</mapper>
```

##### (3.)配置文件增加mapper识别路径
application.properties配置文件中加入下面这句话：
```
mybatis.mapper-locations=classpath:mapper/*.xml
```

##### (4.)Controller层
```
@RestController
@RequestMapping("mybatis/user")
public class MyBatisUserController {
    
    @Autowired
    private UserMapper userMapper;
    
    //http://127.0.0.1:8080/mybatis/user/queryUserByUserName
    @RequestMapping(value="/queryUserByUserName", method=RequestMethod.GET)
    public List<User> queryUserByUserName(@RequestParam("userName") String userName) {
        return userMapper.queryUserByUserName(userName);
    }
}
```

### 7.Mybatis插件
Mybatis可以直接在xml中通过SQL语句操作数据库，很是灵活。但其操作都要通过SQL语句进行，就必须写大量的xml文件，很是麻烦。通过下面的插件可以简化操作，提升效率。
- Mybatis-Generator:[Mybatis-Generator](https://github.com/mybatis/generator)是Mybatis提供的一个便捷型插件，自动可以为项目生产对应的实体类，Mapper，dao层。
- mybatis-plus:Mybatis-Plus（简称MP）是一个 Mybatis 的增强工具，在 Mybatis 的基础上只做增强不做改变，为简化开发、提高效率而生。这是官方给的定义，关于mybatis-plus的更多介绍及特性，可以参考[mybatis-plus官网](https://baomidou.com/)。其实就是它已经封装好了一些crud方法，不需要再写xml了，直接调用这些方法就行，类似于JPA。

# 四.数据库连接池
### 1.什么是数据库连接池
使用JDBC技术的时候，每次用完了，都会将连接关闭；等到下一次再用的时候，都会将数据库连接再打开。实际上，数据库链接资源是十分宝贵的，在小型的项目中还看不出来，在高并发的项目中，这样频繁的打开和关闭数据库链接会给服务器带来压力，十分影响效率。所谓的数据库连接池技术，就是用来分配，管理，释放数据库连接的，数据库连接池负责分配、管理和释放数据库连接，它允许应用程序重复使用一个现有的数据库连接，而不是再重新建立一个；释放空闲时间超过最大空闲时间的数据库连接来避免因为没有释放数据库连接而引起的数据库连接遗漏。这项技术能明显提高对数据库操作的性能。
**常用的主流开源数据库连接池有C3P0、DBCP、Tomcat Jdbc Pool、BoneCP、Druid等。**
Spring Boot2.0默认使用的连接池是 [HikariCP](https://github.com/brettwooldridge/HikariCP) ，当在在依赖中引入了`spring-boot-starter-jdbc` 或者 `spring-boot-starter-data-jpa` ，且application.properties中没有配置``spring.datasource.type ``为其他的DataSource时。Spring Boot 会默认使用HiKariCP。

### 1.修改数据库连接池为druid
[Druid](https://github.com/alibaba/druid)是阿里巴巴的一个开源项目，号称为监控而生的数据库连接池，在功能、性能、扩展性方面都超过其他例如``DBCP、C3P0、BoneCP、Proxool、JBoss DataSource``等连接池，而且Druid已经在阿里巴巴部署了超过600个应用，通过了极为严格的考验。
1. 如果需要使用其他的连接池，例如druid连接池，则需要引入 druid 依赖：
```
<!-- druid -->
<dependency>
   <groupId>com.alibaba</groupId>
   <artifactId>druid-spring-boot-starter</artifactId>
   <version>1.1.10</version>
</dependency>
```
2. 并且在application.properties中配置
```
#表明使用Druid连接池
spring.datasource.type=com.alibaba.druid.pool.DruidDataSource
```
3. 配置连接池的相关属性，这些参数根据自己的需要灵活配置即可：
```
#初始化时建立物理连接的个数。
spring.datasource.druid.initial-size=5
#最大连接池数量
spring.datasource.druid.max-active=20
#最小连接池数量
spring.datasource.druid.min-idle=5
#获取连接时最大等待时间，单位毫秒
spring.datasource.druid.max-wait=3000
#是否缓存preparedStatement，也就是PSCache，PSCache对支持游标的数据库性能提升巨大，比如说oracle,在mysql下建议关闭。
spring.datasource.druid.pool-prepared-statements=false
#要启用PSCache，必须配置大于0，当大于0时，poolPreparedStatements自动触发修改为true。在Druid中，不会存在Oracle下PSCache占用内存过多的问题，可以把这个数值配置大一些，比如说100
spring.datasource.druid.max-open-prepared-statements= -1
#配置检测可以关闭的空闲连接间隔时间
spring.datasource.druid.time-between-eviction-runs-millis=60000
# 配置连接在池中的最小生存时间
spring.datasource.druid.min-evictable-idle-time-millis= 300000
spring.datasource.druid.max-evictable-idle-time-millis= 400000
```


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
