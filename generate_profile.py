#!/usr/bin/env python3
"""
Cyberpunk Terminal Profile Banner & Portfolio Generator
Designed for GitHub Profile README (Abdallah Shehawey / Terminal Hacker Style)
Author: 0xsabry (Mohamed Sabry Hamdan)
"""

import os
import re
import html
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

# ==========================================
# CONFIGURATION
# ==========================================
CONFIG = {
    # Identity
    "name": "Mohamed Sabry Hamdan",
    "handle": "0xsabry",
    "prompt_user": "0xsabry@soc",
    "status": "HUNTING",  # Top-right live badge (e.g. HUNTING, MONITORING, BUILDING)
    
    # Profile Card Metadata
    "role": "SOC Analyst & DFIR Specialist",
    "based": "Cairo, Egypt",
    "mode": "Threat Hunting / SIEM / Incident Response",
    "writes": "0xsabry.github.io / Notes from the SOC",
    
    # Section 1: Focus Areas
    "section1_title": "- SOC.STACK",
    "section1_rows": [
        ("SIEM:", "Wazuh, FortiSIEM, FortiAnalyzer, Splunk"),
        ("EDR:", "Microsoft Defender, CrowdStrike, Velociraptor"),
        ("DFIR:", "Volatility, Autopsy, FTK Imager, Wireshark"),
        ("Intel:", "MITRE ATT&CK, Sigma, STIX 2.1, FortiGuard"),
    ],
    
    # Section 2: Toolchain
    "section2_title": "- TOOLCHAIN",
    "section2_rows": [
        ("Code:", "Python, Bash, PowerShell, C/C++, SQL"),
        ("Tools:", "ThreatScopeX, IR-Report-Gen, Suricata, Zeek"),
        ("Network:", "Cisco Packet Tracer, OSPF, VLANs, ACLs"),
        ("Infra:", "Linux, Windows Server, Docker, Git, CI/CD"),
    ],
    
    # Footer Banner Motto & Tags
    "motto": "DEFENSIVE ENGINEERING & PROACTIVE THREAT HUNTING",
    "bottom_tags": "SOC OPERATIONS  /  DFIR  /  THREAT HUNTING  /  SECURITY ENGINEERING",
    
    # Links & Socials
    "github_url": "https://github.com/0xsabry",
    "linkedin_url": "https://www.linkedin.com/in/mohamed-sabry-hamdan/",
    "portfolio_url": "https://0xsabry.github.io/soc-lab-project/",
    "academy_url": "https://www.linkedin.com/company/zero-2-aura/",
    "email": "2201381@student.eelu.edu.eg",
    
    # Source Avatar
    "avatar_path": "assets/avatar.png"
}

# XML-safe character ramp ordered from lightest/sparse to densest
ASCII_RAMP = " .`'~!-+*=/|ltvsnaxzCLTYJXmOwZkdbhpqwmkMB8Q@$"

# Desktop grid constants
COLS = 84
ROWS = 82
X_START = 28.0
DX = 3.76
Y_START = 80.09
DY = 4.99


def process_image_to_ascii(image_path, target_cols=84, target_rows=82):
    """
    Converts source image to a 2D matrix of ASCII characters with enhanced contrast
    tuned for cyberpunk dark mode portrait representation.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Avatar image not found at: {image_path}")

    img = Image.open(image_path).convert('RGB')
    w, h = img.size

    # Target aspect ratio for character grid (3:4 portrait)
    target_aspect = (target_cols * DX) / (target_rows * DY)
    current_aspect = w / h

    if current_aspect > target_aspect:
        new_w = int(h * target_aspect)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    else:
        new_h = int(w / target_aspect)
        top = (h - new_h) // 2
        img = img.crop((0, top, w, top + new_h))

    # Grayscale + Contrast stretch + Sharpness
    gray = img.convert('L')
    gray = ImageOps.autocontrast(gray, cutoff=2)
    gray = ImageEnhance.Contrast(gray).enhance(1.75)
    gray = ImageEnhance.Sharpness(gray).enhance(2.2)

    # Resize to exact character matrix
    resized = gray.resize((target_cols, target_rows), Image.Resampling.LANCZOS)
    pixels = np.array(resized)

    # Map pixels to character ramp
    ascii_grid = []
    for r in range(target_rows):
        row_chars = []
        for c in range(target_cols):
            val = pixels[r, c]
            idx = int((val / 255.0) * (len(ASCII_RAMP) - 1))
            row_chars.append(ASCII_RAMP[idx])
        ascii_grid.append(row_chars)

    return ascii_grid


def generate_desktop_banner_svg(ascii_grid, cfg):
    """Generates the 900x556 Desktop SVG Terminal Card."""
    art_lines = []
    for r, row in enumerate(ascii_grid):
        y_pos = Y_START + r * DY
        x_positions = []
        chars = []
        for c, ch in enumerate(row):
            if ch != ' ':
                x_pos = X_START + c * DX
                x_positions.append(f"{x_pos:.2f}".rstrip('0').rstrip('.'))
                chars.append(ch)
        if chars:
            x_str = " ".join(x_positions)
            content_str = "".join(chars)
            content_str = html.escape(content_str, quote=False)
            art_lines.append(f'      <text x="{x_str}" y="{y_pos:.2f}">{content_str}</text>')

    art_block = "\n".join(art_lines)

    def make_kv_row(key, val, y_text, y_line):
        return f'''      <text class="k" x="394" y="{y_text}">{key}</text>
      <line class="ld" x1="478" y1="{y_line}" x2="530" y2="{y_line}"/>
      <text class="v" x="538" y="{y_text}">{html.escape(val)}</text>'''

    right_rows = []
    right_rows.append(make_kv_row("Name:", cfg["name"], 124, 121))
    right_rows.append(make_kv_row("Role:", cfg["role"], 144, 141))
    right_rows.append(make_kv_row("Based:", cfg["based"], 164, 161))
    right_rows.append(make_kv_row("Mode:", cfg["mode"], 184, 181))
    right_rows.append(make_kv_row("Writes:", cfg["writes"], 204, 201))

    # Section 1
    right_rows.append(f'      <text class="sc" x="384" y="240">{cfg["section1_title"]}</text>')
    y_t, y_l = 260, 257
    for k, v in cfg["section1_rows"]:
        right_rows.append(make_kv_row(k, v, y_t, y_l))
        y_t += 20
        y_l += 20

    # Section 2
    right_rows.append(f'      <text class="sc" x="384" y="356">{cfg["section2_title"]}</text>')
    y_t, y_l = 376, 373
    for k, v in cfg["section2_rows"]:
        right_rows.append(make_kv_row(k, v, y_t, y_l))
        y_t += 20
        y_l += 20

    right_rows_str = "\n".join(right_rows)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="556"
     viewBox="0 0 900 556" role="img"
     aria-label="{html.escape(cfg["name"])} - {html.escape(cfg["role"])}">
  <title>{html.escape(cfg["name"])} - {html.escape(cfg["role"])}</title>

  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0d1117"/><stop offset="1" stop-color="#161b22"/>
    </linearGradient>
    <linearGradient id="edge" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#8b949e"/>
      <stop offset="0.48" stop-color="#58a6ff"/>
      <stop offset="1" stop-color="#8b949e"/>
    </linearGradient>
    <linearGradient id="ink" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#f0f6fc"/><stop offset="1" stop-color="#79c0ff"/>
    </linearGradient>
    <linearGradient id="scan" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#58a6ff" stop-opacity="0"/>
      <stop offset="0.5" stop-color="#58a6ff" stop-opacity="0.46"/>
      <stop offset="1" stop-color="#8b949e" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="halo">
      <stop offset="0" stop-color="#58a6ff" stop-opacity="0.12"/>
      <stop offset="0.48" stop-color="#c9d1d9" stop-opacity="0.055"/>
      <stop offset="1" stop-color="#8b949e" stop-opacity="0"/>
    </radialGradient>
    <pattern id="scanlines" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect width="4" height="1" fill="#58a6ff" opacity="0.052"/>
    </pattern>
    <pattern id="grid" width="44" height="44" patternUnits="userSpaceOnUse">
      <path d="M 44 0 H 0 V 44" fill="none" stroke="#c9d1d9" stroke-width="0.65" opacity="0.085"/>
      <circle cx="0" cy="0" r="1.2" fill="#58a6ff" opacity="0.13"/>
    </pattern>
    <clipPath id="card"><rect x="3" y="3" width="894" height="550" rx="16"/></clipPath>
    <clipPath id="portrait"><rect x="14" y="46" width="344" height="454" rx="12"/></clipPath>
  </defs>

  <style>
    text {{ font-family: ui-monospace,'SF Mono','JetBrains Mono','Fira Code','DejaVu Sans Mono',Menlo,Consolas,monospace; white-space: pre; }}
    .bar  {{ font-size: 10.5px;  fill: #8b949e; }}
    .lbl  {{ font-size: 8.5px;  fill: #6e7b8b; letter-spacing: 1.5px; }}
    .art  {{ font-size: 4.79px; fill: url(#ink); }}
    .hd   {{ font-size: 12px;   fill: #f0f6fc; font-weight: 600; }}
    .sc   {{ font-size: 10.5px;   fill: #8b949e; letter-spacing: 0.6px; }}
    .k    {{ font-size: 12px;   fill: #58a6ff; font-weight: 600; }}
    .v    {{ font-size: 12px;   fill: #c9d1d9; }}
    .rl   {{ stroke: #30363d; stroke-width: 1; }}
    .ld   {{ stroke: #3d4855; stroke-width: 1; stroke-dasharray: 1.5 3.5; stroke-linecap: round; }}
    .foot {{ font-size: 9px; fill: #6e7b8b; letter-spacing: 2.2px; }}
    .live {{ font-size: 9px; fill: #58a6ff; letter-spacing: 1.6px; }}
    .tg   {{ font-size: 9px;   fill: #8b949e; letter-spacing: 1.8px; }}
    .orbit {{ transform-box: view-box; }}

    @keyframes scan  {{ from {{ transform: translateY(0); }} to {{ transform: translateY(646px); }} }}
    @keyframes spin  {{ to {{ transform: rotate(360deg); }} }}
    @keyframes rspin {{ to {{ transform: rotate(-360deg); }} }}
    @keyframes blink {{ 0%,49% {{ opacity: 1 }} 50%,100% {{ opacity: 0 }} }}
    @keyframes pulse {{ 0%,100% {{ opacity: 1 }} 50% {{ opacity: 0.25 }} }}

    @media (prefers-reduced-motion: no-preference) {{
      .motion-scan {{ animation: scan 8s linear infinite; }}
      .orbit--fwd  {{ animation: spin 42s linear infinite; }}
      .orbit--rev  {{ animation: rspin 34s linear infinite; }}
      .blink       {{ animation: blink 1.15s steps(1) infinite; }}
      .pulse       {{ animation: pulse 2.4s ease-in-out infinite; }}
    }}
    @media (prefers-reduced-motion: reduce) {{ .motion-scan {{ display: none; }} }}
  </style>

  <rect width="900" height="556" rx="18" fill="url(#bg)"/>
  <rect width="900" height="556" rx="18" fill="url(#scanlines)"/>
  <rect x="3" y="3" width="894" height="34" rx="16" fill="#161b22" fill-opacity="0.84"/>

  <g clip-path="url(#card)">
    <g clip-path="url(#portrait)">
      <rect x="14" y="46" width="344" height="454" fill="url(#grid)"/>
    </g>
    <ellipse cx="186" cy="273" rx="168.56" ry="217.92" fill="url(#halo)"/>
    <ellipse class="orbit orbit--fwd" style="transform-origin:186px 273px"
             cx="186" cy="273" rx="151.36" ry="199.76" fill="none"
             stroke="#c9d1d9" stroke-width="1" stroke-dasharray="3 14" opacity="0.13"/>
    <ellipse class="orbit orbit--rev" style="transform-origin:186px 273px"
             cx="186" cy="273" rx="116.96" ry="154.36" fill="none"
             stroke="#8b949e" stroke-width="1" stroke-dasharray="28 24" opacity="0.10"/>

    <rect x="14" y="46" width="344" height="454" rx="12" fill="#161b22"
          fill-opacity="0.38" stroke="url(#edge)" stroke-opacity="0.42"/>
    <text class="lbl" x="26" y="64">PORTRAIT / {html.escape(cfg["name"].upper())}</text>
    <g class="art">
{art_block}
    </g>

    <text class="lbl" x="384" y="64">PROFILE / SOC ANALYST</text>
    <rect x="372" y="46" width="514" height="454" rx="12" fill="#161b22"
          fill-opacity="0.38" stroke="url(#edge)" stroke-opacity="0.42"/>
    <text class="hd" x="384" y="104">{html.escape(cfg["prompt_user"])}</text>
{right_rows_str}
      <text class="tg" x="384" y="478">{html.escape(cfg["motto"])}</text>

    <rect class="motion-scan" x="0" y="-90" width="900" height="90"
          fill="url(#scan)" opacity="0.42" style="mix-blend-mode:screen"/>
  </g>

  <circle cx="24" cy="17" r="4.5" fill="#58a6ff" opacity="0.88"/>
  <circle cx="42" cy="17" r="4.5" fill="#8b949e" opacity="0.70"/>
  <circle cx="60" cy="17" r="4.5" fill="#8b949e" opacity="0.78"/>
  <text class="bar" x="450" y="20.5" text-anchor="middle">{html.escape(cfg["prompt_user"])}  ~  %  ./profile<tspan class="blink" fill="#58a6ff"> &#9608;</tspan></text>
  <circle class="pulse" cx="797" cy="17" r="3.4" fill="#58a6ff"/>
  <text class="live" x="808" y="20.5">{html.escape(cfg["status"])}</text>

  <line x1="3" y1="516" x2="897" y2="516" stroke="#30363d"/>
  <text class="foot" x="450" y="540" text-anchor="middle">{html.escape(cfg["bottom_tags"])}</text>

  <rect x="3" y="3" width="894" height="550" rx="16" fill="none"
        stroke="url(#edge)" stroke-width="2" opacity="0.76"/>
</svg>
'''
    return svg


def generate_mobile_banner_svg(ascii_grid, cfg):
    """Generates the 440x940 Mobile-Optimized SVG Terminal Card."""
    colors = [
        "#e9f3fc", "#daecfd", "#cbe5fd", "#bcdefd",
        "#add8fe", "#9ed1fe", "#8fcafe", "#80c3ff", "#71bcff"
    ]
    batch_size = 10
    mobile_art_blocks = []

    for b_idx in range(0, len(ascii_grid), batch_size):
        color = colors[min(b_idx // batch_size, len(colors) - 1)]
        batch_lines = []
        for r_offset, row in enumerate(ascii_grid[b_idx:b_idx + batch_size]):
            r = b_idx + r_offset
            y_pos = 74.04 + r * 4.93
            line_str = "".join(row)
            line_str = html.escape(line_str.rstrip(), quote=False)
            batch_lines.append(
                f'      <tspan x="64.00" y="{y_pos:.2f}" textLength="312.00" lengthAdjust="spacingAndGlyphs" xml:space="preserve">{line_str}</tspan>'
            )
        mobile_art_blocks.append(
            f'    <text class="art" fill="{color}">\n' + "\n".join(batch_lines) + '\n    </text>'
        )

    art_block_str = "\n".join(mobile_art_blocks)

    def make_mobile_kv(key, val, y_pos):
        return f'''      <text class="k" x="30" y="{y_pos}">{key}</text>
      <line class="ld" x1="112" y1="{y_pos-3:.1f}" x2="148" y2="{y_pos-3:.1f}"/>
      <text class="v" x="156" y="{y_pos}">{html.escape(val)}</text>'''

    m_rows = []
    m_rows.append(make_mobile_kv("Name:", cfg["name"], 542.0))
    m_rows.append(make_mobile_kv("Role:", cfg["role"], 562.4))
    m_rows.append(make_mobile_kv("Based:", cfg["based"], 582.8))
    m_rows.append(make_mobile_kv("Mode:", cfg["mode"], 603.2))
    m_rows.append(make_mobile_kv("Writes:", cfg["writes"], 623.6))

    # Section 1
    m_rows.append(f'      <text class="sc" x="20" y="659.0">{cfg["section1_title"]}</text>')
    y_curr = 679.4
    for k, v in cfg["section1_rows"]:
        m_rows.append(make_mobile_kv(k, v, y_curr))
        y_curr += 20.4

    # Section 2
    m_rows.append(f'      <text class="sc" x="20" y="765.0">{cfg["section2_title"]}</text>')
    y_curr = 785.4
    for k, v in cfg["section2_rows"]:
        m_rows.append(make_mobile_kv(k, v, y_curr))
        y_curr += 20.4

    m_rows_str = "\n".join(m_rows)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="440" height="940"
     viewBox="0 0 440 940" role="img"
     aria-label="{html.escape(cfg["name"])} - {html.escape(cfg["role"])}">
  <title>{html.escape(cfg["name"])} - {html.escape(cfg["role"])}</title>

  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0d1117"/><stop offset="1" stop-color="#161b22"/>
    </linearGradient>
    <linearGradient id="edge" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#8b949e"/>
      <stop offset="0.48" stop-color="#58a6ff"/>
      <stop offset="1" stop-color="#8b949e"/>
    </linearGradient>
    <linearGradient id="scan" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#58a6ff" stop-opacity="0"/>
      <stop offset="0.5" stop-color="#58a6ff" stop-opacity="0.46"/>
      <stop offset="1" stop-color="#8b949e" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="halo">
      <stop offset="0" stop-color="#58a6ff" stop-opacity="0.12"/>
      <stop offset="0.48" stop-color="#c9d1d9" stop-opacity="0.055"/>
      <stop offset="1" stop-color="#8b949e" stop-opacity="0"/>
    </radialGradient>
    <pattern id="scanlines" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect width="4" height="1" fill="#58a6ff" opacity="0.052"/>
    </pattern>
    <pattern id="grid" width="44" height="44" patternUnits="userSpaceOnUse">
      <path d="M 44 0 H 0 V 44" fill="none" stroke="#c9d1d9" stroke-width="0.65" opacity="0.085"/>
      <circle cx="0" cy="0" r="1.2" fill="#58a6ff" opacity="0.13"/>
    </pattern>
    <clipPath id="card"><rect x="3" y="3" width="434" height="934" rx="16"/></clipPath>
    <clipPath id="portrait"><rect x="10" y="42" width="420" height="430" rx="12"/></clipPath>
  </defs>

  <style>
    text {{ font-family: ui-monospace,'SF Mono','JetBrains Mono','Fira Code','DejaVu Sans Mono',Menlo,Consolas,monospace; }}
    .bar  {{ font-size: 10px;    fill: #8b949e; }}
    .lbl  {{ font-size: 8.5px;   fill: #6e7b8b; letter-spacing: 1.5px; }}
    .art  {{ font-size: 4.8px;   white-space: pre; }}
    .hd   {{ font-size: 11.5px;  fill: #f0f6fc; font-weight: 600; }}
    .sc   {{ font-size: 10px;    fill: #8b949e; letter-spacing: 0.6px; }}
    .k    {{ font-size: 11px;    fill: #58a6ff; font-weight: 600; }}
    .v    {{ font-size: 11px;    fill: #c9d1d9; }}
    .ld   {{ stroke: #3d4855; stroke-width: 1; stroke-dasharray: 1.5 3.5; stroke-linecap: round; }}
    .foot {{ font-size: 8.5px;   fill: #6e7b8b; letter-spacing: 1.8px; }}
    .live {{ font-size: 8.5px;   fill: #58a6ff; letter-spacing: 1.6px; }}
    .tg   {{ font-size: 8.5px;   fill: #8b949e; letter-spacing: 1.4px; }}
    .orbit {{ transform-box: view-box; }}

    @keyframes scan  {{ from {{ transform: translateY(0); }} to {{ transform: translateY(1030px); }} }}
    @keyframes spin  {{ to {{ transform: rotate(360deg); }} }}
    @keyframes rspin {{ to {{ transform: rotate(-360deg); }} }}
    @keyframes blink {{ 0%,49% {{ opacity: 1 }} 50%,100% {{ opacity: 0 }} }}
    @keyframes pulse {{ 0%,100% {{ opacity: 1 }} 50% {{ opacity: 0.25 }} }}

    @media (prefers-reduced-motion: no-preference) {{
      .motion-scan {{ animation: scan 8s linear infinite; }}
      .orbit--fwd  {{ animation: spin 42s linear infinite; }}
      .orbit--rev  {{ animation: rspin 34s linear infinite; }}
      .blink       {{ animation: blink 1.15s steps(1) infinite; }}
      .pulse       {{ animation: pulse 2.4s ease-in-out infinite; }}
    }}
    @media (prefers-reduced-motion: reduce) {{ .motion-scan {{ display: none; }} }}
  </style>

  <rect width="440" height="940" rx="18" fill="url(#bg)"/>
  <rect width="440" height="940" rx="18" fill="url(#scanlines)"/>
  <rect x="3" y="3" width="434" height="30" rx="16" fill="#161b22" fill-opacity="0.84"/>

  <g clip-path="url(#card)">
    <g clip-path="url(#portrait)">
      <rect x="10" y="42" width="420" height="430" fill="url(#grid)"/>
    </g>
    <ellipse cx="220" cy="256" rx="150" ry="180" fill="url(#halo)"/>
    <ellipse class="orbit orbit--fwd" style="transform-origin:220px 256px"
             cx="220" cy="256" rx="140" ry="165" fill="none"
             stroke="#c9d1d9" stroke-width="1" stroke-dasharray="3 14" opacity="0.13"/>
    <ellipse class="orbit orbit--rev" style="transform-origin:220px 256px"
             cx="220" cy="256" rx="105" ry="125" fill="none"
             stroke="#8b949e" stroke-width="1" stroke-dasharray="28 24" opacity="0.10"/>

    <rect x="10" y="42" width="420" height="430" rx="12" fill="#161b22"
          fill-opacity="0.38" stroke="url(#edge)" stroke-opacity="0.42"/>
    <text class="lbl" x="22" y="58">PORTRAIT / {html.escape(cfg["name"].upper())}</text>
{art_block_str}

    <text class="lbl" x="20" y="492">PROFILE / SOC ANALYST</text>
    <rect x="10" y="480" width="420" height="402" rx="12" fill="#161b22"
          fill-opacity="0.38" stroke="url(#edge)" stroke-opacity="0.42"/>
    <text class="hd" x="20" y="522">{html.escape(cfg["prompt_user"])}</text>
{m_rows_str}
      <text class="tg" x="20" y="862.8">{html.escape(cfg["motto"])}</text>

    <rect class="motion-scan" x="0" y="-90" width="440" height="90"
          fill="url(#scan)" opacity="0.42" style="mix-blend-mode:screen"/>
  </g>

  <circle cx="24" cy="15" r="4.5" fill="#58a6ff" opacity="0.88"/>
  <circle cx="42" cy="15" r="4.5" fill="#8b949e" opacity="0.70"/>
  <circle cx="60" cy="15" r="4.5" fill="#8b949e" opacity="0.78"/>
  <text class="bar" x="196" y="18.5" text-anchor="middle">{html.escape(cfg["prompt_user"])}  ~  %  ./profile<tspan class="blink" fill="#58a6ff"> &#9608;</tspan></text>
  <circle class="pulse" cx="326" cy="15" r="3.4" fill="#58a6ff"/>
  <text class="live" x="336" y="18.5">{html.escape(cfg["status"])}</text>

  <line x1="3" y1="898" x2="437" y2="898" stroke="#30363d"/>
  <text class="foot" x="220" y="920" text-anchor="middle">{html.escape(cfg["bottom_tags"])}</text>

  <rect x="3" y="3" width="434" height="934" rx="16" fill="none"
        stroke="url(#edge)" stroke-width="2" opacity="0.76"/>
</svg>
'''
    return svg


def generate_divider_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="20"
     viewBox="0 0 600 20" role="presentation" aria-hidden="true">
  <defs>
    <linearGradient id="fade-l" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#58a6ff" stop-opacity="0"/>
      <stop offset="1" stop-color="#58a6ff" stop-opacity="0.85"/>
    </linearGradient>
    <linearGradient id="fade-r" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#58a6ff" stop-opacity="0.85"/>
      <stop offset="1" stop-color="#58a6ff" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <rect x="0" y="9.2" width="278" height="1.6" rx="0.8" fill="url(#fade-l)"/>
  <rect x="322" y="9.2" width="278" height="1.6" rx="0.8" fill="url(#fade-r)"/>

  <g transform="translate(300 10)" fill="none" stroke="#58a6ff">
    <rect x="-4.9" y="-4.9" width="9.8" height="9.8" rx="1.8"
          transform="rotate(45)" stroke-width="1.4" stroke-opacity="0.9"/>
    <circle r="1.9" fill="#58a6ff" stroke="none"/>
  </g>
  <circle cx="266" cy="10" r="1.5" fill="#58a6ff" fill-opacity="0.55"/>
  <circle cx="334" cy="10" r="1.5" fill="#58a6ff" fill-opacity="0.55"/>
</svg>'''


def generate_footer_svg(cfg):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="140"
     viewBox="0 0 900 140" role="img" aria-label="Profile Footer">
  <title>Profile Footer</title>

  <defs>
    <linearGradient id="glow" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#1e60c8" stop-opacity="0.08"/>
      <stop offset="1" stop-color="#1e60c8" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="clip"><rect width="900" height="140" rx="12"/></clipPath>
  </defs>

  <style>
    text {{ font-family: ui-monospace,'SF Mono','JetBrains Mono','Fira Code','DejaVu Sans Mono',Menlo,Consolas,monospace; white-space: pre; }}
    .prompt {{ font-size: 13px; fill: #5b6b80; }}
    .cmd    {{ font-size: 13px; fill: #58a6ff; }}
    .arg    {{ font-size: 13px; fill: #c5d2e0; }}
    .ok     {{ font-size: 13px; fill: #3fb950; }}
    .dim    {{ font-size: 10.5px; fill: #31435a; letter-spacing: 2.0px; }}
    .dot    {{ stroke: #2b3a4d; stroke-width: 1; stroke-dasharray: 1.5 3.5;
               stroke-linecap: round; }}

    .blink  {{ animation: blink 1.15s steps(1) infinite; }}
    @keyframes blink {{ 0%,49% {{ opacity: 1 }} 50%,100% {{ opacity: 0 }} }}
    @media (prefers-reduced-motion: reduce) {{ .blink {{ animation: none; }} }}
  </style>

  <rect width="900" height="140" rx="12" fill="#070b10"/>
  <g clip-path="url(#clip)">
    <rect width="900" height="140" fill="#0b1017"/>
    <rect width="900" height="140" fill="url(#glow)"/>
  </g>
  <rect x="0.5" y="0.5" width="899" height="139" rx="12" fill="none" stroke="#182231"/>

  <text class="prompt" x="30" y="40">{html.escape(cfg["prompt_user"])}  ~  %  </text>
  <text class="cmd" x="225" y="40">echo</text>
  <text class="arg" x="264" y="40">&#34;Thanks for visiting! Stay secure.&#34;</text>
  <text class="ok" x="30" y="66">Thanks for visiting! Stay secure.</text>

  <text class="prompt" x="30" y="94">{html.escape(cfg["prompt_user"])}  ~  %  </text>
  <text class="cmd" x="225" y="94">exit</text>
  <text class="arg" x="264" y="94">0</text>
  <text class="blink cmd" x="279.6" y="94">&#9608;</text>

  <line class="dot" x1="30" y1="112" x2="870" y2="112"/>
  <text class="dim" x="450" y="126" text-anchor="middle">BUILT FOR BLUE TEAMS  &#183;  POWERED BY THREAT INTEL  &#183;  SECURED BY DESIGN</text>
</svg>'''


def generate_footer_mobile_svg(cfg):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="440" height="172"
     viewBox="0 0 440 172" role="img" aria-label="Profile Footer">
  <title>Profile Footer</title>

  <defs>
    <linearGradient id="glow" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#1e60c8" stop-opacity="0.08"/>
      <stop offset="1" stop-color="#1e60c8" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="clip"><rect width="440" height="172" rx="12"/></clipPath>
  </defs>

  <style>
    text {{ font-family: ui-monospace,'SF Mono','JetBrains Mono','Fira Code','DejaVu Sans Mono',Menlo,Consolas,monospace; white-space: pre; }}
    .prompt {{ font-size: 12px; fill: #5b6b80; }}
    .cmd    {{ font-size: 12px; fill: #58a6ff; }}
    .arg    {{ font-size: 12px; fill: #c5d2e0; }}
    .ok     {{ font-size: 12px; fill: #3fb950; }}
    .dim    {{ font-size: 9.5px; fill: #31435a; letter-spacing: 1.4px; }}
    .dot    {{ stroke: #2b3a4d; stroke-width: 1; stroke-dasharray: 1.5 3.5;
               stroke-linecap: round; }}

    .blink  {{ animation: blink 1.15s steps(1) infinite; }}
    @keyframes blink {{ 0%,49% {{ opacity: 1 }} 50%,100% {{ opacity: 0 }} }}
    @media (prefers-reduced-motion: reduce) {{ .blink {{ animation: none; }} }}
  </style>

  <rect width="440" height="172" rx="12" fill="#070b10"/>
  <g clip-path="url(#clip)">
    <rect width="440" height="172" fill="#0b1017"/>
    <rect width="440" height="172" fill="url(#glow)"/>
  </g>
  <rect x="0.5" y="0.5" width="439" height="171" rx="12" fill="none" stroke="#182231"/>

  <text class="prompt" x="20" y="38">{html.escape(cfg["prompt_user"])}  ~  %  </text>
  <text class="cmd" x="190" y="38">echo</text>
  <text class="arg" x="226" y="38">&#34;Thanks for visiting! Stay secure.&#34;</text>
  <text class="ok" x="20" y="64">Thanks for visiting! Stay secure.</text>

  <text class="prompt" x="20" y="92">{html.escape(cfg["prompt_user"])}  ~  %  </text>
  <text class="cmd" x="190" y="92">exit</text>
  <text class="arg" x="226" y="92">0</text>
  <text class="blink cmd" x="240.4" y="92">&#9608;</text>

  <line class="dot" x1="20" y1="112" x2="420" y2="112"/>
  <text class="dim" x="220" y="134" text-anchor="middle">BUILT FOR BLUE TEAMS  &#183;  POWERED BY THREAT INTEL</text>
  <text class="dim" x="220" y="154" text-anchor="middle">SECURED BY DESIGN</text>
</svg>'''


def generate_profile_readme_md(cfg):
    return f'''<p align="center">
  <picture>
    <source media="(max-width: 760px)" srcset="assets/banner-mobile.svg">
    <img src="assets/banner.svg" width="900" alt="{cfg["name"]} — {cfg["role"]}" />
  </picture>
</p>

<p align="center">
  <a href="{cfg["linkedin_url"]}"><img src="https://img.shields.io/badge/-LinkedIn-161b22?style=flat&logo=linkedin&logoColor=0A66C2" alt="LinkedIn"/></a>
  <a href="{cfg["github_url"]}"><img src="https://img.shields.io/badge/-GitHub-161b22?style=flat&logo=github&logoColor=white" alt="GitHub"/></a>
  <a href="{cfg["portfolio_url"]}"><img src="https://img.shields.io/badge/-SOC_Portfolio-161b22?style=flat&logo=target&logoColor=58a6ff" alt="SOC Portfolio"/></a>
  <a href="{cfg["academy_url"]}"><img src="https://img.shields.io/badge/-Zero2Aura_Instructor-161b22?style=flat&logo=shield&logoColor=3fb950" alt="Zero2Aura"/></a>
  <a href="mailto:{cfg["email"]}"><img src="https://img.shields.io/badge/-Email-161b22?style=flat&logo=gmail&logoColor=EA4335" alt="Email"/></a>
  <img src="https://komarev.com/ghpvc/?username={cfg["handle"]}&label=Profile%20views&color=58a6ff&style=flat" alt="Profile views"/>
</p>

<p align="center">
  <img src="assets/divider.svg" width="900" alt="" />
</p>

## <img src="assets/icons/user.svg" width="23" alt="" /> Hey, I'm Mohamed

**SOC Analyst & DFIR Specialist** specializing in security monitoring, proactive threat detection, digital forensics, and security tool engineering. Currently completing intensive SOC & cybersecurity tracks at **NTI** (Fortinet SecOps) and **ITI** (Enterprise Network Hardening), working in DFIR at the **Digital Egypt Pioneers Initiative (DEPI)**, and serving as a **Cybersecurity Instructor at Zero2Aura**.

<p align="center">
  <img src="assets/divider.svg" width="900" alt="" />
</p>

## <img src="assets/icons/shield.svg" width="23" alt="" /> Core Expertise & Skills

#### <img src="assets/icons/node.svg" width="11" alt="" /> &nbsp;Security Operations & SIEM / EDR

<p>
  <img src="https://img.shields.io/badge/-Wazuh%20SIEM-161b22?style=flat&logo=wazuh&logoColor=007ec6" alt="Wazuh"/>
  <img src="https://img.shields.io/badge/-FortiSIEM-161b22?style=flat&logo=fortinet&logoColor=EE3124" alt="FortiSIEM"/>
  <img src="https://img.shields.io/badge/-FortiAnalyzer-161b22?style=flat&logo=fortinet&logoColor=EE3124" alt="FortiAnalyzer"/>
  <img src="https://img.shields.io/badge/-Splunk-161b22?style=flat&logo=splunk&logoColor=F47E20" alt="Splunk"/>
  <img src="https://img.shields.io/badge/-Elastic%20Security-161b22?style=flat&logo=elastic&logoColor=005571" alt="Elastic"/>
  <img src="https://img.shields.io/badge/-Microsoft%20Sentinel-161b22?style=flat&logo=microsoftazure&logoColor=0078D4" alt="Sentinel"/>
  <img src="https://img.shields.io/badge/-Microsoft%20Defender-161b22?style=flat&logo=windows&logoColor=0078D6" alt="Defender"/>
  <img src="https://img.shields.io/badge/-Velociraptor-161b22?style=flat&logo=linux" alt="Velociraptor"/>
</p>

#### <img src="assets/icons/node.svg" width="11" alt="" /> &nbsp;Threat Intelligence & Detection Engineering

<p>
  <img src="https://img.shields.io/badge/-MITRE%20ATT%26CK-161b22?style=flat&logo=target" alt="MITRE ATT&CK"/>
  <img src="https://img.shields.io/badge/-Sigma%20Rules-161b22?style=flat" alt="Sigma Rules"/>
  <img src="https://img.shields.io/badge/-STIX%202.1%20%2F%20TAXII-161b22?style=flat" alt="STIX 2.1"/>
  <img src="https://img.shields.io/badge/-FortiGuard%20Threat%20Intel-161b22?style=flat&logo=fortinet&logoColor=EE3124" alt="FortiGuard"/>
  <img src="https://img.shields.io/badge/-YARA-161b22?style=flat" alt="YARA"/>
  <img src="https://img.shields.io/badge/-MISP-161b22?style=flat" alt="MISP"/>
  <img src="https://img.shields.io/badge/-ThreatScopeX%20Engine-161b22?style=flat&logoColor=58a6ff" alt="ThreatScopeX"/>
</p>

#### <img src="assets/icons/node.svg" width="11" alt="" /> &nbsp;Digital Forensics & Incident Response (DFIR)

<p>
  <img src="https://img.shields.io/badge/-Volatility%203-161b22?style=flat" alt="Volatility"/>
  <img src="https://img.shields.io/badge/-Autopsy%20Forensics-161b22?style=flat" alt="Autopsy"/>
  <img src="https://img.shields.io/badge/-FTK%20Imager-161b22?style=flat" alt="FTK Imager"/>
  <img src="https://img.shields.io/badge/-KAPE-161b22?style=flat" alt="KAPE"/>
  <img src="https://img.shields.io/badge/-Eric%20Zimmerman%20Tools-161b22?style=flat" alt="EZ Tools"/>
  <img src="https://img.shields.io/badge/-Memory%20Forensics-161b22?style=flat" alt="Memory Forensics"/>
</p>

#### <img src="assets/icons/node.svg" width="11" alt="" /> &nbsp;Enterprise Network Architecture & Hardening

<p>
  <img src="https://img.shields.io/badge/-Cisco%20Packet%20Tracer-161b22?style=flat&logo=cisco&logoColor=1BA0D7" alt="Cisco"/>
  <img src="https://img.shields.io/badge/-OSPF%20%2F%20VLANs%20%2F%20ACLs-161b22?style=flat" alt="Routing & Switching"/>
  <img src="https://img.shields.io/badge/-Wireshark-161b22?style=flat&logo=wireshark&logoColor=1679A7" alt="Wireshark"/>
  <img src="https://img.shields.io/badge/-Suricata%20NIDS-161b22?style=flat" alt="Suricata"/>
  <img src="https://img.shields.io/badge/-Zeek%20(Bro)-161b22?style=flat" alt="Zeek"/>
  <img src="https://img.shields.io/badge/-pfSense-161b22?style=flat&logo=pfsense&logoColor=212121" alt="pfSense"/>
  <img src="https://img.shields.io/badge/-SSH%20Cryptographic%20Hardening-161b22?style=flat" alt="SSH Hardening"/>
</p>

#### <img src="assets/icons/node.svg" width="11" alt="" /> &nbsp;Languages, Automation & SecOps

<p>
  <img src="https://img.shields.io/badge/-Python-161b22?style=flat&logo=python&logoColor=3776AB" alt="Python"/>
  <img src="https://img.shields.io/badge/-Bash%20Scripting-161b22?style=flat&logo=gnubash&logoColor=4EAA25" alt="Bash"/>
  <img src="https://img.shields.io/badge/-PowerShell-161b22?style=flat&logo=powershell&logoColor=5391FE" alt="PowerShell"/>
  <img src="https://img.shields.io/badge/-C%20%2F%20C%2B%2B-161b22?style=flat&logo=c%2B%2B&logoColor=00599C" alt="C/C++"/>
  <img src="https://img.shields.io/badge/-SQL-161b22?style=flat&logo=mysql" alt="SQL"/>
  <img src="https://img.shields.io/badge/-Linux%20Administration-161b22?style=flat&logo=linux&logoColor=FCC624" alt="Linux"/>
  <img src="https://img.shields.io/badge/-Docker-161b22?style=flat&logo=docker&logoColor=2496ED" alt="Docker"/>
  <img src="https://img.shields.io/badge/-Git%20%2F%20GitHub-161b22?style=flat&logo=git" alt="Git"/>
</p>

<p align="center">
  <img src="assets/divider.svg" width="900" alt="" />
</p>

## <img src="assets/icons/terminal.svg" width="23" alt="" /> Featured Open-Source Projects

| Project | Description | Stack / Focus |
| :--- | :--- | :--- |
| 🔍 **[ThreatScopeX](https://github.com/0xsabry/ThreatScopeX)** | Advanced log intelligence and threat detection engine with 115+ built-in detection rules | Python, MITRE ATT&CK, Sigma, STIX 2.1 |
| 📑 **[IR-Report-Generator](https://github.com/0xsabry/IR-Report-Generator)** | Browser-based incident response reporting tool supporting 40+ security tool artifacts | HTML5, CSS3, JS, MITRE Navigator |
| 🛡️ **[SOC Lab Project](https://0xsabry.github.io/soc-lab-project/)** | End-to-end enterprise attack simulation, Wazuh detection, and automated IR simulation | Wazuh, Sysmon, EventLogs, Ubuntu, PowerShell |
| 🎣 **[Phishing IR Framework](https://github.com/0xsabry)** | Complete 6-phase email forensic investigation framework aligned with NIST 800-61 | Email Header Forensics, IOC Extraction |

<p align="center">
  <img src="assets/divider.svg" width="900" alt="" />
</p>

## <img src="assets/icons/briefcase.svg" width="23" alt="" /> Experience & Internships

<p>
<img src="assets/icons/target.svg" width="17" alt="" /> &nbsp; <strong>National Telecommunication Institute (NTI)</strong> | <em>SOC Analyst Intern (FortiAnalyzer + FortiSIEM)</em> | <strong>August 2026 – Present</strong><br/>
• Completing intensive SOC Analyst track focused on Fortinet Security Operations workflows: event examination, event handlers, automated playbooks, forensic analysis, and threat intelligence reporting.<br/>
• Using <strong>FortiAnalyzer</strong> for log collection and analysis, FortiView searches, incident management, threat hunting, custom reports, and Incident Response playbook creation and monitoring.<br/>
• Operating <strong>FortiSIEM</strong> for real-time and historic searches, event correlation, custom incident rules, dashboard configuration, and UEBA-based threat hunting with FortiGuard Threat Intelligence.<br/>
• Practicing detection, analysis, and remediation of security incidents using traditional and AI/ML-assisted methods; preparing for <strong>FCP – Security Operations</strong> and <strong>NSE 6 FortiSIEM Analyst</strong> certifications.
</p>

<p>
<img src="assets/icons/shield.svg" width="17" alt="" /> &nbsp; <strong>Information Technology Institute (ITI)</strong> | <em>Cybersecurity Intern</em> | <strong>April 2026 – Present</strong><br/>
• Engineered and hardened multi-zone enterprise network architecture in Cisco Packet Tracer with multi-VLAN Layer 2/3 segmentation, dynamic DHCP, and multi-area OSPF routing for secure high-availability communication.<br/>
• Designed and enforced Extended ACLs to control traffic flow, isolate wireless zones, and restrict management-plane and server access to authorized hosts.<br/>
• Hardened network appliances by enforcing cryptographic SSH on VTY lines and restricting management access; successfully defended architecture before ITI evaluation panel.<br/>
• Completed modules in Cyber Security Essentials, Ethical Hacking & Vulnerability Assessment, and Huawei HCCDA Tech Essentials (cloud computing and ICT infrastructure).
</p>

<p>
<img src="assets/icons/briefcase.svg" width="17" alt="" /> &nbsp; <strong>Digital Egypt Pioneers Initiative (DEPI)</strong> | <em>Digital Forensics Investigator</em> | <strong>Jan 2025 – Present</strong><br/>
• Conducting digital forensics examinations, artifact analysis, and memory/disk investigation.
</p>

<p>
<img src="assets/icons/award.svg" width="17" alt="" /> &nbsp; <strong><a href="{cfg["academy_url"]}">Zero2Aura Tech Academy</a></strong> | <em>Cybersecurity Instructor</em> | <strong>Oct 2025 – Present</strong><br/>
• Training students and aspiring security analysts in Cybersecurity, DFIR, Penetration Testing, and Networking.
</p>

<p>
<img src="assets/icons/shield.svg" width="17" alt="" /> &nbsp; <strong>Digital Egypt Pioneers Initiative (DEPI)</strong> | <em>Cyber Security Incident Response Analyst</em> | <strong>Oct 2024 – May 2025</strong><br/>
• Analyzed security alerts, mapped incidents to MITRE ATT&CK, and executed IR playbooks.
</p>

<p>
<img src="assets/icons/globe.svg" width="17" alt="" /> &nbsp; <strong>The British University in Egypt (BUE)</strong> | <em>Cyber Security Intern</em> | <strong>Jul 2024</strong>
</p>

<p align="center">
  <img src="assets/divider.svg" width="900" alt="" />
</p>

## <img src="assets/icons/chart.svg" width="23" alt="" /> GitHub Analytics & Streak

<p align="center">
  <img height="165" src="https://github-readme-stats-fjlm.vercel.app/api?username={cfg["handle"]}&show_icons=true&bg_color=0b1017&title_color=58a6ff&text_color=c5d2e0&icon_color=3fb950&border_color=182231" alt="GitHub Stats"/>
  <img height="165" src="https://github-readme-streak-stats-three-sand.vercel.app?user={cfg["handle"]}&background=0b1017&ring=58a6ff&fire=3fb950&currStreakLabel=58a6ff&sideLabels=c5d2e0&currStreakNum=e6edf6&sideNums=e6edf6&dates=5b6b80&border=182231" alt="GitHub Streak"/>
</p>

<p align="center">
  <img src="assets/divider.svg" width="900" alt="" />
</p>

<p align="center">
  <picture>
    <source media="(max-width: 760px)" srcset="assets/footer-mobile.svg">
    <img src="assets/footer.svg" width="900" alt="Thanks for visiting!" />
  </picture>
</p>
'''


def main():
    print("==================================================")
    print(" Cyberpunk Terminal Profile Banner Generator")
    print(f" Target: {CONFIG['name']} ({CONFIG['handle']})")
    print("==================================================")

    os.makedirs("assets", exist_ok=True)
    os.makedirs("assets/icons", exist_ok=True)

    # 1. Process Avatar
    avatar_path = CONFIG["avatar_path"]
    if not os.path.exists(avatar_path):
        scratch_avatar = r"C:\Users\ENG MOHAMED SABRY\.gemini\antigravity-ide\brain\40c9f3f5-0f86-444e-9a53-98646b279c76\scratch\0xsabry_avatar.png"
        if os.path.exists(scratch_avatar):
            import shutil
            shutil.copyfile(scratch_avatar, avatar_path)
            print(f"Copied avatar from scratch to {avatar_path}")
        else:
            raise FileNotFoundError(f"Please place your photo at {avatar_path}")

    print("[1/6] Processing avatar into ASCII character matrix...")
    ascii_grid = process_image_to_ascii(avatar_path, COLS, ROWS)
    print(f"      Generated {len(ascii_grid)} rows x {len(ascii_grid[0])} cols character grid.")

    # 2. Desktop Banner
    print("[2/6] Generating assets/banner.svg (Desktop 900x556)...")
    banner_desktop = generate_desktop_banner_svg(ascii_grid, CONFIG)
    with open("assets/banner.svg", "w", encoding="utf-8") as f:
        f.write(banner_desktop)

    # 3. Mobile Banner
    print("[3/6] Generating assets/banner-mobile.svg (Mobile 440x940)...")
    banner_mobile = generate_mobile_banner_svg(ascii_grid, CONFIG)
    with open("assets/banner-mobile.svg", "w", encoding="utf-8") as f:
        f.write(banner_mobile)

    # 4. Divider & Footers
    print("[4/6] Generating divider and footer vector assets...")
    with open("assets/divider.svg", "w", encoding="utf-8") as f:
        f.write(generate_divider_svg())
    with open("assets/footer.svg", "w", encoding="utf-8") as f:
        f.write(generate_footer_svg(CONFIG))
    with open("assets/footer-mobile.svg", "w", encoding="utf-8") as f:
        f.write(generate_footer_mobile_svg(CONFIG))

    # 5. README
    print("[5/6] Generating PROFILE_README.md...")
    profile_readme = generate_profile_readme_md(CONFIG)
    with open("PROFILE_README.md", "w", encoding="utf-8") as f:
        f.write(profile_readme)

    print("[6/6] All assets generated successfully!")
    print("Files created:")
    print(" - assets/banner.svg")
    print(" - assets/banner-mobile.svg")
    print(" - assets/divider.svg")
    print(" - assets/footer.svg")
    print(" - assets/footer-mobile.svg")
    print(" - assets/icons/ (11 icons)")
    print(" - PROFILE_README.md")


if __name__ == "__main__":
    main()
