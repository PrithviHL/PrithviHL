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

NAME = "Prithvi"
TAGLINE = "Software Engineer  ·  AI/ML Engineer  ·  LLM Systems"
SUBLINE = "M.S. Artificial Intelligence Systems  ·  University of Florida"
STATUS = "OPEN TO FULL-TIME SWE & AI/ML ROLES"

TYPING_LINES = [
    "Building LeaveNow: real-time bus planning for Gainesville",
    "Building LLM observability & evaluation tools",
    "Shipping ECG deep learning to cloud and edge",
    "Retrieval-augmented search over codebases",
    "Turning ML research into production systems",
    "Writing tested, maintainable software end to end",
]

CARDS = [
    {
        "file": "card-spanscope.svg",
        "title": "Spanscope",
        "lines": ["Live LLM observability from", "OpenTelemetry: 52,700 spans/s", "into ClickHouse, 0 dropped."],
        "chips": ["TypeScript", "ClickHouse", "OpenTelemetry", "Python"],
        "pill": "LIVE DEMO",
        "accent": "#4c8dff",
        "accent2": "#9085e9",
        "art": "iso_bars",
    },
    {
        "file": "card-codeatlas.svg",
        "title": "CodeAtlas",
        "lines": ["AST-aware codebase Q&A.", "96.6% exact-source recovery", "291 parser-checked lookups."],
        "chips": ["TypeScript", "Tree-sitter", "Groq"],
        "pill": "LIVE DEMO",
        "accent": "#19c48a",
        "accent2": "#4c8dff",
        "art": "graph3d",
    },
    {
        "file": "card-leavenow-gainesville.svg",
        "title": "LeaveNow",
        "lines": ["Gainesville RTS: 972 stops.", "127 automated tests passed.", "OSM walks + exact-trip tracking."],
        "chips": ["Python", "Streamlit", "GTFS", "Docker"],
        "pill": "LIVE DEMO",
        "accent": "#ff9f43",
        "accent2": "#ff6b6b",
        "art": "iso_route",
    },
    {
        "file": "card-tinyml.svg",
        "title": "SayWatt",
        "lines": ["Offline voice control on a $5", "ESP32: 28 classes, 92% precise", "when it acts. No internet."],
        "chips": ["C++", "Edge Impulse", "ESP32", "WebAssembly"],
        "pill": "LIVE DEMO",
        "accent": "#ff5c8a",
        "accent2": "#9085e9",
        "art": "ring3d",
    },
]

JOURNEY = [
    ("2019 – 2023", "B.E. Information", "Science · VTU"),
    ("2022 – 2023", "ML Engineer Intern", "YBI Foundation"),
    ("2023 – 2024", "Engineer in Test", "Huron Consulting"),
    ("2024 – 2026", "M.S. AI Systems", "Univ. of Florida"),
    ("2025 – 2026", "AI/ML Engineer Intern", "Aventusoft"),
    ("2026 →", "Open to full-time", "SWE & AI/ML roles"),
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
# 3D: rotate real 3D points, project with perspective, shade by depth, and bake
# the result into SMIL keyframes (GitHub READMEs can't run JavaScript).
# ---------------------------------------------------------------------------

import math
import random as _random


def _project(x, y, z, angle, tilt):
    """Rotate around Y by angle, tilt around X, then perspective-project."""
    ca, sa = math.cos(angle), math.sin(angle)
    x1, z1 = x * ca + z * sa, -x * sa + z * ca
    ct, st = math.cos(tilt), math.sin(tilt)
    y1, z2 = y * ct - z1 * st, y * st + z1 * ct
    p = 3.2 / (3.2 + z2)  # z2 > 0 is farther away
    return x1 * p, y1 * p, z2


def _vals(xs, fmt="{:.1f}"):
    return ";".join(fmt.format(v) for v in xs)


def spin_cloud(points, cx, cy, scale, color, dur=14, frames=30, tilt=0.38,
               rmin=0.8, rmax=2.8, color2=None, phase=0.0, sway=None):
    """Animated rotating point cloud. points: list of (x, y, z) in about [-1, 1].
    sway: if set, rock back and forth by this many radians instead of a full spin."""
    out = []
    for i, (x, y, z) in enumerate(points):
        xs, ys, rs, os_ = [], [], [], []
        for f in range(frames + 1):
            a = (sway * math.sin(2 * math.pi * f / frames) if sway else 2 * math.pi * f / frames) + phase
            px, py, pz = _project(x, y, z, a, tilt)
            near = max(0.0, min(1.0, (1 - pz) / 2))  # 1 = nearest
            xs.append(cx + px * scale)
            ys.append(cy + py * scale)
            rs.append(rmin + (rmax - rmin) * near)
            os_.append(0.18 + 0.82 * near)
        col = color2 if (color2 and i % 3 == 0) else color
        out.append(
            f'<circle fill="{col}">'
            f'<animate attributeName="cx" values="{_vals(xs)}" dur="{dur}s" repeatCount="indefinite"/>'
            f'<animate attributeName="cy" values="{_vals(ys)}" dur="{dur}s" repeatCount="indefinite"/>'
            f'<animate attributeName="r" values="{_vals(rs, "{:.2f}")}" dur="{dur}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="{_vals(os_, "{:.2f}")}" dur="{dur}s" repeatCount="indefinite"/>'
            "</circle>"
        )
    return "".join(out)


def spin_edges(points, edges, cx, cy, scale, color, dur=14, frames=30, tilt=0.38, width=1.2):
    out = []
    for i, j in edges:
        cols = {k: [] for k in ("x1", "y1", "x2", "y2", "o")}
        for f in range(frames + 1):
            a = 2 * math.pi * f / frames
            ax, ay, az = _project(*points[i], a, tilt)
            bx, by, bz = _project(*points[j], a, tilt)
            cols["x1"].append(cx + ax * scale)
            cols["y1"].append(cy + ay * scale)
            cols["x2"].append(cx + bx * scale)
            cols["y2"].append(cy + by * scale)
            cols["o"].append(0.12 + 0.5 * max(0.0, min(1.0, (1 - (az + bz) / 2) / 2)))
        anim = "".join(
            f'<animate attributeName="{"opacity" if k == "o" else k}" values="{_vals(v, "{:.2f}" if k == "o" else "{:.1f}")}" dur="{dur}s" repeatCount="indefinite"/>'
            for k, v in cols.items()
        )
        out.append(f'<line stroke="{color}" stroke-width="{width}">{anim}</line>')
    return "".join(out)


def sphere_points(n, seed=1, inner=0.25):
    rnd = _random.Random(seed)
    pts = []
    for i in range(n):
        yy = 1 - (i / (n - 1)) * 2
        r = math.sqrt(1 - yy * yy)
        th = i * 2.399963229728653
        k = 1.0 if rnd.random() > inner else rnd.uniform(0.35, 0.85)
        pts.append((math.cos(th) * r * k, yy * k, math.sin(th) * r * k))
    return pts


def heart_points(n, seed=2):
    rnd = _random.Random(seed)
    pts = []
    for _ in range(n):
        t = rnd.uniform(0, 2 * math.pi)
        k = math.sqrt(rnd.random()) if rnd.random() < 0.55 else 1.0
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        z = 9 * math.sqrt(max(0.0, 1 - k * k)) * rnd.uniform(-1, 1)
        pts.append((x * k / 17, -(y * k + 2) / 17, z / 17))
    return pts


def torus_points(n, R=0.8, r=0.22, seed=3):
    rnd = _random.Random(seed)
    pts = []
    for i in range(n):
        u = 2 * math.pi * i / n
        v = rnd.uniform(0, 2 * math.pi)
        pts.append(((R + r * math.cos(v)) * math.cos(u), r * math.sin(v), (R + r * math.cos(v)) * math.sin(u)))
    return pts


def iso(x, y, z=0.0, ox=0.0, oy=0.0, s=1.0):
    """Isometric projection of a ground-plane point (x, y) at height z."""
    return ox + (x - y) * 0.866 * s, oy + (x + y) * 0.5 * s - z * s


# ---------------------------------------------------------------------------
# header
# ---------------------------------------------------------------------------


SPHERE_CX = 650


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
  <radialGradient id="sphereGlow"><stop offset="0" stop-color="#4c8dff" stop-opacity="0.28"/><stop offset="1" stop-color="#4c8dff" stop-opacity="0"/></radialGradient>
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

    <text x="60" y="116" font-size="22" fill="{INK_2}">Hi, I'm</text>
    <text x="56" y="192" font-size="78" font-weight="800" letter-spacing="-2" fill="url(#name)">{escape(NAME)}</text>
    <text x="60" y="230" font-size="22" font-weight="600" fill="{INK}">{escape(TAGLINE)}</text>
    <text x="60" y="260" font-size="16" fill="{INK_3}">{escape(SUBLINE)}</text>

    <g aria-hidden="true">
      <circle cx="{SPHERE_CX}" cy="150" r="98" fill="url(#sphereGlow)"/>
      {spin_cloud(sphere_points(130), SPHERE_CX, 150, 82, "#7fb2ff", color2="#7fe8c4", dur=16)}
    </g>
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
        <text x="40" y="88"><tspan fill="#7fb2ff">"role"</tspan><tspan fill="{INK_3}">: </tspan><tspan fill="#7ff0c4">"SWE + AI/ML"</tspan><tspan fill="{INK_3}">,</tspan></text>
        <text x="40" y="112"><tspan fill="#7fb2ff">"focus"</tspan><tspan fill="{INK_3}">: [</tspan><tspan fill="#7ff0c4">"LLMs"</tspan><tspan fill="{INK_3}">, </tspan><tspan fill="#7ff0c4">"Med AI"</tspan><tspan fill="{INK_3}">],</tspan></text>
        <text x="40" y="136"><tspan fill="#7fb2ff">"live_apps"</tspan><tspan fill="{INK_3}">: </tspan><tspan fill="#ffb86b">4</tspan><tspan fill="{INK_3}">,</tspan></text>
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
    if kind == "graph3d":
        rnd = _random.Random(11)
        nodes = [(rnd.uniform(-1, 1), rnd.uniform(-0.8, 0.8), rnd.uniform(-1, 1)) for _ in range(13)]
        edges = []
        for i, p in enumerate(nodes):  # connect each node to its two nearest neighbours
            near = sorted(range(len(nodes)), key=lambda j: sum((p[k] - nodes[j][k]) ** 2 for k in range(3)))[1:3]
            edges += [(i, j) for j in near if (j, i) not in edges]
        return spin_edges(nodes, edges, 398, 118, 50, a, dur=12) + spin_cloud(
            nodes, 398, 118, 50, a, color2=b, dur=12, rmin=2.2, rmax=5.5)
    if kind == "ring3d":
        return (
            f'<circle cx="398" cy="118" r="10" fill="{b}" opacity="0.85">'
            f'<animate attributeName="r" values="8;13;8;8" dur="0.9s" repeatCount="indefinite"/></circle>'
            + spin_cloud(torus_points(96), 398, 118, 62, a, color2=b, dur=9, tilt=1.0, rmin=0.9, rmax=2.6)
        )
    if kind == "iso_bars":
        out = []
        heights = [[16, 22, 18, 26], [20, 28, 24, 46], [14, 18, 32, 22]]
        for r_, row in enumerate(heights):
            for c_, hgt in enumerate(row):
                bx, by = iso(c_ * 22, r_ * 22, 0, 392, 96, 1.0)
                col = "#ff6b6b" if hgt >= 50 else a
                w2 = 6.9  # half-width of the prism's top diamond
                top = f"M0,{-hgt} l{w2},4 l-{w2},4 l-{w2},-4 Z"
                left = f"M-{w2},{-hgt + 4} l{w2},4 v{hgt} l-{w2},-4 Z"
                right = f"M{w2},{-hgt + 4} l-{w2},4 v{hgt} l{w2},-4 Z"
                d = 1.8 + (r_ * 4 + c_) * 0.17
                out.append(
                    f'<g transform="translate({bx:.1f} {by + 8:.1f})"><g>'
                    f'<animateTransform attributeName="transform" type="scale" values="1 0.55;1 1;1 0.75;1 0.55" dur="{d:.2f}s" repeatCount="indefinite"/>'
                    f'<path d="{left}" fill="{col}" fill-opacity="0.55"/><path d="{right}" fill="{col}" fill-opacity="0.8"/>'
                    f'<path d="{top}" fill="{col}"/></g></g>'
                )
        return "".join(out)
    if kind == "iso_route":
        out = []
        S, O = 15, (398, 78)
        for k in range(6):  # street grid on a tilted plane
            x0, y0 = iso(k * S, 0, 0, *O)
            x1, y1 = iso(k * S, 5 * S, 0, *O)
            out.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{a}" stroke-opacity="0.22"/>')
            x0, y0 = iso(0, k * S, 0, *O)
            x1, y1 = iso(5 * S, k * S, 0, *O)
            out.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{a}" stroke-opacity="0.22"/>')
        for gx, gy, hgt in [(0, 0, 18), (3, 0, 26), (0, 3, 14), (3, 3, 20), (1.2, 1.2, 10)]:  # buildings
            cx, cy = iso(gx * S + S / 2, gy * S + S / 2, 0, *O)
            w2 = 8
            out.append(
                f'<g transform="translate({cx:.1f} {cy:.1f})" opacity="0.9">'
                f'<path d="M-{w2},-{hgt} l{w2},4.6 v{hgt} l-{w2},-4.6 Z" fill="#2a3352"/>'
                f'<path d="M{w2},-{hgt} l-{w2},4.6 v{hgt} l{w2},-4.6 Z" fill="#36416a"/>'
                f'<path d="M0,-{hgt + 4.6} l{w2},4.6 l-{w2},4.6 l-{w2},-4.6 Z" fill="#46548a"/></g>'
            )
        route = [(0, 2), (2, 2), (2, 5), (5, 5)]
        pts = [iso(x * S, y * S, 0, *O) for x, y in route]
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        out.append(f'<path d="{d}" fill="none" stroke="{a}" stroke-width="3" stroke-linejoin="round" stroke-dasharray="3 5"/>')
        for x, y in (pts[0], pts[-1]):
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="{BG_A}" stroke="{a}" stroke-width="2.2"/>')
        out.append(
            f'<g><rect x="-6" y="-4" width="12" height="8" rx="2" fill="{b}"/>'
            f'<animateMotion dur="5s" repeatCount="indefinite" path="{d}"/></g>'
        )
        return "".join(out)
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


ABOUT = [
    ("#ff5c8a", "Most recently", "ML Engineer Intern at Aventusoft (2025–26): ECG deep learning for arrhythmia classification and PQRST detection, shipped to TensorFlow Lite and AWS SageMaker."),
    ("#4c8dff", "Now building", "LeaveNow, a real-time bus planner for Gainesville; LLM observability (Spanscope); RAG over codebases (CodeAtlas); and offline voice control (SayWatt)."),
    ("#2fe0a0", "Learning", "LLM inference and serving, Model Context Protocol, and event-driven systems at scale."),
    ("#9085e9", "Ask me about", "ECG signals, medical imaging, RAG and search, LLM evaluation, and deploying models to cloud and edge."),
    ("#ffb86b", "Fun fact", "From automating 120+ Salesforce test workflows to AI that detects heart conditions with 94% accuracy."),
]
ABOUT_INTRO = "I build production-minded AI systems: LLM and retrieval apps, evaluation and observability tools, and deep learning for medical signals."


def _wrap(text, width):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        if len(cur) + len(wd) + 1 > width:
            lines.append(cur)
            cur = wd
        else:
            cur = f"{cur} {wd}".strip()
    return lines + [cur]


def about() -> str:
    w = 1200
    rows, y = [], 104
    for color, label, text in ABOUT:
        lines = _wrap(text, 84)
        rows.append(f'<rect x="60" y="{y - 13}" width="10" height="10" rx="3" fill="{color}"/>')
        rows.append(f'<text x="84" y="{y - 3}" font-size="15" font-weight="700" fill="{INK}">{escape(label)}</text>')
        for k, line in enumerate(lines):
            rows.append(f'<text x="220" y="{y - 3 + k * 21}" font-size="15" fill="{INK_2}">{escape(line)}</text>')
        y += 21 * len(lines) + 16
    h = max(y + 10, 380)
    body = f"""
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG_A}"/><stop offset="1" stop-color="{BG_B}"/></linearGradient>
  <radialGradient id="heartGlow"><stop offset="0" stop-color="#ff5c8a" stop-opacity="0.35"/><stop offset="1" stop-color="#ff5c8a" stop-opacity="0"/></radialGradient>
</defs>
<rect width="{w}" height="{h}" rx="20" fill="url(#bg)"/>
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="20" fill="none" stroke="#ffffff" stroke-opacity="0.08"/>
<g font-family="{SANS}">
  <text x="60" y="58" font-size="17" fill="{INK}">{escape(ABOUT_INTRO)}</text>
  {"".join(rows)}
</g>
<g aria-hidden="true">
  <circle cx="1060" cy="{h / 2:.0f}" r="105" fill="url(#heartGlow)">
    <animate attributeName="r" values="95;120;95;95" dur="0.9s" repeatCount="indefinite"/>
  </circle>
  {spin_cloud(heart_points(170), 1060, h / 2 - 6, 92, "#ff5c8a", color2="#ffb0c6", dur=8, tilt=0.15, rmin=0.9, rmax=2.8, sway=0.9)}
</g>"""
    return svg(w, h, body, "About me: " + ABOUT_INTRO + " " + " ".join(f"{l}: {t}" for _, l, t in ABOUT))


def main() -> None:
    OUT.mkdir(exist_ok=True)
    files = {
        "header.svg": header(),
        "about.svg": about(),
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
