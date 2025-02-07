
$action = New-ScheduledTaskAction -Execute 'pythonw.exe' -Argument 'C:/Users/rene/source/repos/Redirect/redirect.py start-server'
sleep 1
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval (New-TimeSpan -Minutes 1) -RepetitionDuration (New-TimeSpan -Hours 23 -Minutes 55)
sleep 1
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
sleep 1
Register-ScheduledTask -Action $action -Trigger $trigger -Settings $settings -TaskName 'Redirect Youtube' -Description 'Redirect Youtube'
sleep 1
    