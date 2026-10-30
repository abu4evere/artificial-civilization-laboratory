# Registers the Windows scheduled task "ACL research tick" (Phase 1). It runs tools\research_tick.ps1 every hour at
# minute 7, only while you are logged on, never two at once, each for at most 1 hour.
#   powershell -ExecutionPolicy Bypass -File tools\install_research_task.ps1            # registered DISABLED
#   powershell -ExecutionPolicy Bypass -File tools\install_research_task.ps1 -Enable    # registered and running
# Stop everything at any time:  powershell -ExecutionPolicy Bypass -File tools\stop_research.ps1
param([switch]$Enable)

$name   = 'ACL research tick'
$action = New-ScheduledTaskAction -Execute 'powershell.exe' `
          -Argument '-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File D:\acl\tools\research_tick.ps1' `
          -WorkingDirectory 'D:\acl'
$start  = (Get-Date).Date.AddHours((Get-Date).Hour + 1).AddMinutes(7)
$trigger = New-ScheduledTaskTrigger -Once -At $start -RepetitionInterval (New-TimeSpan -Hours 1) `
           -RepetitionDuration (New-TimeSpan -Days 3650)
$settings = New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Hours 1) `
            -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive -RunLevel Limited
Register-ScheduledTask -TaskName $name -Action $action -Trigger $trigger -Settings $settings -Principal $principal `
    -Description 'ACL autonomous research: one bounded step per tick (D:\acl\research\README.md). Stop: tools\stop_research.ps1' `
    -Force | Out-Null
if ($Enable) { Enable-ScheduledTask -TaskName $name | Out-Null; "registered and ENABLED: first run $start" }
else { Disable-ScheduledTask -TaskName $name | Out-Null; "registered DISABLED (enable with -Enable, or in Task Scheduler)" }
