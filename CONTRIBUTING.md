# 贡献指南
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/your-username/prompt-library/pulls)

欢迎参与本仓库的提示词贡献！本指南旨在统一提示词格式，确保仓库内容高质量、易复用。

## 一、贡献前准备
1. Fork 本仓库到你的GitHub账号；
2. 克隆Fork后的仓库到本地：
   ```bash
   git clone https://github.com/你的用户名/prompt-library.git
   cd prompt-library
   ```
3. 创建特性分支（避免直接修改 main 分支）：
   ```bash
   git checkout -b feat/[提示词用途，如add-sql-null-prompt]
   ```

## 二、提示词编写规范

### 1. 格式要求
- 必须遵循 基础模板 编写，不得缺失「基础信息」「提示词正文」「使用示例」核心模块；
- 文件编码为 UTF-8，每行字符数≤80，代码块必须标注语言（如sql/python）；
- 禁止包含侵权、违法、敏感内容，禁止提交无实际用途的冗余提示词。

### 2. 文件命名规则
- 格式：[分类]-[核心用途]-v[版本号].md（全部小写，连字符分隔）；
- 示例：code-sql-null-filter-v1.0.md、general-text-summary-v1.0.md；
- 版本号遵循「语义化版本」：主版本。次版本。修订号（如 v1.0.1）。

### 3. 目录归属规则
- 通用场景 → prompts/general/；
- 代码生成 / 调试 → prompts/code/（按语言子分类，如 python/sql）；
- AI 绘画 → prompts/ai-art/；
- 模型专属 → prompts/llm-specific/；
- 无法归类的新场景 → 先提 Issue 确认分类。

## 三、提交与 PR 规范

### 1. Git 提交信息规范
遵循「Conventional Commits」，格式：
```
<类型>: <描述>
```

支持的类型：
- feat: 新增提示词（如feat: 添加SQL筛选NULL值提示词）；
- fix: 修复提示词错误（如fix: 修正Python提示词的代码语法）；
- docs: 更新文档（如docs: 完善贡献指南的PR流程）；
- refactor: 重构提示词格式（如refactor: 统一表格样式）；
- style: 仅格式调整（无内容变更，如style: 调整换行符）。

### 2. PR 提交流程
1. 本地提交后推送到你的 Fork 仓库：
   ```bash
   git add .
   git commit -m "feat: 添加SQL筛选NULL值提示词"
   git push origin feat/add-sql-null-prompt
   ```
2. 打开 GitHub，在原仓库发起 PR，标题格式与提交信息一致；
3. PR 描述中需说明：
   - 提示词适用场景；
   - 测试过的模型（如 GPT-4/Claude 3）；
   - 核心解决的问题。

### 3. PR 审核标准
- 格式符合模板要求；
- 示例真实有效，可复现；
- 无语法 / 逻辑错误；
- 目录 / 命名符合规则。

## 四、其他说明
- 若提交的是提示词优化（如补充示例 / 修复错误），需在 PR 中说明变更点；
- 首次贡献者可参考 示例提示词 对齐格式；
- 审核通过后会合并到 main 分支，重大更新会同步到 Releases；
- 如有疑问，可提 Issue 或在 Discussions 中交流。

## 五、版权说明
- 提交的提示词需为原创，或基于 MIT 协议复用的内容；
- 贡献的内容将默认采用仓库的 MIT 许可证（见 LICENSE 文件）。