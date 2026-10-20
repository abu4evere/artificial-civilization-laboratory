# Render the KDP covers (made by make_kdp_covers.py) to PNG with headless Edge, with the cover's web font.
#   powershell -File drafts\book_rewrite\kdp\render_kdp_covers.ps1 -W 3734 -H 2775
param([int]$W = 3734, [int]$H = 2775)
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$edge = @("${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe",
          "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe") | Where-Object { Test-Path $_ } | Select-Object -First 1
function Render($svgName, $pngName, $w, $h) {
  $svg = Get-Content (Join-Path $here $svgName) -Raw -Encoding UTF8
  $page = Join-Path $here "_render.html"
  @"
<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400;1,500&display=block" rel="stylesheet">
<style>html,body{margin:0;padding:0;background:#000;overflow:hidden}svg{display:block}</style></head>
<body>$svg</body></html>
"@ | Set-Content -Encoding utf8 $page
  $out = Join-Path $here $pngName
  & $edge --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 `
    --window-size=$w,$h --virtual-time-budget=10000 --screenshot="$out" "file:///$($page -replace '\\','/')" | Out-Null
  Start-Sleep -Milliseconds 800
}
Render "paperback_cover.svg" "paperback_cover.png" $W $H
Render "kindle_cover.svg" "kindle_cover.png" 1600 2560
