# [提示词名称] - v[主版本.次版本.修订号]
> 简短描述：一句话概括该提示词的核心用途（如「生成筛选SQL字段为NULL的语句」）

#### 1. 基础信息
| 字段         | 内容                          |
|--------------|-------------------------------|
| ID           | [唯一标识，如prompt-code-sql-001] |
| 适用模型     | [如GPT-4/Claude 3/Midjourney v6/通义千问] |
| 难度等级     | [基础/进阶/专家]              |
| 创建时间     | [YYYY-MM-DD]                  |
| 最后更新时间 | [YYYY-MM-DD]                  |
| 作者         | [GitHub用户名/姓名]           |

#### 2. 核心用途
详细说明：
- 该提示词解决什么问题？
- 适用的业务场景/用户需求？
- 相比普通提示词的优势？

#### 3. 提示词正文
> 建议遵循 ROLE-TASK-CONSTRAINT-OUTPUT 框架（可根据场景调整）

### 角色
[定义 AI 的角色，如「你是资深 SQL 工程师，熟悉 MySQL/PostgreSQL/Oracle 语法规范」]

### 任务
[明确 AI 要完成的核心任务，如「帮我编写 SQL 语句，筛选出指定表中指定字段为 NULL 的记录」]

### 约束条件
[技术约束，如「语句需兼容 MySQL 8.0+，避免使用专有语法」]
[格式约束，如「输出结果需包含注释，解释核心逻辑」]
[其他约束，如「同时提供筛选 NULL 和非 NULL 的两种写法」]

### 输出格式
[指定输出的结构 / 格式，如：
```sql
-- 筛选NULL的语句
SELECT * FROM [表名] WHERE [字段名] IS NULL;

-- 筛选非NULL的语句
SELECT * FROM [表名] WHERE [字段名] IS NOT NULL;
```]

#### 4. 使用示例

##### 输入场景
[用户实际需求示例，如「从 improvement_records 表中筛选 A2_improver 字段为 NULL 的所有记录」]

##### 输出结果
[AI 实际返回的结果示例，如：
```sql
SELECT * FROM improvement_records WHERE A2_improver IS NULL;
```]

#### 5. 注意事项
1. [使用该提示词的坑点，如「SQL中NULL不能用=判断，必须用IS NULL」]
2. [跨模型适配说明，如「Claude/通义千问使用该提示词无需修改，Midjourney不适用」]
3. [扩展用法，如「如需筛选多个NULL字段，可叠加 AND 条件」]

#### 6. 变更日志
- v[版本号]（YYYY-MM-DD）：[变更说明，如「初始版本，完成基础SQL NULL筛选提示词」]
- v[版本号]（YYYY-MM-DD）：[变更说明，如「补充PostgreSQL适配说明」]