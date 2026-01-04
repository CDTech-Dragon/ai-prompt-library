# SQL提示词使用示例

## 场景说明
本示例展示如何使用 `prompts/code/code-sql-null-filter-v1.0.md` 提示词，生成筛选SQL字段为NULL的语句。

## 步骤1：选择合适的提示词
从仓库中选择对应的提示词文件：
- 文件路径：`prompts/code/code-sql-null-filter-v1.0.md`
- 提示词名称：SQL筛选NULL值提示词
- 适用场景：需要筛选数据库表中NULL值的场景

## 步骤2：复制提示词正文
从提示词文件中复制「提示词正文」部分：

```
角色：你是资深数据库工程师，熟悉MySQL、PostgreSQL、Oracle等主流数据库语法规范。

任务：请编写SQL语句，筛选出指定表中指定字段为NULL或非NULL的记录。

约束条件：
1. 语句需兼容MySQL 8.0+、PostgreSQL 13+、Oracle 19c
2. 输出包含详细注释，解释核心逻辑
3. 同时提供筛选NULL和非NULL的两种写法
4. 支持多字段筛选场景
5. 代码格式规范，可读性强

输出格式：
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
```

## 步骤3：修改占位符
根据实际需求，修改提示词中的占位符：

### 实际需求
从 `employee` 表中筛选 `department_id` 字段为NULL的所有记录，并同时筛选 `hire_date` 字段非NULL的记录。

### 调整后的提示词
```
角色：你是资深数据库工程师，熟悉MySQL、PostgreSQL、Oracle等主流数据库语法规范。

任务：请编写SQL语句，从employee表中筛选department_id字段为NULL且hire_date字段非NULL的所有记录。

约束条件：
1. 语句需兼容MySQL 8.0+、PostgreSQL 13+、Oracle 19c
2. 输出包含详细注释，解释核心逻辑
3. 代码格式规范，可读性强

输出格式：
```sql
-- 筛选语句
SELECT * 
FROM employee 
WHERE department_id IS NULL 
  AND hire_date IS NOT NULL;
```
```

## 步骤4：执行提示词
将调整后的提示词粘贴到AI模型对话框中执行，例如使用GPT-4：

### 输入
```
角色：你是资深数据库工程师，熟悉MySQL、PostgreSQL、Oracle等主流数据库语法规范。

任务：请编写SQL语句，从employee表中筛选department_id字段为NULL且hire_date字段非NULL的所有记录。

约束条件：
1. 语句需兼容MySQL 8.0+、PostgreSQL 13+、Oracle 19c
2. 输出包含详细注释，解释核心逻辑
3. 代码格式规范，可读性强

输出格式：
```sql
-- 筛选语句
SELECT * 
FROM employee 
WHERE department_id IS NULL 
  AND hire_date IS NOT NULL;
```
```

### 输出结果
```sql
-- 筛选employee表中department_id为NULL且hire_date非NULL的记录
-- 兼容MySQL 8.0+、PostgreSQL 13+、Oracle 19c
SELECT * 
FROM employee 
WHERE department_id IS NULL 
  AND hire_date IS NOT NULL;
```

## 步骤5：验证和使用
1. 将生成的SQL语句复制到数据库客户端（如MySQL Workbench、pgAdmin等）
2. 替换数据库连接信息，执行语句
3. 检查结果是否符合预期

## 扩展用法

### 示例1：筛选多个NULL字段

**需求**：从 `product` 表中筛选 `category_id` 和 `supplier_id` 均为NULL的记录。

**调整后的提示词任务**：
```
任务：请编写SQL语句，从product表中筛选category_id和supplier_id均为NULL的记录。
```

**生成的SQL**：
```sql
-- 筛选product表中category_id和supplier_id均为NULL的记录
SELECT * 
FROM product 
WHERE category_id IS NULL 
  AND supplier_id IS NULL;
```

### 示例2：结合其他条件筛选

**需求**：从 `order` 表中筛选 `customer_id` 为NULL，且 `order_date` 大于 '2025-01-01' 的记录。

**调整后的提示词任务**：
```
任务：请编写SQL语句，从order表中筛选customer_id为NULL，且order_date大于'2025-01-01'的记录。
```

**生成的SQL**：
```sql
-- 筛选order表中customer_id为NULL且order_date大于'2025-01-01'的记录
SELECT * 
FROM order 
WHERE customer_id IS NULL 
  AND order_date > '2025-01-01';
```

## 注意事项

1. **占位符替换**：确保替换所有占位符（如`[表名]`、`[字段名]`）为实际值
2. **数据库兼容性**：根据实际使用的数据库调整语法，虽然提示词已兼容主流数据库，但某些特殊语法可能仍需调整
3. **性能优化**：对于大数据表，建议添加索引或使用更高效的查询方式
4. **结果验证**：执行生成的SQL语句后，务必验证结果是否符合预期
5. **安全考虑**：避免直接在生产环境执行未验证的SQL语句，建议先在测试环境验证

## 最佳实践

1. **保存调整后的提示词**：将常用的调整后的提示词保存为个人模板，提高复用效率
2. **记录使用效果**：记录不同模型对同一提示词的生成效果，选择最适合的模型
3. **定期更新提示词**：关注仓库更新，及时获取优化后的提示词版本
4. **贡献反馈**：如发现提示词存在问题或可以优化，欢迎提交PR或Issue

## 相关提示词

- `prompts/code/code-sql-join-v1.0.md`：SQL连接查询提示词
- `prompts/code/code-sql-aggregate-v1.0.md`：SQL聚合查询提示词
- `prompts/code/code-sql-update-v1.0.md`：SQL更新语句提示词

## 常见问题

### Q：生成的SQL语句执行报错怎么办？
**A**：检查以下几点：
1. 表名和字段名是否正确
2. 数据库语法是否兼容
3. 括号、引号等语法是否正确
4. 是否缺少必要的权限

### Q：如何优化生成的SQL语句性能？
**A**：可以在提示词中添加性能优化相关的约束，例如：
```
约束条件：
...
6. 语句需经过性能优化，适合大数据表查询
7. 建议添加合适的索引
```

### Q：可以生成复杂的SQL语句吗？
**A**：可以，只需在提示词任务中详细描述需求，例如：
```
任务：请编写SQL语句，统计每个部门的员工数量、平均工资和最高工资，筛选出平均工资大于5000的部门，并按员工数量降序排序。
```

## 总结

通过使用标准化的提示词，我们可以快速生成高质量、易维护的SQL语句，提高开发效率。建议根据实际需求调整提示词，创建个人化的提示词模板，进一步提高工作效率。