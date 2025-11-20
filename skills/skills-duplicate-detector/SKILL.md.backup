# Skills Duplicate Detector

Expert skill for identifying duplicate, similar, and overlapping Claude Code skills across your collection using intelligent comparison algorithms.

## Purpose
Analyze a collection of Claude Code skills to identify duplicates, near-duplicates, and functionally similar skills. Helps maintain a clean, organized skills collection by detecting redundancy and suggesting consolidation.

## When to Use
- After bulk downloading skills from multiple sources
- Maintaining an existing skills collection
- Before committing new skills to a repository
- Auditing skill collections for redundancy

## Capabilities

### 1. Duplicate Detection Methods

#### Exact Name Matching
- Identify skills with identical names
- Detect name variations with prefixes/suffixes
- Find skills differing only in case

#### Semantic Similarity
- Analyze SKILL.md descriptions
- Compare stated purposes and capabilities
- Identify functional overlap
- Calculate similarity scores

#### Content Analysis
- Compare skill file structures
- Analyze included scripts and tools
- Check for shared dependencies
- Detect copy/paste variations

### 2. Similarity Categories

#### Perfect Duplicates (100% match)
- Identical names and content
- Same functionality and purpose
- Likely from same source

#### Near Duplicates (80-99% match)
- Similar names with minor variations
- Nearly identical functionality
- Possible version differences

#### Functional Overlaps (60-79% match)
- Different names, similar purpose
- Overlapping capabilities
- May serve different use cases

#### Related Skills (40-59% match)
- Adjacent functionality
- Complementary features
- Worth noting but not duplicates

### 3. Analysis Outputs

#### Duplicate Report
```markdown
# Duplicate Skills Analysis

## Perfect Duplicates (7 found)

### Group 1: Code Review
- **code-review_mrgoonie** (KEEP - most comprehensive)
  - Location: /skills/code-review_mrgoonie
  - Size: 15 KB
  - Features: Requesting, receiving, verification

- **receiving-code-review_obra** (DUPLICATE)
  - Location: /skills/receiving-code-review_obra
  - Similarity: 95%
  - Recommendation: Move to /duplicates

- **requesting-code-review_obra** (DUPLICATE)
  - Location: /skills/requesting-code-review_obra
  - Similarity: 92%
  - Recommendation: Move to /duplicates

**Reason**: All three provide code review functionality. mrgoonie version combines both requesting and receiving in one comprehensive skill.
```

## Usage Instructions

### Basic Duplicate Detection
```
Use the skills-duplicate-detector skill to analyze /skills directory and identify all duplicates.
```

### Detailed Analysis
```
Use the skills-duplicate-detector skill to:
1. Scan all skills in /skills directory
2. Identify duplicates with 70%+ similarity
3. Generate a detailed report with recommendations
4. Create a DUPLICATES_LOG.md file
```

### Pre-commit Check
```
Before committing new skills, use skills-duplicate-detector to check if they already exist in the collection.
```

## Detection Algorithm

### Phase 1: Name Analysis
```python
# Normalize skill names
def normalize_name(skill_name):
    # Remove source suffixes (_obra, _mrgoonie, etc.)
    # Convert to lowercase
    # Remove special characters
    # Standardize spacing
    return normalized_name

# Find exact and near matches
for skill1, skill2 in pairs:
    name_similarity = levenshtein_distance(
        normalize_name(skill1),
        normalize_name(skill2)
    )
```

### Phase 2: Content Analysis
```python
# Compare SKILL.md descriptions
def compare_descriptions(skill1, skill2):
    # Extract purpose statements
    # Tokenize and compare keywords
    # Calculate semantic similarity
    # Weight by capability overlap
    return similarity_score
```

### Phase 3: Structural Analysis
```python
# Compare file structures
def compare_structure(skill1, skill2):
    # List files and directories
    # Compare organization
    # Check for shared patterns
    # Identify clones vs. variations
    return structure_score
```

## Comparison Heuristics

### Name-Based Detection
- **Exact match**: Same name after normalization → 100%
- **Prefix/suffix variation**: `skill` vs `skill_source` → 95%
- **Hyphen/underscore**: `code-review` vs `code_review` → 90%
- **Abbreviations**: `db-helper` vs `database-helper` → 80%

### Purpose-Based Detection
- **Identical purpose**: Same goals stated → 95%
- **Overlapping functionality**: 80%+ feature overlap → 85%
- **Complementary**: Different aspects of same domain → 60%
- **Related**: Adjacent problem spaces → 40%

### Quality Assessment
When duplicates are found, recommend keeping the version with:
1. ✅ Most comprehensive documentation
2. ✅ Largest feature set
3. ✅ Most recent updates
4. ✅ Better code quality
5. ✅ More complete examples

## Output Formats

### Console Report
```
Duplicate Detection Results
===========================

Total skills scanned: 161
Unique skills: 154
Duplicates found: 7
Similarity threshold: 70%

Perfect Duplicates (3 groups):
  - Code review skills (3 items)
  - Debugging skills (2 items)
  - Skill creation tools (3 items)

Near Duplicates (2 groups):
  - Brainstorming skills (2 items)
  - Document skills (2 items)

Recommendations:
  - Move 7 skills to /duplicates
  - Keep 154 unique skills in /skills
  - Estimated disk space saved: 2.3 MB
```

### Markdown Report (DUPLICATES_LOG.md)
- Detailed analysis of each duplicate group
- Side-by-side comparison tables
- Recommendations with reasoning
- Links to source repositories

### JSON Export
```json
{
  "analysis_date": "2025-11-07",
  "total_skills": 161,
  "unique_skills": 154,
  "duplicates": [
    {
      "group_id": 1,
      "group_name": "code-review",
      "members": [
        {
          "path": "/skills/code-review_mrgoonie",
          "keep": true,
          "reason": "Most comprehensive"
        },
        {
          "path": "/skills/receiving-code-review_obra",
          "keep": false,
          "similarity": 0.95
        }
      ]
    }
  ]
}
```

## Configuration Options

### Similarity Thresholds
```yaml
thresholds:
  perfect_duplicate: 0.95      # 95%+ similarity
  near_duplicate: 0.80         # 80-94% similarity
  functional_overlap: 0.60     # 60-79% similarity
  related: 0.40                # 40-59% similarity
  report_minimum: 0.60         # Only report 60%+ matches
```

### Comparison Weights
```yaml
weights:
  name_similarity: 0.30        # 30% weight on name matching
  purpose_similarity: 0.40     # 40% weight on purpose/description
  structure_similarity: 0.20   # 20% weight on file structure
  feature_overlap: 0.10        # 10% weight on feature comparison
```

### Output Options
```yaml
output:
  console_report: true
  markdown_report: true
  json_export: false
  auto_move_duplicates: false  # Require confirmation
  create_backups: true         # Before moving files
```

## Detection Patterns

### Common Duplicate Patterns

1. **Source-Suffixed Variants**
   ```
   skill-name_obra
   skill-name_mrgoonie
   skill-name_diet103
   ```

2. **Naming Convention Differences**
   ```
   code-review
   code_review
   codeReview
   ```

3. **Scope Variations**
   ```
   document-skills         (broad)
   scientific-document-skills  (specialized)
   pdf-document-skills     (narrow)
   ```

4. **Feature Splits**
   ```
   code-review             (combined)
   requesting-code-review  (split)
   receiving-code-review   (split)
   ```

## Special Cases

### Not Duplicates
- **Specialized vs. General**: Scientific brainstorming vs. general brainstorming
- **Different Frameworks**: React testing vs. Vue testing
- **Language-Specific**: Python debugging vs. JavaScript debugging
- **Platform-Specific**: AWS deployment vs. GCP deployment

### Borderline Cases
- **Related Workflows**: Git branching vs. Git worktrees
- **Tool Variations**: Docker basics vs. Docker Compose
- **Complementary**: API client vs. API server

## Integration with Other Skills

### Works Well With
- `bulk-github-skills-downloader`: Detect duplicates after download
- `skills-consolidator`: Merge similar skills
- `git-workflow-helper`: Commit duplicate cleanup
- `skill-creator_mrgoonie`: Check before creating new skills

## Workflow

1. **Scan Phase**
   - Enumerate all skills in /skills
   - Read SKILL.md files
   - Extract metadata and features

2. **Analysis Phase**
   - Calculate pairwise similarities
   - Group related skills
   - Score and rank matches

3. **Recommendation Phase**
   - Identify best version to keep
   - Suggest duplicates to move
   - Generate reasoning

4. **Action Phase**
   - Create DUPLICATES_LOG.md
   - Optionally move duplicates
   - Update inventory

## Best Practices

1. **Review Before Moving**: Always review recommendations before moving files
2. **Preserve History**: Keep duplicates in /duplicates, don't delete
3. **Document Decisions**: Record why certain skills were kept
4. **Regular Audits**: Run detector quarterly on growing collections
5. **Version Awareness**: Consider that "duplicates" might be different versions

## Performance

- **Speed**: ~10-20 skills per second
- **Memory**: Minimal (streaming analysis)
- **Accuracy**: 95%+ for exact duplicates, 80%+ for near duplicates

## Limitations

- Cannot detect functional duplicates with completely different implementations
- Requires SKILL.md files for semantic analysis
- May miss duplicates in non-standard formats
- Similarity scores are heuristic-based

## Advanced Usage

### Custom Similarity Rules
```
Detect duplicates but treat these as separate:
- Python-specific vs. JavaScript-specific skills
- Scientific vs. general-purpose variations
- Enterprise vs. open-source tool integrations
```

### Bulk Cleanup
```
Use skills-duplicate-detector to:
1. Find all duplicates above 90% similarity
2. Automatically keep the most comprehensive version
3. Move others to /duplicates
4. Generate cleanup report
5. Commit changes with detailed message
```

---

**Version**: 1.0.0
**Last Updated**: 2025-11-07
**Maintained by**: @yourusername
