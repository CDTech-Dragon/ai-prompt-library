# PC在线监测系统 - 技术文档

## 1. 系统概述

PC在线监测系统是一个基于Vue 3 + TypeScript开发的前端应用，用于实时监测PC设备的运行状态，包括重启次数、生产数量、问题条数等关键指标。系统支持数据筛选、查询、排序、详情查看等功能，同时提供报警管理、密码验证等辅助功能。

## 2. 技术架构

### 2.1 前端架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        浏览器层                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                        应用层                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                        组件层                             │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │                    App.vue                         │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │                  PcMonitor.vue                      │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                        工具层                             │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │                    api.ts                           │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │                  apiConfig.ts                       │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                        依赖层                             │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │                   Vue 3 + TypeScript                │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │                    Element Plus                     │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │                     Vite                            │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                        后端层                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                        API层                              │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │                    RESTful API                      │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 技术栈

| 技术/框架 | 版本 | 用途 |
|----------|------|------|
| Vue | 3.5.22 | 前端框架 |
| TypeScript | ~5.9.3 | 类型系统 |
| Element Plus | 2.11.7 | UI组件库 |
| Vite | 7.1.14 | 构建工具 |
| Lodash | - | 工具库 |
| @vueuse/core | 14.0.0 | Vue组合式API工具集 |
| @element-plus/icons-vue | 2.3.2 | Element Plus图标库 |

## 3. 代码结构

```
pcreboot-frontend/
├── src/
│   ├── assets/          # 静态资源
│   │   └── vue.svg
│   ├── components/      # 组件
│   │   └── PcMonitor.vue # 主监控组件
│   ├── utils/           # 工具函数
│   │   ├── api.ts       # API调用封装
│   │   └── apiConfig.ts # API路径配置
│   ├── App.vue          # 根组件
│   └── main.ts          # 入口文件
├── .gitignore           # Git忽略配置
├── index.html           # HTML模板
├── package.json         # 项目依赖配置
├── tsconfig.json        # TypeScript配置
├── tsconfig.app.json    # TypeScript应用配置
├── tsconfig.node.json   # TypeScript Node配置
├── vite.config.ts       # Vite配置
├── INITIAL_REQUIREMENTS.md # 初始需求文档
└── TECHNICAL_DOCUMENTATION.md # 技术文档
```

## 4. 核心功能实现

### 4.1 PC设备监控

#### 4.1.1 数据展示

PC设备监控的核心功能是展示PC设备的基本信息和关键指标，包括PC编号、责任人、车间、线别、地域、重启次数、生产数量、问题条数等。数据通过后端API获取，并在前端进行展示。

```vue
<el-table
  v-loading="loading"
  :data="paginatedData"
  style="width: 100%"
  fit
  @sort-change="handleSort"
  :default-sort="{prop: 'restartCount', order: 'descending'}"
  border
  :header-cell-style="{backgroundColor: '#364578', color: 'white', fontWeight: 'bold'}"
>
  <el-table-column type="index" label="序号" width="80" align="center" :index="indexMethod" />
  <el-table-column prop="pcNo" label="PC资产编号" sortable="custom" min-width="120" />
  <el-table-column prop="responsiblePerson" label="责任人" sortable="custom" min-width="100" />
  <el-table-column prop="region" label="地域" sortable="custom" min-width="80" align="center" />
  <el-table-column prop="workshop" label="车间" sortable="custom" align="center" min-width="80" />
  <el-table-column prop="line" label="线别" sortable="custom" min-width="180" />
  <el-table-column prop="portNo" label="端口" sortable="custom" align="center" min-width="70" />
  <el-table-column prop="model" label="机型" sortable="custom" min-width="180" />
  <el-table-column prop="restartCount" label="重启总次数" sortable="custom" min-width="120" show-overflow-tooltip>
    <template #default="scope">
      <el-tooltip
          effect="dark"
          :content="'（双击查看详情）'"
          placement="top"
        >
        <span
          :class="{ 'text-danger': scope.row.restartCount >= 3 }"
          @dblclick="showPCRestartDetails(scope.row)"
          style="cursor: pointer; padding-left: 25px; font-weight: bold;"
        >
              {{ formatNumber(scope.row.restartCount) }}次
        </span>
      </el-tooltip>
    </template>
  </el-table-column>
  <!-- 其他列省略 -->
</el-table>
```

#### 4.1.2 数据加载

数据加载功能通过调用后端API获取PC设备信息，并在前端进行处理和展示。

```typescript
/**
 * 加载PC设备数据
 * @description 从后端API获取PC设备数据，并更新到表格中
 */
const loadData = async () => {
  loading.value = true
  try {
    // 构建请求参数
    const params = {
      page: pagination.currentPage,
      pageSize: pagination.pageSize,
      keyword: searchForm.keyword,
      workshop: searchForm.workshop,
      line: searchForm.line,
      region: selectedRegion.value,
      productionStatus: productionStatus.value,
      startDate: searchForm.dateRange?.[0],
      endDate: searchForm.dateRange?.[1],
      sortField: sortField.value,
      sortOrder: sortOrder.value
    }
    
    // 调用API获取数据
    const response = await fetch(`${API_PATHS.PC_INFO_PAGE}?${new URLSearchParams(params as any)}`)
    const data = await response.json()
    
    // 更新表格数据
    allData.value = data.records || []
    pagination.total = data.total || 0
    
    // 更新统计数据
    totalComputerCount.value = data.total || 0
    totalRestartCount.value = data.totalRestartCount || 0
    totalProductionCount.value = data.totalProductionCount || 0
    totalProblemCount.value = data.totalProblemCount || 0
  } catch (error) {
    console.error('加载数据失败:', error)
    ElMessage.error('加载数据失败，请重试')
  } finally {
    loading.value = false
  }
}
```

### 4.2 数据筛选与查询

#### 4.2.1 筛选条件

系统支持多种筛选条件，包括日期范围、车间、线别、地域、关键字、生产/未生产状态等。

```vue
<el-form :model="searchForm" class="optimized-form">
  <!-- 第一行：所有筛选条件在一行显示 -->
  <div class="form-row single-line-filters">
    <el-form-item label="起止日期" class="form-item date-picker-item">
      <el-date-picker
        v-model="searchForm.dateRange"
        type="daterange"
        range-separator="至"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
        value-format="YYYY-MM-DD HH:mm:ss"
        style="width: 100%"
        class="form-control"
        size="default"
        @change="handleDateRangeChange"
      />
    </el-form-item>
    
    <el-form-item label="车间" class="form-item select-item">
      <el-select
        v-model="searchForm.workshop"
        placeholder="请选择车间"
        clearable
        style="width: 100%"
        @change="handleWorkshopChange"
        class="form-control"
        size="default"
        :disabled="getWorkshopDisabled()"
      >
        <el-option v-for="workshop in availableWorkshops" :key="workshop" :label="workshop" :value="workshop" />
      </el-select>
    </el-form-item>
    
    <el-form-item label="线别" class="form-item select-item">
      <el-select
        v-model="searchForm.line"
        placeholder="请先选择车间"
        clearable
        style="width: 100%"
        class="form-control"
        size="default"
        :disabled="getLineDisabled()"
        :loading="isLineLoading"
        @change="handleLineChange"
      >
        <!-- 线别选项省略 -->
      </el-select>
    </el-form-item>
    
    <el-form-item label="筛选条件" class="form-item keyword-item">
      <div style="display: flex; align-items: center; gap: 12px; width: 100%;">
        <el-input
          v-model="searchForm.keyword"
          placeholder="请输入PC编号/责任人/车间/线别/机型/机型描述/MAC地址"
          clearable
          style="flex: 1; min-width: 0;"
          class="form-control"
          size="default"
        >
          <!-- 输入框提示省略 -->
        </el-input>  
      </div>
    </el-form-item>
  </div>
  
  <!-- 第二行：左侧统计信息，右侧操作按钮 -->
  <div class="form-row second-row">
    <!-- 左侧统计信息省略 -->
    
    <!-- 右侧操作按钮 -->
    <div class="button-group right-buttons">
      <!-- 生产/未生产状态切换按钮 -->
      <div class="status-toggle-buttons">
        <el-button 
          size="small" 
          :class="['status-btn', productionStatus === 'production' ? 'active-status-btn' : productionStatus === '' ? 'neutral-status-btn' : 'inactive-status-btn']"
          @click="toggleProductionStatus('production')"
          :loading="isLoadingData"
        >
          生产
        </el-button>
        <el-button 
          size="small" 
          :class="['status-btn', productionStatus === 'unproduction' ? 'active-status-btn' : productionStatus === '' ? 'neutral-status-btn' : 'inactive-status-btn']"
          @click="toggleProductionStatus('unproduction')"
          :loading="isLoadingData"
        >
          未生产
        </el-button>
      </div>
      
      <!-- 地域切换按钮 -->
      <div class="region-buttons improved-region-buttons">
        <el-button 
          size="small" 
          :class="['region-btn', selectedRegion === '' ? 'active-region-btn' : 'inactive-region-btn']"
          @click="changeRegion('')"
          :data-region="''"
          :disabled="getRegionDisabled('')"
        >
          ALL
        </el-button>
        <el-button 
          size="small" 
          :class="['region-btn', selectedRegion === 'HN' ? 'active-region-btn' : 'inactive-region-btn']"
          @click="changeRegion('HN')"
          data-region="HN"
          :disabled="getRegionDisabled('HN')"
        >
          HN
        </el-button>
        <el-button 
          size="small" 
          :class="['region-btn', selectedRegion === 'SZ' ? 'active-region-btn' : 'inactive-region-btn']"
          @click="changeRegion('SZ')"
          data-region="SZ"
          :disabled="getRegionDisabled('SZ')"
        >
          SZ
        </el-button>
      </div>
      
      <!-- 其他按钮省略 -->
    </div>
  </div>
</el-form>
```

#### 4.2.2 筛选逻辑

筛选逻辑通过计算属性实现，根据用户选择的筛选条件动态过滤表格数据。

```typescript
// 计算属性 - 过滤和排序后的数据
const filteredData = computed(() => {
  let data = [...allData.value]

  // 地域筛选
  if (selectedRegion.value) {
    data = data.filter(item => item.region === selectedRegion.value)
  }

  // 车间筛选
  if (searchForm.workshop) {
    data = data.filter(item => item.workshop === searchForm.workshop)
  }
  
  // 线别筛选
  if (searchForm.line) {
    data = data.filter(item => item.line === searchForm.line)
  }

  // 关键字筛选
  if (searchForm.keyword) {
    const keyword = searchForm.keyword.toLowerCase()
    data = data.filter(item =>
      item.pcNo.toLowerCase().includes(keyword) ||
      item.responsiblePerson.toLowerCase().includes(keyword) ||
      item.workshop.toLowerCase().includes(keyword) ||
      item.line.toLowerCase().includes(keyword) ||
      item.region.toLowerCase().includes(keyword) ||
      item.model.toLowerCase().includes(keyword) ||
      (item.modelDescription && item.modelDescription.toLowerCase().includes(keyword)) ||
      item.macAddress.toLowerCase().includes(keyword)
    )
  }

  // 生产/未生产状态筛选
  if (productionStatus.value === 'production') {
    // 生产状态：展示所有重启次数大于0或生产数量大于0的数据
    data = data.filter(item => (item.restartCount || 0) > 0 || (item.productionCount || 0) > 0)
  } else if (productionStatus.value === 'unproduction') {
    // 未生产状态：展示所有生产数量等于0且重启次数为0的数据
    data = data.filter(item => (item.productionCount || 0) === 0 && (item.restartCount || 0) === 0)
  }

  // 排序
  if (sortField.value && sortOrder.value) {
    data.sort((a, b) => {
      const aValue = a[sortField.value as keyof PCInfo]
      const bValue = b[sortField.value as keyof PCInfo]

      // 特殊处理"落实"列的排序
      if (sortField.value === 'isImplemented') {
        // 定义排序优先级：NG > OK > 无问题
        const getPriority = (value: string) => {
          return value === 'OK' ? 3 : value === 'NG' ? 2 : value === '无问题' ? 1 : 0
        }
        const aPriority = getPriority(aValue as string)
        const bPriority = getPriority(bValue as string)
        return sortOrder.value === 'ascending' ? aPriority - bPriority : bPriority - aPriority
      }
      // 特殊处理"更新时间"列的排序，将其作为日期类型进行比较
      else if (sortField.value === 'updateTime') {
        // 处理特殊情况：无重启时间
        const aIsValidDate = aValue as string !== '无重启时间' && !isNaN(new Date(aValue as string).getTime())
        const bIsValidDate = bValue as string !== '无重启时间' && !isNaN(new Date(bValue as string).getTime())
        
        // 如果两者都不是有效日期，视为相等
        if (!aIsValidDate && !bIsValidDate) {
          return 0
        }
        // 如果只有a是有效日期，a排在前面
        if (aIsValidDate && !bIsValidDate) {
          return sortOrder.value === 'ascending' ? -1 : 1
        }
        // 如果只有b是有效日期，b排在前面
        if (!aIsValidDate && bIsValidDate) {
          return sortOrder.value === 'ascending' ? 1 : -1
        }
        // 如果两者都是有效日期，比较日期大小
        const aDate = new Date(aValue as string)
        const bDate = new Date(bValue as string)
        return sortOrder.value === 'ascending' ? aDate.getTime() - bDate.getTime() : bDate.getTime() - aDate.getTime()
      }
      // 其他列按照默认方式排序
      else {
        if (aValue < bValue) {
          return sortOrder.value === 'ascending' ? -1 : 1
        }
        if (aValue > bValue) {
          return sortOrder.value === 'ascending' ? 1 : -1
        }
        return 0
      }
    })
  }

  return data
})
```

### 4.3 详情查看

#### 4.3.1 重启详情

重启详情功能允许用户双击PC设备的重启次数，查看该设备的详细重启记录，包括重启时间、操作人员、机型等信息。

```vue
<!-- 重启详情对话框 -->
<el-dialog
  v-model="dialogVisible"
  :title="`${selectedPC?.pcNo} - 重启详情`"
  width="60%"
  :fullscreen="isMobile"
  center
  style="font-size: 16px;"
  class="restart-detail-dialog"
>
  <div class="restart-detail-container">
    <div class="detail-header">
      <el-descriptions :column="3" border>
        <el-descriptions-item label="PC编号">{{ selectedPC?.pcNo }}</el-descriptions-item>
        <el-descriptions-item label="PIE责任人">{{ selectedPC?.responsiblePerson }}</el-descriptions-item>
        <el-descriptions-item label="车间">{{ selectedPC?.workshop }}</el-descriptions-item>
        <el-descriptions-item label="线别">{{ selectedPC?.line }}</el-descriptions-item>
        <el-descriptions-item label="MAC地址">{{ selectedPC?.macAddress }}</el-descriptions-item>
        <el-descriptions-item label="IP地址">{{ selectedPC?.ipAddress }}</el-descriptions-item>
      </el-descriptions>
    </div>
    <h3 style="margin: 0 0 5px 10px; font-weight: bold; color: #364578;">重启记录</h3>
    <div class="restart-log">
      <!-- 加载状态指示器 -->
      <div v-if="loadingRestartDetails" class="loading-container">
        <el-icon class="loading-icon"><Loading /></el-icon>
        <span class="loading-text">正在加载重启详情...</span>
      </div>
      
      <!-- 重启记录表格 -->
      <el-table
        v-else
        :data="paginatedRestartDetails"
        style="width: 100%"
        border
        fit
        class="restart-log-table"
        max-height="380"
        @sort-change="handleRestartSort"
        :header-cell-style="{backgroundColor: '#364578', color: 'white', fontWeight: 'bold'}"
        :empty-text="filteredRestartDetails.length === 0 && !loadingRestartDetails ? '暂无重启记录' : '加载中...'"
      >
        <el-table-column type="index" label="序号" width="80" align="center" />
        <el-table-column prop="restartTime" label="重启时间" min-width="80" sortable="custom" />
        <el-table-column prop="operator" label="生产责任人" min-width="60" sortable="custom" />
        <el-table-column prop="model" label="机型" min-width="120" align="center">
          <template #default="scope">
            <span>{{ scope.row.model || '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="modelDescription" label="机型描述" min-width="200" align="center">
          <!-- 机型描述省略 -->
        </el-table-column>
      </el-table>
      
      <!-- 分页控件省略 -->
    </div>
  </div>
</el-dialog>
```

#### 4.3.2 问题详情

问题详情功能允许用户双击PC设备的问题条数，查看该设备的详细问题记录，包括问题内容、问题原因、改善方向等信息。

```vue
<!-- 问题详情对话框 -->
<el-dialog
  v-model="problemDetailVisible"
  :title="`${selectedProblemPC?.pcNo} - 问题详情`"
  width="60%"
  :fullscreen="isMobile"
  center
  style="font-size: 16px;"
  class="problem-detail-dialog"
>
  <div class="problem-detail-container">
    <div class="detail-header">
      <el-descriptions :column="3" border>
        <el-descriptions-item label="责任人">{{ selectedProblemPC?.responsiblePerson }}</el-descriptions-item>
        <el-descriptions-item label="车间">{{ selectedProblemPC?.workshop }}</el-descriptions-item>
        <el-descriptions-item label="线别">{{ selectedProblemPC?.line }}</el-descriptions-item>
        <el-descriptions-item label="机型">{{ selectedProblemPC?.model }}</el-descriptions-item>
        <el-descriptions-item label="MAC地址">{{ selectedProblemPC?.macAddress }}</el-descriptions-item>
        <el-descriptions-item label="IP地址">{{ selectedProblemPC?.ipAddress }}</el-descriptions-item>
      </el-descriptions>
    </div>
    
    <!-- 问题详情表格 -->
    <div class="problem-details-content" style="margin-top: 5px;">
      <h3 style="margin: 0 0 5px 10px; font-weight: bold; color: #364578;">问题记录</h3>
      
      <!-- 加载状态显示 -->
      <div v-if="loadingProblemDetails" class="loading-container" style="display: flex; justify-content: center; align-items: center; height: 150px;">
        <!-- 加载状态省略 -->
      </div>
      
      <!-- 问题详情表格 -->
      <el-table
        v-else
        :data="paginatedProblemDetails"
        style="width: 100%"
        max-height="450"
        border
        fit
        @sort-change="handleProblemSort"
        :header-cell-style="{backgroundColor: '#364578', color: 'white', fontWeight: 'bold'}"
      >
        <!-- 表头结构 -->
        <el-table-column type="index" label="序号" width="60" align="center" />
        <el-table-column prop="alarmMessage" label="问题内容" min-width="300" align="center" sortable="custom">
          <!-- 问题内容省略 -->
        </el-table-column>
        <el-table-column prop="alarmType" label="问题原因" min-width="150" align="center" sortable="custom" />
        <el-table-column prop="improvementDirection" label="改善方向" min-width="150" align="center" sortable="custom" />
        <el-table-column prop="improver" label="改善人" min-width="100" align="center" sortable="custom" />
        <el-table-column prop="status" label="落实" min-width="100" align="center" sortable="custom">
          <template #default="scope">
            <el-tag :type="scope.row.status === 'OK' ? 'success' : 'danger'">
              {{ scope.row.status === 'OK' ? '已落实' : '未落实' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="confirmer" label="确认人" min-width="100" align="center" sortable="custom" />
        <el-table-column prop="confirmationTime" label="确认时间" min-width="180" align="center" sortable="custom" />
      </el-table>
      
      <!-- 分页控件省略 -->
    </div>
  </div>
</el-dialog>
```

### 4.4 报警管理

#### 4.4.1 报警信息查看

报警信息查看功能允许用户查看PC设备的报警信息，包括PC编号、MAC地址、位置、负责人、报警信息、报警时间、机型等。

```vue
<!-- 报警信息抽屉 -->
<el-drawer
  v-model="drawerVisible"
  direction="rtl"
  size="60%"
  :before-close="handleDrawerClose"
  class="alert-drawer"
>
  <template #header>
    <span style="color: #183c85; font-size: 18px; font-weight: bold;">报警信息</span>
  </template>
  <!-- 报警信息表格 -->
  <el-table
    :data="alertData"
    style="width: 100%"
    class="alert-table"
    max-height="450"
    row-key="$index"
    @sort-change="handleAlertSort"
  >
    <el-table-column type="index" label="序号" width="60" align="center" />
    <el-table-column prop="pcNumber" label="PC编号" sortable="custom" min-width="100" />
    <el-table-column prop="macAddress" label="MAC地址" sortable="custom" min-width="120" />
    <el-table-column prop="location" label="位置" min-width="80" />
    <el-table-column prop="responsiblePerson" label="负责人" min-width="70" />
    <el-table-column prop="model" label="机型" sortable="custom" min-width="100">
      <template #default="scope">
        <span>{{ scope.row.model || '-' }}</span>
      </template>
    </el-table-column>
    <el-table-column prop="alarmMessage" label="报警信息" min-width="200">
      <!-- 报警信息省略 -->
    </el-table-column>
    <el-table-column prop="createdAt" label="报警时间" min-width="180" sortable="custom">
      <template #default="scope">
        {{ formatDateTime(scope.row.createdAt) || '-' }}
      </template>
    </el-table-column>
  </el-table>
  
  <!-- 其他报警功能省略 -->
</el-drawer>
```

#### 4.4.2 报警规则管理

报警规则管理功能允许用户查看和修改报警规则，包括每小时重启次数阈值和每天重启次数阈值。

```vue
<!-- 报警规则表格 -->
<div class="rules-table-section">
  <h3>报警规则列表</h3>
  <el-table
    :data="alertRuleList"
    style="width: 100%"
    border
    class="rules-table"
    :row-class-name="rowClassName"
    :header-row-style="{background: '#f8f9fa', fontWeight: 500}"
    empty-text="暂无报警规则"
  >
    <el-table-column
      prop="createTime"
      label="制定时间"
      min-width="180"
      align="center"
    />
    <el-table-column
      prop="ruleCode"
      label="规则编码"
      min-width="120"
      align="center"
      :formatter="formatRuleCode"
    />
    <el-table-column
      prop="ruleContent"
      label="规则内容"
      min-width="300"
      align="left"
    />
    <el-table-column
      label="操作"
      min-width="140"
      align="center"
    >
      <template #default="scope">
        <el-button
          type="primary"
          size="small"
          @click="editRule(scope.row)"
          :disabled="!isAuthenticated || editingRuleId !== null && editingRuleId !== scope.row.id"
          :title="isAuthenticated ? '修改规则' : '请先进行密码验证'"
          style="margin-right: 8px;"
        >
          修改
        </el-button>
      </template>
    </el-table-column>
  </el-table>
</div>

<!-- 规则制定区域 -->
<div v-if="showRulesForm" class="rules-form-container">
  <h3>规则制定</h3>
  <el-form :model="alertRules" class="rules-form">
    <!-- 阈值设置提示 -->
    <div class="threshold-tip" style="margin-bottom: 10px; padding: 8px; background-color: #f0f9ff; border: 1px solid #91d5ff; border-radius: 4px; color: #1890ff;">
      <i class="el-icon-info"></i> 请选择以下两种阈值类型之一，不可同时设置
    </div>
    
    <el-form-item label="小时重启阈值" :label-style="{ color: '#364578' }">
      <el-input-number
        v-model="alertRules.hourlyThreshold"
        :min="0"
        :max="999"
        :step="1"
        style="width: 120px;"
        placeholder="请输入次数"
      />
      <span class="threshold-unit">次/小时</span>
      <span v-if="alertRules.hourlyThreshold === 0" class="zero-threshold-tip">（将被忽略）</span>
    </el-form-item>
    <el-form-item label="&nbsp;&nbsp;&nbsp;&nbsp;天重启阈值" :label-style="{ color: '#364578' }">
      <el-input-number
        v-model="alertRules.dailyThreshold"
        :min="0"
        :max="9999"
        :step="1"
        style="width: 120px;"
        placeholder="请输入次数"
      />
      <span class="threshold-unit">次/天</span>
      <span v-if="alertRules.dailyThreshold === 0" class="zero-threshold-tip">（将被忽略）</span>
    </el-form-item>
  </el-form>
</div>
```

### 4.5 密码验证

密码验证功能用于保护敏感操作，如修改报警规则等。系统支持密码错误次数限制，超过限制后将无法继续操作。

```vue
<!-- 密码验证Dialog -->
<el-dialog
  v-model="passwordDialogVisible"
  title="请输入密码"
  width="380px"
  :close-on-click-modal="false"
  :close-on-press-escape="false"
  destroy-on-close
>
  <div class="password-dialog-content">
    <div class="password-icon">
      <el-icon class="lock-icon"><Lock /></el-icon>
    </div>
    <div class="password-input-container">
      <el-input
        ref="passwordInputRef"
        v-model="password"
        type="password"
        placeholder="请输入访问密码"
        show-password
        autocomplete="new-password"
        class="password-input"
        :disabled="isVerifying"
        @keyup.enter="handlePasswordConfirm"
      />
    </div>
    <div class="password-hint">
      <small v-if="passwordErrorCount > 0" class="error-count">
        (错误次数：{{ passwordErrorCount }}/{{ maxErrorAttempts }})
      </small>
    </div>
  </div>
  <template #footer>
    <span class="dialog-footer">
      <el-button @click="handlePasswordCancel" :disabled="isVerifying">取消</el-button>
      <el-button type="primary" @click="handlePasswordConfirm" :loading="isVerifying">
        {{ isVerifying ? '验证中...' : '确认' }}
      </el-button>
    </span>
  </template>
</el-dialog>
```

## 5. API 设计

### 5.1 API 路径配置

| API名称 | API路径 | 方法 | 用途 |
|--------|---------|------|------|
| PC设备信息分页查询 | /api/pc/info/page | GET | 获取PC设备信息列表，支持分页、筛选、排序 |
| PC设备信息统计 | /api/pc/info/count | GET | 获取PC设备信息统计数据 |
| PC重启详情分页查询 | /api/pc/restart-details/page | GET | 获取PC重启详情列表，支持分页、筛选、排序 |
| PC重启详情统计 | /api/pc/restart-details/count | GET | 获取PC重启详情统计数据 |
| 问题详情列表 | /api/problem/list | GET | 获取问题详情列表，支持筛选 |
| 报警规则列表 | /api/alarm-rule/list | GET | 获取报警规则列表 |
| 报警规则更新 | /api/alarm-rule/update | POST | 更新报警规则 |
| 报警规则创建 | /api/alarm-rule/create | POST | 创建报警规则 |
| 今日报警信息 | /api/alarm/today | GET | 获取今日报警信息列表 |

### 5.2 API 调用示例

```typescript
/**
 * 获取PC设备信息列表
 * @param params 查询参数
 * @returns PC设备信息列表
 */
export const fetchPCInfoList = async (params: any) => {
  const response = await fetch(`${API_PATHS.PC_INFO_PAGE}?${new URLSearchParams(params as any)}`)
  return response.json()
}

/**
 * 获取PC重启详情列表
 * @param macAddress MAC地址
 * @param startDate 开始日期
 * @param endDate 结束日期
 * @returns PC重启详情列表
 */
export const fetchRestartDetails = async (macAddress: string, startDate?: string, endDate?: string) => {
  const params = {
    macAddress,
    startDate,
    endDate
  }
  const response = await fetch(`${API_PATHS.PC_RESTART_DETAILS_PAGE}?${new URLSearchParams(params as any)}`)
  return response.json()
}

/**
 * 获取问题详情列表
 * @param macAddress MAC地址
 * @param startDate 开始日期
 * @param endDate 结束日期
 * @returns 问题详情列表
 */
export const fetchProblemDetails = async (macAddress: string, startDate?: string, endDate?: string) => {
  const params = {
    macAddress,
    startDate,
    endDate
  }
  const response = await fetch(`${API_PATHS.PROBLEM_LIST}?${new URLSearchParams(params as any)}`)
  return response.json()
}

/**
 * 获取报警规则列表
 * @returns 报警规则列表
 */
export const fetchAlarmRules = async () => {
  const response = await fetch(API_PATHS.ALARM_RULE_LIST)
  return response.json()
}

/**
 * 更新报警规则
 * @param rule 报警规则
 * @returns 更新结果
 */
export const updateAlarmRule = async (rule: AlertRule) => {
  const response = await fetch(API_PATHS.ALARM_RULE_UPDATE, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(rule)
  })
  return response.json()
}

/**
 * 获取今日报警信息
 * @returns 今日报警信息列表
 */
export const fetchTodayAlarms = async () => {
  const response = await fetch(API_PATHS.ALARM_TODAY)
  return response.json()
}
```

## 6. 性能优化

### 6.1 分页加载

系统采用分页加载机制，每次只加载当前页的数据，减少一次性加载大量数据的压力，提高页面加载速度和响应速度。

### 6.2 虚拟滚动

对于大量数据的表格，系统支持虚拟滚动，只渲染当前可见区域的数据，减少DOM节点数量，提高表格的渲染性能和滚动流畅度。

### 6.3 缓存机制

系统采用缓存机制，对频繁调用的API进行缓存，减少API调用次数，提高页面响应速度。

### 6.4 懒加载

系统采用懒加载机制，对于非关键资源（如图片、视频等），在需要时才进行加载，减少初始加载时间。

### 6.5 代码分割

系统采用代码分割机制，将代码分成多个小块，按需加载，减少初始加载时间。

## 7. 安全性

### 7.1 密码验证

系统支持密码验证功能，保护敏感操作，如修改报警规则等。密码验证采用前端验证和后端验证相结合的方式，提高安全性。

### 7.2 跨域请求配置

系统支持跨域请求配置，允许来自不同域名的请求访问API，提高系统的灵活性和可用性。

### 7.3 数据加密

系统支持数据加密，对敏感数据（如密码、MAC地址等）进行加密存储和传输，提高数据的安全性。

### 7.4 错误处理

系统采用统一的错误处理机制，对API调用错误、网络错误等进行捕获和处理，提高系统的稳定性和可靠性。

## 8. 部署与运行

### 8.1 开发环境

#### 8.1.1 安装依赖

```bash
npm install
```

#### 8.1.2 启动开发服务器

```bash
npm run dev
```

开发服务器启动后，可以通过 http://localhost:5173 访问系统。

### 8.2 生产环境

#### 8.2.1 构建生产版本

```bash
npm run build
```

构建完成后，生成的静态文件位于 `dist` 目录下。

#### 8.2.2 部署生产版本

将 `dist` 目录下的静态文件部署到Web服务器（如Nginx、Apache等）即可。

## 9. 监控与维护

### 9.1 日志监控

系统支持日志监控，记录系统运行过程中的关键操作和错误信息，便于问题定位和分析。

### 9.2 性能监控

系统支持性能监控，监控系统的响应时间、页面加载时间、API调用次数等指标，便于性能优化和问题定位。

### 9.3 错误监控

系统支持错误监控，捕获和记录系统运行过程中的错误信息，便于问题定位和修复。

## 10. 总结

PC在线监测系统是一个功能完善、性能优良、安全性高的前端应用，用于实时监测PC设备的运行状态。系统采用Vue 3 + TypeScript开发，使用Element Plus组件库，支持数据筛选、查询、排序、详情查看等功能，同时提供报警管理、密码验证等辅助功能。系统具有良好的扩展性和可维护性，便于后续功能扩展和技术升级。
