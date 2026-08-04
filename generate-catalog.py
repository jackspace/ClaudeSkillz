#!/usr/bin/env python3
"""Generate skills catalog for ClaudeSkillz"""

import json
import os
import re
from pathlib import Path


def parse_frontmatter(text):
    """Return the YAML frontmatter of a SKILL.md as a dict of str -> str.

    Only handles the small subset skills actually use: plain scalars, quoted
    strings, '|' block scalars, '>' folded scalars, and indented continuation
    lines. Good enough for name/description, and it never leaks a raw
    'key: value' line into the catalog the way line-scanning did.
    """
    m = re.match(r'^---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|$)', text, re.S)
    if not m:
        return {}

    fields = {}
    key = None
    buf = []
    folded = False

    def flush():
        if key is None:
            return
        joined = ' '.join(p.strip() for p in buf if p.strip()) if folded else '\n'.join(buf)
        fields[key] = joined.strip()

    for line in m.group(1).split('\n'):
        line = line.rstrip('\r')
        head = re.match(r'^([A-Za-z_][A-Za-z0-9_-]*):[ \t]*(.*)$', line)
        if head and not line.startswith((' ', '\t')):
            flush()
            key, rest = head.group(1), head.group(2).strip()
            if rest in ('|', '|-', '|+', '>', '>-', '>+'):
                buf, folded = [], rest.startswith('>')
            else:
                if len(rest) >= 2 and rest[0] == rest[-1] and rest[0] in '"\'':
                    rest = rest[1:-1]
                buf, folded = ([rest] if rest else []), True
        elif key is not None and (line.startswith((' ', '\t')) or not line.strip()):
            buf.append(line.strip() if folded else line.lstrip())
    flush()
    return fields


def generate_catalog():
    skills_dir = Path(__file__).parent / 'skills'
    catalog = []

    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue

        skill_name = skill_dir.name
        skill_json = skill_dir / 'SKILL.json'
        skill_md = skill_dir / 'SKILL.md'

        # SKILL.md frontmatter wins. It is what Claude Code actually loads, so
        # treating it as the single source of truth keeps an edit there from
        # being silently overridden by a stale SKILL.json copy.
        description = ""
        category = "General"
        content = ""

        if skill_md.exists():
            try:
                with open(skill_md, 'r', encoding='utf-8') as f:
                    content = f.read()
                description = parse_frontmatter(content).get('description', '').strip()
            except:
                pass

        if not description and skill_json.exists():
            try:
                with open(skill_json, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    description = data.get('description', '')
                    if not description and 'overview' in data:
                        description = data['overview']
                    # Some SKILL.json files carry a bare block-scalar marker
                    # instead of a description. Treat that as absent.
                    if str(description).strip() in ('|', '|-', '|+', '>', '>-', '>+', '---'):
                        description = ''
            except:
                pass

        if not description and content:
            # Nothing structured to work with, so fall back to the first real
            # paragraph of prose, skipping the heading and any block markers.
            try:
                body = re.sub(r'^---[ \t]*\r?\n.*?\r?\n---[ \t]*\r?\n', '', content, flags=re.S)
                for line in body.split('\n')[:30]:
                    line = line.strip()
                    if not line or line[0] in '|->#*`' or line.startswith('---'):
                        continue
                    if len(line) > 20:
                        description = line
                        break
            except:
                pass

        # Collapse whitespace so multi-line block scalars stay on one line.
        description = ' '.join(description.split())

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
