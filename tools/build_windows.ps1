Param(
  [switch]$OneFolder,
  [string]$Name = 'ABHub'
)

$ErrorActionPreference = 'Stop'

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
  Write-Error 'Python no está instalado en esta PC. Instálalo y vuelve a intentar.'
}

python -m pip install --upgrade pip > $null
python -m pip install pyinstaller pillow > $null

$pyArgs = @('--noconfirm','--windowed',"--name=$Name")
if ($OneFolder) { $pyArgs += '--onedir' } else { $pyArgs += '--onefile' }

# Incluir recursos necesarios
$pyArgs += @(
  '--add-data','src;src',
  '--add-data','Linea divisora.png;.',
  '--add-data','Vector.png;.'
)

pyinstaller @pyArgs panel_tareas.py

Write-Host "`nListo. Ejecutable en dist/$Name.exe (o carpeta $Name)."

