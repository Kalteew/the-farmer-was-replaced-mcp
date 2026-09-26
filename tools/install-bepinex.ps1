$ErrorActionPreference = 'Stop'

$gameRoot = $env:TFWR_GAME_ROOT
if ([string]::IsNullOrWhiteSpace($gameRoot)) {
    $programFiles86 = [Environment]::GetEnvironmentVariable('ProgramFiles(x86)')
    $gameRoot = Join-Path $programFiles86 'Steam\steamapps\common\The Farmer Was Replaced'
}
$projectRoot = Split-Path -Parent $PSScriptRoot
$packageRoot = Join-Path $projectRoot '.deps\bepinex-5.4.23.5\package'
$plugin = Join-Path $projectRoot 'bridge\TFWRBridge\bin\Debug\net472\TFWRBridge.dll'

if (-not (Test-Path (Join-Path $gameRoot 'TheFarmerWasReplaced.exe'))) { throw "Jeu introuvable : $gameRoot" }
if (-not (Test-Path $packageRoot)) { throw 'Package BepInEx absent : lancez la préparation ou téléchargez BepInEx 5.4.23.5.' }
if (-not (Test-Path $plugin)) { throw 'Plugin non compilé : dotnet build bridge/TFWRBridge/TFWRBridge.csproj' }

Get-ChildItem -LiteralPath $packageRoot | ForEach-Object {
    Copy-Item -LiteralPath $_.FullName -Destination $gameRoot -Recurse -Force
}

$pluginRoot = Join-Path $gameRoot 'BepInEx\plugins'
New-Item -ItemType Directory -Path $pluginRoot -Force | Out-Null
Copy-Item -LiteralPath $plugin -Destination (Join-Path $pluginRoot 'TFWRBridge.dll') -Force
Write-Output "TFWR Bridge installé dans $pluginRoot"
