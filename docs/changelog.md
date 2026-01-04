# 更新日志

## 版本更新遵循「语义化版本」规范：主版本.次版本.修订号

## v1.0.0 (2026-01-04)

### 初始化版本

- 完成基础目录结构搭建
- 创建核心模板文件：
  - `templates/base-prompt-template.md`：提示词基础模板
  - `CONTRIBUTING.md`：贡献指南
  - `LICENSE`：MIT许可证
  - `README.md`：仓库总览
- 完善文档体系：
  - `docs/guidelines.md`：提示词编写指南
  - `docs/faq.md`：常见问题
  - `docs/changelog.md`：更新日志
- 新增示例提示词：
  - `prompts/general/general-text-summary-v1.0.md`：通用文本总结示例
  - `prompts/code/code-sql-null-filter-v1.0.md`：SQL筛选NULL值示例
- 添加提示词格式校验脚本：
  - `scripts/validate-prompt.py`：简单版格式校验工具

## v0.1.0 (2025-12-31)

### 预览版本

- 完成仓库架构设计
- 创建基础模板文件
- 测试提示词格式校验脚本

## 待规划功能

### v1.1.0
- 新增AI绘画提示词分类
- 添加模型专属提示词目录
- 完善提示词格式校验脚本，支持更多校验规则
- 添加自动化测试流程

### v1.2.0
- 新增多语言支持（英文提示词）
- 添加提示词效果评估机制
- 创建提示词最佳实践文档
- 支持提示词标签系统

### v2.0.0
- 重构目录结构，支持更细粒度的分类
- 开发提示词管理工具（Web界面）
- 支持提示词版本对比功能
- 添加AI自动生成提示词的辅助工具

## 变更说明规范

### 类型说明
- **feat**：新增功能或提示词
- **fix**：修复错误
- **docs**：更新文档
- **refactor**：重构代码或格式
- **style**：仅格式调整
- **test**：添加或更新测试
- **chore**：构建过程或辅助工具的变动

### 示例
```
## v1.0.0 (2026-01-04)

### feat
- 新增SQL筛选NULL值提示词
- 添加通用文本总结提示词

### docs
- 完善提示词编写指南
- 更新贡献指南

### fix
- 修复提示词模板中的语法错误

### refactor
- 统一提示词格式
```

## 更新频率

- 每周至少更新一次
- 重大功能更新会同步发布Release版本
- 修复bug会及时更新

## 如何获取更新

1. **Star/Watch仓库**：在GitHub上Star或Watch本仓库，接收更新通知
2. **定期查看**：定期访问本文件查看最新更新
3. **关注Releases**：关注仓库的Releases页面，获取稳定版本

## 历史版本归档

所有历史版本都会在GitHub Releases页面归档，包含完整的更新日志和源代码包。

## 贡献者名单

感谢以下贡献者对本仓库的支持：

- [contributor1](https://github.com/contributor1)：初始化仓库架构
- [contributor2](https://github.com/contributor2)：编写提示词模板
- [contributor3](https://github.com/contributor3)：完善文档体系

（按贡献时间排序，欢迎加入我们！）