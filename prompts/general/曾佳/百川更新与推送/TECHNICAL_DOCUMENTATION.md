# 技术文档 (TECHNICAL_DOCUMENTATION.md)

## 1. 系统架构

### 1.1 总体架构
该系统采用Spring Boot框架开发，是一个典型的后端服务应用，主要负责将MySQL数据库中的报警信息推送到SQL Server数据库，并从SQL Server数据库查询反馈信息更新到MySQL数据库中。系统采用分层架构设计，包括控制器层、服务层、数据访问层和基础设施层。

### 1.2 分层架构

#### 1.2.1 控制器层 (Controller)
负责处理HTTP请求，提供API接口。目前包含一个控制器类：
- `PushUpdateController`：提供手动触发更新反馈数据的接口

#### 1.2.2 服务层 (Service)
包含系统的核心业务逻辑，主要负责：
- 报警信息推送
- 动态数据源切换
- 反馈信息查询与更新
- 定时任务执行

主要服务类：
- `AlarmPushService`：实现报警信息推送和反馈信息更新的核心业务逻辑

#### 1.2.3 数据访问层 (Mapper/DAO)
负责与数据库交互，包括：
- MyBatis Mapper接口：用于操作MySQL数据库
- JdbcTemplate：用于操作多种数据源

主要数据访问组件：
- `AlarmInfoMapper`：MyBatis Mapper接口，用于操作报警信息表

#### 1.2.4 基础设施层
提供系统的基础设施支持，包括：
- 数据源配置
- 定时任务配置
- 日志配置
- 连接池配置

主要基础设施组件：
- `DataSourceConfig`：数据源配置类
- `DataSourceContextHolder`：数据源上下文持有者
- `DynamicDataSource`：动态数据源实现

### 1.3 系统模块图
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Controller层   │────▶│   Service层     │────▶│  Data Access层  │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                        │                        │
        │                        │                        ▼
        │                        │            ┌─────────────────┐
        │                        │            │                 │
        │                        │            │  MySQL数据库     │
        │                        │            │                 │
        │                        │            └─────────────────┘
        │                        │                        │
        │                        ▼                        ▼
        │            ┌─────────────────┐     ┌─────────────────┐
        │            │                 │     │                 │
        │            │ SQL Server数据库1│     │ SQL Server数据库2│
        │            │                 │     │                 │
        │            └─────────────────┘     └─────────────────┘
        │                        │                        │
        ▼                        ▼                        ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  定时任务调度    │     │  重试机制       │     │  日志记录       │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## 2. 核心组件设计

### 2.1 动态数据源组件

#### 2.1.1 设计思路
为了支持根据PC编号动态选择目标SQL Server数据源，系统设计了动态数据源组件，主要包括：
- `DataSourceConfig`：负责配置多种数据源
- `DataSourceContextHolder`：用于保存当前线程使用的数据源标识
- `DynamicDataSource`：实现`AbstractRoutingDataSource`接口，根据当前线程的数据源标识获取对应的数据源

#### 2.1.2 实现细节
- 配置了三种数据源：mysql3（主数据源）、sqlserver、sqlserver2
- 使用`@Qualifier`注解区分不同的数据源
- 通过`ThreadLocal`保存当前线程的数据源标识
- 实现了`determineCurrentLookupKey`方法，根据当前线程的数据源标识获取对应的数据源

### 2.2 报警推送组件

#### 2.2.1 设计思路
报警推送组件负责将MySQL数据库中的报警信息推送到SQL Server数据库，主要包括：
- 报警信息查询
- 动态数据源选择
- 存储过程调用
- 推送状态更新

#### 2.2.2 实现细节
- 使用`AlarmInfoMapper`查询未推送的报警信息
- 根据PC编号前缀选择目标数据源
- 使用`SimpleJdbcCall`调用SQL Server存储过程`dbo.vpsAlert_Append`
- 推送成功后更新报警信息的推送状态为"已推送"

### 2.3 重试机制组件

#### 2.3.1 设计思路
为了提高推送成功率，系统设计了重试机制，主要包括：
- 最大重试次数配置
- 重试间隔配置
- 重试逻辑实现

#### 2.3.2 实现细节
- 最大重试次数：3次
- 重试间隔：5分钟
- 使用`Thread.sleep`实现重试间隔
- 重试失败后记录日志，保留未推送状态以支持后续重试

### 2.4 反馈信息更新组件

#### 2.4.1 设计思路
反馈信息更新组件负责从SQL Server查询反馈信息，更新到MySQL数据库中，主要包括：
- 待处理报警信息查询
- 反馈信息查询
- 报警信息更新

#### 2.4.2 实现细节
- 查询所有状态不是"OK"的报警信息
- 根据PC编号前缀分类查询反馈信息
- 分批处理查询结果，每批最多20个ID
- 更新报警信息的相关字段，包括报警类型、改善方向、改善人、状态等

### 2.5 定时任务组件

#### 2.5.1 设计思路
定时任务组件负责定时触发报警信息推送，主要包括：
- 小时推送任务
- 天推送任务

#### 2.5.2 实现细节
- 使用Spring Scheduling实现定时任务
- 小时推送：每小时10分执行，推送上一个小时区间内未推送的报警信息
- 天推送：每天执行，推送当天的天报警信息
- 推送完成后调用反馈信息更新功能

## 3. 数据流设计

### 3.1 报警信息推送流程

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  定时任务触发   │────▶│ 查询未推送报警   │────▶│ 动态选择数据源   │
└─────────────────┘     │   信息         │     │                 │
                        └─────────────────┘     └─────────────────┘
                                │                         │
                                ▼                         ▼
                        ┌─────────────────┐     ┌─────────────────┐
                        │ 准备存储过程     │     │ 调用SQL Server  │
                        │  参数           │────▶│ 存储过程        │
                        └─────────────────┘     └─────────────────┘
                                │                         │
                                ▼                         ▼
                        ┌─────────────────┐     ┌─────────────────┐
                        │ 推送成功？      │     │ 推送失败        │
                        │                 │     │                 │
                        └─────────────────┘     └─────────────────┘
                               /  \                        │
                              /    \                       ▼
                             /      \              ┌─────────────────┐
                            ▼        ▼             │ 重试机制        │
┌─────────────────┐     ┌─────────────────┐        │                 │
│ 更新推送状态为  │     │ 记录失败日志    │        └─────────────────┘
│  "已推送"       │     │                 │                 │
└─────────────────┘     └─────────────────┘                 │
                                │                          │
                                ▼                          ▼
                        ┌─────────────────┐     ┌─────────────────┐
                        │ 结束推送流程    │     │ 重试次数达到     │
                        │                 │     │ 最大值？         │
                        └─────────────────┘     └─────────────────┘
                                                      /  \
                                                     /    \
                                                    ▼      ▼
                                      ┌─────────────────┐     ┌─────────────────┐
                                      │ 继续重试        │     │ 记录最终失败日志 │
                                      │                 │     │                 │
                                      └─────────────────┘     └─────────────────┘
```

### 3.2 反馈信息更新流程

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  触发更新       │────▶│ 查询待处理报警   │────▶│ 按PC编号前缀     │
│  （定时或手动）  │     │   信息         │     │ 分类            │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                │                         │
                                ▼                         ▼
                        ┌─────────────────┐     ┌─────────────────┐
                        │ 动态选择数据源   │     │ 分批查询反馈     │
                        │                 │────▶│ 信息            │
                        └─────────────────┘     └─────────────────┘
                                │                         │
                                ▼                         ▼
                        ┌─────────────────┐     ┌─────────────────┐
                        │ 处理反馈数据     │     │ 更新报警信息     │
                        │                 │────▶│                 │
                        └─────────────────┘     └─────────────────┘
                                │                         │
                                ▼                         ▼
                        ┌─────────────────┐     ┌─────────────────┐
                        │ 记录更新日志    │     │ 结束更新流程    │
                        │                 │     │                 │
                        └─────────────────┘     └─────────────────┘
```

## 4. 核心类与方法

### 4.1 数据源配置类

#### 4.1.1 `DataSourceConfig`
**功能**：配置多种数据源，包括mysql3、sqlserver、sqlserver2
**核心方法**：
- `mysql3DataSource()`：配置mysql3数据源
- `sqlserverDataSource()`：配置sqlserver数据源
- `sqlserver2DataSource()`：配置sqlserver2数据源
- `dynamicDataSource()`：创建动态数据源
- 多种JdbcTemplate配置方法

### 4.2 动态数据源实现

#### 4.2.1 `DynamicDataSource`
**功能**：实现动态数据源切换
**核心方法**：
- `determineCurrentLookupKey()`：根据当前线程的数据源标识获取对应的数据源

### 4.3 数据源上下文持有者

#### 4.3.1 `DataSourceContextHolder`
**功能**：保存当前线程的数据源标识
**核心方法**：
- `setDataSourceType()`：设置当前线程的数据源标识
- `getDataSourceType()`：获取当前线程的数据源标识
- `clearDataSourceType()`：清除当前线程的数据源标识

### 4.4 报警推送服务

#### 4.4.1 `AlarmPushService`
**功能**：实现报警信息推送和反馈信息更新的核心业务逻辑
**核心方法**：

##### 4.4.1.1 报警推送相关方法
- `pushAlarmToSqlServer(AlarmInfo alarmInfo)`：推送报警信息到SQL Server
- `selectDataSource(String pcNumber)`：根据PC编号选择数据源
- `prepareStoredProcedureParams(AlarmInfo alarmInfo)`：准备存储过程参数
- `pushHourlyAlarms()`：推送小时报警信息
- `pushDailyAlarms()`：推送天报警信息
- `pushAlarmWithRetry(AlarmInfo alarmInfo)`：带重试机制的报警信息推送

##### 4.4.1.2 反馈信息更新相关方法
- `queryFeedbackAndUpdate()`：查询反馈并更新报警信息
- `queryFeedbackData(List<String> alarmIds, List<String> alarmLevels, JdbcTemplate jdbcTemplate)`：查询反馈数据
- `manualUpdateFeedback()`：手动触发更新报警信息反馈数据

### 4.5 控制器类

#### 4.5.1 `PushUpdateController`
**功能**：提供手动触发更新反馈数据的接口
**核心方法**：
- `updateFeedback()`：处理手动触发更新反馈数据的HTTP请求

### 4.6 实体类

#### 4.6.1 `AlarmInfo`
**功能**：报警信息实体类
**核心字段**：
- `id`：主键ID
- `pcNumber`：PC编号
- `macAddress`：MAC地址
- `alarmMessage`：报警信息详情
- `alarmLevel`：报警级别
- `status`：处理状态
- `pushStatus`：推送状态

## 5. 数据库设计

### 5.1 MySQL数据库

#### 5.1.1 报警信息表 (alarm_info)
**功能**：存储报警信息
**字段说明**：
| 字段名 | 类型 | 描述 |
|-------|------|------|
| id | BIGINT | 主键ID |
| pc_number | VARCHAR | PC编号 |
| mac_address | VARCHAR | MAC地址 |
| location | VARCHAR | 位置信息 |
| responsible_person | VARCHAR | 负责人 |
| alarm_message | VARCHAR | 报警信息详情 |
| alarm_level | VARCHAR | 报警级别 |
| alarm_type | VARCHAR | 报警类型 |
| status | VARCHAR | 处理状态 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |
| resolved_at | DATETIME | 解决时间 |
| improvement_direction | VARCHAR | 改善方向 |
| improver | VARCHAR | 改善人 |
| improvement_time | DATETIME | 改善时间 |
| confirmer | VARCHAR | 确认人 |
| confirmation_time | DATETIME | 确认时间 |
| push_status | VARCHAR | 推送状态 |
| hour_interval | VARCHAR | 小时区间 |
| model | VARCHAR | 设备型号 |

### 5.2 SQL Server数据库

#### 5.2.1 存储过程 `dbo.vpsAlert_Append`
**功能**：接收报警信息并存储
**参数说明**：
| 参数名 | 类型 | 描述 |
|-------|------|------|
| @Line | VARCHAR | 生产线 |
| @PNO | VARCHAR | PC编号 |
| @PRJ | VARCHAR | MAC地址 |
| @Sect | VARCHAR | 部门 |
| @Sort | VARCHAR | 类型 |
| @Desc | VARCHAR | 描述 |
| @User | VARCHAR | 用户 |
| @Code | VARCHAR | 代码 |
| @Text | VARCHAR | 文本 |
| @STP | VARCHAR | 停止标志 |
| @NOR | VARCHAR | 正常标志 |
| @Level | VARCHAR | 级别 |
| @PC | VARCHAR | PC标志 |
| @RUNID | INT | 运行ID |
| @RMOID | INT | 维修ID |

#### 5.2.2 反馈信息表 `vpsALEQ`
**功能**：存储报警反馈信息
**核心字段**：
| 字段名 | 类型 | 描述 |
|-------|------|------|
| AL_CODE | VARCHAR | 报警ID |
| ANALYS_Q | VARCHAR | 报警类型 |
| RSOLVE_Q | VARCHAR | 改善方向 |
| RSOLVE_U | VARCHAR | 改善人 |
| EFFECT_Q | VARCHAR | 效果确认 |
| EFFECT_U | VARCHAR | 确认人 |
| EFFECT_T | DATETIME | 确认时间 |

## 6. 配置信息

### 6.1 应用配置

#### 6.1.1 端口配置
```properties
server.port=8096
```

#### 6.1.2 数据库连接配置

##### 6.1.2.1 MySQL3数据源配置
```properties
spring.datasource.mysql3.url=jdbc:mysql://192.168.1.130:3306/pcmonitor?useUnicode=true&characterEncoding=utf8&serverTimezone=GMT%2B8&sessionVariables=sql_mode='STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION'
spring.datasource.mysql3.username=ems
spring.datasource.mysql3.password=B8n$eQ!zW4%kLmX9
spring.datasource.mysql3.driver-class-name=com.mysql.cj.jdbc.Driver
```

##### 6.1.2.2 SQL Server数据源配置
```properties
spring.datasource.sqlserver.url=jdbc:sqlserver://192.168.2.15:1433;DatabaseName=VPS_CDT
spring.datasource.sqlserver.username=cdtmes
spring.datasource.sqlserver.password=cdt518102@
spring.datasource.sqlserver.driver-class-name=com.microsoft.sqlserver.jdbc.SQLServerDriver
```

##### 6.1.2.3 SQL Server2数据源配置
```properties
spring.datasource.sqlserver2.url=jdbc:sqlserver://192.168.192.11:1433;DatabaseName=VPS_CDT
spring.datasource.sqlserver2.username=cdtmes
spring.datasource.sqlserver2.password=cdt518102@
spring.datasource.sqlserver2.driver-class-name=com.microsoft.sqlserver.jdbc.SQLServerDriver
```

#### 6.1.3 HikariCP连接池配置
```properties
# MySQL3连接池配置
spring.datasource.mysql3.hikari.maximum-pool-size=5
spring.datasource.mysql3.hikari.minimum-idle=2
spring.datasource.mysql3.hikari.connection-timeout=10000
spring.datasource.mysql3.hikari.idle-timeout=300000
spring.datasource.mysql3.hikari.max-lifetime=600000
spring.datasource.mysql3.hikari.leak-detection-threshold=15000

# SQL Server连接池配置
spring.datasource.sqlserver.hikari.maximum-pool-size=5
spring.datasource.sqlserver.hikari.minimum-idle=2
spring.datasource.sqlserver.hikari.connection-timeout=10000
spring.datasource.sqlserver.hikari.idle-timeout=300000
spring.datasource.sqlserver.hikari.max-lifetime=600000
spring.datasource.sqlserver.hikari.leak-detection-threshold=15000

# SQL Server2连接池配置
spring.datasource.sqlserver2.hikari.maximum-pool-size=5
spring.datasource.sqlserver2.hikari.minimum-idle=2
spring.datasource.sqlserver2.hikari.connection-timeout=10000
spring.datasource.sqlserver2.hikari.idle-timeout=300000
spring.datasource.sqlserver2.hikari.max-lifetime=600000
spring.datasource.sqlserver2.hikari.leak-detection-threshold=15000
```

#### 6.1.4 MyBatis配置
```properties
mybatis.mapper-locations=classpath*:mapper/*.xml
mybatis.configuration.map-underscore-to-camel-case=true
```

#### 6.1.5 日志配置
```properties
logging.level.org.example.alarm=debug
logging.level.org.springframework.jdbc=debug
logging.level.org.mybatis=debug

# 使用自定义的logback-spring.xml
logging.config=classpath:logback-spring.xml
```

## 7. 部署与运行

### 7.1 环境要求
- JDK 1.8
- Maven 3.x
- MySQL 8.0
- SQL Server

### 7.2 编译与打包
```bash
# 编译项目
mvn compile

# 打包项目
mvn package

# 跳过测试打包
mvn package -DskipTests
```

### 7.3 运行项目
```bash
# 使用Java命令运行
java -jar alarm-simplified-0.0.1-SNAPSHOT.jar

# 指定配置文件运行
java -jar alarm-simplified-0.0.1-SNAPSHOT.jar --spring.config.location=file:./application.properties
```

### 7.4 运行参数
- `server.port`：指定服务端口，默认8096
- `spring.config.location`：指定配置文件位置

## 8. 监控与日志

### 8.1 日志配置
系统使用Logback框架进行日志记录，日志配置文件为`logback-spring.xml`。日志级别分为DEBUG、INFO、WARN、ERROR四个级别，默认日志级别为DEBUG。

### 8.2 日志输出
- 控制台输出：实时显示系统运行日志
- 文件输出：日志文件存储在`target/logs/`目录下，分为普通日志和错误日志

### 8.3 关键日志信息
- 报警信息推送日志
- 数据源切换日志
- 存储过程调用日志
- 反馈信息更新日志
- 推送失败重试日志

## 9. 性能优化

### 9.1 连接池优化
使用HikariCP连接池，配置了合理的连接池参数：
- 最大连接数：5
- 最小空闲连接数：2
- 连接超时时间：10秒
- 空闲超时时间：300秒
- 最大生命周期：600秒
- 泄漏检测阈值：15秒

### 9.2 分批处理
在查询反馈数据时，采用分批处理的方式，每批最多处理20个ID，避免SQL长度限制和数据库压力过大。

### 9.3 幂等性设计
在推送报警信息前，检查推送状态，已推送的信息跳过，避免重复推送。

### 9.4 重试机制
实现了推送失败的重试机制，提高推送成功率。

## 10. 故障排查

### 10.1 常见问题

#### 10.1.1 数据源连接失败
- 检查数据库连接配置是否正确
- 检查数据库服务是否正常运行
- 检查网络连接是否正常

#### 10.1.2 存储过程调用失败
- 检查存储过程是否存在
- 检查存储过程参数是否正确
- 检查数据库权限是否足够

#### 10.1.3 推送失败
- 检查日志中的错误信息
- 检查目标数据源是否正常
- 检查PC编号前缀是否符合规则

#### 10.1.4 反馈信息更新失败
- 检查反馈信息查询SQL是否正确
- 检查反馈信息字段类型是否匹配
- 检查数据库连接是否正常

### 10.2 日志分析
- 查看系统日志，定位错误信息
- 检查关键节点的日志记录
- 分析错误原因，采取相应的解决措施

## 11. 代码结构

```
src/main/
├── java/
│   └── org/
│       └── example/
│           └── alarm/
│               ├── AlarmApplication.java           # 应用主类
│               ├── config/
│               │   ├── DataSourceConfig.java       # 数据源配置
│               │   ├── DataSourceContextHolder.java# 数据源上下文持有者
│               │   ├── DynamicDataSource.java      # 动态数据源实现
│               │   └── LocalDateTimeTypeHandler.java# 本地日期时间类型处理器
│               ├── controller/
│               │   └── PushUpdateController.java   # 控制器
│               ├── entity/
│               │   └── AlarmInfo.java              # 报警信息实体类
│               ├── mapper/
│               │   └── AlarmInfoMapper.java        # MyBatis Mapper接口
│               ├── schedule/
│               │   └── AlarmPushSchedule.java      # 定时任务配置
│               └── service/
│                   └── AlarmPushService.java       # 报警推送服务
└── resources/
    ├── application.properties                     # 应用配置文件
    ├── logback-spring.xml                         # 日志配置文件
    └── mapper/
        └── AlarmInfoMapper.xml                    # MyBatis Mapper XML文件
```

## 12. 技术选型说明

### 12.1 框架选型
- **Spring Boot**：简化Spring应用的开发和部署，提供自动配置功能
- **MyBatis**：轻量级的持久层框架，支持自定义SQL、存储过程和高级映射
- **Spring Scheduling**：提供定时任务调度功能

### 12.2 数据库选型
- **MySQL**：开源关系型数据库，性能优良，适合存储大量数据
- **SQL Server**：微软的关系型数据库，支持复杂的存储过程和事务处理

### 12.3 连接池选型
- **HikariCP**：高性能的JDBC连接池，具有快速的初始化和获取连接的能力

### 12.4 其他依赖
- **Lombok**：简化Java代码，减少样板代码
- **Spring JDBC**：提供JdbcTemplate，简化JDBC操作

## 13. 变更记录

| 日期 | 版本 | 变更内容 | 变更人 |
|------|------|----------|--------|
| 2025-12-22 | V1.0 | 初始技术文档 | - |