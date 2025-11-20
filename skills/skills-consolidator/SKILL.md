# Skills Consolidator

Expert skill for merging, organizing, and maintaining large collections of Claude Code skills with intelligent conflict resolution and structure optimization.

## Purpose
Consolidate skills from multiple sources into a well-organized, conflict-free collection. Handles directory flattening, naming conflicts, metadata preservation, documentation generation, and repository maintenance.

## When to Use
- Merging skills from multiple repositories
- Organizing chaotic skill collections
- Preparing skills for distribution
- Maintaining a curated skills library
- Resolving naming conflicts across sources

## Capabilities

### 1. Collection Management

#### Directory Flattening
- Extract skills from nested structures
- Preserve skill integrity
- Maintain internal file relationships
- Handle multiple source patterns:
  - `repo/.claude/skills/skill-name/`
  - `repo/skills/skill-name/`
  - `repo/category/skill-name/`

#### Naming Strategy
- Add source suffixes to prevent conflicts
- Normalize naming conventions
- Handle special characters
- Preserve semantic meaning

#### Structure Validation
- Verify SKILL.md presence
- Check for required files
- Validate skill completeness
- Report structural issues

### 2. Conflict Resolution

#### Naming Conflicts
```
Conflict: Two skills named "code-review"
Source 1: obra/superpowers
Source 2: mrgoonie/claudekit-skills

Resolution:
- code-review_obra
- code-review_mrgoonie

Keep both for user choice.
```

#### Content Conflicts
- Detect identical skills from different sources
- Use duplicate detector to identify
- Keep most comprehensive version
- Archive alternatives

#### Metadata Conflicts
- Merge compatible metadata
- Preserve all source attributions
- Combine feature lists
- Aggregate documentation

### 3. Organization Strategies

#### By Source (Default)
```
/skills/
├── skill-name_obra/
├── skill-name_mrgoonie/
├── another-skill_diet103/
└── ...
```

#### By Category
```
/skills/
├── development/
│   ├── debugging/
│   ├── testing/
│   └── code-review/
├── infrastructure/
│   ├── docker/
│   └── kubernetes/
└── scientific/
    ├── databases/
    └── analysis/
```

#### Hybrid Approach
```
/skills/
├── core/              # Essential, curated skills
├── specialized/       # Domain-specific skills
├── experimental/      # New or untested skills
└── archived/          # Deprecated or superseded
```

### 4. Documentation Generation

#### Collection README
- Inventory of all skills
- Source attribution
- Installation instructions
- Usage examples
- License information

#### Category Indices
- Skills grouped by purpose
- Quick reference guides
- Search-optimized metadata
- Cross-references

#### Attribution Files
- License compliance
- Author credits
- Source repository links
- Contribution guidelines

## Usage Instructions

### Basic Consolidation
```
Use the skills-consolidator skill to:
1. Analyze all skills in /skills directory
2. Flatten any nested structures
3. Resolve naming conflicts with source suffixes
4. Generate comprehensive documentation
```

### Advanced Organization
```
Use the skills-consolidator skill to reorganize skills by category:
- Development tools → /skills/development/
- Scientific computing → /skills/scientific/
- Infrastructure → /skills/infrastructure/
- General purpose → /skills/general/

Maintain source attributions and generate category README files.
```

### Merge New Repository
```
Use the skills-consolidator skill to merge skills from new-repo into existing collection:
1. Extract skills from new-repo
2. Check for conflicts with existing skills
3. Add source suffix: _new-repo
4. Update main documentation
5. Generate merge report
```

## Consolidation Workflow

### Phase 1: Discovery & Analysis
```
1. Scan source directories
2. Identify all skills
3. Validate structure
4. Detect conflicts
5. Generate analysis report
```

### Phase 2: Organization
```
1. Create target structure
2. Flatten nested directories
3. Apply naming strategy
4. Resolve conflicts
5. Preserve metadata
```

### Phase 3: Validation
```
1. Verify all skills moved correctly
2. Check SKILL.md integrity
3. Validate file permissions
4. Test skill references
5. Confirm completeness
```

### Phase 4: Documentation
```
1. Generate main README
2. Create category indices
3. Build attribution files
4. Update changelogs
5. Create search indices
```

### Phase 5: Cleanup
```
1. Remove empty directories
2. Delete temporary files
3. Archive old structures
4. Optimize file organization
5. Commit changes
```

## Naming Conflict Resolution

### Strategy 1: Source Suffixes (Recommended)
```
code-review (from obra) → code-review_obra
code-review (from mrgoonie) → code-review_mrgoonie
```

**Pros**: Clear source attribution, no loss of skills
**Cons**: Longer names, requires user choice

### Strategy 2: Version Hierarchy
```
code-review (keep most comprehensive)
code-review-v1 (alternative version)
code-review-minimal (lightweight version)
```

**Pros**: Clear versioning, guided choice
**Cons**: Subjective quality assessment

### Strategy 3: Merge Strategy
```
code-review (merged best features from all sources)
├── from obra: requesting workflow
├── from mrgoonie: receiving workflow
└── from diet103: automation tools
```

**Pros**: Best-of-breed combination
**Cons**: Requires manual integration work

### Strategy 4: Namespace Prefixing
```
obra/code-review
mrgoonie/code-review
diet103/skill-developer
```

**Pros**: Mimics repository structure
**Cons**: Incompatible with flat skill loading in some systems

## Quality Assurance

### Pre-Consolidation Checks
- ✅ All source repositories cloned successfully
- ✅ Skills contain required SKILL.md files
- ✅ No malformed directory structures
- ✅ Licenses are compatible
- ✅ No binary files or secrets included

### Post-Consolidation Checks
- ✅ All skills extracted and flattened
- ✅ No naming conflicts remain unresolved
- ✅ Documentation is complete and accurate
- ✅ Attribution preserved for all sources
- ✅ Directory structure is optimized
- ✅ No broken internal references

### Validation Reports
```markdown
# Consolidation Validation Report

## Statistics
- Skills processed: 161
- Skills successfully consolidated: 154
- Duplicates identified: 7
- Naming conflicts resolved: 0
- Documentation files generated: 5

## Issues Found
- None

## Recommendations
- Consider categorizing skills by domain
- Update main repository README
- Add search functionality
- Create getting-started guide
```

## Integration Points

### Input Sources
- GitHub repositories (via bulk-github-skills-downloader)
- Local skill directories
- Exported skill collections
- Individual skill files

### Output Formats
- Flat directory structure (Claude Code compatible)
- Categorized hierarchy (browsing-friendly)
- Archived/compressed collections (distribution)
- Documentation websites (Jekyll/Hugo compatible)

### Tool Integration
- `bulk-github-skills-downloader`: Provides raw skills
- `skills-duplicate-detector`: Identifies redundancy
- `git-workflow-helper`: Commits organized collection
- `github-auth`: Pushes to remote repository

## Advanced Features

### Incremental Updates
```
Track previously consolidated skills:
- Skip unchanged skills
- Update modified skills only
- Add new skills automatically
- Remove deprecated skills
```

### Smart Categorization
```python
# Analyze skill purpose and auto-categorize
categories = {
    'development': ['debug', 'test', 'review', 'refactor'],
    'infrastructure': ['docker', 'kubernetes', 'deploy'],
    'scientific': ['database', 'analysis', 'research'],
    'documentation': ['markdown', 'diagram', 'wiki']
}

for skill in skills:
    category = auto_categorize(skill)
    move_to_category(skill, category)
```

### Dependency Analysis
```
Analyze skill dependencies:
- Required tools and CLIs
- Python/npm package requirements
- System dependencies
- API key requirements

Generate dependency matrix for collection.
```

### Health Metrics
```
Calculate collection health:
- Skill completeness score
- Documentation quality
- Last update recency
- Community activity
- Bug/issue count
```

## Configuration Options

### Organization Strategy
```yaml
organization:
  strategy: "source-suffix"  # source-suffix, category, hybrid, namespace
  flat_structure: true
  preserve_sources: true
  merge_duplicates: false
```

### Naming Conventions
```yaml
naming:
  suffix_separator: "_"      # skill-name_source
  normalize_case: "kebab"    # kebab-case, snake_case, camelCase
  remove_prefixes: ["skill", "claude"]
  max_length: 50
```

### Documentation
```yaml
documentation:
  generate_readme: true
  generate_categories: true
  generate_attribution: true
  include_statistics: true
  create_search_index: true
```

### Quality Control
```yaml
quality:
  require_skill_md: true
  validate_structure: true
  check_licenses: true
  scan_for_secrets: false    # Optional security scan
  enforce_naming: true
```

## Output Structure

### Consolidated Repository
```
your_claude_skills/
├── skills/                          # All consolidated skills
│   ├── skill-name_source/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   └── references/
│   └── ...
├── duplicates/                      # Archived duplicates
│   ├── DUPLICATES_LOG.md
│   └── duplicate-skill/
├── docs/                            # Generated documentation
│   ├── INDEX.md                     # Master index
│   ├── by-category.md               # Categorical view
│   ├── by-source.md                 # Source attribution
│   └── statistics.md                # Collection metrics
├── SKILLS_COLLECTION_README.md      # Main documentation
├── ATTRIBUTION.md                   # License compliance
└── CHANGELOG.md                     # Version history
```

## Best Practices

1. **Always Preserve Sources**: Keep attribution clear
2. **Document Decisions**: Record why conflicts were resolved a certain way
3. **Validate Thoroughly**: Check structure before and after
4. **Version Control**: Commit consolidation as atomic operation
5. **Incremental Approach**: Consolidate in batches if collection is large
6. **User Communication**: Explain organization strategy clearly
7. **Regular Maintenance**: Re-consolidate periodically as collection grows

## Performance Optimization

### Large Collections (500+ skills)
- Stream processing instead of loading all into memory
- Parallel validation checks
- Incremental documentation updates
- Chunked git commits

### Network Efficiency
- Shallow clones for source repositories
- Sparse checkouts when possible
- Cache frequently accessed repositories
- Batch API requests

## Error Handling

### Common Issues
1. **Naming Conflicts**: Apply resolution strategy automatically
2. **Missing SKILL.md**: Create basic template from directory name
3. **Broken Links**: Update or remove invalid references
4. **Permission Errors**: Report and skip problematic skills
5. **Disk Space**: Check available space before consolidation

### Recovery
- Create backup before consolidation
- Transaction-like operation (all or nothing)
- Rollback capability if validation fails
- Detailed error logs for troubleshooting

## Use Cases

### Scenario 1: Building Master Collection
```
Goal: Create comprehensive Claude skills library
1. Download top 20 skill repositories
2. Consolidate into single collection
3. Remove duplicates
4. Generate searchable documentation
5. Publish to GitHub
```

### Scenario 2: Team Skills Repository
```
Goal: Curated skills for development team
1. Select relevant skills from master collection
2. Organize by team workflow
3. Add team-specific customizations
4. Integrate with company tools
5. Maintain in private repository
```

### Scenario 3: Distribution Package
```
Goal: Package skills for easy installation
1. Consolidate selected skills
2. Flatten to Claude-compatible structure
3. Generate installation script
4. Create compressed archive
5. Publish release
```

## Maintenance Schedule

### Weekly
- Check for new skills in tracked repositories
- Update modified skills
- Regenerate documentation if needed

### Monthly
- Run duplicate detection
- Review categorization
- Update attribution files
- Check for deprecated skills

### Quarterly
- Full re-consolidation
- Structure optimization
- Documentation overhaul
- Community feedback integration

---

**Version**: 1.0.0
**Last Updated**: 2025-11-07
**Maintained by**: @yourusername
