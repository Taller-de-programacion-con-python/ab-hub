Param(
  [Parameter(Mandatory=$true)][string]$ExePath,
  [string]$ShortcutName = 'ABHub'
)
$ErrorActionPreference = 'Stop'
$desktop = [Environment]::GetFolderPath('Desktop')
$lnk = Join-Path $desktop ("$ShortcutName.lnk")
$wsh = New-Object -ComObject WScript.Shell
$sc = $wsh.CreateShortcut($lnk)
$sc.TargetPath = (Resolve-Path $ExePath)
$sc.WorkingDirectory = Split-Path (Resolve-Path $ExePath)
$sc.WindowStyle = 1
$sc.Save()
Write-Host "Acceso directo creado: $lnk"
