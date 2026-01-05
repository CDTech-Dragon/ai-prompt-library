# 技术文档 (TECHNICAL_DOCUMENTATION.md)

## 1. 系统架构

### 1.1 整体架构

```
┌─────────────────────────────────────────────────────────────────┐
│                       PCM后端系统架构                          │
├─────────────────┬─────────────────┬─────────────────────────────┤
│    表现层       │    业务层       │           数据层            │
├─────────────────┼─────────────────┼─────────────────────────────┤
│   Controller    │   Service       │  Mapper/DAO → 多数据源      │
└─────────────────┴─────────────────┴─────────────────────────────┘
        │                │                      │
        ▼                ▼                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                          前端应用                               │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 核心模块

- **PC设备管理模块**：负责PC设备信息的CRUD操作
- **告警管理模块**：负责告警信息的收集、存储和查询
- **重启记录模块**：负责PC重启记录的管理和查询
- **多数据源模块**：负责多数据源的配置和切换
- **静态资源模块**：负责前端静态资源的访问

## 2. 技术栈

### 2.1 基础框架

| 技术         | 版本       | 用途                     |
|--------------|------------|--------------------------|
| Spring Boot  | 2.x        | 应用框架                 |
| Spring MVC   | 内置       | Web请求处理              |
| MyBatis Plus | 3.x        | ORM框架                  |
| Maven        | 3.x        | 项目构建和依赖管理       |
| JDK          | 8+         | 开发语言环境             |

### 2.2 数据库

| 数据库       | 版本       | 用途                     |
|--------------|------------|--------------------------|
| MySQL        | 5.7+       | 主数据库和业务数据库     |

### 2.3 中间件

| 中间件       | 版本       | 用途                     |
|--------------|------------|--------------------------|
| Redis        | 可选       | 缓存（预留）             |

## 3. 核心组件实现

### 3.1 多数据源实现

#### 3.1.1 数据源配置

```java
@Configuration
public class MySQLConfig {
    // 配置多个数据源
    // 使用@Bean注解定义不同的DataSource
    // ...
}
```

#### 3.1.2 数据源切换

```java
public class DataSourceContextHolder {
    private static final ThreadLocal<String> CONTEXT_HOLDER = new ThreadLocal<>();

    // 设置数据源类型
    public static void setDataSourceType(String dataSourceType) {
        CONTEXT_HOLDER.set(dataSourceType);
    }

    // 获取数据源类型
    public static String getDataSourceType() {
        return CONTEXT_HOLDER.get();
    }

    // 清除数据源类型
    public static void clearDataSourceType() {
        CONTEXT_HOLDER.remove();
    }
}
```

#### 3.1.3 数据源切面

```java
@Aspect
@Component
public class DataSourceAspect {
    // 定义数据源切换的切点
    // 使用@Around注解实现数据源切换逻辑
    // ...
}
```

### 3.2 PC设备信息管理

#### 3.2.1 Controller实现

```java
@RestController
@RequestMapping("/api/pc")
public class PCInfoController {
    @Autowired
    private IPCInfoService pcInfoService;

    // 分页查询PC设备信息
    @GetMapping("/info/page")
    public CommonResult<PageResult<PCInfo>> getPCInfoByPage(@RequestParam(defaultValue = "1") Integer current,
                                                            @RequestParam(defaultValue = "50") Integer size) {
        // 实现分页查询逻辑
        // ...
    }
}
```

#### 3.2.2 Service实现

```java
@Service
public class PCInfoServiceImpl extends ServiceImpl<PCInfoMapper, PCInfo> implements IPCInfoService {
    @Override
    public PageResult<PCInfo> getPCInfoByPage(Integer current, Integer size) {
        // 实现业务逻辑
        // ...
    }
}
```

### 3.3 告警信息管理

#### 3.3.1 Controller实现

```java
@RestController
@RequestMapping("/api/alarm")
public class AlarmInfoController {
    @Autowired
    private IAlarmInfoService alarmInfoService;

    // 获取今日告警信息
    @GetMapping("/today")
    public CommonResult<List<AlarmInfo>> getTodayAlarmInfo() {
        // 实现今日告警查询逻辑
        // ...
    }
}
```

### 3.4 静态资源处理

```java
@RestController
public class StaticResourceController {
    // 处理根路径请求
    @GetMapping(value = {"", "/", "*.html"})
    public ModelAndView index() {
        ModelAndView modelAndView = new ModelAndView();
        modelAndView.setViewName("index.html");
        return modelAndView;
    }
}
```

## 4. API接口设计

### 4.1 PC设备信息接口

| 接口URL                | 方法 | 参数                          | 描述                |
|------------------------|------|-------------------------------|--------------------|
| /api/pc/info/page      | GET  | current: 页码, size: 每页条数 | PC设备信息分页查询  |

### 4.2 告警信息接口

| 接口URL                | 方法 | 参数                          | 描述                |
|------------------------|------|-------------------------------|--------------------|
| /api/alarm/today       | GET  | 无                            | 今日告警信息查询    |
| /api/alarm/page        | GET  | current: 页码, size: 每页条数 | 告警信息分页查询    |

### 4.3 重启记录接口

| 接口URL                | 方法 | 参数                          | 描述                |
|------------------------|------|-------------------------------|--------------------|
| /api/reboot/page       | GET  | current: 页码, size: 每页条数 | 重启记录分页查询    |

## 5. 数据库设计

### 5.1 主要表结构

#### 5.1.1 PC设备信息表 (pc_info)

| 字段名       | 数据类型    | 约束         | 描述                |
|--------------|-------------|--------------|--------------------|
| id           | bigint      | PRIMARY KEY  | 主键ID              |
| pc_no        | varchar(50) | UNIQUE NOT NULL | PC编号          |
| pc_name      | varchar(100)| NOT NULL     | PC名称              |
| status       | varchar(20) | NOT NULL     | 状态                |
| config       | varchar(255)|              | 配置信息            |
| create_time  | datetime    | NOT NULL     | 创建时间            |
| update_time  | datetime    | NOT NULL     | 更新时间            |

#### 5.1.2 告警信息表 (alarm_info)

| 字段名       | 数据类型    | 约束         | 描述                |
|--------------|-------------|--------------|--------------------|
| id           | bigint      | PRIMARY KEY  | 主键ID              |
| alarm_type   | varchar(50) | NOT NULL     | 告警类型            |
| alarm_content| text        | NOT NULL     | 告警内容            |
| alarm_time   | datetime    | NOT NULL     | 告警时间            |
| pc_no        | varchar(50) | NOT NULL     | 关联PC编号          |
| status       | varchar(20) | NOT NULL     | 告警状态            |

#### 5.1.3 重启记录表 (reboot_record)

| 字段名       | 数据类型    | 约束         | 描述                |
|--------------|-------------|--------------|--------------------|
| id           | bigint      | PRIMARY KEY  | 主键ID              |
| pc_no        | varchar(50) | NOT NULL     | PC编号              |
| reboot_time  | datetime    | NOT NULL     | 重启时间            |
| reboot_reason| text        |              | 重启原因            |
| operator     | varchar(50) |              | 操作人员            |

## 6. 部署说明

### 6.1 环境要求

- JDK 8+
- MySQL 5.7+
- Maven 3.x

### 6.2 部署步骤

1. **克隆项目**
   ```bash
   git clone <项目地址>
   cd pcm-backend
   ```

2. **配置数据库**
   - 修改 `src/main/resources/application.properties` 文件中的数据库配置
   - 确保数据库已创建并配置正确的访问权限

3. **编译项目**
   ```bash
   mvn clean compile
   ```

4. **运行项目**
   ```bash
   mvn spring-boot:run
   ```
   或使用打包后的jar文件运行：
   ```bash
   mvn package
   java -jar target/pcm-backend-1.0.0.jar
   ```

5. **访问系统**
   - API接口：`http://localhost:8095/api/`
   - 前端页面：`http://localhost:8095/`

## 7. 开发规范

### 7.1 代码规范

- 遵循Spring Boot编码规范
- 使用驼峰命名法
- 为所有函数添加函数级注释
- 确保文件编码为UTF-8

### 7.2 API规范

- 所有API接口使用统一前缀 `/api`
- 使用RESTful风格设计API
- 返回格式统一使用CommonResult封装
- 分页接口返回PageResult对象

### 7.3 多数据源规范

- 使用`@DataSource`注解指定数据源
- 确保在事务边界内切换数据源
- 避免在同一事务中频繁切换数据源

## 8. 问题排查

### 8.1 常见问题

1. **API 404错误**
   - 检查Controller的RequestMapping路径是否正确
   - 确保API前缀`/api`已正确添加

2. **数据源切换失败**
   - 检查`@DataSource`注解是否正确使用
   - 确保数据源名称与配置一致

3. **静态资源访问失败**
   - 检查静态资源的存放路径
   - 确保静态资源配置没有拦截API请求

4. **中文乱码问题**
   - 确保文件编码为UTF-8
   - 检查数据库连接字符串中的编码配置

## 9. 版本历史

| 版本号 | 日期       | 描述                     |
|--------|------------|--------------------------|
| 1.0.0  | 2025-12-18 | 初始版本，包含核心功能   |
