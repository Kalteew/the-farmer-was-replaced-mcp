param(
  [Parameter(Mandatory = $true)]
  [ValidateSet('F5', 'Shift+F5', 'Ctrl+F5', 'Ctrl+S')]
  [string] $Key
)

Add-Type @'
using System;
using System.Runtime.InteropServices;
public static class TfwrNative {
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
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

[TfwrNative]::ShowWindow($process.MainWindowHandle, 9) | Out-Null
[TfwrNative]::keybd_event(0x12, 0, 0, [UIntPtr]::Zero)
[TfwrNative]::keybd_event(0x12, 0, 0x0002, [UIntPtr]::Zero)
[TfwrNative]::SetForegroundWindow($process.MainWindowHandle) | Out-Null
[TfwrNative]::SwitchToThisWindow($process.MainWindowHandle, $true)
Start-Sleep -Milliseconds 100

$vkF5 = [byte]0x74
$vkS = [byte]0x53
$vkShift = [byte]0x10
$vkControl = [byte]0x11
$keyUp = [uint32]0x0002

if ($Key -eq 'Ctrl+S') {
  [TfwrNative]::keybd_event($vkControl, 0, 0, [UIntPtr]::Zero)
  [TfwrNative]::keybd_event($vkS, 0, 0, [UIntPtr]::Zero)
  [TfwrNative]::keybd_event($vkS, 0, $keyUp, [UIntPtr]::Zero)
  [TfwrNative]::keybd_event($vkControl, 0, $keyUp, [UIntPtr]::Zero)
} else {
  if ($Key -eq 'Shift+F5') { [TfwrNative]::keybd_event($vkShift, 0, 0, [UIntPtr]::Zero) }
  if ($Key -eq 'Ctrl+F5') { [TfwrNative]::keybd_event($vkControl, 0, 0, [UIntPtr]::Zero) }
  [TfwrNative]::keybd_event($vkF5, 0, 0, [UIntPtr]::Zero)
  [TfwrNative]::keybd_event($vkF5, 0, $keyUp, [UIntPtr]::Zero)
  if ($Key -eq 'Shift+F5') { [TfwrNative]::keybd_event($vkShift, 0, $keyUp, [UIntPtr]::Zero) }
  if ($Key -eq 'Ctrl+F5') { [TfwrNative]::keybd_event($vkControl, 0, $keyUp, [UIntPtr]::Zero) }
}

Write-Output "sent $Key"
