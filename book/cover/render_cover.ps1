# Render cover.svg to cover.png (1600 x 2400) with headless Edge.
#   powershell -File book\cover\render_cover.ps1
#   powershell -File book\cover\render_cover.ps1 -Svg other.svg -Png other.png     (an edition's cover)
param([string]$Svg = "", [string]$Png = "")
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$edge = @("${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe",
          "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe") | Where-Object { Test-Path $_ } | Select-Object -First 1
$page = Join-Path $here "cover_page.html"
$svgPath = if ($Svg) { (Resolve-Path $Svg).Path } else { Join-Path $here "cover.svg" }
$svg = Get-Content $svgPath -Raw
@"
<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;1,500&display=block" rel="stylesheet">
<style>html,body{margin:0;padding:0;background:#000;overflow:hidden}svg{display:block}</style></head>
<body>$svg</body></html>
"@ | Set-Content -Encoding utf8 $page
$out = if ($Png) { [System.IO.Path]::GetFullPath($Png) } else { Join-Path $here "cover.png" }
& $edge --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 `
  --window-size=1600,2400 --virtual-time-budget=8000 --screenshot="$out" "file:///$($page -replace '\\','/')" | Out-Null
Start-Sleep -Milliseconds 500
Remove-Item $page
Get-Item $out | Select-Object Name, Length
