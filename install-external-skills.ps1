# Installs reviewed third-party skills into the personal (~/.claude) and work (~/.claude-work) Claude Code setups.
# Each entry is pinned to the exact commit that was read and reviewed; bump a commit only after re-reviewing.
# The skills themselves are not copied into this repo (they're downloaded from their official sources).
#
# Usage:  powershell -ExecutionPolicy Bypass -File install-external-skills.ps1
#         ... -ConfigDirs "$HOME\.claude"        (only one setup)

param([string[]]$ConfigDirs)
$ErrorActionPreference = 'Stop'

$Sources = @(
    @{ Repo = 'https://github.com/coreyhaines31/marketingskills.git'; Sha = '8fd2fcade2fd6629026e9dfe6d133b55b36968b9'; Reviewed = '2026-11-24'
       Skills = @('skills/product-marketing', 'skills/reverse-engineer-marketing', 'skills/competitor-profiling', 'skills/competitors', 'skills/marketing-plan', 'skills/copywriting') },
    @{ Repo = 'https://github.com/christianjohnston-ai/honeypot.git'; Sha = '90555b91b98cd6eccbe50fa251a83d60edeb7475'; Reviewed = '2026-11-24'
       Skills = @('honeypot-setup') },
    @{ Repo = 'https://github.com/mattpocock/skills.git'; Sha = 'd65391149dbb5fe76478e76fa8d5122b2aa5a70e'; Reviewed = '2026-11-24'
       Skills = @('skills/productivity/grill-me', 'skills/productivity/grilling') },
    @{ Repo = 'https://github.com/vercel-labs/skills.git'; Sha = '57217cf86ba38148a57af9e90d14a4c049558330'; Reviewed = '2026-11-24'
       Skills = @('skills/find-skills')
       # Upstream Step 6 installs with `npx skills add -g -y` (no confirmation, no review). Replace it with our process.
       Patch = @{ File = 'SKILL.md'; Find = '(?s)### Step 6: Offer to Install.*?(?=## Common Skill Categories)'; Replace = @'
### Step 6: Hand it to Noah's review process (never install directly)

Do NOT run `npx skills add`. Every skill on Noah's machines is read before it's installed and pinned to the reviewed commit.
If Noah wants one of the finds:
1. Clone its repo into a scratch folder and read the skill's SKILL.md and every script (network calls, logins, API keys, anything it runs).
2. Report in plain words what it does, what it touches, and any red flags; check name clashes in `~/.claude/skills` and `~/.claude-work/skills`.
3. Only after Noah says yes, add it to `C:\Users\nwnel\OneDrive\claude-skills\install-external-skills.ps1` pinned to that commit, run the installer, and note it in BACKLOG.md.

'@ } }
)
# Deliberately NOT installed: Panniantong/Agent-Reach (copies your Chrome logins for X/Reddit etc. into its own
# browser to scrape; account-ban and security risk). See BACKLOG.md #7.

if (-not $ConfigDirs) { $ConfigDirs = @("$HOME\.claude", "$HOME\.claude-work") | Where-Object { Test-Path $_ } }
$stage = Join-Path ([IO.Path]::GetTempPath()) ("ext-skills-" + [guid]::NewGuid().ToString('N').Substring(0, 8))
New-Item -ItemType Directory $stage | Out-Null
try {
    foreach ($s in $Sources) {
        $parts = $s.Repo -split '/'
        $name = ($parts[-2] + '__' + $parts[-1]) -replace '\.git$', ''
        $dir = Join-Path $stage $name
        git init -q $dir
        git -C $dir remote add origin $s.Repo
        git -C $dir fetch -q --depth 1 origin $s.Sha
        if ($LASTEXITCODE -ne 0) { throw "Could not fetch $($s.Repo) at $($s.Sha)" }
        git -C $dir -c advice.detachedHead=false checkout -q FETCH_HEAD
        foreach ($p in $s.Skills) {
            $from = Join-Path $dir ($p -replace '/', '\')
            if (-not (Test-Path (Join-Path $from 'SKILL.md'))) { throw "No SKILL.md at $p in $($s.Repo)" }
            $skill = Split-Path $from -Leaf
            Set-Content (Join-Path $from 'SOURCE.txt') "$($s.Repo)`r`ncommit $($s.Sha)`r`npath $p`r`nreviewed $($s.Reviewed)"
            if ($s.Patch) {
                $pf = Join-Path $from $s.Patch.File
                $before = Get-Content $pf -Raw
                $after = [regex]::Replace($before, $s.Patch.Find, $s.Patch.Replace)
                if ($after -eq $before) { throw "Patch did not apply to $p ($($s.Patch.File)); re-review upstream." }
                Set-Content $pf $after -NoNewline -Encoding utf8
                Add-Content (Join-Path $from 'SOURCE.txt') "patched locally: $($s.Patch.File) (see install-external-skills.ps1)"
            }
            $lic = Join-Path $dir 'LICENSE'
            if ((Test-Path $lic) -and -not (Test-Path (Join-Path $from 'LICENSE*'))) { Copy-Item $lic (Join-Path $from 'LICENSE.upstream') }
            foreach ($cfg in $ConfigDirs) {
                $dest = Join-Path $cfg "skills\$skill"
                if (Test-Path $dest) { Remove-Item $dest -Recurse -Force }
                New-Item -ItemType Directory (Split-Path $dest) -Force | Out-Null
                Copy-Item $from $dest -Recurse
            }
            Write-Host "Installed $skill  ($name @ $($s.Sha.Substring(0,7))) -> $($ConfigDirs -join ', ')"
        }
    }
}
finally { Remove-Item $stage -Recurse -Force -ErrorAction SilentlyContinue }
Write-Host "Start a new Claude Code session to pick up the skills."
