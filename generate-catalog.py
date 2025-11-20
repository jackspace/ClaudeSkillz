#!/usr/bin/env python3
"""Generate skills catalog for ClaudeSkillz"""

import json
import os
from pathlib import Path

def generate_catalog():
    skills_dir = Path(__file__).parent / 'skills'
    catalog = []

    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue

        skill_name = skill_dir.name
        skill_json = skill_dir / 'SKILL.json'
        skill_md = skill_dir / 'SKILL.md'

        # Try to read from JSON first, then MD
        description = ""
        category = "General"

        if skill_json.exists():
            try:
                with open(skill_json, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    description = data.get('description', '')
                    if not description and 'overview' in data:
                        description = data['overview']
            except:
                pass

        if not description and skill_md.exists():
            try:
                with open(skill_md, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    # Look for description in first 20 lines
                    for line in lines[:20]:
                        if line.strip() and not line.startswith('#') and not line.startswith('```'):
                            description = line.strip()
                            break
            except:
                pass

        # Determine category from name prefix
        if skill_name.startswith('scientific-'):
            category = 'Scientific'
        elif skill_name.startswith('cloudflare-'):
            category = 'Cloud & Infrastructure'
        elif any(x in skill_name for x in ['docker', 'devops', 'terraform', 'kubernetes']):
            category = 'Infrastructure'
        elif any(x in skill_name for x in ['react', 'nextjs', 'tailwind', 'web', 'frontend']):
            category = 'Web Development'
        elif any(x in skill_name for x in ['git', 'github', 'testing', 'code', 'debug']):
            category = 'Development Tools'
        elif any(x in skill_name for x in ['bash', 'script', 'automation', 'workflow']):
            category = 'Automation'

        catalog.append({
            'name': skill_name,
            'description': description[:200] if description else f"Claude Code skill: {skill_name}",
            'category': category
        })

    # Save catalog
    docs_dir = Path(__file__).parent / 'docs'
    docs_dir.mkdir(exist_ok=True)

    with open(docs_dir / 'skills-catalog.json', 'w', encoding='utf-8') as f:
        json.dump({'skills': catalog}, f, indent=2)

    print(f"Generated catalog with {len(catalog)} skills")
    print(f"Output: {docs_dir / 'skills-catalog.json'}")

    return catalog

if __name__ == '__main__':
    catalog = generate_catalog()
