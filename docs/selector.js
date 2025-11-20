// ClaudeSkillz Selector Logic
let allSkills = [];
let selectedSkills = new Set();

// Easter Egg Variables
let logoClickCount = 0;
let logoClickTimeout = null;
const konamiCode = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a'];
let konamiIndex = 0;

function initializeSkills() {
    if (window.EMBEDDED_SKILLS && window.EMBEDDED_SKILLS.length > 0) {
        allSkills = window.EMBEDDED_SKILLS;
        console.log(`Loaded ${allSkills.length} skills`);

        // Auto-detect OS and pre-select radio button
        const userAgent = navigator.userAgent.toLowerCase();
        if (userAgent.includes('win')) {
            document.getElementById('osWindows').checked = true;
        } else {
            // Mac and Linux both use Unix script
            document.getElementById('osUnix').checked = true;
        }

        // Load dark mode preference
        loadDarkModePreference();

        updateStats();
        renderSkills();
        setupEventListeners();
    } else {
        document.getElementById('skillsContainer').innerHTML = '<div class="loading">No skills found. Please regenerate the catalog.</div>';
    }
}

function setupEventListeners() {
    document.getElementById('searchInput').addEventListener('input', renderSkills);

    // Konami Code Easter Egg
    document.addEventListener('keydown', handleKonamiCode);
}

// Dark Mode Functions
function loadDarkModePreference() {
    const darkMode = localStorage.getItem('claudeskillz-darkmode') === 'true';
    if (darkMode) {
        document.body.classList.add('dark-mode');
        updateDarkModeButton();
    }
}

function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    localStorage.setItem('claudeskillz-darkmode', isDark);
    updateDarkModeButton();
}

function updateDarkModeButton() {
    const btn = document.getElementById('darkModeToggle');
    const isDark = document.body.classList.contains('dark-mode');
    btn.textContent = isDark ? '☀️ Light Mode' : '🌙 Dark Mode';
}

// Easter Egg: Logo Click Counter
function easterEggClick() {
    logoClickCount++;

    clearTimeout(logoClickTimeout);
    logoClickTimeout = setTimeout(() => {
        logoClickCount = 0;
    }, 2000);

    if (logoClickCount === 5) {
        activateMatrixMode();
        logoClickCount = 0;
    } else if (logoClickCount === 3) {
        const logo = document.getElementById('logo');
        logo.style.transform = 'rotate(360deg)';
        logo.style.transition = 'transform 0.5s ease';
        setTimeout(() => {
            logo.style.transform = 'rotate(0deg)';
        }, 500);
    }
}

// Easter Egg: Konami Code
function handleKonamiCode(e) {
    if (e.key === konamiCode[konamiIndex]) {
        konamiIndex++;
        if (konamiIndex === konamiCode.length) {
            activateMatrixMode();
            konamiIndex = 0;
        }
    } else {
        konamiIndex = 0;
    }
}

// Easter Egg: Matrix Mode
function activateMatrixMode() {
    const wasMatrix = document.body.classList.contains('matrix-mode');
    document.body.classList.toggle('matrix-mode');

    if (!wasMatrix) {
        alert('🎉 MATRIX MODE ACTIVATED! 🎉\n\nYou found the secret mode!\n\nTry the Konami Code or click the logo 5 times fast to toggle.');
        console.log('%c WELCOME TO THE MATRIX ', 'background: #000; color: #0f0; font-size: 20px; font-family: monospace;');
    }
}

function updateStats() {
    document.getElementById('totalSkills').textContent = allSkills.length;
    document.getElementById('selectedCount').textContent = selectedSkills.size;
}

function groupSkillsByCategory() {
    const grouped = {};
    allSkills.forEach(skill => {
        const category = skill.category || 'General';
        if (!grouped[category]) {
            grouped[category] = [];
        }
        grouped[category].push(skill);
    });

    // Sort categories alphabetically, but put General last
    const sortedCategories = Object.keys(grouped).sort((a, b) => {
        if (a === 'General') return 1;
        if (b === 'General') return -1;
        return a.localeCompare(b);
    });

    const sortedGrouped = {};
    sortedCategories.forEach(cat => {
        // Sort skills within category alphabetically
        sortedGrouped[cat] = grouped[cat].sort((a, b) => a.name.localeCompare(b.name));
    });

    return sortedGrouped;
}

function renderSkills() {
    const container = document.getElementById('skillsContainer');
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();

    const groupedSkills = groupSkillsByCategory();
    let html = '';
    let totalVisible = 0;

    Object.keys(groupedSkills).forEach(category => {
        const skillsInCategory = groupedSkills[category];

        // Filter skills by search term
        const filteredSkills = skillsInCategory.filter(skill => {
            return skill.name.toLowerCase().includes(searchTerm) ||
                   skill.description.toLowerCase().includes(searchTerm);
        });

        if (filteredSkills.length === 0) return;

        totalVisible += filteredSkills.length;

        html += `
            <div class="category-section">
                <div class="category-header">
                    <div class="category-title">
                        ${category} <span class="category-count">(${filteredSkills.length})</span>
                    </div>
                    <button class="category-select-all" onclick="selectCategory('${category}')">
                        Select All
                    </button>
                </div>
                <div class="skills-list">
                    ${filteredSkills.map(skill => {
                        const escapedName = skill.name.replace(/'/g, "\\'").replace(/"/g, '&quot;');
                        const isChecked = selectedSkills.has(skill.name) ? 'checked' : '';
                        return `
                            <div class="skill-item">
                                <input type="checkbox"
                                       id="skill-${skill.name}"
                                       ${isChecked}
                                       onchange="toggleSkill('${escapedName}')">
                                <label class="skill-name" for="skill-${skill.name}">${skill.name}</label>
                                <div class="skill-tooltip">${skill.description}</div>
                            </div>
                        `;
                    }).join('')}
                </div>
            </div>
        `;
    });

    if (totalVisible === 0) {
        container.innerHTML = '<div class="loading">No skills found matching your search.</div>';
    } else {
        container.innerHTML = html;
    }
}

function toggleSkill(skillName) {
    if (selectedSkills.has(skillName)) {
        selectedSkills.delete(skillName);
    } else {
        selectedSkills.add(skillName);
    }
    updateStats();
    updateGenerateButton();
    updateScriptPreview();
}

function selectAll() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    allSkills.forEach(skill => {
        const matchesSearch = skill.name.toLowerCase().includes(searchTerm) ||
                            skill.description.toLowerCase().includes(searchTerm);

        if (matchesSearch) {
            selectedSkills.add(skill.name);
        }
    });
    updateStats();
    updateGenerateButton();
    renderSkills();
    updateScriptPreview();
}

function selectCategory(category) {
    // Get all skills in this category
    const categorySkills = allSkills.filter(skill => (skill.category || 'General') === category);

    // Check if all are already selected
    const allSelected = categorySkills.every(skill => selectedSkills.has(skill.name));

    if (allSelected) {
        // Deselect all in category
        categorySkills.forEach(skill => selectedSkills.delete(skill.name));
    } else {
        // Select all in category
        categorySkills.forEach(skill => selectedSkills.add(skill.name));
    }

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

function handleOSChange() {
    updateGenerateButton();
    updateScriptPreview();
}

function updateGenerateButton() {
    const btn = document.getElementById('generateBtn');
    const hasSelection = selectedSkills.size > 0;
    // OS is always selected (radio buttons)
    btn.disabled = !hasSelection;
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

    if (osWindows) {
        title.textContent = 'Installation Script - Windows (PowerShell)';
        content.textContent = generateWindowsScript(skills);
    } else {
        title.textContent = 'Installation Script - Linux/macOS (Bash)';
        content.textContent = generateLinuxScript(skills);
    }

    preview.classList.add('active');
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

    const skills = Array.from(selectedSkills);
    const osWindows = document.getElementById('osWindows').checked;

    if (osWindows) {
        downloadScript(generateWindowsScript(skills), 'install-claudeskillz.ps1', 'text/plain');
        alert(`Install script generated for ${skills.length} skill(s)!\n\nCheck your Downloads folder for:\n- install-claudeskillz.ps1 (Windows)`);
    } else {
        downloadScript(generateLinuxScript(skills), 'install-claudeskillz.sh', 'text/x-shellscript');
        alert(`Install script generated for ${skills.length} skill(s)!\n\nCheck your Downloads folder for:\n- install-claudeskillz.sh (Linux/macOS)`);
    }
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
