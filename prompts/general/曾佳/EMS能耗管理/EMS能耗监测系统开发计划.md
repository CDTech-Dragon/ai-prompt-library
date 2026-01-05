6. - # EMS能耗监测系统开发计划
   
     ## 一、项目概述
   
     EMS能耗监测系统专注于设备信息展示、能耗查询和报警信息查看功能，采用Vue 3 + Element Plus前端和Node.js后端架构。
   
     ## 二、技术栈
   
     - **前端**：Vue 3 + Element Plus
     - **后端**：Node.js + Express
     - **HTTP客户端**：Axios
     - **构建工具**：Vite
   
     ## 三、项目结构
   
     ```
     ems-energy-monitoring/
     ├── backend/              # Node.js后端服务
     │   ├── config/          # 配置文件
     │   │   └── index.js     # API配置
     │   ├── routes/          # 路由
     │   │   └── api.js       # API路由
     │   ├── services/        # 业务逻辑
     │   │   └── emsApi.js    # EMS API调用服务
     │   ├── app.js           # 应用入口
     │   ├── package.json     # 依赖
     │   └── .env             # 环境变量
     └── frontend/            # Vue 3前端应用
         ├── public/          # 静态资源
         ├── src/             # 源代码
         │   ├── assets/      # 资源文件
         │   ├── components/  # Vue组件
         │   │   ├── DeviceList.vue       # 设备列表
         │   │   ├── DeviceDetail.vue     # 设备详情
         │   │   ├── EnergyQuery.vue       # 能耗查询
         │   │   └── AlarmInfo.vue         # 报警信息
         │   ├── services/    # 服务
         │   │   └── api.js   # API调用
         │   ├── App.vue      # 根组件
         │   ├── main.js      # 入口
         │   └── style.css    # 全局样式
         ├── package.json     # 依赖
         └── vite.config.js   # Vite配置
     ```
   
     ## 四、核心功能实现
   
     ### 1. 后端服务（Node.js + Express）
   
     #### 1.1 API配置
   
     - 在`.env`中配置EMS API基础URL
     - 实现Token自动获取和刷新机制
     - 配置CORS允许前端跨域访问
   
     #### 1.2 路由设计
   
     | 前端调用路径       | 方法 | 后端处理     | EMS API调用                                                  |
     | :----------------- | :--- | :----------- | :----------------------------------------------------------- |
     | `/api/devices`     | GET  | 获取设备列表 | `/SubstationWEBV2/sys/getMeterUseInfoList/SubstationWEBV2/sys/getCircuitInfoTree/SubstationWEBV2/main/getMeterParamValueByKey` |
     | `/api/devices/:id` | GET  | 获取设备详情 | `/SubstationWEBV2/sys/getMeterUseInfoList/SubstationWEBV2/main/getMeterParamValueByKey` |
     | `/api/energy`      | POST | 查询能耗数据 | `/SubstationWEBV2/sys/ElectricityFeesNoHj`                   |
     | `/api/alarm`       | POST | 查询报警信息 | `/SubstationWEBV2/main/getAlarmEventLogList`                 |
   
     #### 1.3 数据整合
   
     - 后端整合来自不同EMS API的数据
     - 返回统一格式给前端，减少前端数据处理
   
     ### 2. 前端应用（Vue 3 + Element Plus）
   
     #### 2.1 主页面（App.vue）
   
     - 简化布局，直接展示核心功能
     - 顶部显示系统名称：EMS能耗监测系统
     - 包含查询表单和查看报警信息按钮
     - 内容区动态切换设备列表、详情和报警信息
   
     #### 2.2 设备列表组件（DeviceList.vue）
   
     - **功能**：展示所有设备基本信息
     - **展示字段**：序号、仪表编码、回路名称、仪表位置、连接状态、回路状态、用电量、问题条数、是否落实、更新时间
     - **交互**：点击详情按钮跳转到设备详情
     - **数据来源**：后端`/api/devices`接口
   
     #### 2.3 设备详情组件（DeviceDetail.vue）
   
     - **功能**：展示单个设备的详细信息和用电详情
     - **布局**：
       - 上半部分：设备基本信息卡片
       - 下半部分：用电详情表格和时间查询控件
     - **数据来源**：后端`/api/devices/:id`接口
   
     #### 2.4 能耗查询组件（EnergyQuery.vue）
   
     - **功能**：根据时间区间查询能耗数据
     - **时间选择**：
       - 快捷选择：今日、昨日、本周、本月
       - 自定义时间范围（精确到天）
       - 按天切换按钮
     - **展示字段**：回路名称、统计时间、时段用电量、时段电费
     - **数据来源**：后端`/api/energy`接口
   
     #### 2.5 报警信息组件（AlarmInfo.vue）
   
     - **功能**：展示设备报警信息
   
     - **触发方式**：点击页面头部查询表单的"查看报警信息"按钮
   
     - **展示字段**：
   
       | 字段名   | 数据来源        | 描述                    |
       | :------- | :-------------- | :---------------------- |
       | 序号     | 前端生成        | -                       |
       | 设备编号 | fDevicecode     | 发生报警的设备编号      |
       | 报警类型 | fMessinfodesc   | 报警事件描述            |
       | 报警等级 | fMessinfotypeid | 1：普通 2：严重 3：事故 |
       | 报警时间 | fAlarmtime      | 报警发生时间            |
       | 报警值   | fValue          | 触发报警的参数值        |
       | 限值     | fLimitvalue     | 报警阈值                |
       | 确认状态 | fConfirmstatus  | 未确认/已确认           |
       | 确认人   | fConfirmperson  | 确认报警的人员          |
   
     - **数据来源**：后端`/api/alarm`接口
   
     ## 五、关键技术点
   
     ### 1. 后端Token管理
   
     - 首次调用EMS API获取Token
     - Token过期自动刷新
     - 确保所有请求携带有效Token
   
     ### 2. 数据整合策略
   
     - 后端统一整合多API数据
     - 前端直接使用整合后的数据
     - 减少前端数据处理复杂度
   
     ### 3. 前端状态管理
   
     - 使用Vue 3 Composition API
     - 组件内状态管理
     - 简单的props/event通信
   
     ### 4. 时间区间处理
   
     - 前端实现多种时间选择方式
     - 后端处理时间格式转换
     - 确保与EMS API时间格式兼容
   
     ### 5. 报警信息查询
   
     - 支持按时间范围查询报警信息
     - 支持按设备编号查询特定设备报警
     - 支持按报警等级筛选
   
     ## 六、预期交付物
   
     1. 完整的Node.js后端服务代码
     2. 完整的Vue 3前端应用代码
     3. 项目部署文档
     4. 功能测试报告
   
     ## 七、开发步骤
   
     1. **后端开发**：
        - 初始化Express项目
        - 配置API连接和Token管理
        - 实现设备列表、详情、能耗查询和报警信息的API服务
     2. **前端开发**：
        - 初始化Vue 3项目
        - 配置Element Plus和Axios
        - 开发设备列表、详情和能耗查询组件
        - 开发报警信息查询和展示组件
        - 实现页面头部查询表单和报警按钮
     3. **系统测试**：
        - 测试所有API接口
        - 测试前端组件功能
        - 测试跨域访问
        - 测试数据展示准确性
     4. **部署上线**：
        - 部署后端服务
        - 构建并部署前端应用
        - 配置Nginx反向代理
   
     ## 八、注意事项
   
     1. 确保后端服务的安全性，防止未授权访问
     2. 优化前端性能，特别是大数据量展示时的渲染性能
     3. 确保API调用的错误处理和重试机制
     4. 考虑系统的可扩展性，便于后续功能扩展
   
     以上开发计划包含了用户要求的所有功能：设备信息展示、能耗查询、时间区间筛选和报警信息查看。