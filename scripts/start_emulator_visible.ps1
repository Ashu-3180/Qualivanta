# Qualivanta: launch the Android Emulator and force its window onto the primary display.
# Usage: .\scripts\start_emulator_visible.ps1

$ErrorActionPreference = 'Stop'
$AvdName = 'Qualivanta_API_37'
$WindowWaitSeconds = 120

# Find the Android SDK without assuming a single installation location.
$sdkRoots = @(
    $env:ANDROID_HOME,
    $env:ANDROID_SDK_ROOT,
    (Join-Path $env:LOCALAPPDATA 'Android\Sdk')
) | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Select-Object -Unique

$emulatorExe = $null
foreach ($root in $sdkRoots) {
    $candidate = Join-Path $root 'emulator\emulator.exe'
    if (Test-Path -LiteralPath $candidate) {
        $emulatorExe = $candidate
        break
    }
}
if (-not $emulatorExe) {
    throw "Could not locate emulator.exe. Checked ANDROID_HOME, ANDROID_SDK_ROOT, and $env:LOCALAPPDATA\Android\Sdk."
}

# Load the small Win32 helper once per PowerShell session.
if (-not ('QualivantaEmulatorWindowFix' -as [type])) {
    Add-Type -TypeDefinition @'
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Text;

public static class QualivantaEmulatorWindowFix
{
    [StructLayout(LayoutKind.Sequential)]
    private struct RECT
    {
        public int Left;
        public int Top;
        public int Right;
        public int Bottom;
    }

    public class WindowInfo
    {
        public IntPtr Handle { get; set; }
        public int ProcessId { get; set; }
        public string ProcessName { get; set; }
        public string Title { get; set; }
        public int X { get; set; }
        public int Y { get; set; }
        public int Width { get; set; }
        public int Height { get; set; }
    }

    private delegate bool EnumWindowsProc(IntPtr hWnd, IntPtr lParam);

    [DllImport("user32.dll")]
    private static extern bool EnumWindows(EnumWindowsProc callback, IntPtr lParam);
    [DllImport("user32.dll")]
    private static extern bool IsWindowVisible(IntPtr hWnd);
    [DllImport("user32.dll", CharSet = CharSet.Unicode)]
    private static extern int GetWindowText(IntPtr hWnd, StringBuilder text, int maxCount);
    [DllImport("user32.dll")]
    private static extern int GetWindowTextLength(IntPtr hWnd);
    [DllImport("user32.dll")]
    private static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint processId);
    [DllImport("user32.dll")]
    private static extern bool GetWindowRect(IntPtr hWnd, out RECT rect);
    [DllImport("user32.dll")]
    private static extern bool ShowWindow(IntPtr hWnd, int command);
    [DllImport("user32.dll", SetLastError = true)]
    private static extern bool SetWindowPos(IntPtr hWnd, IntPtr insertAfter, int x, int y, int width, int height, uint flags);
    [DllImport("user32.dll")]
    private static extern bool SetForegroundWindow(IntPtr hWnd);

    public static WindowInfo[] FindEmulatorWindows()
    {
        List<WindowInfo> found = new List<WindowInfo>();
        EnumWindowsProc callback = delegate(IntPtr hWnd, IntPtr lParam)
        {
            if (!IsWindowVisible(hWnd)) return true;
            int length = GetWindowTextLength(hWnd);
            if (length <= 0) return true;

            StringBuilder titleBuffer = new StringBuilder(length + 1);
            GetWindowText(hWnd, titleBuffer, titleBuffer.Capacity);
            string title = titleBuffer.ToString();
            uint processId;
            GetWindowThreadProcessId(hWnd, out processId);

            string processName = "";
            try { processName = Process.GetProcessById((int)processId).ProcessName; }
            catch { return true; }

            bool looksLikeEmulator =
                processName.IndexOf("emulator", StringComparison.OrdinalIgnoreCase) >= 0 ||
                processName.IndexOf("qemu", StringComparison.OrdinalIgnoreCase) >= 0 ||
                title.IndexOf("Android Emulator", StringComparison.OrdinalIgnoreCase) >= 0;
            if (!looksLikeEmulator) return true;

            RECT rect;
            if (!GetWindowRect(hWnd, out rect)) return true;
            found.Add(new WindowInfo {
                Handle = hWnd,
                ProcessId = (int)processId,
                ProcessName = processName,
                Title = title,
                X = rect.Left,
                Y = rect.Top,
                Width = rect.Right - rect.Left,
                Height = rect.Bottom - rect.Top
            });
            return true;
        };

        EnumWindows(callback, IntPtr.Zero);
        GC.KeepAlive(callback);
        return found.ToArray();
    }

    public static bool RestoreAndMove(IntPtr hWnd, int x, int y, int width, int height)
    {
        const uint SWP_NOZORDER = 0x0004;
        const uint SWP_SHOWWINDOW = 0x0040;
        const int SW_RESTORE = 9;
        ShowWindow(hWnd, SW_RESTORE);
        bool moved = SetWindowPos(hWnd, IntPtr.Zero, x, y, width, height, SWP_NOZORDER | SWP_SHOWWINDOW);
        SetForegroundWindow(hWnd);
        return moved;
    }
}
'@
}

function Find-TargetEmulatorWindow {
    $windows = @([QualivantaEmulatorWindowFix]::FindEmulatorWindows())
    if ($windows.Count -eq 0) { return $null }

    $preferred = $windows | Where-Object { $_.Title -like "*$AvdName*" } | Select-Object -First 1
    if ($preferred) { return $preferred }

    $preferred = $windows | Where-Object {
        $_.ProcessName -match '^emulator$' -or $_.Title -match 'Android Emulator'
    } | Select-Object -First 1
    if ($preferred) { return $preferred }

    if ($windows.Count -eq 1) { return $windows[0] }
    return $windows[0]
}

# If the emulator isn't running, start it. If it's already open off-screen, just reposition it.
$target = Find-TargetEmulatorWindow
if (-not $target) {
    $running = Get-Process -Name 'emulator','qemu-system-x86_64' -ErrorAction SilentlyContinue
    if (-not $running) {
        Write-Host "Starting $AvdName..." -ForegroundColor Cyan
        Start-Process -FilePath $emulatorExe -ArgumentList @('-avd', $AvdName) | Out-Null
    } else {
        Write-Host 'Emulator process is already running; waiting for its window...' -ForegroundColor Cyan
    }

    $deadline = (Get-Date).AddSeconds($WindowWaitSeconds)
    do {
        Start-Sleep -Seconds 2
        $target = Find-TargetEmulatorWindow
    } until ($target -or (Get-Date) -ge $deadline)
}

if (-not $target) {
    throw "Could not find the emulator window within $WindowWaitSeconds seconds. Check that $AvdName starts normally in Android Studio."
}

Add-Type -AssemblyName System.Windows.Forms
$area = [System.Windows.Forms.Screen]::PrimaryScreen.WorkingArea
$margin = 20
$maxWidth = [Math]::Max(400, $area.Width - (2 * $margin))
$maxHeight = [Math]::Max(400, $area.Height - (2 * $margin))
$width = [Math]::Min([Math]::Max(400, $target.Width), $maxWidth)
$height = [Math]::Min([Math]::Max(400, $target.Height), $maxHeight)
$x = $area.Left + $margin
$y = $area.Top + $margin

$moved = [QualivantaEmulatorWindowFix]::RestoreAndMove($target.Handle, $x, $y, $width, $height)
if (-not $moved) {
    throw "Windows could not reposition the emulator window. Try running PowerShell as the same user that launched Android Studio."
}

Write-Host "`nEmulator window repositioned onto the primary display." -ForegroundColor Green
Write-Host "Window: $($target.Title)"
Write-Host "Position: x=$x, y=$y | Size: ${width}x${height}"
Write-Host 'Use this script to launch the emulator or bring an already-running emulator back on-screen.' -ForegroundColor Cyan
