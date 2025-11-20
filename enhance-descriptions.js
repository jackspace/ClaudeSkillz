#!/usr/bin/env node
/**
 * Skill Description Enhancement Script
 *
 * This script reads SKILL.md files and extracts meaningful descriptions
 * to replace generic "Claude Code skill for X" descriptions.
 */

const fs = require('fs');
const path = require('path');

// Paths
const CATALOG_PATH = path.join(__dirname, 'docs', 'skills-catalog.json');
const SKILLS_DIR = path.join(__dirname, 'skills');

console.log('🚀 Starting skill description enhancement...\n');

// Read the catalog
let catalog;
try {
    const catalogData = fs.readFileSync(CATALOG_PATH, 'utf8');
    catalog = JSON.parse(catalogData);
} catch (error) {
    console.error('❌ Error reading catalog:', error.message);
    process.exit(1);
}

// Find skills with generic descriptions
const genericPattern = /^Claude Code skill for/i;
const skillsToEnhance = catalog.skills.filter(skill =>
    genericPattern.test(skill.description)
);

console.log(`Found ${skillsToEnhance.length} skills with generic descriptions\n`);

let enhanced = 0;
let failed = 0;
let skipped = 0;

// Process each skill
for (const skill of skillsToEnhance) {
    const skillPath = path.join(SKILLS_DIR, skill.name, 'SKILL.md');

    if (!fs.existsSync(skillPath)) {
        console.log(`⚠️  ${skill.name}: SKILL.md not found, skipping`);
        skipped++;
        continue;
    }

    try {
        const content = fs.readFileSync(skillPath, 'utf8');
        const newDescription = extractDescription(content, skill.name);

        if (newDescription && newDescription !== skill.description) {
            skill.description = newDescription;
            console.log(`✅ ${skill.name}`);
            console.log(`   → ${newDescription.substring(0, 80)}${newDescription.length > 80 ? '...' : ''}`);
            enhanced++;
        } else {
            console.log(`⚠️  ${skill.name}: Could not extract better description`);
            failed++;
        }
    } catch (error) {
        console.log(`❌ ${skill.name}: Error - ${error.message}`);
        failed++;
    }
}

// Save updated catalog
if (enhanced > 0) {
    try {
        fs.writeFileSync(CATALOG_PATH, JSON.stringify(catalog, null, 2), 'utf8');
        console.log(`\n✨ Success! Enhanced ${enhanced} skill descriptions`);
        console.log(`📁 Updated: ${CATALOG_PATH}`);
    } catch (error) {
        console.error(`\n❌ Error saving catalog: ${error.message}`);
        process.exit(1);
    }
} else {
    console.log('\n⚠️  No descriptions were enhanced');
}

console.log(`\n📊 Summary:`);
console.log(`   Enhanced: ${enhanced}`);
console.log(`   Failed: ${failed}`);
console.log(`   Skipped: ${skipped}`);
console.log(`   Total: ${skillsToEnhance.length}`);

/**
 * Extract a meaningful description from SKILL.md content
 */
function extractDescription(content, skillName) {
    // Remove frontmatter if present
    content = content.replace(/^---[\s\S]*?---\n/, '');

    // Try to find description in common patterns
    const patterns = [
        // Look for "description:" field
        /description:\s*["']?([^"'\n]+)["']?/i,
        // Look for first paragraph after title
        /^#\s+.+?\n\n([^\n]+)/m,
        // Look for "Use when" or "Use this" patterns
        /(?:Use (?:when|this|for)[:\s]+)([^.\n]+[.])/i,
        // Look for any substantial first paragraph
        /^(?:#{1,3}\s+.*?\n+)?([A-Z][^.\n]{20,}\.)/m
    ];

    for (const pattern of patterns) {
        const match = content.match(pattern);
        if (match && match[1]) {
            let desc = match[1].trim();

            // Clean up the description
            desc = desc
                .replace(/\s+/g, ' ')  // Normalize whitespace
                .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')  // Remove markdown links
                .replace(/[*_`]/g, '')  // Remove markdown formatting
                .trim();

            // Truncate if too long
            if (desc.length > 250) {
                desc = desc.substring(0, 247) + '...';
            }

            // Make sure it ends with period
            if (!desc.endsWith('.') && !desc.endsWith('...')) {
                desc += '.';
            }

            // Validate it's actually useful
            if (desc.length > 20 && !desc.toLowerCase().includes('claude code skill')) {
                return desc;
            }
        }
    }

    // Fallback: try to get first meaningful sentence
    const sentences = content.match(/[A-Z][^.!?]*[.!?]/g);
    if (sentences && sentences.length > 0) {
        for (const sentence of sentences.slice(0, 5)) {
            const cleaned = sentence.replace(/[#*_`\[\]()]/g, '').trim();
            if (cleaned.length > 30 && cleaned.length < 250 &&
                !cleaned.toLowerCase().includes('claude code skill')) {
                return cleaned;
            }
        }
    }

    return null;
}
