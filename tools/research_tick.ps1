# One scheduled ACL research tick (Phase 1 of docs/proposal_autonomous_researcher_2026-10-30.md).
# Run by Windows Task Scheduler ("ACL research tick"), or by hand:  powershell -ExecutionPolicy Bypass -File tools\research_tick.ps1
# Order: STOP -> lock -> gate (free) -> budget -> a fresh `claude -p` session with a time limit -> record -> unlock.
# Three failed ticks in a row write research\PAUSE and send a problem message.
# A manual run can name its reason and skip the gate (STOP, lock and budget still apply):
#   powershell -ExecutionPolicy Bypass -File tools\research_tick.ps1 -Reason "demonstration: read-only status"
param([string]$Reason = '')

$ErrorActionPreference = 'Stop'
$root   = 'D:\acl'
$local  = Join-Path $root 'research\local'
$ticks  = Join-Path $local 'ticks'
$claude = 'C:\Users\User\.local\bin\claude.exe'
New-Item -ItemType Directory -Force $ticks | Out-Null
Set-Location $root

function Log($msg) { Add-Content -Path (Join-Path $local 'tick.log') -Value ("{0} {1}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $msg) -Encoding UTF8 }
function Notify($kind, $text) { & python tools\notify.py --kind $kind $text | Out-Null }

if (Test-Path (Join-Path $root 'research\STOP')) { Log 'STOP present: nothing done'; exit 0 }

# --- lock: one tick at a time ---
$lock = Join-Path $local 'lock.json'
if (Test-Path $lock) {
    try { $l = Get-Content $lock -Raw | ConvertFrom-Json } catch { $l = $null }
    if ($l -and (Get-Process -Id $l.pid -ErrorAction SilentlyContinue)) { Log "another tick is running (pid $($l.pid))"; exit 0 }
}
@{ pid = $PID; started = (Get-Date -Format 's') } | ConvertTo-Json | Set-Content $lock -Encoding UTF8

try {
    $state   = Get-Content (Join-Path $root 'research\state.json') -Raw | ConvertFrom-Json
    $timeout = [int]$state.budgets.tick_timeout_minutes
    $maxFail = [int]$state.budgets.failures_before_pause

    # --- gate: free; wakes Claude only when something changed ---
    if ($Reason) { $gate = [pscustomobject]@{ wake = $true; reasons = @($Reason) } }
    else {
        $gateRaw = & python tools\research_gate.py
        $gate = $gateRaw | ConvertFrom-Json
    }
    if (-not $gate.wake) { Log ("gate: no wake (" + ($gate.reasons -join '; ') + ")"); exit 0 }

    # --- budget ---
    $budFile = Join-Path $local 'budget.json'
    $today = Get-Date -Format 'yyyy-MM-dd'
    $bud = @{ date = $today; ticks = 0; failures = 0 }
    if (Test-Path $budFile) {
        $b = Get-Content $budFile -Raw | ConvertFrom-Json
        $bud.failures = [int]$b.failures
        if ($b.date -eq $today) { $bud.ticks = [int]$b.ticks }
    }
    $bud.ticks += 1
    $bud | ConvertTo-Json | Set-Content $budFile -Encoding UTF8

    # --- the session ---
    $stamp  = Get-Date -Format 'yyyyMMdd-HHmm'
    $prompt = Join-Path $ticks "$stamp.prompt.md"
    $outLog = Join-Path $ticks "$stamp.log"
    $errLog = Join-Path $ticks "$stamp.err"
    (Get-Content (Join-Path $root 'research\tick_prompt.md') -Raw) + "`r`n`r`nWhy this tick woke: " + ($gate.reasons -join '; ') |
        Set-Content $prompt -Encoding UTF8
    $allowed = @('Read', 'Glob', 'Grep', 'Edit', 'Write', 'Bash(python *)', 'Bash(git status*)', 'Bash(git add *)',
                 'Bash(git commit *)', 'Bash(git push*)', 'Bash(git log*)', 'Bash(git diff*)', 'Bash(cp *)',
                 'Bash(C:/Users/User/gh/bin/gh.exe run *)', 'PowerShell(Get-CimInstance *)', 'PowerShell(Copy-Item *)')
    $denied  = @('Edit(acl/**)', 'Edit(tests/**)', 'Edit(.github/**)',   # Edit rules cover every file-editing tool
                 'Bash(git push --force*)', 'Bash(git reset*)', 'Bash(git checkout*)',
                 'Bash(rm *)', 'Bash(C:/Users/User/gh/bin/gh.exe workflow*)', 'PowerShell(Remove-Item *)')
    $q = { param($a) '"' + $a + '"' }
    $argList = @('-p', '--permission-mode', 'dontAsk', '--output-format', 'text', '--allowedTools') +
               ($allowed | ForEach-Object { & $q $_ }) + @('--disallowedTools') + ($denied | ForEach-Object { & $q $_ })
    Log ("tick starts: " + ($gate.reasons -join '; '))
    $p = Start-Process -FilePath $claude -ArgumentList $argList -WorkingDirectory $root -NoNewWindow -PassThru `
         -RedirectStandardInput $prompt -RedirectStandardOutput $outLog -RedirectStandardError $errLog
    $null = $p.Handle                 # keeps the handle so ExitCode is readable after the wait
    $p.PriorityClass = 'BelowNormal'
    if (-not $p.WaitForExit($timeout * 60 * 1000)) {
        try { $p.Kill() } catch {}
        $ok = $false; Log "tick killed after $timeout minutes"
    } else {
        $ok = ($p.ExitCode -eq 0); Log "tick ended, exit code $($p.ExitCode)"
    }

    if ($ok) {
        $bud.failures = 0
        if ($gate.reasons -contains 'daily summary due') { $today | Set-Content (Join-Path $local 'summary_sent.txt') -Encoding UTF8 }
    } else {
        $bud.failures += 1
        if ($bud.failures -ge $maxFail) {
            "$(Get-Date -Format 'yyyy-MM-dd HH:mm') $($bud.failures) failed ticks in a row" | Set-Content (Join-Path $root 'research\PAUSE') -Encoding UTF8
            Notify 'problem' "ACL Researcher: $($bud.failures) research ticks failed in a row. Paused; logs in research\local\ticks. Nothing was deleted."
        }
    }
    $bud | ConvertTo-Json | Set-Content $budFile -Encoding UTF8
}
catch {
    Log ("wrapper error: " + $_.Exception.Message)
    Notify 'problem' 'ACL Researcher: the research tick wrapper hit an error; see research\local\tick.log.'
}
finally {
    Remove-Item $lock -ErrorAction SilentlyContinue
}
