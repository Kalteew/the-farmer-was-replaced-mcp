param(
    [string]$SaveName = "Save3"
)

$workspaceRoot = Split-Path -Parent $PSScriptRoot
$source = Join-Path $workspaceRoot ("game\{0}" -f $SaveName)
$saveRoot = Join-Path $env:USERPROFILE "AppData\LocalLow\TheFarmerWasReplaced\TheFarmerWasReplaced\Saves"
$destination = Join-Path $saveRoot $SaveName

if (-not (Test-Path -LiteralPath $source)) {
    throw "Dossier de code introuvable : $source"
}
if (-not (Test-Path -LiteralPath $destination)) {
    throw "Sauvegarde introuvable : $destination"
}

Get-ChildItem -LiteralPath $source -Filter *.py -File | ForEach-Object {
    Copy-Item -LiteralPath $_.FullName -Destination $destination -Force
    Write-Output ("Synchronisé : {0}" -f $_.Name)
}
