#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将曾佳目录下的文件转换为标准提示词格式的脚本
"""
import os
import re
from datetime import datetime

# 输入目录路径
INPUT_DIR = r"E:\AI\prompt-library\prompts\general\曾佳"
# 输出目录路径
OUTPUT_DIR = r"E:\AI\prompt-library\prompts\general\zengjia-standard"

# 确保输出目录存在
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# 项目类型映射
PROJECT_TYPES = {
    "pc重启前端": "pc-reboot-frontend",
    "pc重启后端": "pc-reboot-backend",
    "百川更新与推送": "baichuan-update-push",
    "能耗监测系统": "energy-monitoring",
    "金机异常报警信息投放": "gold-machine-alarm",
    "静电监测系统&报警信息看板": "static-monitoring-alarm"
}

# 基础提示词模板
PROMPT_TEMPLATE = """
# {title} - v1.0.0
> 简短描述：{description}

#### 1. 基础信息
| 字段         | 内容                          |
|--------------|-------------------------------|
| ID           | {id}                          |
| 适用模型     | GPT-4, Claude 3, 通义千问     |
| 难度等级     | 进阶                          |
| 创建时间     | {create_date}                 |
| 最后更新时间 | {update_date}                 |
| 作者         | prompt-library-contributors   |

#### 2. 核心用途
详细说明：
- 该提示词用于生成{project_type}相关的解决方案
- 适用于{application_scene}场景
- 相比普通提示词，包含了完整的需求分析和技术实现要求

#### 3. 提示词正文
> 遵循 ROLE-TASK-CONSTRAINT-OUTPUT 框架

### 角色
你是资深{role}，擅长{expertise}。

### 任务
请根据以下需求，设计{project_type}的解决方案，包括架构设计、功能实现和技术选型。

### 约束条件
1. 充分理解需求，确保方案符合业务逻辑
2. 技术选型合理，考虑性能、安全性和可扩展性
3. 输出格式需结构化，便于阅读和实施
4. 包含完整的功能实现和技术细节
5. 支持{tech_stack}技术栈

### 输出格式
```markdown
# {project_type}解决方案

## 1. 需求分析
{requirements_summary}

## 2. 架构设计

### 2.1 系统架构
- [架构描述]

### 2.2 技术选型
- [技术栈列表]

## 3. 功能实现

### 3.1 核心功能
- [核心功能列表]

### 3.2 辅助功能
- [辅助功能列表]

## 4. 性能优化
- [性能优化措施]

## 5. 部署方案
- [部署架构和步骤]
```

#### 4. 使用示例

##### 输入场景
请根据以上提示词，设计{project_type}的详细方案。

##### 输出结果
```markdown
# {project_type}解决方案

## 1. 需求分析
[需求分析内容]

## 2. 架构设计

### 2.1 系统架构
- [架构描述]

### 2.2 技术选型
- [技术栈列表]

## 3. 功能实现

### 3.1 核心功能
- [核心功能列表]

### 3.2 辅助功能
- [辅助功能列表]

## 4. 性能优化
- [性能优化措施]

## 5. 部署方案
- [部署架构和步骤]
```

#### 5. 注意事项
1. 需确保方案符合业务需求和技术规范
2. 考虑系统的可扩展性和可维护性
3. 注意数据安全性和隐私保护
4. 进行充分的测试和验证
5. 提供完整的文档和培训

#### 6. 变更日志
- v1.0.0 ({create_date})：初始版本，完成{project_type}提示词
"""

def get_file_content(file_path):
    """读取文件内容"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_requirements(file_content):
    """从文件内容中提取需求摘要"""
    # 简单提取前几行作为需求摘要
    lines = file_content.split('\n')
    requirements = []
    in_requirements = False
    for line in lines[:50]:  # 只处理前50行
        line = line.strip()
        if line.startswith('## 2. 功能需求') or line.startswith('### 2.1 核心功能'):
            in_requirements = True
        elif in_requirements and line.startswith('## 3.'):
            break
        if in_requirements and line:
            requirements.append(line)
    return '\n'.join(requirements)

def convert_file(file_path, project_dir, file_type):
    """转换单个文件"""
    # 获取文件内容
    content = get_file_content(file_path)
    
    # 提取项目类型
    project_type_zh = project_dir
    project_type = PROJECT_TYPES.get(project_type_zh, "unknown-project")
    
    # 提取标题
    title = re.search(r'^# (.*)$', content, re.MULTILINE)
    if title:
        title = title.group(1)
    else:
        title = f"{project_type_zh} - {file_type}"
    
    # 生成描述
    if file_type == "INITIAL_REQUIREMENTS":
        description = f"用于生成{project_type_zh}的初始需求分析和功能设计"
        role = "需求分析师"
        expertise = "需求分析和系统设计"
        application_scene = project_type_zh
    else:  # TECHNICAL_DOCUMENTATION
        description = f"用于生成{project_type_zh}的技术实现方案"
        role = "系统架构师"
        expertise = "系统架构设计和技术实现"
        application_scene = project_type_zh
    
    # 生成ID
    id = f"prompt-general-{project_type}-{'req' if file_type == 'INITIAL_REQUIREMENTS' else 'tech'}-001"
    
    # 生成日期
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 提取需求摘要
    requirements_summary = extract_requirements(content)
    
    # 技术栈
    tech_stack = "Node.js + Express.js + MySQL + HTML5 + Bootstrap + JavaScript"
    
    # 生成提示词内容
    prompt_content = PROMPT_TEMPLATE.format(
        title=title,
        description=description,
        id=id,
        project_type=project_type_zh,
        application_scene=application_scene,
        role=role,
        expertise=expertise,
        tech_stack=tech_stack,
        requirements_summary=requirements_summary,
        create_date=today,
        update_date=today
    )
    
    # 生成输出文件名
    output_filename = f"general-{project_type}-{'requirements' if file_type == 'INITIAL_REQUIREMENTS' else 'tech'}-v1.0.md"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    
    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(prompt_content)
    
    print(f"转换完成: {output_path}")

def main():
    """主函数"""
    # 遍历所有子目录
    for root, dirs, files in os.walk(INPUT_DIR):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                # 获取项目目录名称
                project_dir = os.path.basename(root)
                # 获取文件类型
                file_type = os.path.splitext(file)[0]
                # 转换文件
                convert_file(file_path, project_dir, file_type)
    
    print("\n所有文件转换完成！")

if __name__ == "__main__":
    main()
