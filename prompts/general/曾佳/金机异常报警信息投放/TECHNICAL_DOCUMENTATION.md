# 金机投放异常报警系统技术文档

## 1. 项目概述
金机投放异常报警系统是一个基于Spring Boot的自动化监控系统，用于定期检查长沙和深圳两个数据源的金机投放情况，并将异常数据插入到130数据源的alarm_info表中。系统支持定时任务和手动触发两种检查方式，确保金机投放的规范性和准确性。

## 2. 技术栈

### 2.1 核心技术
- **Spring Boot 2.7.18**：应用框架
- **Java 1.8**：开发语言
- **MySQL 5.7+**：数据库
- **Spring JDBC**：数据访问层
- **Maven 3.8.1**：项目管理工具

### 2.2 辅助依赖
- **Lombok**：简化Java代码
- **Hutool 5.8.22**：Java工具库
- **SLF4J + Logback**：日志框架

## 3. 项目结构

```
com.cdtech
├── config              # 配置类
│   ├── DataSourceConfig.java        # 多数据源配置
│   └── ScheduledConfig.java         # 定时任务配置
├── controller          # 控制器层
│   └── AlarmController.java         # 报警系统API接口
├── service             # 业务逻辑层
│   ├── AlarmService.java            # 报警服务接口
│   └── impl
│       └── AlarmServiceImpl.java    # 报警服务实现
└── GoldenSampleAlarmApplication.java # 应用主类
```

### 3.1 主要文件说明

| 文件名 | 路径 | 功能描述 |
| --- | --- | --- |
| GoldenSampleAlarmApplication.java | src/main/java/com/cdtech/ | 应用主类，Spring Boot应用入口 |
| DataSourceConfig.java | src/main/java/com/cdtech/config/ | 多数据源配置，配置长沙、深圳和130三个数据源 |
| ScheduledConfig.java | src/main/java/com/cdtech/config/ | 定时任务配置，配置场景1和场景2的定时执行 |
| AlarmController.java | src/main/java/com/cdtech/controller/ | API接口控制器，提供手动触发检查的接口 |
| AlarmService.java | src/main/java/com/cdtech/service/ | 报警服务接口，定义检查方法 |
| AlarmServiceImpl.java | src/main/java/com/cdtech/service/impl/ | 报警服务实现类，实现业务逻辑 |
| application.yml | src/main/resources/ | 应用配置文件，包含数据源连接信息 |
| logback-spring.xml | src/main/resources/ | 日志配置文件，配置日志输出和轮转策略 |

## 4. 核心功能实现

### 4.1 多数据源配置

系统使用Spring Boot的多数据源配置，通过`@Configuration`和`@Bean`注解实现三个数据源的配置：

- 长沙数据源：用于读取长沙地区的金机投放数据
- 深圳数据源：用于读取深圳地区的金机投放数据
- 130数据源：用于存储报警信息

**关键代码**：
```java
@Configuration
public class DataSourceConfig {
    @Bean(name = "chsDataSource")
    @ConfigurationProperties(prefix = "spring.datasource.chs")
    public DataSource chsDataSource() {
        return DataSourceBuilder.create().build();
    }

    // 深圳数据源和130数据源配置类似...

    @Bean(name = "chsJdbcTemplate")
    public JdbcTemplate chsJdbcTemplate(@Qualifier("chsDataSource") DataSource dataSource) {
        return new JdbcTemplate(dataSource);
    }

    // 深圳数据源和130数据源的JdbcTemplate配置类似...
}
```

### 4.2 定时任务配置

系统使用Spring Boot的`@Scheduled`注解实现定时任务，配置了两个场景的定时执行：

- 场景1：每天00:05执行，检查前一天的金机投放情况
- 场景2：每小时15分执行，检查上一小时的金机投放情况

**关键代码**：
```java
@Configuration
@EnableScheduling
public class ScheduledConfig {
    @Autowired
    private AlarmService alarmService;

    // 场景1：每天00:05执行
    @Scheduled(cron = "0 5 0 * * ?")
    public void checkDailyGoldenSample() {
        alarmService.checkDailyGoldenSample();
    }

    // 场景2：每小时15分执行
    @Scheduled(cron = "0 15 * * * ?")
    public void checkHourlyGoldenSample() {
        alarmService.checkHourlyGoldenSample();
    }
}
```

### 4.3 业务逻辑实现

**场景1实现**：
```java
@Override
public void checkDailyGoldenSample() {
    log.info("开始执行场景1：每天金机投放情况检查");

    // 长沙数据源SQL
    String chsSql = "select 'HNZ' pc_number,temp.gLineNo location, ' ' responsible_person, CONCAT('异常信息描述：',temp.gLineNo,' ',temp.gModel,' ',CURDATE() - INTERVAL 1 DAY,'当天应投良品金机',temp.gNum,'次，不良品金机',temp.gNum, '次，实际投放良品',temp.gPassTotal,'次，不良品',(temp.gFailTotal_am + temp.gFailTotal_pm + temp.gFailTotal_night),'次，未达标' ) alarm_message, '金机投放异常推送' alarm_level " +
            "from (select mgl.*,(select 2 * ports from mes_lineinfo where  mgl.gLineNo = lineName) AS gNum " +
            "from mes_gs_linerecord mgl where gTestDate = CURDATE() - INTERVAL 1 DAY and (remarks is null or remarks = '无金机') AND mgl.gModel REGEXP '^CD(W|B)') as temp " +
            "where temp.gPassTotal < temp.gNum or (temp.gFailTotal_am + temp.gFailTotal_pm + temp.gFailTotal_night) < temp.gNum";

    // 深圳数据源SQL
    String szSql = "select 'ZLT' pc_number,temp.gLineNo location, ' ' responsible_person, CONCAT('异常信息描述：',temp.gLineNo,' ',temp.gModel,' ',CURDATE() - INTERVAL 1 DAY,'当天应投良品金机',temp.gNum,'次，不良品金机',temp.gNum, '次，实际投放良品',temp.gPassTotal,'次，不良品',(temp.gFailTotal_am + temp.gFailTotal_pm + temp.gFailTotal_night),'次，未达标' ) alarm_message, '金机投放异常推送' alarm_level " +
            "from (select mgl.*,(select 2 * ports from mes_lineinfo where  mgl.gLineNo = lineName) AS gNum " +
            "from mes_gs_linerecord mgl where gTestDate = CURDATE() - INTERVAL 1 DAY and (remarks is null or remarks = '无金机') AND mgl.gModel REGEXP '^CD(W|B)') as temp " +
            "where temp.gPassTotal < temp.gNum or (temp.gFailTotal_am + temp.gFailTotal_pm + temp.gFailTotal_night) < temp.gNum";

    // 执行长沙数据源查询并插入报警信息
    executeAndInsertAlarm(chsSql, chsJdbcTemplate);

    // 执行深圳数据源查询并插入报警信息
    executeAndInsertAlarm(szSql, szJdbcTemplate);

    log.info("场景1：每天金机投放情况检查完成");
}
```

**场景2实现**：
```java
@Override
public void checkHourlyGoldenSample() {
    log.info("开始执行场景2：每小时金机投放情况检查");

    // 获取当前时间
    LocalDateTime now = LocalDateTime.now();
    // 计算上一小时的开始时间（xx:00:00）
    LocalDateTime lastHourStart = now.minusHours(1).withMinute(0).withSecond(0).withNano(0);
    // 计算上一小时的结束时间（xx:59:59）
    LocalDateTime lastHourEnd = now.minusHours(1).withMinute(59).withSecond(59).withNano(999999999);

    // 调用带时间区间参数的方法
    checkHourlyGoldenSampleByTimeRange(lastHourStart, lastHourEnd);

    log.info("场景2：每小时金机投放情况检查完成");
}
```

### 4.4 数据插入实现

```java
private void insertAlarmInfo(List<Map<String, Object>> results) {
    if (results == null || results.isEmpty()) {
        log.info("没有查询到异常数据，无需插入报警信息");
        return;
    }

    log.info("查询到 {} 条异常数据，开始插入报警信息表", results.size());

    // 插入SQL - 添加所有NOT NULL字段，并提供默认值
    String insertSql = "INSERT INTO alarm_info (pc_number, location, responsible_person, alarm_message, alarm_level, " +
            "mac_address, alarm_type, status, created_at, updated_at) " +
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, NOW(), NOW())";

    // 批量插入
    for (Map<String, Object> result : results) {
        String pcNumber = (String) result.get("pc_number");
        String location = (String) result.get("location");
        // 处理场景1没有responsible_person的情况
        String responsiblePerson = (String) result.getOrDefault("responsible_person", "");
        String alarmMessage = (String) result.get("alarm_message");
        String alarmLevel = (String) result.get("alarm_level");
        // 为NOT NULL字段提供默认值
        String macAddress = "";
        String alarmType = null;
        String status = "NG";

        // 执行插入
        alarmJdbcTemplate.update(insertSql, pcNumber, location, responsiblePerson, alarmMessage, alarmLevel, 
                macAddress, alarmType, status);
    }

    log.info("报警信息插入完成");
}
```

## 5. API接口实现

```java
@RestController
@RequestMapping("/api/alarm")
public class AlarmController {
    @Autowired
    private AlarmService alarmService;

    // 场景1：每天金机投放情况检查
    @PostMapping("/daily-check")
    public String dailyCheck() {
        alarmService.checkDailyGoldenSample();
        return "场景1执行成功";
    }

    // 场景2：每小时金机投放情况检查
    @PostMapping("/hourly-check")
    public String hourlyCheck() {
        alarmService.checkHourlyGoldenSample();
        return "场景2执行成功";
    }

    // 执行所有场景检查
    @PostMapping("/all-check")
    public String allCheck() {
        alarmService.checkDailyGoldenSample();
        alarmService.checkHourlyGoldenSample();
        return "所有场景执行成功";
    }
}
```

## 6. 配置说明

### 6.1 数据源配置

```yaml
spring:
  datasource:
    # 长沙数据源
    chs:
      driver-class-name: com.mysql.cj.jdbc.Driver
      url: jdbc:mysql://localhost:3306/chs_db?useUnicode=true&characterEncoding=utf-8&useSSL=false&serverTimezone=Asia/Shanghai
      username: root
      password: password

    # 深圳数据源
    sz:
      driver-class-name: com.mysql.cj.jdbc.Driver
      url: jdbc:mysql://localhost:3306/sz_db?useUnicode=true&characterEncoding=utf-8&useSSL=false&serverTimezone=Asia/Shanghai
      username: root
      password: password

    # 130数据源
    alarm:
      driver-class-name: com.mysql.cj.jdbc.Driver
      url: jdbc:mysql://localhost:3306/alarm_db?useUnicode=true&characterEncoding=utf-8&useSSL=false&serverTimezone=Asia/Shanghai
      username: root
      password: password
```

### 6.2 日志配置

系统使用Logback作为日志框架，配置文件为`logback-spring.xml`，主要配置包括：

- 控制台输出：彩色日志，包含时间、线程、日志级别、类名和日志消息
- 文件输出：将日志输出到项目根路径下的logs文件夹
- 日志轮转：按日期轮转，文件命名格式为：golden-sample-alarm.%d{yyyy-MM-dd}.log
- 日志保留：最长保留时间为30天，总大小不超过1GB

## 7. 部署和运行

### 7.1 环境要求
- JDK 1.8+
- MySQL 5.7+
- Maven 3.8.1+

### 7.2 部署步骤

1. 克隆项目代码
2. 配置数据库连接信息（application.yml）
3. 编译项目：`mvn clean compile`
4. 打包项目：`mvn package`
5. 运行项目：`java -jar target/golden-sample-alarm-1.0.0.jar`

### 7.3 开发环境运行

- 直接运行：`mvn spring-boot:run`
- 使用IDE运行：直接运行GoldenSampleAlarmApplication.java

## 8. 监控和维护

### 8.1 日志监控

系统生成的日志文件位于项目根路径下的logs文件夹中，日志文件包含详细的运行信息、错误信息和警告信息，便于问题排查和系统监控。

### 8.2 常见问题处理

| 问题 | 可能原因 | 解决方案 |
| --- | --- | --- |
| 定时任务不执行 | 1. 定时任务配置错误<br>2. 系统时间不正确<br>3. 应用未正确启动 | 1. 检查cron表达式是否正确<br>2. 检查系统时间<br>3. 检查应用启动日志 |
| 数据查询失败 | 1. 数据源连接信息错误<br>2. SQL语句错误<br>3. 数据库表结构变化 | 1. 检查数据源配置<br>2. 检查SQL语句<br>3. 检查数据库表结构 |
| 数据插入失败 | 1. 130数据源连接信息错误<br>2. alarm_info表结构变化<br>3. 插入数据不符合约束 | 1. 检查130数据源配置<br>2. 检查alarm_info表结构<br>3. 检查插入数据格式 |

## 9. 性能优化

### 9.1 SQL优化
- 使用索引优化查询性能
- 避免在SQL语句中使用复杂的函数和子查询
- 合理设计查询条件，减少数据扫描量

### 9.2 批量处理
- 使用批量插入代替单条插入，提高数据插入效率
- 合理设置批量处理大小，平衡内存使用和插入效率

### 9.3 异步处理
- 考虑使用异步处理方式执行耗时的操作，提高系统响应速度
- 使用线程池管理异步任务，避免资源耗尽

## 10. 未来扩展

### 10.1 功能扩展
- 添加更多的检查场景和规则
- 支持自定义检查规则
- 添加报警通知功能（邮件、短信等）

### 10.2 性能扩展
- 考虑使用缓存技术优化查询性能
- 支持分布式部署，提高系统吞吐量

### 10.3 监控扩展
- 添加系统监控和告警功能
- 提供可视化的监控界面

## 11. 总结

金机投放异常报警系统实现了对长沙和深圳两个数据源的金机投放数据进行定时检查，并将异常数据插入到130数据源的alarm_info表中。系统使用Spring Boot框架开发，支持定时任务和手动触发两种检查方式，提供了详细的日志记录和API接口。系统具有良好的可维护性、可靠性和扩展性，可以满足金机投放异常监控的需求。

---

**文档版本**：1.0
**编制日期**：2025-12-20
**编制人**：zengjia