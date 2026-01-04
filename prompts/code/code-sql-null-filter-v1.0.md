# SQL筛选NULL值提示词 - v1.0.0
> 简短描述：生成筛选SQL字段为NULL或非NULL的语句，支持多种数据库

#### 1. 基础信息
| 字段         | 内容                          |
|--------------|-------------------------------|
| ID           | prompt-code-sql-001           |
| 适用模型     | GPT-4, Claude 3, 通义千问, Gemini |
| 难度等级     | 基础                          |
| 创建时间     | 2026-01-04                    |
| 最后更新时间 | 2026-01-04                    |
| 作者         | prompt-library-contributors   |

#### 2. 核心用途
详细说明：
- 该提示词用于生成SQL语句，筛选出指定表中指定字段为NULL或非NULL的记录
- 适用于数据库查询、数据分析、报表生成等场景
- 相比普通提示词，生成的SQL语句兼容性更好，包含详细注释，便于理解和修改

#### 3. 提示词正文
> 遵循 ROLE-TASK-CONSTRAINT-OUTPUT 框架

### 角色
你是资深数据库工程师，熟悉MySQL、PostgreSQL、Oracle等主流数据库语法规范。

### 任务
请编写SQL语句，筛选出指定表中指定字段为NULL或非NULL的记录。

### 约束条件
1. 语句需兼容MySQL 8.0+、PostgreSQL 13+、Oracle 19c
2. 输出包含详细注释，解释核心逻辑
3. 同时提供筛选NULL和非NULL的两种写法
4. 支持多字段筛选场景
5. 代码格式规范，可读性强

### 输出格式
```sql
-- 筛选NULL值的语句
SELECT * 
FROM [表名] 
WHERE [字段名1] IS NULL;

-- 筛选非NULL值的语句  
SELECT * 
FROM [表名] 
WHERE [字段名1] IS NOT NULL;

-- 多字段筛选NULL值的语句
SELECT * 
FROM [表名] 
WHERE [字段名1] IS NULL 
  AND [字段名2] IS NULL;

-- 多字段筛选非NULL值的语句
SELECT * 
FROM [表名] 
WHERE [字段名1] IS NOT NULL 
  AND [字段名2] IS NOT NULL;
```

#### 4. 使用示例

##### 输入场景
从 `improvement_records` 表中筛选 `A2_improver` 字段为 NULL 的所有记录

##### 输出结果
```sql
-- 筛选improvement_records表中A2_improver字段为NULL的记录
SELECT * 
FROM improvement_records 
WHERE A2_improver IS NULL;

-- 筛选improvement_records表中A2_improver字段非NULL的记录
SELECT * 
FROM improvement_records 
WHERE A2_improver IS NOT NULL;
```

#### 5. 注意事项
1. SQL中NULL不能用`=`或`!=`判断，必须用`IS NULL`或`IS NOT NULL`
2. 不同数据库对NULL的处理方式基本一致，该提示词支持主流数据库
3. 如需筛选多个NULL字段，可叠加`AND`条件
4. 对于包含NULL值的字段排序，不同数据库行为可能不同，需注意
5. 在使用聚合函数时，NULL值会被忽略，如需包含NULL值需特殊处理

#### 6. 变更日志
- v1.0.0（2026-01-04）：初始版本，完成SQL筛选NULL值提示词