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
                    content = f.read()
                    lines = content.split('\n')

                    # Look for description patterns
                    for i, line in enumerate(lines[:30]):
                        # Skip headers, code blocks, and YAML frontmatter
                        if line.startswith('#') or line.startswith('```') or line.startswith('---'):
                            continue

                        # Look for "Use when", "Use this", description patterns
                        if any(pattern in line.lower() for pattern in ['use when', 'use this', 'this skill']):
                            description = line.strip()
                            break

                        # Get first substantial paragraph (not just symbols/dashes)
                        if line.strip() and len(line.strip()) > 20 and not line.strip()[0] in '|->#*':
                            description = line.strip()
                            break
            except:
                pass

        # If still no description, generate from name
        if not description or description in ['|', '---', '>']:
            # Convert kebab-case to readable
            name_words = skill_name.replace('-', ' ').replace('_', ' ').title()
            description = f"Claude Code skill for {name_words}"

        # Determine category from name prefix and keywords
        if skill_name.startswith('scientific-'):
            category = 'Scientific'
        elif skill_name.startswith('cloudflare-') or 'cloudflare' in skill_name:
            category = 'Cloudflare'
        elif any(x in skill_name for x in ['ai-', 'openai', 'gemini', 'ml-', 'llm', 'embeddings', 'agents', 'multimodal']):
            category = 'AI/ML'
        elif any(x in skill_name for x in ['devops', 'docker', 'terraform', 'kubernetes', 'infrastructure']):
            category = 'DevOps'
        elif any(x in skill_name for x in ['react', 'nextjs', 'tailwind', 'web', 'frontend', 'svelte', 'vue']):
            category = 'Web Development'
        elif any(x in skill_name for x in ['git', 'github', 'testing', 'code', 'debug', 'review']):
            category = 'Development Tools'
        elif any(x in skill_name for x in ['bash', 'script', 'automation', 'workflow', 'playwright']):
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
