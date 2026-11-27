# Capture a window by process name with PrintWindow (works even when another window is on top).
# powershell -File shot.ps1 <processName> <out.png>
param([string]$Name, [string]$Out)
Add-Type -AssemblyName System.Drawing
Add-Type @"
using System; using System.Runtime.InteropServices;
public class W { [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
[DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr dc, uint f);
public struct RECT { public int L, T, R, B; } }
"@
$p = Get-Process $Name | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
$r = New-Object W+RECT; [W]::GetWindowRect($p.MainWindowHandle, [ref]$r) | Out-Null
$bmp = New-Object System.Drawing.Bitmap ($r.R - $r.L), ($r.B - $r.T)
$g = [System.Drawing.Graphics]::FromImage($bmp); $dc = $g.GetHdc()
[W]::PrintWindow($p.MainWindowHandle, $dc, 3) | Out-Null; $g.ReleaseHdc($dc)
$bmp.Save($Out); "saved $($bmp.Width)x$($bmp.Height)"
