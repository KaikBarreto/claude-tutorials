#!/usr/bin/env bash
# Monta cenas_v2.html (16:9) e cenas_v2_vertical.html (9:16) a partir dos moldes + cenas_v2.js. Rode de novo se mexer no molde.
cd "$(dirname "$0")" || exit 1
ICONS=$(grep -o "'[a-z][a-z0-9-]*'" cenas_v2.js | sort -u | tr '\n' ',')
{
  head -n 91 cenas_modelo.html | sed 's|</style></head>|.selo{display:inline-flex;align-items:center;gap:.45em;border-radius:6px;font-weight:800;color:#fff;white-space:nowrap;line-height:1;letter-spacing:.02em}.lbl{font-weight:800;line-height:1.12}.sub2{font-weight:600;color:var(--c);line-height:1.25}\n</style></head>|'
  echo "const V=false,BW=1280,BH=670;const ICON_NAMES=[${ICONS}];"
  echo '</script><script src="cenas_v2.js"></script><script>'
  echo 'let RENDER=null;window.setup=d=>{RENDER=window.setupCena(d);return true};window.R=t=>{RENDER(t);return true};'
  echo '</script></body></html>'
} > cenas_v2.html
{
  head -n 92 cenas_modelo_vertical.html
  echo "const V=true,BW=SEG.w,BH=SEG.h;const ICON_NAMES=[${ICONS}];"
  echo '</script><script src="cenas_v2.js"></script><script>'
  sed -n 111,123p cenas_modelo_vertical.html | sed 's#RENDER=CAPS\[d.cap\]();return true};#RENDER=window.setupCena(d);return true};#'
  echo 'window.R=t=>{RENDER(t);return true};'
  echo '</script></body></html>'
} > cenas_v2_vertical.html
sed -n 111,123p cenas_modelo_vertical.html | tail -6
