# ClaudeSkillz

> A curated collection of 260+ Claude Code skills for productivity, development, and automation

[![Skills](https://img.shields.io/badge/skills-261-blue)](https://claudeskillz.jackspace.com)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Website](https://img.shields.io/badge/website-claudeskillz.jackspace.com-purple)](https://claudeskillz.jackspace.com)

## What is ClaudeSkillz?

ClaudeSkillz is a professionally curated collection of Claude Code skills, carefully sanitized and ready for public use. These skills enhance Claude Code's capabilities across development, infrastructure, scientific computing, and automation tasks.

**Live Site**: [claudeskillz.jackspace.com](https://claudeskillz.jackspace.com)

## Quick Start

### Browse & Install Skills

Visit the **[Interactive Skill Selector](https://claudeskillz.jackspace.com)** to browse all 261 skills with filtering, search, and one-click installation.

### Manual Installation

1. **Navigate to your Claude Code skills directory:**
   ```bash
   cd ~/.claude/skills  # Linux/macOS
   # or
   cd %USERPROFILE%\.claude\skills  # Windows
   ```

2. **Clone a specific skill:**
   ```bash
   # Example: Install the Docker helper skill
   git clone https://github.com/jackspace/ClaudeSkillz.git temp-repo
   cp -r temp-repo/skills/docker-helper .
   rm -rf temp-repo
   ```

3. **Verify installation:**
   ```bash
   ls -la docker-helper/
   # Should see SKILL.md or SKILL.json
   ```

## Skill Categories

| Category | Count | Examples |
|----------|-------|----------|
| **Development Tools** | 80+ | Git workflows, testing, debugging, code review |
| **Cloud & Infrastructure** | 60+ | Cloudflare Workers, Docker, serverless, databases |
| **Scientific Computing** | 120+ | Bioinformatics, data science, machine learning |
| **Automation** | 40+ | Scripting, batch processing, workflow automation |
| **Documentation** | 20+ | PDF processing, markdown, technical writing |
| **Web Development** | 50+ | React, Next.js, Tailwind, authentication |

## Featured Skills

### Development
- `bash-script-helper` - Expert guidance for bash scripting and debugging
- `docker-helper` - Container management and Docker Compose optimization
- `git-workflow-helper` - Advanced Git workflows and branching strategies
- `code-review_mrgoonie` - Automated code review with technical rigor

### Cloud & Infrastructure
- `cloudflare-worker-base` - Serverless functions on Cloudflare's edge network
- `cloudflare-d1` - SQLite databases at the edge
- `cloudflare-r2` - S3-compatible object storage
- `devops_mrgoonie` - Deploy and manage cloud infrastructure

### Scientific & Data
- `scientific-pkg-biopython` - Bioinformatics tools and sequence analysis
- `scientific-pkg-scanpy` - Single-cell RNA-seq analysis
- `scientific-pkg-rdkit` - Cheminformatics and molecular modeling
- `scientific-db-pubmed-database` - PubMed literature search and analysis

### Automation & Productivity
- `context-manager` - Permanent memory storage for decisions and context
- `error-debugger` - Analyze errors and provide immediate fixes
- `project-planning` - Break down projects into actionable steps
- `session-launcher` - Quick session management and templates

## Installation Methods

### Method 1: Interactive Selector (Recommended)

1. Visit [claudeskillz.jackspace.com](https://claudeskillz.jackspace.com)
2. Browse and select skills
3. Click "Generate Install Script"
4. Run the downloaded PowerShell script

### Method 2: Bulk Clone

Clone the entire repository and copy skills you need:

```bash
git clone https://github.com/jackspace/ClaudeSkillz.git
cd ClaudeSkillz/skills

# Copy specific skills to Claude Code
cp -r docker-helper ~/.claude/skills/
cp -r bash-script-helper ~/.claude/skills/
```

### Method 3: Individual Skill

Download a single skill directly:

```bash
# Using curl
curl -L https://github.com/jackspace/ClaudeSkillz/archive/main.tar.gz | \
  tar xz --strip=2 ClaudeSkillz-main/skills/docker-helper

# Using wget
wget -O- https://github.com/jackspace/ClaudeSkillz/archive/main.tar.gz | \
  tar xz --strip=2 ClaudeSkillz-main/skills/docker-helper
```

## Skill Structure

Each skill follows a consistent structure:

```
skill-name/
├── SKILL.md          # Markdown format (human-readable)
├── SKILL.json        # JSON format (token-optimized)
└── README.md         # Optional: additional documentation
```

## Important Notes

### Placeholders

All credentials and personal information in examples are placeholders. Replace with your actual values:

- `YOUR_API_KEY_HERE` → Your actual API key
- `yourusername` → Your username
- `yourdomain.com` → Your domain
- `192.168.1.100` → Your actual IP address

### Security

- Never commit real credentials to version control
- Always use environment variables for sensitive data
- Review skills before installation
- Follow each skill's security guidelines

## Contributing

### Reporting Issues

Found a bug or have a suggestion? [Open an issue](https://github.com/jackspace/ClaudeSkillz/issues)

### Adding Skills

1. Fork this repository
2. Add your skill to `skills/`
3. Follow the skill structure guidelines
4. Ensure all credentials are placeholders
5. Submit a pull request

### Skill Guidelines

- Use clear, descriptive names
- Include comprehensive documentation
- Provide working examples (with placeholders)
- Test thoroughly before submitting
- Follow security best practices

## Building from Source

### Prerequisites

- Python 3.7+
- Git

### Generate Catalog

```bash
# Generate skills catalog JSON
python tools/generate-catalog.py

# Output: docs/skills-catalog.json
```

### Run Local Server

```bash
# Serve documentation locally
cd docs
python -m http.server 8000

# Visit: http://localhost:8000
```

## SkillSelector Features

The interactive selector includes:

- **Search** - Find skills by name or description
- **Category Filtering** - Filter by development, cloud, scientific, etc.
- **Multi-Select** - Choose multiple skills at once
- **Install Script** - Generate PowerShell installation script
- **Responsive Design** - Works on desktop and mobile
- **Ninite-Inspired UI** - Clean, intuitive interface

## License

MIT License - See [LICENSE](LICENSE) file for details

## Credits

### Skills Sources

Skills in this collection are sourced from:
- Community contributions
- Open source projects
- Professional developers
- Scientific researchers

### Acknowledgments

- [Claude Code](https://claude.com/claude-code) by Anthropic
- Community skill creators
- Open source contributors

## Support

- **Documentation**: [claudeskillz.jackspace.com](https://claudeskillz.jackspace.com)
- **Issues**: [GitHub Issues](https://github.com/jackspace/ClaudeSkillz/issues)
- **Discussions**: [GitHub Discussions](https://github.com/jackspace/ClaudeSkillz/discussions)

## Roadmap

- [ ] Skill testing framework
- [ ] Automated dependency detection
- [ ] Skill compatibility checker
- [ ] Version management
- [ ] Skill update notifications
- [ ] Community ratings and reviews

## Statistics

- **Total Skills**: 261
- **Categories**: 6 major categories
- **Contributors**: Growing community
- **License**: MIT (open source)
- **Update Frequency**: Regular additions and updates

---

**Made with ❤️ for the Claude Code community**

Visit [claudeskillz.jackspace.com](https://claudeskillz.jackspace.com) to get started!
