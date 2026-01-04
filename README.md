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
| 模型专属     | [prompts/llm-specific/](prompts/llm-specific/) | 特定模型优化提示词 |
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