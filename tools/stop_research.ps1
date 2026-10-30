# Emergency stop for autonomous ACL research (Phase 1). Safe and reversible; deletes nothing.
#   powershell -ExecutionPolicy Bypass -File tools\stop_research.ps1
# 1. writes research\STOP (no tick does any work while it exists);
# 2. disables the scheduled task "ACL research tick";
# 3. lists running cloud runs (cancel one with: C:\Users\User\gh\bin\gh.exe run cancel <id> -R abu4evere/artificial-civilization-laboratory).
# Undo: delete research\STOP and run tools\install_research_task.ps1 -Enable.

"$(Get-Date -Format 'yyyy-MM-dd HH:mm') stopped by tools\stop_research.ps1" | Set-Content 'D:\acl\research\STOP' -Encoding UTF8
try { Disable-ScheduledTask -TaskName 'ACL research tick' -ErrorAction Stop | Out-Null; 'scheduled task disabled' }
catch { 'no scheduled task to disable' }
'STOP file written: no research tick will do any work.'
'Cloud runs still in progress (not cancelled automatically):'
& 'C:\Users\User\gh\bin\gh.exe' run list -R abu4evere/artificial-civilization-laboratory -w cloud-run -s in_progress -L 5
