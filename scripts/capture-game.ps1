param(
  [Parameter(Mandatory = $true)]
  [string] $OutputPath
)

Add-Type -AssemblyName System.Drawing
Add-Type @'
using System;
using System.Runtime.InteropServices;
public struct TfwrRect {
  public int Left;
  public int Top;
  public int Right;
  public int Bottom;
}
public static class TfwrCaptureNative {
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr hWnd, out TfwrRect rect);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern void SwitchToThisWindow(IntPtr hWnd, bool fAltTab);
  [DllImport("user32.dll")] public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);
}
'@

$process = Get-Process -Name 'TheFarmerWasReplaced' -ErrorAction SilentlyContinue |
  Where-Object { $_.MainWindowHandle -ne 0 } |
  Select-Object -First 1

if ($null -eq $process) {
  throw 'The Farmer Was Replaced n''a pas de fenêtre active.'
}

[TfwrCaptureNative]::ShowWindow($process.MainWindowHandle, 9) | Out-Null
[TfwrCaptureNative]::keybd_event(0x12, 0, 0, [UIntPtr]::Zero)
[TfwrCaptureNative]::keybd_event(0x12, 0, 0x0002, [UIntPtr]::Zero)
[TfwrCaptureNative]::SetForegroundWindow($process.MainWindowHandle) | Out-Null
[TfwrCaptureNative]::SwitchToThisWindow($process.MainWindowHandle, $true)
Start-Sleep -Milliseconds 150

$rect = New-Object TfwrRect
if (-not [TfwrCaptureNative]::GetWindowRect($process.MainWindowHandle, [ref]$rect)) {
  throw 'Impossible de lire les dimensions de la fenêtre du jeu.'
}

$width = $rect.Right - $rect.Left
$height = $rect.Bottom - $rect.Top
if ($width -le 0 -or $height -le 0) {
  throw 'La fenêtre du jeu a une taille invalide.'
}

$bitmap = New-Object System.Drawing.Bitmap($width, $height)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
try {
  $graphics.CopyFromScreen($rect.Left, $rect.Top, 0, 0, $bitmap.Size)
  $bitmap.Save($OutputPath, [System.Drawing.Imaging.ImageFormat]::Png)
} finally {
  $graphics.Dispose()
  $bitmap.Dispose()
}

Write-Output ("captured {0}x{1}" -f $width, $height)
