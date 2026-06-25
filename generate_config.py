#!/usr/bin/env python3
"""
自動掃描HTML檔案，生成config.json
在Netlify build時自動執行
"""

import os
import json
import re
from pathlib import Path

def extract_metadata_from_html(filepath):
    """從HTML檔案中提取標題"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 提取title
        title_match = re.search(r'<title>([^<]+)</title>', content)
        if title_match:
            title = title_match.group(1).strip()
            # 清理標題
            if ' | ' in title:
                title = title.split(' | ')[0].strip()
            return title
        
        return None
    except Exception as e:
        print(f"Warning: Could not read {filepath}: {e}")
        return None

def extract_filename_title(filename):
    """從檔案名提取標題"""
    name = filename.replace('.html', '')
    # CamelCase轉空格
    name = re.sub(r'([A-Z])', r' \1', name).strip()
    # underscore轉空格
    name = name.replace('_', ' ')
    # 多空格合併
    name = ' '.join(name.split())
    return name

def generate_config(directory='.'):
    """掃描目錄，生成配置"""
    
    html_files = []
    
    # 掃描所有HTML檔案（除了index.html）
    for file in sorted(Path(directory).glob('*.html')):
        if file.name != 'index.html':
            html_files.append(file.name)
    
    if not html_files:
        print("⚠️  沒有找到任何HTML檔案")
        # 建立空config.json
        config = {'modules': []}
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        return
    
    # 預設的emoji和顏色循環
    icons = ['🎮', '🤖', '🚀', '🔐', '📊', '📚', '🔬', '🎨', '🌐', '⚡', '🎓', '💡']
    colors = ['color-blue', 'color-red', 'color-green', 'color-orange', 'color-purple', 'color-pink']
    
    modules = []
    
    for idx, html_file in enumerate(html_files):
        # 提取檔案名作為ID
        file_stem = Path(html_file).stem
        module_id = file_stem.lower().replace('_', '-').replace(' ', '-')
        
        # 嘗試從HTML的title提取，否則從檔案名
        title = extract_metadata_from_html(html_file)
        if not title:
            title = extract_filename_title(html_file)
        
        module = {
            'id': module_id,
            'title': title,
            'icon': icons[idx % len(icons)],
            'description': f'深度探究專題：{title}',
            'tags': ['探究', '自主學習'],
            'file': html_file,
            'color': colors[idx % len(colors)]
        }
        
        modules.append(module)
        print(f"✓ {html_file:45} → {title}")
    
    # 生成config.json
    config = {'modules': modules}
    
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 成功生成 config.json ({len(modules)} 個專題)")

if __name__ == '__main__':
    print("🔍 正在掃描HTML檔案...\n")
    generate_config()
