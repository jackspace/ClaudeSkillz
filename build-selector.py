#!/usr/bin/env python3
"""Build the enhanced skill selector with embedded data"""

import json
from pathlib import Path

# Read catalog
with open('docs/skills-catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

skills_js = json.dumps(catalog['skills'], ensure_ascii=False)

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ClaudeSkillz - Claude Code Skills Installer</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{
            background: #2c3e50;
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .header p {{ font-size: 1.1em; opacity: 0.9; }}
        .controls {{
            background: #34495e;
            padding: 15px 30px;
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            align-items: center;
        }}
        .search-box {{ flex: 1; min-width: 200px; }}
        .search-box input {{
            width: 100%;
            padding: 12px 20px;
            border: none;
            border-radius: 6px;
            font-size: 16px;
        }}
        .filter-buttons {{ display: flex; gap: 10px; flex-wrap: wrap; }}
        .filter-btn {{
            padding: 10px 20px;
            border: none;
            border-radius: 6px;
            background: #2c3e50;
            color: white;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.2s;
        }}
        .filter-btn:hover {{ background: #1a252f; }}
        .filter-btn.active {{ background: #3498db; }}
        .stats {{
            background: #f8f9fa;
            padding: 20px 30px;
            display: flex;
            justify-content: space-around;
            text-align: center;
            border-bottom: 2px solid #e9ecef;
        }}
        .stat {{ flex: 1; }}
        .stat-number {{ font-size: 2.5em; font-weight: bold; color: #3498db; }}
        .stat-label {{
            font-size: 0.9em;
            color: #7f8c8d;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .skills-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
            padding: 30px;
            max-height: 600px;
            overflow-y: auto;
        }}
        .skill-card {{
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            cursor: pointer;
            transition: all 0.2s;
            position: relative;
            background: white;
        }}
        .skill-card:hover {{
            border-color: #3498db;
            box-shadow: 0 4px 12px rgba(52,152,219,0.2);
        }}
        .skill-card.selected {{
            border-color: #3498db;
            background: #f0f8ff;
        }}
        .checkbox {{
            position: absolute;
            top: 15px;
            right: 15px;
            width: 24px;
            height: 24px;
            border: 2px solid #bdc3c7;
            border-radius: 4px;
            background: white;
        }}
        .skill-card.selected .checkbox {{
            background: #3498db;
            border-color: #3498db;
        }}
        .skill-card.selected .checkbox::after {{
            content: '✓';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: white;
            font-size: 16px;
            font-weight: bold;
        }}
        .skill-name {{
            font-size: 1.1em;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 10px;
            padding-right: 40px;
        }}
        .skill-description {{
            font-size: 0.9em;
            color: #7f8c8d;
            line-height: 1.5;
            margin-bottom: 10px;
        }}
        .skill-tags {{ display: flex; gap: 6px; flex-wrap: wrap; }}
        .tag {{
            background: #ecf0f1;
            color: #7f8c8d;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.75em;
            font-weight: 500;
        }}
        .actions {{
            background: #2c3e50;
            color: white;
            padding: 20px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
        }}
        .action-buttons {{ display: flex; gap: 15px; flex-wrap: wrap; }}
        .btn {{
            padding: 12px 30px;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.2s;
            font-weight: 500;
        }}
        .btn-secondary {{ background: #95a5a6; color: white; }}
        .btn-secondary:hover {{ background: #7f8c8d; }}
        .btn-primary {{
            background: #3498db;
            color: white;
            font-size: 18px;
            padding: 15px 40px;
        }}
        .btn-primary:hover {{ background: #2980b9; }}
        .btn-primary:disabled {{ background: #95a5a6; cursor: not-allowed; }}
        .os-selector {{ display: flex; gap: 10px; align-items: center; }}
        .os-label {{ font-weight: 500; }}
        .os-checkbox {{
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 8px 15px;
            background: #34495e;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .os-checkbox:hover {{ background: #2c3e50; }}
        .os-checkbox input[type="checkbox"] {{
            width: 18px;
            height: 18px;
            cursor: pointer;
        }}
        .script-preview {{
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 30px;
            max-height: 300px;
            overflow-y: auto;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 13px;
            line-height: 1.5;
            display: none;
        }}
        .script-preview.active {{ display: block; }}
        .script-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid #3e3e3e;
        }}
        .script-title {{ font-weight: 600; color: #569cd6; }}
        .copy-btn {{
            padding: 6px 15px;
            background: #0e639c;
            border: none;
            border-radius: 4px;
            color: white;
            cursor: pointer;
            font-size: 12px;
        }}
        .copy-btn:hover {{ background: #1177bb; }}
        .script-content {{ white-space: pre-wrap; word-wrap: break-word; }}
        .footer {{
            background: #34495e;
            color: white;
            padding: 20px 30px;
            text-align: center;
            font-size: 14px;
        }}
        .footer-links {{
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-bottom: 15px;
            flex-wrap: wrap;
        }}
        .footer-link {{
            color: #3498db;
            text-decoration: none;
            transition: color 0.2s;
        }}
        .footer-link:hover {{ color: #5dade2; }}
        .loading {{
            text-align: center;
            padding: 50px;
            font-size: 20px;
            color: #7f8c8d;
        }}
        @media (max-width: 768px) {{
            .skills-grid {{ grid-template-columns: 1fr; }}
            .controls {{ flex-direction: column; }}
            .stats {{ flex-direction: column; gap: 15px; }}
            .actions {{ flex-direction: column; }}
            .os-selector {{ flex-direction: column; align-items: flex-start; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>ClaudeSkillz</h1>
            <p>Select the skills you want to install</p>
        </div>
        <div class="controls">
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="Search skills...">
            </div>
            <div class="filter-buttons">
                <button class="filter-btn active" data-filter="all">All</button>
                <button class="filter-btn" data-filter="cloudflare">Cloudflare</button>
                <button class="filter-btn" data-filter="ai">AI/ML</button>
                <button class="filter-btn" data-filter="web">Web Dev</button>
                <button class="filter-btn" data-filter="devops">DevOps</button>
            </div>
        </div>
        <div class="stats">
            <div class="stat">
                <div class="stat-number" id="totalSkills">0</div>
                <div class="stat-label">Total Skills</div>
            </div>
            <div class="stat">
                <div class="stat-number" id="selectedCount">0</div>
                <div class="stat-label">Selected</div>
            </div>
            <div class="stat">
                <div class="stat-number" id="filteredSkills">0</div>
                <div class="stat-label">Showing</div>
            </div>
        </div>
        <div class="skills-grid" id="skillsGrid">
            <div class="loading">Loading skills...</div>
        </div>
        <div class="script-preview" id="scriptPreview">
            <div class="script-header">
                <span class="script-title" id="scriptTitle">Installation Script</span>
                <button class="copy-btn" onclick="copyScript()">Copy to Clipboard</button>
            </div>
            <div class="script-content" id="scriptContent"></div>
        </div>
        <div class="actions">
            <div class="action-buttons">
                <button class="btn btn-secondary" onclick="selectAll()">Select All</button>
                <button class="btn btn-secondary" onclick="deselectAll()">Deselect All</button>
            </div>
            <div class="os-selector">
                <span class="os-label">Target OS:</span>
                <label class="os-checkbox">
                    <input type="checkbox" id="osWindows" checked onchange="updateGenerateButton()">
                    <span>Windows</span>
                </label>
                <label class="os-checkbox">
                    <input type="checkbox" id="osLinux" onchange="updateGenerateButton()">
                    <span>Linux</span>
                </label>
                <label class="os-checkbox">
                    <input type="checkbox" id="osMacOS" onchange="updateGenerateButton()">
                    <span>macOS</span>
                </label>
            </div>
            <button class="btn btn-primary" onclick="generateInstallScript()" id="generateBtn" disabled>
                Generate Install Script
            </button>
        </div>
        <div class="footer">
            <div class="footer-links">
                <a href="https://github.com/jackspace/ClaudeSkillz" target="_blank" class="footer-link">GitHub Repository</a>
                <a href="https://github.com/jackspace/ClaudeSkillz/blob/master/CONTRIBUTING.md" target="_blank" class="footer-link">Contribute</a>
                <a href="https://github.com/jackspace/ClaudeSkillz/issues" target="_blank" class="footer-link">Report Issue</a>
            </div>
            <p>Powered by Claude Code Mastery Collective | Select skills and click "Generate Install Script" to download</p>
        </div>
    </div>
    <script src="selector.js"></script>
    <script>
        window.EMBEDDED_SKILLS = {skills_js};
        window.addEventListener('DOMContentLoaded', () => {{
            initializeSkills();
        }});
    </script>
</body>
</html>
'''

# Write the HTML
with open('docs/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"[OK] Enhanced index.html generated with {len(catalog['skills'])} skills!")
print("All improvements applied:")
print("  - OS selection (Windows/Linux/macOS) with multi-select")
print("  - Script preview with copy-to-clipboard")
print("  - GitHub links at bottom")
print("  - Removed 'Ninite style' text")
print("  - Fixed category filters (Cloudflare, AI/ML, DevOps)")
print("  - Added Contribute link")
print("  - Changed attribution to 'Claude Code Mastery Collective'")
print("  - Improved skill descriptions")
