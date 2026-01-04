#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提示词格式校验脚本：检查是否包含核心模块、编码是否为UTF-8
"""
import os
import chardet
import argparse

# 要校验的提示词目录默认值
DEFAULT_PROMPT_DIR = "./prompts/"

# 必须包含的核心模块
REQUIRED_SECTIONS = [
    "1. 基础信息",
    "2. 核心用途",
    "3. 提示词正文",
    "4. 使用示例"
]

# 文件命名规则正则表达式（简化版）
# 格式：[分类]-[核心用途]-v[版本号].md
# 示例：code-sql-null-filter-v1.0.md
def is_valid_filename(filename):
    """检查文件名是否符合规范"""
    if not filename.endswith('.md'):
        return False
    
    parts = filename[:-3].split('-')  # 移除.md后缀并分割
    if len(parts) < 4:
        return False
    
    # 检查是否包含版本号
    version_part = parts[-1]
    if not version_part.startswith('v'):
        return False
    
    # 检查版本号格式（vX.X或vX.X.X）
    version_numbers = version_part[1:].split('.')
    if len(version_numbers) not in [2, 3]:
        return False
    
    # 检查版本号是否为数字
    for num in version_numbers:
        if not num.isdigit():
            return False
    
    return True

def check_file_encoding(file_path):
    """检查文件编码是否为UTF-8"""
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding'] == 'utf-8', result['encoding']

def check_prompt_sections(file_path):
    """检查是否包含核心模块"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    missing_sections = []
    for section in REQUIRED_SECTIONS:
        if section not in content:
            missing_sections.append(section)
    
    return missing_sections

def check_yaml_frontmatter(file_path):
    """检查是否包含YAML Front Matter（可选）"""
    with open(file_path, 'r', encoding='utf-8') as f:
        first_line = f.readline().strip()
    return first_line == '---'

def main():
    parser = argparse.ArgumentParser(description="提示词格式校验脚本")
    parser.add_argument(
        "--dir", 
        type=str, 
        default=DEFAULT_PROMPT_DIR, 
        help=f"提示词目录路径，默认: {DEFAULT_PROMPT_DIR}"
    )
    parser.add_argument(
        "--verbose", 
        action="store_true", 
        help="显示详细校验信息"
    )
    args = parser.parse_args()
    
    prompt_dir = args.dir
    verbose = args.verbose
    
    print(f"\n开始校验提示词目录: {prompt_dir}")
    print("=" * 60)
    
    total_files = 0
    valid_files = 0
    invalid_files = 0
    
    for root, dirs, files in os.walk(prompt_dir):
        for file in files:
            if not file.endswith('.md'):
                continue
            
            total_files += 1
            file_path = os.path.join(root, file)
            
            if verbose:
                print(f"\n校验文件：{file_path}")
                print("-" * 40)
            
            # 检查文件名
            filename_valid = is_valid_filename(file)
            
            # 检查编码
            encoding_valid, actual_encoding = check_file_encoding(file_path)
            
            # 检查核心模块
            missing_sections = check_prompt_sections(file_path)
            sections_valid = len(missing_sections) == 0
            
            # 综合判断
            is_valid = filename_valid and encoding_valid and sections_valid
            
            if is_valid:
                valid_files += 1
                if verbose:
                    print(f"✅ 校验通过")
            else:
                invalid_files += 1
                if verbose:
                    print(f"❌ 校验失败")
                    if not filename_valid:
                        print(f"   - 文件名格式错误：{file}")
                    if not encoding_valid:
                        print(f"   - 文件编码错误：{actual_encoding}，应为UTF-8")
                    if not sections_valid:
                        print(f"   - 缺失核心模块：{', '.join(missing_sections)}")
            
            if verbose:
                print("-" * 40)
    
    print("=" * 60)
    print(f"校验完成：")
    print(f"  总文件数：{total_files}")
    print(f"  有效文件：{valid_files}")
    print(f"  无效文件：{invalid_files}")
    print(f"  有效率：{valid_files / total_files * 100:.1f}%" if total_files > 0 else "  有效率：0%")
    print("=" * 60)
    
    if invalid_files > 0:
        print(f"\n存在 {invalid_files} 个无效文件，请检查并修复。")
        return 1
    else:
        print(f"\n所有文件校验通过！")
        return 0

if __name__ == "__main__":
    exit(main())