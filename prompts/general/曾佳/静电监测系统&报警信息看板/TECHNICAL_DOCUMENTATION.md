# 静电监测系统和报警信息看板技术文档

## 1. 系统架构

### 1.1 整体架构

静电监测系统和报警信息看板采用前后端分离的架构设计，主要包含以下组件：

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  前端应用层     │     │  后端服务层     │     │  数据存储层     │
│                 │     │                 │     │                 │
│  - em-frontend  │────▶│  - Spring Boot  │────▶│  - MySQL        │
│    (静电监测)   │     │    应用        │     │                 │
│                 │     │                 │     │                 │
│  - alarm-frontend│────▶│                 │     │                 │
│    (报警看板)   │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### 1.2 分层架构

#### 1.2.1 前端架构

```
┌─────────────────┐
│  视图层         │
│  (Vue Components)│
└─────────┬───────┘
          │
┌─────────▼───────┐
│  逻辑层         │
│  (Composition API)│
└─────────┬───────┘
          │
┌─────────▼───────┐
│  服务层         │
│  (API 调用)     │
└─────────┬───────┘
          │
┌─────────▼───────┐
│  数据层         │
│  (响应式状态)   │
└─────────────────┘
```

#### 1.2.2 后端架构

```
┌─────────────────┐
│  控制器层       │
│  (Controller)   │
└─────────┬───────┘
          │
┌─────────▼───────┐
│  服务层         │
│  (Service)      │
└─────────┬───────┘
          │
┌─────────▼───────┐
│  数据访问层     │
│  (Mapper)       │
└─────────┬───────┘
          │
┌─────────▼───────┐
│  实体层         │
│  (Entity)       │
└─────────┬───────┘
          │
┌─────────▼───────┐
│  数据库         │
│  (MySQL)        │
└─────────────────┘
```

## 2. 系统模块划分

### 2.1 后端模块

| 模块名称 | 主要功能 | 核心类/接口 |
|---------|---------|-------------|
| 设备管理模块 | 设备信息查询、设备状态管理 | ElestaticInfoController、ElestaticInfoService |
| 超标记录模块 | 超标记录查询、超标检查 | ElestaticLimitController、ElestaticLimitService |
| 报警管理模块 | 报警信息查询、报警生成、报警处理 | AlarmController、AlarmInfoService、AlarmGenerateService |
| 报警规则模块 | 报警规则管理、规则应用 | AlarmRuleService |
| 定时任务模块 | 定时检查超标情况、生成报警信息 | AlarmGenerateTask、ElestaticLimitTask |
| 数据传输模块 | 数据DTO、VO转换 | ElestaticInfoQueryDTO、ElestaticInfoVO |
| 配置模块 | 系统配置、跨域配置 | CorsConfig、MyBatisPlusConfig |
| 异常处理模块 | 统一异常处理 | GlobalExceptionHandler |

### 2.2 前端模块

#### 2.2.1 静电监测系统（em-frontend）

| 模块名称 | 主要功能 | 核心文件 |
|---------|---------|---------|
| 设备监控模块 | 设备列表展示、状态监控 | ElestaticMonitor.vue、elestatic-monitor.ts |
| 数据查询模块 | 多条件筛选、综合搜索 | elestatic-monitor.ts |
| 超标记录模块 | 超标次数展示、详情查看 | elestatic-monitor.ts |
| 报警信息模块 | 报警信息查看、规则管理 | elestatic-monitor.ts |
| API调用模块 | 后端API请求封装 | request.ts、elestaticMonitor.ts |
| 工具函数模块 | 日期格式化、状态格式化 | format.ts |

#### 2.2.2 报警信息看板（alarm-frontend）

| 模块名称 | 主要功能 | 核心文件 |
|---------|---------|---------|
| 报警列表模块 | 报警信息展示、筛选、排序 | alarm-board.vue |
| 报警编辑模块 | 报警信息编辑、状态更新 | alarm-board.vue |
| 报警详情模块 | 报警详情查看 | alarm-board.vue |
| API调用模块 | 后端API请求封装 | request.ts、alarm.ts |
| 类型定义模块 | TypeScript类型定义 | alarm.ts |

## 3. 核心功能实现

### 3.1 设备监控功能

#### 3.1.1 设备列表查询

**后端实现**：
- 控制器：`ElestaticInfoController.getElestaticInfo`
- 服务层：`ElestaticInfoServiceImpl.pageQuery`
- 实现逻辑：
  1. 接收查询参数（车间、线别、设备状态、关键词、时间范围等）
  2. 构建查询条件
  3. 使用MyBatis-Plus进行分页查询
  4. 将查询结果转换为VO对象返回

**前端实现**：
- 组件：`ElestaticMonitor.vue`
- 逻辑层：`useElestaticMonitor`
- 实现逻辑：
  1. 初始化查询参数
  2. 调用API获取设备列表
  3. 处理分页、排序、筛选逻辑
  4. 渲染设备列表表格

#### 3.1.2 设备状态展示

**实现逻辑**：
- 设备状态分为正常、超标、异常等类型
- 后端通过`formatMonitorStatus`方法将状态码转换为状态描述和颜色
- 前端使用不同颜色的标签展示设备状态
- 状态数据实时更新，默认按超标次数降序排序

### 3.2 超标记录功能

#### 3.2.1 超标检查

**后端实现**：
- 服务层：`ElestaticLimitServiceImpl.checkElestaticLimit`
- 实现逻辑：
  1. 获取所有设备最新数据
  2. 遍历设备数据，检查一路和二路阻值是否超标
  3. 将原始值乘以0.01转换为实际阻值
  4. 与最大/最小阻值比对，判断是否超标
  5. 记录超标信息到数据库

**定时任务**：
- 定时任务：`ElestaticLimitTask.checkElestaticLimitTask`
- 执行频率：每5分钟执行一次
- 功能：定时检查所有设备的超标情况

#### 3.2.2 超标详情查看

**前端实现**：
- 组件：`ElestaticMonitor.vue`
- 逻辑层：`openLimitDialog`函数
- 实现逻辑：
  1. 点击设备的超标次数或问题条
  2. 调用API获取该设备的超标记录
  3. 打开超标详情弹窗
  4. 展示超标记录列表，支持排序和分页

### 3.3 报警管理功能

#### 3.3.1 报警信息生成

**后端实现**：
- 服务层：`AlarmGenerateService.generateAlarmInfo`
- 实现逻辑：
  1. 检查超时和重大异常情况
  2. 生成相应的报警信息
  3. 保存到数据库
  4. 标记为未处理状态

**定时任务**：
- 定时任务：`AlarmGenerateTask.generateAlarmInfoTask`
- 执行频率：每小时执行一次
- 功能：定时生成超时和重大异常报警信息

#### 3.3.2 报警信息查询

**后端实现**：
- 控制器：`AlarmController.getAlarmList`
- 服务层：`AlarmInfoServiceImpl.getAlarmList`
- 实现逻辑：
  1. 接收查询参数（报警类型、处理状态、时间范围、关键词等）
  2. 构建查询条件
  3. 使用MyBatis-Plus进行分页查询
  4. 返回查询结果

**前端实现**：
- 组件：`alarm-board.vue`
- 逻辑层：`fetchAlarmList`函数
- 实现逻辑：
  1. 初始化查询参数和默认时间范围
  2. 调用API获取报警列表
  3. 按报警类型分类展示
  4. 支持筛选、排序、分页

#### 3.3.3 报警处理

**前端实现**：
- 组件：`alarm-board.vue`
- 逻辑层：`handleMarkAsHandled`函数
- 实现逻辑：
  1. 点击"标记已处理"按钮
  2. 调用API更新报警状态
  3. 刷新报警列表

### 3.4 报警规则管理功能

#### 3.4.1 规则制定与修改

**前端实现**：
- 组件：`ElestaticMonitor.vue`
- 逻辑层：`applyAlertRules`函数
- 实现逻辑：
  1. 打开报警规则制定区域
  2. 设置小时超标次数或超标持续时间阈值
  3. 点击"应用规则"按钮
  4. 调用API保存规则
  5. 刷新规则列表

**权限控制**：
- 修改规则需要密码验证
- 密码错误次数限制：最多5次
- 验证通过后才能修改规则

## 4. API接口设计

### 4.1 设备管理接口

| 接口路径 | 请求方法 | 功能描述 | 请求参数 | 响应数据 |
|---------|---------|---------|---------|---------|
| `/api/elestatic-info` | GET | 获取设备列表 | `ElestaticInfoQueryDTO` | `PageResult<ElestaticInfoVO>` |
| `/api/elestatic-info/{id}` | GET | 获取设备详情 | `id: Long` | `ElestaticInfoVO` |

### 4.2 超标记录接口

| 接口路径 | 请求方法 | 功能描述 | 请求参数 | 响应数据 |
|---------|---------|---------|---------|---------|
| `/api/elestatic-limit/list` | GET | 获取超标记录列表 | `ElestaticLimitQueryDTO` | `PageResult<ElestaticLimitVO>` |
| `/api/elestatic-limit/check` | GET | 手动检查超标情况 | 无 | `Result<Void>` |
| `/api/elestatic-limit/alarm-count` | GET | 查询设备超标次数 | `eleId: Long, channelType: Integer` | `Result<Integer>` |

### 4.3 报警管理接口

| 接口路径 | 请求方法 | 功能描述 | 请求参数 | 响应数据 |
|---------|---------|---------|---------|---------|
| `/api/alarm/info/list` | GET | 获取报警列表 | `AlarmFilterParams` | `PageResult<AlarmInfo>` |
| `/api/alarm/info/{id}` | GET | 获取报警详情 | `id: Long` | `AlarmInfo` |
| `/api/alarm/info/update` | PUT | 更新报警信息 | `AlarmInfo` | `Result<Void>` |
| `/api/alarm/info/mark-handled` | PUT | 标记报警为已处理 | `id: Long` | `Result<Void>` |
| `/api/alarm/info/count-by-device` | GET | 按设备统计报警数量 | `startTime: LocalDateTime, endTime: LocalDateTime` | `Result<Map<String, Integer>>` |

### 4.4 报警规则接口

| 接口路径 | 请求方法 | 功能描述 | 请求参数 | 响应数据 |
|---------|---------|---------|---------|---------|
| `/api/alarm/rule/list` | GET | 获取报警规则列表 | 无 | `Result<List<AlarmRule>>` |
| `/api/alarm/rule/save` | POST | 保存报警规则 | `AlarmRule` | `Result<Void>` |
| `/api/alarm/rule/update` | PUT | 更新报警规则 | `AlarmRule` | `Result<Void>` |
| `/api/alarm/rule/{id}` | GET | 获取报警规则详情 | `id: Long` | `AlarmRule` |

### 4.5 报警类型接口

| 接口路径 | 请求方法 | 功能描述 | 请求参数 | 响应数据 |
|---------|---------|---------|---------|---------|
| `/api/alarm/level/all` | GET | 获取所有报警类型 | 无 | `Result<List<String>>` |

## 5. 数据库设计

### 5.1 核心表结构

#### 5.1.1 设备信息表（elestatic_info）

| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|-----|------|
| id | bigint | PRIMARY KEY, AUTO_INCREMENT | 设备ID |
| floor_no | varchar(50) | NOT NULL | 车间 |
| user | varchar(50) | | 责任人 |
| ele_no | varchar(50) | NOT NULL | 设备编码 |
| line_no_one | varchar(50) | | 一路线别 |
| name_one | varchar(50) | | 一路设备名称 |
| status_now_one | varchar(20) | | 一路状态 |
| ele_value_one | decimal(10,2) | | 一路阻值 |
| alarm_count_one | int | DEFAULT 0 | 一路超标次数 |
| line_no_two | varchar(50) | | 二路线别 |
| name_two | varchar(50) | | 二路设备名称 |
| status_now_two | varchar(20) | | 二路状态 |
| ele_value_two | decimal(10,2) | | 二路阻值 |
| alarm_count_two | int | DEFAULT 0 | 二路超标次数 |
| uptime | datetime | | 更新时间 |
| up_info_time | datetime | | 上传信息时间 |
| factory_no | int | | 工厂编号 |

#### 5.1.2 超标记录表（elestatic_limit）

| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|-----|------|
| id | bigint | PRIMARY KEY, AUTO_INCREMENT | 记录ID |
| ele_id | bigint | NOT NULL | 设备ID |
| one_start_time | datetime | | 一路超标开始时间 |
| one_end_time | datetime | | 一路超标结束时间 |
| one_duration | int | | 一路超标持续时间(秒) |
| one_max_value | decimal(10,2) | | 一路最大阻值 |
| two_start_time | datetime | | 二路超标开始时间 |
| two_end_time | datetime | | 二路超标结束时间 |
| two_duration | int | | 二路超标持续时间(秒) |
| two_max_value | decimal(10,2) | | 二路最大阻值 |
| factory_no | int | | 工厂编号 |

#### 5.1.3 报警信息表（alarm_info）

| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|-----|------|
| id | bigint | PRIMARY KEY, AUTO_INCREMENT | 报警ID |
| pc_number | varchar(50) | | PC编号 |
| mac_address | varchar(50) | | MAC地址 |
| location | varchar(100) | | 位置 |
| responsible_person | varchar(50) | | 责任人 |
| alarm_message | varchar(255) | | 报警信息 |
| alarm_level | varchar(50) | | 报警类型 |
| alarm_type | varchar(50) | | 报警类型（细分） |
| hour_interval | varchar(20) | | 小时间隔 |
| status | varchar(20) | DEFAULT 'NG' | 处理状态 |
| created_at | datetime | NOT NULL | 创建时间 |
| updated_at | datetime | | 更新时间 |
| resolved_at | datetime | | 解决时间 |
| improvement_direction | varchar(255) | | 改善方向 |
| improver | varchar(50) | | 改善人 |
| improvement_time | datetime | | 改善时间 |
| confirmer | varchar(50) | | 确认人 |
| confirmation_time | datetime | | 确认时间 |
| push_status | varchar(20) | | 推送状态 |
| model | varchar(50) | | 机型 |

#### 5.1.4 报警规则表（alarm_rule）

| 字段名 | 数据类型 | 约束 | 描述 |
|-------|---------|-----|------|
| id | bigint | PRIMARY KEY, AUTO_INCREMENT | 规则ID |
| rule_code | varchar(50) | NOT NULL | 规则编码 |
| rule_content | varchar(255) | NOT NULL | 规则内容 |
| create_time | datetime | NOT NULL | 制定时间 |
| hour_restart_threshold | int | | 小时超标次数阈值 |
| day_restart_threshold | int | | 超标持续时间阈值(秒) |

### 5.2 表关系

```
elestatic_info (设备信息表)
    │
    └─┬─ elestatic_limit (超标记录表)  (1:N)
      │
      └─ alarm_info (报警信息表)  (1:N)

alarm_rule (报警规则表)  (1:1)
```

## 6. 技术栈与依赖

### 6.1 后端技术栈

| 技术/依赖 | 版本 | 用途 |
|---------|-----|------|
| Spring Boot | 2.7.18 | 后端框架 |
| Java | 8 | 开发语言 |
| MyBatis-Plus | 3.5.3.1 | ORM框架 |
| MySQL | 8.0 | 数据库 |
| Lombok | 1.18.30 | 简化代码 |
| Slf4j | 1.7.36 | 日志框架 |
| Logback | 1.4.11 | 日志实现 |
| Spring Boot Starter Web | 2.7.18 | Web支持 |
| Spring Boot Starter Test | 2.7.18 | 测试支持 |

### 6.2 前端技术栈

| 技术/依赖 | 版本 | 用途 |
|---------|-----|------|
| Vue | 3.4.15 | 前端框架 |
| TypeScript | 5.2.2 | 类型系统 |
| Vite | 5.0.8 | 构建工具 |
| Element Plus | 2.5.1 | UI组件库 |
| Axios | 1.6.3 | HTTP客户端 |
| @element-plus/icons-vue | 2.3.1 | 图标库 |

## 7. 开发与部署

### 7.1 开发环境

| 环境 | 版本 | 用途 |
|-----|-----|------|
| JDK | 8 | Java开发 |
| Node.js | 16.x | 前端开发 |
| MySQL | 8.0 | 数据库 |
| IntelliJ IDEA | 2023.2 | 后端开发IDE |
| VS Code | 1.85.1 | 前端开发IDE |
| Maven | 3.9.6 | Java项目构建 |
| npm | 8.19.4 | Node.js包管理 |

### 7.2 构建与运行

#### 7.2.1 后端服务

**构建命令**：
```bash
cd em-backend
mvn clean package -DskipTests
```

**运行命令**：
```bash
java -jar target/em-backend-1.0.0.jar
```

**开发环境运行**：
```bash
mvn spring-boot:run
```

#### 7.2.2 前端应用

**安装依赖**：
```bash
cd em-frontend
npm install
```

**开发环境运行**：
```bash
npm run dev
```

**构建生产版本**：
```bash
npm run build
```

### 7.3 部署配置

#### 7.3.1 后端配置

配置文件：`em-backend/src/main/resources/application.properties`

主要配置项：
```properties
# 服务器配置
server.port=8088

# 数据库配置
spring.datasource.url=jdbc:mysql://localhost:3306/cdtech?useUnicode=true&characterEncoding=utf8&useSSL=false&serverTimezone=Asia/Shanghai
spring.datasource.username=root
spring.datasource.password=123456

# MyBatis配置
mybatis-plus.mapper-locations=classpath*:/mapper/**/*.xml
mybatis-plus.type-aliases-package=com.cdtech.entity

# 日志配置
logging.level.com.cdtech=info
```

#### 7.3.2 前端配置

**开发环境配置**：`.env.development`
```properties
VITE_APP_BASE_API=/api
```

**生产环境配置**：`.env.production`
```properties
VITE_APP_BASE_API=/api
```

**Vite配置**：`vite.config.ts`
```typescript
export default defineConfig({
  server: {
    port: 5175,
    proxy: {
      '/api': {
        target: 'http://localhost:8088',
        changeOrigin: true
      }
    }
  }
})
```

## 8. 系统监控与维护

### 8.1 日志管理

**日志框架**：Logback

**日志级别**：INFO

**日志文件**：`logs/em-backend.log`

**日志内容**：
- API请求日志
- 数据库操作日志
- 业务逻辑日志
- 异常日志

### 8.2 常见问题排查

#### 8.2.1 API请求400错误

**可能原因**：
- 请求参数格式错误
- 缺少必填参数
- 日期时间格式不匹配

**解决方案**：
- 检查请求参数是否符合API文档要求
- 确保所有必填参数都已提供
- 日期时间格式使用：`yyyy-MM-dd HH:mm:ss`

#### 8.2.2 数据库连接失败

**可能原因**：
- 数据库服务未启动
- 数据库连接配置错误
- 数据库账号密码错误

**解决方案**：
- 检查MySQL服务是否正常运行
- 验证数据库连接配置是否正确
- 确认数据库账号密码是否正确

#### 8.2.3 前端页面空白

**可能原因**：
- 前端服务未启动
- API请求失败
- 前端代码错误

**解决方案**：
- 检查前端服务是否正常运行
- 查看浏览器控制台是否有错误信息
- 检查API请求是否能正常响应

## 9. 性能优化

### 9.1 后端优化

1. **数据库索引优化**：
   - 为频繁查询的字段添加索引
   - 优化查询语句，减少全表扫描
   - 使用合理的索引类型（B-Tree、Hash等）

2. **缓存优化**：
   - 对频繁访问的数据进行缓存
   - 使用Redis缓存热点数据
   - 实现缓存失效机制

3. **并发优化**：
   - 使用线程池处理并发请求
   - 优化数据库连接池配置
   - 减少锁竞争

### 9.2 前端优化

1. **组件优化**：
   - 使用Vue 3的Composition API，减少组件耦合
   - 合理使用`v-if`和`v-show`
   - 实现组件的懒加载

2. **API请求优化**：
   - 减少不必要的API请求
   - 实现请求防抖和节流
   - 使用分页加载大数据量

3. **渲染优化**：
   - 使用虚拟列表处理长列表
   - 优化CSS选择器
   - 减少DOM操作

## 10. 安全设计

### 10.1 前端安全

1. **输入验证**：
   - 对用户输入进行严格验证
   - 防止XSS攻击
   - 防止CSRF攻击

2. **权限控制**：
   - 敏感操作需要密码验证
   - 密码输入错误次数限制
   - 验证通过后才允许操作

### 10.2 后端安全

1. **接口安全**：
   - 实现接口访问控制
   - 防止SQL注入
   - 防止恶意请求

2. **数据安全**：
   - 敏感数据加密存储
   - 数据传输使用HTTPS
   - 实现数据备份机制

3. **日志安全**：
   - 防止日志泄露敏感信息
   - 实现日志审计
   - 定期清理日志文件

## 11. 未来扩展

### 11.1 功能扩展

1. **实时数据推送**：
   - 集成WebSocket实现实时数据推送
   - 实时显示设备状态变化
   - 实时推送报警信息

2. **数据分析与可视化**：
   - 添加数据统计图表
   - 实现趋势分析功能
   - 生成报表功能

3. **移动端支持**：
   - 开发移动端应用
   - 实现响应式设计
   - 支持移动端推送

4. **告警通知扩展**：
   - 支持邮件告警
   - 支持短信告警
   - 支持企业微信/钉钉告警

### 11.2 技术扩展

1. **微服务架构**：
   - 将系统拆分为多个微服务
   - 实现服务注册与发现
   - 实现服务容错机制

2. **容器化部署**：
   - 使用Docker容器化部署
   - 使用Kubernetes进行容器编排
   - 实现自动化部署

3. **云原生支持**：
   - 支持云平台部署
   - 实现弹性伸缩
   - 支持云存储和云数据库

## 12. 附录

### 12.1 代码规范

#### 12.1.1 Java代码规范

- 遵循阿里巴巴Java开发手册
- 类名使用驼峰命名法，首字母大写
- 方法名、变量名使用驼峰命名法，首字母小写
- 常量名使用全大写，下划线分隔
- 每行代码不超过120个字符
- 方法注释使用Javadoc格式

#### 12.1.2 TypeScript代码规范

- 遵循Vue 3官方风格指南
- 使用TypeScript严格模式
- 组件名使用PascalCase
- 变量名、方法名使用camelCase
- 接口名使用PascalCase，以I开头
- 每行代码不超过120个字符
- 组件注释使用JSDoc格式

### 12.2 常用命令

**查看端口占用**：
```bash
netstat -ano | findstr 8088
```

**终止进程**：
```bash
taskkill /F /PID <PID>
```

**查看Java进程**：
```bash
jps -l
```

**查看日志**：
```bash
tail -f logs/em-backend.log
```

### 12.3 相关文档

- [Spring Boot官方文档](https://spring.io/projects/spring-boot)
- [Vue 3官方文档](https://vuejs.org/)
- [Element Plus官方文档](https://element-plus.org/)
- [MyBatis-Plus官方文档](https://baomidou.com/)
- [MySQL官方文档](https://dev.mysql.com/doc/)

## 13. 版本历史

| 版本号 | 发布日期 | 主要变更 | 作者 |
|-------|---------|---------|------|
| V1.0.0 | 2025-12-22 | 初始版本，包含基本功能 | zengjia |
| V1.1.0 | 2025-12-30 | 优化性能，修复bug | zengjia |
| V1.2.0 | 2026-01-15 | 新增报警规则管理功能 | zengjia |
| V1.3.0 | 2026-01-30 | 优化界面设计，提升用户体验 | zengjia |
