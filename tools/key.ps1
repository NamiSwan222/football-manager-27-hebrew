# Focus a process's window and press keys: key.ps1 <processName> <vk hex,vk hex,...> [delayMs]
# Refuses to press anything if the window could not be brought to the front (keys would go elsewhere).
param([string]$Name, [string]$Keys, [int]$Delay = 400)
Add-Type @"
using System; using System.Runtime.InteropServices;
public class K { [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
[DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
[DllImport("user32.dll")] public static extern void keybd_event(byte vk, byte sc, uint f, UIntPtr x);
[DllImport("user32.dll")] public static extern uint MapVirtualKey(uint c, uint t); }
"@
$p = Get-Process $Name | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
$h = $p.MainWindowHandle
[K]::keybd_event(0x12, 0, 0, [UIntPtr]::Zero); [K]::keybd_event(0x12, 0, 2, [UIntPtr]::Zero)
[K]::SetForegroundWindow($h) | Out-Null; Start-Sleep -Milliseconds 300
foreach ($k in $Keys.Split(',')) {
  if ([K]::GetForegroundWindow() -ne $h) { Write-Error "stopped: $Name is not the foreground window"; exit 1 }
  $vk = [Convert]::ToByte($k, 16); $sc = [byte][K]::MapVirtualKey($vk, 0)
  [K]::keybd_event($vk, $sc, 0, [UIntPtr]::Zero); Start-Sleep -Milliseconds 60
  [K]::keybd_event($vk, $sc, 2, [UIntPtr]::Zero); Start-Sleep -Milliseconds $Delay }
