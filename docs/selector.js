// ClaudeSkillz Selector Logic
let allSkills = [];
let selectedSkills = new Set();
let currentFilter = 'all';

function initializeSkills() {
    if (window.EMBEDDED_SKILLS && window.EMBEDDED_SKILLS.length > 0) {
        allSkills = window.EMBEDDED_SKILLS;
        console.log(`Loaded ${allSkills.length} skills`);

        // Auto-detect OS and pre-select checkbox
        const userAgent = navigator.userAgent.toLowerCase();
        if (userAgent.includes('win')) {
            document.getElementById('osWindows').checked = true;
        } else if (userAgent.includes('mac')) {
            document.getElementById('osMacOS').checked = true;
        } else if (userAgent.includes('linux')) {
            document.getElementById('osLinux').checked = true;
        }

        updateStats();
        renderSkills();
        setupEventListeners();
    } else {
        document.getElementById('skillsGrid').innerHTML = '<div class="loading">No skills found. Please regenerate the catalog.</div>';
    }
}

function setupEventListeners() {
    document.getElementById('searchInput').addEventListener('input', renderSkills);

    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            currentFilter = this.dataset.filter;
            renderSkills();
        });
    });
}

function updateStats() {
    document.getElementById('totalSkills').textContent = allSkills.length;
    document.getElementById('selectedCount').textContent = selectedSkills.size;
}

function renderSkills() {
    const grid = document.getElementById('skillsGrid');
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();

    let filteredSkills = allSkills.filter(skill => {
        const matchesSearch = skill.name.toLowerCase().includes(searchTerm) ||
                            skill.description.toLowerCase().includes(searchTerm);

        const matchesFilter = currentFilter === 'all' ||
                            (skill.category && skill.category.toLowerCase().includes(currentFilter.toLowerCase()));

        return matchesSearch && matchesFilter;
    });

    document.getElementById('filteredSkills').textContent = filteredSkills.length;

    if (filteredSkills.length === 0) {
        grid.innerHTML = '<div class="loading">No skills found matching your criteria.</div>';
        return;
    }

    grid.innerHTML = filteredSkills.map(skill => {
        const escapedName = skill.name.replace(/'/g, "\\'");
        return `
            <div class="skill-card ${selectedSkills.has(skill.name) ? 'selected' : ''}"
                 onclick="toggleSkill('${escapedName}')">
                <div class="checkbox"></div>
                <div class="skill-name">${skill.name}</div>
                <div class="skill-description">${skill.description}</div>
                <div class="skill-tags">
                    ${skill.category ? `<span class="tag">${skill.category}</span>` : ''}
                </div>
            </div>
        `;
    }).join('');
}

function toggleSkill(skillName) {
    if (selectedSkills.has(skillName)) {
        selectedSkills.delete(skillName);
    } else {
        selectedSkills.add(skillName);
    }
    updateStats();
    updateGenerateButton();
    renderSkills();
    updateScriptPreview();
}

function selectAll() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    allSkills.forEach(skill => {
        const matchesSearch = skill.name.toLowerCase().includes(searchTerm) ||
                            skill.description.toLowerCase().includes(searchTerm);
        const matchesFilter = currentFilter === 'all' ||
                            (skill.category && skill.category.toLowerCase().includes(currentFilter.toLowerCase()));

        if (matchesSearch && matchesFilter) {
            selectedSkills.add(skill.name);
        }
    });
    updateStats();
    updateGenerateButton();
    renderSkills();
    updateScriptPreview();
}

function deselectAll() {
    selectedSkills.clear();
    updateStats();
    updateGenerateButton();
    renderSkills();
    updateScriptPreview();
}

function updateGenerateButton() {
    const btn = document.getElementById('generateBtn');
    const hasSelection = selectedSkills.size > 0;
    const hasOS = document.getElementById('osWindows').checked ||
                 document.getElementById('osLinux').checked ||
                 document.getElementById('osMacOS').checked;
    btn.disabled = !hasSelection || !hasOS;
}

function generateWindowsScript(skills) {
    return `# ClaudeSkillz Installation Script for Windows
# Generated: ${new Date().toISOString()}
# Selected Skills: ${skills.length}

$skillsDir = "$env:USERPROFILE\\.claude\\skills"
$repoUrl = "https://github.com/jackspace/ClaudeSkillz.git"
$tempDir = "$env:TEMP\\claudeskillz-temp"

Write-Host "ClaudeSkillz Installer" -ForegroundColor Cyan
Write-Host "Installing ${skills.length} selected skills..." -ForegroundColor Cyan
Write-Host ""

# Create skills directory if it doesn't exist
if (-not (Test-Path $skillsDir)) {
    New-Item -ItemType Directory -Path $skillsDir -Force | Out-Null
    Write-Host "[OK] Created skills directory" -ForegroundColor Green
}

# Clone repository to temp
Write-Host "Cloning ClaudeSkillz repository..." -ForegroundColor Yellow
if (Test-Path $tempDir) {
    Remove-Item -Recurse -Force $tempDir
}
git clone --depth 1 $repoUrl $tempDir

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to clone repository" -ForegroundColor Red
    exit 1
}

# Install selected skills
$selectedSkills = @(
${skills.map(s => `    '${s}'`).join(',\n')}
)

foreach ($skill in $selectedSkills) {
    $sourcePath = Join-Path $tempDir "skills\\$skill"
    $destPath = Join-Path $skillsDir $skill

    if (Test-Path $sourcePath) {
        Copy-Item -Recurse -Force $sourcePath $destPath
        Write-Host "[OK] Installed: $skill" -ForegroundColor Green
    } else {
        Write-Host "[SKIP] Not found: $skill" -ForegroundColor Yellow
    }
}

# Cleanup
Remove-Item -Recurse -Force $tempDir
Write-Host ""
Write-Host "Installation complete! ${skills.length} skills installed." -ForegroundColor Cyan`;
}

function generateLinuxScript(skills) {
    return `#!/usr/bin/env bash
# ClaudeSkillz Installation Script for Linux/macOS
# Generated: ${new Date().toISOString()}
# Selected Skills: ${skills.length}

set -e

SKILLS_DIR="$HOME/.claude/skills"
REPO_URL="https://github.com/jackspace/ClaudeSkillz.git"
TEMP_DIR="/tmp/claudeskillz-temp"

echo "ClaudeSkillz Installer"
echo "Installing ${skills.length} selected skills..."
echo ""

# Create skills directory
mkdir -p "$SKILLS_DIR"
echo "[OK] Skills directory ready"

# Clone repository
echo "Cloning ClaudeSkillz repository..."
rm -rf "$TEMP_DIR"
git clone --depth 1 "$REPO_URL" "$TEMP_DIR"

# Install selected skills
SKILLS=(
${skills.map(s => `    "${s}"`).join('\n')}
)

for skill in "\${SKILLS[@]}"; do
    SOURCE_PATH="$TEMP_DIR/skills/$skill"
    DEST_PATH="$SKILLS_DIR/$skill"

    if [ -d "$SOURCE_PATH" ]; then
        cp -r "$SOURCE_PATH" "$DEST_PATH"
        echo "[OK] Installed: $skill"
    else
        echo "[SKIP] Not found: $skill"
    fi
done

# Cleanup
rm -rf "$TEMP_DIR"
echo ""
echo "Installation complete! ${skills.length} skills installed."`;
}

function updateScriptPreview() {
    const preview = document.getElementById('scriptPreview');
    const content = document.getElementById('scriptContent');
    const title = document.getElementById('scriptTitle');

    if (selectedSkills.size === 0) {
        preview.classList.remove('active');
        return;
    }

    const skills = Array.from(selectedSkills);
    const osWindows = document.getElementById('osWindows').checked;
    const osLinux = document.getElementById('osLinux').checked;
    const osMacOS = document.getElementById('osMacOS').checked;

    let scripts = [];
    if (osWindows) scripts.push({ os: 'Windows (PowerShell)', content: generateWindowsScript(skills) });
    if (osLinux || osMacOS) scripts.push({ os: 'Linux/macOS (Bash)', content: generateLinuxScript(skills) });

    if (scripts.length > 0) {
        const script = scripts[0];
        title.textContent = `Installation Script - ${script.os}`;
        content.textContent = script.content;
        preview.classList.add('active');
    }
}

function copyScript() {
    const content = document.getElementById('scriptContent').textContent;
    navigator.clipboard.writeText(content).then(() => {
        const btn = event.target;
        const originalText = btn.textContent;
        btn.textContent = 'Copied!';
        setTimeout(() => {
            btn.textContent = originalText;
        }, 2000);
    }).catch(err => {
        alert('Failed to copy: ' + err);
    });
}

function generateInstallScript() {
    console.log('[DEBUG] generateInstallScript called');
    console.log('[DEBUG] selectedSkills.size:', selectedSkills.size);

    if (selectedSkills.size === 0) {
        alert('Please select at least one skill to install.');
        return;
    }

    const osWindows = document.getElementById('osWindows').checked;
    const osLinux = document.getElementById('osLinux').checked;
    const osMacOS = document.getElementById('osMacOS').checked;

    if (!osWindows && !osLinux && !osMacOS) {
        alert('Please select at least one target operating system.');
        return;
    }

    const skills = Array.from(selectedSkills);

    // Generate scripts for selected OSes
    if (osWindows) {
        downloadScript(generateWindowsScript(skills), 'install-claudeskillz.ps1', 'text/plain');
    }

    if (osLinux || osMacOS) {
        downloadScript(generateLinuxScript(skills), 'install-claudeskillz.sh', 'text/x-shellscript');
    }

    alert(`Install script(s) generated for ${skills.length} skill(s)!\n\nCheck your Downloads folder for:\n` +
          (osWindows ? '- install-claudeskillz.ps1 (Windows)\n' : '') +
          (osLinux || osMacOS ? '- install-claudeskillz.sh (Linux/macOS)' : ''));
}

function downloadScript(content, filename, mimeType) {
    try {
        const blob = new Blob([content], { type: mimeType });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.style.display = 'none';

        document.body.appendChild(a);

        setTimeout(() => {
            a.click();
            setTimeout(() => {
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            }, 100);
        }, 0);
    } catch (error) {
        console.error('[ERROR] Failed to generate download:', error);
        alert('Error generating download: ' + error.message);
    }
}
