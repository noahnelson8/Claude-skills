# site-design-kit installer
# Copies this kit into each Claude config's skills folder (personal ~/.claude and work ~/.claude-work by default)
# and downloads the three bundled tools from their official GitHub repos at pinned commits into vendor/.
# The vendor files are not committed to the claude-skills repo (MotionSites' examples/media may not be redistributed).
#
# Usage:  powershell -ExecutionPolicy Bypass -File install.ps1
#         powershell -ExecutionPolicy Bypass -File install.ps1 -ConfigDirs "$HOME\.claude"
#         powershell -ExecutionPolicy Bypass -File install.ps1 -Update   (re-download vendor even if present)

param(
    [string[]]$ConfigDirs,
    [switch]$Update
)
$ErrorActionPreference = 'Stop'

# name, repo, pinned commit, folder inside the repo that holds the skill
$Vendors = @(
    @{ Name = 'motionsites';   Repo = 'https://github.com/Motionsites-AI/claude-skill.git';          Sha = 'a57e6d245ec4982fd804db5ac38711569bdfd094'; Path = 'plugins/motionsites-web-builder/skills/motionsites-web-builder' },
    @{ Name = 'scroll-craft';  Repo = 'https://github.com/nateherkai/scroll-craft.git';              Sha = '75d81f74e83692add18cd7a8a8e078b8a887a579'; Path = 'plugins/nateherk-design/skills/scroll-craft' },
    @{ Name = 'ui-ux-pro-max'; Repo = 'https://github.com/nextlevelbuilder/ui-ux-pro-max-skill.git'; Sha = 'cc7b20d85d64d8fa022292cfad731995d3cd4eeb'; Path = '.claude/skills/ui-ux-pro-max' }
)
$KitFiles = @('SKILL.md', 'install.ps1', 'references', 'scripts')

$src = $PSScriptRoot
if (-not $ConfigDirs) {
    $ConfigDirs = @("$HOME\.claude", "$HOME\.claude-work") | Where-Object { Test-Path $_ }
}
if (-not $ConfigDirs) { throw "No Claude config folder found (looked for ~/.claude and ~/.claude-work)." }
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw "git is required." }

# 1. Download each vendor once, at its pinned commit
$stage = Join-Path ([IO.Path]::GetTempPath()) ("sdk-vendor-" + [guid]::NewGuid().ToString('N').Substring(0, 8))
New-Item -ItemType Directory $stage | Out-Null
try {
    foreach ($v in $Vendors) {
        $repoDir = Join-Path $stage $v.Name
        Write-Host "Downloading $($v.Name) @ $($v.Sha.Substring(0,7)) ..."
        git init -q $repoDir
        git -C $repoDir remote add origin $v.Repo
        git -C $repoDir fetch -q --depth 1 origin $v.Sha
        if ($LASTEXITCODE -ne 0) { throw "Could not fetch $($v.Repo) at $($v.Sha)" }
        git -C $repoDir -c advice.detachedHead=false checkout -q FETCH_HEAD
        $skillDir = Join-Path $repoDir ($v.Path -replace '/', '\')
        if (-not (Test-Path (Join-Path $skillDir 'SKILL.md'))) { throw "$($v.Name): SKILL.md not found at $($v.Path)" }
        # Rename so Claude never registers the bundled tool as a separate, competing skill
        Rename-Item (Join-Path $skillDir 'SKILL.md') 'UPSTREAM-SKILL.md'
        $lic = Join-Path $repoDir 'LICENSE'
        if (Test-Path $lic) { Copy-Item $lic (Join-Path $skillDir 'LICENSE.upstream') }
        Set-Content (Join-Path $skillDir 'SOURCE.txt') "$($v.Repo)`r`ncommit $($v.Sha)`r`npath $($v.Path)"
        $v.Staged = $skillDir
    }

    # 2. Install the kit + vendor into each config folder
    foreach ($cfg in $ConfigDirs) {
        $dest = Join-Path $cfg 'skills\site-design-kit'
        New-Item -ItemType Directory $dest -Force | Out-Null
        if ((Resolve-Path $dest).Path -ne (Resolve-Path $src).Path) {
            foreach ($f in $KitFiles) { Copy-Item (Join-Path $src $f) $dest -Recurse -Force }
            if (-not (Test-Path (Join-Path $dest 'runs.md'))) { Copy-Item (Join-Path $src 'runs.md') $dest }
        }
        foreach ($v in $Vendors) {
            $vd = Join-Path $dest "vendor\$($v.Name)"
            if ((Test-Path $vd) -and -not $Update) {
                $have = Get-Content (Join-Path $vd 'SOURCE.txt') -ErrorAction SilentlyContinue
                if ($have -match $v.Sha) { continue }
            }
            if (Test-Path $vd) { Remove-Item $vd -Recurse -Force }
            New-Item -ItemType Directory (Split-Path $vd) -Force | Out-Null
            Copy-Item $v.Staged $vd -Recurse
        }
        Write-Host "Installed site-design-kit -> $dest"
    }
}
finally {
    Remove-Item $stage -Recurse -Force -ErrorAction SilentlyContinue
}

# 3. Report what each lead needs
$py = [bool](Get-Command python -ErrorAction SilentlyContinue)
$node = [bool](Get-Command node -ErrorAction SilentlyContinue)
Write-Host ""
Write-Host ("Python (UI UX Pro Max, screenshots): " + $(if ($py) { 'ok' } else { 'MISSING: winget install Python.Python.3.12' }))
Write-Host ("Node.js (ScrollCraft lead only):     " + $(if ($node) { 'ok' } else { 'missing: winget install OpenJS.NodeJS.LTS (only needed for scroll experiences)' }))
Write-Host "Restart Claude Code (or start a new session) so it picks up the skill."
