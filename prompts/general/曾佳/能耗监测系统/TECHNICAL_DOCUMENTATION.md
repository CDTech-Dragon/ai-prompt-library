# TECHNICAL_DOCUMENTATION.md

## 1. 系统架构概述

### 1.1 架构设计
EMS能耗监测系统采用前后端分离的架构设计，前端和后端通过API进行通信。系统主要由以下几个部分组成：

- **前端应用**：基于Vue 3和Element Plus构建，负责用户界面展示和交互
- **后端服务**：基于Node.js和Express构建，负责API请求处理和数据整合
- **EMS API**：外部能源管理系统API，提供设备数据、能耗数据和报警信息
- **数据存储**：前端使用localStorage存储token等临时数据

### 1.2 系统架构图

```
+----------------+       +----------------+       +----------------+
|                |       |                |       |                |
|   前端应用      |       |   后端服务      |       |   EMS API       |
|  (Vue 3 +      |       |  (Node.js +     |       |  (外部系统)     |
|   Element Plus) |<----->|   Express)      |<----->|                |
|                |       |                |       |                |
+----------------+       +----------------+       +----------------+
        ^
        |
+----------------+
|                |
|  本地存储       |
| (localStorage)  |
|                |
+----------------+
```

### 1.3 技术栈

| 技术         | 版本    | 用途                     |
|------------|-------|------------------------|
| Vue        | 3.x   | 前端框架                  |
| Element Plus | 2.x   | UI组件库                 |
| Axios      | 1.x   | HTTP客户端               |
| Vite       | 7.x   | 构建工具                  |
| Node.js    | 18.x  | 后端运行环境                |
| Express    | 4.x   | Web框架                 |
| dotenv     | 17.x  | 环境变量管理                |
| winston    | 3.x   | 日志管理                  |

## 2. 前端技术实现

### 2.1 项目结构

```
frontend/
├── public/          # 静态资源
├── src/             # 源代码
│   ├── assets/      # 资源文件
│   │   └── css/     # 样式文件
│   ├── components/  # Vue组件
│   │   ├── AlarmInfo.vue         # 报警信息组件
│   │   ├── DeviceDetail.vue      # 设备详情组件
│   │   ├── DeviceList.vue        # 设备列表组件
│   │   └── EnergyQuery.vue       # 能耗查询组件
│   ├── services/    # 服务
│   │   └── api.js   # API调用服务
│   ├── App.vue      # 根组件
│   ├── main.js      # 入口文件
│   └── style.css    # 全局样式
├── .gitignore       # Git忽略文件
├── index.html       # HTML模板
├── package.json     # 依赖管理
└── vite.config.js   # Vite配置
```

### 2.2 核心组件设计

#### 2.2.1 App.vue
- **功能**：根组件，负责整体布局和组件切换
- **主要属性**：
  - `selectedDeviceId`：当前选中的设备ID
  - `showDeviceDetail`：是否显示设备详情
  - `showAlarmInfo`：是否显示报警信息
  - `dateRange`：日期范围
  - `timeType`：时间类型
- **主要方法**：
  - `handleViewDeviceDetail`：处理查看设备详情
  - `handleCloseDeviceDetail`：处理关闭设备详情
  - `handleViewAlarmInfo`：处理查看报警信息
  - `handleCloseAlarmInfo`：处理关闭报警信息
  - `setToday`/`setYesterday`/`setThisWeek`/`setThisMonth`：设置快捷日期范围

#### 2.2.2 DeviceList.vue
- **功能**：设备列表组件，显示所有设备的基本信息
- **主要属性**：
  - `deviceList`：设备列表数据
  - `internalLoading`：内部加载状态
  - `pagination`：分页信息
- **主要方法**：
  - `getDeviceList`：获取设备列表数据
  - `getTotalUsage`：获取总用电量
  - `handleViewDetail`：处理查看设备详情
  - `handlePageChange`：处理分页变化
  - `handleSizeChange`：处理每页条数变化

#### 2.2.3 DeviceDetail.vue
- **功能**：设备详情组件，显示设备的详细信息和用电详情
- **主要属性**：
  - `deviceDetail`：设备详情数据
  - `energyDetail`：用电详情数据
  - `loading`：加载状态
  - `energyLoading`：能耗数据加载状态
- **主要方法**：
  - `getDeviceDetail`：获取设备详情数据
  - `getEnergyDetail`：获取用电详情数据
  - `handleClose`：处理关闭详情

#### 2.2.4 AlarmInfo.vue
- **功能**：报警信息组件，显示设备的报警信息
- **主要属性**：
  - `visible`：是否显示抽屉
  - `alarmData`：报警信息数据
  - `loading`：加载状态
- **主要方法**：
  - `getAlarmInfo`：获取报警信息
  - `handleClose`：处理关闭抽屉

### 2.3 API服务设计

#### 2.3.1 api.js
- **功能**：提供API调用服务，包括设备、能耗和报警相关API
- **主要功能**：
  - 创建axios实例
  - Token管理（获取、刷新、存储）
  - 请求拦截器（添加Token）
  - 响应拦截器（处理错误和Token过期）
  - API接口封装

## 3. 后端技术实现

### 3.1 项目结构

```
backend/
├── config/          # 配置文件
│   └── index.js     # API配置
├── routes/          # 路由
│   └── api.js       # API路由
├── services/        # 业务逻辑
│   └── emsApi.js    # EMS API调用服务
├── utils/           # 工具函数
│   └── logger.js    # 日志工具
├── .env             # 环境变量
├── app.js           # 应用入口
├── package-lock.json # 依赖锁文件
└── package.json     # 依赖管理
```

### 3.2 核心模块设计

#### 3.2.1 app.js
- **功能**：后端应用入口，负责服务器启动和中间件配置
- **主要配置**：
  - CORS配置
  - JSON请求体解析
  - URL编码请求体解析
  - API调用日志中间件
  - API路由配置
  - 健康检查路由

#### 3.2.2 emsApi.js
- **功能**：EMS API调用服务，负责与外部EMS系统API通信
- **主要功能**：
  - 创建axios实例
  - Token管理（获取、刷新、存储）
  - 请求拦截器（添加Token）
  - 响应拦截器（处理错误和Token过期）
  - API接口封装

#### 3.2.3 api.js (路由)
- **功能**：API路由配置，定义后端API接口
- **主要路由**：
  - `/api/devices`：获取设备列表
  - `/api/devices/:id`：获取设备详情
  - `/api/energy`：查询能耗数据
  - `/api/alarm`：查询报警信息

#### 3.2.4 logger.js
- **功能**：日志管理工具，负责记录API请求和响应日志
- **主要功能**：
  - 配置日志格式
  - 实现日志脱敏
  - 支持控制台和文件输出
  - 日志按日期轮转

### 3.3 环境变量配置

| 变量名                | 用途                     | 默认值                     |
|--------------------|------------------------|-------------------------|
| PORT               | 服务器端口                  | 3000                    |
| EMS_API_BASE_URL   | EMS API基础URL           | http://192.168.2.11:8090 |
| EMS_API_PROJECT_TYPE | EMS API项目类型         | 3                       |
| EMS_API_VERSION    | EMS API版本              | 2.0.0                   |
| EMS_API_USERNAME   | EMS API用户名             | admin                   |
| EMS_API_PASSWORD   | EMS API密码              | Acrel001                |

## 4. API设计

### 4.1 前端API调用

#### 4.1.1 设备相关API

| API名称     | 方法   | URL                             | 参数                     | 描述               |
|----------|------|---------------------------------|------------------------|------------------|
| getDevices | GET  | /SubstationWEBV2/sys/getMeterUseInfoList | fSubId, pageNo, pageSize | 获取设备列表         |
| getDeviceDetail | GET  | /SubstationWEBV2/sys/getMeterUseInfoList | search, fSubId        | 获取设备详情         |

#### 4.1.2 能耗相关API

| API名称     | 方法   | URL                             | 参数                     | 描述               |
|----------|------|---------------------------------|------------------------|------------------|
| getEnergyData | POST | /SubstationWEBV2/sys/ElectricityFeesNoHj | fSubid, startTime, endTime, fCircuitids, DA | 获取能耗数据         |
| getElectricityUsage | POST | /SubstationWEBV2/sys/ElectricityFeesNoHj | fSubid, startTime, endTime, fMetercode, DA | 获取用电量数据 |
| getTotalUsage | GET  | /SubstationWEBV2/main/getMeterParamValueByKey | fSubid, fMetercode, fParamcode | 获取总用电量 |

#### 4.1.3 报警相关API

| API名称     | 方法   | URL                             | 参数                     | 描述               |
|----------|------|---------------------------------|------------------------|------------------|
| getAlarmInfo | POST | /SubstationWEBV2/main/getAlarmEventLogList | fSubid, startTime, endTime | 获取报警信息         |

### 4.2 后端API接口

#### 4.2.1 设备相关API

| API路径          | 方法   | 功能描述          | EMS API调用                                                                                                                      |
|---------------|------|---------------|------------------------------------------------------------------------------------------------------------------------------|
| /api/devices  | GET  | 获取设备列表        | /SubstationWEBV2/sys/getMeterUseInfoList/SubstationWEBV2/sys/getCircuitInfoTree/SubstationWEBV2/main/getMeterParamValueByKey |
| /api/devices/:id | GET  | 获取设备详情        | /SubstationWEBV2/sys/getMeterUseInfoList/SubstationWEBV2/main/getMeterParamValueByKey                                        |

#### 4.2.2 能耗相关API

| API路径          | 方法   | 功能描述          | EMS API调用                                                                                                                      |
|---------------|------|---------------|------------------------------------------------------------------------------------------------------------------------------|
| /api/energy   | POST | 查询能耗数据        | /SubstationWEBV2/sys/ElectricityFeesNoHj                                                                                     |

#### 4.2.3 报警相关API

| API路径          | 方法   | 功能描述          | EMS API调用                                                                                                                      |
|---------------|------|---------------|------------------------------------------------------------------------------------------------------------------------------|
| /api/alarm    | POST | 查询报警信息        | /SubstationWEBV2/main/getAlarmEventLogList                                                                                   |

## 5. 数据流程

### 5.1 设备列表数据流程

```
1. 用户访问系统，前端加载设备列表组件
2. 前端调用deviceApi.getDevices()获取设备列表数据
3. 前端api.js检查Token是否存在或过期，若过期则自动刷新
4. 前端向EMS API发送GET请求，获取设备列表
5. EMS API返回设备列表数据
6. 前端接收数据，更新设备列表
7. 前端调用energyApi.getTotalUsage()获取设备总用电量
8. 前端向EMS API发送GET请求，获取总用电量数据
9. EMS API返回总用电量数据
10. 前端更新设备列表的用电量信息
11. 前端渲染设备列表
```

### 5.2 设备详情数据流程

```
1. 用户点击设备列表中的"详情"按钮
2. 前端切换到设备详情组件
3. 前端调用deviceApi.getDeviceDetail()获取设备详情数据
4. 前端api.js检查Token是否存在或过期，若过期则自动刷新
5. 前端向EMS API发送GET请求，获取设备详情
6. EMS API返回设备详情数据
7. 前端更新设备详情信息
8. 前端调用energyApi.getEnergyData()获取用电详情数据
9. 前端向EMS API发送POST请求，获取用电详情数据
10. EMS API返回用电详情数据
11. 前端更新用电详情信息
12. 前端渲染设备详情
```

### 5.3 Token刷新数据流程

```
1. 前端发起API请求
2. 前端api.js检查Token是否存在或过期
3. 若Token过期，前端调用getToken()获取新Token
4. 前端向EMS API发送POST请求，获取新Token
5. EMS API返回新Token
6. 前端存储新Token到localStorage
7. 前端将新Token添加到请求头
8. 前端重新发送API请求
9. EMS API处理请求，返回数据
10. 前端接收数据，完成请求
```

## 6. 部署方案

### 6.1 前端部署

1. **构建前端项目**：
   ```bash
   cd frontend
   npm install
   npm run build
   ```

2. **部署前端代码**：
   - 将`frontend/dist`目录下的文件部署到Web服务器（如Nginx、Apache等）
   - 配置Web服务器，指向`frontend/dist`目录

3. **配置Nginx示例**：
   ```nginx
   server {
       listen 80;
       server_name example.com;
       root /path/to/frontend/dist;
       index index.html;
       
       location / {
           try_files $uri $uri/ /index.html;
       }
   }
   ```

### 6.2 后端部署

1. **安装依赖**：
   ```bash
   cd backend
   npm install
   ```

2. **配置环境变量**：
   - 复制`.env.example`文件为`.env`
   - 修改`.env`文件中的配置项

3. **启动后端服务**：
   ```bash
   node app.js
   ```

4. **使用PM2管理进程**：
   ```bash
   npm install -g pm2
   pm2 start app.js --name ems-backend
   pm2 save
   pm2 startup
   ```

### 6.3 环境要求

- **操作系统**：Windows 10/11 64位或Linux
- **Node.js版本**：18.x或更高版本
- **内存**：至少2GB RAM
- **CPU**：至少2核CPU
- **磁盘空间**：至少1GB可用空间

## 7. 开发环境配置

### 7.1 前端开发环境

1. **安装Node.js**：
   - 下载并安装Node.js 18.x或更高版本
   - 验证安装：`node -v` 和 `npm -v`

2. **创建Vue项目**：
   ```bash
   npm create vite@latest frontend -- --template vue
   ```

3. **安装依赖**：
   ```bash
   cd frontend
   npm install
   npm install element-plus axios
   ```

4. **启动开发服务器**：
   ```bash
   npm run dev
   ```

### 7.2 后端开发环境

1. **安装Node.js**：
   - 下载并安装Node.js 18.x或更高版本
   - 验证安装：`node -v` 和 `npm -v`

2. **创建后端项目**：
   ```bash
   mkdir backend
   cd backend
   npm init -y
   ```

3. **安装依赖**：
   ```bash
   npm install express cors axios dotenv winston winston-daily-rotate-file
   ```

4. **创建项目文件**：
   - 创建`app.js`、`config/index.js`、`routes/api.js`、`services/emsApi.js`、`utils/logger.js`等文件
   - 创建`.env`文件，配置环境变量

5. **启动开发服务器**：
   ```bash
   node app.js
   ```

## 8. 代码规范

### 8.1 前端代码规范

- **Vue组件命名**：使用PascalCase命名，如`DeviceList.vue`
- **变量命名**：使用camelCase命名，如`deviceList`
- **函数命名**：使用camelCase命名，如`getDeviceList`
- **常量命名**：使用UPPER_CASE命名，如`API_BASE_URL`
- **代码缩进**：使用2个空格进行缩进
- **代码注释**：为所有函数添加函数级注释，包含功能描述、参数说明、返回值类型及用途
- **组件结构**：
  ```vue
  <script setup>
  // 导入和配置
  </script>
  
  <template>
  <!-- 组件模板 -->
  </template>
  
  <style scoped>
  /* 组件样式 */
  </style>
  ```

### 8.2 后端代码规范

- **文件命名**：使用kebab-case命名，如`ems-api.js`
- **变量命名**：使用camelCase命名，如`deviceList`
- **函数命名**：使用camelCase命名，如`getDeviceList`
- **常量命名**：使用UPPER_CASE命名，如`PORT`
- **代码缩进**：使用2个空格进行缩进
- **代码注释**：为所有函数添加函数级注释，包含功能描述、参数说明、返回值类型及用途
- **错误处理**：使用try-catch语句处理异步错误
- **日志记录**：使用winston记录所有API请求和响应日志

## 9. 测试方案

### 9.1 前端测试

#### 9.1.1 单元测试
- **测试框架**：Vitest
- **测试内容**：
  - 组件渲染测试
  - 组件属性测试
  - 组件方法测试
  - 组件事件测试

#### 9.1.2 集成测试
- **测试框架**：Cypress
- **测试内容**：
  - 页面导航测试
  - 表单提交测试
  - API调用测试
  - 组件交互测试

#### 9.1.3 测试命令
```bash
# 单元测试
npm run test:unit

# 集成测试
npm run test:e2e
```

### 9.2 后端测试

#### 9.2.1 单元测试
- **测试框架**：Mocha + Chai
- **测试内容**：
  - 路由测试
  - 中间件测试
  - 服务层测试
  - 工具函数测试

#### 9.2.2 集成测试
- **测试框架**：Supertest
- **测试内容**：
  - API请求测试
  - 数据验证测试
  - 错误处理测试
  - 认证授权测试

#### 9.2.3 测试命令
```bash
# 单元测试
npm run test:unit

# 集成测试
npm run test:integration
```

## 10. 维护与支持

### 10.1 日志管理

- **前端日志**：使用浏览器控制台输出日志，包含API请求和响应信息
- **后端日志**：使用winston记录日志，分为info和error两个级别
- **日志文件**：按日期轮转，存储在`backend/logs`目录下
- **日志格式**：JSON格式，包含时间戳、日志级别、请求ID、请求方法、URL、状态码、响应时间等信息

### 10.2 错误处理

- **前端错误处理**：
  - 使用try-catch语句处理异步错误
  - 在响应拦截器中处理API错误
  - 显示友好的错误提示给用户

- **后端错误处理**：
  - 使用try-catch语句处理异步错误
  - 统一的错误处理中间件
  - 返回标准化的错误响应格式

### 10.3 常见问题与解决方案

| 问题描述 | 可能原因 | 解决方案 |
|---------|---------|--------|
| 无法获取设备列表 | Token过期或无效 | 检查Token是否过期，重新获取Token |
| 设备详情显示为空 | 设备ID无效或设备不存在 | 检查设备ID是否正确，确认设备存在 |
| 能耗数据显示异常 | 查询参数错误 | 检查查询参数，特别是日期范围和设备编码 |
| 页面加载缓慢 | 网络问题或API响应慢 | 检查网络连接，优化API响应速度 |
| Token刷新失败 | 用户名或密码错误 | 检查.env文件中的用户名和密码配置 |

## 11. 附录

### 11.1 术语定义

| 术语 | 英文全称 | 中文解释 |
|-----|--------|--------|
| EMS | Energy Management System | 能源管理系统 |
| API | Application Programming Interface | 应用程序编程接口 |
| Vue 3 | Vue.js 3 | 一种渐进式JavaScript框架，用于构建用户界面 |
| Element Plus | - | 一套基于Vue 3的桌面端组件库 |
| Node.js | - | 一个基于Chrome V8引擎的JavaScript运行环境 |
| Express | - | 一个基于Node.js的Web应用框架 |
| Token | - | 用于身份验证的令牌 |
| CORS | Cross-Origin Resource Sharing | 跨域资源共享 |
| RESTful | Representational State Transfer | 表述性状态转移，一种软件架构风格 |

### 11.2 参考文档

- [Vue 3官方文档](https://v3.vuejs.org/)
- [Element Plus官方文档](https://element-plus.org/)
- [Axios官方文档](https://axios-http.com/)
- [Vite官方文档](https://vite.dev/)
- [Node.js官方文档](https://nodejs.org/)
- [Express官方文档](https://expressjs.com/)
- [Winston官方文档](https://winstonjs.com/)

### 11.3 联系方式

- **项目负责人**：zengjia
- **联系邮箱**：[联系邮箱]
- **联系电话**：[联系电话]
- **项目地址**：d:\MyTools\MyProject\trae_project\ems

## 12. 版本历史

| 版本 | 日期 | 变更内容 | 作者 |
|-----|-----|--------|-----|
| v1.0 | 2025-12-22 | 初始版本，包含设备管理、能耗查询、报警管理功能 | zengjia |
| v1.1 | YYYY-MM-DD | [后续版本变更内容] | [作者] |
| v1.2 | YYYY-MM-DD | [后续版本变更内容] | [作者] |
