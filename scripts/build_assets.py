#!/usr/bin/env python3
"""Builds the animated SVG artwork used by the profile README.

Everything is self-contained SVG (no external fonts, scripts or services), so
GitHub renders it reliably. Edit the text in the DATA section, then run:

    python3 scripts/build_assets.py

and commit the regenerated files in assets/.
"""

from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"

# ---------------------------------------------------------------------------
# DATA: edit me
# ---------------------------------------------------------------------------

NAME = "Prithvi Halagere Lokesha"
TAGLINE = "AI/ML Engineer  ·  LLM Systems  ·  Medical AI"
SUBLINE = "M.S. Artificial Intelligence Systems  ·  University of Florida"
STATUS = "OPEN TO FULL-TIME ROLES"

TYPING_LINES = [
    "Building LLM observability & evaluation tools",
    "Shipping ECG deep learning to cloud and edge",
    "Retrieval-augmented search over codebases",
    "Turning ML research into production systems",
]

CARDS = [
    {
        "file": "card-spanscope.svg",
        "title": "Spanscope",
        "lines": ["Live LLM observability: latency,", "errors and cost per model from", "OpenTelemetry traces."],
        "chips": ["TypeScript", "Hono", "ClickHouse", "OpenTelemetry"],
        "pill": "LIVE DEMO",
        "accent": "#4c8dff",
        "accent2": "#9085e9",
        "art": "bars",
    },
    {
        "file": "card-codeatlas.svg",
        "title": "CodeAtlas",
        "lines": ["Ask questions about any public", "GitHub repo; answers cite", "commit-pinned source code."],
        "chips": ["TypeScript", "RAG", "LangGraph", "Qdrant"],
        "pill": "LIVE DEMO",
        "accent": "#19c48a",
        "accent2": "#4c8dff",
        "art": "graph",
    },
    {
        "file": "card-leavenow.svg",
        "title": "LeaveNow",
        "lines": ["Bus trip planner for Rochester", "RTS: live and scheduled times,", "journeys with one transfer."],
        "chips": ["Python", "Streamlit", "GTFS", "Docker"],
        "pill": "LIVE DEMO",
        "accent": "#ff9f43",
        "accent2": "#ff6b6b",
        "art": "route",
    },
    {
        "file": "card-tinyml.svg",
        "title": "TinyML Voice on ESP32",
        "lines": ["On-device voice command", "recognition on a microcontroller,", "with a live OLED readout."],
        "chips": ["C++", "TinyML", "Edge Impulse", "ESP32"],
        "pill": "EDGE AI",
        "accent": "#ff5c8a",
        "accent2": "#9085e9",
        "art": "wave",
    },
]

JOURNEY = [
    ("2019 – 2023", "B.E. Information", "Science · VTU"),
    ("2022 – 2023", "ML Engineer", "YBI Foundation"),
    ("2023 – 2024", "Engineer in Test", "Huron Consulting"),
    ("2024 – 2026", "M.S. AI Systems", "Univ. of Florida"),
    ("2025 – 2026", "AI/ML Engineer Intern", "Aventusoft"),
    ("2026 →", "Open to full-time", "ML / AI / SWE roles"),
]

# ---------------------------------------------------------------------------
# shared style
# ---------------------------------------------------------------------------

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
BG_A, BG_B = "#0b1020", "#111a33"
INK, INK_2, INK_3 = "#f2f4fa", "#c4c9d8", "#8a92a8"
ECG = "#2fe0a0"


def svg(w: int, h: int, body: str, title: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'role="img" aria-label="{escape(title)}">\n<title>{escape(title)}</title>\n{body}\n</svg>\n'
    )


def ecg_path(x0: float, x1: float, base: float, period: float, amp: float = 1.0) -> str:
    """A repeating PQRST heartbeat trace from x0 to x1."""
    d = [f"M{x0:.1f},{base:.1f}"]
    x = x0
    while x < x1:
        seg = [
            (0.18, 0), (0.06, -6), (0.06, 0),      # P wave
            (0.06, 0), (0.02, 6), (0.035, -62),    # Q, R
            (0.035, 26), (0.03, 0),                # S
            (0.12, 0), (0.08, -12), (0.08, 0),     # T wave
            (0.205, 0),
        ]
        for frac, dy in seg:
            x += frac * period
            if x > x1:
                x = x1
            d.append(f"L{x:.1f},{base + dy * amp:.1f}")
            if x >= x1:
                break
    return " ".join(d)


def glow_filter(fid: str, std: float = 4) -> str:
    return (
        f'<filter id="{fid}" x="-20%" y="-50%" width="140%" height="200%">'
        f'<feGaussianBlur stdDeviation="{std}" result="b"/>'
        f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
    )


# ---------------------------------------------------------------------------
# header
# ---------------------------------------------------------------------------


def header() -> str:
    w, h = 1200, 360
    grid = "".join(
        f'<line x1="{x}" y1="0" x2="{x}" y2="{h}"/>' for x in range(0, w + 1, 40)
    ) + "".join(f'<line x1="0" y1="{y}" x2="{w}" y2="{y}"/>' for y in range(0, h + 1, 40))
    trace = ecg_path(0, w, 300, 300, 0.75)
    body = f"""
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{BG_A}"/><stop offset="1" stop-color="{BG_B}"/>
  </linearGradient>
  <radialGradient id="glowA" cx="0.15" cy="0.2" r="0.6">
    <stop offset="0" stop-color="#4c8dff" stop-opacity="0.35"/><stop offset="1" stop-color="#4c8dff" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="glowB" cx="0.85" cy="0.1" r="0.55">
    <stop offset="0" stop-color="#9085e9" stop-opacity="0.32"/><stop offset="1" stop-color="#9085e9" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="name" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#7fb2ff"/><stop offset="0.5" stop-color="#b9a8ff"/><stop offset="1" stop-color="#7fe8c4"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="-0.3 0;0.3 0;-0.3 0" dur="10s" repeatCount="indefinite"/>
  </linearGradient>
  {glow_filter("ecgGlow", 3)}
  <clipPath id="frame"><rect width="{w}" height="{h}" rx="22"/></clipPath>
</defs>
<g clip-path="url(#frame)">
  <rect width="{w}" height="{h}" fill="url(#bg)"/>
  <rect width="{w}" height="{h}" fill="url(#glowA)"/>
  <rect width="{w}" height="{h}" fill="url(#glowB)"/>
  <g stroke="#ffffff" stroke-opacity="0.035" stroke-width="1">{grid}</g>

  <g font-family="{SANS}">
    <rect x="60" y="48" width="{len(STATUS) * 8.6 + 48:.0f}" height="30" rx="15" fill="#2fe0a0" fill-opacity="0.12" stroke="#2fe0a0" stroke-opacity="0.35"/>
    <circle cx="80" cy="63" r="5" fill="#2fe0a0">
      <animate attributeName="opacity" values="1;0.25;1" dur="1.6s" repeatCount="indefinite"/>
    </circle>
    <text x="94" y="68" font-size="13" font-weight="700" letter-spacing="1.4" fill="#7ff0c4">{escape(STATUS)}</text>

    <text x="60" y="128" font-size="22" fill="{INK_2}">Hi, I'm</text>
    <text x="58" y="186" font-size="54" font-weight="800" letter-spacing="-1.2" fill="url(#name)">{escape(NAME)}</text>
    <text x="60" y="226" font-size="22" font-weight="600" fill="{INK}">{escape(TAGLINE)}</text>
    <text x="60" y="256" font-size="16" fill="{INK_3}">{escape(SUBLINE)}</text>

    <g transform="translate(800 44)">
      <rect width="340" height="206" rx="14" fill="#05080f" fill-opacity="0.72" stroke="#ffffff" stroke-opacity="0.1"/>
      <rect width="340" height="34" rx="14" fill="#ffffff" fill-opacity="0.04"/>
      <circle cx="20" cy="17" r="5" fill="#ff5f57"/><circle cx="38" cy="17" r="5" fill="#febc2e"/><circle cx="56" cy="17" r="5" fill="#28c840"/>
      <text x="170" y="22" text-anchor="middle" font-family="{MONO}" font-size="12.5" fill="{INK_3}">now.json</text>
      <g transform="translate(276 9)">
        <path d="M9 4c-2.4-3.2-7.2-2.4-7.2 1.6 0 3.2 7.2 8 7.2 8s7.2-4.8 7.2-8c0-4-4.8-4.8-7.2-1.6z" fill="#ff5c8a">
          <animate attributeName="opacity" values="1;0.35;1;1" dur="0.83s" repeatCount="indefinite"/>
        </path>
        <text x="20" y="13" font-family="{MONO}" font-size="12" font-weight="700" fill="#7ff0c4">72</text>
      </g>
      <g font-family="{MONO}" font-size="14.5">
        <text x="22" y="62" fill="{INK_3}">{{</text>
        <text x="40" y="88"><tspan fill="#7fb2ff">"role"</tspan><tspan fill="{INK_3}">: </tspan><tspan fill="#7ff0c4">"AI/ML Engineer"</tspan><tspan fill="{INK_3}">,</tspan></text>
        <text x="40" y="112"><tspan fill="#7fb2ff">"focus"</tspan><tspan fill="{INK_3}">: [</tspan><tspan fill="#7ff0c4">"LLMs"</tspan><tspan fill="{INK_3}">, </tspan><tspan fill="#7ff0c4">"Med AI"</tspan><tspan fill="{INK_3}">],</tspan></text>
        <text x="40" y="136"><tspan fill="#7fb2ff">"live_apps"</tspan><tspan fill="{INK_3}">: </tspan><tspan fill="#ffb86b">3</tspan><tspan fill="{INK_3}">,</tspan></text>
        <text x="40" y="160"><tspan fill="#7fb2ff">"open_to_work"</tspan><tspan fill="{INK_3}">: </tspan><tspan fill="#b9a8ff">true</tspan></text>
        <text x="22" y="184" fill="{INK_3}">}}</text>
        <rect x="36" y="171" width="9" height="17" fill="#7ff0c4"><animate attributeName="opacity" values="1;0;1" dur="1.1s" calcMode="discrete" repeatCount="indefinite"/></rect>
      </g>
    </g>
  </g>

  <path d="{trace}" fill="none" stroke="{ECG}" stroke-opacity="0.18" stroke-width="2"/>
  <path d="{trace}" fill="none" stroke="{ECG}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"
        pathLength="1" stroke-dasharray="0.16 0.84" filter="url(#ecgGlow)">
    <animate attributeName="stroke-dashoffset" from="0.16" to="-0.84" dur="5s" repeatCount="indefinite"/>
  </path>
</g>
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="22" fill="none" stroke="#ffffff" stroke-opacity="0.08"/>"""
    return svg(w, h, body, f"{NAME}: {TAGLINE}")


# ---------------------------------------------------------------------------
# typing line
# ---------------------------------------------------------------------------


def typing() -> str:
    w, h, fs = 900, 44, 22
    cw = fs * 0.6
    slot, total = 5.0, 5.0 * len(TYPING_LINES)
    parts = []
    for i, line in enumerate(TYPING_LINES):
        tw = len(line) * cw
        x0 = (w - tw) / 2
        s = i * slot / total
        t1 = s + 1.6 / total
        t2 = s + 4.0 / total
        t3 = s + 4.6 / total
        if i == 0:
            kt, wv, xv = f"0;{t1:.4f};{t2:.4f};{t3:.4f};1", f"0;{tw:.1f};{tw:.1f};0;0", None
        else:
            kt, wv = f"0;{s:.4f};{t1:.4f};{t2:.4f};{t3:.4f};1", f"0;0;{tw:.1f};{tw:.1f};0;0"
        xv = ";".join(f"{x0 + float(v):.1f}" for v in wv.split(";"))
        vis_kt = f"0;{s:.4f};{t3:.4f}" if i else f"0;{t3:.4f}"
        vis_v = "0;1;0" if i else "1;0"
        parts.append(
            f"""<clipPath id="c{i}"><rect x="{x0:.1f}" y="0" width="0" height="{h}">
  <animate attributeName="width" values="{wv}" keyTimes="{kt}" dur="{total}s" repeatCount="indefinite"/></rect></clipPath>
<text x="{x0:.1f}" y="29" clip-path="url(#c{i})" font-family="{MONO}" font-size="{fs}" fill="url(#tg)">{escape(line)}</text>
<rect y="9" width="3" height="26" rx="1.5" fill="#7ff0c4" opacity="0">
  <animate attributeName="x" values="{xv}" keyTimes="{kt}" dur="{total}s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values="{vis_v}" keyTimes="{vis_kt}" calcMode="discrete" dur="{total}s" repeatCount="indefinite"/>
</rect>"""
        )
    body = f"""<defs><linearGradient id="tg" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="#7fb2ff"/><stop offset="1" stop-color="#b9a8ff"/></linearGradient></defs>
{chr(10).join(parts)}"""
    return svg(w, h, body, " / ".join(TYPING_LINES))


# ---------------------------------------------------------------------------
# project cards
# ---------------------------------------------------------------------------


def card_art(kind: str, a: str, b: str) -> str:
    ox, oy = 330, 70  # art area origin (130 x 90)
    if kind == "bars":
        heights = [22, 26, 20, 28, 24, 30, 26, 70, 56, 30]
        out = []
        for i, hgt in enumerate(heights):
            x = ox + i * 13
            color = "#ff6b6b" if i in (7, 8) else a
            out.append(
                f'<rect x="{x}" y="{oy + 90 - hgt}" width="9" height="{hgt}" rx="2" fill="{color}" fill-opacity="0.9">'
                f'<animate attributeName="height" values="{hgt * 0.6:.0f};{hgt};{hgt * 0.75:.0f};{hgt * 0.6:.0f}" dur="{2.4 + i * 0.13:.2f}s" repeatCount="indefinite"/>'
                f'<animate attributeName="y" values="{oy + 90 - hgt * 0.6:.0f};{oy + 90 - hgt};{oy + 90 - hgt * 0.75:.0f};{oy + 90 - hgt * 0.6:.0f}" dur="{2.4 + i * 0.13:.2f}s" repeatCount="indefinite"/></rect>'
            )
        out.append(
            f'<path d="M{ox} {oy + 50} L{ox + 30} {oy + 46} L{ox + 60} {oy + 48} L{ox + 90} {oy + 14} L{ox + 128} {oy + 22}" '
            f'fill="none" stroke="{b}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>'
        )
        return "".join(out)
    if kind == "graph":
        nodes = [(0, 45), (40, 15), (45, 70), (85, 40), (125, 12), (120, 75)]
        edges = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4), (3, 5), (1, 4)]
        out = [
            f'<line x1="{ox + nodes[i][0]}" y1="{oy + nodes[i][1]}" x2="{ox + nodes[j][0]}" y2="{oy + nodes[j][1]}" stroke="{a}" stroke-opacity="0.45" stroke-width="1.6"/>'
            for i, j in edges
        ]
        for k, (x, y) in enumerate(nodes):
            r = 9 if k == 3 else 6
            out.append(
                f'<circle cx="{ox + x}" cy="{oy + y}" r="{r}" fill="{a if k != 3 else b}">'
                f'<animate attributeName="r" values="{r};{r + 2.5};{r}" dur="{2 + k * 0.4:.1f}s" repeatCount="indefinite"/></circle>'
            )
        out.append(
            f'<circle r="3.5" fill="#ffffff"><animateMotion dur="3s" repeatCount="indefinite" '
            f'path="M{ox} {oy + 45} L{ox + 40} {oy + 15} L{ox + 85} {oy + 40} L{ox + 125} {oy + 12}"/></circle>'
        )
        return "".join(out)
    if kind == "route":
        path = f"M{ox} {oy + 75} C{ox + 30} {oy + 75} {ox + 30} {oy + 20} {ox + 65} {oy + 20} S{ox + 100} {oy + 70} {ox + 128} {oy + 50}"
        out = [
            f'<path d="{path}" fill="none" stroke="{a}" stroke-opacity="0.35" stroke-width="7" stroke-linecap="round"/>',
            f'<path d="{path}" fill="none" stroke="{a}" stroke-width="2.5" stroke-dasharray="2 7" stroke-linecap="round"/>',
        ]
        for x, y in [(0, 75), (65, 20), (128, 50)]:
            out.append(f'<circle cx="{ox + x}" cy="{oy + y}" r="6" fill="{BG_A}" stroke="{a}" stroke-width="2.5"/>')
        out.append(
            f'<g><rect x="-9" y="-6" width="18" height="12" rx="3" fill="{b}"/>'
            f'<animateMotion dur="4.5s" repeatCount="indefinite" rotate="auto" path="{path}"/></g>'
        )
        return "".join(out)
    # wave
    out = []
    for i in range(16):
        x = ox + i * 8
        base = [10, 18, 30, 44, 60, 40, 24, 50, 70, 46, 28, 38, 22, 14, 10, 8][i]
        out.append(
            f'<rect x="{x}" y="{oy + 45 - base / 2:.0f}" width="5" height="{base}" rx="2.5" fill="{a if i % 3 else b}">'
            f'<animate attributeName="height" values="{base};{base * 0.35:.0f};{base}" dur="{0.9 + (i % 5) * 0.17:.2f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="y" values="{oy + 45 - base / 2:.0f};{oy + 45 - base * 0.175:.0f};{oy + 45 - base / 2:.0f}" dur="{0.9 + (i % 5) * 0.17:.2f}s" repeatCount="indefinite"/></rect>'
        )
    return "".join(out)


def card(c: dict) -> str:
    w, h = 480, 250
    a, b = c["accent"], c["accent2"]
    chips, x = [], 28
    for chip in c["chips"]:
        cw = len(chip) * 7.4 + 22
        chips.append(
            f'<rect x="{x:.0f}" y="196" width="{cw:.0f}" height="28" rx="14" fill="#ffffff" fill-opacity="0.06" stroke="#ffffff" stroke-opacity="0.12"/>'
            f'<text x="{x + cw / 2:.0f}" y="214.5" text-anchor="middle" font-size="12.5" font-weight="600" fill="{INK_2}">{escape(chip)}</text>'
        )
        x += cw + 8
    pill_w = len(c["pill"]) * 8 + 34
    lines = "".join(
        f'<text x="28" y="{108 + i * 22}" font-size="14.5" fill="{INK_2}">{escape(t)}</text>'
        for i, t in enumerate(c["lines"])
    )
    title_size = 24 if len(c["title"]) < 16 else 21
    body = f"""
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#121a31"/><stop offset="1" stop-color="{BG_A}"/></linearGradient>
  <radialGradient id="hl" cx="0.92" cy="0.05" r="0.7"><stop offset="0" stop-color="{a}" stop-opacity="0.28"/><stop offset="1" stop-color="{a}" stop-opacity="0"/></radialGradient>
  <linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a}" stop-opacity="0.7"/><stop offset="0.5" stop-color="#ffffff" stop-opacity="0.06"/><stop offset="1" stop-color="{b}" stop-opacity="0.6"/></linearGradient>
</defs>
<rect width="{w}" height="{h}" rx="18" fill="url(#bg)"/>
<rect width="{w}" height="{h}" rx="18" fill="url(#hl)"/>
<rect x="0.75" y="0.75" width="{w - 1.5}" height="{h - 1.5}" rx="17.5" fill="none" stroke="url(#edge)" stroke-width="1.5"/>
<g font-family="{SANS}">
  <rect x="28" y="28" width="6" height="34" rx="3" fill="{a}"/>
  <text x="46" y="55" font-size="{title_size}" font-weight="800" letter-spacing="-0.4" fill="{INK}">{escape(c["title"])}</text>
  <g transform="translate({w - 28 - pill_w} 30)">
    <rect width="{pill_w}" height="26" rx="13" fill="{a}" fill-opacity="0.14" stroke="{a}" stroke-opacity="0.45"/>
    <circle cx="14" cy="13" r="4" fill="{a}"><animate attributeName="opacity" values="1;0.3;1" dur="1.6s" repeatCount="indefinite"/></circle>
    <text x="24" y="17.5" font-size="11.5" font-weight="700" letter-spacing="1" fill="{INK}">{escape(c["pill"])}</text>
  </g>
  {lines}
  {"".join(chips)}
</g>
<g opacity="0.95">{card_art(c["art"], a, b)}</g>"""
    return svg(w, h, body, f'{c["title"]}: {" ".join(c["lines"])}')


# ---------------------------------------------------------------------------
# journey timeline
# ---------------------------------------------------------------------------


def journey() -> str:
    w, h = 1200, 230
    n = len(JOURNEY)
    margin = 130
    step = (w - 2 * margin) / (n - 1)
    nodes = []
    for i, (when, l1, l2) in enumerate(JOURNEY):
        x = margin + i * step
        last = i == n - 1
        color = "#2fe0a0" if last else ("#4c8dff" if i % 2 == 0 else "#9085e9")
        pulse = (
            f'<circle cx="{x:.0f}" cy="110" r="10" fill="none" stroke="{color}" stroke-width="2">'
            f'<animate attributeName="r" values="10;24" dur="1.8s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0.9;0" dur="1.8s" repeatCount="indefinite"/></circle>'
            if last
            else ""
        )
        nodes.append(
            f"""{pulse}<circle cx="{x:.0f}" cy="110" r="10" fill="{BG_A}" stroke="{color}" stroke-width="3"/>
<circle cx="{x:.0f}" cy="110" r="4" fill="{color}"/>
<text x="{x:.0f}" y="76" text-anchor="middle" font-family="{MONO}" font-size="13" font-weight="700" fill="{color}">{escape(when)}</text>
<text x="{x:.0f}" y="152" text-anchor="middle" font-size="15" font-weight="700" fill="{INK}">{escape(l1)}</text>
<text x="{x:.0f}" y="174" text-anchor="middle" font-size="13" fill="{INK_3}">{escape(l2)}</text>"""
        )
    body = f"""
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG_A}"/><stop offset="1" stop-color="{BG_B}"/></linearGradient>
  <linearGradient id="line" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4c8dff"/><stop offset="0.6" stop-color="#9085e9"/><stop offset="1" stop-color="#2fe0a0"/></linearGradient>
</defs>
<rect width="{w}" height="{h}" rx="20" fill="url(#bg)"/>
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="20" fill="none" stroke="#ffffff" stroke-opacity="0.08"/>
<text x="60" y="38" font-family="{SANS}" font-size="13" font-weight="700" letter-spacing="2" fill="{INK_3}">JOURNEY</text>
<line x1="{margin}" y1="110" x2="{w - margin}" y2="110" stroke="#ffffff" stroke-opacity="0.08" stroke-width="4" stroke-linecap="round"/>
<line x1="{margin}" y1="110" x2="{w - margin}" y2="110" stroke="url(#line)" stroke-width="4" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1">
  <animate attributeName="stroke-dashoffset" values="1;0;0" keyTimes="0;0.35;1" dur="6s" repeatCount="indefinite"/>
</line>
<g font-family="{SANS}">{"".join(nodes)}</g>"""
    return svg(w, h, body, "Journey: " + "; ".join(f"{a} {b} {c}" for a, b, c in JOURNEY))


# ---------------------------------------------------------------------------
# ECG divider
# ---------------------------------------------------------------------------


def divider() -> str:
    w, h = 1200, 60
    trace = ecg_path(0, w, 40, 400, 0.5)
    body = f"""
<defs>
  <linearGradient id="fade" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{ECG}" stop-opacity="0"/><stop offset="0.15" stop-color="{ECG}"/>
    <stop offset="0.85" stop-color="#9085e9"/><stop offset="1" stop-color="#9085e9" stop-opacity="0"/>
  </linearGradient>
  {glow_filter("g", 2.5)}
</defs>
<path d="{trace}" fill="none" stroke="url(#fade)" stroke-opacity="0.25" stroke-width="1.6"/>
<path d="{trace}" fill="none" stroke="url(#fade)" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"
      pathLength="1" stroke-dasharray="0.12 0.88" filter="url(#g)">
  <animate attributeName="stroke-dashoffset" from="0.12" to="-0.88" dur="4s" repeatCount="indefinite"/>
</path>"""
    return svg(w, h, body, "Heartbeat divider")


def main() -> None:
    OUT.mkdir(exist_ok=True)
    files = {
        "header.svg": header(),
        "typing.svg": typing(),
        "journey.svg": journey(),
        "divider.svg": divider(),
        **{c["file"]: card(c) for c in CARDS},
    }
    for name, content in files.items():
        (OUT / name).write_text(content, encoding="utf-8")
        print(f"wrote assets/{name} ({len(content):,} bytes)")


if __name__ == "__main__":
    main()
