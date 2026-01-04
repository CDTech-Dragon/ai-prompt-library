# 一、标准化提示词仓库骨架（可直接复制创建目录 / 文件）
先给出完整的仓库目录结构，你可在本地 / GitHub 上按此创建：
-----------------------------------------------------------------------
prompt-library/
├── README.md                # 仓库总览（下方附完整内容）
├── CONTRIBUTING.md          # 贡献规范（下方附完整模板）
├── LICENSE                  # MIT许可证（下方附内容）
├── docs/
│   ├── guidelines.md        # 提示词编写指南（附模板）
│   ├── faq.md               # 常见问题（附模板）
│   └── changelog.md         # 更新日志（附模板）
├── templates/
│   └── base-prompt-template.md  # 核心提示词模板（附完整内容）
├── prompts/
│   ├── general/             # 通用场景示例
│   │   └── general-text-summary-v1.0.md  # 文本总结示例
│   ├── code/                # 代码场景示例
│   │   └── code-sql-null-filter-v1.0.md  # SQL筛选NULL示例
│   └── ai-art/              # AI绘画占位目录
├── examples/
│   └── code-sql-usage-example.md  # 提示词使用示例
└── scripts/
    └── validate-prompt.py   # 提示词格式校验脚本（简单版）
-----------------------------------------------------------------------
# 二、核心模板文件（可直接复制）

## 1. templates/base-prompt-template.md（提示词基础模板）
-----------------------------------------------------------------------
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
------------------------------------------------------------------------

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
-------------------------------------------------------------------------
-- 筛选NULL的语句
SELECT * FROM [表名] WHERE [字段名] IS NULL;

-- 筛选非NULL的语句
SELECT * FROM [表名] WHERE [字段名] IS NOT NULL;
```]
-------------------------------------------------------------------------
## 4. 使用示例
输入场景
[用户实际需求示例，如「从 improvement_records 表中筛选 A2_improver 字段为 NULL 的所有记录」]
输出结果
[AI 实际返回的结果示例，如：
---------------------------------------------------------------------------------------
SELECT * FROM improvement_records WHERE A2_improver IS NULL;
```]

## 5. 注意事项
1. [使用该提示词的坑点，如「SQL中NULL不能用=判断，必须用IS NULL」]
2. [跨模型适配说明，如「Claude/通义千问使用该提示词无需修改，Midjourney不适用」]
3. [扩展用法，如「如需筛选多个NULL字段，可叠加 AND 条件」]

## 6. 变更日志
- v[版本号]（YYYY-MM-DD）：[变更说明，如「初始版本，完成基础SQL NULL筛选提示词」]
- v[版本号]（YYYY-MM-DD）：[变更说明，如「补充PostgreSQL适配说明」]
----------------------------------------------------------------------------------------
#### 4. 使用示例
输入场景
[用户实际需求示例，如「从 improvement_records 表中筛选 A2_improver 字段为 NULL 的所有记录」]
输出结果
[AI 实际返回的结果示例，如：

-----------------------------------------------------------------------------------------
SELECT * FROM improvement_records WHERE A2_improver IS NULL;
```]

## 5. 注意事项
1. [使用该提示词的坑点，如「SQL中NULL不能用=判断，必须用IS NULL」]
2. [跨模型适配说明，如「Claude/通义千问使用该提示词无需修改，Midjourney不适用」]
3. [扩展用法，如「如需筛选多个NULL字段，可叠加 AND 条件」]

## 6. 变更日志
- v[版本号]（YYYY-MM-DD）：[变更说明，如「初始版本，完成基础SQL NULL筛选提示词」]
- v[版本号]（YYYY-MM-DD）：[变更说明，如「补充PostgreSQL适配说明」]
----------------------------------------------------------------------------------------
## 2. CONTRIBUTING.md（完整贡献规范模板）
----------------------------------------------------------------------------------------
# 贡献指南
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/your-username/prompt-library/pulls)

欢迎参与本仓库的提示词贡献！本指南旨在统一提示词格式，确保仓库内容高质量、易复用。

## 一、贡献前准备
1. Fork 本仓库到你的GitHub账号；
2. 克隆Fork后的仓库到本地：
   ```bash
   git clone https://github.com/你的用户名/prompt-library.git
   cd prompt-library
-----------------------------------------------------------------------------------------
## 3.创建特性分支（避免直接修改 main 分支）：
-----------------------------------------------------------------------------------------
git checkout -b feat/[提示词用途，如add-sql-null-prompt]
-----------------------------------------------------------------------------------------

# 二、提示词编写规范
#### 1. 格式要求
必须遵循 基础模板 编写，不得缺失「基础信息」「提示词正文」「使用示例」核心模块；
文件编码为 UTF-8，每行字符数≤80，代码块必须标注语言（如sql/python）；
禁止包含侵权、违法、敏感内容，禁止提交无实际用途的冗余提示词。
#### 2. 文件命名规则
格式：[分类]-[核心用途]-v[版本号].md（全部小写，连字符分隔）；
示例：code-sql-null-filter-v1.0.md、general-text-summary-v1.0.md；
版本号遵循「语义化版本」：主版本。次版本。修订号（如 v1.0.1）。
#### 3. 目录归属规则
通用场景 → prompts/general/；
代码生成 / 调试 → prompts/code/（按语言子分类，如 python/sql）；
AI 绘画 → prompts/ai-art/；
模型专属 → prompts/llm-specific/；
无法归类的新场景 → 先提 Issue 确认分类。
# 三、提交与 PR 规范
#### 1. Git 提交信息规范
遵循「Conventional Commits」，格式：
---------------------------------------------------------------------------------------
plaintext
<类型>: <描述>
---------------------------------------------------------------------------------------

支持的类型：
feat: 新增提示词（如feat: 添加SQL筛选NULL值提示词）；
fix: 修复提示词错误（如fix: 修正Python提示词的代码语法）；
docs: 更新文档（如docs: 完善贡献指南的PR流程）；
refactor: 重构提示词格式（如refactor: 统一表格样式）；
style: 仅格式调整（无内容变更，如style: 调整换行符）。
#### 2. PR 提交流程
本地提交后推送到你的 Fork 仓库：
--------------------------------------------------------------------------------------
git add .
git commit -m "feat: 添加SQL筛选NULL值提示词"
git push origin feat/add-sql-null-prompt
--------------------------------------------------------------------------------------
打开 GitHub，在原仓库发起 PR，标题格式与提交信息一致；
PR 描述中需说明：
提示词适用场景；
测试过的模型（如 GPT-4/Claude 3）；
核心解决的问题。
#### 3. PR 审核标准
格式符合模板要求；
示例真实有效，可复现；
无语法 / 逻辑错误；
目录 / 命名符合规则。

# 四、其他说明
若提交的是提示词优化（如补充示例 / 修复错误），需在 PR 中说明变更点；
首次贡献者可参考 示例提示词 对齐格式；
审核通过后会合并到 main 分支，重大更新会同步到 Releases；
如有疑问，可提 Issue 或在 Discussions 中交流。

# 五、版权说明
提交的提示词需为原创，或基于 MIT 协议复用的内容；
贡献的内容将默认采用仓库的 MIT 许可证（见 LICENSE 文件）。
---------------------------------------------------------------------------------------


### 三、仓库配套核心文件（可直接复制）
#### 1. README.md（仓库总览）
```markdown
# Prompt Library - 标准化提示词库
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Update Frequency](https://img.shields.io/badge/update-weekly-green.svg)](docs/changelog.md)

## 仓库简介
本仓库整理了面向主流AI模型（GPT-4/Claude 3/通义千问/Midjourney等）的标准化提示词，覆盖代码生成、文本处理、AI绘画等场景。所有提示词遵循统一编写规范，可直接复制复用，也支持按需微调。

## 快速导航
| 分类         | 目录                          | 核心场景                  |
|--------------|-------------------------------|---------------------------|
| 通用提示词   | [prompts/general/](prompts/general/) | 文本总结、翻译、问答      |
| 代码提示词   | [prompts/code/](prompts/code/)       | SQL编写、Python调试、前端开发 |
| AI绘画提示词 | [prompts/ai-art/](prompts/ai-art/)   | Midjourney/Stable Diffusion |
| 编写指南     | [docs/guidelines.md](docs/guidelines.md) | 如何编写标准化提示词      |

## 使用方法
1. 进入对应分类目录，选择所需提示词文件（如`code-sql-null-filter-v1.0.md`）；
2. 复制「提示词正文」模块的内容；
3. 替换占位符（如表名/字段名），粘贴到AI模型对话框中执行。

## 贡献指南
欢迎提交符合规范的提示词，详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可证
本仓库采用 [MIT许可证](LICENSE)，你可自由复用、修改提示词（注明来源即可）。

## 常见问题
见 [FAQ](docs/faq.md)，如有其他问题可提Issue交流。
----------------------------------------------------------------------------------------
#### 2. LICENSE（MIT 许可证）
----------------------------------------------------------------------------------------
MIT License

Copyright (c) [年份] [你的名字/组织名]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
------------------------------------------------------------------------------------------
#### 3. docs/guidelines.md（提示词编写指南）
------------------------------------------------------------------------------------------
# 提示词编写指南
## 核心原则
1. 清晰性：明确角色、任务、约束，避免模糊表述；
2. 可复用性：通用部分固化，个性化部分用占位符标注；
3. 适配性：注明适用模型，跨模型差异需补充说明；
4. 可验证性：提供真实使用示例，确保效果可复现。

## 框架推荐
### ROLE-TASK-CONSTRAINT-OUTPUT 框架
- **ROLE（角色）**：定义AI的身份（如「资深SQL工程师」「产品经理」）；
- **TASK（任务）**：明确要完成的核心目标（避免歧义）；
- **CONSTRAINT（约束）**：技术/格式/风格约束；
- **OUTPUT（输出）**：指定输出结构/格式。

### 示例
------------------------------------------------------------------------------------------
角色：你是资深 MySQL 工程师，熟悉电商业务场景任务：编写 SQL 语句，统计近 7 天每个商品的下单量（去重）约束：
兼容 MySQL 8.0+
输出包含注释，解释分组 / 过滤逻辑
处理 NULL 值（下单量为 0 的商品也要显示）
输出格式：

--------------------------
sql^

-- 近7天商品下单量统计
SELECT 
  goods_id,
  COUNT(DISTINCT order_id) AS order_count
FROM order_table
WHERE create_time >= DATE_SUB(NOW(), INTERVAL 7 DAY)
GROUP BY goods_id
ORDER BY order_count DESC;
--------------------------

--------------------------
plaintext^
--------------------------

## 避坑指南
1. 避免使用「帮我写一个SQL」这类模糊表述，需明确场景；
2. SQL类提示词需注明数据库类型（MySQL/PostgreSQL/Oracle）；
3. AI绘画提示词需区分模型（Midjourney/Stable Diffusion），标注权重/参数；
4. 不要包含敏感信息（如手机号、密钥），用占位符替代。
--------------------------
#### 4. docs/faq.md（常见问题）
 
----------------------------------------------------------------------------------------------
markdown^

# 常见问题
## 使用类
### Q1：提示词在不同模型中效果不一致怎么办？
A1：参考提示词文件中的「注意事项」，不同模型的适配规则已标注；若未标注，可提Issue补充。

### Q2：如何快速找到所需的提示词？
A2：可通过README的「快速导航」进入分类，或使用GitHub的仓库搜索功能（快捷键`t`）。

## 贡献类
### Q3：提交的PR被驳回了怎么办？
A3：查看PR评论中的驳回原因，按规范调整后重新提交即可；若有疑问可直接回复评论交流。

### Q4：新增的提示词场景没有对应分类怎么办？
A4：先提Issue说明场景，维护者确认后会创建新分类，再按新分类提交。

## 其他
### Q5：可以商用仓库中的提示词吗？
A5：可以，本仓库采用MIT许可证，商用时注明来源即可。
----------------------------------------------------------------------------------------------

#### 5. docs/changelog.md（更新日志）
----------------------------------------------------------------------------------------------
markdown^

# 更新日志
## v1.0.0（YYYY-MM-DD）
- 初始化仓库，完成基础目录结构搭建；
- 新增「通用文本总结」「SQL筛选NULL值」2个示例提示词；
- 完善README、CONTRIBUTING、LICENSE核心文档。

## 待更新
- 新增AI绘画（Midjourney）提示词分类；
- 补充Python代码调试类提示词；
- 增加提示词格式校验CI/CD流程。

----------------------------------------------------------------------------------------------
#### 6. scripts/validate-prompt.py（简单校验脚本）

----------------------------------------------------------------------------------------------
python^

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提示词格式校验脚本：检查是否包含核心模块、编码是否为UTF-8
"""
import os
import chardet

# 要校验的提示词目录
PROMPT_DIR = "./prompts/"
# 必须包含的核心模块
REQUIRED_SECTIONS = ["1. 基础信息", "3. 提示词正文", "4. 使用示例"]

def check_file_encoding(file_path):
    """检查文件编码是否为UTF-8"""
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding'] == 'utf-8'

def check_prompt_sections(file_path):
    """检查是否包含核心模块"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    missing_sections = []
    for section in REQUIRED_SECTIONS:
        if section not in content:
            missing_sections.append(section)
    return missing_sections

def main():
    for root, dirs, files in os.walk(PROMPT_DIR):
        for file in files:
            if not file.endswith('.md'):
                continue
            file_path = os.path.join(root, file)
            print(f"校验文件：{file_path}")
            
            # 检查编码
            if not check_file_encoding(file_path):
                print(f"❌ 错误：文件编码非UTF-8")
                continue
            
            # 检查核心模块
            missing = check_prompt_sections(file_path)
            if missing:
                print(f"❌ 错误：缺失核心模块 → {', '.join(missing)}")
            else:
                print("✅ 校验通过")
            print("-" * 50)

if __name__ == "__main__":
    main()

---------------------------------------------------------------------------------
## 四、快速搭建仓库的步骤
1.本地创建目录：按最上方的仓库骨架，在本地新建文件夹prompt-library，并创建对应子目录（docs/templates/prompts 等）；
2.创建文件：将上述模板内容分别复制到对应文件中（替换占位符，如[你的用户名]/[年份]）；
3.初始化 Git 仓库：
---------------------------------------------------------------------------------
bash^

cd prompt-library
git init
git add .
git commit -m "feat: 初始化标准化提示词仓库"

---------------------------------------------------------------------------------
4.推送到 GitHub：
在 GitHub 创建空仓库prompt-library；
关联远程仓库并推送：

---------------------------------------------------------------------------------
bash^
git remote add origin https://github.com/你的用户名/prompt-library.git
git push -u origin main

--------------------------------------------------------------------------------
