# Registers the Windows scheduled task "ACL Telegram listener": starts tools\tg_listener.py at logon and checks every
# 10 minutes that it is still running (never two at once). Runs only while you are logged on, with no window.
#   powershell -ExecutionPolicy Bypass -File tools\install_telegram_listener.ps1
# Stop it: powershell -ExecutionPolicy Bypass -File tools\stop_research.ps1   (stops research ticks and this listener)

$name   = 'ACL Telegram listener'
$action = New-ScheduledTaskAction -Execute 'C:\Python314\pythonw.exe' -Argument 'D:\acl\tools\tg_listener.py' `
          -WorkingDirectory 'D:\acl'
$atLogon = New-ScheduledTaskTrigger -AtLogOn -User "$env:USERDOMAIN\$env:USERNAME"
$every10 = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval (New-TimeSpan -Minutes 10) `
           -RepetitionDuration (New-TimeSpan -Days 3650)
$settings = New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Days 0) `
            -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive -RunLevel Limited
Register-ScheduledTask -TaskName $name -Action $action -Trigger @($atLogon, $every10) -Settings $settings `
    -Principal $principal -Description 'ACL: answers the creator''s Telegram messages (only theirs). Stop: tools\stop_research.ps1' `
    -Force | Out-Null
Remove-Item 'D:\acl\research\local\TG_OFF' -ErrorAction SilentlyContinue
Start-ScheduledTask -TaskName $name
"registered and started: $name"
