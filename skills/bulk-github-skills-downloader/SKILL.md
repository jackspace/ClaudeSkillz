# Bulk GitHub Skills Downloader

Expert skill for downloading and consolidating Claude Code skills from multiple GitHub repositories efficiently.

## Purpose
Automate the process of discovering, downloading, and organizing Claude Code skills from GitHub repositories at scale. This skill handles repository cloning, skill extraction, directory flattening, and organization.

## When to Use
- Downloading skills from multiple GitHub repositories
- Building a comprehensive skills collection
- Updating existing skill collections with new repositories
- Performing batch downloads of skills from curated lists

## Capabilities

### 1. Repository Discovery
- Search GitHub for "claude skills" repositories
- Parse curated lists (like awesome-claude-skills)
- Filter by stars, activity, and relevance
- Identify actual skill repositories vs. meta-repositories

### 2. Batch Download
- Clone multiple repositories in parallel
- Handle rate limiting and authentication
- Resume interrupted downloads
- Skip already-downloaded repositories

### 3. Skill Extraction
- Locate skills in various directory structures:
  - `/.claude/skills/`
  - `/skills/`
  - `/`
- Extract skills from nested directory structures
- Preserve skill metadata and structure

### 4. Organization
- Flatten nested directories to `/skills/` root
- Add source suffixes to prevent naming conflicts
- Create source attribution metadata
- Generate inventory documentation

## Usage Instructions

### Basic Batch Download
```
Use the bulk-github-skills-downloader skill to download skills from:
- obra/superpowers
- diet103/claude-code-infrastructure-showcase
- mrgoonie/claudekit-skills

Organize them in /skills with source suffixes.
```

### Download from Awesome List
```
Use the bulk-github-skills-downloader skill to:
1. Parse the BehiSecc/awesome-claude-skills repository
2. Download all listed skill repositories
3. Organize and document them
```

### Update Existing Collection
```
Use the bulk-github-skills-downloader skill to update my collection with:
- Any new repositories with 100+ stars
- Skills from the last 30 days
- Skip repositories I already have
```

## Key Features

### Parallel Processing
- Clone multiple repositories simultaneously
- Efficient resource utilization
- Configurable concurrency limits

### Smart Filtering
- Detect meta-repositories (lists, tools, converters)
- Identify actual skill collections
- Skip archived or inactive repositories
- Filter by license compatibility

### Error Handling
- Retry failed downloads
- Log errors with context
- Continue on partial failures
- Generate error reports

### Attribution Tracking
- Record source repository URLs
- Preserve LICENSE files
- Track author information
- Generate attribution documentation

## Workflow

1. **Discovery Phase**
   - Search GitHub or parse curated list
   - Filter and prioritize repositories
   - Check for existing downloads

2. **Download Phase**
   - Clone repositories to /tmp
   - Verify skill presence
   - Extract skill directories

3. **Organization Phase**
   - Flatten directory structure
   - Add source suffixes
   - Move to /skills directory
   - Preserve metadata

4. **Documentation Phase**
   - Generate inventory
   - Create attribution file
   - Update main README
   - Log statistics

## Repository Detection Logic

### Actual Skill Repositories
✅ Contains `/.claude/skills/` or `/skills/` directories
✅ Has individual skill folders with SKILL.md files
✅ Primary content is skills

### Meta-Repositories (Skip)
❌ Curated lists (awesome-* pattern)
❌ Converter tools (documentation → skills)
❌ Frameworks or libraries
❌ Archived repositories

## Directory Structure After Download

```
/skills/
├── skill-name_source/          # Individual skills with source suffix
│   ├── SKILL.md
│   └── ...
├── another-skill_source/
│   └── ...
└── ...
```

## Configuration Options

### Concurrency
```yaml
max_parallel_clones: 5
max_parallel_extractions: 10
```

### Filtering
```yaml
min_stars: 50
max_age_days: 365
include_archived: false
license_types:
  - MIT
  - Apache-2.0
  - BSD
```

### Organization
```yaml
flatten_skills: true
add_source_suffix: true
preserve_metadata: true
cleanup_temp: true
```

## Output

### Success Message
```
Successfully downloaded 154 skills from 5 repositories:
- obra/superpowers: 21 skills
- diet103/claude-code-infrastructure-showcase: 5 skills
- lackeyjb/playwright-skill: 1 skill
- mrgoonie/claudekit-skills: 22 skills
- K-Dense-AI/claude-scientific-skills: 105 skills

Skills organized in /skills/
Documentation generated in SKILLS_COLLECTION_README.md
```

### Error Handling
- Log failed repositories
- Continue with successful downloads
- Generate error report
- Suggest manual intervention if needed

## Best Practices

1. **Authentication**: Use GitHub token for higher rate limits
2. **Incremental Updates**: Download new repositories only
3. **Verification**: Check skill structure after download
4. **Attribution**: Always preserve license and author info
5. **Cleanup**: Remove temporary files after extraction

## Integration with Other Skills

### Works Well With
- `skills-duplicate-detector`: Identify duplicate skills
- `skills-consolidator`: Merge and organize downloaded skills
- `git-workflow-helper`: Commit and push changes
- `github-auth`: Handle authentication

## Performance

- **Typical Speed**: 5-10 repositories per minute
- **Parallel Clones**: Up to 5 simultaneous
- **Network**: Depends on repository size
- **Disk Space**: ~100MB per large repository

## Error Recovery

### Network Failures
- Automatic retry with exponential backoff
- Resume from last successful download
- Log failed repositories for manual review

### Permission Issues
- Check GitHub authentication
- Verify write permissions
- Handle rate limiting gracefully

## Advanced Usage

### Custom Repository List
```
Download skills from these repositories:
- https://github.com/user1/repo1
- https://github.com/user2/repo2

Skip repositories marked as:
- archived
- forks
- less than 10 stars
```

### Selective Download
```
Download only skills related to:
- Python development
- Scientific computing
- Database management

From the top 20 claude-skills repositories.
```

## Maintenance

This skill should be updated when:
- New popular skill repositories emerge
- GitHub API changes
- Directory structure patterns change
- New skill metadata standards are adopted

---

**Version**: 1.0.0
**Last Updated**: 2025-11-07
**Maintained by**: @yourusername
