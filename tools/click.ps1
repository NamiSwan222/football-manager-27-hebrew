# Click inside a process's window at window-relative pixel coords: click.ps1 <processName> <x> <y>
# Brings the window to the front first (Alt-key trick so Windows allows it) and refuses to click if it
# is still not the foreground window, so a click never lands in some other program.
param([string]$Name, [int]$X, [int]$Y)
Add-Type @"
using System; using System.Runtime.InteropServices;
public class C { [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
[DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
[DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int c);
[DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out R r);
[DllImport("user32.dll")] public static extern bool SetCursorPos(int x, int y);
[DllImport("user32.dll")] public static extern void keybd_event(byte vk, byte sc, uint f, UIntPtr x);
[DllImport("user32.dll")] public static extern void mouse_event(uint f, int x, int y, uint d, UIntPtr e);
public struct R { public int L, T, Ri, B; } }
"@
$p = Get-Process $Name | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
$h = $p.MainWindowHandle
[C]::keybd_event(0x12, 0, 0, [UIntPtr]::Zero); [C]::keybd_event(0x12, 0, 2, [UIntPtr]::Zero)
[C]::ShowWindow($h, 9) | Out-Null; [C]::SetForegroundWindow($h) | Out-Null; Start-Sleep -Milliseconds 400
if ([C]::GetForegroundWindow() -ne $h) { Write-Error "not clicked: $Name is not the foreground window"; exit 1 }
$r = New-Object C+R; [C]::GetWindowRect($h, [ref]$r) | Out-Null
[C]::SetCursorPos($r.L + $X, $r.T + $Y) | Out-Null; Start-Sleep -Milliseconds 100
[C]::mouse_event(2, 0, 0, 0, [UIntPtr]::Zero); Start-Sleep -Milliseconds 60; [C]::mouse_event(4, 0, 0, 0, [UIntPtr]::Zero)
